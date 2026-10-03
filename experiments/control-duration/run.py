#!/usr/bin/env python3
"""How long does a change of control take to settle? Durations of military occupations. Issue #20.

Reads Wikipedia's "List of military occupations" at a pinned revision, extracts start and end years,
and reports how many occupations end before a waiting time T and how many of those that reach T end soon after.

Run from the repository root: python3 experiments/control-duration/run.py
"""
from __future__ import annotations

import csv
import hashlib
import json
import re
import sys
import urllib.parse
import urllib.request
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PAGE = "List_of_military_occupations"
REVISION = 1377366365          # read 2026-10-03
AS_OF = 2026                   # year at which ongoing occupations are censored
THRESHOLDS = (1, 2, 3, 5, 10)  # waiting times T, in years
FOLLOW_UP = 10                 # "ends soon after" = within this many years after reaching T
AGENT = "ctr-control-duration/0.1 (https://github.com/uncovering-world/travel-regions-extraction)"


def page_html() -> str:
    cache = ROOT / "cache" / f"{PAGE}-{REVISION}.html"
    if not cache.exists():
        query = urllib.parse.urlencode({"action": "parse", "oldid": REVISION, "prop": "text", "format": "json", "formatversion": 2})
        request = urllib.request.Request(f"https://en.wikipedia.org/w/api.php?{query}", headers={"User-Agent": AGENT})
        with urllib.request.urlopen(request) as response:
            html = json.load(response)["parse"]["text"]
        cache.parent.mkdir(exist_ok=True)
        cache.write_text(html)
    return cache.read_text()


def span(value: str | None) -> int:
    """rowspan/colspan attribute as a number; the page has a few malformed values such as '63\"'."""
    digits = re.match(r"\s*(\d+)", value or "")
    return max(1, int(digits.group(1))) if digits else 1


class Tables(HTMLParser):
    """Collect wikitables as grids of cell texts, expanding rowspan and colspan; remember the heading above each."""

    def __init__(self) -> None:
        super().__init__()
        self.tables: list[dict] = []
        self.heading = ""
        self._in_heading = False
        self._table: dict | None = None
        self._row: list | None = None
        self._cell: dict | None = None
        self._pending: dict[int, list] = {}   # column -> [rows left, text]
        self._skip = 0                        # depth inside <sup>/<style>: footnote markers and CSS are not content
        self._depth = 0

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag in ("h2", "h3"):
            self._in_heading, self.heading = True, ""
        elif tag == "table":
            if self._table is None and "wikitable" in attrs.get("class", ""):
                self._table = {"heading": self.heading, "rows": []}
                self._pending = {}
            elif self._table is not None:
                self._depth += 1
        elif self._table is not None and self._depth == 0:
            if tag == "tr":
                self._row = []
            elif tag in ("td", "th") and self._row is not None:
                self._cell = {"text": "", "rowspan": span(attrs.get("rowspan")), "colspan": span(attrs.get("colspan")),
                              "header": tag == "th"}
            elif tag in ("sup", "style") and self._cell is not None:
                self._skip += 1
            elif tag == "br" and self._cell is not None:
                self._cell["text"] += " / "

    def handle_endtag(self, tag):
        if tag in ("h2", "h3"):
            self._in_heading = False
        elif tag == "table" and self._table is not None:
            if self._depth:
                self._depth -= 1
            else:
                self.tables.append(self._table)
                self._table = None
        elif self._table is not None and self._depth == 0:
            if tag in ("sup", "style") and self._skip:
                self._skip -= 1
            elif tag in ("td", "th") and self._cell is not None and self._row is not None:
                self._row.append(self._cell)
                self._cell = None
            elif tag == "tr" and self._row is not None:
                self._table["rows"].append(self._expand(self._row))
                self._row = None

    def handle_data(self, data):
        if self._in_heading:
            self.heading += data
        elif self._cell is not None and not self._skip:
            self._cell["text"] += data

    def _expand(self, cells: list[dict]) -> list[str]:
        out: list[str] = []
        queue = list(cells)
        column = 0
        while queue or column in self._pending:
            if column in self._pending:
                left, text = self._pending[column]
                out.append(text)
                if left > 1:
                    self._pending[column] = [left - 1, text]
                else:
                    del self._pending[column]
                column += 1
                continue
            cell = queue.pop(0)
            text = re.sub(r"\s+", " ", cell["text"]).strip()
            for _ in range(cell["colspan"]):
                out.append(text)
                if cell["rowspan"] > 1:
                    self._pending[column] = [cell["rowspan"] - 1, text]
                column += 1
        return out


