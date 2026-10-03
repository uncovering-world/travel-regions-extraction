#!/usr/bin/env python3
"""World Stage 1 draft: registry cells plus cited CR-W splits. Count-only, no geometry.

Experiment for issue #22. Nothing here is the canon. Run from the repository root:

    python3 experiments/stage1-world-draft/run.py
"""
from __future__ import annotations

import csv
import hashlib
import math
import json
import sys
import urllib.request
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CACHE, INPUTS, OUTPUTS = ROOT / "cache", ROOT / "inputs", ROOT / "outputs"

# National points of view published by Natural Earth as ADM0_A3_<POV> columns.
# The UN and WB columns are empty (-99) in v5.1.2 and are not used.
POVS = ["AR", "BD", "BR", "CN", "DE", "EG", "ES", "FR", "GB", "GR", "ID", "IL", "IN", "IT", "JP", "KO",
        "MA", "NL", "NP", "PK", "PL", "PS", "PT", "RU", "SA", "SE", "TR", "TW", "UA", "US", "VN"]
# A feature smaller than this is below the draft's resolution: it is reported, not made a cell.
MIN_AREA_KM2 = (0, 100, 1000)
BASELINE_MIN_AREA = 100
# A disputed feature covering at least this share of its ISO entry is that entry, not a part of it.
WHOLE_ENTRY_SHARE = 0.8

PERSPECTIVE_SETS = {
    "iso_only": [],
    "ne_default": ["NE"],
    "all_povs": ["NE", *POVS],
}


def load_sources() -> dict:
    return json.loads((INPUTS / "sources.json").read_text())


def fetch(name: str, meta: dict) -> dict:
    """Return the parsed file, downloading it into cache/ if needed; warn on checksum drift."""
    path = CACHE / name
    if not path.exists():
        CACHE.mkdir(exist_ok=True)
        with urllib.request.urlopen(meta["url"]) as response:
            path.write_bytes(response.read())
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    if digest != meta["sha256"]:
        print(f"WARNING: {name} sha256 {digest} differs from recorded {meta['sha256']}", file=sys.stderr)
    return json.loads(path.read_text())


def read_csv(path: Path) -> list[dict]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def area_km2(geometry: dict) -> float:
    """Approximate area: shoelace on longitude/latitude scaled by cos(latitude). Good enough to rank sizes."""
    polygons = geometry["coordinates"] if geometry["type"] == "MultiPolygon" else [geometry["coordinates"]]
    total = 0.0
    for polygon in polygons:
        ring = polygon[0]
        twice = sum((x1 * y2 - x2 * y1) * math.cos(math.radians((y1 + y2) / 2)) for (x1, y1), (x2, y2) in zip(ring, ring[1:]))
        total += abs(twice) / 2
    return total * 111.32 ** 2


def features(collection: dict) -> list[dict]:
    return [{**f["properties"], "area_km2": area_km2(f["geometry"])} for f in collection["features"]]


def code(props: dict, perspective: str) -> str:
    """Attribution of a feature under one perspective, as Natural Earth states it."""
    value = props["ADM0_A3"] if perspective == "NE" else props[f"ADM0_A3_{perspective}"]
    return str(value)


def registry_cells(iso: list[dict], countries: list[dict], disputed: list[dict], perspectives: list[str],
                   min_area: float = BASELINE_MIN_AREA) -> tuple[list[dict], list[dict]]:
    """Coarsest set of cells refining ISO 3166-1 and each perspective's attribution.

    Every ISO entry is a cell. A Natural Earth feature becomes a further cell when at least one
    perspective attributes it to something other than the ISO entry that administers it by default.
    Features with the same administering entry and the same attribution under every perspective
    are one cell (R009: coarsest partition; D012: non-contiguity does not split).
    Returns (cells, skipped), where skipped lists features left out and why.
    """
    codes = {e["alpha_2"] for e in iso}
    cells = [{"cell": e["alpha_2"], "kind": "iso", "iso": e["alpha_2"], "name": e["name"], "members": "", "signature": "", "area_km2": ""}
             for e in iso]
    skipped: list[dict] = []
    if not perspectives:
        return cells, skipped
    a3_to_iso = {f["ADM0_A3"]: f["ISO_A2_EH"] for f in countries if f["ISO_A2_EH"] in codes}
    entry_area: dict[str, float] = {}
    for f in countries:
        if f["ISO_A2_EH"] in codes:
            entry_area[f["ISO_A2_EH"]] = max(entry_area.get(f["ISO_A2_EH"], 0.0), f["area_km2"])
    seen: set = set()
    groups: dict[tuple, list[dict]] = defaultdict(list)
    for feature in [*disputed, *(f for f in countries if f["ISO_A2_EH"] not in codes)]:
        if feature["NE_ID"] in seen:
            continue  # the same feature appears in both layers
        seen.add(feature["NE_ID"])
        home = a3_to_iso.get(feature["ADM0_A3"], "-")
        attributed = tuple(a3_to_iso.get(code(feature, p), code(feature, p)) for p in perspectives)
        if home != "-" and all(value == home for value in attributed):
            continue  # every perspective agrees with the administering ISO entry: no boundary
        if home != "-" and feature["area_km2"] >= WHOLE_ENTRY_SHARE * entry_area.get(home, math.inf):
            skipped.append({"name": feature["NAME"], "iso": home, "area_km2": round(feature["area_km2"]), "reason": "whole_iso_entry"})
            continue
        groups[(home, attributed)].append(feature)
    for (home, attributed), members in sorted(groups.items(), key=lambda item: (item[0][0], sorted(f["NAME"] for f in item[1]), item[0][1])):
        names = sorted({f["NAME"] for f in members})
        size = sum(f["area_km2"] for f in members)
        if size < min_area:
            skipped.append({"name": "; ".join(names), "iso": home, "area_km2": round(size), "reason": "below_resolution"})
            continue
        tally = Counter(attributed)
        cells.append({
            "cell": f"{home}/{'+'.join(names)}#{min(f['NE_ID'] for f in members)}", "kind": "registry_extra", "iso": home,
            "name": "; ".join(names), "members": "; ".join(sorted({f["NOTE_BRK"] for f in members if f.get("NOTE_BRK")})),
            "signature": " ".join(f"{k}:{v}" for k, v in sorted(tally.items(), key=lambda kv: (-kv[1], kv[0]))),
            "area_km2": round(size),
        })
    return cells, skipped


