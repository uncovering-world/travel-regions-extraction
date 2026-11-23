#!/usr/bin/env python3
"""Catalogue points that lie in no GADM 4.1 unit, and where D081's added land puts them (TYR's request).

Reads TYR's read-only points snapshot, GADM 4.1, the canon's own land files, World Polygons 11.4 and
release/added_land_D081.geojson (built by added_land_D081.py). Writes release/points_outside_gadm.csv, one row
per point in no GADM unit:

  status: added_piece (in a D081 piece), own_land (in an own land file), wp_land_below_floor (on World Polygons
          land no piece covers: under D083's floor or narrower than the snap), water (in neither source)
  piece_id, region_id, basis, gadm_unit, area_km2: the D081 piece (status added_piece)
  wp_genc_3, wp_name: the World Polygons feature the point lies in, if any

Run from the repository root:
  nice -n 10 uv run --no-project --with shapely python experiments/release-draft/points_outside_gadm.py
"""
import csv
import json
import os
import sqlite3
from pathlib import Path

import shapely
from shapely.geometry import shape

REPO = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
GADM = Path(os.environ.get("GADM_GPKG", REPO.parent / "track-your-regions" / "deployment" / "gadm_410.gpkg"))
WP = REPO / "data" / "custom-geometries" / "cache" / "WorldPolygons11_4.gpkg"
POINTS = Path.home() / "tyr-exports" / "real-points-2026-11-19.csv"
ADDED = HERE / "release" / "added_land_D081.geojson"
OUT = HERE / "release" / "points_outside_gadm.csv"


def gpkg_geometry(blob: bytes):
    envelope = {0: 0, 1: 32, 2: 48, 3: 48, 4: 64}[(blob[3] >> 1) & 7]
    return shapely.make_valid(shapely.from_wkb(blob[8 + envelope:]))


def main() -> None:
    gadm = sqlite3.connect(f"file:{GADM}?mode=ro", uri=True)
    rows = list(csv.DictReader(POINTS.open(encoding="utf-8")))
    outside = []
    for r in rows:
        x, y = float(r["lon"]), float(r["lat"])
        p = shapely.Point(x, y)
        fids = [f for (f,) in gadm.execute("select id from rtree_gadm_410_geom where minx<=? and maxx>=? and "
                                           "miny<=? and maxy>=?", (x, x, y, y))]
        if not any(gpkg_geometry(gadm.execute("select geom from gadm_410 where fid=?", (f,)).fetchone()[0]).covers(p)
                   for f in fids):
            outside.append({"location_id": r["location_id"], "lon": r["lon"], "lat": r["lat"], "point": p})
    print("points in no GADM unit:", len(outside), flush=True)
    tree = shapely.STRtree([o["point"] for o in outside])

    # own land files
    for path in sorted((REPO / "data" / "custom-geometries" / "land").glob("*.geojson")):
        for f in json.loads(path.read_text())["features"]:
            for i in tree.query(shape(f["geometry"]), predicate="covers"):
                outside[i].setdefault("status", "own_land")

    # World Polygons feature of each point
    wp = sqlite3.connect(f"file:{WP}?mode=ro", uri=True)
    for _fid, blob, name, genc3 in wp.execute("select fid, geom, WP_Name, GENC_3 from DoS_WP_11_4 order by fid"):
        for i in tree.query(gpkg_geometry(blob), predicate="covers"):
            outside[i].setdefault("wp_name", name)
            outside[i].setdefault("wp_genc_3", genc3 or "")

    # D081 pieces (one feature per line)
    with ADDED.open(encoding="utf-8") as f:
        for line in f:
            line = line.lstrip(",")
            if not line.startswith('{"type":"Feature"'):
                continue
            ft = json.loads(line.rstrip().rstrip(","))
            for i in tree.query(shape(ft["geometry"]), predicate="covers"):
                pr = ft["properties"]
                o = outside[i]
                if o.get("status") != "added_piece":
                    o.update(status="added_piece", **{k: pr[k] for k in
                                                       ("piece_id", "region_id", "basis", "gadm_unit", "area_km2")})

    for o in outside:
        o.setdefault("status", "wp_land_below_floor" if "wp_name" in o else "water")
    fields = ["location_id", "lon", "lat", "status", "piece_id", "region_id", "basis", "gadm_unit", "area_km2",
              "wp_genc_3", "wp_name"]
    outside.sort(key=lambda o: int(o["location_id"]) if o["location_id"].isdigit() else o["location_id"])
    with OUT.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore", lineterminator="\n")
        w.writeheader()
        for o in outside:
            w.writerow({k: o.get(k, "") for k in fields})
    counts = {}
    for o in outside:
        counts[o["status"]] = counts.get(o["status"], 0) + 1
    print(json.dumps(counts))


if __name__ == "__main__":
    main()
