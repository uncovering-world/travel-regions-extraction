#!/usr/bin/env python3
"""Write the data of the local map viewer (tools/map-viewer) from the rendered draft.

Reads the region polygons rendered by render_map.py (cache/map/regions.js), the release's regions.csv and
membership.csv, and the canon's own geometries; writes tools/map-viewer/public/data/regions.geojson and
own_geometries.geojson. The output contains GADM-derived geometry and stays out of git (the viewer's .gitignore).

Run from the repository root: python3 experiments/release-draft/export_viewer_data.py
"""
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[1]
OUT = REPO / "tools" / "map-viewer" / "public" / "data"


def main() -> None:
    js = (ROOT / "cache" / "map" / "regions.js").read_text(encoding="utf-8")
    rendered = json.loads(js[js.index("{"): js.index(";\nwindow.MISSING")])
    geometry = {f["properties"]["id"]: f["geometry"] for f in rendered["features"]}
    rows = {r["region_id"]: r for r in csv.DictReader((ROOT / "release" / "regions.csv").open(encoding="utf-8"))}
    membership = list(csv.DictReader((ROOT / "release" / "membership.csv").open(encoding="utf-8")))
    a3 = {c["alpha_2"]: c["alpha_3"] for c in json.loads(Path("/usr/share/iso-codes/json/iso_3166-1.json").read_text())["3166-1"]}
    features = []
    for rid, geom in geometry.items():
        r = rows.get(rid, {})
        povs = {k[4:]: v for k, v in r.items() if k.startswith("pov_")}
        povs["__canon_a3"] = a3.get(r.get("country_code", ""), "")
        units = [f"{m['role']} {m['source']} {m['unit']}" + (f" (clip to {m['clip_to']})" if m.get("clip_to") else "")
                 for m in membership if m["region_id"] == rid]
        features.append({"type": "Feature", "geometry": geom, "properties": {
            "id": rid, "name": r.get("name", rid), "country": r.get("country", ""), "country_code": r.get("country_code", ""),
            "basis": r.get("basis", ""), "evidence": r.get("evidence", ""), "open": r.get("open", ""),
            "wikidata_id": r.get("wikidata_id", ""), "povs": povs, "units": units[:20]}})
    own = []
    for s in csv.DictReader((REPO / "data" / "custom-geometries" / "sources.csv").open(encoding="utf-8")):
        data = json.loads((REPO / "data" / "custom-geometries" / s["file"]).read_text(encoding="utf-8"))
        for f in data["features"]:
            own.append({"type": "Feature", "geometry": f["geometry"], "properties": {
                k: s[k] for k in ("place", "region", "rank", "whose_line", "publisher", "licence")}})
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "regions.geojson").write_text(json.dumps({"type": "FeatureCollection", "features": features}, ensure_ascii=False))
    (OUT / "own_geometries.geojson").write_text(json.dumps({"type": "FeatureCollection", "features": own}, ensure_ascii=False))
    print(f"{len(features)} regions, {len(own)} own geometry features -> {OUT}")


if __name__ == "__main__":
    main()
