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

## What is not checked

- The custom geometries are not intersected with GADM: that a Natural Earth polygon cuts the right land out of the right GADM units, and leaves no sliver, needs a geometry engine and is the next check.
- Only one perspective (the canon's attribution) is in `regions.csv`; the other declared perspectives are not yet columns.
- No correspondence table: this is the first draft.
- TYR's importer reads only the tree; binding by unit identifiers and own geometry need the importer changes listed in the [output-format proposal](../../docs/proposals/output-format.md).
