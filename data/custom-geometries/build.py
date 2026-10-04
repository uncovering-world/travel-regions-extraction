#!/usr/bin/env python3
"""Rebuild the canon's own geometries from the pinned inputs listed in sources.json.

Every place in sources.json names one input and the features of it that draw the place. The input is downloaded
into cache/ (gitignored) and checked against its pinned sha256; the selected features are written to the place's
GeoJSON file unmodified, except that several source features of one place are merged by a plain union, and that an
OpenStreetMap relation is assembled from its member ways (outer rings minus inner rings). An input of kind
"document-points" is a committed transcription (documents/) of the boundary points a cited document lists: its ring
is drawn with straight lines between the points, edges the document runs along a river follow a pinned OpenStreetMap
river line, and the areas the document excludes are cut out. A place whose land is divided by a line of control
(D066) is written as that line, from the member ways of a pinned OSM relation with both ends prolonged a little,
and a point on the holder's side; the consumer splits the donors' units by the line and keeps the side with the point. All inputs are already in
WGS84 longitude/latitude, so nothing is reprojected. No geometry is clipped here: the clip to the substrate (GADM)
units of each place's donor regions is expressed in the release's membership and done by the consumer (D062).
Files marked "kept" are not rebuilt; only their sha256 is checked.

The script also writes sources.csv, the readable table of sources.json.

Needs shapely (2.x). Run from anywhere:
    python3 data/custom-geometries/build.py            # build and write the files
    python3 data/custom-geometries/build.py --check    # build in memory and compare with the files on disk

Environment:
    CTR_WORLDPOLYGONS_GPKG  path to an existing copy of WorldPolygons11_4.gpkg (3.5 GB); it is verified by sha256
                            and used instead of extracting it from the publisher's 2.4 GB zip by range requests.
"""
import argparse
import csv
import hashlib
import io
import json
import os
import sqlite3
import struct
import sys
import time
import urllib.parse
import urllib.request
import zipfile
import zlib
from pathlib import Path

from shapely import wkb
from shapely.geometry import LineString, Point, Polygon, mapping, shape
from shapely.ops import linemerge, polygonize, substring, unary_union

HERE = Path(__file__).resolve().parent
CACHE = HERE / "cache"
USER_AGENT = "travel-regions-extraction custom-geometries build (https://github.com/uncovering-world/travel-regions-extraction)"
CSV_COLUMNS = ["place", "region", "donors", "rank", "whose_line", "publisher", "source_url", "version_or_date",
               "feature_id", "licence", "file", "notes"]


# ---------------------------------------------------------------- downloads


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1 << 22), b""):
            h.update(block)
    return h.hexdigest()


def http(url: str, data: bytes | None = None, headers: dict | None = None, timeout: int = 600) -> bytes:
    req = urllib.request.Request(url, data=data, headers={"User-Agent": USER_AGENT, **(headers or {})})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def http_range(url: str, start: int, end: int) -> bytes:
    return http(url, headers={"Range": f"bytes={start}-{end}"})


def zip_listing(url: str, base: int, size: int) -> dict:
    """Central directory of a zip that occupies bytes [base, base+size) of the remote file: name -> entry."""
    tail = http_range(url, base + max(0, size - 300000), base + size - 1)
    j = tail.rfind(b"PK\x06\x06")
    if j >= 0:
        z = tail[j:j + 56]
        cd_size, cd_off = struct.unpack("<QQ", z[40:56])
    else:
        i = tail.rfind(b"PK\x05\x06")
        cd_size, cd_off = struct.unpack("<II", tail[i + 12:i + 20])
    cd = http_range(url, base + cd_off, base + cd_off + cd_size - 1)
    out, p = {}, 0
    while p < len(cd):
        (_, _, _, _, method, _, _, _, csize, usize, fnl, exl, cml, _, _, _, lho) = struct.unpack(
            "<IHHHHHHIIIHHHHHII", cd[p:p + 46])
        name = cd[p + 46:p + 46 + fnl].decode()
        extra, q = cd[p + 46 + fnl:p + 46 + fnl + exl], 0
        while q < len(extra):
            hid, hs = struct.unpack("<HH", extra[q:q + 4])
            if hid == 1:
                vals, k = extra[q + 4:q + 4 + hs], 0
                if usize == 0xFFFFFFFF:
                    usize = struct.unpack("<Q", vals[k:k + 8])[0]; k += 8
                if csize == 0xFFFFFFFF:
                    csize = struct.unpack("<Q", vals[k:k + 8])[0]; k += 8
                if lho == 0xFFFFFFFF:
                    lho = struct.unpack("<Q", vals[k:k + 8])[0]; k += 8
            q += 4 + hs
        out[name] = {"method": method, "csize": csize, "usize": usize, "lho": lho}
        p += 46 + fnl + exl + cml
    return out


