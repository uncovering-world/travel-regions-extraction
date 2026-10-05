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
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[1]
OUT = ROOT / "release"
GADM = "GADM 4.1"
NE = "Natural Earth 5.1.2 disputed areas"
CUSTOM = "custom geometry"
INPUTS = [
    "experiments/stage1-list/outputs/regions.csv",
    "experiments/gadm-binding/outputs/bindings.csv",
    "experiments/outline-sources/outputs/regions.csv",
    "data/entry-rules/census.csv",
    "experiments/release-draft/inputs/attribution.csv",
    "experiments/release-draft/inputs/gadm_leftovers.csv",
    "data/custom-geometries/sources.csv",
    "experiments/stage1-list/inputs/claims.csv",
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


def landless(membership: list[dict]) -> set[str]:
    """Regions none of whose GADM rows is left after their exclusions, and that have no own geometry (reads GADM)."""
    import sqlite3
    gpkg = Path(os.environ.get("GADM_GPKG", REPO.parent / "track-your-regions" / "deployment" / "gadm_410.gpkg"))
    inc, exc, own = {}, {}, set()
    for m in membership:
        if m["source"] == CUSTOM:
            own.add(m["region_id"])
        elif m["source"] == GADM:
            (inc if m["role"] == "include" else exc).setdefault(m["region_id"], set()).add(m["unit"])
    db = sqlite3.connect(f"file:{gpkg}?mode=ro", uri=True)
    empty = set()
    for rid, units in inc.items():
        if rid in own or not exc.get(rid):
            continue
        left = 0
        for unit in units:
            level = unit.count(".")                       # GID_0 for "SHN", GID_1 for "SHN.1_1", ...
            for gids in db.execute(f"select GID_0, GID_1, GID_2, GID_3, GID_4, GID_5 from gadm_410 where GID_{level} = ?", (unit,)):
                if not any(g in exc[rid] for g in gids if g):
                    left += 1
                    break
            if left:
                break
        if not left:
            empty.add(rid)
    return empty


def main() -> None:
    regions = read("experiments/stage1-list/outputs/regions.csv")
    bindings = {r["region"]: r for r in read("experiments/gadm-binding/outputs/bindings.csv")}
    items = {r["region"]: r["item"] for r in read("experiments/outline-sources/outputs/regions.csv")}
    census = {r["id"]: r for r in read("data/entry-rules/census.csv")}
    attribution = {r["region"]: r for r in read("experiments/release-draft/inputs/attribution.csv")}
    claims = {r["area_id"]: r for r in read("experiments/stage1-list/inputs/claims.csv")}

    def single(holder: str) -> bool:
        return holder not in ("", "none", "unclear") and not holder.startswith("split")
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
        elif claims.get(rid[5:], {}).get("holder") == "none":
            country, code = "none", ""                         # no single holder (R048 as amended by D055)
        elif single(claims.get(rid[5:], {}).get("holder", "")):
            # a region made by a claim goes with its holder (R050, R051); an area whose control is not yet accepted
            # goes with the party it was taken from, its last settled holder (R049)
            c = claims[rid[5:]]
            taken_from = [x for x in c["claimants"].split() if x not in c["renounced"].split()]
            code = taken_from[0] if r["country"].startswith("unsettled") and len(taken_from) == 1 else c["holder"]
            country = iso_names.get(code, code)
            if code.startswith("area/"):
                code, country = "", attribution.get(code, {}).get("country", code)
        else:
            country, code = "", ""
            gaps.append({"item": rid, "missing": "country attribution"})
        table.append({"region_id": rid, "name": r["name"], "wikidata_id": items.get(rid, ""),
                      "basis": r["basis"].split(":")[0].split(";")[0], "country": country, "country_code": code,
                      "evidence": r["evidence"], "open": r["open"]})

    # the country of each region under each party's point of view (R045 as amended by D064-D069): a party counts the
    # areas it claims and the areas it holds as its own; everywhere else its view is the canon's attribution.
    # Natural Earth's views are only a lead (D065), checked in experiments/stage1-list/outputs/natural_earth_lead.csv.
    links = {r["area_id"]: r for r in read("experiments/stage1-list/inputs/links.csv")}
    kinds = {r["area_id"]: r["kind"] for r in read("data/disputed-areas/registry.csv")}
    own: dict[str, dict[str, str]] = {}                      # region id -> {party: party} where the party counts it its own
    for area_id, c in claims.items():
        link = links.get(area_id, {})
        if link.get("iso") and link.get("basis", "").startswith("own ISO entry"):
            rid = link["iso"]                                 # a claim to a whole ISO entry
        elif link.get("part_of", "").startswith("rule/"):
            rid = link["part_of"]                             # a claim to the whole of a region made for another reason
        else:
            rid = "area/" + area_id
        if rid not in ids:
            continue
        renounced = set(c["renounced"].split())
        parties = set(c["claimants"].split()) - renounced
        holder = c["holder"]
        if single(holder) and kinds.get(area_id) != "lease_or_base" and not rid.isupper():
            parties.add(holder)
        for party in parties:
            own.setdefault(rid, {})[party] = party
    parties = sorted({p for v in own.values() for p in v})
    view_name = {p: p.split("/", 1)[1] if "/" in p else p for p in parties}
    for r in table:
        slug = r["region_id"].split("/", 1)[1] if r["region_id"].startswith("area/") else ""
        canon = r["country_code"] or ("none" if r["country"] == "none" else slug if "area/" + slug in parties else
                                     next((view_name[p] for p in parties if p.startswith("area/") and
                                           attribution.get(p, {}).get("country") == r["country"]), ""))
        for p in parties:
            mine = own.get(r["region_id"], {}).get(p)
            r[f"view_{view_name[p]}"] = view_name[mine] if mine else canon

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
                           "precedence": 1, "clip_to": r["donors"].replace(";", " "), "remnants_to": r.get("remnants_to", "")})
    # a region whose GADM units are all taken by other regions and that has no own geometry has no land: an ISO entry
    # divided entirely into entry-rule regions stays a country node in the tree, not a region of its own
    empty = landless(membership)
    if empty:
        membership = [m for m in membership if m["region_id"] not in empty]
        table = [r for r in table if r["region_id"] not in empty]
        ids -= empty
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
              + [f"view_{view_name[p]}" for p in parties])
    write_csv(OUT / "membership.csv", membership, ["region_id", "source", "unit", "role", "precedence", "clip_to", "remnants_to"])
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
