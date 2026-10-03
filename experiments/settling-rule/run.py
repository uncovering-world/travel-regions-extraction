#!/usr/bin/env python3
"""Back-test of the settling rule for contested areas with waiting times T = 1, 2, 3, 5, 10. Issue #20.

The rule: an area taken by force is unsettled and stays attributed to its last settled holder; the canon accepts
the new holder after T consecutive quiet calendar years; a return of control ends the unsettled status at once.

Sources (pinned in inputs/sources.json): the Modern Conquest dataset v3.0 (seizures by states), Table 2 of
Florea 2020 (de facto states, transcribed in inputs/defacto_states.csv) and the UCDP/PRIO Armed Conflict
Dataset v26.1 (years of fighting).

Run from the repository root: python3 experiments/settling-rule/run.py
"""
from __future__ import annotations

import csv
import hashlib
import io
import json
import re
import sys
import urllib.request
import xml.etree.ElementTree as ET
import zipfile
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCES = json.loads((ROOT / "inputs" / "sources.json").read_text(encoding="utf-8"))
WAITS = (1, 2, 3, 5, 10)
MC_FIRST, MC_LAST = 1946, 2024      # seizures considered; last year the conquest dataset covers
FLOREA_LAST = 2016                  # last year Florea's table covers
HOW = {"1": "force", "2": "force", "3": "pressure", "4": "pressure",
       "5": "agreed", "6": "agreed", "7": "agreed", "8": "other"}
NS = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"


def fetch(key: str) -> bytes:
    """Download a pinned source into cache/ once and warn if its checksum differs from the recorded one."""
    source = SOURCES[key]
    path = ROOT / "cache" / source["url"].rsplit("/", 1)[1]
    if not path.exists():
        path.parent.mkdir(exist_ok=True)
        request = urllib.request.Request(source["url"], headers={"User-Agent": "Mozilla/5.0 (research; ctr-settling-rule)"})
        with urllib.request.urlopen(request) as response:
            path.write_bytes(response.read())
    data = path.read_bytes()
    digest = hashlib.sha256(data).hexdigest()
    if digest != source["sha256"]:
        print(f"WARNING: {key} sha256 {digest} differs from the recorded one", file=sys.stderr)
    return data


def read_xlsx(data: bytes) -> list[dict]:
    """First sheet of a workbook as a list of dicts keyed by the header row (standard library only)."""
    book = zipfile.ZipFile(io.BytesIO(data))
    strings = ["".join(t.text or "" for t in si.iter(f"{NS}t"))
               for si in ET.fromstring(book.read("xl/sharedStrings.xml")).findall(f"{NS}si")]
    rows = []
    for row in ET.fromstring(book.read("xl/worksheets/sheet1.xml")).iter(f"{NS}row"):
        cells = {}
        for c in row.findall(f"{NS}c"):
            column = 0
            for ch in re.match(r"[A-Z]+", c.get("r")).group(0):
                column = column * 26 + ord(ch) - 64
            v = c.find(f"{NS}v")
            if c.get("t") == "s" and v is not None:
                cells[column - 1] = strings[int(v.text)]
            elif c.get("t") == "inlineStr":
                cells[column - 1] = "".join(t.text or "" for t in c.iter(f"{NS}t"))
            else:
                cells[column - 1] = v.text if v is not None else ""
        if cells:
            rows.append([cells.get(i, "") for i in range(max(cells) + 1)])
    header = rows[0]
    return [dict(zip(header, r + [""] * (len(header) - len(r)))) for r in rows[1:]]


def number(text: str) -> int | None:
    try:
        return int(float(text))
    except (TypeError, ValueError):
        return None


def load_conquests() -> list[dict]:
    archive = zipfile.ZipFile(io.BytesIO(fetch("modern_conquest")))
    rows = read_xlsx(archive.read(SOURCES["modern_conquest"]["member"]))
    out = []
    for r in rows:
        year, until = number(r["year"]), number(r["helduntil"])
        if year is None or year < MC_FIRST or until is None:
            continue                                 # before 1946, or outcome not coded (Ukraine 2022)
        lost = None if until == -99 else until
        if lost is not None and r["held"] == "1" and number(r["regained"]) == lost:
            lost = None                              # lost and retaken within the same conflict year
        out.append({"key": r["acnum"], "year": year, "holder": r["perp"], "from": r["victim"],
                    "territory": r["territory"].strip(), "lost": lost,
                    "how": HOW.get(r["losstype"], "") if lost is not None else "",
                    "initial": r["retaliatory"] == "0", "retake_only": r["retaliatoryx"] in ("1", "4"),
                    "perp": number(r["perpid"]), "vic": number(r["vicid"])})
    return out


