#!/usr/bin/env python3
"""How long territory-specific entry regimes last, and what a rule of N consecutive yearly cut-offs would do. Issue #20.

Input: inputs/regimes.csv, collected from sources on 2026-10-03 (each date with a quoted passage; see README).
Run from the repository root: python3 experiments/regime-lifetimes/run.py
"""
from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
LAST = 2025                # last complete year
CUTOFFS = (1, 2, 3)        # consecutive year-end cut-offs a regime must be in force at before it enters a release
FOLLOW = 5


def year(text: str) -> int | None:
    return int(text[:4]) if text[:4].isdigit() else None


def covid(row: dict) -> bool:
    return row["end_kind"] == "suspended" and row["end_date"][:4] == "2020"


def main() -> None:
    rows = list(csv.DictReader((ROOT / "inputs" / "regimes.csv").open(encoding="utf-8")))
    new = [r for r in rows if (year(r["start_date"]) or 0) >= 2000]
    summary = {"regimes": len(rows), "started_2000_or_later": len(new),
               "border_resident_schemes_among_them": sum(r["regime_kind"] == "local_border_traffic" for r in new)}
    for label, keep in (("all_endings", lambda r: True), ("without_2020_closures", lambda r: not covid(r))):
        spans = []          # years from start to the first ending or suspension; None if none counted
        for r in new:
            start, end = year(r["start_date"]), year(r["end_date"])
            spans.append(end - start if end is not None and keep(r) else None)
        ended = [s for s in spans if s is not None]
        part = {"ended_or_suspended": len(ended),
                "within_years_of_start": {str(k): sum(s <= k for s in ended) for k in (0, 1, 2, 3, 5, 10)}}
        for n in CUTOFFS:
            entered = left = pending = 0
            for r, span in zip(new, spans):
                start = year(r["start_date"])
                if span is not None and span <= n - 1:
                    continue                      # gone before its n-th cut-off: never enters
                if start + n - 1 > LAST:
                    pending += 1                  # too recent to have reached its n-th cut-off
                    continue
                entered += 1
                if span is not None and span - (n - 1) <= FOLLOW:
                    left += 1
            part[f"cutoffs_{n}"] = {"entered": entered, "left_within_5_years_of_entering": left, "too_recent": pending}
        summary[label] = part
    stated = [r for r in new if r["stated_expiry_or_pilot"] == "yes"]
    summary["stated_expiry_or_pilot"] = {
        "yes": len(stated), "no": sum(r["stated_expiry_or_pilot"] == "no" for r in new),
        "unknown": sum(r["stated_expiry_or_pilot"] == "" for r in new),
        "of_yes_ended_other_than_2020_closure": sum(bool(r["end_date"]) and not covid(r) for r in stated),
        "early_endings_within_2_years_with_stated_expiry": sum(
            bool(r["end_date"]) and not covid(r) and year(r["end_date"]) - year(r["start_date"]) <= 2 for r in stated)}
    suspended = [r for r in rows if r["end_kind"] == "suspended"]
    gaps = sorted(year(r["resumed_date"]) - year(r["end_date"]) for r in suspended if r["resumed_date"])
    summary["suspensions"] = {"all": len(suspended), "in_2020": sum(covid(r) for r in suspended),
                              "resumed": len(gaps), "years_until_resumed": gaps}
    summary["evidence"] = {k: sum(r["evidence"] == k for r in rows) for k in ("primary", "secondary")}
    (ROOT / "outputs").mkdir(exist_ok=True)
    (ROOT / "outputs" / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=1))


if __name__ == "__main__":
    main()
