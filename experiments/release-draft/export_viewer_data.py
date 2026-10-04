#!/usr/bin/env python3
"""Write the data of the local map viewer (tools/map-viewer) from the rendered draft.

Reads the region polygons rendered by render_map.py (cache/map/regions.js), the release's regions.csv and
membership.csv, the Stage 1 list, the register of disputed areas, the entry-rule census and the canon's own
geometries; writes tools/map-viewer/public/data/regions.geojson and own_geometries.geojson. Each region carries a
plain explanation of why it is a region, with links to the rules, and the facts it rests on with their sources and
quoted passages. The output contains GADM-derived geometry and stays out of git (the viewer's .gitignore).

Run from the repository root: python3 experiments/release-draft/export_viewer_data.py
"""
import csv
import json
import math
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[1]
OUT = REPO / "tools" / "map-viewer" / "public" / "data"
GITHUB = "https://github.com/uncovering-world/travel-regions-extraction/blob/main/"

# Why a region exists, in plain words, by the basis the Stage 1 list gives it (experiments/stage1-list/run.py).
WHY = {
    "ISO 3166-1 entry": ("It has its own ISO 3166-1 code. Every ISO entry is a region.", ["R045"]),
    "registry: points of view differ": (
        "Countries' points of view disagree about whose land this is. A region never crosses a country boundary "
        "under any supported point of view, so the area is cut out and each user can choose a side.", ["R045", "D064"]),
    "residents; points of view differ (line dispute)": (
        "The parties draw the border in different places and civilians live between the lines, so the strip is a "
        "region of its own, cut along both lines.", ["R050", "D063"]),
    "residents; points of view differ": (
        "Another country claims it, a supported point of view shows the claim, and civilians live there.", ["R051"]),
    "residents; islet group": ("A disputed group of islets where civilians live.", ["R051"]),
    "residents; no single holder": (
        "A buffer, separation or demilitarised zone that no single party controls; civilians live there and the "
        "parties state its outline.", ["R052"]),
    "unclaimed land": ("Land that no country claims.", ["R058"]),
    "leased area held by the lessee": (
        "Leased to another state, which decides who may enter, and civilians live there. The land still counts to "
        "the lessor's country.", ["R053", "D057", "D058"]),
    "entry rule of the holder": (
        "Held by a party other than the country that claims it, and the holder runs its own entry rules for it "
        "along a line the parties state.", ["R048", "R056"]),
    "entry rule": (
        "An ordinary visitor needs a separate visa or permit to enter or stay, the rule covers the whole unit (a "
        "top-level unit, or a detached island or exclave with a rule written for it), and it has been in force at "
        "two yearly releases.", ["R044", "R056", "R055"]),
}
REGIME = {
    "permit_whole_territory": "a permit to enter the whole unit",
    "own_visa_system": "its own visa or entry permission",
    "separate_immigration_control": "its own immigration control",
    "visa_required_differs": "a different visa requirement",
    "tour_operator_only": "access only through a tour operator",
    "visa_exemption": "a visa exemption that the rest of the country does not have",
    "stay_limit": "a stay limit of its own",
}
EVIDENCE = {
    "registry": "taken from the reference lists (ISO 3166-1, Natural Earth)",
    "confirmed_primary": "confirmed in a primary source (the law or the authority itself)",
    "cited_secondary": "cited from a secondary source",
    "secondary": "from secondary sources",
    "primary": "from a primary source",
    "unconfirmed": "not confirmed: the passage was not found in the source",
    "conflicted": "sources conflict",
    "machine": "read by machine from a dataset",
}
AREA_FIELDS = ["kind", "parties", "holder", "holder_since", "on_the_ground", "origin", "inhabited", "traveller_access",
               "stated_outline", "area_km2"]
KIND = {
    "de_facto_state": "a state that controls its territory but is not widely recognised",
    "occupied_or_annexed": "held by a party that took it without the consent of the country it is attributed to",
    "line_position": "a dispute about where the border line runs",
    "paper_claim": "a claim on paper, without control",
    "islets_for_maritime_zone": "islets disputed mostly for their sea zones",
    "own_regime": "a zone with no single holder (buffer, demilitarised zone, condominium)",
    "lease_or_base": "a leased area or a foreign base",
    "unclaimed": "land no country claims",
    "resolved_recently": "a dispute resolved recently",
    "no_agreed_boundary": "a stretch where no boundary is agreed",
}

