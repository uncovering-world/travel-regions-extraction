#!/usr/bin/env python3
"""Discover candidate territory-specific entry rules from Wikipedia's "Visa policy of <country>" articles.

The set of articles comes from the navbox "Template:Visa policy by country" at a pinned revision; every article
is read at a pinned revision. All pins live in sources.json. From each article the script keeps the sentences
(and table rows) that use an entry-rule word, and in them the places that Wikidata records as located in the
article's country. One candidate is one (article, place) pair. Every candidate must be accounted for in
discovery-map.csv: mapped to rows of the census of entry rules, ignored with a reason, or left empty (unmapped).
Deterministic for the pins in sources.json and the place answers in places.json.

    python3 data/entry-rules/discover.py             # regenerate candidates.csv and DISCOVERY.md from the pins
    python3 data/entry-rules/discover.py --latest    # move every pin to the current revision, then regenerate
    python3 data/entry-rules/discover.py --prefill   # also add map rows for new candidates (name matches filled in)
    python3 data/entry-rules/discover.py --check     # offline: are candidates.csv and DISCOVERY.md up to date?
"""
from __future__ import annotations

import argparse
import csv
import html
import io
import json
import re
import sys
import time
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent.parent
CENSUS = ROOT / "census.csv"
CACHE = ROOT / "cache"
AGENT = "ctr-entry-rules/0.1 (https://github.com/uncovering-world/travel-regions-extraction)"
WIKIPEDIA_API = "https://en.wikipedia.org/w/api.php"
WIKIDATA_API = "https://www.wikidata.org/w/api.php"
NAVBOX = "Template:Visa policy by country"
ARTICLE_PREFIX = re.compile(r"^Visa (?:policy|policies|history) of (?:the )?", re.I)

# A sentence is kept when it uses one of these words or phrases (case-insensitive). Broad on purpose:
# a place is a candidate only if a kept sentence names it, so recall depends on this list.
TRIGGER = re.compile(r"\b(?:" + "|".join([
    r"visa[- ]free", r"without (?:a )?visas?", r"visa[- ]exempt\w*", r"exempt\w*", r"waiver", r"waived",
    r"visas? on arrival", r"e-?visas?", r"permits?", r"permission", r"authori[sz]ation", r"restricted",
    r"protected areas?", r"prohibited", r"forbidden", r"closed (?:cit(?:y|ies)|areas?|zones?|town)",
    r"special administrative", r"special (?:economic|tourism|tourist|development) zones?", r"economic zones?",
    r"free (?:trade |economic |tourist )?zones?", r"free ports?", r"separate (?:immigration|entry|visa)",
    r"own (?:immigration|entry|visa)", r"immigration control", r"entry (?:permit|pass|card|ticket)s?",
    r"landing permits?", r"border (?:zones?|areas?|regions?|pass(?:es)?)", r"frontier (?:zones?|areas?)",
    r"inner line", r"autonom\w+", r"valid only", r"only valid", r"limited to", r"confined to", r"restricted to",
    r"transit", r"may (?:visit|enter|stay|travel)", r"allowed to (?:visit|enter|stay|travel)",
    r"not (?:allowed|permitted) to (?:visit|enter|travel)", r"escort\w*", r"tour (?:group|operator)s?",
]) + r")\b", re.I)

# Wikidata classes that are not a part of a country: a place of one of these classes is never a candidate.
NOT_A_PART = {"Q3624078": "sovereign state", "Q6256": "country", "Q5107": "continent"}


# ---------------------------------------------------------------- network

def get(api: str, params: dict) -> dict:
    """GET a MediaWiki API, backing off on 429, 5xx, maxlag and network errors. Raises after the last try."""
    url = api + "?" + urllib.parse.urlencode({**params, "format": "json", "formatversion": 2, "maxlag": 5})
    delay = 2.0
    for attempt in range(10):
        time.sleep(0.3)
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": AGENT}), timeout=60) as r:
                data = json.load(r)
            if data.get("error", {}).get("code") == "maxlag":
                raise urllib.error.HTTPError(url, 503, "maxlag", {}, None)
            return data
        except (urllib.error.URLError, TimeoutError, ConnectionError) as error:
            code = getattr(error, "code", None)
            if code is not None and code not in (429, 500, 502, 503, 504):
                raise
            retry_after = getattr(error, "headers", None) and error.headers.get("Retry-After")
            wait = float(retry_after) if retry_after and str(retry_after).isdigit() else delay
            print(f"  {code or error}: waiting {wait:.0f}s (attempt {attempt + 1})", file=sys.stderr)
            time.sleep(wait)
            delay = min(delay * 2, 120)
    raise RuntimeError(f"gave up after 10 attempts: {url}")


