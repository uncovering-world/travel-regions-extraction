# Canon map viewer

A local viewer for a draft release of the canon: every region drawn from its membership rules, coloured by its country under the canon's attribution or under any of Natural Earth's 31 national points of view, with what it is made of on hover. For visual checks only; nothing here is published.

TypeScript, [MapLibre GL JS](https://maplibre.org/) and Vite.

## Run

```bash
# 1. geometry (needs shapely; GADM 4.1 at ../track-your-regions/deployment/gadm_410.gpkg or $GADM_GPKG)
python experiments/release-draft/render_map.py            # first run unites GADM units, about 15 minutes; cached after
python3 experiments/release-draft/export_viewer_data.py   # writes tools/map-viewer/public/data/

# 2. viewer
cd tools/map-viewer
npm install
npm run dev                                               # opens on http://localhost:5173
```

`public/data/` holds GADM-derived geometry, whose licence forbids redistribution; it is gitignored.

## What it shows

- **Regions**, coloured by country under the chosen point of view (selector at the top right). Hover: name, id, country, the countries other points of view give it, the rule it rests on, evidence level, open points, the GADM units and own geometries it is made of. Click pins a region and zooms to it; the search box finds a region by name or id.
- **Own geometries** (dashed outline): the canon's geometries from `data/custom-geometries`, with rank and whose line they draw.
- **Regions whose country differs** from the canon's under the chosen point of view (purple outline).
- An optional OpenStreetMap background.

Outlines are simplified for display (0.01° by default; `render_map.py --tolerance`).
