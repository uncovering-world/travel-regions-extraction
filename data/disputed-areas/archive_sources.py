#!/usr/bin/env python3
"""Store an archived copy for every source that is a live page, so its quoted passages stay checkable.

A live page is a manual source that is neither a pinned Wikipedia revision nor a file at a pinned commit. For each
one without an archived copy, the Wayback Machine is asked for a snapshot taken within MAX_AGE_DAYS of the run; if
there is none, it is asked to take one. The snapshot URL is written into the source's `note` as "archived: <url>".
Nothing else changes. Requests are spaced out to stay within the archive's limits for anonymous use.

    python3 data/disputed-areas/archive_sources.py            # all live pages without an archived copy
    python3 data/disputed-areas/archive_sources.py --dry-run  # only list them
"""
from __future__ import annotations

import argparse
import csv
import io
import json
import re
import sys
import time
import urllib.parse
import urllib.request
from datetime import date, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent
COLUMNS = ["source_id", "url", "access", "note"]
AGENT = "Mozilla/5.0 (research; ctr-disputed-areas archive)"
MAX_AGE_DAYS = 30
PAUSE = 12              # seconds between save requests
PINNED = (re.compile(r"[?&]oldid=\d+"), re.compile(r"/[0-9a-f]{40}/"), re.compile(r"^https?://web\.archive\.org/web/\d+"))


def live(source: dict) -> bool:
    return (source["access"] == "manual" and "archived: " not in source["note"]
            and not any(p.search(source["url"]) for p in PINNED))


def get(url: str, timeout: int = 90) -> urllib.request.addinfourl:
    return urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": AGENT}), timeout=timeout)


def recent_snapshot(url: str, today: date) -> str | None:
    query = "https://archive.org/wayback/available?" + urllib.parse.urlencode({"url": url, "timestamp": today.strftime("%Y%m%d")})
    with get(query) as response:
        closest = json.load(response).get("archived_snapshots", {}).get("closest") or {}
    if not closest.get("available") or not str(closest.get("status", "")).startswith("2"):
        return None
    taken = datetime.strptime(closest["timestamp"][:8], "%Y%m%d").date()
    return closest["url"].replace("http://", "https://", 1) if abs((today - taken).days) <= MAX_AGE_DAYS else None


def save(url: str) -> str | None:
    with get("https://web.archive.org/save/" + url, timeout=180) as response:
        final = response.geturl()
        location = response.headers.get("Content-Location", "")
    match = re.search(r"/web/\d{14}/", location or final)
    return "https://web.archive.org" + (location if location.startswith("/web/") else urllib.parse.urlparse(final).path) if match else None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    path = ROOT / "sources.csv"
    with path.open(encoding="utf-8", newline="") as handle:
        sources = list(csv.DictReader(handle))
    todo = [s for s in sources if live(s)]
    print(f"{len(todo)} live pages without an archived copy")
    if args.dry_run:
        print("\n".join(f"{s['source_id']} {s['url']}" for s in todo))
        return 0
    failed = []
    today = date.today()
    for n, source in enumerate(todo, 1):
        snapshot = None
        try:
            snapshot = recent_snapshot(source["url"], today)
            if not snapshot:
                time.sleep(PAUSE)
                snapshot = save(source["url"])
        except Exception as error:  # the archive refuses some sites and times out on others; report and go on
            print(f"  {source['source_id']}: {type(error).__name__}: {error}", file=sys.stderr)
        if snapshot:
            source["note"] = (source["note"] + "; " if source["note"] else "") + "archived: " + snapshot
            buffer = io.StringIO()
            writer = csv.DictWriter(buffer, fieldnames=COLUMNS, lineterminator="\n")
            writer.writeheader()
            writer.writerows(sources)
            path.write_text(buffer.getvalue(), encoding="utf-8")   # after each success, so an interrupted run keeps its work
        else:
            failed.append(source)
        print(f"[{n}/{len(todo)}] {source['source_id']} {'ok' if snapshot else 'FAILED'}")
    if failed:
        print("No archived copy for:\n" + "\n".join(f"  {s['source_id']} {s['url']}" for s in failed))
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
