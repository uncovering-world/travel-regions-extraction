# Output format for Track Your Regions — proposal

**Status: adopted as D060 (R059) on 2026-10-04.** It implements requirement C5 of the [consumer contract](consumer-contract.md) and feeds issue [#22](https://github.com/uncovering-world/travel-regions-extraction/issues/22). Read against TYR's `docs/tech/world-view-import-format.md` and `docs/tech/world-views.md` at commit f0acfc077 (2026-10-03).

## What TYR's file import does today

- A world view is uploaded as a JSON tree of nodes: `name` (required), `children`, and optional `sourceUrl`, `wikidataId`, `regionMapUrl`, `mapImageCandidates`.
- Geometry is never in the file. After upload a matcher binds nodes to administrative divisions of the substrate; an admin reviews what it could not bind. Three policies exist: `country-based` (name matching, default for files), `hierarchical` (used by the base-layer mirror; binds 100% when names equal division names) and `none`.
- A region's geometry is then computed from the divisions bound to it.

## What a canon release needs to say

For every region: a stable identifier; a name; its country under each declared perspective; the rule and inputs that define it (C4); and its membership — which substrate units it is made of, or its own geometry where no unit fits (C6: South Ossetia and the China–India–Pakistan border area in GADM).

## Proposed release package

1. **`canon.json`** — the import tree in TYR's existing format, two levels below the root: country (per the default perspective), then region. Loadable today; everything beyond names is carried in the sidecar.
2. **`regions.csv`** — one row per region: `region_id`, `name`, `wikidata_id`, `rule_ids`, `stage1_cell`, and one `country_<perspective>` column per declared perspective.
3. **`membership.csv`** — one row per (region, substrate unit): `region_id`, `substrate` (name and version), `unit_id` in that substrate. A region bound to several substrates has rows for each, so the substrate can be swapped without redefining regions.
4. **`geometry/`** — only for regions that no substrate unit can represent: a published polygon with its source and licence.
5. **`manifest.json`** — release identifier, cutoff date, rule and registry versions, input hashes (R033), and the correspondence table to the previous release (C7).

Rows are sorted and files are deterministic, so two builds from the same inputs are identical.

## Gaps in the importer, as candidate TYR issues

None is filed yet; they are to be raised in the TYR repository once the first release package exists.

| Gap | Why the canon needs it | Possible shape |
|---|---|---|
| Explicit membership | Name matching is the wrong tool when the file already knows the units; a canon import must bind 100% without review. | A node field listing substrate unit identifiers, and a matching policy `explicit` that binds exactly those. |
| Own geometry | Some regions have no unit in the substrate. | A node field referencing a polygon shipped with the file; the import stores it as the region's geometry. |
| Stable region identifier | A re-import must update regions in place so that curator edits survive (TYR #594, #1159). | A node field `externalId`, kept on the region and used to match nodes on re-import. |
| Country marking | Counts per country (TYR #770) under a chosen perspective (TYR #771). | A node field for the country per perspective, or the sidecar table loaded beside the tree. |

Until those exist, a release can still be loaded through the current importer with the `hierarchical` or `country-based` policy and manual review, which is enough for looking at drafts.

## Open points

- Whether the tree should group countries under continents or macro-regions for browsing; the canon itself is single-level (R005), so any such grouping is presentation only.
- Which substrates to bind in the first release: GADM as the owner allows, and one alternative to prove C6.
