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

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[1]
GADM = Path(os.environ.get("GADM_GPKG", REPO.parent / "track-your-regions" / "deployment" / "gadm_410.gpkg"))
OUT = ROOT / "cache" / "map"


def gpkg_geometry(blob):
    envelope = {0: 0, 1: 32, 2: 48, 3: 48, 4: 64}[(blob[3] >> 1) & 7]
    return wkb.loads(bytes(blob[8 + envelope:]))


def log(message):
    print(time.strftime("%H:%M:%S"), message, file=sys.stderr, flush=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--tolerance", type=float, default=0.01, help="display simplification, degrees")
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
    apply_own(geoms, membership)
    write(geoms, regions, membership, args.tolerance)


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
    ids = sorted(geoms)
    tree = shapely.STRtree([geoms[i] for i in ids])
    for m in membership:
        if m["source"] != "custom geometry":
            continue
        data = json.loads((REPO / "data" / "custom-geometries" / m["unit"]).read_text())
        geom = shapely.make_valid(shapely.union_all([shape(f["geometry"]) for f in data["features"]]))
        donors = [d for d in m.get("clip_to", "").split() if d in geoms]
        taken = shapely.intersection(geom, shapely.union_all([geoms[d] for d in donors])) if donors else shapely.Polygon()
        near = [geoms[ids[i]] for i in tree.query(geom)]
        uncovered = shapely.difference(geom, shapely.union_all(near)) if near else geom
        piece = shapely.make_valid(shapely.union_all([taken, uncovered]))
        for d in donors:
            geoms[d] = shapely.make_valid(shapely.difference(geoms[d], piece))
        own[m["region_id"]].append(piece)
    for rid, pieces in own.items():
        geoms[rid] = shapely.make_valid(shapely.union_all(pieces + ([geoms[rid]] if rid in geoms else [])))
    log("own geometries applied")


def write(geoms, regions, membership, tolerance):
    """Display features for the simple HTML page (index.html, regions.js)."""
    features = []
    for rid, geom in sorted(geoms.items()):
        r = regions.get(rid, {"name": rid})
        povs = {k[4:]: v for k, v in r.items() if k.startswith("pov_") and v}
        majority = max(set(povs.values()), key=list(povs.values()).count) if povs else ""
        differing = {k: v for k, v in povs.items() if v != majority}
        simple = geom.simplify(tolerance, preserve_topology=True)
        if simple.is_empty:
            simple = geom
        features.append({"type": "Feature", "geometry": mapping(shapely.set_precision(simple, 1e-4)), "properties": {
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
