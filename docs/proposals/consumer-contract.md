# Consumer contract — proposal

**Status: proposal, not adopted.** Issue: [#27](https://github.com/uncovering-world/travel-regions-extraction/issues/27). When adopted, each item becomes an R item in [spec.md](../spec.md) through a D entry.

Track Your Regions (TYR) is the consumer of the canon. This page states what TYR needs from it, where each need comes from, and how a draft partition is checked against it. Sources: TYR issues #587, #767–#771 and #1159 (read 2026-10-03), TYR's `docs/tech/world-view-import-format.md` (commit f0acfc077), and the owner's statements in conversation on 2026-10-03.

## Requirements

| # | Requirement | Source | Check on a draft partition |
|---|---|---|---|
| C1 | **One point, one region.** Every point of the declared universe belongs to exactly one region. | Already R003, R004 | No gaps or overlaps (V001) |
| C2 | **One country per region under every supported perspective.** For each perspective in the declared list, every region lies inside exactly one country of that perspective, or inside none (land under no country). | TYR #770 (country marking), #771 (declared views and counting standards) | For each region and perspective, the set of countries it intersects has at most one member |
| C3 | **Regions per country can be read from the canon.** "3 of 17 regions of Spain" needs no second source. | TYR #770 | Follows from C2: group regions by country per perspective |
| C4 | **Every boundary is explained** by a rule and its inputs. | Already R001; TYR #786 ("argue with a source or a threshold, never with a person") | Each boundary carries a rule ID and input references |
| C5 | **Deliverable as a TYR world view through the existing file import.** Each region states its membership explicitly — substrate units or published geometry — and carries a stable identifier and its country per perspective. Where the importer cannot take this, the gap becomes an issue in the TYR repository rather than a workaround here. | Owner, 2026-10-03; TYR #1159, #767 | A release exports to the import format and loads without manual matching |
| C6 | **Not tied to one substrate.** Region definitions do not depend on a single boundary dataset. GADM is allowed, not required; it is known to be weak in places (South Ossetia; the China–India–Pakistan border area). | Owner, 2026-10-03; TYR #769 | Region definitions name the substrate and version they bind to; a region whose substrate lacks the needed unit is reported, not approximated silently |
| C7 | **Stable between releases.** Regions and identifiers do not change without a stated reason, so progress numbers and curator edits survive a re-import. Visits are not at stake: TYR records them as points (TYR #768). | TYR #768, #1159, #594 | A correspondence table between consecutive releases; details in #20 |

## Not requirements

- **Scale.** The owner expects a result of roughly NomadMania's size (about 1,300 regions), but the number must follow from the rules and may differ. It is a reference for validation, not a target.
- **Agreement with the ERP experiment.** Experiential Region Partitioning (TYR #767) is an independent attempt to derive a canon by another method, in its own repository. Its ideas may be used for Stage 2 here; nothing here has to match its output.

## Known gaps in the TYR file import (as of f0acfc077)

The format is a tree of names with optional `sourceUrl`, `wikidataId` and map images. Geometry comes from matching names to GADM divisions, with admin review. For C5 the format lacks: explicit unit membership, region geometry where no unit fits, a stable region identifier and a country marking. These are candidates for TYR issues once the canon's output format is drafted.

## What adoption would change

- C2 is new. It is the requirement the reference-registry rule (#19) would implement.
- C5 and C6 are new and shape the output format of the first drafts (#22).
- C7 replaces the visit-related motivation of R032 with progress and curation stability; the mechanism is decided in #20.
- C1 and C4 are already in the spec; C3 follows from C2.
