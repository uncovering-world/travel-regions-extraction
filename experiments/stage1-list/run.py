#!/usr/bin/env python3
"""Stage 1 as a list under the rules decided on 2026-10-03: regions, special places, markers and missing facts. Issue #22.

Inputs: the first world draft's registry cells and census of entry rules, the register of disputed areas,
inputs/links.csv, which ties register areas to ISO entries, registry cells and census rows, and
data/entry-rules/ (census.csv and facts.csv: the living census of entry rules and what their texts say, with quoted passages).
Run from the repository root: python3 experiments/stage1-list/run.py
"""
from __future__ import annotations

import csv
import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[1]
DRAFT = REPO / "experiments" / "stage1-world-draft"
SPECIAL = {"line_position", "no_agreed_boundary"}             # never regions
BY_RESIDENTS = {"islets_for_maritime_zone", "own_regime"}     # region if civilians live there
BY_CONTROL = {"de_facto_state", "occupied_or_annexed"}        # settling rule decides whose; other rules decide separateness
NOT_A_WITNESS = {"none", "customs_or_tax_only", "transit_only"}
CITED = {"confirmed_primary", "cited_secondary"}
GROUP_ONLY = re.compile(r"in approved tour groups|^tour groups", re.I)   # a rule for organised groups only is not a witness
RELEASE_YEAR = 2025
WAIT = 3                                                      # quiet years before a new holder is accepted                                           # a rule must hold at the ends of 2024 and 2025


