#!/usr/bin/env python3
"""D081 / R064: land the land source draws and the substrate does not, given to a region.

Land source: World Polygons 11.4 (layer DoS_WP_11_4, pinned in data/custom-geometries/sources.json). Substrate:
GADM 4.1. Every World Polygons part (a large part cut into 1-degree tiles) minus the GADM units and own land files
that meet it leaves pieces of land no unit draws. A piece narrower than D079's snapping distance is the same line
drawn twice and is dropped; a piece smaller than FLOOR_KM2 is not added (D083) and is counted in the summary. Pieces cut by a tile edge are joined again. Each piece goes to the region with which it
shares the longest border; a piece that borders no region takes the region its World Polygons country code (GENC_3,
which is GADM's GID_0 for the same country) maps to in membership.csv; the rest are listed for a decision by hand.

Writes release/added_land_D081.geojson (one feature per piece: piece_id, region_id, basis (longest_border,
country_code, hand (decided in inputs/added_land_hand.csv) or undecided (no region yet: a reported gap)), decided_by (the border length or the
code), gadm_unit (the finest GADM unit of the region it attaches to: longest border, else nearest), the World Polygons
code, a point inside and the area), release/added_land_D081.csv (the same without geometry) and
release/added_land_D081.json (counts, inputs).

Run from the repository root (heavy: run niced, under the shared lock):
  nice -n 10 flock ~/.cache/tyr-heavy.lock uv run --no-project --with shapely --with pyproj \
      python experiments/release-draft/added_land_D081.py [--bbox minx,miny,maxx,maxy] [--out-suffix _sample]
"""
import argparse
import csv
import gc
import hashlib
import json
import math
import os
import pickle
import sqlite3
import time
from collections import Counter, defaultdict
from pathlib import Path

import shapely
from pyproj import Geod
from shapely.geometry import box, mapping, shape

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[1]
GADM = Path(os.environ.get("GADM_GPKG", REPO.parent / "track-your-regions" / "deployment" / "gadm_410.gpkg"))
WP = REPO / "data" / "custom-geometries" / "cache" / "WorldPolygons11_4.gpkg"
SNAP = 1e-7   # D079's snapping distance, degrees
EDGE = 1e-7   # how close a piece's edge must run to a neighbour's boundary to count as a shared border
TILE = 1.0    # degrees
FLOOR_KM2 = 0.01  # D083: a piece smaller than this is not added; the consumer's nearest-region rule takes it
GEOD = Geod(ellps="WGS84")


def gpkg_geometry(blob: bytes):
    flags = blob[3]
    envelope = {0: 0, 1: 32, 2: 48, 3: 48, 4: 64}[(flags >> 1) & 7]
    return shapely.from_wkb(blob[8 + envelope:])


def km2(g) -> float:
    return abs(GEOD.geometry_area_perimeter(g)[0]) / 1e6


def metres(length_deg: float, lat: float) -> float:
    return length_deg * 111320 * math.sqrt((1 + math.cos(math.radians(lat)) ** 2) / 2)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def inner_point(g) -> tuple[float, float]:
    """A point inside g, rounded as coarsely as stays inside (the piece's stable key)."""
    c = shapely.maximum_inscribed_circle(g, 1e-9).coords[0]
    for d in range(7, 16):
        x, y = round(c[0], d), round(c[1], d)
        if g.contains(shapely.Point(x, y)):
            return x, y
    return c


def polygons(g):
    return [p for p in getattr(g, "geoms", [g]) if p.geom_type == "Polygon" and not p.is_empty]


