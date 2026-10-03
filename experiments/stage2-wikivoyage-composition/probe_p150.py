#!/usr/bin/env python3
"""Second resolver: do the regions' own Wikidata items list official units through P150? Issue #28.

Run after run.py, from the repository root: python3 experiments/stage2-wikivoyage-composition/probe_p150.py
"""
from __future__ import annotations

import csv
import json
import sys
import time
import urllib.parse
import urllib.request
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
import run  # noqa: E402

CACHE = ROOT / "cache" / "wikidata-p150.json"


def main() -> int:
    pages = json.loads((run.SURVEY / "cache" / "wikivoyage.json").read_text())
    with (run.SURVEY / "inputs" / "wikivoyage-levels.csv").open(newline="") as handle:
        title = {r["iso"]: r["page"] for r in csv.DictReader(handle)}
    codes = json.loads(run.CACHE.read_text())
    own: dict[tuple[str, str], list[str]] = {}
    for iso in run.COUNTRIES:
        shapes = run.titled_shapes(pages.get(title[iso]))
        for name in run.region_names(pages.get(title[iso])):
            ids = [q for q in shapes.get(name, []) if not codes.get(q)]  # ids that are not official units
            if ids:
                own[(iso, name)] = ids
    cache = json.loads(CACHE.read_text()) if CACHE.exists() else {}
    todo = sorted({q for ids in own.values() for q in ids} - cache.keys())
    for i in range(0, len(todo), 50):
        query = urllib.parse.urlencode({"action": "wbgetentities", "ids": "|".join(todo[i:i + 50]), "props": "claims", "format": "json"})
        request = urllib.request.Request(f"https://www.wikidata.org/w/api.php?{query}", headers={"User-Agent": run.AGENT})
        with urllib.request.urlopen(request) as response:
            entities = json.load(response).get("entities", {})
        for qid in todo[i:i + 50]:
            claims = entities.get(qid, {}).get("claims", {}).get("P150", [])
            cache[qid] = [c["mainsnak"]["datavalue"]["value"]["id"] for c in claims if c["mainsnak"].get("datavalue")]
        time.sleep(1)
    CACHE.write_text(json.dumps(cache, sort_keys=True))
    per = defaultdict(lambda: [0, 0])
    for (iso, _), ids in sorted(own.items()):
        per[iso][0] += 1
        per[iso][1] += any(cache[q] for q in ids)
    with (ROOT / "outputs" / "p150.csv").open("w", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(["iso", "regions_drawn_from_own_item", "of_those_with_p150"])
        for iso in run.COUNTRIES:
            if iso in per:
                writer.writerow([iso, *per[iso]])
                print(iso, *per[iso])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