def read(path: Path) -> list[dict]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def main() -> None:
    cells = read(DRAFT / "outputs" / "cells.csv")
    census = {r["id"]: r for r in read(REPO / "data" / "entry-rules" / "census.csv")}
    areas = read(REPO / "data" / "disputed-areas" / "registry.csv")
    links = {r["area_id"]: r for r in read(ROOT / "inputs" / "links.csv")}
    not_witness = {r["id"] for r in read(ROOT / "inputs" / "not_a_witness.csv")}
    lease_roles = {r["area_id"]: r for r in read(ROOT / "inputs" / "lease_holders.csv")}
    no_outline = {r["area_id"] for r in read(ROOT / "inputs" / "no_outline.csv")}   # R047: no stated line, no cell
    # D064-D069: a point of view is a party's sourced claims; inputs/claims.csv reads the register's facts into codes
    claims = {r["area_id"]: r for r in read(ROOT / "inputs" / "claims.csv")}

    def claimed(area_id: str) -> bool:
        """Whether a party other than the holder claims the area (D065): some point of view puts it in another country."""
        c = claims.get(area_id, {})
        return bool(set(c.get("claimants", "").split()) - set(c.get("renounced", "").split()))
    held: dict[str, dict] = {}
    for r in read(REPO / "data" / "disputed-areas" / "facts.csv"):
        if r["field"] in ("holder", "holder_since", "stated_outline"):
            held.setdefault(r["area_id"], {})[r["field"]] = r["value"]
    rule_facts: dict[str, dict] = {}
    for r in read(REPO / "data" / "entry-rules" / "facts.csv"):
        rule_facts.setdefault(r["id"], {}).setdefault(r["field"], r["value"])
    known = {a["area_id"] for a in areas}
    registry = {c["cell"]: c for c in cells if c["kind"] == "registry_extra"}
    small = {r["name"] for r in read(DRAFT / "outputs" / "skipped.csv") if r["reason"] == "below_resolution"}
    sys.path.insert(0, str(REPO / "experiments" / "settling-rule"))
    import run as settling                                    # the pinned UCDP data and the clock
    fight_years, _, _ = settling.load_fighting()
    conflicts = {r["area_id"]: [i for i in r["ucdp_conflict_ids"].split(";") if i]
                 for r in read(REPO / "data" / "disputed-areas" / "ucdp-links.csv")}
    for link in links.values():
        assert link["area_id"] in known, link["area_id"]
        assert not link["registry_cell"] or link["registry_cell"] in registry, link["registry_cell"]
        assert not link["small_feature"] or link["small_feature"] in small, link["small_feature"]
        assert not link["census_id"] or link["census_id"] in census, link["census_id"]

    regions, places, markers, gaps, lead = [], [], [], [], []
    for c in cells:
        if c["kind"] == "iso":
            regions.append({"id": c["cell"], "name": c["name"], "basis": "ISO 3166-1 entry", "country": c["cell"],
                            "evidence": "registry", "open": ""})

    def entry_rule(row: dict) -> tuple[bool, list[str]]:
        """Whether a census row can separate under the decided rules, and what is still missing to say so."""
        missing = []
        if row["id"] in not_witness:
            return False, []
        known = rule_facts.get(row["id"])
        if known is not None:                                  # checked against the text of the rule
            if row["regime_kind"] in NOT_A_WITNESS or GROUP_ONLY.search(row["affected_classes"]):
                return False, []
            if known.get("in_force") == "no" or row["whole_named_unit"] == "no":
                return False, []
            top = known.get("unit_level") == "top_level"
            own_detached = known.get("detached") in ("island", "exclave") and known.get("own_rule") == "own"
            if "unit_level" not in known or ("detached" not in known and not top):
                missing.append("level of the unit or whether it is detached")
            elif not (top or own_detached):
                return False, []
            if "in_force" not in known:
                missing.append("not confirmed in force")
            years = re.findall(r"(1[5-9]\d\d|20[0-2]\d)", known.get("start_date", "") or row["since"])
            if not years:
                missing.append("start date of the rule")
            elif min(map(int, years)) > RELEASE_YEAR - 1:
                return False, []
            return True, missing
        if row["regime_kind"] in NOT_A_WITNESS or GROUP_ONLY.search(row["affected_classes"]):
            return False, []
        if row["whole_named_unit"] != "yes" or row["unit_kind"] in ("zone_or_band", "site_list", "class_of_parcels"):
            return False, []
        if row["evidence"] not in CITED:
            missing.append("no cited source for the rule")
        if row["in_force_2026"] != "yes":
            missing.append("not confirmed in force")
        years = re.findall(r"(1[5-9]\d\d|20[0-2]\d)", row["since"])
        if not years:
            missing.append("start date of the rule")
        elif min(map(int, years)) > RELEASE_YEAR - 1:
            return False, []                                   # younger than two yearly releases
        if row["unit_kind"] == "admin_unit":
            missing.append("whether the unit is a top-level unit of its country")
        elif row["unit_kind"] == "island":
            missing.append("whether the rule is written for this place or is a line in a list")
        return True, missing

    used_cells, used_census = set(), set()
    for a in areas:
        link = links.get(a["area_id"], {})
        kind, lives = a["kind"], a["inhabited"]
        cell, rule = link.get("registry_cell", "") or link.get("small_feature", ""), link.get("census_id", "")
        used_cells.add(cell)
        used_census.add(rule)
        differ = claimed(a["area_id"])                        # D065: claims decide; Natural Earth is only a lead
        if bool(cell or link.get("pov_feature")) != differ:
            lead.append({"area_id": a["area_id"], "name": a["name"], "kind": a["kind"],
                         "natural_earth": cell or link.get("pov_feature", ""), "claimants": claims.get(a["area_id"], {}).get("claimants", ""),
                         "finding": "Natural Earth separates it but no claim is recorded" if not differ
                                    else "a claim is recorded but Natural Earth does not separate it"})

        def gap(fact: str, consequence: str) -> None:
            gaps.append({"area_id": a["area_id"], "name": a["name"], "kind": kind, "missing": fact, "undecided": consequence})

        def region(basis: str, country: str, pending: str = "") -> None:
            regions.append({"id": "area/" + a["area_id"], "name": a["name"], "basis": basis, "country": country,
                            "evidence": a["weakest_evidence"] or "none", "open": pending})

        def place(why: str) -> None:
            places.append({"id": "place/" + a["area_id"], "name": a["name"], "kind": kind, "why": why})

        whole = link.get("part_of", "")
        if whole and {k: claims.get(a["area_id"], {}).get(k) for k in ("holder", "claimants")} == \
                {k: claims.get(whole, {}).get(k) for k in ("holder", "claimants")}:
            # under every point of view it belongs where the area it is part of belongs (R045): no boundary of its own
            markers.append({"area_id": a["area_id"], "name": a["name"], "marker": f"part of the area {whole}, with the same holder and claims; it goes with that area's region"})
        elif not kind:
            gap("kind", "everything")
        elif a["area_id"] in no_outline:
            place("no stated outline found (R047, D061)")
        elif link.get("iso"):
            # the area is, or lies inside, an ISO entry: that entry is the region (Antarctica is one cell, D040);
            # a registry cell inside it still separates
            markers.append({"area_id": a["area_id"], "name": a["name"], "marker": f"covered by the ISO entry {link['iso']}; {kind}"})
            # a claim to a whole ISO entry changes only whose it is under the claimant's view, not any boundary; a part
            # of an entry separates when one party with a view other than the entry holds it (the canon's own
            # attribution, R045); Antarctica stays one cell (D040)
            holder = claims.get(a["area_id"], {}).get("holder", "")
            part = not link["basis"].startswith("own ISO entry") and link["iso"] != "AQ"
            if part and holder not in ("", "none", "unclear") and not holder.startswith("split") and holder != link.get("entry_holder", ""):
                h = held.get(a["area_id"], {})
                region("registry: points of view differ", f"held by {h.get('holder', '?')} since {h.get('holder_since', '?')}", "" if h else "who holds it")
        elif kind == "line_position" and differ and lives == "yes":
            # D063: a line dispute takes the residents test when a supported point of view differs
            h = held.get(a["area_id"], {})
            region("residents; points of view differ (line dispute)", h.get("holder", "holder"))
        elif kind in SPECIAL:
            place("a dispute about a line or an undelimited stretch; the land goes with whoever holds it")
        elif kind == "unclaimed":
            region("unclaimed land", "none")
        elif kind == "resolved_recently":
            markers.append({"area_id": a["area_id"], "name": a["name"], "marker": "dispute resolved; outcome taken over"})
        elif kind in BY_RESIDENTS or kind == "paper_claim":
            if kind == "paper_claim" and not differ:
                markers.append({"area_id": a["area_id"], "name": a["name"], "marker": "claimed on paper, but no claim of a party with a point of view is recorded (D065)"})
            elif lives == "yes":
                region("residents; " + ("points of view differ" if kind == "paper_claim" else "no single holder" if kind == "own_regime" else "islet group"),
                       "none" if kind == "own_regime" else "holder", "" if kind == "own_regime" else "who holds it")
            elif lives in ("no", "garrison_only"):
                place("no resident civilians")
            else:
                place("residents unknown: treated as a special place until sourced")
                gap("whether civilians live there", "region or special place")
        elif kind == "lease_or_base":
            # R053 as amended by D057 and D058: a region when its holder (R048) is a state other than the lessor
            # and civilians live there
            role = lease_roles.get(a["area_id"], {}).get("holder_role", "")
            if role == "lessee" and a["inhabited"] == "yes":
                region("leased area held by the lessee", "the lessor; held by " + held.get(a["area_id"], {}).get("holder", "?")[:60])
            elif differ and a["inhabited"] == "yes":           # a claim on a lease takes the residents test (D058)
                region("registry: points of view differ", "per the registry")
            elif role:
                place(f"leased; held by the {role}")
            else:
                place("leased; holder not recorded")
                gap("who holds the area", "region or special place")
        elif kind in BY_CONTROL:
            h = held.get(a["area_id"], {})
            if "holder" in h and "holder_since" in h:
                since = re.search(r"(1[5-9]\d\d|20[0-2]\d)", h["holder_since"])
                if a["area_id"] in conflicts and since:
                    fighting = set().union(*(fight_years[i] for i in conflicts[a["area_id"]])) if conflicts[a["area_id"]] else set()
                    accepted, _ = settling.simulate(int(since.group(1)), None, fighting, WAIT, RELEASE_YEAR)
                    active = RELEASE_YEAR in fighting
                    whose = (f"{h['holder']} (accepted {accepted})" if accepted else f"unsettled: held by {h['holder']} since {since.group(1)}")
                    whose += "; active conflict" if active else ""
                    pending = ""
                else:
                    whose, pending = f"held by {h['holder']} since {h['holder_since']}", "quiet years not counted"
                    gap("the UCDP conflict about the area, or a year in holder_since", "whether the holder is accepted or the area is still unsettled")
            else:
                whose, pending = "by the settling rule", "who holds it and since when"
                gap("who holds the area and since when", "the country it is listed under")
            moving = h.get("stated_outline", "").startswith("none")
            # for an area another party holds, the holder's own entry rule is the witness; the test for units of
            # one country (top-level, or detached with its own rule) is not applied to it
            witness = bool(rule) and census[rule]["regime_kind"] not in NOT_A_WITNESS and census[rule]["evidence"] in CITED \
                and rule_facts.get(rule, {}).get("in_force", census[rule]["in_force_2026"]) == "yes"
            if moving:
                markers.append({"area_id": a["area_id"], "name": a["name"], "marker": "the line is moving: a flag on the regions it touches; " + whose})
            elif differ or witness:
                region("registry: points of view differ" if differ else "entry rule of the holder", whose, pending)
            else:
                markers.append({"area_id": a["area_id"], "name": a["name"], "marker": "no witness, no boundary: no claim of another party and no entry rule recorded, so it stays inside its region; " + whose})

    for cid, c in registry.items():
        if cid not in used_cells:
            regions.append({"id": cid, "name": c["name"], "basis": "registry: points of view differ", "country": "by the settling rule",
                            "evidence": "registry", "open": "not tied to a register area: its kind and residents are unknown"})
            gaps.append({"area_id": "", "name": cid, "kind": "", "missing": "the register area this registry cell corresponds to", "undecided": "region or special place"})

    for rid, row in sorted(census.items()):
        if rid in used_census:
            continue
        ok, missing = entry_rule(row)
        if ok:
            regions.append({"id": "rule/" + rid, "name": row["name"], "basis": "entry rule: " + row["regime_kind"], "country": row["iso_code"],
                            "evidence": row["evidence"], "open": "; ".join(missing)})
            for m in missing:
                gaps.append({"area_id": "", "name": row["name"], "kind": "entry_rule", "missing": m, "undecided": "region or object inside its region"})
        elif row["regime_kind"] not in ("none",):
            markers.append({"area_id": rid, "name": row["name"], "marker": "entry rule that does not make a region: " + row["regime_kind"] + ", " + row["unit_kind"]})

    out = ROOT / "outputs"
    out.mkdir(exist_ok=True)
    for name, rows in (("regions", regions), ("special_places", places), ("markers", markers), ("gaps", gaps),
                       ("natural_earth_lead", lead)):
        with (out / f"{name}.csv").open("w", encoding="utf-8", newline="") as handle:
            fields = list(rows[0]) if rows else ["area_id", "name", "kind", "natural_earth", "claimants", "finding"]
            writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
            writer.writeheader()
            writer.writerows(rows)
    firm = [r for r in regions if not r["open"]]
    summary = {
        "regions": len(regions), "regions_by_basis": dict(Counter(r["basis"].split(":")[0].split(";")[0] for r in regions).most_common()),
        "regions_with_nothing_open": len(firm), "regions_with_an_open_point": len(regions) - len(firm),
        "special_places": len(places), "special_places_by_kind": dict(Counter(p["kind"] for p in places).most_common()),
        "markers": len(markers), "gaps": len(gaps), "gaps_by_missing_fact": dict(Counter(g["missing"] for g in gaps).most_common()),
        "register_areas": len(areas), "register_areas_linked": len(links),
        "registry_cells": len(registry), "registry_cells_not_tied_to_an_area": sum(c not in used_cells for c in registry),
    }
    (out / "summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()
