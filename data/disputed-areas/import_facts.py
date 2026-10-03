#!/usr/bin/env python3
"""Import sourced facts from CSV files into the register. Deterministic: the same files give the same result.

Each file has the columns area_id, field, value, source_url, quote, evidence: one manual fact per row, with the
passage of the source it rests on. A row that breaks a rule of the register is left out and listed. So is a row for
an area and field that already has a value: an existing fact is never replaced. A source already in sources.csv
keeps its id; new sources get the next free S number, in the order of their URLs. Exit code 1 if any row was left out.

    python3 data/disputed-areas/import_facts.py --date 2026-10-03 batch-1.csv batch-2.csv
The sources are not opened here: run verify_quotes.py next, then build.py.
"""
from __future__ import annotations

import argparse
import csv
import io
import re
import sys
from collections import Counter
from datetime import date
from pathlib import Path

import build
from refresh_machine import FACT_COLUMNS

ROOT = Path(__file__).resolve().parent
COLUMNS = ["area_id", "field", "value", "source_url", "quote", "evidence"]
SOURCE_COLUMNS = ["source_id", "url", "access", "note"]
MANUAL_FIELDS = [f for f in build.FIELDS if not f.startswith(("ne_", "wd_"))]  # the others belong to refresh_machine.py
MANUAL_EVIDENCE = [e for e in build.EVIDENCE if e != "machine"]


def objection(row: dict, areas: set[str]) -> str | None:
    """Why the register cannot take this row as a manual fact, if it cannot."""
    if None in row or None in row.values():
        return "wrong number of columns"
    if row["area_id"] not in areas:
        return f"unknown area {row['area_id']}"
    if row["field"] not in MANUAL_FIELDS:
        return f"{row['field']} is not a manual field"
    allowed = build.FIELDS[row["field"]]
    if not row["value"] or allowed and row["value"] not in allowed:
        return f"value {row['value']!r} not allowed for {row['field']}"
    if row["evidence"] not in MANUAL_EVIDENCE:
        return f"evidence must be one of {', '.join(MANUAL_EVIDENCE)}, not {row['evidence']!r}"
    if len(row["quote"].strip()) < build.MIN_QUOTE:
        return "a manual fact needs the passage of the source it rests on"
    if not re.fullmatch(r"https?://\S+", row["source_url"]):
        return f"the source is not a URL: {row['source_url']!r}"
    if re.search(r"//[a-z-]+\.wikipedia\.org/", row["source_url"]) and not re.search(r"[?&]oldid=\d+", row["source_url"]):
        return "a Wikipedia source must be the permanent link of a revision (oldid)"
    return None


def merge(rows: list[tuple[str, dict]], areas: list[dict], facts: list[dict], sources: list[dict],
          read_date: date) -> tuple[list[dict], list[dict], list[str]]:
    """The register's facts and sources with the rows added, and the rows left out, each with the reason.

    `rows` pairs each input row with where it stands ("file line n").
    """
    known = {a["area_id"] for a in areas}
    held = {(f["area_id"], f["field"]): f["value"] for f in facts}
    reasons = []
    for _, row in rows:
        key = (row["area_id"], row["field"])
        why = objection(row, known)
        if not why and key in held:
            why = f"the register already has {held[key]!r} here and the row gives {row['value']!r}; nothing was replaced"
        reasons.append(why)
    times = Counter((row["area_id"], row["field"]) for (_, row), why in zip(rows, reasons) if not why)
    left_out, good = [], []
    for (where, row), why in zip(rows, reasons):
        if not why and times[(row["area_id"], row["field"])] > 1:
            why = f"{times[(row['area_id'], row['field'])]} rows give this area and field a value; none was taken"
        if why:
            left_out.append(f"{where}: {row['area_id']}/{row['field']}: {why}")
        else:
            good.append(row)

    sources = list(sources)
    source_id = {s["url"]: s["source_id"] for s in sources}
    number = max((int(s["source_id"][1:]) for s in sources if re.fullmatch(r"S\d+", s["source_id"])), default=0)
    for url in sorted({row["source_url"] for row in good} - set(source_id)):
        number += 1
        source_id[url] = f"S{number:04d}"
        sources.append({"source_id": source_id[url], "url": url, "access": "manual", "note": ""})

    fields = list(build.FIELDS)
    new = [{"area_id": row["area_id"], "field": row["field"], "value": row["value"], "source_ids": source_id[row["source_url"]],
            "quote": row["quote"], "read_date": read_date.isoformat(), "evidence": row["evidence"], "origin": "manual"} for row in good]
    new.sort(key=lambda f: fields.index(f["field"]))
    order = {a["area_id"]: n for n, a in enumerate(areas)}
    # the order refresh_machine.py keeps: by area, manual facts first; rows already there do not move past each other
    return sorted(facts + new, key=lambda f: (order[f["area_id"]], f["origin"] == "machine")), sources, left_out


def rendered(columns: list[str], rows: list[dict]) -> str:
    buffer = io.StringIO()
    writer = csv.DictWriter(buffer, fieldnames=columns, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return buffer.getvalue()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("files", nargs="+", type=Path, help="CSV files with the columns " + ",".join(COLUMNS))
    parser.add_argument("--date", type=date.fromisoformat, required=True, help="the day the sources were read")
    args = parser.parse_args()
    rows: list[tuple[str, dict]] = []
    for path in args.files:
        with path.open(newline="") as handle:
            reader = csv.DictReader(handle)
            if reader.fieldnames != COLUMNS:
                parser.error(f"{path}: the columns must be {','.join(COLUMNS)}")
            rows += [(f"{path.name} line {n}", row) for n, row in enumerate(reader, 2)]
    areas, facts, sources = build.read("areas.csv"), build.read("facts.csv"), build.read("sources.csv")
    errors = build.validate(areas, facts, sources)  # the register has to be sound before anything is added to it
    if not errors:
        merged, listed, left_out = merge(rows, areas, facts, sources, args.date)
        errors = build.validate(areas, merged, listed)  # and what was added has to pass the same check
    if errors:
        print("\n".join(errors[:50]), file=sys.stderr)
        return 1
    files = {"facts.csv": rendered(FACT_COLUMNS, merged), "sources.csv": rendered(SOURCE_COLUMNS, listed)}
    for name, content in files.items():  # both are complete before either file is touched
        (ROOT / name).write_text(content)
    if left_out:
        print("\n".join(left_out), file=sys.stderr)
    print(f"{len(merged) - len(facts)} of {len(rows)} rows imported, {len(left_out)} left out; {len(listed) - len(sources)} new sources")
    return 1 if left_out else 0


if __name__ == "__main__":
    raise SystemExit(main())
