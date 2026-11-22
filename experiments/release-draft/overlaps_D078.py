#!/usr/bin/env python3
"""D078 / D079 / R063: ground that two GADM 4.1 rows of different regions both draw, and what cleaning leaves of it.

The substrate is cleaned as a coverage (D079: snap SNAP degrees, gap width 0, longest border). Only an overlap wider
than the snapping distance can survive it, so only those are listed, with their holder; on GADM 4.1 the list is
empty. As a check, every pair of rows with an overlap is also cleaned on its own and must leave no overlap.

For every pair of GADM rows whose bounding boxes meet (the GeoPackage's own R-tree) and which the membership table
gives to different regions, the intersection of positive area is a strip. It goes to the region with which it shares
the longer border (D073's fallback): the part of the strip's edge that runs along row B's boundary borders row A's own
ground, and the other way round. A strip that lies inside an own geometry of the canon is left out: the outline, not
GADM, decides that ground. Writes release/overlaps_D078.csv. Reads GADM directly, a few rows at a time.

Run from the repository root:
  uv run --no-project --with shapely python experiments/release-draft/overlaps_D078.py
"""
import csv
import json
import math
import os
import sqlite3
from pathlib import Path

import shapely
from shapely.geometry import shape

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[1]
GADM = Path(os.environ.get("GADM_GPKG", REPO.parent / "track-your-regions" / "deployment" / "gadm_410.gpkg"))
OUT = ROOT / "release" / "overlaps_D078.csv"
SNAP = 1e-7  # degrees, about 1 cm: D079's snapping distance
EDGE = 1e-9  # degrees (about 0.1 mm): how close a piece of the strip's edge must run to a row's boundary to lie on it


def gpkg_geometry(blob: bytes):
    """A GeoPackage geometry blob: an 8-byte header, an envelope whose size the flags give, then WKB."""
    flags = blob[3]
    envelope = {0: 0, 1: 32, 2: 48, 3: 48, 4: 64}[(flags >> 1) & 7]
    return shapely.make_valid(shapely.from_wkb(blob[8 + envelope:]))


def regions_of_rows(db):
    """Each GADM row's region, as check_cover.py resolves it: include rows up its GID chain, minus exclude rows."""
    inc, exc = {}, {}
    for r in csv.DictReader((ROOT / "release" / "membership.csv").open()):
        if r["source"] == "GADM 4.1":
            (inc if r["role"] == "include" else exc).setdefault(r["unit"], set()).add(r["region_id"])
    region, unit = {}, {}
    for fid, uid, *gids in db.execute("select fid, UID, GID_0, GID_1, GID_2, GID_3, GID_4, GID_5 from gadm_410"):
        chain = [g for g in gids if g]
        owners = set()
        for g in chain:
            owners |= inc.get(g, set())
        for g in chain:
            owners -= exc.get(g, set())
        if len(owners) == 1:
            region[fid] = owners.pop()
            unit[fid] = chain[-1] if chain else f"UID {uid}"
    return region, unit


def metres(length_deg: float, lat: float) -> float:
    return length_deg * 111320 * math.sqrt((1 + math.cos(math.radians(lat)) ** 2) / 2)


def main() -> None:
    db = sqlite3.connect(f"file:{GADM}?mode=ro", uri=True)
    region, unit = regions_of_rows(db)
    pairs = [(a, b) for a, b in db.execute(
        "select a.id, b.id from rtree_gadm_410_geom a, rtree_gadm_410_geom b "
        "where b.minx <= a.maxx and b.maxx >= a.minx and b.miny <= a.maxy and b.maxy >= a.miny and a.id < b.id")
        if a in region and b in region and region[a] != region[b]]
    print(f"{len(pairs)} row pairs of different regions with meeting boxes")
    outlines = shapely.union_all([shape(f["geometry"]) for p in sorted((REPO / "data" / "custom-geometries").glob("*.geojson"))
                                  for f in json.loads(p.read_text())["features"]])
    cache = {}

    def geometry(fid):
        if fid not in cache:
            if len(cache) > 4000:
                cache.clear()
            cache[fid] = gpkg_geometry(db.execute("select geom from gadm_410 where fid = ?", (fid,)).fetchone()[0])
        return cache[fid]

    rows, strips, left = [], 0, 0
    for a, b in sorted(pairs):
        ga, gb = geometry(a), geometry(b)
        inter = shapely.intersection(ga, gb)
        found = [p for p in getattr(inter, "geoms", [inter]) if p.geom_type == "Polygon" and p.area > 0
                 and not outlines.contains(p.representative_point())]
        if not found:
            continue
        strips += len(found)
        ca, cb = shapely.coverage_clean([ga, gb], gap_width=0.0, snapping_distance=SNAP)
        left += shapely.intersection(ca, cb).area > 0
        for part in found:
            width = 2 * shapely.maximum_inscribed_circle(part, 1e-12).length
            if width <= SNAP:
                continue
            lat = part.representative_point().y
            edge = part.boundary
            with_a = metres(shapely.intersection(edge, gb.boundary.buffer(EDGE)).length, lat)  # borders A's own ground
            with_b = metres(shapely.intersection(edge, ga.boundary.buffer(EDGE)).length, lat)
            holder = region[a] if with_a > with_b else region[b] if with_b > with_a else ""
            c = shapely.maximum_inscribed_circle(part, 1e-9).coords[0]
            x, y = next(((round(c[0], d), round(c[1], d)) for d in range(7, 16)
                         if part.contains(shapely.Point(round(c[0], d), round(c[1], d)))), c)
            m2 = part.area * (111320 ** 2) * math.cos(math.radians(lat))
            rows.append([unit[a], region[a], unit[b], region[b], holder, x, y, f"{m2:.4g}", metres(width, lat),
                         round(with_a, 3), round(with_b, 3)])
    rows.sort(key=lambda r: (r[1], r[3], r[0], r[2], -float(r[7])))
    with OUT.open("w", encoding="utf-8", newline="") as handle:
        out = csv.writer(handle, lineterminator="\n")
        out.writerow(["unit_a", "region_a", "unit_b", "region_b", "holder", "lon", "lat", "area_m2", "width_m",
                      "border_with_a_m", "border_with_b_m"])
        out.writerows(rows)
    summary = {"geos": ".".join(map(str, shapely.geos_version)), "snap_deg": SNAP, "strips_between_regions": strips,
               "wider_than_snap": len(rows), "row_pairs_with_overlap_left_after_cleaning": left}
    (ROOT / "release" / "overlaps_D078.json").write_text(json.dumps(summary, indent=1) + "\n")
    print(summary)


if __name__ == "__main__":
    main()
