#!/usr/bin/env python3
"""Quality checks of the rendered geometry (tools/map-viewer/public/data/regions.geojson), run after render_map.py.

Defects a reader sees on the map and that the release checks (check_cover.py, check_custom.py) do not catch:
  fragments  a small detached part of a region lying against another region (e.g. the substrate's own, misplaced copy
             of an exclave left behind by an own geometry); listed unless inputs/known_fragments.csv explains it;
  seams      parts of one region that touch each other instead of being one polygon (a line is drawn between them);
  slits      holes inside a region narrower than a couple of metres (a cut that the map draws as a line, not water);
  overlaps   land in two regions at once;
  slivers    thin gaps between regions (holes in the union of all regions that are long and narrow).
Overlaps and slivers are checked in the detail zones only, where the display is exact.
Writes cache/map/display_check.json and, for each finding, a box for check_screens.cjs to photograph.
Needs shapely and pyproj. Run from the repository root:
    python experiments/release-draft/check_display.py
"""
import csv
import json
import math
import sys
import time
from pathlib import Path

import shapely
from pyproj import Geod
from shapely.geometry import shape

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[1]
DATA = REPO / "tools" / "map-viewer" / "public" / "data" / "regions.geojson"
OUT = ROOT / "cache" / "map"
GEOD = Geod(ellps="WGS84")
FRAGMENT_KM2 = 50          # a detached part smaller than this ...
FRAGMENT_SHARE = 0.05      # ... and than this share of its region is a fragment
SLIVER_KM2 = (0.001, 50)   # gaps in this size range ...
SLIVER_SHAPE = 0.2         # ... with a compactness (4πA/P²) below this are slivers
OVERLAP_KM2 = 0.001
MARGIN = 0.2              # the detail zones of render_map.py
SLIT_WIDTH_M = 2          # a hole narrower than this is a cut, not a river or a lake
VISIBLE_KM2 = 0.05        # smaller fragments, overlaps and slivers are counted, not shown first


def log(message):
    print(time.strftime("%H:%M:%S"), message, file=sys.stderr, flush=True)


def wide(g, margin=0.05) -> list:
    """The bounds of g widened by margin degrees, for a screenshot (no buffer: g may be a large collection)."""
    x0, y0, x1, y1 = g.bounds
    return [round(x0 - margin, 4), round(y0 - margin, 4), round(x1 + margin, 4), round(y1 + margin, 4)]


def km2(g) -> float:
    return abs(GEOD.geometry_area_perimeter(g)[0]) / 1e6


def compactness(g) -> float:
    area, perimeter = GEOD.geometry_area_perimeter(g)
    return 4 * math.pi * abs(area) / perimeter ** 2 if perimeter else 0.0


