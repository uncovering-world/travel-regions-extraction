#!/usr/bin/env python3
"""Refresh the machine-read facts of the register. Deterministic for a given state of the sources.

For every area linked in areas.csv:
  natural_earth_id (one or more NE_ID values, space-separated) -> ne_* facts from the pinned Natural Earth file;
  wikidata_id -> wd_* facts from the Wikidata API (label, area P2046, population P1082, coordinates P625).
Machine facts in facts.csv are replaced wholesale; manual facts are never touched.

    python3 data/disputed-areas/refresh_machine.py --date 2026-10-03
    python3 data/disputed-areas/refresh_machine.py --suggest      # print link candidates, change nothing
Then run build.py.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import sys
import time
import urllib.parse
import urllib.request
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CACHE = ROOT / "cache"
NE_URL = "https://raw.githubusercontent.com/nvkelso/natural-earth-vector/v5.1.2/geojson/ne_10m_admin_0_disputed_areas.geojson"
NE_SHA256 = "9cafef8b7dfb6b164dc58f218f981f4ace9f716f6c03795d4c62d1ac9f3d50f5"
AGENT = "ctr-disputed-areas/0.1 (https://github.com/uncovering-world/travel-regions-extraction)"
POVS = ["AR", "BD", "BR", "CN", "DE", "EG", "ES", "FR", "GB", "GR", "ID", "IL", "IN", "IT", "JP", "KO",
        "MA", "NL", "NP", "PK", "PL", "PS", "PT", "RU", "SA", "SE", "TR", "TW", "UA", "US", "VN"]
FACT_COLUMNS = ["area_id", "field", "value", "source_ids", "read_date", "evidence", "origin"]


def natural_earth() -> dict[str, dict]:
    path = CACHE / "ne_10m_admin_0_disputed_areas.geojson"
    if not path.exists():
        CACHE.mkdir(exist_ok=True)
        with urllib.request.urlopen(NE_URL) as response:
            path.write_bytes(response.read())
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    if digest != NE_SHA256:
        print(f"WARNING: Natural Earth file sha256 {digest} differs from the recorded one", file=sys.stderr)
    return {str(f["properties"]["NE_ID"]): f for f in json.loads(path.read_text())["features"]}


def area_km2(geometry: dict) -> float:
    polygons = geometry["coordinates"] if geometry["type"] == "MultiPolygon" else [geometry["coordinates"]]
    total = 0.0
    for polygon in polygons:
        ring = polygon[0]
        twice = sum((x1 * y2 - x2 * y1) * math.cos(math.radians((y1 + y2) / 2)) for (x1, y1), (x2, y2) in zip(ring, ring[1:]))
        total += abs(twice) / 2
    return total * 111.32 ** 2


def ne_facts(ids: list[str], features: dict[str, dict]) -> dict[str, str]:
    props = [features[i]["properties"] for i in ids]
    tally: dict[str, int] = {}
    for pov in POVS:
        key = "+".join(sorted({str(p[f"ADM0_A3_{pov}"]) for p in props}))
        tally[key] = tally.get(key, 0) + 1
    return {
        "ne_name": "; ".join(p["NAME"] for p in props),
        "ne_type": "; ".join(sorted({p["TYPE"] for p in props})),
        "ne_note": "; ".join(sorted({p["NOTE_BRK"] for p in props if p.get("NOTE_BRK")})),
        "ne_area_km2": str(round(sum(area_km2(features[i]["geometry"]) for i in ids))),
        "ne_attribution": " ".join(f"{k}:{v}" for k, v in sorted(tally.items(), key=lambda kv: (-kv[1], kv[0]))),
    }


def wikidata(ids: list[str]) -> dict[str, dict[str, str]]:
    out: dict[str, dict[str, str]] = {}
    for i in range(0, len(ids), 50):
        query = urllib.parse.urlencode({"action": "wbgetentities", "ids": "|".join(ids[i:i + 50]), "props": "labels|claims",
                                        "languages": "en", "format": "json"})
        request = urllib.request.Request(f"https://www.wikidata.org/w/api.php?{query}", headers={"User-Agent": AGENT})
        with urllib.request.urlopen(request) as response:
            entities = json.load(response)["entities"]
        for qid in ids[i:i + 50]:
            entity = entities.get(qid, {})

            def best(prop: str):
                claims = [c for c in entity.get("claims", {}).get(prop, []) if c["mainsnak"].get("datavalue") and c.get("rank") != "deprecated"]
                claims.sort(key=lambda c: c.get("rank") != "preferred")
                return claims[0]["mainsnak"]["datavalue"]["value"] if claims else None

            facts = {"wd_label": entity.get("labels", {}).get("en", {}).get("value", "")}
            area, population, coordinates = best("P2046"), best("P1082"), best("P625")
            if area and area.get("unit", "").endswith("Q712226"):  # square kilometre
                facts["wd_area_km2"] = area["amount"].lstrip("+")
            if population:
                facts["wd_population"] = population["amount"].lstrip("+")
            if coordinates:
                facts["wd_coordinates"] = f"{coordinates['latitude']:.4f} {coordinates['longitude']:.4f}"
            out[qid] = {k: v for k, v in facts.items() if v}
        time.sleep(1)
    return out


def suggest(areas: list[dict], features: dict[str, dict]) -> None:
    by_name: dict[str, list[str]] = {}
    for ne_id, feature in features.items():
        by_name.setdefault(feature["properties"]["NAME"].lower(), []).append(ne_id)
    for area in areas:
        if not area["natural_earth_id"]:
            hits = by_name.get(area["name"].lower(), [])
            if len(hits) == 1:
                print(f"{area['area_id']}: Natural Earth candidate {hits[0]} (exact name)")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--date", type=date.fromisoformat, help="read date to record for the refreshed facts")
    parser.add_argument("--suggest", action="store_true")
    args = parser.parse_args()
    with (ROOT / "areas.csv").open(newline="") as handle:
        areas = list(csv.DictReader(handle))
    features = natural_earth()
    if args.suggest:
        suggest(areas, features)
        return 0
    if not args.date:
        parser.error("--date is required when refreshing")
    with (ROOT / "facts.csv").open(newline="") as handle:
        facts = [f for f in csv.DictReader(handle) if f["origin"] == "manual"]
    labels = wikidata(sorted({a["wikidata_id"] for a in areas if a["wikidata_id"]}))
    for area in areas:
        machine: dict[str, tuple[str, str]] = {}
        ne_ids = area["natural_earth_id"].split()
        unknown = [i for i in ne_ids if i not in features]
        if unknown:
            print(f"{area['area_id']}: Natural Earth id not found: {unknown}", file=sys.stderr)
            return 1
        if ne_ids:
            machine |= {k: (v, "NE") for k, v in ne_facts(ne_ids, features).items() if v}
        machine |= {k: (v, "WD") for k, v in labels.get(area["wikidata_id"], {}).items()}
        facts += [{"area_id": area["area_id"], "field": k, "value": v, "source_ids": s, "read_date": args.date.isoformat(),
                   "evidence": "machine", "origin": "machine"} for k, (v, s) in machine.items()]
    order = {a["area_id"]: n for n, a in enumerate(areas)}
    facts.sort(key=lambda f: (order[f["area_id"]], f["origin"] == "machine"))  # stable: manual rows keep their order
    with (ROOT / "facts.csv").open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FACT_COLUMNS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(facts)
    print(f"machine facts for {sum(bool(a['natural_earth_id']) for a in areas)} Natural Earth links and {len(labels)} Wikidata links")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
