#!/usr/bin/env python3
"""Count Wikivoyage regions one and two levels below each country page. Issue #28.

Reads English Wikivoyage through the MediaWiki API (50 titles per request), caches raw wikitext in
cache/ (gitignored) and writes inputs/wikivoyage-levels.csv with counts only.
Run from the repository root: python3 experiments/stage2-scale-survey/fetch_wikivoyage.py
"""
from __future__ import annotations

import csv
import json
import re
import time
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CACHE = ROOT / "cache" / "wikivoyage.json"
API = "https://en.wikivoyage.org/w/api.php"
AGENT = "ctr-stage2-scale-survey/0.1 (https://github.com/uncovering-world/travel-regions-extraction)"
# Page titles that differ from the NomadMania country name.
TITLES = {"United States": "United States of America", "Congo, Democratic Republic": "Democratic Republic of the Congo",
          "Congo, Republic": "Republic of the Congo", "Korea, North": "North Korea", "Korea, South": "South Korea",
          "Micronesia": "Federated States of Micronesia", "Myanmar (Burma)": "Myanmar", "Timor Leste": "East Timor",
          "Vatican": "Vatican City", "Georgia": "Georgia (country)", "French Southern and Antarctic Lands": "French Southern and Antarctic Lands",
          "Palestine": "Palestinian territories", "Gambia": "The Gambia", "Bahamas": "The Bahamas", "Ireland": "Ireland",
          "Macedonia": "North Macedonia", "Swaziland": "Eswatini", "Cape Verde": "Cape Verde", "Ivory Coast": "Côte d'Ivoire"}


def fetch(titles: list[str], cache: dict) -> None:
    todo = [t for t in titles if t not in cache]
    for i in range(0, len(todo), 50):
        batch = todo[i:i + 50]
        query = urllib.parse.urlencode({"action": "query", "prop": "revisions", "rvprop": "content", "rvslots": "main",
                                        "redirects": 1, "format": "json", "formatversion": 2, "titles": "|".join(batch)})
        request = urllib.request.Request(f"{API}?{query}", headers={"User-Agent": AGENT})
        with urllib.request.urlopen(request) as response:
            data = json.load(response)["query"]
        alias = {r["from"]: r["to"] for r in data.get("redirects", [])} | {n["from"]: n["to"] for n in data.get("normalized", [])}
        text = {p["title"]: (p["revisions"][0]["slots"]["main"]["content"] if "revisions" in p else None) for p in data["pages"]}
        for title in batch:
            target = title
            for _ in range(3):
                target = alias.get(target, target)
            cache[title] = text.get(target)
        time.sleep(1)


def regions(text: str | None) -> list[str]:
    """Names given as regionNname in the page's Regionlist template; linked names are link targets."""
    out = []
    for match in re.finditer(r"region\d+name\s*=\s*([^\n|]*(?:\[\[[^\]]*\]\][^\n|]*)*)", text or ""):
        value = match.group(1).strip()
        link = re.search(r"\[\[([^\]|#]+)", value)
        if link or value:
            out.append((link.group(1) if link else value).strip())
    return out


def main() -> int:
    cache = json.loads(CACHE.read_text()) if CACHE.exists() else {}
    with (ROOT / "inputs" / "nomadmania-counts.csv").open(newline="") as handle:
        countries = [r for r in csv.DictReader(handle) if r["iso"]]
    title = {r["country"]: TITLES.get(r["country"], r["country"]) for r in countries}
    fetch(sorted(set(title.values())), cache)
    level1 = {c: regions(cache.get(t)) for c, t in title.items()}
    fetch(sorted({name for names in level1.values() for name in names}), cache)
    CACHE.parent.mkdir(exist_ok=True)
    CACHE.write_text(json.dumps(cache, sort_keys=True))
    with (ROOT / "inputs" / "wikivoyage-levels.csv").open("w", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(["iso", "country", "page", "page_found", "level1", "level2", "level1_pages_missing"])
        for row in sorted(countries, key=lambda r: r["iso"]):
            names = level1[row["country"]]
            subs = [len(regions(cache.get(n))) for n in names]
            writer.writerow([row["iso"], row["country"], title[row["country"]], int(cache.get(title[row["country"]]) is not None),
                             len(names), sum(max(n, 1) for n in subs), sum(cache.get(n) is None for n in names)])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
