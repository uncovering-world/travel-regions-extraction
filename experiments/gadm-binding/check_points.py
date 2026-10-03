#!/usr/bin/env python3
"""Where does GADM put each Natural Earth disputed area? Point check at Natural Earth's label point. Q013.

For each of the 99 features of Natural Earth's disputed-areas layer (the pinned edition the registry uses), find the
GADM 4.1 unit that contains its label point (LABEL_X, LABEL_Y), and report it next to the register area and the
Stage 1 list's treatment of that area. A label point is one point, not the outline: this finds where GADM puts the
place, not whether GADM's line follows the stated one.

Run from the repository root: python3 experiments/gadm-binding/check_points.py
"""
import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[1]
sys.path.insert(0, str(ROOT))
from gadm_points import which  # noqa: E402

ne = json.loads((REPO / "experiments" / "stage1-world-draft" / "cache" / "ne_10m_admin_0_disputed_areas.geojson").read_text())
areas = {}
for r in csv.DictReader((REPO / "data" / "disputed-areas" / "facts.csv").open(encoding="utf-8")):
    pass
links = {}
for r in csv.DictReader((REPO / "experiments" / "stage1-list" / "inputs" / "links.csv").open(encoding="utf-8")):
    if r["registry_cell"]:
        links[r["registry_cell"].rsplit("#", 1)[1]] = r["area_id"]
    if r.get("small_feature"):
        links[r["small_feature"]] = r["area_id"]
treatment = {}
for name in ("regions", "special_places", "markers"):
    for r in csv.DictReader((REPO / "experiments" / "stage1-list" / "outputs" / f"{name}.csv").open(encoding="utf-8")):
        key = r.get("id", "").split("/", 1)[-1] if name != "markers" else r["area_id"]
        treatment.setdefault(key, name[:-1] if name != "special_places" else "special place")
rows = []
for f in sorted(ne["features"], key=lambda f: f["properties"]["NE_ID"]):
    p = f["properties"]
    area = links.get(str(p["NE_ID"])) or links.get(p.get("NAME"), "")
    _, hits = which(p["LABEL_X"], p["LABEL_Y"])
    rows.append({"ne_id": p["NE_ID"], "ne_name": p.get("BRK_NAME") or p.get("NAME"), "ne_note": p.get("NOTE_BRK") or "",
                 "label_x": p["LABEL_X"], "label_y": p["LABEL_Y"], "register_area": area,
                 "canon": treatment.get(area, ""), "gadm_gid_0": hits[0][0] if hits else "",
                 "gadm_unit": " / ".join(x for x in hits[0][1:] if x) if hits else "no GADM polygon"})
out = ROOT / "outputs" / "disputed_points.csv"
with out.open("w", encoding="utf-8", newline="") as handle:
    writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
print(f"{len(rows)} features; {sum(1 for r in rows if not r['gadm_gid_0'])} with no GADM polygon at the label point")
