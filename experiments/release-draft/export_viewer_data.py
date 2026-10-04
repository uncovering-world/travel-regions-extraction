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
AREA_FIELDS = ["kind", "parties", "holder", "holder_since", "on_the_ground", "inhabited", "traveller_access",
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


def read(path: Path) -> list[dict]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


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
        povs = {k[4:]: v for k, v in r.items() if k.startswith("pov_")}
        povs["__canon_a3"] = a3.get(r.get("country_code", ""), "")
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
        mine = a3.get(p["id"], "") if re.fullmatch(r"[A-Z]{2}", p["id"]) else ""
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
    own = []
    for s in read(REPO / "data" / "custom-geometries" / "sources.csv"):
        data = json.loads((REPO / "data" / "custom-geometries" / s["file"]).read_text(encoding="utf-8"))
        for f in data["features"]:
            own.append({"type": "Feature", "geometry": f["geometry"], "properties": {
                k: s[k] for k in ("place", "region", "rank", "whose_line", "publisher", "licence", "source_url", "notes")}})
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "regions.geojson").write_text(json.dumps({"type": "FeatureCollection", "features": features}, ensure_ascii=False))
    (OUT / "own_geometries.geojson").write_text(json.dumps({"type": "FeatureCollection", "features": own}, ensure_ascii=False))
    print(f"{len(features)} regions, {len(own)} own geometry features -> {OUT}")


if __name__ == "__main__":
    main()
