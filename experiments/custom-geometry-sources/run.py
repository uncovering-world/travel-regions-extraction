#!/usr/bin/env python3
"""Which polygon sources exist for the places GADM cannot represent (Q013). Coverage only; nothing is fetched.

inputs/places.csv lists the places of groups A (regions with no GADM unit), B (land GADM gives to another country)
and C (places GADM has no polygon for), with their Natural Earth disputed-area features. Each place's Wikidata item
comes from the Natural Earth feature's WIKIDATAID, else from the outline-source survey; the item's OpenStreetMap
relation (P402) and Commons map (P3896) are read from Wikidata.

Run from the repository root: python3 experiments/custom-geometry-sources/run.py
"""
import csv
import json
import time
import urllib.parse
import urllib.request
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[1]
AGENT = "ctr-custom-geometry/0.1 (https://github.com/uncovering-world/travel-regions-extraction)"


def api(params):
    url = "https://www.wikidata.org/w/api.php?" + urllib.parse.urlencode({**params, "format": "json"})
    for attempt in range(6):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": AGENT}), timeout=60) as r:
                return json.load(r)
        except Exception:
            time.sleep(10 * (attempt + 1))
    raise RuntimeError("Wikidata did not answer")


def main():
    ne = {str(f["properties"]["NE_ID"]): f["properties"] for f in json.loads(
        (REPO / "experiments" / "stage1-world-draft" / "cache" / "ne_10m_admin_0_disputed_areas.geojson").read_text())["features"]}
    survey = {r["region"]: r for r in csv.DictReader((REPO / "experiments" / "outline-sources" / "outputs" / "regions.csv").open())}
    places = list(csv.DictReader((ROOT / "inputs" / "places.csv").open()))
    for p in places:
        ids = p["ne_ids"].split()
        items = [ne[i].get("WIKIDATAID") for i in ids if ne.get(i, {}).get("WIKIDATAID")]
        if not items and p["place"] in survey and survey[p["place"]]["item"]:
            items = [survey[p["place"]]["item"]]
        p["wikidata"] = " ".join(items)
    claims = {}
    all_items = sorted({i for p in places for i in p["wikidata"].split()})
    for i in range(0, len(all_items), 50):
        for qid, e in api({"action": "wbgetentities", "ids": "|".join(all_items[i:i + 50]), "props": "claims"})["entities"].items():
            claims[qid] = {prop: [c["mainsnak"].get("datavalue", {}).get("value") for c in e.get("claims", {}).get(prop, [])]
                           for prop in ("P402", "P3896")}
    for p in places:
        items = p["wikidata"].split()
        p["natural_earth"] = "yes" if p["ne_ids"] else ""
        p["osm_relation"] = " ".join(str(v) for q in items for v in claims.get(q, {}).get("P402", []) if v)
        p["commons_map"] = " ".join(str(v) for q in items for v in claims.get(q, {}).get("P3896", []) if v)
        p["sources"] = " + ".join(s for s, ok in (("Natural Earth", p["natural_earth"]), ("OpenStreetMap", p["osm_relation"]),
                                                  ("Commons map", p["commons_map"])) if ok) or "none"
    with (ROOT / "outputs" / "places.csv").open("w", encoding="utf-8", newline="") as h:
        w = csv.DictWriter(h, fieldnames=list(places[0]), lineterminator="\n")
        w.writeheader()
        w.writerows(places)
    summary = {"places": len(places),
               "by_group": {g: dict(Counter(p["sources"] for p in places if p["group"] == g)) for g in "ABC"},
               "with_natural_earth": sum(1 for p in places if p["natural_earth"]),
               "no_source": [p["place"] for p in places if p["sources"] == "none"],
               "only_openstreetmap_or_commons": [p["place"] for p in places if not p["natural_earth"] and p["sources"] != "none"]}
    (ROOT / "outputs" / "summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()
