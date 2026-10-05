#!/usr/bin/env python3
"""Render the draft release as an interactive local map for a visual check (needs shapely).

Builds each region's polygon from the membership rules: GADM 4.1 rows assigned by their identifiers (include minus
exclude), then the canon's own geometries, each clipped to its donor regions (plus land no GADM unit covers) and
moved from the donors to its region. Simplifies for display and writes cache/map/: index.html, regions.js.

The output contains GADM-derived geometry, whose licence forbids redistribution: it stays in the gitignored cache.
Run from the repository root with an environment that has shapely:
    python experiments/release-draft/render_map.py [--tolerance 0.01]
then open experiments/release-draft/cache/map/index.html in a browser.
"""
import argparse
import csv
import hashlib
import json
import os
import pickle
import sqlite3
import sys
import time
from collections import defaultdict
from pathlib import Path

import shapely
from shapely import wkb
from shapely.geometry import mapping, shape
from shapely.ops import split

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[1]
GADM = Path(os.environ.get("GADM_GPKG", REPO.parent / "track-your-regions" / "deployment" / "gadm_410.gpkg"))
OUT = ROOT / "cache" / "map"


def gpkg_geometry(blob):
    envelope = {0: 0, 1: 32, 2: 48, 3: 48, 4: 64}[(blob[3] >> 1) & 7]
    return wkb.loads(bytes(blob[8 + envelope:]))


def rounded(geom):
    """Coordinates rounded to 1e-5 degrees, about a metre (display only; validity is not re-checked)."""
    return shapely.transform(geom, lambda xy: xy.round(5))


