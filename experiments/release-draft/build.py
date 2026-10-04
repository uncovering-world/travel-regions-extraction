#!/usr/bin/env python3
"""Build a draft release package (R059) from the Stage 1 list, the GADM binding and the custom geometries.

Not a release: the inputs are experiment outputs and several tables in inputs/ are reviewed by hand.
Writes release/ next to this file: canon.json (TYR's import tree), regions.csv, membership.csv, geometry/,
manifest.json, and gaps.csv for what could not be filled.

Membership semantics: a region is the union of its `include` rows minus its `exclude` rows; rows of a custom
geometry (Natural Earth feature or a file in data/custom-geometries) take precedence over GADM units, i.e. land in
a custom geometry belongs to the region the geometry is assigned to, whatever GADM unit it lies in.

Run from the repository root: python3 experiments/release-draft/build.py
"""
from __future__ import annotations

import csv
import hashlib
import io
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[1]
OUT = ROOT / "release"
GADM = "GADM 4.1"
NE = "Natural Earth 5.1.2 disputed areas"
CUSTOM = "custom geometry"
POVS = ["AR", "BD", "BR", "CN", "DE", "EG", "ES", "FR", "GB", "GR", "ID", "IL", "IN", "IT", "JP", "KO",
        "MA", "NL", "NP", "PK", "PL", "PS", "PT", "RU", "SA", "SE", "TR", "TW", "UA", "US", "VN"]
INPUTS = [
    "experiments/stage1-list/outputs/regions.csv",
    "experiments/gadm-binding/outputs/bindings.csv",
    "experiments/outline-sources/outputs/regions.csv",
    "data/entry-rules/census.csv",
    "experiments/release-draft/inputs/attribution.csv",
    "experiments/release-draft/inputs/gadm_leftovers.csv",
    "data/custom-geometries/sources.csv",
    "experiments/release-draft/inputs/pov_features.csv",
    "data/custom-geometries/sources.json",
    "docs/spec.md",
]


