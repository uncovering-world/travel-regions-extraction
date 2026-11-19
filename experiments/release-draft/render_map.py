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
import math
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
# D073 moves a strip or rim, not land: a cut-off part moves only if no point of it lies farther than this from its
# edge (the radius of the largest circle inside it), i.e. it is a strip at most twice as wide. Wider parts stay with
# the donor and are listed as kept.
RIM_MAX_RADIUS_M = 2000


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
    parser.add_argument("--display-tolerance", type=float, default=0.003,
                        help="simplification of what is drawn outside the detail zones, degrees (the GADM rows are united "
                             "at --tolerance / 10)")
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
    # the cache holds the result of apply_own, so it also depends on that function's code
    import inspect
    key2 = key + hashlib.sha256(b"".join(f.read_bytes() for f in own_files) + (inspect.getsource(apply_own) + inspect.getsource(cut_off) + inspect.getsource(inner_radius_m)
                                                                  + repr(RIM_MAX_RADIUS_M)).encode()).hexdigest()
    cached = pickle.loads(final.read_bytes()) if final.exists() else {}
    if cached.get("key") == key2:
        geoms = {rid: wkb.loads(g) for rid, g in cached["geoms"].items()}
        cached.pop("geoms")
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
            # the detail layer holds only the zones: each donor's main land is the one of the full map
            mains = {d: max(polygons(g), key=lambda x: x.area) for d, g in geoms.items() if polygons(g)}
            apply_own(detail, membership, mains)
            detail_cache.write_bytes(pickle.dumps({"key": key2, "geoms": {rid: wkb.dumps(g) for rid, g in detail.items()}}))
        del cached_d
    write(geoms, regions, membership, args.display_tolerance, zones, detail)
    # what D073 moved or kept, for the consumer (TYR's request 3): shipped beside the membership table
    listed = OUT / "cut_off_D073.csv"
    if listed.exists():
        (ROOT / "release" / "cut_off_D073.csv").write_bytes(listed.read_bytes())
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


def without_specks(geom, min_deg2=1e-6):
    """Drops holes smaller than about 0.01 km² (specks of water or gaps the substrate leaves, drawn as a ring)."""
    def clean(p):
        return shapely.Polygon(p.exterior, [r for r in p.interiors if shapely.Polygon(r).area >= min_deg2])
    parts = [clean(p) for p in getattr(geom, "geoms", [geom]) if p.geom_type == "Polygon"]
    return shapely.MultiPolygon(parts) if len(parts) > 1 else parts[0] if parts else geom


def displayed(geom, simple, zones, detail_geom):
    """The region simplified outside the detail zones, the full-precision detail layer inside them."""
    if zones is None or not geom.intersects(zones):
        return simple if not simple.is_empty else geom
    # cut by the zone shrunk by about a metre: the two parts overlap in a thin band instead of meeting on one edge,
    # so they dissolve without a slit and no seam is drawn on the zone's boundary
    outside = shapely.difference(simple, zones.buffer(-1e-5, join_style="mitre"))
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