def log(message):
    print(time.strftime("%H:%M:%S"), message, file=sys.stderr, flush=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--tolerance", type=float, default=0.01, help="display simplification, degrees")
    parser.add_argument("--detail-margin", type=float, default=0.2,
                        help="degrees around disputed regions and own geometries kept at full precision (0: none)")
    args = parser.parse_args()
    release = ROOT / "release"
    regions = {r["region_id"]: r for r in csv.DictReader((release / "regions.csv").open(encoding="utf-8"))}
    membership = list(csv.DictReader((release / "membership.csv").open(encoding="utf-8")))
    inc, exc = defaultdict(set), defaultdict(set)
    for m in membership:
        if m["source"] == "GADM 4.1":
            (inc if m["role"] == "include" else exc)[m["unit"]].add(m["region_id"])

    # 1. GADM rows to regions, by identifiers (united polygons are cached: the step takes minutes)
    united = OUT / f"united-{args.tolerance}.pickle"
    key = hashlib.sha256((release / "membership.csv").read_bytes()).hexdigest()
    geoms = None
    if united.exists():
        cached = pickle.loads(united.read_bytes())
        if cached["key"] == key:
            geoms = {rid: wkb.loads(g) for rid, g in cached["geoms"].items()}
            log(f"united regions read from {united.name}")
    if geoms is None:
        geoms = unite(args.tolerance, inc, exc)
        OUT.mkdir(parents=True, exist_ok=True)
        united.write_bytes(pickle.dumps({"key": key, "geoms": {rid: wkb.dumps(g) for rid, g in geoms.items()}}))
    final = OUT / f"final-{args.tolerance}.pickle"
    own_files = sorted((REPO / "data" / "custom-geometries").glob("*.geojson"))
    # the cache holds the result of apply_own, so it also depends on this script
    key2 = key + hashlib.sha256(b"".join(f.read_bytes() for f in own_files) + Path(__file__).read_bytes()).hexdigest()
    cached = pickle.loads(final.read_bytes()) if final.exists() else {}
    if cached.get("key") == key2:
        geoms = {rid: wkb.loads(g) for rid, g in cached["geoms"].items()}
        log(f"regions with own geometries read from {final.name}")
    else:
        pieces = apply_own(geoms, membership)
        final.write_bytes(pickle.dumps({"key": key2, "geoms": {rid: wkb.dumps(g) for rid, g in geoms.items()},
                                        "pieces": {u: wkb.dumps(g) for u, g in pieces.items()}}))
        cached = {"pieces": {u: wkb.dumps(g) for u, g in pieces.items()}}
    pieces = {u: wkb.loads(g) for u, g in cached.get("pieces", {}).items()}
    zones, detail = None, {}
    if args.detail_margin > 0:
        # full precision where boundaries are disputed or drawn by the canon itself: around every region of the register
        # of disputed areas and every own geometry, GADM rows are taken unsimplified and clipped to these zones
        zones = detail_zones(geoms, pieces, args.detail_margin)
        detail_cache = OUT / f"detail-{args.detail_margin}.pickle"
        cached_d = pickle.loads(detail_cache.read_bytes()) if detail_cache.exists() else {}
        if cached_d.get("key") == key2:
            detail = {rid: wkb.loads(g) for rid, g in cached_d["geoms"].items()}
            log(f"detail layer read from {detail_cache.name}")
        else:
            detail = unite_detail(zones, inc, exc)
            apply_own(detail, membership)
            detail_cache.write_bytes(pickle.dumps({"key": key2, "geoms": {rid: wkb.dumps(g) for rid, g in detail.items()}}))
    write(geoms, regions, membership, args.tolerance, zones, detail)
    write_pieces(pieces, args.tolerance, zones)


def detail_zones(geoms, pieces, margin):
    """Boxes around every region of the register of disputed areas and every own geometry, widened by margin."""
    boxes = []
    for rid, g in geoms.items():
        if rid.startswith("area/") and not g.is_empty:
            boxes.append(shapely.box(*g.bounds).buffer(margin, join_style="mitre"))
    for g in pieces.values():
        if not g.is_empty:
            boxes.append(shapely.box(*g.bounds).buffer(margin, join_style="mitre"))
    zones = shapely.union_all(boxes)
    log(f"detail zones: {len(boxes)} boxes")
    return zones


def unite_detail(zones, inc, exc):
    """GADM rows inside the zones, unsimplified and clipped to them, united per region."""
    db = sqlite3.connect(f"file:{GADM}?mode=ro", uri=True)
    parts = defaultdict(list)
    seen = set()
    for z in getattr(zones, "geoms", [zones]):
        x0, y0, x1, y1 = z.bounds
        for fid, in db.execute("select id from rtree_gadm_410_geom where maxx>=? and minx<=? and maxy>=? and miny<=?",
                               (x0, x1, y0, y1)):
            if fid in seen:
                continue
            seen.add(fid)
            blob, *gids = db.execute("select geom, GID_0, GID_1, GID_2, GID_3, GID_4, GID_5 from gadm_410 where fid=?",
                                     (fid,)).fetchone()
            chain = [g for g in gids if g]
            owners = set()
            for g in chain:
                owners |= inc.get(g, set())
            for g in chain:
                owners -= exc.get(g, set())
            if len(owners) != 1:
                continue
            g = shapely.make_valid(gpkg_geometry(blob))
            if g.intersects(zones):
                parts[owners.pop()].append(shapely.intersection(g, zones))
            if len(seen) % 2000 == 0:
                log(f"detail: {len(seen)} GADM rows read")
    log(f"detail: {len(seen)} GADM rows in the zones; uniting {len(parts)} regions")
    return {rid: shapely.make_valid(shapely.union_all(items, grid_size=1e-7)) for rid, items in parts.items()}


def displayed(geom, tolerance, zones, detail_geom):
    """Simplified outside the detail zones, the full-precision detail layer inside them."""
    if zones is None or not geom.intersects(zones):
        simple = geom.simplify(tolerance, preserve_topology=False)
        return simple if not simple.is_empty else geom
    outside = shapely.difference(geom, zones).simplify(tolerance, preserve_topology=False)
    inside = detail_geom if detail_geom is not None else shapely.intersection(geom, zones)
    return shapely.make_valid(shapely.union_all([outside, inside]))


def unite(tolerance, inc, exc):
    db = sqlite3.connect(f"file:{GADM}?mode=ro", uri=True)
    parts = defaultdict(list)
    n = 0
    for blob, *gids in db.execute("select geom, GID_0, GID_1, GID_2, GID_3, GID_4, GID_5 from gadm_410"):
        chain = [g for g in gids if g]
        owners = set()
        for g in chain:
            owners |= inc.get(g, set())
        for g in chain:
            owners -= exc.get(g, set())
        n += 1
        if n % 50000 == 0:
            log(f"{n} GADM rows read")
        if len(owners) == 1:
            geom = gpkg_geometry(blob)
            # a light simplification of each row keeps the unions fast; display tolerance is applied later
            parts[owners.pop()].append(shapely.make_valid(geom.simplify(tolerance / 10)))
    log(f"{n} GADM rows read; uniting {len(parts)} regions")
    geoms = {}
    for i, (rid, items) in enumerate(sorted(parts.items(), key=lambda kv: -len(kv[1]))):
        geoms[rid] = shapely.make_valid(shapely.union_all(items, grid_size=1e-6))
        if i % 25 == 0:
            log(f"united {i + 1}/{len(parts)} ({rid}, {len(items)} rows)")

    return geoms


def apply_own(geoms, membership):
    """The canon's own geometries, clipped to their donors (plus land no GADM unit covers), moved to their region."""
    own = defaultdict(list)
    pieces = {}
    ids = sorted(geoms)
    tree = shapely.STRtree([geoms[i] for i in ids])
    for m in membership:
        if m["source"] != "custom geometry":
            continue
        data = json.loads((REPO / "data" / "custom-geometries" / m["unit"]).read_text())
        donors = [d for d in m.get("clip_to", "").split() if d in geoms]
        if data["features"][0]["geometry"]["type"] == "LineString":
            # a line of control (D066): split the donors by it and keep the side with the holder's point
            line = shape(data["features"][0]["geometry"])
            point = shapely.Point(data["features"][0]["properties"]["holder_point"]["lonlat"])
            land = shapely.union_all([geoms[d] for d in donors])   # whole donors: a box could cut off land on the far side
            piece = shapely.union_all([p for p in split(land, line).geoms if p.intersects(point.buffer(1e-6))])
            for d in donors:
                geoms[d] = shapely.make_valid(shapely.difference(geoms[d], piece))
            own[m["region_id"]].append(piece)
            pieces[m["unit"]] = piece
            log(f"own geometry {m['unit']} -> {m['region_id']} (line of control, donors: {' '.join(donors)})")
            continue
        geom = shapely.make_valid(shapely.union_all([shape(f["geometry"]) for f in data["features"]]))
        # only the neighbourhood of the piece matters: clip whole countries to its box before any union
        x0, y0, x1, y1 = geom.bounds
        local = lambda g: shapely.make_valid(shapely.clip_by_rect(g, x0 - 0.1, y0 - 0.1, x1 + 0.1, y1 + 0.1))
        donors = [d for d in m.get("clip_to", "").split() if d in geoms]
        taken = shapely.intersection(geom, shapely.union_all([local(geoms[d]) for d in donors])) if donors else shapely.Polygon()
        near = [local(geoms[ids[i]]) for i in tree.query(geom)]
        uncovered = shapely.difference(geom, shapely.union_all(near)) if near else geom
        piece = shapely.make_valid(shapely.union_all([taken, uncovered]))
        for d in donors:
            geoms[d] = shapely.make_valid(shapely.difference(geoms[d], piece))
        own[m["region_id"]].append(piece)
        pieces[m["unit"]] = piece
        log(f"own geometry {m['unit']} -> {m['region_id']} (donors: {' '.join(donors) or 'none'})")
    for rid, parts in own.items():
        geoms[rid] = shapely.make_valid(shapely.union_all(parts + ([geoms[rid]] if rid in geoms else [])))
    log("own geometries applied")
    return pieces


def write_pieces(pieces, tolerance, zones=None):
    """Each own geometry as clipped to its donors: the land it actually moves (own_pieces.json), unsimplified
    when detail zones are on (every own geometry lies inside them)."""
    out = {u: mapping(rounded(g if zones is not None else g.simplify(tolerance / 4))) for u, g in sorted(pieces.items())
           if not g.is_empty}
    (OUT / "own_pieces.json").write_text(json.dumps(out), encoding="utf-8")
    log(f"wrote {len(out)} clipped own geometries")


def write(geoms, regions, membership, tolerance, zones=None, detail=None):
    """Display features for the simple HTML page (index.html, regions.js)."""
    features = []
    for rid, geom in sorted(geoms.items()):
        r = regions.get(rid, {"name": rid})
        povs = {k[5:]: v for k, v in r.items() if k.startswith("view_") and v}
        majority = max(set(povs.values()), key=list(povs.values()).count) if povs else ""
        differing = {k: v for k, v in povs.items() if v != majority}
        simple = displayed(geom, tolerance, zones, (detail or {}).get(rid))
        if len(features) % 50 == 0:
            log(f"wrote {len(features)} regions")
        features.append({"type": "Feature", "geometry": mapping(rounded(simple)), "properties": {
            "id": rid, "name": r.get("name", rid), "country": r.get("country", ""), "basis": r.get("basis", ""),
            "evidence": r.get("evidence", ""), "open": r.get("open", ""), "pov_majority": majority,
            "pov_differing": differing,
            "units": [f"{m['role']} {m['source']} {m['unit']}" + (f" clip to {m['clip_to']}" if m.get("clip_to") else "")
                      for m in membership if m["region_id"] == rid][:12]}})
    missing = sorted(set(regions) - set(geoms))
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "regions.js").write_text("window.REGIONS = " + json.dumps({"type": "FeatureCollection", "features": features},
                                                                       ensure_ascii=False) + ";\nwindow.MISSING = "
                                    + json.dumps(missing) + ";\n", encoding="utf-8")
    (OUT / "index.html").write_text((ROOT / "map_template.html").read_text(encoding="utf-8"), encoding="utf-8")
    log(f"wrote {len(features)} regions; regions without geometry: {missing}")


if __name__ == "__main__":
    main()
