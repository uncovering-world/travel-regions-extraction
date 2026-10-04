# Status

Updated: 2026-10-04.

## Focus

A first Stage 1 release of the canon for Track Your Regions. The rules for Stage 1 are decided (D038–D069 in [decisions.md](decisions.md), R045–R059 in [spec.md](spec.md)); the [draft release package](../experiments/release-draft/README.md) is built from them and can be inspected on a local map ([tools/map-viewer](../tools/map-viewer/)). Stage 2 comes after the first release (#28).

## Decided on 2026-10-03 and 2026-10-04

Reference registry and points of view (D038, D039, D064–D069): every country's point of view is built from its sourced claims, Natural Earth is only a lead (#19). Disputed areas by kind and the settling rule (D040–D048, D053–D058, D063). Outlines from stated lines, ranked sources, lines of control (D042, D056, D059, D061, D062, D066). Releases and their format (D049, D060). CR-W amendments and the product profile (D050, D051).

## Waiting for the owner

- Whether a claim like Olivenza's (the claimant does not contest control) should make a region or a curiosity — raised by the owner, not yet discussed.
- The open questions that remain: Q015 (one rule over several units), Q016 (islet groups held in parts), Q018 (how special places are carried and attributed), Q019 (release mechanics), Q020 (unchecked Natural Earth differences; the outline of a claim without a line), Q013 (pinning and versioning of geometries).

## Active

- [Release draft](../experiments/release-draft/README.md) (#22): 331 regions with `view_<party>` columns, membership in GADM units, 54 own geometries, manifest; every GADM unit in exactly one region. Open items: Migingo (holder unclear), the Okpara villages (which villages, see the register's [review list](../data/disputed-areas/REVIEW.md)), Hans Island (the 2022 line is transcribed in the review list; whether the agreement is in force is not confirmed), small plots of the Baikonur lease far from the cosmodrome, whether the Philippine law of 2009 kept the Sabah claim.
- [Stage 1 as a list](../experiments/stage1-list/README.md) (#22): rerun under D064–D069; `outputs/natural_earth_lead.csv` lists where Natural Earth and the recorded claims disagree.
- Long term: a canon for every year from 2000 ([#30](https://github.com/uncovering-world/travel-regions-extraction/issues/30)).

## Next step

Close the release draft's open items above, then cut a first release candidate and raise the [importer needs](proposals/tyr-importer-needs.md) with TYR.