def apply_own(geoms, membership, mains=None):
    """The canon's own geometries, clipped to their donors (plus land no GADM unit covers), moved to their region; then
    what they cut off from a donor goes on by D073. mains: each donor's main land, from the full map, for a layer that
    holds only part of it (the detail zones); by default the largest part of the donor in geoms."""
    own = defaultdict(list)
    pieces = {}
    start = dict(geoms)          # before any cut: to tell a part the outlines cut from one they left whole
    outlines = []                # (region, outline) of every polygon own geometry, for D073
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
        before = {d: geoms[d] for d in donors}
        for d in donors:
            geoms[d] = shapely.make_valid(shapely.difference(geoms[d], piece))
        # D072: the rest of the substrate's copy of a detached part that this outline overlaps goes to the region the
        # outline's source puts there ("AZ>AM": Azerbaijan's leftovers to Armenia); never the donor's main land, never
        # land of a register area (condition 3, the source's own assignment, is checked by check_custom.py)
        for pair in m.get("remnants_to", "").split():
            src, _, dst = pair.partition(">")
            if src not in before or dst not in geoms:
                continue
            parts = list(getattr(before[src], "geoms", [before[src]]))
            main = max(parts, key=lambda g: g.area)
            disputed = [g for r, g in geoms.items() if r.startswith("area/") and r != m["region_id"]]
            moved = []
            for g in parts:
                if g is main or shapely.intersection(g, geom).area <= 0:
                    continue
                rest = shapely.make_valid(shapely.difference(g, piece))
                if rest.is_empty or any(shapely.intersection(rest, x).area > 0 for x in disputed if rest.intersects(x)):
                    continue
                moved.append(rest)
            if moved:
                rest = shapely.union_all(moved)
                geoms[src] = shapely.make_valid(shapely.difference(geoms[src], rest))
                geoms[dst] = shapely.make_valid(shapely.union_all([geoms[dst], rest]))
                log(f"  {len(moved)} leftover part(s) of {src}'s copy near {m['unit']} moved to {dst} (D072)")
        own[m["region_id"]].append(piece)
        pieces[m["unit"]] = piece
        outlines.append((m["region_id"], geom, donors))
        log(f"own geometry {m['unit']} -> {m['region_id']} (donors: {' '.join(donors) or 'none'})")
    for rid, parts in own.items():
        geoms[rid] = shapely.make_valid(shapely.union_all(parts + ([geoms[rid]] if rid in geoms else [])))
    log("own geometries applied")
    moves, kept = cut_off(geoms, start, outlines, mains)
    # the list for the consumer comes from the full-precision detail layer (mains given), which covers every own
    # geometry; the simplified full map can detach a strip that stays joined to its donor at full precision
    name = "cut_off_D073.csv" if mains is not None else "cut_off_D073_simplified.csv"
    OUT.mkdir(parents=True, exist_ok=True)
    with (OUT / name).open("w", encoding="utf-8", newline="") as handle:
        out = csv.writer(handle)
        out.writerow(["donor", "receiver", "lon", "lat", "area_km2", "radius_m", "outcome"])
        rows = [(d, to, p, r, "moved") for d, to, p, r in moves] + [(d, d, p, r, "kept: wider than a rim")
                                                                    for d, p, r in kept]
        for d, to, p, r, outcome in sorted(rows, key=lambda x: (x[0], x[1], -x[2].area)):
            c = p.representative_point()
            out.writerow([d, to, round(c.x, 7), round(c.y, 7), f"{km2(p):.4g}", round(r), outcome])
    return pieces


def polygons(g) -> list:
    return [p for p in getattr(g, "geoms", [g]) if p.geom_type == "Polygon"] if not g.is_empty else []


def km2(g) -> float:
    """Area in km², from degrees at the part's latitude (good enough for small parts)."""
    lat = g.representative_point().y
    return g.area * 111.32 ** 2 * math.cos(math.radians(lat))


def inner_radius_m(g) -> float:
    """Radius of the largest circle inside g, in metres (degrees scaled at the part's latitude, the smaller axis)."""
    lat = g.representative_point().y
    r = shapely.maximum_inscribed_circle(g, 1e-5).length
    return r * 111320 * min(1.0, math.cos(math.radians(lat)) or 1.0)


def cut_off(geoms, start, outlines, mains=None):
    """D073: a part of a donor that an own geometry cut off from the donor's main land (a strip, an island's rim) goes
    to the region the outline's source puts there, else to the neighbour with the longest shared border; it stays if
    the outline's source leaves it out on purpose (it lies in a hole of the outline: a settlement excluded from a
    lease, an enclave left out of a district) or if another register area's outline covers it. The outlines we use
    draw only their own region, so outside a hole the source says nothing about the part: the longest border decides.
    Returns the moves (donor, receiver, part)."""
    donors = sorted({d for _, _, ds in outlines for d in ds if d in geoms})
    ids = sorted(geoms)
    tree = shapely.STRtree([geoms[i] for i in ids])
    moves, kept = [], []
    hulls = [shapely.union_all([shapely.Polygon(x.exterior) for x in polygons(o)]) for _, o, _ in outlines]
    for d in donors:
        parts = polygons(geoms[d])
        if len(parts) < 2:
            continue
        main = (mains or {}).get(d)
        if main is None:
            main = max(parts, key=lambda g: g.area)
        shapely.prepare(main)
        before = polygons(start[d])
        before_tree = shapely.STRtree(before)
        for p in parts:
            if p is main or main.intersects(p):
                continue
            # a part the outlines left whole (an island, an exclave) is not cut off
            if any(abs(before[k].area - p.area) <= 1e-12 * max(1.0, before[k].area)
                   for k in before_tree.query(p, predicate="intersects")):
                continue
            c = p.representative_point()
            if any(hull.contains(c) and not o.contains(c)
                   for hull, (_, o, ds) in zip(hulls, outlines) if d in ds and hull.intersects(p)):
                continue                                    # left out by the outline's source: stays
            near = [ids[k] for k in tree.query(p.buffer(1e-6), predicate="intersects") if ids[k] != d]
            x0, y0, x1, y1 = p.bounds
            shared = {n: shapely.intersection(p.boundary, shapely.clip_by_rect(geoms[n], x0 - 1e-4, y0 - 1e-4, x1 + 1e-4,
                                                                               y1 + 1e-4).buffer(1e-6)).length
                      for n in near}
            shared = {n: v for n, v in shared.items() if v > 0}
            if not shared:
                continue
            to = max(sorted(shared), key=lambda n: shared[n])
            if any(r != to and r.startswith("area/") and shapely.intersection(o, p).area > 0.01 * p.area
                   for r, o, _ in outlines):
                log(f"  D073: part of {d} at {c.x:.4f},{c.y:.4f} lies in another register area's outline; kept")
                continue
            r = inner_radius_m(p)
            if r > RIM_MAX_RADIUS_M:
                kept.append((d, p, r))
                log(f"  D073: part of {d} at {c.x:.4f},{c.y:.4f} ({km2(p):.3g} km², {r:.0f} m inside) is land, not a rim; kept")
                continue
            moves.append((d, to, p, r))
    # one difference and one union per region: the parts are disjoint, so this equals moving them one by one
    taken, given = defaultdict(list), defaultdict(list)
    for d, to, p, _ in moves:
        taken[d].append(p)
        given[to].append(p)
    for d, ps in taken.items():
        geoms[d] = shapely.make_valid(shapely.difference(geoms[d], shapely.union_all(ps)))
    for to, ps in given.items():
        geoms[to] = shapely.make_valid(shapely.union_all([geoms[to]] + ps))
    by_pair = defaultdict(list)
    for d, to, p, _ in moves:
        by_pair[(d, to)].append(p)
    for (d, to), ps in sorted(by_pair.items()):
        log(f"  D073: {len(ps)} cut-off part(s) of {d} moved to {to}")
    return moves, kept


