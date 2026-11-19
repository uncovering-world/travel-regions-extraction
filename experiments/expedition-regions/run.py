#!/usr/bin/env python3
"""Apply the candidate definition of an expedition region (README) to inputs/facts.csv; write outputs/summary.json.

expedition = no permanent residents and no scheduled transport (revision of 2026-11-19: expedition cruises do not
count as regular access).
"""
import csv, hashlib, json
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def verdict(r: dict, a: dict) -> str:
    """Revisions of 2026-11-19 (owner): a publicly sold expedition cruise is an expedition, not regular access; a
    place is closed only where an act bars civilians (travel advice does not count); and a place an ordinary visitor
    can walk or drive into (inputs/access.csv, land_access) is ordinary, like one with scheduled transport."""
    if a.get("closed_by_act") == "yes":
        return "closed"
    if r["residents"] == "yes":
        return "ordinary: residents"
    if r["scheduled"] == "yes":
        return "ordinary: scheduled transport"
    if a.get("land_access") == "yes":
        return "ordinary: open land access"
    if r["residents"] == "no" and r["scheduled"] == "no" and a.get("land_access", "no") == "no":
        return "expedition" + (" (sold expedition landings)" if r["tours"] == "yes" else "")
    return "undecided: facts unknown"


def main() -> None:
    path = ROOT / "inputs" / "facts.csv"
    rows = list(csv.DictReader(path.open(encoding="utf-8")))
    access_path = ROOT / "inputs" / "access.csv"
    access = {a["region_id"]: a for a in csv.DictReader(access_path.open(encoding="utf-8"))}
    out = {r["region_id"]: {"verdict": verdict(r, access.get(r["region_id"], {})), "residents": r["residents"], "scheduled": r["scheduled"],
                            "tours": r["tours"], "permit": r["permit"]} for r in sorted(rows, key=lambda r: r["region_id"])}
    counts = {}
    for v in out.values():
        counts[v["verdict"]] = counts.get(v["verdict"], 0) + 1
    summary = {"input_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
               "access_sha256": hashlib.sha256(access_path.read_bytes()).hexdigest(), "counts": dict(sorted(counts.items())),
               "regions": out}
    (ROOT / "outputs").mkdir(exist_ok=True)
    (ROOT / "outputs" / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    for rid, v in out.items():
        print(f"{rid:28} {v['verdict']:50} {v['permit'][:60]}")


if __name__ == "__main__":
    main()
