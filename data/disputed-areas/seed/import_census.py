#!/usr/bin/env python3
"""One-off, deterministic import of the 2026-10-03 census into the register's tables.

Kept for the record: it shows exactly how the first rows were produced. Rerunning it overwrites
areas.csv, facts.csv and sources.csv, so do not run it once the register has been edited.
"""
from __future__ import annotations

import csv
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
READ = "2026-10-03"
# The census took these from pages it fetched; the rest of each row is mostly general knowledge.
SOURCED = ("parties", "kind", "origin")
RECALLED = {"approx_area_km2": "area_km2", "on_the_ground": "on_the_ground", "inhabited": "inhabited",
            "traveller_access": "traveller_access"}


def main() -> int:
    with (HERE / "census-2026-10-03.csv").open(newline="") as handle:
        rows = sorted(csv.DictReader(handle), key=lambda r: r["id"])
    urls = sorted({u for r in rows for u in r["sources"].split()})
    source_id = {u: f"S{i:04d}" for i, u in enumerate(urls, 1)}
    with (ROOT / "sources.csv").open("w", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(["source_id", "url", "access", "note"])
        writer.writerow(["MEMORY", "", "none", "General knowledge of the agent that compiled the census; not checked against any source"])
        writer.writerow(["NE", "https://github.com/nvkelso/natural-earth-vector/tree/v5.1.2", "machine", "Natural Earth 10m admin-0 disputed areas, v5.1.2"])
        writer.writerow(["WD", "https://www.wikidata.org/", "machine", "Wikidata, read through the API at refresh time"])
        for url in urls:
            writer.writerow([source_id[url], url, "manual", ""])
    with (ROOT / "areas.csv").open("w", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(["area_id", "name", "wikidata_id", "natural_earth_id"])
        for r in rows:
            writer.writerow([r["id"], r["name"], "", ""])
    with (ROOT / "facts.csv").open("w", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(["area_id", "field", "value", "source_ids", "read_date", "evidence", "origin"])
        for r in rows:
            refs = " ".join(source_id[u] for u in r["sources"].split()) or "MEMORY"
            level = r["evidence"] if refs != "MEMORY" else "memory"
            for field in SOURCED:
                if r[field]:
                    writer.writerow([r["id"], field, r[field], refs, READ, level, "manual"])
            for column, field in RECALLED.items():
                if r[column] and r[column] != "unknown":
                    writer.writerow([r["id"], field, r[column], "MEMORY", READ, "memory", "manual"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
