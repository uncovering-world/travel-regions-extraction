# What Track Your Regions' importer needs to load a canon release — draft issues

**Status: proposal, to be raised in the TYR repository by its maintainers; nothing is filed from here (AGENTS.md).** Basis: the release format adopted as D060 (R059) and the [draft release package](../../experiments/release-draft/README.md). Read against TYR's `docs/tech/world-view-import-format.md` and `docs/tech/world-views.md` at commit 77cdbd081.

Today a world view is uploaded as a tree of names with optional `sourceUrl`, `wikidataId`, `regionMapUrl` and `mapImageCandidates`; a matcher (`country-based`, `hierarchical` or `none`) binds leaves to GADM divisions and an admin reviews the rest. The draft release can be loaded that way now, with review. Each item below removes a step that is manual or lossy for a canon release.

## 1. Bind regions by GADM identifiers

- **Need.** The release already knows, for 297 of 314 regions, exactly which GADM 4.1 units make each region, including units to cut out (China minus Hainan, Tibet, Hong Kong and Macau; Ukraine minus Crimea and Sevastopol). Name matching re-derives this and errs: in the binding work three of 30 automatic name matches were wrong (San Andrés matched three municipalities elsewhere).
- **Shape.** A node field listing GADM unit ids to include and to exclude (the release's `membership.csv` rows with `source` = GADM 4.1), and a matching policy, say `explicit`, that binds exactly those and marks the node matched without review.
- **Check on import.** Every GADM row lands in exactly one region (the release ships the same check: 356,507 of 356,508 rows do; the Caspian Sea, water, in none).

## 2. Regions with their own geometry

- **Need.** 42 places have geometry no GADM unit gives: zones, leases, unclaimed land, islets GADM has no polygon for, and land GADM gives to another country than its holder (Siachen, Demchok, Halayib…). The release ships each as a GeoJSON with its source and licence.
- **Shape.** A node field referencing a geometry file in the package, a precedence over GADM units, and a list of regions it may take land from (`clip_to`). On import the geometry is clipped to the GADM units of those regions and wins over them; land GADM lacks (islets) is added as is. One file is a line, not a polygon (a line of control, D066; Siachen): the importer splits the units of the `clip_to` regions by the line and takes the side that contains the file's `holder_point` (PostGIS `ST_Split`).
- **Licences.** OpenStreetMap-derived files are ODbL; the rest are public domain, US government work or CC BY-IGO (listed per file).

## 3. A stable region identifier

- **Need.** A re-import of the next release must update regions in place, so that curator edits and per-region history survive; identifiers never change meaning (R032).
- **Shape.** A node field `externalId` (the release's `region_id`, e.g. `rule/kr-jeju`, `area/crimea`, `JP`), stored on the region and used to match nodes on re-import; the release's correspondence table says which old ids map to new ones.

## 4. The country of a region under a chosen point of view

- **Need.** Counts per country (TYR #770) under the user's chosen point of view (TYR #771). A region never crosses a country boundary under any supported point of view (R045); the release gives, per region, the country under the canon's attribution and under each of Natural Earth's 31 national points of view.
- **Shape.** Load `regions.csv`'s `country_code` and `pov_XX` columns beside the tree, or a node field holding them; the UI picks the column.

## 5. Special places ("border curiosities")

- **Need.** About 90 places are not regions but tickable objects inside a region (line disputes, undelimited stretches, uninhabited islets and claimed rocks, small leases); the owner expects them as a category of their own (D041/R046).
- **Shape.** A list of special places with a point or polygon, the region that holds them and a short reason, imported as objects attached to that region; not counted as regions. The release does not yet ship this list as a file; it is in `experiments/stage1-list/outputs/special_places.csv`.

## Not needed from TYR

The canon decides regions, their countries under each perspective, and their geometry; TYR draws and counts. Nothing above asks TYR to judge a dispute.
