#!/usr/bin/env python3
"""Third resolver: official unit names in a region's listed items or sub-region names. Issue #28.

Run after run.py, from the repository root: python3 experiments/stage2-wikivoyage-composition/probe_names.py
"""
from __future__ import annotations

import csv
import json
import re
import sys
import unicodedata
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
import run  # noqa: E402

GENERIC = r"\b(province|provincia|region|governorate|county|department|departamento|state|oblast|prefecture|canton|district|city|municipality|metropolitan|autonomous|capital|territory|of|de|del|la|el|al)\b"


def norm(name: str) -> str:
    text = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode().lower()
    text = re.sub(r"\([^)]*\)", " ", text)
    text = re.sub(GENERIC, " ", text)
    return re.sub(r"[^a-z0-9]+", "", text)


def items(text: str | None) -> dict[str, list[str]]:
    """On a country page: region name -> link targets and labels listed in its regionNitems."""
    names = dict(re.findall(r"region(\d+)name\s*=\s*([^\n]*)", text or ""))
    listed = dict(re.findall(r"region(\d+)items\s*=\s*([^\n]*)", text or ""))
    out = {}
    for number, raw in names.items():
        link = re.search(r"\[\[([^\]|#]+)", raw)
        region = (link.group(1) if link else raw).strip()
        out[region] = [part for pair in re.findall(r"\[\[([^\]|#]+)(?:\|([^\]]+))?\]\]", listed.get(number, "")) for part in pair if part]
    return out


def main() -> int:
    pages = json.loads((run.SURVEY / "cache" / "wikivoyage.json").read_text())
    with (run.SURVEY / "inputs" / "wikivoyage-levels.csv").open(newline="") as handle:
        title = {r["iso"]: r["page"] for r in csv.DictReader(handle)}
    with (ROOT / "inputs" / "iso3166-2-names.csv").open(newline="") as handle:
        units = defaultdict(dict)
        for r in csv.DictReader(handle):
            units[r["code"][:2]][r["code"]] = norm(r["name"])
    with (ROOT / "outputs" / "coverage.csv").open(newline="") as handle:
        by_id = {r["iso"]: r for r in csv.DictReader(handle)}
    rows = []
    for iso in run.COUNTRIES:
        listed = items(pages.get(title[iso]))
        assigned = defaultdict(set)
        for region in run.region_names(pages.get(title[iso])):
            candidates = {norm(x) for x in [*listed.get(region, []), *run.region_names(pages.get(region))]} - {""}
            for code, name in units[iso].items():
                if name and name in candidates:
                    assigned[code].add(region)
        once = sum(len(v) == 1 for v in assigned.values())
        rows.append({"iso": iso, "official_units": len(units[iso]), "by_ids": by_id[iso]["units_in_exactly_one_region"],
                     "by_names_exactly_one": once, "by_names_several": sum(len(v) > 1 for v in assigned.values()),
                     "coverage_by_names": round(once / len(units[iso]), 3)})
    with (ROOT / "outputs" / "names.csv").open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    for r in rows:
        print(*r.values())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
