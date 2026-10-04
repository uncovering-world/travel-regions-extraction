# First draft of a release package

**A draft, not a release and not the canon.** Built to see the package of R059 (D060) filled end to end. Issue [#22](https://github.com/uncovering-world/travel-regions-extraction/issues/22).

```bash
python3 experiments/release-draft/build.py
```

## What goes in

- Regions: the [Stage 1 list](../stage1-list/README.md) (314 regions).
- Substrate units: the [GADM binding](../gadm-binding/README.md) (GADM 4.1 unit identifiers; no GADM geometry is copied).
- The canon's own geometries: [data/custom-geometries](../../data/custom-geometries/README.md), 42 places, sources ranked by whose line they draw (D062), each with the regions it may take land from (`donors`).
- Reviewed tables in `inputs/`: `attribution.csv` (the country of each non-ISO region under the canon's attribution, with its basis) and `gadm_leftovers.csv` (GADM pseudo-countries no region claims).

## What comes out (`release/`)

- `canon.json` — TYR's import tree: World → country → regions (a country with one region is a leaf).
- `regions.csv` — 314 regions with name, Wikidata id, basis, country and evidence level.
- `membership.csv` — 402 rows. A region is the union of its `include` rows minus its `exclude` rows; an own geometry (precedence 1), clipped by the consumer to the GADM units of the regions in `clip_to`, wins over GADM units (precedence 2), so land GADM gives to another country (Siachen, Demchok, Halayib…) goes where the canon says, and no geometry reaches into a neighbouring country.
- `geometry/` — the 42 own geometries, as in `data/custom-geometries/` (licences per file there; 13 OpenStreetMap-derived files are under ODbL).
- `manifest.json` — versions, the membership rule and the sha256 of every input.
- `gaps.csv` — empty in this build.

## Checks

`check_cover.py` assigns every one of GADM 4.1's 356,508 rows (its smallest units) to regions by the membership rules, by identifiers alone. Result (`release/cover_check.json`): 356,507 rows fall into exactly one region; one, the Caspian Sea (`XCA`), into none, as intended (water). So the GADM part of the partition has no gaps and no overlaps.

`check_custom.py` (needs shapely and pyproj) intersects every own geometry with the GADM units under it and reports, in km², the land it takes from each donor region and the land the clip removes (`release/custom_check.json`). With the ranked sources and the clip (D062): intended moves are kept (Siachen 2,154 km² from Gilgit-Baltistan, Halayib 17,799 km² from Sudan, Demchok's India-held sector 435 km² from China); what the clip removes is small and all of it outside the donors — Somaliland 176 km² of Ethiopia and 3 km² of Djibouti, South Ossetia 15 km² of Russia, Siachen 12 km² of China, Kalapani 13 km² of Tibet, the Cyprus buffer zone 2 km² of the Sovereign Base Areas. Island geometries mostly add land GADM lacks. One overlap between own geometries remains: the 1949 no-man's-lands and East Jerusalem share 0.1 km².

An earlier run on Natural Earth's polygons alone had shown how far they were off (the Korean DMZ about 2.5 times too wide, the Cyprus buffer zone displaced, Natural Earth's "Bhutan (northwest valleys)" lying inside China) and how they reached into neighbouring countries (Somaliland 747 km² of Ethiopia); that led to D062.

## What is not checked
- Only one perspective (the canon's attribution) is in `regions.csv`; the other declared perspectives are not yet columns.
- No correspondence table: this is the first draft.
- TYR's importer reads only the tree; binding by unit identifiers and own geometry need the importer changes listed in the [output-format proposal](../../docs/proposals/output-format.md).