def main() -> None:
    features = json.loads(DATA.read_text(encoding="utf-8"))["features"]
    regions = {f["properties"]["id"]: shapely.make_valid(shape(f["geometry"])) for f in features}
    names = {f["properties"]["id"]: f["properties"]["name"] for f in features}
    known_path = ROOT / "inputs" / "known_fragments.csv"
    known = {}
    if known_path.exists():
        with known_path.open(encoding="utf-8", newline="") as handle:
            known = {(r["region"], r["near"]): r["why"] for r in csv.DictReader(handle)}
    ids = sorted(regions)
    tree = shapely.STRtree([regions[i] for i in ids])
    log(f"{len(ids)} regions read")
    findings = []

    for rid in ids:
        g = regions[rid]
        parts = [p for p in getattr(g, "geoms", [g]) if p.geom_type == "Polygon"]
        # seams: parts of one region that share an edge (a valid multipolygon's parts meet at points at most)
        if len(parts) > 1:
            ptree = shapely.STRtree(parts)
            touching = 0
            for i, p in enumerate(parts):
                for j in ptree.query(p, predicate="intersects"):
                    if j > i and shapely.intersection(p, parts[j]).length > 0:
                        touching += 1
            if touching:
                findings.append({"check": "seam", "region": rid, "name": names[rid], "parts_touching": touching,
                                 "where": [round(g.centroid.x, 3), round(g.centroid.y, 3)], "box": [round(v, 4) for v in g.bounds]})
        # slits: zero-width cuts inside a region (an edge that runs inside the polygon and is drawn as a line); a hole
        # thinner than a few metres or a ring that touches itself along a line shows them
        for p in parts:
            for ring in p.interiors:
                hole = shapely.Polygon(ring)
                area, perimeter = GEOD.geometry_area_perimeter(hole)
                width = 2 * abs(area) / perimeter if perimeter else 0.0   # metres, for a long thin hole
                if 0 < width < SLIT_WIDTH_M:
                    c = hole.representative_point()
                    findings.append({"check": "slit", "region": rid, "name": names[rid], "km2": round(km2(hole), 5),
                                     "where": [round(c.x, 4), round(c.y, 4)], "box": wide(hole)})
        # fragments: small detached parts lying against another region
        total = km2(g)
        for p in parts:
            if len(parts) == 1:
                break
            a = km2(p)
            if a >= FRAGMENT_KM2 or a >= FRAGMENT_SHARE * total:
                continue
            neighbours = [ids[i] for i in tree.query(p.buffer(0.002), predicate="intersects") if ids[i] != rid]
            if not neighbours:
                continue                                   # an island on its own
            near = neighbours[0] if len(neighbours) == 1 else max(
                neighbours, key=lambda n: shapely.intersection(p.buffer(0.002), regions[n]).area)
            entry = {"check": "fragment", "region": rid, "name": names[rid], "km2": round(a, 3), "near": near,
                     "where": [round(p.centroid.x, 4), round(p.centroid.y, 4)], "box": wide(p)}
            if (rid, near) in known:
                entry["explained"] = known[(rid, near)]
            findings.append(entry)

    log("seams and fragments checked")
    # overlaps and slivers, checked in the detail zones (boxes 0.2° around every register region and own geometry,
    # as render_map.py draws them at full precision); elsewhere the display is simplified on purpose
    own = json.loads((DATA.parent / "own_geometries.geojson").read_text(encoding="utf-8"))["features"]
    boxes = [shapely.box(*regions[r].bounds).buffer(MARGIN, join_style="mitre") for r in ids if r.startswith("area/")]
    boxes += [shapely.box(*shape(f["geometry"]).bounds).buffer(MARGIN, join_style="mitre") for f in own]
    zones = shapely.union_all(boxes)
    zone_list = list(getattr(zones, "geoms", [zones]))
    log(f"{len(zone_list)} detail zones")
    for zi, zone in enumerate(zone_list):
        inside = {ids[k]: shapely.intersection(regions[ids[k]], zone) for k in tree.query(zone, predicate="intersects")}
        log(f"zone {zi}: {len(inside)} regions, box {[round(v, 1) for v in zone.bounds]}")
        inside = {r: g for r, g in inside.items() if not g.is_empty and g.area > 0}
        names_in = sorted(inside)
        local = shapely.STRtree([inside[r] for r in names_in])
        for a in names_in:
            for k in local.query(inside[a]):
                b = names_in[k]
                if b <= a:
                    continue
                inter = shapely.intersection(inside[a], inside[b])
                if inter.geom_type == "GeometryCollection":
                    inter = shapely.union_all([x for x in inter.geoms if x.area > 0]) if any(x.area > 0 for x in inter.geoms) else shapely.Polygon()
                if not inter.is_empty and inter.area > 0 and km2(inter) > OVERLAP_KM2:
                    c = inter.representative_point()
                    findings.append({"check": "overlap", "region": a, "other": b, "km2": round(km2(inter), 4),
                                     "where": [round(c.x, 4), round(c.y, 4)], "box": wide(inter)})
        union = shapely.union_all(list(inside.values()))
        for poly in getattr(union, "geoms", [union]):
            if poly.geom_type != "Polygon":
                continue
            for ring in poly.interiors:
                hole = shapely.Polygon(ring)
                a = km2(hole)
                if SLIVER_KM2[0] <= a <= SLIVER_KM2[1] and compactness(hole) < SLIVER_SHAPE:
                    c = hole.representative_point()
                    around = sorted({names_in[k] for k in local.query(hole.buffer(0.002))})
                    findings.append({"check": "sliver", "km2": round(a, 4), "between": around,
                                     "where": [round(c.x, 4), round(c.y, 4)], "box": wide(hole)})

    log("overlaps and slivers checked")
    # what a reader sees at the scale of a region: findings of at least VISIBLE_KM2 (slits and seams always)
    for f in findings:
        f["visible"] = f["check"] in ("slit", "seam") or f.get("km2", 0) >= VISIBLE_KM2
    counts = {}
    for f in findings:
        key = f["check"] + (" (explained)" if f.get("explained") else "") + ("" if f["visible"] else " (small)")
        counts[key] = counts.get(key, 0) + 1
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "display_check.json").write_text(json.dumps({"counts": counts, "findings": findings}, indent=1,
                                                       ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(counts))
    for f in sorted(findings, key=lambda f: -f.get("km2", 1)):
        if f["visible"] and not f.get("explained"):
            print({k: v for k, v in f.items() if k not in ("box", "visible")})


if __name__ == "__main__":
    main()