def years(text: str) -> tuple[int, int] | None:
    """Start and end year from a 'Years' cell such as '1914–1918', '1914', '1990-91'."""
    found = re.findall(r"\b(1[89]\d\d|20\d\d)\b", text)
    if not found:
        return None
    start = int(found[0])
    end = int(found[-1])
    short = re.search(r"\b(1[89]\d\d|20\d\d)\s*[–-]\s*(\d\d)\b(?!\d)", text)
    if len(found) == 1 and short:
        end = start // 100 * 100 + int(short.group(2))
    return (start, end) if end >= start else None


def era(start: int) -> str:
    if 1914 <= start <= 1918:
        return "world_war_1"
    if 1939 <= start <= 1945:
        return "world_war_2"
    return "before_1946_other" if start < 1946 else "since_1946"


def load() -> list[dict]:
    parser = Tables()
    parser.feed(page_html())
    rows: list[dict] = []
    for table in parser.tables:
        if not table["rows"]:
            continue
        header = [h.lower() for h in table["rows"][0]]
        if "years" in header:                       # historical occupations
            t, y, o, a = header.index("occupied territory"), header.index("years"), header.index("occupying state"), len(header) - 1
            for r in table["rows"][1:]:
                span = years(r[y]) if len(r) > max(t, y, o) else None
                if span:
                    rows.append({"territory": r[t], "occupier": r[o], "start": span[0], "end": span[1], "ongoing": 0,
                                 "annexed": int(r[a].lower().startswith("yes")) if len(r) > a else 0, "section": table["heading"].strip()})
        elif "since" in header:                     # ongoing occupations
            t, y = header.index("territory"), header.index("since")
            o = header.index("occupying state")
            for r in table["rows"][1:]:
                span = years(r[y]) if len(r) > max(t, y, o) else None
                if span:
                    rows.append({"territory": r[t], "occupier": r[o], "start": span[0], "end": AS_OF, "ongoing": 1,
                                 "annexed": 0, "section": table["heading"].strip()})
    rows.sort(key=lambda r: (r["start"], r["end"], r["territory"], r["occupier"]))
    return rows


def apply_annexation_outcomes(rows: list[dict]) -> None:
    """For occupations since 1946 that the list marks as annexed, the listed end year is the year of
    annexation, not necessarily the end of control. inputs/annexed_outcomes.csv says, with a source for
    each, whether the annexing state still holds the territory; if so the change of control is ongoing."""
    with (ROOT / "inputs" / "annexed_outcomes.csv").open(newline="") as handle:
        outcome = {(r["territory"], int(r["start"])): r["control_continues_today"] for r in csv.DictReader(handle)}
    for r in rows:
        if r["start"] >= 1946 and r["annexed"]:
            key = (r["territory"], r["start"])
            if key not in outcome:
                raise SystemExit(f"annexed occupation without a sourced outcome: {key}")
            if outcome[key] == "yes":
                r["end"], r["ongoing"] = AS_OF, 1


