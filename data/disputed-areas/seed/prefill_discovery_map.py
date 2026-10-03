#!/usr/bin/env python3
"""One-off prefill of discovery-map.csv. Kept for the record; do not rerun after the map has been edited.

Natural Earth features are mapped through the links already in areas.csv. A Wikipedia row is mapped to an
area when the area's short name occurs in the row's label. These name matches are marked for review.
"""
from __future__ import annotations

import csv
import re
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def norm(text: str) -> str:
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", " ", text).strip()


def main() -> int:
    with (ROOT / "areas.csv").open(newline="") as handle:
        areas = list(csv.DictReader(handle))
    with (ROOT / "candidates.csv").open(newline="") as handle:
        candidates = list(csv.DictReader(handle))
    by_ne = {ne_id: a["area_id"] for a in areas for ne_id in a["natural_earth_id"].split()}
    short = {a["area_id"]: norm(re.split(r" \(| and |,|/", a["name"])[0]) for a in areas}
    rows = []
    for c in candidates:
        if c["source"] == "natural_earth":
            if c["key"] in by_ne:
                rows.append([c["source"], c["key"], by_ne[c["key"]], "linked in areas.csv"])
            continue
        label = f" {norm(c['label'])} "
        hits = sorted(a for a, name in short.items() if len(name) >= 5 and f" {name} " in label)
        if hits:
            rows.append([c["source"], c["key"], " ".join(hits), "prefill by name match; to be reviewed"])
    with (ROOT / "discovery-map.csv").open("w", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(["source", "key", "area_ids", "reason"])
        writer.writerows(rows)
    print(len(rows), "entries")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
