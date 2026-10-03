#!/usr/bin/env python3
"""Do Wikivoyage regions state their composition in official units? Issue #28.

For each test country: which ISO 3166-2 top-tier units are assigned to exactly one level-1 Wikivoyage
region, through the Wikidata ids in the `mapshape` templates of that region's page or of the country page.
Uses the scale survey's cached wikitext and looks up Wikidata P300 (ISO 3166-2 code) for the ids found.
Run from the repository root: python3 experiments/stage2-wikivoyage-composition/run.py
"""
from __future__ import annotations

import csv
import json
import re
import time
import urllib.parse
import urllib.request
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SURVEY = ROOT.parent / "stage2-scale-survey"
CACHE = ROOT / "cache" / "wikidata-p300.json"
AGENT = "ctr-stage2-composition/0.1 (https://github.com/uncovering-world/travel-regions-extraction)"
# Countries of the survey's "groups the top tier" class with at least six reference regions, plus two controls.
COUNTRIES = ["TH", "JP", "TR", "VN", "DZ", "KE", "IR", "NG", "CO", "PE", "PH", "EG", "MY", "UA", "TZ", "CL", "CH", "AO", "PG", "IT", "DE"]
CONTROLS = {"IT", "DE"}


def region_names(text: str | None) -> list[str]:
    out = []
    for match in re.finditer(r"region\d+name\s*=\s*([^\n|]*(?:\[\[[^\]]*\]\][^\n|]*)*)", text or ""):
        value = match.group(1).strip()
        link = re.search(r"\[\[([^\]|#]+)", value)
        if link or value:
            out.append((link.group(1) if link else value).strip())
    return out


def shape_ids(text: str | None) -> list[str]:
    """Wikidata ids named by mapshape templates on a page."""
    ids: list[str] = []
    for template in re.findall(r"\{\{\s*[Mm]apshape[^{}]*\}\}", text or ""):
        match = re.search(r"wikidata\s*=\s*([Q0-9,\s]+)", template)
        if match:
            ids += re.findall(r"Q\d+", match.group(1))
    return ids


def titled_shapes(text: str | None) -> dict[str, list[str]]:
    """On a parent page: mapshape title (the region it draws) -> Wikidata ids it is composed of."""
    out: dict[str, list[str]] = defaultdict(list)
    for template in re.findall(r"\{\{\s*[Mm]apshape[^{}]*\}\}", text or ""):
        ids = re.search(r"wikidata\s*=\s*([Q0-9,\s]+)", template)
        title = re.search(r"title\s*=\s*(?:\[\[)?([^\]|}\n]+)", template)
        if ids and title:
            out[title.group(1).strip()] += re.findall(r"Q\d+", ids.group(1))
    return dict(out)


def p300(ids: set[str]) -> dict[str, str]:
    """Wikidata id -> ISO 3166-2 code (empty when the item has none)."""
    cache = json.loads(CACHE.read_text()) if CACHE.exists() else {}
    todo = sorted(ids - cache.keys())
    for i in range(0, len(todo), 50):
        query = urllib.parse.urlencode({"action": "wbgetentities", "ids": "|".join(todo[i:i + 50]), "props": "claims", "format": "json"})
        request = urllib.request.Request(f"https://www.wikidata.org/w/api.php?{query}", headers={"User-Agent": AGENT})
        with urllib.request.urlopen(request) as response:
            entities = json.load(response).get("entities", {})
        for qid in todo[i:i + 50]:
            claims = entities.get(qid, {}).get("claims", {}).get("P300", [])
            values = [c["mainsnak"]["datavalue"]["value"] for c in claims if c["mainsnak"].get("datavalue") and c.get("rank") != "deprecated"]
            cache[qid] = values[0] if values else ""
        time.sleep(1)
    CACHE.parent.mkdir(exist_ok=True)
    CACHE.write_text(json.dumps(cache, sort_keys=True))
    return cache


def main() -> int:
    pages = json.loads((SURVEY / "cache" / "wikivoyage.json").read_text())
    with (SURVEY / "inputs" / "wikivoyage-levels.csv").open(newline="") as handle:
        title = {r["iso"]: r["page"] for r in csv.DictReader(handle)}
    with (SURVEY / "inputs" / "iso3166-2.csv").open(newline="") as handle:
        units = defaultdict(set)
        for r in csv.DictReader(handle):
            if not r["parent"]:
                units[r["code"][:2]].add(r["code"])
    found: dict[str, dict[str, list[str]]] = {}
    for iso in COUNTRIES:
        regions = region_names(pages.get(title[iso]))
        on_parent = titled_shapes(pages.get(title[iso]))
        # A region's units: ids its own page draws, plus ids the country page draws under the region's name.
        found[iso] = {name: shape_ids(pages.get(name)) + on_parent.get(name, []) for name in regions}
        found[iso]["(country page)"] = shape_ids(pages.get(title[iso]))
    codes = p300({q for per in found.values() for ids in per.values() for q in ids})

    rows = []
    for iso in COUNTRIES:
        per = found[iso]
        regions = [n for n in per if n != "(country page)"]
        assigned: dict[str, set[str]] = defaultdict(set)
        for name in regions:
            for qid in per[name]:
                if codes.get(qid) in units[iso]:
                    assigned[codes[qid]].add(name)
        once = sum(len(v) == 1 for v in assigned.values())
        many = sum(len(v) > 1 for v in assigned.values())
        own_shape = len(per["(country page)"])
        rows.append({
            "iso": iso, "control": int(iso in CONTROLS), "level1_regions": len(regions), "official_units": len(units[iso]),
            "units_in_exactly_one_region": once, "units_in_several_regions": many,
            "units_unassigned": len(units[iso]) - once - many,
            "coverage": round(once / len(units[iso]), 3) if units[iso] else "",
            "regions_with_any_unit": len({n for v in assigned.values() for n in v}),
            "shape_ids_on_country_page": own_shape,
            "country_page_ids_that_are_official_units": sum(codes.get(q) in units[iso] for q in per["(country page)"]),
        })
    out = ROOT / "outputs"
    out.mkdir(exist_ok=True)
    with (out / "coverage.csv").open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    test = [r for r in rows if not r["control"]]
    bands = Counter("90%+" if r["coverage"] >= 0.9 else "50-90%" if r["coverage"] >= 0.5 else "under 50%" for r in test)
    summary = {"test_countries": len(test), "coverage_bands": dict(sorted(bands.items())),
               "countries_with_units_in_several_regions": [r["iso"] for r in rows if r["units_in_several_regions"]]}
    (out / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2))
    for r in rows:
        print(r)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