CRW_PROFILES = {
    # name: (transit, anchored, permit_convention, evidence levels admitted)
    "amended": (False, False, True, {"confirmed_primary", "cited_secondary"}),
    "raw": (True, True, True, {"confirmed_primary", "cited_secondary"}),
    "amended_no_permits": (False, False, False, {"confirmed_primary", "cited_secondary"}),
    "amended_confirmed_only": (False, False, True, {"confirmed_primary"}),
    "amended_any_evidence": (False, False, True, {"confirmed_primary", "cited_secondary", "unconfirmed", "conflicted"}),
}
ANCHORED_KINDS = {"zone_or_band", "site_list", "class_of_parcels"}
NEVER = {"customs_or_tax_only", "none"}


def crw_active(row: dict, profile: str) -> bool:
    transit, anchored, permits, evidence = CRW_PROFILES[profile]
    if row["in_force_2026"] != "yes" or row["regime_kind"] in NEVER or row["evidence"] not in evidence:
        return False
    if row["regime_kind"] == "transit_only" and not transit:
        return False
    if row["unit_kind"] in ANCHORED_KINDS and not anchored:
        return False
    if row["regime_kind"] == "permit_whole_territory" and not permits:
        return False
    return True


def crw_cells(rows: list[dict], profile: str, registry: list[dict]) -> list[dict]:
    """One cell per active scope that the registry does not already separate."""
    out = []
    for row in rows:
        if row["covered_by_registry"] == "yes" or not crw_active(row, profile):
            continue
        out.append({"cell": f"{row['iso_code']}/{row['id']}", "kind": "crw", "iso": row["iso_code"], "name": row["name"],
                    "members": row["rule_summary"], "signature": f"{row['regime_kind']} {row['unit_kind']} {row['evidence']}", "area_km2": ""})
    return out


def main() -> int:
    sources = load_sources()
    iso = read_csv(INPUTS / "iso3166-1.csv")
    countries = features(fetch("ne_10m_admin_0_countries.geojson", sources["ne_10m_admin_0_countries.geojson"]))
    disputed = features(fetch("ne_10m_admin_0_disputed_areas.geojson", sources["ne_10m_admin_0_disputed_areas.geojson"]))
    crw_path = INPUTS / "crw_scopes.csv"
    crw_rows = read_csv(crw_path) if crw_path.exists() else []

    summary: dict = {"inputs": {name: meta["sha256"] for name, meta in sources.items()}, "registry": {}, "crw": {}, "totals": {}}
    for name, perspectives in PERSPECTIVE_SETS.items():
        for min_area in MIN_AREA_KM2:
            cells, _ = registry_cells(iso, countries, disputed, perspectives, min_area)
            summary["registry"][f"{name}/min_area_{min_area}"] = len(cells)
    registry, skipped = registry_cells(iso, countries, disputed, PERSPECTIVE_SETS["all_povs"])
    summary["registry_baseline"] = {"perspectives": "all_povs", "min_area_km2": BASELINE_MIN_AREA, "cells": len(registry),
                                    "skipped": dict(Counter(s["reason"] for s in skipped))}
    for profile in CRW_PROFILES:
        extra = crw_cells(crw_rows, profile, registry)
        summary["crw"][profile] = {"cells": len(extra), "by_regime": dict(sorted(Counter(c["signature"].split()[0] for c in extra).items()))}
        summary["totals"][profile] = len(registry) + len(extra)
    baseline = [*registry, *crw_cells(crw_rows, "amended", registry)]
    per_iso = Counter(c["iso"] for c in baseline)
    summary["cells_per_iso_entry"] = {"entries_with_more_than_one_cell": {k: v for k, v in sorted(per_iso.items()) if v > 1 and k != "-"},
                                      "cells_outside_any_iso_entry": per_iso.get("-", 0)}
    summary["crw_share_of_baseline"] = round(sum(c["kind"] == "crw" for c in baseline) / len(baseline), 4)

    OUTPUTS.mkdir(exist_ok=True)
    (OUTPUTS / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    with (OUTPUTS / "cells.csv").open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["cell", "kind", "iso", "name", "members", "signature", "area_km2"], lineterminator="\n")
        writer.writeheader()
        writer.writerows(baseline)
    with (OUTPUTS / "skipped.csv").open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["name", "iso", "area_km2", "reason"], lineterminator="\n")
        writer.writeheader()
        writer.writerows(sorted(skipped, key=lambda s: (s["reason"], s["iso"], s["name"])))
    print(json.dumps({k: summary[k] for k in ("registry", "registry_baseline", "totals", "crw_share_of_baseline")}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
