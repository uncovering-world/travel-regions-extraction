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

Pending.

## Result

Not run yet.

## Conclusion

Pending.

## Status

Planned: set up 2026-10-03.