def split(g):
    """g cut into pieces no wider or taller than TILE, on whole-TILE lines, halving the box each time so that a huge
    part (Antarctica, Eurasia) is never clipped whole once per tile."""
    if g.is_empty:
        return []
    x0, y0, x1, y1 = g.bounds
    if x1 - x0 <= TILE and y1 - y0 <= TILE:
        return [g]
    if x1 - x0 >= y1 - y0:
        cut = math.floor((x0 + x1) / 2 / TILE) * TILE
        cut = cut if x0 < cut < x1 else math.ceil(x0 / TILE + 1e-12) * TILE
        halves = [shapely.clip_by_rect(g, x0, y0, cut, y1), shapely.clip_by_rect(g, cut, y0, x1, y1)]
    else:
        cut = math.floor((y0 + y1) / 2 / TILE) * TILE
        cut = cut if y0 < cut < y1 else math.ceil(y0 / TILE + 1e-12) * TILE
        halves = [shapely.clip_by_rect(g, x0, y0, x1, cut), shapely.clip_by_rect(g, x0, cut, x1, y1)]
    return [t for h in halves for t in split(shapely.make_valid(h))]


def regions_of_rows(db):
    """Each GADM row's region (include rows up its GID chain, minus exclude rows), and each GID_0's region."""
    inc, exc = {}, {}
    for r in csv.DictReader((ROOT / "release" / "membership.csv").open()):
        if r["source"] == "GADM 4.1":
            (inc if r["role"] == "include" else exc).setdefault(r["unit"], set()).add(r["region_id"])
    region = {}
    for fid, *gids in db.execute("select fid, GID_0, GID_1, GID_2, GID_3, GID_4, GID_5 from gadm_410"):
        chain = [g for g in gids if g]
        owners = set()
        for g in chain:
            owners |= inc.get(g, set())
        for g in chain:
            owners -= exc.get(g, set())
        if len(owners) == 1:
            region[fid] = owners.pop()
    country = {u: next(iter(rs)) for u, rs in inc.items() if len(u) == 3 and len(rs) == 1}
    return region, country