def chunks(items: list, size: int):
    for i in range(0, len(items), size):
        yield items[i:i + size]


def wikitext(revision: int) -> str:
    """The wikitext of one revision, from the local cache or Wikipedia."""
    cache = CACHE / f"{revision}.json"
    if cache.exists():
        return json.loads(cache.read_text())["text"]
    data = get(WIKIPEDIA_API, {"action": "query", "prop": "revisions", "revids": revision,
                               "rvprop": "content", "rvslots": "main"})
    pages = data["query"].get("pages", [])
    if not pages or "revisions" not in pages[0]:
        raise RuntimeError(f"revision {revision} not returned")
    text = pages[0]["revisions"][0]["slots"]["main"]["content"]
    CACHE.mkdir(exist_ok=True)
    (CACHE / ".gitignore").write_text("*\n")
    cache.write_text(json.dumps({"text": text}))
    return text


def resolve(titles: list[str]) -> dict[str, dict]:
    """For each title: the page it lands on after redirects, that page's latest revision and Wikidata item."""
    out = {}
    for batch in chunks(sorted(set(titles)), 50):
        q = get(WIKIPEDIA_API, {"action": "query", "titles": "|".join(batch), "redirects": 1,
                                "prop": "pageprops|revisions", "ppprop": "wikibase_item", "rvprop": "ids"})["query"]
        step = {n["from"]: n["to"] for n in q.get("normalized", [])}
        redirects = {r["from"]: r["to"] for r in q.get("redirects", [])}
        pages = {p["title"]: p for p in q.get("pages", [])}
        for title in batch:
            landed = step.get(title, title)
            for _ in range(5):
                if landed not in redirects:
                    break
                landed = redirects[landed]
            page = pages.get(landed, {})
            out[title] = {"title": landed, "exists": "missing" not in page and "invalid" not in page and bool(page),
                          "item": page.get("pageprops", {}).get("wikibase_item", ""),
                          "revid": (page.get("revisions") or [{}])[0].get("revid")}
    return out


def entities(items: list[str]) -> dict[str, dict]:
    """The claims P31, P17, P625 and P297 of Wikidata items, with the revision they were read at."""
    out = {}
    for batch in chunks(sorted(set(i for i in items if i)), 50):
        for qid, e in get(WIKIDATA_API, {"action": "wbgetentities", "ids": "|".join(batch),
                                         "props": "claims|info"})["entities"].items():
            claims = e.get("claims", {})

            def values(prop):
                vals = []
                for c in claims.get(prop, []):
                    if c.get("rank") == "deprecated":
                        continue
                    v = c["mainsnak"].get("datavalue", {}).get("value")
                    vals.append(v.get("id") if isinstance(v, dict) and "id" in v else v)
                return [v for v in vals if v]
            out[qid] = {"instance_of": sorted(set(values("P31"))), "country": sorted(set(values("P17"))),
                        "coordinates": bool(values("P625")), "iso": sorted(set(values("P297"))),
                        "lastrevid": e.get("lastrevid")}
    return out


# ---------------------------------------------------------------- pins

def today() -> str:
    return datetime.now(timezone.utc).date().isoformat()


def navbox_links(text: str) -> list[tuple[str, str]]:
    """(link target, label) for every visa-policy link in the navbox lists; extra links on a bullet share its label."""
    out = []
    for line in text.splitlines():
        if not line.lstrip().startswith("*"):
            continue
        links = re.findall(r"\[\[([^\[\]|]+)(?:\|([^\[\]]*))?\]\]", line)
        if not links or not ARTICLE_PREFIX.match(links[0][0]):
            continue
        label = links[0][1] or links[0][0]
        out += [(target.split("#")[0].strip(), label) for target, _ in links if ARTICLE_PREFIX.match(target)]
    return out


