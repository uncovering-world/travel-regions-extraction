"""Which GADM 4.1 polygon contains a point? Pure Python: rtree prefilter, then ray casting on the GPKG WKB."""
import sqlite3, struct, sys
import os
from pathlib import Path
GADM = Path(os.environ.get('GADM_GPKG', Path(__file__).resolve().parents[3] / 'track-your-regions' / 'deployment' / 'gadm_410.gpkg'))
DB = f'file:{GADM}?mode=ro'

def polygons(blob):
    flags = blob[3]; env = (flags >> 1) & 7
    off = 8 + {0: 0, 1: 32, 2: 48, 3: 48, 4: 64}[env]
    wkb = blob[off:]
    out = []
    def read(pos):
        bo = '<' if wkb[pos] == 1 else '>'
        t = struct.unpack(bo + 'I', wkb[pos+1:pos+5])[0] % 1000
        pos += 5
        if t == 3:
            n = struct.unpack(bo + 'I', wkb[pos:pos+4])[0]; pos += 4; rings = []
            for _ in range(n):
                m = struct.unpack(bo + 'I', wkb[pos:pos+4])[0]; pos += 4
                pts = struct.unpack(bo + 'd' * (2 * m), wkb[pos:pos + 16 * m]); pos += 16 * m
                rings.append(list(zip(pts[0::2], pts[1::2])))
            out.append(rings); return pos
        if t == 6:
            n = struct.unpack(bo + 'I', wkb[pos:pos+4])[0]; pos += 4
            for _ in range(n): pos = read(pos)
            return pos
        raise ValueError(t)
    read(0)
    return out

def inside(ring, x, y):
    c = False
    for (x1, y1), (x2, y2) in zip(ring, ring[1:] + ring[:1]):
        if (y1 > y) != (y2 > y) and x < (x2 - x1) * (y - y1) / (y2 - y1) + x1:
            c = not c
    return c

def which(x, y):
    db = sqlite3.connect(DB, uri=True)
    ids = [r[0] for r in db.execute("select id from rtree_gadm_410_geom where minx<=? and maxx>=? and miny<=? and maxy>=?", (x, x, y, y))]
    hits = []
    for fid in ids:
        blob, g0, g1, n1, g2, n2 = db.execute("select geom,GID_0,GID_1,NAME_1,GID_2,NAME_2 from gadm_410 where fid=?", (fid,)).fetchone()
        for poly in polygons(blob):
            if inside(poly[0], x, y) and not any(inside(h, x, y) for h in poly[1:]):
                hits.append((g0, g1, n1, g2, n2)); break
    return ids, hits

if __name__ == '__main__':
    x, y = float(sys.argv[1]), float(sys.argv[2])
    ids, hits = which(x, y)
    print(f'point {x},{y}: {len(ids)} bounding boxes, contained in: {hits or "NO GADM POLYGON"}')