def zip_data_start(url: str, base: int, lho: int) -> int:
    h = http_range(url, base + lho, base + lho + 29)
    fnl, exl = struct.unpack("<HH", h[26:30])
    return base + lho + 30 + fnl + exl


def fetch_nested_zip_member(url: str, members: list, dest: Path) -> None:
    """Extract members[-1] from a chain of zips nested in the remote file, by HTTP range requests only."""
    size = int(urllib.request.urlopen(urllib.request.Request(url, method="HEAD", headers={"User-Agent": USER_AGENT}),
                                      timeout=120).headers["Content-Length"])
    base = 0
    for depth, name in enumerate(members):
        entry = zip_listing(url, base, size)[name]
        start = zip_data_start(url, base, entry["lho"])
        if depth < len(members) - 1:
            if entry["method"] != 0:
                raise SystemExit(f"{name}: nested zip is compressed; cannot range-read it")
            base, size = start, entry["csize"]
            continue
        tmp = dest.with_suffix(dest.suffix + ".part")
        inflater = zlib.decompressobj(-15) if entry["method"] == 8 else None
        req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT,
                                                   "Range": f"bytes={start}-{start + entry['csize'] - 1}"})
        with urllib.request.urlopen(req, timeout=600) as r, tmp.open("wb") as f:
            for block in iter(lambda: r.read(1 << 22), b""):
                f.write(inflater.decompress(block) if inflater else block)
            if inflater:
                f.write(inflater.flush())
        tmp.rename(dest)


def overpass(endpoints: list, query: str) -> dict:
    last = None
    for attempt in range(8):
        for ep in endpoints:
            try:
                body = http(ep, data=urllib.parse.urlencode({"data": query}).encode(), timeout=900)
                return json.loads(body)
            except Exception as e:  # busy servers answer 429/504 or an HTML error page
                last = e
                print(f"  overpass {ep}: {e}; retrying", file=sys.stderr)
        time.sleep(min(300, 20 * 2 ** attempt))
    raise SystemExit(f"Overpass failed: {last}")