def load_fighting() -> tuple[dict, dict, dict]:
    """Per UCDP conflict over territory: its active years, its label and, for interstate ones, the opposing pairs of states."""
    archive = zipfile.ZipFile(io.BytesIO(fetch("ucdp_acd")))
    name = next(n for n in archive.namelist() if n.endswith(".csv"))
    years, label, states = defaultdict(set), {}, {}
    for r in csv.DictReader(io.StringIO(archive.read(name).decode("utf-8-sig"))):
        if r["incompatibility"] not in ("1", "3"):
            continue
        cid = r["conflict_id"]
        years[cid].add(int(r["year"]))
        label[cid] = f"{r['territory_name']} ({r['location']})"
        if r["type_of_conflict"] == "2":                # primary parties only: supporters are not opponents
            side_a = {int(c) for c in re.findall(r"\d+", r["gwno_a"])}
            side_b = {int(c) for c in re.findall(r"\d+", r["gwno_b"])}
            states.setdefault(cid, set()).update((x, y) for x in side_a for y in side_b)
    return years, label, states


def simulate(taken: int, lost: int | None, fighting: set[int], wait: int, last: int) -> tuple[int | None, str]:
    """Year the canon accepts the new holder (or None) and one letter per year from `taken` to `last`.

    b: seized and lost within the year, f: unsettled, fighting, w: unsettled, quiet, clock running,
    A: accepted, F: accepted, fighting again, x: control ended.
    """
    accepted, clock, track = None, 0, ""
    for year in range(taken, last + 1):
        if lost is not None and year >= lost:
            track += "b" if lost == taken else "x"
            break
        active = year in fighting
        if year == taken:                            # the year of the seizure never counts as a quiet year
            track += "f" if active else "w"
        elif accepted is not None:
            track += "F" if active else "A"
        else:
            clock = 0 if active else clock + 1
            if clock >= wait:
                accepted = year
                track += "A"
            else:
                track += "f" if active else "w"
    return accepted, track


def run_cases(cases: list[dict], last: int) -> dict:
    """Aggregate the rule's behaviour over `cases` for every waiting time, with and without the conflict data."""
    out = {}
    for clock_name in ("quiet", "plain"):
        per_wait = {}
        for wait in WAITS:
            tally = Counter()
            undone = []
            for c in cases:
                fighting = c["fighting"] if clock_name == "quiet" else set()
                accepted, track = simulate(c["year"], c["lost"], fighting, wait, last)
                c.setdefault(clock_name, {})[wait] = {"accepted": accepted, "track": track}
                tally["unsettled_year_ends"] += sum(track.count(x) for x in "fw")
                if accepted is None:
                    tally["never_accepted_lost_first" if c["lost"] is not None else "still_unsettled"] += 1
                    continue
                tally["accepted"] += 1
                if c["lost"] is not None:
                    tally[f"undone_{c['how']}"] += 1
                    tally["undone"] += 1
                    if c["lost"] - accepted <= 10:
                        tally["undone_within_10_years"] += 1
                    undone.append(f"{c['label']} (accepted {accepted}, ended {c['lost']}, {c['how']})")
            per_wait[str(wait)] = dict(sorted(tally.items())) | {"undone_cases": undone}
        out[clock_name] = per_wait
    out["clocks_differ"] = {
        str(w): sorted(c["label"] for c in cases if c["quiet"][w]["accepted"] != c["plain"][w]["accepted"])
        for w in WAITS}
    out["decided_differently"] = {}
    for a, b in zip(WAITS, WAITS[1:]):
        changed = []
        for c in cases:
            ya, yb = c["quiet"][a]["accepted"], c["quiet"][b]["accepted"]
            if (ya is None) != (yb is None):
                end = f"ended {c['lost']}, {c['how']}" if c["lost"] is not None else f"still held in {last}"
                changed.append(f"{c['label']}: accepted {ya} at T={a}, not at T={b}; {end}")
        out["decided_differently"][f"{a}->{b}"] = changed
    return out