def spans(rows: list[dict]) -> dict:
    """Year-resolution statistics. span = end year - start year, so the true duration is within a year of it."""
    ended = [r["end"] - r["start"] for r in rows if not r["ongoing"]]
    out: dict = {"occupations": len(rows), "ended": len(ended), "ongoing": sum(r["ongoing"] for r in rows)}
    if ended:
        ordered = sorted(ended)
        out["ended_median_span"] = ordered[len(ordered) // 2]
        out["ended_share_span_at_most"] = {str(k): round(sum(s <= k for s in ended) / len(ended), 3) for k in (0, 1, 2, 4, 9)}
    by_t = {}
    for t in THRESHOLDS:
        # Occupations whose fate at T is known: ended, or ongoing for at least T years.
        known = [r for r in rows if not r["ongoing"] or r["end"] - r["start"] >= t]
        reached = [r for r in known if r["end"] - r["start"] >= t]
        # Of those that reached T, the ones whose fate at T + FOLLOW_UP is known.
        followed = [r for r in reached if not r["ongoing"] or r["end"] - r["start"] >= t + FOLLOW_UP]
        ended_soon = [r for r in followed if not r["ongoing"] and r["end"] - r["start"] < t + FOLLOW_UP]
        by_t[str(t)] = {
            "fate_known": len(known), "ended_before_T": len(known) - len(reached),
            "share_ended_before_T": round((len(known) - len(reached)) / len(known), 3) if known else None,
            "reached_T_with_known_follow_up": len(followed), "of_those_ended_within_follow_up": len(ended_soon),
            "share_reverting_after_T": round(len(ended_soon) / len(followed), 3) if followed else None,
        }
    out["by_waiting_time"] = by_t
    return out


def kaplan_meier(rows: list[dict]) -> dict:
    """Product-limit estimate of P(span >= T), ongoing occupations censored at their current age.
    Also, for each waiting time T, the estimated share of those reaching T that end within FOLLOW_UP years."""
    events = Counter(r["end"] - r["start"] for r in rows if not r["ongoing"])
    ages = [r["end"] - r["start"] for r in rows]
    survival, s = {}, 1.0
    for year in range(0, max(ages, default=0) + 1):
        survival[year] = s                       # P(span >= year)
        at_risk = sum(a >= year for a in ages)
        if at_risk:
            s *= 1 - events.get(year, 0) / at_risk
    def reach(year: int) -> float | None:
        return survival.get(year)
    out = {"reaches_T": {str(t): round(reach(t), 3) for t in (1, 2, 3, 5, 10, 20) if reach(t) is not None}}
    out["ends_within_follow_up_after_reaching_T"] = {
        str(t): round(1 - reach(t + FOLLOW_UP) / reach(t), 3)
        for t in THRESHOLDS if reach(t) and reach(t + FOLLOW_UP) is not None}
    out["ends_within_5_years_after_reaching_T"] = {
        str(t): round(1 - reach(t + 5) / reach(t), 3) for t in THRESHOLDS if reach(t) and reach(t + 5) is not None}
    return out


def main() -> int:
    html = page_html()
    rows = load()
    apply_annexation_outcomes(rows)
    for r in rows:
        r["era"] = era(r["start"])
    recent = [r for r in rows if r["era"] == "since_1946"]
    summary = {
        "source": {"page": PAGE, "revision": REVISION, "sha256": hashlib.sha256(html.encode()).hexdigest(), "as_of_year": AS_OF,
                   "follow_up_years": FOLLOW_UP},
        "all": spans(rows),
        "by_era": {name: spans([r for r in rows if r["era"] == name]) for name in ("since_1946", "world_war_2", "world_war_1", "before_1946_other")},
        "since_1946_survival": kaplan_meier(recent),
        "since_1946_survival_annexed_only": kaplan_meier([r for r in recent if r["annexed"]]),
        "since_1946_survival_not_annexed": kaplan_meier([r for r in recent if not r["annexed"]]),
        "span_histogram_since_1946_ended": dict(sorted(Counter(r["end"] - r["start"] for r in rows if r["era"] == "since_1946" and not r["ongoing"]).items())),
    }
    out = ROOT / "outputs"
    out.mkdir(exist_ok=True)
    (out / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    with (out / "occupations.csv").open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["territory", "occupier", "start", "end", "ongoing", "annexed", "era", "section"], lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    print(json.dumps({"rows": len(rows), "since_1946": summary["by_era"]["since_1946"], "survival": summary["since_1946_survival"],
                      "histogram": summary["span_histogram_since_1946_ended"]}, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
