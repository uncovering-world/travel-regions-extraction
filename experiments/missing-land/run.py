#!/usr/bin/env python3
"""Land World Polygons 11.4 draws and GADM 4.1 does not (see README). Run from the repository root."""
import csv
import hashlib
import json
import math
import os
import sqlite3
from pathlib import Path

import shapely
from pyproj import Geod
from shapely.geometry import shape

REPO = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
GADM = Path(os.environ.get("GADM_GPKG", REPO.parent / "track-your-regions" / "deployment" / "gadm_410.gpkg"))
WP = REPO / "data" / "custom-geometries" / "cache" / "WorldPolygons11_4.gpkg"
POINTS = Path.home() / "tyr-exports" / "real-points-2026-11-19.csv"
MIN_KM2 = 0.01
NEAR_M = 1000
GEOD = Geod(ellps="WGS84")


def gpkg_geometry(blob: bytes):
    flags = blob[3]
    envelope = {0: 0, 1: 32, 2: 48, 3: 48, 4: 64}[(flags >> 1) & 7]
    return shapely.from_wkb(blob[8 + envelope:])


def km2(g) -> float:
    return abs(GEOD.geometry_area_perimeter(g)[0]) / 1e6


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def main() -> None:
    gadm = sqlite3.connect(f"file:{GADM}?mode=ro", uri=True)
    wp = sqlite3.connect(f"file:{WP}?mode=ro", uri=True)
    own = [shape(f["geometry"]) for p in sorted((REPO / "data" / "custom-geometries" / "land").glob("*.geojson"))
           for f in json.loads(p.read_text())["features"]]
    own_tree = shapely.STRtree(own)
    cache = {}

    def unit(fid):
        if fid not in cache:
            if len(cache) > 3000:
                cache.clear()
            cache[fid] = shapely.make_valid(gpkg_geometry(
                gadm.execute("select geom from gadm_410 where fid = ?", (fid,)).fetchone()[0]))
        return cache[fid]

    def in_gadm(pt) -> bool:
        for (fid,) in gadm.execute("select id from rtree_gadm_410_geom where minx <= ? and maxx >= ? and miny <= ? "
                                   "and maxy >= ?", (pt.x, pt.x, pt.y, pt.y)):
            if unit(fid).covers(pt):
                return True
        return False

    def uncovered(part):
        """The part of `part` no GADM unit and no own land file covers."""
        x0, y0, x1, y1 = part.bounds
        units = [unit(fid) for (fid,) in gadm.execute(
            "select id from rtree_gadm_410_geom where minx <= ? and maxx >= ? and miny <= ? and maxy >= ?",
            (x1, x0, y1, y0))]
        units += [own[i] for i in own_tree.query(part)]
        units = [u for u in units if u.intersects(part)]
        return shapely.difference(part, shapely.union_all(units)) if units else part

    missing, tested = [], 0
    for fid, blob, name, genc3, iso in wp.execute(
            "select fid, geom, WP_Name, GENC_3, ISO_3166_1 from DoS_WP_11_4 order by fid"):
        g = gpkg_geometry(blob)
        for part in getattr(g, "geoms", [g]):
            if part.geom_type != "Polygon":
                continue
            # a cheap degree-area filter before the geodesic one
            if part.area * 12364 * max(math.cos(math.radians(part.representative_point().y)), 0.01) < MIN_KM2 / 2:
                continue
            area = km2(part)
            if area < MIN_KM2:
                continue
            tested += 1
            pt = part.representative_point()
            if in_gadm(pt):
                continue
            if any(own[i].covers(pt) for i in own_tree.query(pt)):
                continue
            # the point may fall in a lagoon or lake GADM leaves out: measure what is really uncovered
            gap = uncovered(part)
            gap_km2 = km2(gap) if not gap.is_empty else 0.0
            if gap_km2 < max(MIN_KM2, 0.5 * area):
                continue
            pt = gap.representative_point()
            missing.append({"wp_fid": fid, "wp_name": name, "genc_3": genc3, "iso_3166_1": iso or "",
                            "lon": round(pt.x, 6), "lat": round(pt.y, 6), "km2": round(area, 4),
                            "uncovered_km2": round(gap_km2, 4), "part": gap})
    # catalogue points within NEAR_M of each missing part
    pts = [(float(r["lon"]), float(r["lat"]), r["experience_name"]) for r in csv.DictReader(POINTS.open())]
    ptree = shapely.STRtree([shapely.Point(x, y) for x, y, _ in pts])
    for m in missing:
        lat = m["lat"]
        deg = NEAR_M / (111320 * max(math.cos(math.radians(lat)), 0.05))
        near = [pts[i] for i in ptree.query(m["part"].buffer(deg))
                if GEOD.inv(pts[i][0], pts[i][1], *shapely.ops.nearest_points(m["part"], shapely.Point(pts[i][:2]))[0].coords[0])[2] <= NEAR_M]
        m["points_within_1km"] = len(near)
        m["example_point"] = near[0][2] if near else ""
        del m["part"]
    missing.sort(key=lambda m: (-m["uncovered_km2"], m["wp_fid"]))
    (HERE / "outputs").mkdir(exist_ok=True)
    with (HERE / "outputs" / "missing.csv").open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(missing[0].keys()) if missing else ["wp_fid"], lineterminator="\n")
        w.writeheader()
        w.writerows(missing)
    by_country = {}
    for m in missing:
        c = by_country.setdefault(m["genc_3"] or m["wp_name"], {"parts": 0, "km2": 0.0, "near_points": 0})
        c["parts"] += 1
        c["km2"] = round(c["km2"] + m["uncovered_km2"], 4)
        c["near_points"] += m["points_within_1km"]
    summary = {"min_km2": MIN_KM2, "parts_tested": tested, "missing_parts": len(missing),
               "missing_km2": round(sum(m["uncovered_km2"] for m in missing), 3),
               "missing_parts_near_points": sum(1 for m in missing if m["points_within_1km"]),
               "missing_over_1km2": sum(1 for m in missing if m["uncovered_km2"] >= 1),
               "by_country": dict(sorted(by_country.items(), key=lambda kv: -kv[1]["km2"])),
               "inputs": {"WorldPolygons11_4.gpkg": sha256(WP), "points": sha256(POINTS),
                          "gadm_410.gpkg size": GADM.stat().st_size}}
    (HERE / "outputs" / "summary.json").write_text(json.dumps(summary, indent=1, ensure_ascii=False) + "\n")
    print(json.dumps({k: v for k, v in summary.items() if k != "by_country"}, indent=1))


if __name__ == "__main__":
    import shapely.ops  # noqa: F401  (nearest_points)
    main()