def refresh_pins() -> dict:
    """Move every pin to the current revision: the navbox, the articles it links, their Wikidata countries."""
    nav = resolve([NAVBOX])[NAVBOX]
    text = get(WIKIPEDIA_API, {"action": "query", "prop": "revisions", "revids": nav["revid"], "rvprop": "content",
                               "rvslots": "main"})["query"]["pages"][0]["revisions"][0]["slots"]["main"]["content"]
    links = navbox_links(text)
    landed = resolve([t for t, _ in links])
    articles, unread = {}, {}
    for target, label in links:
        page = landed[target]
        if not page["exists"]:
            entry = unread.setdefault(target, {"link": target, "labels": [], "reason": "no such page on Wikipedia"})
            entry["labels"] = sorted(set(entry["labels"]) | {label})
            continue
        entry = articles.setdefault(page["title"], {"title": page["title"], "oldid": page["revid"], "read": today(),
                                                    "wikidata": page["item"], "links": [], "labels": []})
        entry["links"] = sorted(set(entry["links"]) | {target})
        entry["labels"] = sorted(set(entry["labels"]) | {label})
    claims = entities([a["wikidata"] for a in articles.values()])
    countries = entities([c for a in articles.values() for c in claims.get(a["wikidata"], {}).get("country", [])])
    for a in articles.values():
        a["countries"] = {c: (countries.get(c, {}).get("iso") or [""])[0]
                          for c in claims.get(a["wikidata"], {}).get("country", [])}
    return {"navbox": {"title": NAVBOX, "oldid": nav["revid"], "read": today()},
            "wikidata_read": today(),
            "articles": [articles[t] for t in sorted(articles)],
            "unread": [unread[t] for t in sorted(unread)]}


# ---------------------------------------------------------------- reading an article

# Templates whose visible text is a parameter: {{nowrap|x}} shows its first, {{lang|xx|x}} its second.
SHOW_FIRST = {"nowrap", "nobr", "small", "abbr", "flag", "flagu", "flagcountry", "flagdeco", "flaglink", "lang-en"}
SHOW_SECOND = {"lang", "transl", "native name"}


def template_text(m: re.Match) -> str:
    name, *params = [p.strip() for p in m.group(1).split("|")]
    params = [p for p in params if not re.match(r"[\w -]+=", p)]
    name = name.lower()
    if name in SHOW_FIRST and params:
        return params[0]
    if name in SHOW_SECOND and len(params) > 1:
        return params[1]
    return ""


def strip_templates(text: str) -> str:
    """Drop templates, innermost first, keeping the visible text of the few in SHOW_FIRST and SHOW_SECOND."""
    while True:
        new = re.sub(r"\{\{([^{}]*)\}\}", template_text, text)
        if new == text:
            return text
        text = new


def clean(text: str) -> str:
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    text = re.sub(r"<ref[^>/]*/>|<ref[^>]*>.*?</ref>", "", text, flags=re.S | re.I)
    text = strip_templates(text)
    text = re.sub(r"\[\[(?:File|Image|Category):(?:[^\[\]]|\[\[[^\[\]]*\]\])*\]\]", "", text, flags=re.I)
    text = html.unescape(re.sub(r"<[^>]+>", " ", text))
    return re.sub(r"'''?", "", text)


def link_title(target: str) -> str:
    title = target.split("#")[0].replace("_", " ").strip()
    return title[:1].upper() + title[1:] if title else ""


def flatten(unit: str) -> tuple[str, list[tuple[int, int, str]]]:
    """Plain text of a piece of wikitext and the links in it as (start, end, target title)."""
    out, links, pos = [], [], 0
    length = 0
    for m in re.finditer(r"\[\[([^\[\]|]+)(?:\|([^\[\]]*))?\]\]|\[https?://[^\s\]]+(?:\s+([^\]]*))?\]", unit):
        before = unit[pos:m.start()]
        out.append(before)
        length += len(before)
        if m.group(1) is not None:
            target = m.group(1)
            shown = m.group(2) if m.group(2) is not None else target
            if not re.match(r"\s*:?\s*(?:wikt|wiktionary|s|commons|[a-z]{2,3}):", target, re.I):
                links.append((length, length + len(shown), link_title(target.lstrip(":"))))
        else:
            shown = m.group(3) or ""
        out.append(shown)
        length += len(shown)
        pos = m.end()
    out.append(unit[pos:])
    return "".join(out), links


