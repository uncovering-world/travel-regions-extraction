#!/usr/bin/env python3
"""Which land does each custom geometry of the draft take, and from which regions? Needs shapely and pyproj.

For every precedence-1 membership row with a polygon available locally (Natural Earth features from the pinned
cache, files in data/custom-geometries), intersect the polygon with the GADM 4.1 rows under it, assign each GADM row
to its region by the membership rules (as check_cover.py does), and report the area taken from each region,
in km² in a local equal-area projection. Also reports overlaps between custom geometries of different regions.

Run from the repository root with an environment that has shapely and pyproj:
    python3 experiments/release-draft/check_custom.py
"""
import csv
import json
import os
import sqlite3
from pathlib import Path

from pyproj import Transformer
from shapely import wkb
from shapely.geometry import Point, shape
from shapely.ops import split, transform, unary_union

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[1]
GADM = Path(os.environ.get("GADM_GPKG", REPO.parent / "track-your-regions" / "deployment" / "gadm_410.gpkg"))
NE = REPO / "experiments" / "stage1-world-draft" / "cache" / "ne_10m_admin_0_disputed_areas.geojson"


def gpkg_geometry(blob: bytes):
    flags = blob[3]
    envelope = {0: 0, 1: 32, 2: 48, 3: 48, 4: 64}[(flags >> 1) & 7]
    return wkb.loads(bytes(blob[8 + envelope:]))


def km2(geom, lon, lat) -> float:
    laea = Transformer.from_crs("EPSG:4326", f"+proj=laea +lat_0={lat} +lon_0={lon} +units=m", always_xy=True)
    return transform(laea.transform, geom).area / 1e6


def main():
    rows = list(csv.DictReader((ROOT / "release" / "membership.csv").open()))
    inc, exc = {}, {}
    for r in rows:
        if r["source"] == "GADM 4.1":
            (inc if r["role"] == "include" else exc).setdefault(r["unit"], set()).add(r["region_id"])

    def region_of(chain):
        regions = set()
        for g in chain:
            regions |= inc.get(g, set())
        for g in chain:
            regions -= exc.get(g, set())
        return ",".join(sorted(regions)) or "none"

    ne = {str(f["properties"]["NE_ID"]): shape(f["geometry"]) for f in json.loads(NE.read_text())["features"]}
    custom = []
    for r in rows:
        if r["precedence"] != "1":
            continue
        if r["source"].startswith("Natural Earth"):
            geom = ne.get(r["unit"])
        elif r["source"] == "custom geometry":
            data = json.loads((REPO / "data" / "custom-geometries" / r["unit"]).read_text())
            geom = unary_union([shape(f["geometry"]) for f in data["features"]])
            if geom.geom_type == "LineString":   # a line of control (D066): resolved against the donors below
                geom = ("line", geom, data["features"][0]["properties"]["holder_point"]["lonlat"])
        else:
            geom = None   # OpenStreetMap relations are not fetched here
        custom.append((r["region_id"], r["source"], r["unit"], geom, set(r.get("clip_to", "").split())))

    db = sqlite3.connect(f"file:{GADM}?mode=ro", uri=True)

    def split_side(line, point, donors):
        """The donors' GADM land on the holder's side of a line of control: split by the line, keep the side with point."""
        minx, miny, maxx, maxy = line.buffer(0.5).bounds
        land = []
        for fid, in db.execute("select id from rtree_gadm_410_geom where maxx>=? and minx<=? and maxy>=? and miny<=?",
                               (minx, maxx, miny, maxy)):
            blob, *gids = db.execute("select geom, GID_0, GID_1, GID_2, GID_3, GID_4, GID_5 from gadm_410 where fid=?",
                                     (fid,)).fetchone()
            if region_of([x for x in gids if x]) in donors:
                land.append(gpkg_geometry(blob))
        pt = Point(point)
        return unary_union([p for p in split(unary_union(land), line).geoms if p.intersects(pt.buffer(1e-6))])

    custom = [(r, s, u, split_side(g[1], g[2], d) if isinstance(g, tuple) else g, d) for r, s, u, g, d in custom]
    report = []
    for region, source, unit, geom, donors in custom:
        if geom is None:
            report.append({"region": region, "source": source, "unit": unit, "note": "geometry not available locally"})
            continue
        c = geom.representative_point()
        minx, miny, maxx, maxy = geom.bounds
        taken, land = {}, []
        for fid, in db.execute("select id from rtree_gadm_410_geom where maxx>=? and minx<=? and maxy>=? and miny<=?",
                               (minx, maxx, miny, maxy)):
            blob, *gids = db.execute("select geom, GID_0, GID_1, GID_2, GID_3, GID_4, GID_5 from gadm_410 where fid=?",
                                     (fid,)).fetchone()
            g = gpkg_geometry(blob)
            if not g.intersects(geom):
                continue
            part = g.intersection(geom)
            if part.is_empty:
                continue
            land.append(part)
            donor = region_of([x for x in gids if x])
            key = ("already its own" if donor == region else donor if donor in donors else f"clipped away: {donor}")
            taken[key] = taken.get(key, 0) + km2(part, c.x, c.y)
        total = km2(geom, c.x, c.y)
        on_land = km2(unary_union(land), c.x, c.y) if land else 0.0
        report.append({"region": region, "source": source, "unit": unit, "polygon_km2": round(total, 2),
                       "on_gadm_land_km2": round(on_land, 2),
                       "donors": sorted(donors), "taken_from": {k: round(v, 2) for k, v in sorted(taken.items(), key=lambda kv: -kv[1])}})

    overlaps = []
    shapes = [(r, u, g) for r, s, u, g, _ in custom if g is not None]
    for i, (r1, u1, g1) in enumerate(shapes):
        for r2, u2, g2 in shapes[i + 1:]:
            if r1 != r2 and g1.intersects(g2):
                inter = g1.intersection(g2)
                if not inter.is_empty and inter.area > 0:
                    c = inter.representative_point()
                    overlaps.append({"a": f"{r1} ({u1})", "b": f"{r2} ({u2})", "km2": round(km2(inter, c.x, c.y), 3)})
    out = {"custom_geometries": report, "overlaps_between_regions": overlaps}
    (ROOT / "release" / "custom_check.json").write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    for r in report:
        print(r)
    print("overlaps:", overlaps)


if __name__ == "__main__":
    main()
