#!/usr/bin/env python3
"""Pictures of the findings of check_display.py, drawn from the rendered geometry itself, for review.

Each picture shows every region in the finding's box, filled by region with its outline drawn, and the finding in red.
Seams and slits show as lines inside one colour; fragments as a red island of another colour. Drawn from
tools/map-viewer/public/data/regions.geojson, the file the map viewer shows (no browser needed).
Needs shapely and matplotlib. Run from the repository root after check_display.py:
    python experiments/release-draft/plot_findings.py [max] [--all]
--all also draws the findings that inputs/known_fragments.csv explains.
"""
import hashlib
import json
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import shapely  # noqa: E402
from matplotlib.patches import PathPatch  # noqa: E402
from matplotlib.path import Path as MPath  # noqa: E402
from shapely.geometry import shape  # noqa: E402

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[1]
DATA = REPO / "tools" / "map-viewer" / "public" / "data" / "regions.geojson"
OUT = ROOT / "cache" / "map" / "findings"


def colour(rid: str) -> tuple:
    h = hashlib.sha256(rid.encode()).digest()
    return (0.55 + h[0] / 640, 0.55 + h[1] / 640, 0.55 + h[2] / 640)


def patch(g, **style):
    verts, codes = [], []
    for p in getattr(g, "geoms", [g]):
        if p.geom_type != "Polygon":
            continue
        for ring in [p.exterior, *p.interiors]:
            xy = list(ring.coords)
            verts += xy
            codes += [MPath.MOVETO] + [MPath.LINETO] * (len(xy) - 2) + [MPath.CLOSEPOLY]
    return PathPatch(MPath(verts, codes), **style) if verts else None


def main() -> None:
    limit = int(next((a for a in sys.argv[1:] if a.isdigit()), 60))
    check = json.loads((ROOT / "cache" / "map" / "display_check.json").read_text(encoding="utf-8"))
    todo = [f for f in check["findings"] if f["visible"] and ("--all" in sys.argv or not f.get("explained"))]
    todo = sorted(todo, key=lambda f: -f.get("km2", 1))[:limit]
    features = json.loads(DATA.read_text(encoding="utf-8"))["features"]
    ids = [f["properties"]["id"] for f in features]
    geoms = [shapely.make_valid(shape(f["geometry"])) for f in features]
    tree = shapely.STRtree(geoms)
    OUT.mkdir(parents=True, exist_ok=True)
    for old in OUT.glob("*.png"):
        old.unlink()
    for i, f in enumerate(todo):
        x0, y0, x1, y1 = f["box"]
        # square-ish view around the finding
        span = max(x1 - x0, y1 - y0, 0.02)
        cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
        view = shapely.box(cx - span / 2, cy - span / 2, cx + span / 2, cy + span / 2)
        fig, ax = plt.subplots(figsize=(7, 7), dpi=110)
        ax.set_facecolor("#dfe8f0")
        shown = []
        for k in tree.query(view, predicate="intersects"):
            part = shapely.intersection(geoms[k], view.buffer(span * 0.05))
            pp = patch(part, facecolor=colour(ids[k]), edgecolor="black", linewidth=0.5)
            if pp:
                ax.add_patch(pp)
                c = part.representative_point()
                shown.append(ids[k])
                ax.annotate(ids[k], (c.x, c.y), fontsize=7, ha="center", color="#333")
        px, py = f["where"]
        ax.plot([px], [py], marker="o", markersize=14, markerfacecolor="none", markeredgecolor="red", markeredgewidth=1.5)
        ax.set_xlim(cx - span / 2, cx + span / 2)
        ax.set_ylim(cy - span / 2, cy + span / 2)
        ax.set_aspect(1 / max(0.2, abs(__import__("math").cos(__import__("math").radians(cy)))))
        label = {k: v for k, v in f.items() if k not in ("box", "visible", "where")}
        ax.set_title(json.dumps(label, ensure_ascii=False)[:150], fontsize=7, wrap=True)
        who = (f.get("region") or "+".join(f.get("between", [])))[:40]
        name = f"{i:03d}-{f['check']}-{''.join(c if c.isalnum() else '_' for c in who)}.png"
        fig.savefig(OUT / name, bbox_inches="tight")
        plt.close(fig)
        print(name)


if __name__ == "__main__":
    main()