def own_geometries():
    """Own outlines with their region (sources.csv), and own land files (land GADM lacks that they already add)."""
    rows = {r["file"]: r for r in csv.DictReader((REPO / "data" / "custom-geometries" / "sources.csv").open())}
    outlines, land = [], []
    for p in sorted((REPO / "data" / "custom-geometries").glob("*.geojson")):
        g = shapely.make_valid(shapely.union_all([shape(f["geometry"]) for f in json.loads(p.read_text())["features"]]))
        outlines.append((g, rows[p.name]["region"]))
    for p in sorted((REPO / "data" / "custom-geometries" / "land").glob("*.geojson")):
        land += [shapely.make_valid(shape(f["geometry"])) for f in json.loads(p.read_text())["features"]]
    return outlines, land


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--bbox", help="only World Polygons land in minx,miny,maxx,maxy (a sample run)")
    ap.add_argument("--out-suffix", default="")
    ap.add_argument("--reuse-pieces", action="store_true",
                    help="skip the cut and reuse cache/added_land_pieces<suffix>.pkl from the last run")
    args = ap.parse_args()
    clip_box = box(*map(float, args.bbox.split(","))) if args.bbox else None
    t0 = time.time()

    gadm = sqlite3.connect(f"file:{GADM}?mode=ro", uri=True)
    wp = sqlite3.connect(f"file:{WP}?mode=ro", uri=True)
    region_of, region_of_country = regions_of_rows(gadm)
    outlines, own_land = own_geometries()
    outline_tree = shapely.STRtree([g for g, _ in outlines])
    land_tree = shapely.STRtree(own_land)
    cache = {}

    def unit(fid):
        if fid not in cache:
            if len(cache) > 1500:
                cache.clear()
            cache[fid] = shapely.make_valid(gpkg_geometry(
                gadm.execute("select geom from gadm_410 where fid = ?", (fid,)).fetchone()[0]))
        return cache[fid]

    def units_meeting(g):
        x0, y0, x1, y1 = g.bounds
        fids = [fid for (fid,) in gadm.execute(
            "select id from rtree_gadm_410_geom where minx <= ? and maxx >= ? and miny <= ? and maxy >= ?",
            (x1, x0, y1, y0))]
        return [(fid, unit(fid)) for fid in fids]

    def clipped(g, bounds, pad=1e-4):
        """g cut to a box around bounds: a huge unit (Antarctica, Russia) is never used whole."""
        x0, y0, x1, y1 = bounds
        return shapely.clip_by_rect(g, x0 - pad, y0 - pad, x1 + pad, y1 + pad)

    def uncovered(part):
        cover = [u for _, u in units_meeting(part)] + [own_land[i] for i in land_tree.query(part)]
        cover = [c for c in (clipped(u, part.bounds) for u in cover) if not c.is_empty and c.intersects(part)]
        return shapely.difference(part, shapely.union_all(cover)) if cover else part

    # the cut; pieces are kept as WKB to save memory, and saved so a failed assignment does not redo the cut
    store = ROOT / "cache" / f"added_land_pieces{args.out_suffix}.pkl"
    if args.reuse_pieces:
        pieces, below_n, below_km2, parts_seen = pickle.loads(store.read_bytes())
    else:
        pieces, edge_pieces = [], defaultdict(list)   # pieces: (wkb, genc_3); edge_pieces: genc_3 -> [wkb]
        below_n, below_km2, parts_seen = 0, 0.0, 0

        def keep(p, c):
            nonlocal below_n, below_km2
            a = km2(p)
            if a < FLOOR_KM2:   # D083: the floor
                below_n += 1
                below_km2 += a
            else:
                pieces.append((shapely.to_wkb(p), c))

        for fid, blob, genc3 in wp.execute("select fid, geom, GENC_3 from DoS_WP_11_4 order by fid"):
            g = gpkg_geometry(blob)
            for part in polygons(g):
                if clip_box is not None:
                    if not part.intersects(clip_box):
                        continue
                    part = shapely.intersection(part, clip_box)
                    if part.is_empty:
                        continue
                parts_seen += 1
                tiles = split(part)
                for piece_src in tiles:
                    for p in polygons(uncovered(piece_src)):
                        if shapely.buffer(p, -SNAP / 2).is_empty:
                            continue   # narrower than the snapping distance: one line drawn twice
                        if len(tiles) > 1:
                            edge_pieces[genc3].append(shapely.to_wkb(p))
                        else:
                            keep(p, genc3)
            del g
            print(f"wp fid {fid}: {len(pieces)} pieces kept, {below_n} below the floor, "
                  f"{sum(map(len, edge_pieces.values()))} tiled, {time.time() - t0:.0f} s", flush=True)
        # join pieces a tile edge cut, within one World Polygons country
        for c in sorted(edge_pieces, key=str):
            for p in polygons(shapely.union_all(shapely.from_wkb(edge_pieces.pop(c)))):
                keep(p, c)
        del edge_pieces
        store.parent.mkdir(exist_ok=True)
        store.write_bytes(pickle.dumps((pieces, below_n, below_km2, parts_seen)))
    gc.collect()
    print(f"{len(pieces)} pieces at or above {FLOOR_KM2} km2 ({below_n} below, {below_km2:.3f} km2), "
          f"{time.time() - t0:.0f} s", flush=True)

    # assign each piece (D081); the finest GADM unit it attaches to, within its region, by the same rule
    def gid(fid):
        return next(g for g in reversed(gadm.execute(
            "select GID_0, GID_1, GID_2, GID_3, GID_4, GID_5 from gadm_410 where fid = ?", (fid,)).fetchone()) if g)

    def nearest_unit(p, reg):
        for pad in (0.05, 0.5, 2.0, 8.0):
            near = [(shapely.distance(p, u), ufid) for ufid, u in units_meeting(p.buffer(pad))
                    if region_of.get(ufid) == reg]
            if near:
                return min(near)[1]
        return None

    # World Polygons codes that are not GADM GID_0 codes, mapped by hand with evidence (inputs/added_land_codes.csv);
    # keyed by code, and the piece must lie in that World Polygons feature (two features have no code: Spain and the
    # Caspian Sea)
    wp_codes = {}
    for d in csv.DictReader((ROOT / "inputs" / "added_land_codes.csv").open()):
        blob, name = wp.execute("select geom, WP_Name from DoS_WP_11_4 where fid = ?", (int(d["wp_fid"]),)).fetchone()
        if name != d["wp_name"]:
            raise SystemExit(f"inputs/added_land_codes.csv: feature {d['wp_fid']} is {name!r}, not {d['wp_name']!r}")
        feature = gpkg_geometry(blob)
        shapely.prepare(feature)
        wp_codes[d["genc_3"] or None] = (d["region_id"], feature, f"{d['genc_3'] or d['wp_name']} (hand map)")

    def code_region(c, p):
        if c in region_of_country:
            return region_of_country[c], "country_code", c
        if c in wp_codes and wp_codes[c][1].intersects(p.representative_point()):
            return wp_codes[c][0], "country_code", wp_codes[c][2]
        return None

    rows, how = [], defaultdict(int)
    for k, (wkb, c) in enumerate(pieces):
        p = shapely.from_wkb(wkb)
        if k % 20000 == 0:
            print(f"assigned {k}, {time.time() - t0:.0f} s", flush=True)
        lat = p.representative_point().y
        edge = p.boundary
        near = edge.buffer(EDGE)
        border, unit_border = defaultdict(float), defaultdict(float)
        own_near = outline_tree.query(near)
        for i in own_near:
            g, reg = outlines[i]
            g = clipped(g, p.bounds)
            border[reg] += metres(shapely.intersection(edge, g.buffer(EDGE)).length, lat)
        inside_own = (shapely.union_all([clipped(outlines[i][0], p.bounds) for i in own_near])
                      if len(own_near) else None)
        for ufid, u in units_meeting(near):
            if ufid not in region_of:
                continue
            u = clipped(u, p.bounds)
            if u.is_empty or not u.intersects(near):
                continue
            shared = shapely.intersection(edge, u.boundary.buffer(EDGE))
            if inside_own is not None:
                shared = shapely.difference(shared, inside_own)
            m = metres(shared.length, lat)
            if m > 0:
                border[region_of[ufid]] += m
                unit_border[ufid] = m
        best = sorted(((r, m) for r, m in border.items() if m > 0), key=lambda kv: (-kv[1], kv[0]))
        ufid = None
        if best and (len(best) == 1 or best[0][1] > best[1][1]):
            holder, basis, decided_by = best[0][0], "longest_border", f"{best[0][1]:.1f} m"
            mine = sorted(((m, f) for f, m in unit_border.items() if region_of[f] == holder), reverse=True)
            ufid = mine[0][1] if mine else None
        elif not best and code_region(c, p):
            holder, basis, decided_by = code_region(c, p)
            ufid = nearest_unit(p, holder)
        else:
            holder, basis = "", "undecided"
            decided_by = ("tied: " + "; ".join(f"{r} {m:.1f} m" for r, m in best)) if best else f"no region for {c}"
        how[basis] += 1
        x, y = inner_point(p)
        rows.append({"piece_id": f"wp{c or 'none'}-{x:.7f}_{y:.7f}", "region_id": holder, "basis": basis,
                     "decided_by": decided_by, "gadm_unit": gid(ufid) if ufid else "",
                     "wp_genc_3": c or "", "lon": x, "lat": y, "area_km2": round(km2(p), 6), "geometry": wkb})
    rows.sort(key=lambda r: r["piece_id"])
    ids = [r["piece_id"] for r in rows]
    if len(set(ids)) != len(ids):
        raise SystemExit("piece_id is not unique: " + ", ".join(sorted(i for i, n in Counter(ids).items() if n > 1)[:10]))

    # hand decisions (inputs/added_land_hand.csv), keyed by World Polygons code and a point, not by piece_id: a new
    # edition changes the piece and its id, and the point finds the piece again. A point in no piece fails the build.
    decisions = list(csv.DictReader((ROOT / "inputs" / "added_land_hand.csv").open()))
    tree = shapely.STRtree(shapely.from_wkb([r["geometry"] for r in rows])) if decisions else None
    for d in decisions:
        pt = shapely.Point(float(d["lon"]), float(d["lat"]))
        hit = [rows[i] for i in tree.query(pt, predicate="intersects") if rows[i]["wp_genc_3"] == d["wp_genc_3"]]
        if len(hit) != 1:
            raise SystemExit(f"hand decision at {d['lon']},{d['lat']} ({d['wp_genc_3']}) lies in {len(hit)} pieces")
        how[hit[0]["basis"]] -= 1
        how["hand_decided"] += 1
        hit[0].update(region_id=d["region_id"], basis="hand", decided_by=d["evidence"], gadm_unit=d["gadm_unit"])
    how = {k: v for k, v in how.items() if v}

    out = ROOT / "release"
    licence = "US government work, not subject to US copyright (17 U.S.C. § 105)"
    source = "US Department of State, World Polygons 11.4 (DoS_WP_11_4), minus GADM 4.1 and the canon's own land"
    fields = ["piece_id", "region_id", "basis", "decided_by", "gadm_unit", "wp_genc_3", "lon", "lat", "area_km2"]
    with (out / f"added_land_D081{args.out_suffix}.geojson").open("w", encoding="utf-8") as f:
        f.write('{"type":"FeatureCollection","source":%s,"licence":%s,"features":[\n'
                % (json.dumps(source), json.dumps(licence)))
        for k, r in enumerate(rows):
            feat = {"type": "Feature", "properties": {k2: r[k2] for k2 in fields},
                    "geometry": mapping(shapely.set_precision(shapely.from_wkb(r["geometry"]), 1e-9))}
            f.write(("," if k else "") + json.dumps(feat, separators=(",", ":"), ensure_ascii=False) + "\n")
        f.write("]}\n")
    with (out / f"added_land_D081{args.out_suffix}.csv").open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore", lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    sizes = defaultdict(int)
    for r in rows:
        a = r["area_km2"]
        sizes["<0.001" if a < 0.001 else "<0.01" if a < 0.01 else "<0.1" if a < 0.1 else "<1" if a < 1
              else "<10" if a < 10 else ">=10"] += 1
    features = sorted({r["region_id"] for r in rows if r["region_id"]})
    summary = {"bbox": args.bbox, "wp_parts": parts_seen, "pieces": len(pieces),
               "below_floor": {"floor_km2": FLOOR_KM2, "pieces": below_n, "km2": round(below_km2, 3)},
               "by_basis": dict(sorted(how.items())),
               "regions_gaining_land": len(features),
               "added_km2": round(sum(r["area_km2"] for r in rows if r["region_id"]), 3),
               "undecided_km2": round(sum(r["area_km2"] for r in rows if not r["region_id"]), 3),
               "pieces_by_km2": dict(sorted(sizes.items())),
               "cut_against": "GADM 4.1 units as stored (not coverage-cleaned) and the canon's own land files; "
                              "edges meet cleaned units within compare_within_deg",
               "compare_within_deg": SNAP,
               "snap_deg": SNAP, "tile_deg": TILE, "geos": ".".join(map(str, shapely.geos_version)),
               "inputs": {"WorldPolygons11_4.gpkg": sha256(WP) if not args.bbox else "(sample)",
                          "gadm_410.gpkg size": GADM.stat().st_size},
               "seconds": round(time.time() - t0)}
    (out / f"added_land_D081{args.out_suffix}.json").write_text(json.dumps(summary, indent=1) + "\n")
    print(json.dumps(summary, indent=1))


if __name__ == "__main__":
    main()
