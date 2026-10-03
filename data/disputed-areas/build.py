#!/usr/bin/env python3
"""Validate the register of disputed and special-status areas and regenerate its derived files.

Inputs (edited by hand or by refresh_machine.py): areas.csv, facts.csv, sources.csv.
Outputs (never edited by hand): registry.csv, pages/<area_id>.md, REPORT.md.

    python3 data/disputed-areas/build.py            # regenerate
    python3 data/disputed-areas/build.py --check    # fail if the committed outputs are out of date
    python3 data/disputed-areas/build.py --today 2027-01-15   # staleness as of a given day
"""
from __future__ import annotations

import argparse
import csv
import io
import sys
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent

KINDS = ["own_regime", "lease_or_base", "de_facto_state", "occupied_or_annexed", "paper_claim",
         "islets_for_maritime_zone", "line_position", "no_agreed_boundary", "unclaimed", "resolved_recently"]
# field -> allowed values (None = free text)
FIELDS = {
    "parties": None, "kind": KINDS, "origin": None, "on_the_ground": None,
    "inhabited": ["yes", "no", "garrison_only"],
    "traveller_access": ["open", "restricted", "closed", "expedition_only"],
    "area_km2": None,
    # machine fields
    "ne_name": None, "ne_type": None, "ne_note": None, "ne_area_km2": None, "ne_attribution": None,
    "wd_label": None, "wd_area_km2": None, "wd_population": None, "wd_coordinates": None,
}
EVIDENCE = ["primary", "secondary", "machine"]  # there is no level for facts written from memory: they are not admitted
REQUIRED = ["parties", "kind"]
STALE_AFTER_DAYS = 365  # a manual fact older than this is listed for re-checking
MIN_QUOTE = 15  # characters; the passage of a manual fact has to be long enough to be found on the page
REGISTRY_COLUMNS = ["area_id", "name", "status", "kind", "parties", "area_km2", "inhabited", "traveller_access",
                    "weakest_evidence", "oldest_read", "wikidata_id", "natural_earth_id"]


def read(name: str) -> list[dict]:
    with (ROOT / name).open(newline="") as handle:
        return list(csv.DictReader(handle))


def validate(areas: list[dict], facts: list[dict], sources: list[dict]) -> list[str]:
    errors = []
    ids = [a["area_id"] for a in areas]
    known_sources = {s["source_id"] for s in sources}
    if len(ids) != len(set(ids)):
        errors.append("duplicate area_id in areas.csv")
    if ids != sorted(ids):
        errors.append("areas.csv is not sorted by area_id")
    seen = set()
    for n, f in enumerate(facts, 2):
        where = f"facts.csv line {n}"
        if f["area_id"] not in set(ids):
            errors.append(f"{where}: unknown area {f['area_id']}")
        if f["field"] not in FIELDS:
            errors.append(f"{where}: unknown field {f['field']}")
        elif FIELDS[f["field"]] and f["value"] not in FIELDS[f["field"]]:
            errors.append(f"{where}: value {f['value']!r} not allowed for {f['field']}")
        if not f["value"]:
            errors.append(f"{where}: empty value")
        refs = f["source_ids"].split()
        if not refs or any(r not in known_sources for r in refs):
            errors.append(f"{where}: missing or unknown source")
        if f["evidence"] not in EVIDENCE:
            errors.append(f"{where}: unknown evidence level {f['evidence']}")
        if f["origin"] == "manual" and len(f["quote"].strip()) < MIN_QUOTE:
            errors.append(f"{where}: a manual fact needs the passage of the source it rests on")
        if f["origin"] not in ("manual", "machine"):
            errors.append(f"{where}: origin must be manual or machine")
        try:
            date.fromisoformat(f["read_date"])
        except ValueError:
            errors.append(f"{where}: read_date is not a date")
        if (f["area_id"], f["field"]) in seen:
            errors.append(f"{where}: second value for {f['area_id']}/{f['field']}")
        seen.add((f["area_id"], f["field"]))
    return errors