REGIME_NOTE = {
    "visa_exemption": "a visa exemption", "visa_requirement": "a visa requirement of its own",
    "permit_whole_territory": "a permit to enter", "own_visa_system": "its own visa or entry permission",
    "customs_or_tax_only": "customs or tax rules only", "transit_only": "a transit-only rule", "stay_limit": "a stay limit",
}
UNIT_NOTE = {
    "admin_unit": "an administrative unit", "zone_or_band": "a zone or border band", "site_list": "a list of places",
    "class_of_parcels": "a class of land parcels", "island": "an island", "de_facto_territory": "a de facto territory",
}


def note(text: str) -> str:
    """A Stage 1 marker in plain words."""
    m = re.match(r"entry rule that does not make a region: (\w+), (\w+)", text)
    if not m:
        return text
    regime, unit = m.groups()
    if regime in ("customs_or_tax_only", "transit_only"):
        why = "it does not change who may enter or stay (R056)"
    elif unit in ("zone_or_band", "site_list", "class_of_parcels"):
        why = "it covers a zone, a list of places or a class of land, not a whole unit (R056, item 6)"
    elif unit == "de_facto_territory":
        why = "the territory is treated by the register of disputed areas"
    else:
        why = "it fails a test of R056 or R055 (scope, a witness for independent visitors, or two yearly releases in force)"
    return f"Entry rule ({REGIME_NOTE.get(regime, regime)}, for {UNIT_NOTE.get(unit, unit)}); not a region because {why}."

PEOPLE = {"yes": "Civilians live there.", "no": "Nobody lives there.",
          "garrison_only": "Nobody lives there except soldiers or officials posted there."}
ACCESS = {"open": "A traveller can visit it.", "restricted": "A traveller can visit it only with permission or under conditions.",
          "closed": "It is closed to travellers.", "expedition_only": "Only organised expeditions can reach it."}


def why_not_region(text: str) -> str:
    """Why a special place or a note is not a region of its own, in plain words (from the Stage 1 list's reasons)."""
    if text.startswith("Entry rule ("):
        return text
    rules = [
        ("no resident civilians", "It is not a separate region because no civilians live there; its land counts to "
                                  "the region of whoever holds it (R051, R052)."),
        ("a dispute about a line", "It is not a separate region: the dispute is about where the border runs, and the "
                                   "land counts to the region of whoever holds it (R050)."),
        ("no stated outline", "It is not a separate region because no outline that the parties themselves state was "
                              "found, and the canon never draws one of its own (R047)."),
        ("leased; held by", "It is not a separate region: the land of a lease stays with the lessor's country unless "
                            "another state controls who enters and civilians live there (R053)."),
        ("residents unknown", "It is kept as a special place until a source says whether civilians live there (R051)."),
        ("claimed on paper", "It is only a note: the claim exists on paper, and none of the points of view the canon "
                             "supports shows it yet, so it creates no boundary (R051). Once the claimant's own point of "
                             "view is built (D064), this may change."),
        ("dispute resolved", "It is only a note: the dispute has been settled, and the canon follows the agreed outcome (R054)."),
        ("the line is moving", "It is only a note: control is changing along a line that nobody has stated, so no area "
                               "can be cut out; the regions it touches carry a flag (R049)."),
        ("no witness, no boundary", "It is only a note: no supported point of view separates it and no entry rule of "
                                    "its holder is recorded, so it stays inside its region (R057)."),
        ("covered by the ISO entry", "It is only a note: it lies inside a country or territory that is a region of its "
                                     "own anyway (R045)."),
    ]
    for key, plain in rules:
        if key in text:
            return plain
    return text


def story(name: str, facts: dict, rule: dict, why: str) -> list[dict]:
    """A short explanation for someone who hears of the place for the first time: what, who, what is on the
    ground, how it came about, people, visiting, and why it is shown as it is. Every sentence comes from a sourced
    fact or from the rules."""
    out = []
    if rule:
        out.append({"label": "What it is", "text": rule["rule_summary"]})
        if rule.get("affected_classes"):
            out.append({"label": "Who it applies to", "text": rule["affected_classes"]})
        if rule.get("since"):
            out.append({"label": "Since", "text": rule["since"]})
    else:
        if "kind" in facts:
            out.append({"label": "What it is", "text": f"{name}: {KIND.get(facts['kind'], facts['kind'])}."})
        if "parties" in facts:
            out.append({"label": "Who is involved", "text": facts["parties"]})
        if "holder" in facts:
            since = f" (since {facts['holder_since']})" if "holder_since" in facts else ""
            out.append({"label": "Who controls it", "text": facts["holder"] + since})
        if "on_the_ground" in facts:
            out.append({"label": "On the ground", "text": facts["on_the_ground"]})
        if "origin" in facts:
            out.append({"label": "How it came about", "text": facts["origin"]})
        people = PEOPLE.get(facts.get("inhabited", "").split(" ")[0], "")
        if "area_km2" in facts:
            try:
                size = f"{float(facts['area_km2']):,.0f}" if float(facts["area_km2"]) >= 10 else facts["area_km2"]
            except ValueError:
                size = facts["area_km2"]
            people = (people + f" About {size} km².").strip()
        if people:
            out.append({"label": "People", "text": people})
        if facts.get("traveller_access", "").split(" ")[0] in ACCESS:
            out.append({"label": "Visiting", "text": ACCESS[facts["traveller_access"].split(" ")[0]]})
    out.append({"label": "On this map", "text": why_not_region(why)})
    return out


