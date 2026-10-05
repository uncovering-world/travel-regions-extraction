#!/usr/bin/env python3
"""Which N separates pressed from dormant paper claims (D070, Q021)? See README.md.

Reads inputs/steps.csv (the claimants' official steps, one row per step) and the register; for each claim of kind
paper_claim with resident civilians (or residents unknown), and for each N, decides at every yearly release from 2005
to 2025 whether the claim has a step in the N years up to that release, and counts how often its status changes.
Writes outputs/claims.csv and outputs/summary.json. Run from the repository root:
    python3 experiments/claim-activity/run.py
"""
from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[1]
NS = [3, 5, 10, 15, 20]
RELEASES = list(range(2005, 2026))


def read(path: Path) -> list[dict]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def main() -> None:
    registry = read(REPO / "data" / "disputed-areas" / "registry.csv")
    population = sorted(r["area_id"] for r in registry if r["kind"] == "paper_claim" and r["inhabited"] in ("yes", ""))
    names = {r["area_id"]: r["name"] for r in registry}
    steps = read(ROOT / "inputs" / "steps.csv")
    years: dict[str, set[int]] = {a: set() for a in population}
    kinds: dict[str, set[str]] = {a: set() for a in population}
    for s in steps:
        if s["area_id"] in years and s.get("use", "yes") == "yes":
            years[s["area_id"]].add(int(s["date"][:4]))
            kinds[s["area_id"]].add(s["kind"])

    rows, flicker = [], {n: 0 for n in NS}
    regions_2025 = {n: 0 for n in NS}
    flickering = {n: [] for n in NS}
    for a in population:
        ys = sorted(years[a])
        after = [y for y in ys if y >= 2000]
        gaps = [b - a_ for a_, b in zip(after, after[1:])]
        row = {"area_id": a, "name": names[a], "steps": len([s for s in steps if s["area_id"] == a]),
               "years_with_a_step": " ".join(map(str, ys)), "latest": ys[-1] if ys else "",
               "longest_gap_since_2000": max(gaps) if gaps else "", "kinds": " ".join(sorted(kinds[a]))}
        for n in NS:
            status = [any(y - n < x <= y for x in ys) for y in RELEASES]
            changes = sum(1 for p, q in zip(status, status[1:]) if p != q)
            row[f"region_2025_N{n}"] = "yes" if status[-1] else "no"
            row[f"changes_N{n}"] = changes
            flicker[n] += changes
            regions_2025[n] += status[-1]
            if changes:
                flickering[n].append(a)
        rows.append(row)

    # the second test: a claim is pressed at a release if it has steps in at least K distinct years of the last N
    frequency = {}
    for n in NS:
        for k in (1, 2, 3, 4):
            pressed_2025, changes_total, changing, dormant = 0, 0, [], []
            for a in population:
                ys = years[a]
                status = [sum(1 for x in ys if y - n < x <= y) >= k for y in RELEASES]
                changes = sum(1 for p_, q in zip(status, status[1:]) if p_ != q)
                changes_total += changes
                pressed_2025 += status[-1]
                if changes:
                    changing.append(a)
                if not status[-1]:
                    dormant.append(a)
            frequency[f"N{n}_K{k}"] = {"pressed_at_2025": pressed_2025, "status_changes_2005_2025": changes_total,
                                       "claims_that_change": changing, "not_pressed_at_2025": dormant}
    for row in rows:
        row["distinct_years_2016_2025"] = sum(1 for x in years[row["area_id"]] if 2016 <= x <= 2025)

    out = ROOT / "outputs"
    out.mkdir(exist_ok=True)
    with (out / "claims.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    undated = [r["area_id"] for r in rows if not r["latest"]]
    summary = {
        "population": len(population), "claims_with_a_dated_step": len(population) - len(undated), "undated": undated,
        "steps": len(steps),
        "by_N": {str(n): {"regions_at_2025": regions_2025[n], "status_changes_2005_2025": flicker[n],
                          "claims_that_change": flickering[n]} for n in NS},
        "frequency_test": frequency,
        "inputs_sha256": {"inputs/steps.csv": hashlib.sha256((ROOT / "inputs" / "steps.csv").read_bytes()).hexdigest()},
    }
    (out / "summary.json").write_text(json.dumps(summary, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(summary["by_N"], indent=1))


if __name__ == "__main__":
    main()
