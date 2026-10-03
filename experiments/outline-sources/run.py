#!/usr/bin/env python3
"""Which ready-made outlines exist for the regions of the Stage 1 list (Q013). Coverage count only; no geometry.

Each region is tied to a Wikidata item, preferably through an identifier a dataset publishes (a Natural Earth
feature's WIKIDATAID, the register's wikidata_id), otherwise by a name search whose answer is recorded in
inputs/name_ties.csv for review. For each item the run reads its OpenStreetMap relation (P402), GADM id (P8714)
and ISO 3166-2 code (P300), and whether a Natural Earth 10m admin-0 or admin-1 feature carries it.

Run from the repository root: python3 experiments/outline-sources/run.py
"""
from __future__ import annotations

import csv
import hashlib
import json
import sys
import time
import urllib.parse
import urllib.request
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[1]
DRAFT_CACHE = REPO / "experiments" / "stage1-world-draft" / "cache"
NE_ADMIN1 = {"url": "https://raw.githubusercontent.com/nvkelso/natural-earth-vector/v5.1.2/geojson/"
                    "ne_10m_admin_1_states_provinces.geojson", "file": "ne_10m_admin_1_states_provinces.geojson"}
WIKIDATA = "https://www.wikidata.org/w/api.php"
AGENT = "ctr-outline-sources/0.1 (https://github.com/uncovering-world/travel-regions-extraction)"
PROPS = {"P402": "osm_relation", "P8714": "gadm_id", "P300": "iso_3166_2"}


def read(path: Path) -> list[dict]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def api(params: dict) -> dict:
    url = WIKIDATA + "?" + urllib.parse.urlencode({**params, "format": "json", "maxlag": 5})
    for attempt in range(8):
        time.sleep(0.4)
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": AGENT}), timeout=60) as r:
                data = json.load(r)
            if data.get("error", {}).get("code") == "maxlag":
                raise TimeoutError("maxlag")
            return data
        except Exception as error:  # 429, 5xx, maxlag, network: back off and retry
            wait = 5 * 2 ** attempt
            print(f"  wikidata: {error}; waiting {wait}s", file=sys.stderr)
            time.sleep(wait)
    raise RuntimeError("Wikidata did not answer")


def ne(name: str, url: str | None = None) -> list[dict]:
    path = DRAFT_CACHE / name if (DRAFT_CACHE / name).exists() else ROOT / "cache" / name
    if not path.exists():
        path.parent.mkdir(exist_ok=True)
        with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": AGENT}), timeout=300) as r:
            path.write_bytes(r.read())
    data = path.read_bytes()
    print(f"  {name}: sha256 {hashlib.sha256(data).hexdigest()}", file=sys.stderr)
    return [f["properties"] for f in json.loads(data)["features"]]


