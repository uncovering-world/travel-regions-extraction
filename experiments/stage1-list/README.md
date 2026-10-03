# Stage 1 as a list, under the rules decided on 2026-10-03

**Experiment, not the canon.** Issues: [#22](https://github.com/uncovering-world/travel-regions-extraction/issues/22), [#19](https://github.com/uncovering-world/travel-regions-extraction/issues/19), [#17](https://github.com/uncovering-world/travel-regions-extraction/issues/17).

## Question

The owner's decisions of 2026-10-03 (recorded in [docs/status.md](../../docs/status.md), not yet in the spec) give every kind of disputed or special-status area a treatment and narrow which entry rules make a region. Applied to the data already in the repository, without geometry:

1. Which regions, special places and markers result, and how many of each?
2. For which places can the rules not be applied because a fact is missing, and which fact?

Assumes those decisions as the rule set, and the product profile "no witness, no boundary" with evidence level "cited". No geometry and no binding to a substrate; the list is a draft.

## Related

R044; D004–D007; the [first world draft](../stage1-world-draft/README.md), whose registry cells and census of entry rules are inputs; the [register of disputed areas](../../data/disputed-areas/README.md); the [settling rule](../../docs/proposals/settling-rule.md).

## What would change our mind

Written before the first run.

1. If most places of the kinds that depend on a register fact (residents, who holds the area, a recorded entry rule) cannot be decided, the next step is collecting those facts, not geometry.
2. If the count of regions moves far from the first draft's 304 in either direction, the decided rules behave differently from what was assumed when they were chosen, and the cases behind the difference go back to the owner.
3. If accepted product constraints D004–D007 do not come out of the rules, a rule is missing.
4. If many registry cells cannot be tied to a register area, or the reverse, the two lists describe the world differently and need to be reconciled before a release.

## Method

```bash
python3 experiments/stage1-list/run.py
```

`run.py` reads the 249 ISO entries and 29 registry cells of the first world draft (Natural Earth points of view, areas of 100 km² and more), its census of 116 entry rules, and the register's 210 areas, and applies the decided treatment per kind. `inputs/links.csv` ties 34 register areas to an ISO entry, a registry cell or a census row, each with the basis of the tie; the ties were made by name and by the registry's own notes, not from a source, and are the weakest input. Where a rule needs a fact the data does not hold, the place gets the cautious outcome and a row in `outputs/gaps.csv`.

Not applied, because the facts are missing everywhere: the settling rule's attribution (who holds an area and since when), and the two-part test for entry rules (a top-level unit, or a detached place with a rule of its own). Places that depend on them are listed as regions with an open point.

## Result

| | Count |
|---|---|
| Regions | 322 |
| — ISO 3166-1 entries | 249 |
| — from an entry rule (candidates) | 42 |
| — registry cells where points of view differ | 16 |
| — residents test (islets, paper claims, zones with no single holder) | 12 |
| — unclaimed land | 3 |
| Regions with nothing open | 258 |
| Special places | 95 |
| Markers | 141 |
| Missing facts | 193 |

Missing facts, by what is missing: a tie from a paper claim to a registry cell, or confirmation that no supported point of view shows it (38); whether a unit with its own entry rule is top-level (29); who holds a contested area and since when, any act ending the contest, its UCDP conflict (28); for areas held by another party, a stated outline or entry rule, or confirmation that the line still moves (19); entry rules not confirmed in force (18) or without a start date (15); whether a leased area has its own entry rule (10); whether an island's rule is its own (10); whether civilians live there (9); registry cells with no register area (7); entry rules with no cited source (6); areas with no kind (3).

## Conclusion

A draft list, not a canon.

1. *Facts first.* Of 73 regions that do not come from an ISO entry, 64 have an open point. The next step is collecting the named facts, not geometry.
2. *Count.* 322 against the first draft's 304; the difference is not meaningful while 42 entry-rule regions are candidates that the two-part test has not been applied to.
3. *Accepted constraints.* D004 and D005 hold through ISO entries, D006 through the registry cell for Crimea, D007 through the ISO entry for Western Sahara and the registry cell for the part Morocco administers.
4. *The two lists do not line up yet.* Only 34 of 210 register areas are tied to anything, and 7 of 29 registry cells have no register area. They have to be reconciled before a release.

## Second run, 2026-10-03: with the facts the first run asked for

Two collections were added the same day, each fact with a quoted passage: who holds 29 contested areas and since when (now in the register, passages re-opened and found), and what the texts of 43 entry rules say (`inputs/entry_rule_facts.csv`; the collectors' own check found every passage, they were **not re-opened here**).

| | First run | Second run |
|---|---|---|
| Regions | 322 | 315 |
| — from an entry rule | 42 | 34 |
| Regions with nothing open | 258 | 279 |
| Special places | 95 | 94 |
| Missing facts | 193 | 127 |

- Entry rules that no longer make a region: places that are neither a top-level unit nor a detached place with a rule of its own (Kish, Qeshm, Matsu, the Chittagong Hill Tracts), and rules found not in force (Rason, north-east Syria, Russia's former regional e-visas).
- Five contested areas are recorded with a moving line (the four occupied Ukrainian oblasts and Israeli-held southern Syria): no region, a flag on the regions they touch.
- Still open: ties from paper claims to the registry (38); the UCDP conflict for each contested area, without which quiet years cannot be counted (27); start dates of entry rules (11); entry rules of leased areas (10); residents (9); registry cells with no register area (7).

Points the rules do not settle and that go back to the owner:

- Rules for residents of a neighbouring area only (the Chukotka–Alaska arrangement, the Ceuta and Melilla exemption for two Moroccan provinces) pass the test as written, although they are not rules for a visitor in general.
- The Chukotka permit is reported to cover designated districts, not the whole okrug, while the unit is top-level.
- Socotra's rule is reported to work through organised tours only; Zanzibar's own immigration check was not found in a source, only its insurance.

## Status

Concluded 2026-10-03 (two runs).
