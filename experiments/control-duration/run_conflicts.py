#!/usr/bin/env python3
"""After fighting over a territory stops, how long before one can tell it will not resume? Issue #20.

Uses the UCDP/PRIO Armed Conflict Dataset v26.1 (conflict-years 1946-2025, CC BY 4.0). A conflict is active
in a year when it caused at least 25 battle-related deaths. Only conflicts over territory are used.

Run from the repository root: python3 experiments/control-duration/run_conflicts.py
"""
from __future__ import annotations

import csv
import hashlib
import io
import json
import sys
import urllib.request
import zipfile
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent
URL = "https://ucdp.uu.se/downloads/ucdpprio/ucdp-prio-acd-261-csv.zip"
SHA256 = "5f951743222964674a446e32a5a871077b29bd13349588d85fc59953d89c878a"
LAST_YEAR = 2025               # last year covered by v26.1
QUIET = (1, 2, 3, 5, 10)       # quiet years Q after which the situation would be reviewed
FOLLOW_UP = 10
TYPES = {"1": "extrasystemic", "2": "interstate", "3": "intrastate", "4": "internationalized_intrastate"}


def conflict_years() -> list[dict]:
    path = ROOT / "cache" / "ucdp-prio-acd-261-csv.zip"
    if not path.exists():
        path.parent.mkdir(exist_ok=True)
        request = urllib.request.Request(URL, headers={"User-Agent": "Mozilla/5.0 (research; ctr-control-duration)"})
        with urllib.request.urlopen(request) as response:
            path.write_bytes(response.read())
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    if digest != SHA256:
        print(f"WARNING: dataset sha256 {digest} differs from the recorded one", file=sys.stderr)
    with zipfile.ZipFile(path) as archive:
        name = next(n for n in archive.namelist() if n.endswith(".csv"))
        text = archive.read(name).decode("utf-8-sig")
    return list(csv.DictReader(io.StringIO(text)))


def episodes(rows: list[dict]) -> list[dict]:
    """One record per episode: a run of consecutive active years of one conflict."""
    years = defaultdict(set)
    meta = {}
    for r in rows:
        years[r["conflict_id"]].add(int(r["year"]))
        meta[r["conflict_id"]] = r
    out = []
    for cid in sorted(years, key=int):
        active = sorted(years[cid])
        runs, start, prev = [], active[0], active[0]
        for y in active[1:]:
            if y != prev + 1:
                runs.append((start, prev))
                start = y
            prev = y
        runs.append((start, prev))
        for i, (s, e) in enumerate(runs):
            nxt = runs[i + 1][0] if i + 1 < len(runs) else None
            out.append({
                "conflict_id": cid, "location": meta[cid]["location"], "territory": meta[cid]["territory_name"],
                "type": TYPES.get(meta[cid]["type_of_conflict"], meta[cid]["type_of_conflict"]),
                "start": s, "end": e, "active_years": e - s + 1, "ongoing": int(e == LAST_YEAR),
                "resumed_in": nxt or "", "quiet_years": (nxt - e - 1) if nxt else (LAST_YEAR - e),
                "resumed": int(nxt is not None),
            })
    return out


def recurrence(eps: list[dict]) -> dict:
    """Among ended episodes: product-limit estimate of staying quiet, and of resuming after Q quiet years."""
    ended = [e for e in eps if not e["ongoing"]]
    events = Counter(e["quiet_years"] for e in ended if e["resumed"])   # resumed after this many full quiet years
    observed = [e["quiet_years"] for e in ended]                        # quiet years seen (to resumption or to LAST_YEAR)
    survival, s = {}, 1.0
    for q in range(0, max(observed, default=0) + 2):
        survival[q] = s                                               # P(at least q quiet years)
        at_risk = sum(o >= q for o in observed)
        if at_risk:
            s *= 1 - events.get(q, 0) / at_risk
    out = {
        "ended_episodes": len(ended), "resumed_so_far": sum(e["resumed"] for e in ended),
        "stays_quiet_at_least": {str(q): round(survival[q], 3) for q in (1, 2, 3, 5, 10, 20) if q in survival},
        "resumes_within_follow_up_after_Q_quiet_years": {
            str(q): round(1 - survival[q + FOLLOW_UP] / survival[q], 3)
            for q in QUIET if survival.get(q) and (q + FOLLOW_UP) in survival},
        "resumes_within_5_years_after_Q_quiet_years": {
            str(q): round(1 - survival[q + 5] / survival[q], 3) for q in QUIET if survival.get(q) and (q + 5) in survival},
        "quiet_years_before_resumption": dict(sorted(events.items())),
    }
    return out


def lengths(eps: list[dict]) -> dict:
    done = sorted(e["active_years"] for e in eps if not e["ongoing"])
    return {"ended_episodes": len(done), "median_active_years": done[len(done) // 2] if done else None,
            "share_lasting_at_most": {str(k): round(sum(d <= k for d in done) / len(done), 3) for k in (1, 2, 5, 10)} if done else {}}


def main() -> int:
    rows = [r for r in conflict_years() if r["incompatibility"] in ("1", "3")]   # over territory, or territory and government
    eps = episodes(rows)
    groups = {
        "all_territorial": eps,
        "interstate": [e for e in eps if e["type"] == "interstate"],
        "within_states": [e for e in eps if e["type"] in ("intrastate", "internationalized_intrastate")],
    }
    summary = {
        "source": {"dataset": "UCDP/PRIO Armed Conflict Dataset v26.1", "url": URL, "sha256": SHA256, "last_year": LAST_YEAR,
                   "licence": "CC BY 4.0", "conflict_years_over_territory": len(rows),
                   "conflicts_over_territory": len({r["conflict_id"] for r in rows})},
        "episode_length": {k: lengths(v) for k, v in groups.items()},
        "recurrence": {k: recurrence(v) for k, v in groups.items()},
    }
    out = ROOT / "outputs"
    out.mkdir(exist_ok=True)
    (out / "conflicts_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    with (out / "conflict_episodes.csv").open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(eps[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(eps)
    print(json.dumps(summary, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