def units(text: str):
    """(section path, wikitext) for every paragraph, list item and table row of an article."""
    path: list[str] = []
    table: list[str] = []
    depth = 0
    for line in clean(text).splitlines():
        stripped = line.strip()
        heading = re.fullmatch(r"(=+)\s*(.*?)\s*\1", stripped)
        if heading and depth == 0:
            level = len(heading.group(1))
            path = path[:max(level - 2, 0)] + [flatten(heading.group(2))[0].strip()]
            continue
        if stripped.startswith("{|"):
            depth += 1
            continue
        if depth:
            if stripped.startswith("|}"):
                depth -= 1
                if table:
                    yield " / ".join(path), " | ".join(table)
                table = []
            elif stripped.startswith("|-") or stripped.startswith("|+"):
                if table:
                    yield " / ".join(path), " | ".join(table)
                table = []
            elif stripped:
                for cell in re.split(r"\|\||!!", stripped.lstrip("|!")):
                    if re.match(r"\s*(?:rowspan|colspan|style|class|width|align|scope|data-sort-value)\s*=", cell):
                        cell = cell.split("|", 1)[1] if "|" in cell else ""
                    if cell.strip():
                        table.append(cell.strip())
            continue
        if stripped:
            yield " / ".join(path), stripped.lstrip("*#:; ")


def sentences(plain: str):
    start = 0
    for m in re.finditer(r"(?<=[.!?])\s+(?=[A-Z\"“(\[])", plain):
        yield start, plain[start:m.start()]
        start = m.end()
    yield start, plain[start:]


def mentions(text: str) -> list[dict]:
    """Every trigger sentence of an article with the link titles in it and its plain text."""
    out = []
    for section, unit in units(text):
        plain, links = flatten(unit)
        for start, sentence in sentences(plain):
            if not TRIGGER.search(sentence):
                continue
            end = start + len(sentence)
            out.append({"section": section, "text": re.sub(r"\s+", " ", sentence).strip(),
                        "links": [(plain[s:e], t) for s, e, t in links if s >= start and e <= end]})
    return out


def all_links(text: str) -> list[tuple[str, str]]:
    """(text as shown, title) of every link in an article."""
    out = []
    for _, unit in units(text):
        plain, links = flatten(unit)
        out += [(plain[s:e], t) for s, e, t in links]
    return out


# ---------------------------------------------------------------- places

def is_place(title: str, places: dict, article: dict) -> bool:
    """A link is a place of the article's country if Wikidata gives it coordinates, it is not itself a state or a
    continent, and its recorded country overlaps the article's (a missing country on either side does not exclude)."""
    info = places.get(title)
    if not info or not info.get("item") or not info.get("coordinates"):
        return False
    if info["item"] in article["countries"] or set(info.get("instance_of", [])) & set(NOT_A_PART):
        return False
    own = set(article["countries"])
    return not own or not info.get("country") or bool(own & set(info["country"]))


def resolve_places(titles: set[str], places: dict, everything: bool) -> int:
    todo = sorted(titles if everything else titles - set(places))
    if not todo:
        return 0
    print(f"resolving {len(todo)} link titles on Wikipedia and Wikidata", file=sys.stderr)
    landed = resolve(todo)
    claims = entities([p["item"] for p in landed.values()])
    for title in todo:
        page = landed[title]
        c = claims.get(page["item"], {})
        places[title] = {"page": page["title"], "item": page["item"], "coordinates": c.get("coordinates", False),
                         "instance_of": c.get("instance_of", []), "country": c.get("country", [])}
    return len(todo)


def subject(title: str) -> str:
    return ARTICLE_PREFIX.sub("", title)


def source_url(article: dict) -> str:
    return (f"https://en.wikipedia.org/w/index.php?title={urllib.parse.quote(article['title'].replace(' ', '_'))}"
            f"&oldid={article['oldid']}")


def word(text: str) -> re.Pattern:
    return re.compile(r"(?<!\w)" + re.escape(text) + r"(?!\w)")


def extract(articles: list[dict], texts: dict[int, str], places: dict) -> list[dict]:
    """One candidate per (article, place): the first trigger sentence that names the place, and how many do."""
    out = []
    item_of = {info["page"]: info["item"] for _, info in sorted(places.items())}
    for article in articles:
        text = texts.get(article["oldid"])
        if text is None:
            continue
        # every way the article writes a place it links somewhere: an unlinked later mention is also found
        names: dict[str, set[str]] = {}
        for shown, title in all_links(text):
            if is_place(title, places, article):
                key = places[title]["page"]
                bare = re.sub(r"\s*\(.*\)$", "", key)
                names.setdefault(key, set()).update(n for n in {shown.strip(), key, bare} if len(n) >= 3)
        found: dict[str, dict] = {}
        for m in mentions(text):
            hits = {places[t]["page"]: shown for shown, t in m["links"] if is_place(t, places, article)}
            for page, variants in names.items():
                if page not in hits:
                    shown = next((v for v in sorted(variants, key=len, reverse=True) if word(v).search(m["text"])), None)
                    if shown:
                        hits[page] = shown
            for page, shown in hits.items():
                entry = found.get(page)
                if entry:
                    entry["passages"] += 1
                    continue
                found[page] = {"key": f"{subject(article['title'])} / {page}", "country": subject(article["title"]),
                               "iso_codes": " ".join(sorted(c for c in article["countries"].values() if c)),
                               "place": shown.strip() or page, "place_title": page, "wikidata": item_of[page],
                               "section": m["section"], "passage": m["text"][:600], "passages": 1,
                               "source_url": source_url(article)}
        out += [found[page] for page in sorted(found)]
    return out