def write_pieces(pieces, tolerance, zones=None):
    """Each own geometry as clipped to its donors: the land it actually moves (own_pieces.json), unsimplified
    when detail zones are on (every own geometry lies inside them)."""
    out = {u: mapping(rounded(g if zones is not None else g.simplify(tolerance / 4))) for u, g in sorted(pieces.items())
           if not g.is_empty}
    (OUT / "own_pieces.json").write_text(json.dumps(out), encoding="utf-8")
    log(f"wrote {len(out)} clipped own geometries")


def write(geoms, regions, membership, tolerance, zones=None, detail=None):
    """Display features for the simple HTML page (index.html, regions.js), written one region at a time: each region's
    full geometry is released as soon as it is written, so that the step does not hold the whole map twice."""
    # each region is simplified on its own, so neighbours' edges may differ by up to the tolerance; a coverage
    # simplification would keep them identical but needs regions united from unsimplified GADM rows (see README)
    units = defaultdict(list)
    for m in membership:
        units[m["region_id"]].append(f"{m['role']} {m['source']} {m['unit']}" + (f" clip to {m['clip_to']}" if m.get("clip_to") else ""))
    missing = sorted(set(regions) - set(geoms))
    OUT.mkdir(parents=True, exist_ok=True)
    written = 0
    with (OUT / "regions.js").open("w", encoding="utf-8") as out:
        out.write('window.REGIONS = {"type": "FeatureCollection", "features": [\n')
        for rid in sorted(geoms):
            geom = geoms.pop(rid)
            r = regions.get(rid, {"name": rid})
            povs = {k[5:]: v for k, v in r.items() if k.startswith("view_") and v}
            majority = max(set(povs.values()), key=list(povs.values()).count) if povs else ""
            differing = {k: v for k, v in povs.items() if v != majority}
            simple = displayed(geom, shapely.make_valid(geom.simplify(tolerance, preserve_topology=False)), zones,
                               (detail or {}).get(rid))
            feature = {"type": "Feature", "geometry": mapping(rounded(without_specks(simple))), "properties": {
                "id": rid, "name": r.get("name", rid), "country": r.get("country", ""), "basis": r.get("basis", ""),
                "evidence": r.get("evidence", ""), "open": r.get("open", ""), "pov_majority": majority,
                "pov_differing": differing, "units": units[rid][:12]}}
            out.write((",\n" if written else "") + json.dumps(feature, ensure_ascii=False))
            del geom, simple, feature
            written += 1
            if written % 50 == 0:
                log(f"wrote {written} regions")
        out.write("\n]};\nwindow.MISSING = " + json.dumps(missing) + ";\n")
    (OUT / "index.html").write_text((ROOT / "map_template.html").read_text(encoding="utf-8"), encoding="utf-8")
    log(f"wrote {written} regions; regions without geometry: {missing}")


if __name__ == "__main__":
    main()