def read(path: Path) -> list[dict]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def inside_ring(x: float, y: float, ring: list) -> bool:
    hit = False
    for (x1, y1), (x2, y2) in zip(ring, ring[1:]):
        if (y1 > y) != (y2 > y) and x < x1 + (y - y1) * (x2 - x1) / (y2 - y1):
            hit = not hit
    return hit


def polygons(geometry: dict) -> list:
    return [geometry["coordinates"]] if geometry["type"] == "Polygon" else geometry["coordinates"]


def locate(x: float, y: float, geometry: dict, bbox: tuple) -> bool:
    if not (bbox[0] <= x <= bbox[2] and bbox[1] <= y <= bbox[3]):
        return False
    return any(inside_ring(x, y, poly[0]) and not any(inside_ring(x, y, h) for h in poly[1:]) for poly in polygons(geometry))


def nearest(x: float, y: float, geometry: dict) -> float:
    """Distance in degrees (longitude scaled by latitude) to the closest vertex: enough to name the nearest region."""
    k = math.cos(math.radians(y))
    return min(math.hypot((px - x) * k, py - y) for poly in polygons(geometry) for ring in poly for px, py in ring)


def status(country: str, listed: str) -> str:
    """Whose the area is in the canon, and where it stands under the settling rule (R049), from the Stage 1 list."""
    out = [f"counted to {country}." if country and country != "none" else "counted to no country."]
    accepted = re.search(r"accepted (\d{4})", listed)
    if accepted:
        out.append(f"The holder's control was accepted under the settling rule in {accepted.group(1)}.")
    elif listed.startswith("unsettled"):
        out.append("Unsettled: " + listed.split(":", 1)[1].strip().split(";")[0] + ".")
    if "active conflict" in listed:
        out.append("Armed conflict over it is active (UCDP).")
    return " ".join(out)


def anchors() -> dict[str, str]:
    """GitHub links to the headings of rules and decisions (R045 -> docs/spec.md#r045--...)."""
    out = {}
    for doc in ("docs/spec.md", "docs/decisions.md"):
        for line in (REPO / doc).read_text(encoding="utf-8").splitlines():
            m = re.match(r"#+ ([RD]\d{3}) — ", line)
            if m:
                heading = line.lstrip("#").strip()
                slug = re.sub(r"[^\w\- ]", "", heading.lower()).replace(" ", "-")
                out[m.group(1)] = (GITHUB + doc + "#" + slug, heading.split(" — ", 1)[1].split(" [")[0])
    return out


