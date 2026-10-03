#!/usr/bin/env python3
"""Stage 2 scale survey: NomadMania regions per country against ISO 3166-2 tiers. Issue #28.

Run from the repository root: python3 experiments/stage2-scale-survey/run.py
"""
from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent
FACTOR = 1.5  # "close to a tier" means within this factor


def read(name: str) -> list[dict]:
    with (ROOT / "inputs" / name).open(newline="") as handle:
        return list(csv.DictReader(handle))


def relation(reference: int, top: int, total: int) -> str:
    """Where the reference count sits relative to the official tiers of one country."""
    def close(a: int, b: int) -> bool:
        return b > 0 and max(a, b) / min(a, b) <= FACTOR
    if reference == 1:
        return "single_region"
    if top == 0:
        return "no_official_units"
    if close(reference, top):
        return "matches_top_tier"
    if total != top and close(reference, total):
        return "matches_all_tiers"
    if reference < top:
        return "groups_top_tier"
    if total != top and reference < total:
        return "between_tiers"
    return "descends_below"


def main() -> int:
    top, total = Counter(), Counter()
    for row in read("iso3166-2.csv"):
        country = row["code"][:2]
        total[country] += 1
        if not row["parent"]:
            top[country] += 1
    rows = []
    for row in read("nomadmania-counts.csv"):
        if not row["iso"]:
            continue  # no ISO 3166-1 entry (de facto states, poles)
        n = int(row["n_regions"])
        rows.append({"iso": row["iso"], "country": row["country"], "reference": n, "top_tier": top[row["iso"]],
                     "all_tiers": total[row["iso"]], "relation": relation(n, top[row["iso"]], total[row["iso"]])})
    rows.sort(key=lambda r: (-r["reference"], r["iso"]))
    multi = [r for r in rows if r["reference"] > 1]
    by_relation = Counter(r["relation"] for r in rows)
    weighted = Counter()
    for r in rows:
        weighted[r["relation"]] += r["reference"]
    summary = {
        "countries": len(rows), "countries_with_more_than_one_region": len(multi),
        "reference_regions": sum(r["reference"] for r in rows),
        "top_tier_units_same_countries": sum(r["top_tier"] for r in rows),
        "top_tier_units_world": sum(top.values()), "all_units_world": sum(total.values()),
        "countries_by_relation": dict(sorted(by_relation.items())),
        "reference_regions_by_relation": dict(sorted(weighted.items())),
        "share_of_multi_region_countries_matching_a_tier": round(
            sum(r["relation"] in ("matches_top_tier", "matches_all_tiers") for r in multi) / len(multi), 3),
    }
    out = ROOT / "outputs"
    out.mkdir(exist_ok=True)
    (out / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    with (out / "countries.csv").open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
