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
npm run dev                                               # http://localhost:5199 (fixed; fails if the port is taken)
```

`public/data/` holds GADM-derived geometry, whose licence forbids redistribution; it is gitignored.

## What it shows

- **Regions**, coloured by country under the chosen point of view (selector at the top right). Hover or click: why the region exists in plain words with links to the rules, its country in the canon and under the settling rule, the facts it rests on with sources and quoted passages, the separate regions taken out of it or counted to it, the countries the points of view give it, and the substrate units it is made of. Click pins a region and zooms to it; the search box finds a region by name or id.
- **Own geometries** (dashed outline): the canon's geometries from `data/custom-geometries`, with rank and whose line they draw.
- **Regions whose country differs** from the canon's under the chosen point of view (purple outline).
- **Special places** (orange) and **notes** (blue) of the Stage 1 list, at their Wikidata points (`experiments/release-draft/inputs/place_points.csv`), with what they are and why on hover; a region's details list the ones that lie in it, and entry rules for lists of places or classes of land are listed with their country without a point. A switch dims every region without any.
- An optional OpenStreetMap background.

Outlines are simplified for display (0.01° by default; `render_map.py --tolerance`), except in detail zones: boxes 0.2° wide around every region of the register of disputed areas and every own geometry (`--detail-margin`, 0 to switch off), where GADM rows are taken unsimplified and coordinates are kept to about a metre. What still shows there as a sliver is a real difference between sources, not a display artefact.