def main() -> None:
    regions = read(REPO / "experiments" / "stage1-list" / "outputs" / "regions.csv")
    links = {r["area_id"]: r for r in read(REPO / "experiments" / "stage1-list" / "inputs" / "links.csv")}
    register = {r["area_id"]: r for r in read(REPO / "data" / "disputed-areas" / "areas.csv")}
    census = {r["id"]: r for r in read(REPO / "experiments" / "stage1-world-draft" / "inputs" / "crw_scopes.csv")}
    admin0 = ne("ne_10m_admin_0_map_units.geojson") + ne("ne_10m_admin_0_countries.geojson")
    disputed = ne("ne_10m_admin_0_disputed_areas.geojson")
    admin1 = ne(NE_ADMIN1["file"], NE_ADMIN1["url"])
    by_iso: dict[str, str] = {}
    for p in admin0:
        for code in (p.get("ISO_A2"), p.get("ISO_A2_EH")):
            if code and code != "-99" and p.get("WIKIDATAID"):
                by_iso.setdefault(code, p["WIKIDATAID"])
    by_neid = {str(p["NE_ID"]): p.get("WIKIDATAID") or "" for p in disputed + admin0}
    small_names = {p.get("NAME"): str(p["NE_ID"]) for p in disputed}
    ne_items = {p.get("WIKIDATAID") for p in admin0 + disputed if p.get("WIKIDATAID")}
    admin1_items = {p.get("wikidataid") for p in admin1 if p.get("wikidataid")}

    ties_path = ROOT / "inputs" / "name_ties.csv"
    name_ties = {r["region"]: r for r in read(ties_path)} if ties_path.exists() else {}
    rows = []
    for r in regions:
        rid, item, how = r["id"], "", ""
        if r["basis"].startswith("ISO"):
            item, how = by_iso.get(rid, ""), "Natural Earth admin-0 feature by ISO code"
        elif rid.startswith("area/"):
            area = rid[5:]
            link = links.get(area, {})
            cell = link.get("registry_cell", "")
            neid = cell.rsplit("#", 1)[1] if "#" in cell else small_names.get(link.get("small_feature", ""), "")
            if register.get(area, {}).get("wikidata_id"):
                item, how = register[area]["wikidata_id"], "register wikidata_id"
            elif neid and by_neid.get(neid):
                item, how = by_neid[neid], "Natural Earth disputed-area feature"
        elif not rid.startswith("rule/") and "#" in rid:
            item, how = by_neid.get(rid.rsplit("#", 1)[1], ""), "Natural Earth disputed-area feature"
        if not item:
            if rid not in name_ties:
                name = census[rid[5:]]["name"] if rid.startswith("rule/") else r["name"]
                found = api({"action": "wbsearchentities", "search": name.split(" (")[0], "language": "en",
                             "type": "item", "limit": 1}).get("search", [])
                name_ties[rid] = {"region": rid, "searched": name.split(" (")[0],
                                  "item": found[0]["id"] if found else "",
                                  "label": found[0].get("label", "") if found else "",
                                  "description": found[0].get("description", "") if found else "", "reviewed": ""}
            item = name_ties[rid]["item"]
            how = "name search, reviewed" if name_ties[rid]["reviewed"] else "name search (to be reviewed)"
        rows.append({"region": rid, "name": r["name"], "basis": r["basis"].split(":")[0].split(";")[0],
                     "item": item, "tied_by": how})

    with ties_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["region", "searched", "item", "label", "description", "reviewed"],
                                lineterminator="\n")
        writer.writeheader()
        writer.writerows(sorted(name_ties.values(), key=lambda x: x["region"]))

    claims: dict[str, dict] = {}
    items = sorted({r["item"] for r in rows if r["item"]})
    for i in range(0, len(items), 50):
        data = api({"action": "wbgetentities", "ids": "|".join(items[i:i + 50]), "props": "claims"})
        for qid, entity in data.get("entities", {}).items():
            got = {}
            for prop, field in PROPS.items():
                values = [c["mainsnak"].get("datavalue", {}).get("value") for c in entity.get("claims", {}).get(prop, [])]
                got[field] = " ".join(str(v) for v in values if v)
            claims[qid] = got
    for r in rows:
        c = claims.get(r["item"], {})
        r.update({field: c.get(field, "") for field in PROPS.values()})
        r["natural_earth"] = ("admin-0" if r["item"] in ne_items else "admin-1" if r["item"] in admin1_items else "")
        sources = [s for s, ok in (("Natural Earth", r["natural_earth"]), ("GADM", r["gadm_id"]),
                                   ("OpenStreetMap", r["osm_relation"])) if ok]
        r["outline_sources"] = " + ".join(sources) or "none"

    (ROOT / "outputs").mkdir(exist_ok=True)
    with (ROOT / "outputs" / "regions.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    by_basis: dict[str, Counter] = {}
    for r in rows:
        by_basis.setdefault(r["basis"], Counter())[r["outline_sources"]] += 1
    summary = {
        "regions": len(rows),
        "tied_by": dict(Counter(r["tied_by"] for r in rows).most_common()),
        "no_item": [r["region"] for r in rows if not r["item"]],
        "outline_sources": dict(Counter(r["outline_sources"] for r in rows).most_common()),
        "by_basis": {b: dict(c.most_common()) for b, c in sorted(by_basis.items())},
        "without_natural_earth_or_gadm": [f"{r['region']} ({r['outline_sources']})" for r in rows
                                          if not r["natural_earth"] and not r["gadm_id"]],
    }
    (ROOT / "outputs" / "summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in summary.items() if k != "by_basis"}, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()
