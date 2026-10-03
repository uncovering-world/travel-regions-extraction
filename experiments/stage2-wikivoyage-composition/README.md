# Does Wikivoyage state what its regions are made of?

**Experiment, not the canon.** Issue: [#28](https://github.com/uncovering-world/travel-regions-extraction/issues/28). Follows the [scale survey](../stage2-scale-survey/README.md).

## Question

The scale survey found that Wikivoyage supplies groupings at about the reference scale for most countries where official first-level units are too fine. A grouping is usable for the canon only if it resolves to substrate units without anyone drawing a boundary (consumer-contract C5). For countries of the "groups" class: what share of a country's first-level official units (ISO 3166-2 top tier) is named by exactly one Wikivoyage region — in the region's own name, in the items listed for it on the parent page, or as a sub-region one level down?

No proposal is assumed.

## Related

R040, Q012; consumer-contract proposal C5; TYR #598 (hierarchical matching of Wikivoyage) for the product-side view of the same problem.

## What would change our mind

Written before the first run.

1. If for most test countries at least 90% of first-level units are named by exactly one region, stated composition is a workable resolver and Wikivoyage can be a list source with geometry derived from units.
2. If coverage is mostly between 50% and 90%, composition needs a second resolver (the region map, Wikidata) for the remainder — the cost of that remainder decides whether the source is worth it.
3. If coverage is mostly under 50%, Wikivoyage regions are not defined in terms of official units, and using them means either matching maps or abandoning the source for Stage 2.
4. Units named by more than one region are a separate signal: the regions overlap or cut units, which a partition cannot accept without a rule.

Name matching is approximate (transliteration, "Province" suffixes); the run reports unmatched and ambiguous names so the error can be judged.

## Method

`run.py` (Python ≥ 3.11, standard library), from the repository root:

```bash
python3 experiments/stage2-scale-survey/fetch_wikivoyage.py   # fills the shared wikitext cache
python3 experiments/stage2-wikivoyage-composition/run.py
```

- Test countries: the 19 countries of the scale survey's "groups the top tier" class with at least six reference regions, plus Italy and Germany as controls.
- Wikivoyage draws region maps with `mapshape` templates that list Wikidata ids. A unit counts as assigned to a level-1 region when its id appears in a `mapshape` on that region's page, or in a `mapshape` on the country page titled with the region's name.
- Ids are tied to official units through Wikidata's ISO 3166-2 code (P300), fetched on 2026-10-03 and cached; no name matching is involved, so there are no false matches from spelling, but a unit whose Wikidata item lacks P300 is missed.
- This run did not use the `regionNitems` text or the regions' own Wikidata items; those are other possible resolvers.

## Result

| Coverage of official units by exactly one region | Test countries |
|---|---|
| 90% or more | 7 — Algeria, Iran, Nigeria, Malaysia (all 100%), Thailand (77 of 78), Chile (15 of 16), Ukraine (25 of 27) |
| 50–90% | 3 — Japan (39 of 47), Switzerland (19 of 26), Angola (11 of 18) |
| Under 50% | 9 — Philippines, Papua New Guinea, Turkey, Peru, and zero for Vietnam, Kenya, Colombia, Egypt, Tanzania |

No unit was assigned to more than one region in any country. Controls: Italy 5 of 20, Germany 0 of 16. Per-country rows are in `outputs/coverage.csv`.

The result is bimodal. Where a country's Wikivoyage maps were drawn from unit ids, the composition is complete or nearly so. Where they were drawn from a static image or from one shape per region, this resolver finds nothing.

## Conclusion

Neither outcome 1 nor outcome 3 holds across the board: stated composition through `mapshape` ids is a clean resolver for about a third of the test countries (and never produced an overlap), a partial one for a few, and absent for about half.

So Wikivoyage as a Stage 2 list source needs at least one more resolver before its geometry gap can be judged: the composition recorded on the regions' own Wikidata items, the `regionNitems` lists, or — as a last resort, and at the cost of manual review — the region map images that TYR's importer already reads. Measuring those is the next step; this run sets the baseline they have to beat.

It supports no rule. It does show that "list first, geometry from stated composition, nothing drawn" is achievable today for countries such as Thailand, Algeria, Iran, Nigeria and Malaysia, which makes them good first countries for a Stage 2 prototype.

## Second resolver (added 2026-10-03, before running it)

Question: where the country page draws a region from a single Wikidata id (the region's own item), does that item list official units through "contains the administrative territorial entity" (P150)? What would change our mind: if adding this resolver lifts most of the under-50% countries above 90%, Wikidata composition closes the gap; if it changes little, composition is simply not recorded for those countries and only maps or text remain.

Result (`probe_p150.py`, `outputs/p150.csv`): of 65 level-1 regions drawn from their own Wikidata item, 14 have any P150 statement — all five in Switzerland, three in Thailand, two each in Japan and Papua New Guinea, one each in the Philippines and Chile — and none in Turkey, Vietnam, Colombia, Peru, Tanzania, Angola or Algeria. The resolver changes little: for the countries where `mapshape` composition is absent, Wikidata does not record the composition either. What remains for them is the text of the pages and the map images.

## Third resolver (added 2026-10-03, before running it)

Question: do names help where ids are absent? A unit counts as assigned to a level-1 region when its ISO 3166-2 name matches, after normalisation, a link in the region's `regionNitems` on the country page or the name of one of the region's own sub-regions. What would change our mind: if names lift most under-50% countries above 90%, text composition is the practical resolver (with the usual risk of name collisions, which the run reports as units matched in several regions); if not, only map images remain for those countries.

## Status

Third run planned 2026-10-03.
