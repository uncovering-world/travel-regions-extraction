# First draft of a release package

**A draft, not a release and not the canon.** Built to see the package of R059 (D060) filled end to end. Issue [#22](https://github.com/uncovering-world/travel-regions-extraction/issues/22).

```bash
python3 experiments/release-draft/build.py
```

## What goes in

- Regions: the [Stage 1 list](../stage1-list/README.md) (314 regions after the corrections of 2026-10-04).
- Substrate units: the [GADM binding](../gadm-binding/README.md) (GADM 4.1 unit identifiers; no GADM geometry is copied).
- The canon's own geometries (D059): Natural Earth v5.1.2 disputed-area features referenced by id; OpenStreetMap relations for Gornja Siga and Socotra (versions still to be pinned); `data/custom-geometries/koalou.geojson` (D061).
- Reviewed tables in `inputs/`: `attribution.csv` (the country of each non-ISO region under the canon's attribution, with its basis), `custom_assignments.csv` (to which region the land of each special place or uncovered islet goes, from its holder or Natural Earth's "Admin. by"), `gadm_leftovers.csv` (GADM pseudo-countries no region claims), `osm_geometries.csv`.

## What comes out (`release/`)

- `canon.json` — TYR's import tree: World → country → regions (a country with one region is a leaf).
- `regions.csv` — 314 regions with name, Wikidata id, basis, country and evidence level.
- `membership.csv` — 406 rows. A region is the union of its `include` rows minus its `exclude` rows; a custom geometry (precedence 1) wins over GADM units (precedence 2), so land GADM gives to another country (Siachen, Demchok, Halayib…) goes where the canon says.
- `geometry/` — the one geometry this package carries (Koalou).
- `manifest.json` — versions, the membership rule and the sha256 of every input.
- `gaps.csv` — empty in this build.

## Checks

`check_cover.py` assigns every one of GADM 4.1's 356,508 rows (its smallest units) to regions by the membership rules, by identifiers alone. Result (`release/cover_check.json`): 356,507 rows fall into exactly one region; one, the Caspian Sea (`XCA`), into none, as intended (water). So the GADM part of the partition has no gaps and no overlaps.

`check_custom.py` (needs shapely and pyproj) intersects every custom geometry with the GADM units under it and reports, in km² in a local equal-area projection, how much land it takes from which region (`release/custom_check.json`). Custom geometries of different regions do not overlap each other. What they take:

- **Intended moves.** Siachen takes 2,085 km² from Gilgit-Baltistan; Halayib 18,013 km² from Sudan; Bhutan's north-western valleys 1,220 km² from Tibet; Kalapani 51 km² from Nepal; the zones, leases and registry cells take their land from the region around them.
- **Slivers from neighbours**, where Natural Earth's 1:10 million line and GADM's line differ: Somaliland takes 747 km² from Ethiopia and 246 km² from Djibouti; South Ossetia 20 km² from Russia; Bir Tawil 85 km² from Sudan; the UNDOF zone 9 km² from Lebanon; Koalou 0.1 km² from Togo.
- **To review: Demchok.** Natural Earth's "Demchok" feature (noted "Admin. by India") is 2,268 km² and lies mostly where GADM has China (1,318 km² from China, 552 km² from Tibet). Whether that whole feature is land India holds is not established.
- **Islets.** Most island polygons lie on no GADM land at all (GADM has no polygon there); they add land rather than take it.
- The two OpenStreetMap relations (Gornja Siga, Socotra) are not fetched yet.

## What is not checked
- Only one perspective (the canon's attribution) is in `regions.csv`; the other declared perspectives are not yet columns.
- No correspondence table: this is the first draft.
- TYR's importer reads only the tree; binding by unit identifiers and own geometry need the importer changes listed in the [output-format proposal](../../docs/proposals/output-format.md).