def main() -> None:
    fight_years, fight_label, fight_states = load_fighting()
    links = defaultdict(dict)
    for r in csv.DictReader((ROOT / "inputs" / "links.csv").open(encoding="utf-8")):
        ids = r["ucdp_conflict_ids"].split(";")
        missing = [i for i in ids if i not in fight_years]
        if missing:
            raise SystemExit(f"links.csv: no UCDP territorial conflict {missing} for {r['key']}")
        links[r["source"]][r["key"]] = ids

    # Seizures by states. A seizure is linked to the territorial conflicts between the same two states;
    # links.csv adds the conflicts that UCDP codes against a non-state side.
    conquests = load_conquests()
    for c in conquests:
        ids = [cid for cid, pairs in fight_states.items() if (c["perp"], c["vic"]) in pairs or (c["vic"], c["perp"]) in pairs]
        ids += links["mc"].get(c["key"], [])
        c["ucdp"] = sorted(set(ids), key=int)
        c["fighting"] = set().union(*(fight_years[i] for i in c["ucdp"])) if c["ucdp"] else set()
        c["label"] = f"{c['territory']} ({c['holder']} from {c['from']}, {c['year']})"
    seizures = [c for c in conquests if c["initial"]]
    result_seizures = run_cases(seizures, MC_LAST)

    # Breakaway entities.
    breakaways = []
    for r in csv.DictReader((ROOT / "inputs" / "defacto_states.csv").open(encoding="utf-8")):
        ids = links["florea"].get(r["name"], [])
        how = {"forceful reintegration": "force", "peaceful reintegration": "agreed",
               "statehood": "statehood"}.get(r["type"], "")
        breakaways.append({"key": r["name"], "label": f"{r['name']} ({r['emergence']})", "year": int(r["emergence"]),
                           "lost": int(r["disappearance"]) if r["disappearance"] else None, "how": how,
                           "ucdp": ids, "fighting": set().union(*(fight_years[i] for i in ids)) if ids else set()})
    result_breakaways = run_cases(breakaways, FLOREA_LAST)

    # Areas still held at the end of the conquest data, including those taken during a war already under way;
    # pure retakes of what had just been seized are not changes of holder.
    held_now = [c for c in conquests if c["lost"] is None and not c["retake_only"]]
    run_cases([c for c in held_now if not c["initial"]], MC_LAST)
    picture = []
    for c in sorted(held_now, key=lambda c: (c["year"], int(c["key"]))):
        years = {str(w): c["quiet"][w]["accepted"] for w in WAITS}
        if any(y is None for y in years.values()):
            picture.append({"case": c["label"], "accepted_in": years, "fighting_years": sorted(c["fighting"] & set(range(c["year"], MC_LAST + 2)))})

    # Showcase timelines.
    by_key = {("mc", c["key"]): c for c in conquests} | {("florea", b["key"]): b for b in breakaways}
    showcase = []
    for r in csv.DictReader((ROOT / "inputs" / "showcase.csv").open(encoding="utf-8")):
        c = by_key[(r["source"], r["key"])]
        if "quiet" not in c:
            run_cases([c], MC_LAST)
        for w in WAITS:
            showcase.append({"label": r["label"], "source": r["source"], "key": r["key"], "taken": c["year"],
                             "ended": c["lost"] or "", "how": c["how"], "T": w,
                             "accepted": c["quiet"][w]["accepted"] or "", "track": c["quiet"][w]["track"]})

    out = ROOT / "outputs"
    out.mkdir(exist_ok=True)
    with (out / "seizures.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(["acnum", "year", "holder", "from", "territory", "ended", "how", "ucdp_conflicts"]
                        + [f"accepted_T{w}" for w in WAITS] + [f"plain_T{w}" for w in WAITS])
        for c in seizures:
            writer.writerow([c["key"], c["year"], c["holder"], c["from"], c["territory"], c["lost"] or "", c["how"],
                             ";".join(c["ucdp"])] + [c["quiet"][w]["accepted"] or "" for w in WAITS]
                            + [c["plain"][w]["accepted"] or "" for w in WAITS])
    with (out / "breakaways.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(["name", "emergence", "ended", "how", "ucdp_conflicts"]
                        + [f"accepted_T{w}" for w in WAITS] + [f"plain_T{w}" for w in WAITS])
        for b in breakaways:
            writer.writerow([b["key"], b["year"], b["lost"] or "", b["how"], ";".join(b["ucdp"])]
                            + [b["quiet"][w]["accepted"] or "" for w in WAITS]
                            + [b["plain"][w]["accepted"] or "" for w in WAITS])
    with (out / "showcase.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(showcase[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(showcase)

    lost_after = Counter(c["lost"] - c["year"] for c in seizures if c["lost"] is not None)
    summary = {
        "sources": {k: {"url": v["url"], "sha256": v["sha256"]} for k, v in SOURCES.items()},
        "seizures_by_states": {
            "cases": len(seizures), "period": f"{MC_FIRST}-{MC_LAST}",
            "still_held": sum(c["lost"] is None for c in seizures),
            "ended_years_after_seizure": {str(k): lost_after[k] for k in sorted(lost_after)},
            "linked_to_conflict_data": sum(bool(c["ucdp"]) for c in seizures),
            **result_seizures},
        "breakaway_entities": {
            "cases": len(breakaways), "period": f"1945-{FLOREA_LAST}",
            "linked_to_conflict_data": sum(bool(b["ucdp"]) for b in breakaways),
            **result_breakaways},
        "held_at_end_of_data_not_accepted_under_some_T": picture,
        "linked_conflicts": {cid: fight_label[cid] for cid in sorted({i for c in conquests + breakaways for i in c["ucdp"]}, key=int)},
    }
    (out / "summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    for name, res, n in (("Seizures by states", result_seizures, len(seizures)), ("Breakaway entities", result_breakaways, len(breakaways))):
        print(f"{name} (n={n})")
        for w in WAITS:
            t = res["quiet"][str(w)]
            print(f"  T={w:2d}: accepted {t.get('accepted', 0):2d}, undone {t.get('undone', 0):2d} "
                  f"(force {t.get('undone_force', 0)}, within 10y {t.get('undone_within_10_years', 0)}), "
                  f"never accepted {t.get('never_accepted_lost_first', 0):2d}, still unsettled {t.get('still_unsettled', 0):2d}, "
                  f"unsettled year-ends {t['unsettled_year_ends']}")


if __name__ == "__main__":
    main()