# ---------------------------------------------------------------- report

COLUMNS = ["key", "country", "iso_codes", "place", "place_title", "wikidata", "section", "passage", "passages",
           "source_url", "status"]
MAP_COLUMNS = ["key", "census_ids", "reason"]


def read_csv(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def fold(text: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFKD", text) if not unicodedata.combining(c)).casefold()


def name_matches(candidate: dict, census: list[dict]) -> list[str]:
    """Census rows of the candidate's country whose name contains the place as written or its article title."""
    codes = set(candidate["iso_codes"].split())
    names = {fold(candidate["place"]), fold(re.sub(r"\s*\(.*\)$", "", candidate["place_title"]))}
    return [r["id"] for r in census if r["iso_code"] in codes
            and any(len(n) >= 3 and word(n).search(fold(r["name"])) for n in names)]


def report(candidates: list[dict], mapping: list[dict], census: list[dict], pins: dict,
           not_read: list[str]) -> tuple[str, str, list[str]]:
    ids = {r["id"] for r in census}
    by_key = {r["key"]: r for r in mapping}
    broken, reached, unmapped = [], set(), []
    counts = {"mapped": 0, "ignored": 0, "unmapped": 0}
    rows = []
    for c in candidates:
        entry = by_key.get(c["key"])
        if not entry or not entry["census_ids"].strip():
            status = "unmapped"
            unmapped.append(c)
        elif entry["census_ids"].strip() == "ignore":
            status = "ignored"
            if not entry["reason"].strip():
                broken.append(f"{c['key']}: ignored without a reason")
        else:
            status = "mapped"
            for i in entry["census_ids"].split():
                if i in ids:
                    reached.add(i)
                else:
                    broken.append(f"{c['key']}: unknown census id {i}")
        counts[status] += 1
        rows.append({**c, "status": status})
    keys = {c["key"] for c in candidates}
    orphans = sorted(k for k in by_key if k not in keys)
    buffer = io.StringIO()
    writer = csv.DictWriter(buffer, fieldnames=COLUMNS, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    articles = pins["articles"]
    lines = ["# Discovery report", "", "Generated by `discover.py`; do not edit.", "",
             f"Navbox \"{pins['navbox']['title']}\" at revision {pins['navbox']['oldid']} "
             f"(read {pins['navbox']['read']}); {len(articles)} articles, each at the revision pinned in `sources.json`.",
             "",
             f"Candidates: {len(candidates)} from {len({c['country'] for c in candidates})} articles. "
             f"Mapped to the census: {counts['mapped']}. Ignored: {counts['ignored']}. Unmapped: {counts['unmapped']}. "
             f"Census rows reached from some candidate: {len(reached)} of {len(ids)}.", "",
             "## Articles that could not be read", ""]
    lines += [f"- {u['link']} ({', '.join(u['labels'])}): {u['reason']}" for u in pins.get("unread", [])]
    lines += [f"- {t}: the pinned revision could not be fetched in this run" for t in not_read]
    if not pins.get("unread") and not not_read:
        lines.append("None.")
    lines += ["", "## Candidates not accounted for", "",
              "Place as written, then the start of the first passage that names it.", ""]
    country = None
    for c in sorted(unmapped, key=lambda c: (c["country"], c["place_title"])):
        if c["country"] != country:
            country = c["country"]
            lines += ["", f"### {country}", ""] if lines[-1] != "" else [f"### {country}", ""]
        passage = c["passage"] if len(c["passage"]) <= 200 else c["passage"][:200].rsplit(" ", 1)[0] + " …"
        lines.append(f"- **{c['place']}** ({c['place_title']}, {c['passages']}×): {passage}")
    lines += ["", "## Census rows that no candidate maps to", "",
              "These came from another source than the Visa-policy articles, or their candidate is not mapped yet.", ""]
    lines += [f"- {r['id']}: {r['name']}" for r in census if r["id"] not in reached]
    lines += ["", "## Map entries whose candidate no longer exists", ""] + ([f"- {o}" for o in orphans] or ["None."])
    return buffer.getvalue(), "\n".join(lines) + "\n", broken


def prefill(candidates: list[dict], mapping: list[dict], census: list[dict]) -> list[dict]:
    """Add a map row for each candidate the map does not have yet: census ids where a name match is found, else empty."""
    known = {r["key"] for r in mapping}
    added = []
    for c in candidates:
        if c["key"] in known:
            continue
        ids = name_matches(c, census)
        added.append({"key": c["key"], "census_ids": " ".join(ids),
                      "reason": "prefill by name match; to be reviewed" if ids else ""})
    return mapping + added


def write_csv(path: Path, rows: list[dict], columns: list[str]) -> None:
    buffer = io.StringIO()
    writer = csv.DictWriter(buffer, fieldnames=columns, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    path.write_text(buffer.getvalue(), encoding="utf-8")


def load_json(name: str) -> dict:
    path = ROOT / name
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}


def dump_json(name: str, data: dict) -> None:
    (ROOT / name).write_text(json.dumps(data, indent=1, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--latest", action="store_true", help="move every pin to the current revision first")
    parser.add_argument("--prefill", action="store_true", help="add map rows for candidates not in the map")
    parser.add_argument("--check", action="store_true", help="offline: fail if the generated files are stale")
    args = parser.parse_args()
    census = read_csv(CENSUS)
    map_path = ROOT / "discovery-map.csv"
    mapping = read_csv(map_path) if map_path.exists() else []
    if args.check:
        pins = load_json("sources.json")
        candidates = [{k: v for k, v in r.items() if k != "status"} for r in read_csv(ROOT / "candidates.csv")]
        table, text, broken = report(candidates, mapping, census, pins, read_marker())
        stale = [p.name for p, want in ((ROOT / "candidates.csv", table), (ROOT / "DISCOVERY.md", text))
                 if p.read_text(encoding="utf-8") != want]
        problems = broken + [f"{name} is out of date; run discover.py" for name in stale]
        pinned = {source_url(a) for a in pins["articles"]}
        problems += [f"{c['key']}: source {c['source_url']} is not a pinned revision" for c in candidates
                     if c["source_url"] not in pinned]
        print("\n".join(problems) or "up to date", file=sys.stderr if problems else sys.stdout)
        return 1 if problems else 0
    if args.latest or not (ROOT / "sources.json").exists():
        print("refreshing pins", file=sys.stderr)
        dump_json("sources.json", refresh_pins())
    pins = load_json("sources.json")
    texts, not_read = {}, []
    for article in pins["articles"]:
        try:
            texts[article["oldid"]] = wikitext(article["oldid"])
        except Exception as error:  # recorded in the report, never skipped silently
            print(f"  could not read {article['title']} at {article['oldid']}: {error}", file=sys.stderr)
            not_read.append(article["title"])
    places_file = load_json("places.json")
    places = places_file.get("titles", {})
    titles = {t for text in texts.values() for _, t in all_links(text)}
    if resolve_places(titles, places, everything=args.latest):
        dump_json("places.json", {"read": today(), "note": "Wikidata answers for link titles in the pinned articles; "
                                  "see README.md. Kept between runs; refreshed by --latest.", "titles": places})
    candidates = extract(pins["articles"], texts, places)
    if args.prefill:
        mapping = prefill(candidates, mapping, census)
        write_csv(map_path, mapping, MAP_COLUMNS)
    (ROOT / "not-read.txt").unlink(missing_ok=True)
    if not_read:
        (ROOT / "not-read.txt").write_text("\n".join(not_read) + "\n")
    table, text, broken = report(candidates, mapping, census, pins, not_read)
    (ROOT / "candidates.csv").write_text(table, encoding="utf-8")
    (ROOT / "DISCOVERY.md").write_text(text, encoding="utf-8")
    if broken:
        print("\n".join(broken), file=sys.stderr)
        return 1
    unmapped = sum(1 for c in candidates if not any(m["key"] == c["key"] and m["census_ids"].strip() for m in mapping))
    print(f"{len(texts)} articles read, {len(not_read)} not read, {len(candidates)} candidates, {unmapped} unmapped")
    return 0


def read_marker() -> list[str]:
    path = ROOT / "not-read.txt"
    return path.read_text().split("\n")[:-1] if path.exists() else []


if __name__ == "__main__":
    raise SystemExit(main())