def render(areas: list[dict], facts: list[dict], sources: list[dict], today: date) -> dict[str, str]:
    """All derived files as {relative path: content}."""
    by_area: dict[str, dict[str, dict]] = defaultdict(dict)
    for f in facts:
        by_area[f["area_id"]][f["field"]] = f
    url = {s["source_id"]: s["url"] or s["note"] for s in sources}
    out: dict[str, str] = {}

    buffer = io.StringIO()
    writer = csv.DictWriter(buffer, fieldnames=REGISTRY_COLUMNS, lineterminator="\n")
    writer.writeheader()
    for a in areas:
        own = by_area[a["area_id"]]
        levels = [f["evidence"] for f in own.values() if f["origin"] == "manual"]
        writer.writerow({
            "area_id": a["area_id"], "name": a["name"],
            **{k: own[k]["value"] if k in own else "" for k in ("kind", "parties", "area_km2", "inhabited", "traveller_access")},
            "status": "sourced" if all(k in own for k in REQUIRED) else "unsourced",
            "weakest_evidence": max(levels, key=EVIDENCE.index) if levels else "",
            "oldest_read": min((f["read_date"] for f in own.values()), default=""),
            "wikidata_id": a["wikidata_id"], "natural_earth_id": a["natural_earth_id"],
        })
    out["registry.csv"] = buffer.getvalue()

    for a in areas:
        own = by_area[a["area_id"]]
        lines = [f"# {a['name']}", "", f"`{a['area_id']}` — generated by `build.py` from `facts.csv`; do not edit.", "",
                 "| Field | Value | Evidence | Read | Sources | Passage |", "|---|---|---|---|---|---|"]
        for field in FIELDS:
            if field in own:
                f = own[field]
                value = f["value"].replace("|", "\\|")
                quote = f["quote"].replace("|", "\\|")
                lines.append(f"| {field} | {value} | {f['evidence']} | {f['read_date']} | {f['source_ids']} | {quote} |")
        used = sorted({r for f in own.values() for r in f["source_ids"].split()})
        lines += ["", "Sources:", ""] + [f"- {r}: {url[r]}" for r in used]
        out[f"pages/{a['area_id']}.md"] = "\n".join(lines).rstrip("\n") + "\n"

    kinds = Counter(by_area[a["area_id"]]["kind"]["value"] for a in areas if "kind" in by_area[a["area_id"]])
    unsourced = [a["area_id"] for a in areas if not all(k in by_area[a["area_id"]] for k in REQUIRED)]
    manual = [f for f in facts if f["origin"] == "manual"]
    evidence = Counter(f["evidence"] for f in manual)
    stale = sorted({f["area_id"] for f in manual if (today - date.fromisoformat(f["read_date"])).days > STALE_AFTER_DAYS})
    unlinked_wd = [a["area_id"] for a in areas if not a["wikidata_id"]]
    unlinked_ne = [a["area_id"] for a in areas if not a["natural_earth_id"]]
    missing = {field: sum(field not in by_area[a["area_id"]] for a in areas)
               for field in ("origin", "on_the_ground", "inhabited", "traveller_access", "area_km2")}
    report = ["# Register report", "", "Generated by `build.py`; do not edit.", "",
              f"Areas: {len(areas)}. Facts: {len(facts)} ({len(manual)} manual, {len(facts) - len(manual)} machine).", "",
              "## Areas by kind", ""] + [f"- {k}: {kinds.get(k, 0)}" for k in KINDS] + [
              "", "## Manual facts by evidence", ""] + [f"- {k}: {evidence.get(k, 0)}" for k in EVIDENCE if k != "machine"] + [
              "", "## Work list", "",
              f"- Areas without sourced `parties` and `kind` (not usable by rules yet): {len(unsourced)}",
              f"- Areas without a Wikidata id: {len(unlinked_wd)}",
              f"- Areas without a Natural Earth link: {len(unlinked_ne)}"] + [
              f"- Areas missing `{field}`: {count}" for field, count in missing.items()] + [
              f"- Areas with manual facts older than {STALE_AFTER_DAYS} days: {len(stale)}"
              + (" — " + ", ".join(stale) if stale and len(stale) <= 40 else "")]
    out["REPORT.md"] = "\n".join(report) + "\n"
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--today", type=date.fromisoformat, default=None,
                        help="day for the staleness list; default: the latest read_date in facts.csv, so output is reproducible")
    args = parser.parse_args()
    areas, facts, sources = read("areas.csv"), read("facts.csv"), read("sources.csv")
    errors = validate(areas, facts, sources)
    if errors:
        print("\n".join(errors[:50]), file=sys.stderr)
        return 1
    today = args.today or max((date.fromisoformat(f["read_date"]) for f in facts), default=date.min)
    files = render(areas, facts, sources, today)
    expected_pages = {p for p in files if p.startswith("pages/")}
    existing_pages = {f"pages/{p.name}" for p in (ROOT / "pages").glob("*.md")} if (ROOT / "pages").exists() else set()
    if args.check:
        stale = [p for p, content in files.items() if not (ROOT / p).exists() or (ROOT / p).read_text() != content]
        stale += sorted(existing_pages - expected_pages)
        if stale:
            print("out of date: " + ", ".join(stale[:10]), file=sys.stderr)
            return 1
        return 0
    (ROOT / "pages").mkdir(exist_ok=True)
    for path in existing_pages - expected_pages:
        (ROOT / path).unlink()
    for path, content in files.items():
        (ROOT / path).write_text(content)
    print(f"{len(areas)} areas, {len(facts)} facts; wrote registry.csv, REPORT.md and {len(expected_pages)} pages")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