def read(rel: str) -> list[dict]:
    with (REPO / rel).open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict], columns: list[str]) -> None:
    buffer = io.StringIO()
    writer = csv.DictWriter(buffer, fieldnames=columns, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    path.write_text(buffer.getvalue(), encoding="utf-8")


def main() -> None:
    regions = read("experiments/stage1-list/outputs/regions.csv")
    bindings = {r["region"]: r for r in read("experiments/gadm-binding/outputs/bindings.csv")}
    items = {r["region"]: r["item"] for r in read("experiments/outline-sources/outputs/regions.csv")}
    census = {r["id"]: r for r in read("data/entry-rules/census.csv")}
    attribution = {r["region"]: r for r in read("experiments/release-draft/inputs/attribution.csv")}
    iso_names = {c["alpha_2"]: c.get("common_name", c["name"]) for c in
                 json.loads(Path("/usr/share/iso-codes/json/iso_3166-1.json").read_text())["3166-1"]}
    ids = {r["id"] for r in regions}
    gaps = []

    # regions and their country under the canon's attribution
    table = []
    for r in regions:
        rid = r["id"]
        if r["basis"].startswith("ISO"):
            country, code = iso_names.get(rid, rid), rid
        elif rid in attribution:
            code = attribution[rid]["code"]
            country = iso_names.get(code, attribution[rid]["country"])
        elif rid.startswith("rule/"):
            code = census[rid[5:]]["iso_code"]
            country = iso_names.get(code, code)
        else:
            country, code = "", ""
            gaps.append({"item": rid, "missing": "country attribution"})
        table.append({"region_id": rid, "name": r["name"], "wikidata_id": items.get(rid, ""),
                      "basis": r["basis"].split(":")[0].split(";")[0], "country": country, "country_code": code,
                      "evidence": r["evidence"], "open": r["open"]})

    # the country of each region under each Natural Earth point of view (R045): the ADM0_A3_<POV> value of the
    # Natural Earth feature that represents the region, or of its country's feature
    cache = REPO / "experiments" / "stage1-world-draft" / "cache"
    units = json.loads((cache / "ne_10m_admin_0_map_units.geojson").read_text())["features"]
    disputed = {str(f["properties"]["NE_ID"]): f["properties"] for f in
                json.loads((cache / "ne_10m_admin_0_disputed_areas.geojson").read_text())["features"]}
    by_a2 = {}
    for f in units:
        q = f["properties"]
        for code in (q.get("ISO_A2"), q.get("ISO_A2_EH")):
            if code and code != "-99":
                by_a2.setdefault(code, q)
    links = {r["area_id"]: r for r in read("experiments/stage1-list/inputs/links.csv")}
    countries_by_a3 = {f["properties"]["ADM0_A3"]: f["properties"] for f in
                       json.loads((cache / "ne_10m_admin_0_countries.geojson").read_text())["features"]}
    pov_override = {r["region"]: r["ne_feature"] for r in read("experiments/release-draft/inputs/pov_features.csv")}
    small = {r["ne_name"]: str(r["ne_id"]) for r in read("experiments/gadm-binding/outputs/disputed_points.csv")}
    for r in table:
        rid = r["region_id"]
        feature = None
        if rid.startswith("area/"):
            link = links.get(rid[5:], {})
            cell = link.get("registry_cell", "")
            if "#" in cell:
                feature = disputed.get(cell.rsplit("#", 1)[1])
            elif link.get("small_feature") in small:
                feature = disputed.get(small[link["small_feature"]])
            elif link.get("pov_feature"):
                feature = disputed.get(link["pov_feature"])
        if rid in pov_override:
            kind, _, ref = pov_override[rid].partition(":")
            feature = {"countries": countries_by_a3, "disputed": disputed, "iso": by_a2}.get(kind, {}).get(ref)
            if pov_override[rid] == "none":
                feature = None
        if feature is None and rid not in pov_override:
            feature = by_a2.get(r["country_code"] or rid)
        for pov in POVS:
            r[f"pov_{pov}"] = str(feature.get(f"ADM0_A3_{pov}", "")) if feature else ""
        if feature is None and pov_override.get(rid) != "none":
            gaps.append({"item": rid, "missing": "no Natural Earth feature for its points of view"})

    # membership: GADM units, ISO regions as GADM countries minus units bound elsewhere, custom geometries
    membership = []
    bound_elsewhere: dict[str, list[tuple[str, str]]] = {}
    for rid, b in bindings.items():
        if rid not in ids:
            continue
        for unit in b["gadm_units"].split():
            membership.append({"region_id": rid, "source": GADM, "unit": unit, "role": "include", "precedence": 2})
            if b["level"] != "GID_0" or not b["basis"].startswith("ISO"):
                bound_elsewhere.setdefault(unit.split(".")[0], []).append((unit, rid))
        if not b["gadm_units"]:
            pass
    # a unit bound to another region is cut out of every region that includes one of its GADM ancestors
    def ancestor(outer: str, inner: str) -> bool:
        stem = outer.rsplit("_", 1)[0] if "_" in outer else outer
        return inner != outer and inner.startswith(stem + ".")
    included = [m for m in membership if m["role"] == "include"]
    for row in included:
        for units in bound_elsewhere.values():
            for unit, other in units:
                if other != row["region_id"] and ancestor(row["unit"], unit):
                    membership.append({"region_id": row["region_id"], "source": GADM, "unit": unit, "role": "exclude",
                                       "precedence": 2})
    for r in read("experiments/release-draft/inputs/gadm_leftovers.csv"):
        if r["region"]:
            membership.append({"region_id": r["region"], "source": GADM, "unit": r["gid_0"], "role": "include",
                               "precedence": 2})
    # the canon's own geometries (D059, D062): files in data/custom-geometries, clipped by the consumer to the
    # substrate units of their donor regions
    for r in read("data/custom-geometries/sources.csv"):
        membership.append({"region_id": r["region"], "source": CUSTOM, "unit": r["file"], "role": "include",
                           "precedence": 1, "clip_to": r["donors"].replace(";", " ")})
    with_geometry = {m["region_id"] for m in membership if m["role"] == "include"}
    for r in table:
        if r["region_id"] not in with_geometry:
            gaps.append({"item": r["region_id"], "missing": "geometry: no GADM unit and no custom geometry"})
    unknown = sorted({m["region_id"] for m in membership} - ids)
    gaps += [{"item": u, "missing": "membership row for a region not in the list"} for u in unknown]
    membership.sort(key=lambda m: (m["region_id"], m["precedence"], m["source"], m["role"], m["unit"]))

    # TYR import tree: World -> country -> regions (a country with one region is a leaf)
    by_country: dict[str, list[dict]] = {}
    for r in table:
        by_country.setdefault(r["country"] or "No country", []).append(r)
    children = []
    for country in sorted(by_country, key=lambda c: (c == "No country", c)):
        regs = sorted(by_country[country], key=lambda r: (r["country_code"] != r["region_id"], r["name"]))
        nodes = [{"name": r["name"] if r["region_id"] != r["country_code"] else country,
                  **({"wikidataId": r["wikidata_id"]} if r["wikidata_id"] else {})} for r in regs]
        if len(nodes) == 1 and country != "No country":
            children.append(nodes[0])
        else:
            children.append({"name": "No country" if country in ("none", "No country") else country, "children": nodes})
    tree = {"name": "World", "children": children}

    OUT.mkdir(exist_ok=True)
    (OUT / "geometry").mkdir(exist_ok=True)
    for f in sorted((REPO / "data" / "custom-geometries").glob("*.geojson")):
        (OUT / "geometry" / f.name).write_bytes(f.read_bytes())
    (OUT / "canon.json").write_text(json.dumps(tree, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    write_csv(OUT / "regions.csv", sorted(table, key=lambda r: r["region_id"]),
              ["region_id", "name", "wikidata_id", "basis", "country", "country_code", "evidence", "open"]
              + [f"pov_{p}" for p in POVS])
    write_csv(OUT / "membership.csv", membership, ["region_id", "source", "unit", "role", "precedence", "clip_to"])
    write_csv(OUT / "gaps.csv", gaps, ["item", "missing"])
    manifest = {
        "release": "draft-2026-10-04", "status": "draft, not a release",
        "cutoff": "2025-12-31",
        "rules": "docs/spec.md 0.4.0-draft (D038-D061)",
        "registry": {"ISO 3166-1": "iso-codes 4.20.1", "Natural Earth": "v5.1.2"},
        "substrate": {"GADM": "4.1 (gadm_410.gpkg; unit identifiers only, no GADM geometry in this package)"},
        "membership": "a region is the union of its include rows minus its exclude rows; precedence 1 (own "
                      "geometry, clipped to the GADM units of the regions in clip_to) wins over precedence 2 (GADM units)",
        "counts": {"regions": len(table), "countries_in_tree": len(children),
                   "membership_rows": len(membership), "gaps": len(gaps)},
        "inputs": {rel: hashlib.sha256((REPO / rel).read_bytes()).hexdigest() for rel in INPUTS},
        "correspondence": "none: first draft",
    }
    (OUT / "manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(manifest["counts"]), "gaps:", [g["item"] for g in gaps])


if __name__ == "__main__":
    main()
