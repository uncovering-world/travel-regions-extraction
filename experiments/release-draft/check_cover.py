#!/usr/bin/env python3
"""Does every GADM 4.1 row fall into exactly one region of the draft? Attributes only, no geometry.

A GADM row (the smallest unit GADM stores) belongs to a region if one of its GID ancestors (or itself) is an
`include` row of that region and none is an `exclude` row of it. Custom geometries are not checked here.
Run from the repository root: python3 experiments/release-draft/check_cover.py
"""
import csv
import json
import os
import sqlite3
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent
GADM = Path(os.environ.get("GADM_GPKG", ROOT.parents[2] / "track-your-regions" / "deployment" / "gadm_410.gpkg"))
rows = list(csv.DictReader((ROOT / "release" / "membership.csv").open()))
inc, exc = {}, {}
for r in rows:
    if r["source"] == "GADM 4.1":
        (inc if r["role"] == "include" else exc).setdefault(r["unit"], set()).add(r["region_id"])
db = sqlite3.connect(f"file:{GADM}?mode=ro", uri=True)
result, examples = Counter(), {}
for gids in db.execute("select GID_0, GID_1, GID_2, GID_3, GID_4, GID_5, COUNTRY, NAME_1 from gadm_410"):
    chain = [g for g in gids[:6] if g]
    regions = set()
    for g in chain:
        regions |= inc.get(g, set())
    for g in chain:
        regions -= exc.get(g, set())
    key = "none" if not regions else "one" if len(regions) == 1 else "several"
    result[key] += 1
    if key != "one":
        examples.setdefault((key, chain[0], tuple(sorted(regions))), (gids[6], gids[7], chain[-1]))
summary = {"gadm_rows": sum(result.values()), **result,
           "problems": [{"kind": k[0], "gid_0": k[1], "regions": list(k[2]), "example": v} for k, v in sorted(examples.items())]}
(ROOT / "release" / "cover_check.json").write_text(json.dumps(summary, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
print(json.dumps(summary, indent=1, ensure_ascii=False)[:3000])
