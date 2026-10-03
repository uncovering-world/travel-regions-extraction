#!/usr/bin/env python3
"""Discover candidate areas from machine-readable lists and show which are not yet in the register.

Sources: Wikipedia's "List of territorial disputes" at a pinned revision (ongoing land disputes only),
and Natural Earth's disputed-areas layer at a pinned version. Every candidate must be accounted for in
discovery-map.csv: mapped to one or more area ids, or ignored with a reason. Deterministic for the pins.

    python3 data/disputed-areas/discover.py            # regenerate candidates.csv and DISCOVERY.md
    python3 data/disputed-areas/discover.py --latest   # report what a newer Wikipedia revision would add (changes nothing)
"""
from __future__ import annotations

import argparse
import csv
import io
import json
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
import refresh_machine  # noqa: E402

WIKIPEDIA_PAGE = "List_of_territorial_disputes"
WIKIPEDIA_REVISION = 1377757742  # read 2026-10-01T00:35:39Z
STOP_SECTION = "Disputes over territorial waters"  # everything from here on is out of scope


def wikitext(revision: int | None) -> tuple[int, str]:
    cache = ROOT / "cache" / f"wikipedia-{revision}.json"
    if revision and cache.exists():
        return revision, json.loads(cache.read_text())["text"]
    params = {"action": "parse", "prop": "wikitext|revid", "format": "json", "formatversion": 2}
    params |= {"oldid": revision} if revision else {"page": WIKIPEDIA_PAGE}
    request = urllib.request.Request("https://en.wikipedia.org/w/api.php?" + urllib.parse.urlencode(params),
                                     headers={"User-Agent": refresh_machine.AGENT})
    with urllib.request.urlopen(request) as response:
        data = json.load(response)["parse"]
    if revision:
        cache.parent.mkdir(exist_ok=True)
        cache.write_text(json.dumps({"text": data["wikitext"]}))
    return data["revid"], data["wikitext"]


def plain(cell: str) -> str:
    cell = re.sub(r"<ref[^>]*/>|<ref[^>]*>.*?</ref>", "", cell, flags=re.S)
    cell = re.sub(r"\{\{[^{}]*\}\}", "", cell)
    cell = re.sub(r"\[\[(?:[^\]|]*\|)?([^\]]*)\]\]", r"\1", cell)
    cell = re.sub(r"<[^>]+>|'''?", "", cell)
    return re.sub(r"\s+", " ", cell).strip(" ,;")


def wikipedia_candidates(text: str) -> list[dict]:
    text = text.split(f"== {STOP_SECTION} ==")[0]
    out, section = [], ""
    for block in re.split(r"^(=+[^=\n]+=+)\s*$", text, flags=re.M):
        heading = re.fullmatch(r"=+\s*([^=]+?)\s*=+", block.strip())
        if heading:
            section = heading.group(1)
            continue
        for table in re.findall(r"\{\|.*?\n\|\}", block, flags=re.S):
            for row in re.split(r"\n\|-[^\n]*", table)[1:]:
                cells = [c for c in re.split(r"\n[|!]", "\n" + row.strip()) if c.strip()]
                if not cells or row.lstrip().startswith("!"):
                    continue
                label = plain(cells[0].split("|", 1)[-1] if re.match(r"\s*(rowspan|colspan|style|width|class)", cells[0]) else cells[0])
                if label and label.lower() != "territory":
                    out.append({"source": "wikipedia", "key": f"{section} / {label}"[:200], "label": label, "context": section})
    return out


def natural_earth_candidates() -> list[dict]:
    features = refresh_machine.natural_earth()
    return [{"source": "natural_earth", "key": ne_id, "label": f["properties"]["NAME"],
             "context": f["properties"].get("NOTE_BRK") or f["properties"]["TYPE"]}
            for ne_id, f in sorted(features.items())]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--latest", action="store_true")
    args = parser.parse_args()
    _, pinned = wikitext(WIKIPEDIA_REVISION)
    candidates = wikipedia_candidates(pinned) + natural_earth_candidates()
    if args.latest:
        revision, text = wikitext(None)
        known = {c["key"] for c in candidates}
        new = [c for c in wikipedia_candidates(text) if c["key"] not in known]
        print(f"latest revision {revision}: {len(new)} rows not in pinned revision {WIKIPEDIA_REVISION}")
        for c in new:
            print("  ", c["key"])
        return 0
    with (ROOT / "areas.csv").open(newline="") as handle:
        areas = {r["area_id"] for r in csv.DictReader(handle)}
    with (ROOT / "discovery-map.csv").open(newline="") as handle:
        mapping = {(r["source"], r["key"]): r for r in csv.DictReader(handle)}
    buffer = io.StringIO()
    writer = csv.DictWriter(buffer, fieldnames=["source", "key", "label", "context", "status"], lineterminator="\n")
    writer.writeheader()
    unmapped, broken, covered = [], [], set()
    for c in candidates:
        entry = mapping.get((c["source"], c["key"]))
        if not entry:
            status = "unmapped"
            unmapped.append(c)
        elif entry["area_ids"] == "ignore":
            status = "ignored"
        else:
            ids = entry["area_ids"].split()
            missing = [i for i in ids if i not in areas]
            if missing:
                broken.append(f"{c['source']} {c['key']}: unknown area {missing}")
            covered |= set(ids)
            status = "mapped"
        writer.writerow({**c, "status": status})
    orphan_map = sorted(f"{s} {k}" for (s, k) in mapping if (s, k) not in {(c["source"], c["key"]) for c in candidates})
    (ROOT / "candidates.csv").write_text(buffer.getvalue())
    uncovered = sorted(areas - covered)
    lines = ["# Discovery report", "", "Generated by `discover.py`; do not edit.", "",
             f"Wikipedia revision {WIKIPEDIA_REVISION}; Natural Earth v5.1.2.", "",
             f"Candidates: {len(candidates)} ({sum(c['source'] == 'wikipedia' for c in candidates)} Wikipedia rows, "
             f"{sum(c['source'] == 'natural_earth' for c in candidates)} Natural Earth features). "
             f"Unmapped: {len(unmapped)}. Areas not reached from any candidate: {len(uncovered)}.", "",
             "## Candidates not accounted for", ""] + [f"- {c['source']}: {c['key']} — {c['context']}" for c in unmapped] + [
             "", "## Areas in the register that no candidate maps to", "",
             "These came from another source; their `parties` fact must cite it.", ""] + [f"- {a}" for a in uncovered] + [
             "", "## Map entries whose candidate no longer exists", ""] + [f"- {o}" for o in orphan_map]
    (ROOT / "DISCOVERY.md").write_text("\n".join(lines) + "\n")
    if broken:
        print("\n".join(broken), file=sys.stderr)
        return 1
    print(f"{len(candidates)} candidates, {len(unmapped)} unmapped, {len(uncovered)} areas not reached")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