def osm_canonical(data: dict, date: str) -> bytes:
    """The cached form of an Overpass answer: its elements, sorted, without the server's run-time header."""
    elements = sorted(data["elements"], key=lambda e: (e["type"], e["id"]))
    doc = {"overpass_date": date, "copyright": data.get("osm3s", {}).get("copyright"), "elements": elements}
    return (json.dumps(doc, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode()


def ensure_input(key: str, spec: dict) -> Path:
    CACHE.mkdir(exist_ok=True)
    path = CACHE / spec["cache_file"]
    if spec["kind"] == "worldpolygons-gpkg" and not path.exists() and os.environ.get("CTR_WORLDPOLYGONS_GPKG"):
        src = Path(os.environ["CTR_WORLDPOLYGONS_GPKG"])
        if sha256_file(src) != spec["sha256"]:
            raise SystemExit(f"{src}: sha256 differs from the pinned {spec['sha256']}")
        return src
    if spec["kind"] == "document-points":
        path = HERE / spec["path"]
    elif not path.exists():
        print(f"fetching {key} …", file=sys.stderr)
        if spec["kind"] == "worldpolygons-gpkg":
            fetch_nested_zip_member(spec["url"], spec["zip_members"], path)
        elif spec["kind"] == "osm-overpass":
            q = "".join(f"{t}(id:{','.join(str(i) for i in ids)});" for t, ids in spec["elements"].items())
            query = f'[out:json][timeout:800][date:"{spec["date"]}"];({q});out meta geom;'
            path.write_bytes(osm_canonical(overpass(spec["endpoints"], query), spec["date"]))
        else:
            path.write_bytes(http(spec["url"]))
    digest = sha256_file(path)
    if digest != spec["sha256"]:
        raise SystemExit(f"{key}: {path} has sha256 {digest}, pinned {spec['sha256']}. "
                         "The publisher's file changed: review it and re-pin in sources.json.")
    return path


# ---------------------------------------------------------------- readers


def gpkg_geometry(blob: bytes):
    flags = blob[3]
    envelope = {0: 0, 1: 32, 2: 48, 3: 48, 4: 64}[(flags >> 1) & 7]
    return wkb.loads(bytes(blob[8 + envelope:]))


def read_gpkg(path: Path, sel: dict) -> list:
    db = sqlite3.connect(f"file:{path}?mode=ro", uri=True)
    cols = [r[1] for r in db.execute(f'pragma table_info("{sel["layer"]}")')]
    out = []
    for fid in sel["fids"]:
        row = db.execute(f'select * from "{sel["layer"]}" where fid=?', (fid,)).fetchone()
        rec = dict(zip(cols, row))
        attrs = {k: rec[k] for k in sel["attributes"]}
        out.append((f"{sel['layer']} fid {fid}", attrs, gpkg_geometry(rec["geom"]), None))
    return out


def read_geojson_features(data: dict, sel: dict) -> list:
    wanted = [str(v) for v in sel["values"]]
    found = {}
    for f in data["features"]:
        v = str(f["properties"].get(sel["property"]))
        if v in wanted:
            found[v] = f
    out = []
    for v in wanted:
        f = found[v]
        attrs = {k: f["properties"].get(k) for k in sel["attributes"]}
        out.append((f"{sel.get('member', '')} {sel['property']}={v}".strip(), attrs, shape(f["geometry"]), f["geometry"]))
    return out


def read_geojson(path: Path, sel: dict) -> list:
    if "member" in sel:
        with zipfile.ZipFile(path) as z:
            data = json.loads(z.read(sel["member"]))
    else:
        data = json.loads(path.read_bytes())
    return read_geojson_features(data, sel)


def osm_polygon(e: dict):
    if e["type"] == "way":
        return Polygon([(p["lon"], p["lat"]) for p in e["geometry"]])
    outer, inner = [], []
    for m in e["members"]:
        if m["type"] != "way" or "geometry" not in m:
            continue
        line = LineString([(p["lon"], p["lat"]) for p in m["geometry"]])
        (inner if m["role"] == "inner" else outer).append(line)

    def faces(lines):
        if not lines:
            return Polygon()
        noded = unary_union(lines)
        return unary_union(list(polygonize(list(getattr(noded, "geoms", [noded])))))

    o, i = faces(outer), faces(inner)
    return o.difference(i) if not i.is_empty else o


def read_osm(path: Path, sel: dict) -> list:
    data = json.loads(path.read_bytes())
    index = {(e["type"], e["id"]): e for e in data["elements"]}
    out = []
    for etype, eid, version in sel["elements"]:
        e = index[(etype, eid)]
        if e.get("version") != version:
            raise SystemExit(f"OSM {etype} {eid}: version {e.get('version')} in the input, pinned {version}")
        tags = e.get("tags", {})
        attrs = {"osm": f"{etype}/{eid}", "version": e["version"], "timestamp": e["timestamp"],
                 **{k: tags[k] for k in sel.get("attributes", []) if k in tags}}
        out.append((f"{etype} {eid} v{version}", attrs, osm_polygon(e), None))
    return out


def dms(text: str) -> float:
    """Degrees, minutes and seconds as a document prints them ("45 42 10" or "45 44 14,16")."""
    d, m, sec = text.replace(",", ".").split()
    return float(d) + float(m) / 60 + float(sec) / 3600


def read_document(path: Path, sel: dict, inputs: dict, paths: dict) -> list:
    doc = json.loads(path.read_bytes())
    ring = doc[sel["ring"]]
    pts = [(dms(p["lon"]), dms(p["lat"])) for p in ring["points"]]
    along = {tuple(e) for e in ring.get("along_river", [])}
    river, river_ids = None, []
    if along:
        data = json.loads(paths[sel["river"]["input"]].read_bytes())
        ways = {e["id"]: e for e in data["elements"] if e["type"] == "way"}
        for wid, version in sel["river"]["ways"]:
            if ways[wid].get("version") != version:
                raise SystemExit(f"OSM way {wid}: version {ways[wid].get('version')} in the input, pinned {version}")
        river = linemerge([LineString([(p["lon"], p["lat"]) for p in ways[w]["geometry"]]) for w, _ in sel["river"]["ways"]])
        if river.geom_type != "LineString":
            raise SystemExit("the pinned river ways do not join into one line")
        river_ids = [f"way {w} v{v}" for w, v in sel["river"]["ways"]]
    coords = []
    for i, p in enumerate(pts):
        coords.append(p)
        a, b = i + 1, (i + 1) % len(pts) + 1
        if (a, b) in along:  # the document runs this edge along the river bank: follow the river line
            seg = substring(river, river.project(Point(p)), river.project(Point(pts[b - 1])))
            coords.extend(list(seg.coords)[1:-1])
    outer = Polygon(coords)
    holes = {name: Polygon([(dms(q["lon"]), dms(q["lat"])) for q in points]) for name, points in doc[sel["holes"]].items()}
    geom = outer.difference(unary_union(list(holes.values())))
    if not geom.is_valid:
        raise SystemExit(f"{path.name}: the outline is not valid")
    attrs = {"document": doc["document"], "locator": doc["locator"], "file_sha256": doc["file_sha256"],
             "points": len(pts), "along_river": sorted(map(list, along)), "cut_out": sorted(holes),
             "river": river_ids, "not_drawn": doc.get("not_drawn", "")}
    return [(f"{path.name} {sel['ring']}", attrs, geom, None)]


# ---------------------------------------------------------------- build


def control_line(path: Path, sel: dict) -> tuple[dict, str]:
    """A line of control (D066) from the member ways of a pinned OSM relation, joined into one line; each end is
    prolonged straight along its last segment by prolong_deg so that the line crosses the substrate's own line."""
    data = json.loads(path.read_bytes())
    (etype, eid, version), = sel["elements"]
    rel = next(e for e in data["elements"] if e["type"] == etype and e["id"] == eid)
    if rel.get("version") != version:
        raise SystemExit(f"OSM {etype} {eid}: version {rel.get('version')} in the input, pinned {version}")
    members = {m["ref"]: m for m in rel["members"] if m["type"] == "way"}
    line = linemerge([LineString([(p["lon"], p["lat"]) for p in members[w]["geometry"]]) for w in sel["control_line"]["ways"]])
    if line.geom_type != "LineString":
        raise SystemExit(f"{etype} {eid}: the control-line ways do not join into one line")
    c, step = list(line.coords), sel["control_line"]["prolong_deg"]

    def beyond(a, b):
        dx, dy = a[0] - b[0], a[1] - b[1]
        n = (dx * dx + dy * dy) ** 0.5
        return (round(a[0] + dx / n * step, 7), round(a[1] + dy / n * step, 7))

    line = LineString([beyond(c[0], c[1])] + c + [beyond(c[-1], c[-2])])
    ways = ", ".join(str(w) for w in sel["control_line"]["ways"])
    return mapping(line), (f"line of control (D066): ways {ways} of the relation joined into one line, each end prolonged "
                           f"by {step}° along its last segment; split the donors by it and keep the side with holder_point")


def build_place(place: dict, inputs: dict, paths: dict) -> bytes:
    sel = place["select"]
    path = paths[place["input"]]
    kind = inputs[place["input"]]["kind"]
    if kind == "worldpolygons-gpkg":
        feats = read_gpkg(path, sel)
    elif kind == "document-points":
        feats = read_document(path, sel, inputs, paths)
    elif kind == "osm-overpass":
        feats = read_osm(path, sel)
    else:
        feats = read_geojson(path, sel)
    if len(feats) == 1 and feats[0][3] is not None:
        geometry, operation = feats[0][3], "none (the source feature's geometry as published)"
    elif len(feats) == 1:
        geometry = mapping(feats[0][2])
        operation = ("assembled from the OSM element's member ways (outer minus inner)" if kind == "osm-overpass"
                     else "the document's points joined by straight lines, river edges along the pinned river line, "
                          "excluded areas cut out" if kind == "document-points"
                     else "none (the source feature's geometry as published)")
    else:
        geometry = mapping(unary_union([f[2] for f in feats]))
        operation = f"union of the {len(feats)} source features"
    if "control_line" in sel:
        # D066: the land is divided by a line of control, not outlined: the file is that line, with a point on the
        # holder's side; the consumer splits the donors' substrate units by it and keeps the side with the point
        geometry, operation = control_line(path, sel)
    geometry = json.loads(json.dumps(geometry))  # tuples -> lists
    props = {k: place[k] for k in CSV_COLUMNS if k not in ("file", "notes")}
    if "holder_point" in sel:
        props["holder_point"] = sel["holder_point"]
    props.update({"notes": place["notes"], "input_sha256": inputs[place["input"]]["sha256"],
                  "operation": operation, "crs": "WGS84 longitude/latitude, as in the source (no reprojection)",
                  "source_features": [{"id": f[0], **f[1]} for f in feats]})
    doc = {"type": "FeatureCollection",
           "features": [{"type": "Feature", "properties": props, "geometry": geometry}]}
    return (json.dumps(doc, ensure_ascii=False, separators=(",", ":")) + "\n").encode()


def sources_csv(places: list) -> bytes:
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=CSV_COLUMNS, lineterminator="\n")
    w.writeheader()
    for p in places:
        w.writerow({k: p[k] for k in CSV_COLUMNS})
    return buf.getvalue().encode()


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--check", action="store_true", help="compare with the files on disk instead of writing")
    args = ap.parse_args()
    spec = json.loads((HERE / "sources.json").read_text())
    inputs, places = spec["inputs"], spec["places"]
    needed = {p["input"] for p in places if p["input"] in inputs}
    needed |= {p["select"]["river"]["input"] for p in places if "river" in p["select"]}
    paths = {k: ensure_input(k, inputs[k]) for k in sorted(needed)}
    outputs = {"sources.csv": sources_csv(places)}
    failures = []
    for p in places:
        if p["select"].get("kind") == "kept":
            digest = sha256_file(HERE / p["file"])
            if digest != p["select"]["sha256"]:
                failures.append(f"{p['file']}: sha256 {digest}, pinned {p['select']['sha256']}")
            continue
        outputs[p["file"]] = build_place(p, inputs, paths)
    for name, data in outputs.items():
        target = HERE / name
        if args.check:
            if not target.exists() or target.read_bytes() != data:
                failures.append(f"{name}: differs from a fresh build")
        else:
            target.write_bytes(data)
    for f in failures:
        print("FAIL", f, file=sys.stderr)
    print(f"{'checked' if args.check else 'wrote'} {len(outputs)} files; {len(failures)} failures", file=sys.stderr)
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