def main() -> None:
    js = (ROOT / "cache" / "map" / "regions.js").read_text(encoding="utf-8")
    rendered = json.loads(js[js.index("{"): js.index(";\nwindow.MISSING")])
    geometry = {f["properties"]["id"]: f["geometry"] for f in rendered["features"]}
    rows = {r["region_id"]: r for r in read(ROOT / "release" / "regions.csv")}
    listed = {r["id"]: r for r in read(REPO / "experiments" / "stage1-list" / "outputs" / "regions.csv")}
    membership = read(ROOT / "release" / "membership.csv")
    a3 = {c["alpha_2"]: c["alpha_3"] for c in json.loads(Path("/usr/share/iso-codes/json/iso_3166-1.json").read_text())["3166-1"]}
    rules = anchors()

    sources = {s["source_id"]: s for s in read(REPO / "data" / "disputed-areas" / "sources.csv")}
    area_facts = defaultdict(list)
    for f in read(REPO / "data" / "disputed-areas" / "facts.csv"):
        if f["field"] in AREA_FIELDS:
            area_facts[f["area_id"]].append(f)
    links = {r["area_id"]: r for r in read(REPO / "experiments" / "stage1-list" / "inputs" / "links.csv")}
    census = {r["id"]: r for r in read(REPO / "data" / "entry-rules" / "census.csv")}
    rule_facts = defaultdict(list)
    for f in read(REPO / "data" / "entry-rules" / "facts.csv"):
        rule_facts[f["id"]].append(f)

    def source(sid: str) -> dict:
        s = sources.get(sid, {})
        return {"url": s.get("url", ""), "label": s.get("note", "") or s.get("url", "") or sid}

    def area_evidence(area_id: str) -> list[dict]:
        facts = sorted(area_facts.get(area_id, []), key=lambda f: AREA_FIELDS.index(f["field"]))
        return [{"field": f["field"].replace("_", " "),
                 "value": KIND.get(f["value"], f["value"]) if f["field"] == "kind" else f["value"],
                 "quote": f["quote"], "evidence": f["evidence"],
                 "sources": [source(s) for s in f["source_ids"].split()]} for f in facts]

    def rule_evidence(rule_id: str) -> list[dict]:
        c = census.get(rule_id)
        if not c:
            return []
        out = [{"field": "the rule", "value": c["rule_summary"], "quote": "", "evidence": c["evidence"],
                "sources": [{"url": c["source_url"], "label": c["source_url"]}] if c["source_url"] else []},
               {"field": "who it applies to", "value": c["affected_classes"], "quote": "", "evidence": c["evidence"], "sources": []},
               {"field": "in force since", "value": c["since"], "quote": "", "evidence": c["evidence"], "sources": []}]
        for f in rule_facts.get(rule_id, []):
            out.append({"field": f["field"].replace("_", " "), "value": f["value"], "quote": f["quote"],
                        "evidence": f["evidence"], "sources": [{"url": f["source_url"], "label": f["source_url"]}]})
        return out

    # which regions take land out of which: a region whose GADM unit lies inside another region's unit, or whose
    # own geometry is clipped from it
    includes = defaultdict(set)
    for m in membership:
        if m["role"] == "include" and m["source"] == "GADM 4.1":
            includes[m["region_id"]].add(m["unit"])
    carved = defaultdict(set)
    for m in membership:
        for donor in m.get("clip_to", "").split():
            carved[donor].add(m["region_id"])
    for rid, units in includes.items():
        for other, theirs in includes.items():
            if other != rid and any(u != t and u.startswith(t + ".") for u in units for t in theirs):
                carved[other].add(rid)

    features = []
    for rid, geom in geometry.items():
        r = rows.get(rid, {})
        s = listed.get(rid, {})
        povs = {k[5:]: v for k, v in r.items() if k.startswith("view_")}   # each party's point of view (D064-D069)
        povs["__canon"] = r.get("country_code", "")
        basis = s.get("basis", r.get("basis", ""))
        key = "entry rule" if basis.startswith("entry rule:") else basis
        text, refs = WHY.get(key, ("", []))
        if basis.startswith("entry rule:"):
            kind = basis.split(":", 1)[1].strip()
            text += f" Here: {REGIME.get(kind, kind.replace('_', ' '))}."
        area_id = rid.split("/", 1)[1] if rid.startswith("area/") else ""
        rule_id = rid.split("/", 1)[1] if rid.startswith("rule/") else links.get(area_id, {}).get("census_id", "")
        units = [f"{m['role']} {m['source']} {m['unit']}" + (f" (clip to {m['clip_to']})" if m.get("clip_to") else "")
                 for m in membership if m["region_id"] == rid]
        features.append({"type": "Feature", "geometry": geom, "properties": {
            "id": rid, "name": r.get("name", rid), "country": r.get("country", ""), "country_code": r.get("country_code", ""),
            "basis": basis, "why": text, "rules": [{"id": x, "url": rules[x][0], "title": rules[x][1]} for x in refs if x in rules],
            "status": status(r.get("country", ""), s.get("country", "")) if rid.startswith("area/") else "",
            "evidence": r.get("evidence", ""), "evidence_text": EVIDENCE.get(r.get("evidence", ""), r.get("evidence", "")),
            "open": r.get("open", ""), "wikidata_id": r.get("wikidata_id", ""), "povs": povs,
            "facts": (area_evidence(area_id) if area_id else []) + (rule_evidence(rule_id) if rule_id else []),
            "carved": sorted(carved.get(rid, set())), "units": units[:20]}})
    # for a country, also the separate regions the canon counts to it, or that some point of view counts to it
    props = {f["properties"]["id"]: f["properties"] for f in features}
    for f in features:
        p = f["properties"]
        related = {c: "taken out of its land" for c in p["carved"]}
        mine = p["id"] if re.fullmatch(r"[A-Z]{2}", p["id"]) else ""
        for other, q in props.items():
            if other == p["id"] or re.fullmatch(r"[A-Z]{2}", other) or not mine:
                continue
            views = sorted(k for k, v in q["povs"].items() if v == mine and not k.startswith("__"))
            if q["country_code"] == p["id"]:
                related.setdefault(other, "the canon counts it to this country")
            elif views:
                total = sum(1 for k in q["povs"] if not k.startswith("__"))
                who = ", ".join(views) if len(views) <= 5 else f"{len(views)} of the {total}"
                related.setdefault(other, f"counted to this country under the points of view of {who}")
        p["carved"] = [{"id": c, "name": props.get(c, {}).get("name", c), "how": how} for c, how in sorted(related.items())]
    # special places and markers (R046), placed by their Wikidata point (inputs/place_points.csv)
    points = {r["id"]: r for r in read(ROOT / "inputs" / "place_points.csv") if r["use"] == "yes"}
    listed_dir = REPO / "experiments" / "stage1-list" / "outputs"
    items = [{"id": r["id"].split("/", 1)[1], "name": r["name"], "what": "special place", "why": r["why"]}
             for r in read(listed_dir / "special_places.csv")]
    items += [{"id": r["area_id"], "name": r["name"], "what": "note", "why": note(r["marker"])}
              for r in read(listed_dir / "markers.csv")]
    for it in items:
        facts = {f["field"]: f["value"] for f in area_facts.get(it["id"], [])}
        it["story"] = story(it["name"], facts, census.get(it["id"], {}), it["why"])
        it["why"] = why_not_region(it["why"])
        it["facts"] = area_evidence(it["id"]) if it["id"] in area_facts else rule_evidence(it["id"])
    boxes = {}
    for f in features:
        xs = [c[0] for poly in polygons(f["geometry"]) for c in poly[0]]
        ys = [c[1] for poly in polygons(f["geometry"]) for c in poly[0]]
        boxes[f["properties"]["id"]] = (min(xs), min(ys), max(xs), max(ys))
    places, unplaced = [], []
    for it in items:
        pt = points.get(it["id"])
        country = census.get(it["id"], {}).get("iso_code", "")
        if not pt and country in props:
            # an entry rule for a list of places or a class of land: listed with its country, without a point
            props[country].setdefault("inside", []).append({**it, "region": country, "where": "in this country, no single point"})
            continue
        if not pt:
            unplaced.append(it)
            continue
        x, y = float(pt["lon"]), float(pt["lat"])
        hits = [f["properties"]["id"] for f in features if locate(x, y, f["geometry"], boxes[f["properties"]["id"]])]
        if hits:
            region, where = hits[0], "inside"
        else:
            region = min(features, key=lambda f: nearest(x, y, f["geometry"]))["properties"]["id"]
            where = "nearest region (the point is off land)"
        entry = {**it, "region": region, "where": where, "wikidata_id": pt["wikidata_id"], "wd_label": pt["wd_label"],
                 "link": pt["link"]}
        places.append({"type": "Feature", "geometry": {"type": "Point", "coordinates": [x, y]}, "properties": entry})
        props[region].setdefault("inside", []).append(entry)
    for p in props.values():
        p["inside_count"] = len(p.get("inside", []))

    # the own geometries as clipped to their donors (render_map.py), else as published
    clipped_path = ROOT / "cache" / "map" / "own_pieces.json"
    clipped = json.loads(clipped_path.read_text(encoding="utf-8")) if clipped_path.exists() else {}
    own = []
    for s in read(REPO / "data" / "custom-geometries" / "sources.csv"):
        data = json.loads((REPO / "data" / "custom-geometries" / s["file"]).read_text(encoding="utf-8"))
        shapes = [clipped[s["file"]]] if s["file"] in clipped else [f["geometry"] for f in data["features"]]
        for g in shapes:
            own.append({"type": "Feature", "geometry": g, "properties": {
                k: s[k] for k in ("place", "region", "rank", "whose_line", "publisher", "licence", "source_url", "notes")}})
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "regions.geojson").write_text(json.dumps({"type": "FeatureCollection", "features": features}, ensure_ascii=False))
    (OUT / "places.geojson").write_text(json.dumps({"type": "FeatureCollection", "features": places, "unplaced": unplaced},
                                                   ensure_ascii=False))
    (OUT / "own_geometries.geojson").write_text(json.dumps({"type": "FeatureCollection", "features": own}, ensure_ascii=False))
    print(f"{len(features)} regions, {len(own)} own geometry features, {len(places)} placed special places and notes "
          f"({len(unplaced)} without a location) -> {OUT}")


if __name__ == "__main__":
    main()
