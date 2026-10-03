# Stage 2 scale survey

**Experiment, not the canon.** Issue: [#28](https://github.com/uncovering-world/travel-regions-extraction/issues/28).

## Question

The owner expects the canon to come out at roughly NomadMania's scale (about 1,300 regions), with the number following from rules. Before designing Stage 2: how does that reference scale relate to official administrative units? For each country, compare the number of NomadMania regions with the number of ISO 3166-2 subdivisions at the top tier and at all tiers.

No proposal is assumed. NomadMania is used as a reference for scale only, never as input to rules.

## Related

R040, Q012 (Stage 2 is unspecified); consumer-contract proposal (scale is not a requirement); review problem P5.

## What would change our mind

Written before the first run.

1. If, for most countries with more than one NomadMania region, the NomadMania count is within a factor of 1.5 of an official tier, Stage 2 can be mostly "choose an official tier per country" plus bounded exceptions.
2. If the counts mostly sit between or below tiers (far fewer regions than top-tier units, as with Thailand's 77 provinces), Stage 2 needs a rule that **groups** official units — and the grouping source becomes the central design question.
3. If many countries have more reference regions than top-tier units, Stage 2 also needs a rule that **descends** below the top tier.
4. If the top-tier total for the world is close to the reference total while per-country counts disagree, a matching world count is not evidence that a rule works.

## Method

`run.py` (Python ≥ 3.11, standard library) reads two committed inputs and classifies each country by where its reference count sits relative to the official tiers (within a factor of 1.5 = "matches"). From the repository root:

```bash
python3 experiments/stage2-scale-survey/run.py
```

Inputs:

- `inputs/nomadmania-counts.csv` — regions per country, 1,381 in total: the 1,301-region list from NomadMania's public `static/json/regions_en.json` (last modified 2025-03-31) plus the 80 regions added in the "Great Regions Review" post of 12 May 2026; retrieved 2026-10-03. Countries are NomadMania's; the ISO mapping is ours. Nine entries without an ISO 3166-1 entry (de facto states, the poles, 11 regions) are left out. Only counts are stored, not the list.
- `inputs/iso3166-2.csv` — code, type and parent of each ISO 3166-2 subdivision, from Debian `iso-codes` 4.20.1 (a mirror of the standard), read 2026-10-03. "Top tier" = subdivisions without a parent.

## Result

204 countries, 1,370 reference regions; the same countries have 3,572 top-tier ISO 3166-2 units (5,046 at all tiers worldwide).

| Relation of the reference count to official tiers | Countries | Reference regions |
|---|---|---|
| Single region | 21 | 21 |
| Matches the top tier | 31 | 512 |
| Groups the top tier (fewer regions than units) | 142 | 629 |
| Between tiers | 2 | 57 |
| Descends below the top tier (more regions than units) | 4 | 138 |
| No official units | 4 | 13 |

- Of the 183 countries with more than one reference region, 17% match an official tier.
- The matches are mostly large federations: Russia 90 vs 83, United States 77 vs 57, India 48 vs 36, Brazil 37 vs 27, Germany 20 vs 16, Italy 21 vs 20, Spain 22 vs 19, Argentina 25 vs 24.
- Grouping dominates everywhere else: Thailand 10 vs 78, Turkey 14 vs 81, Vietnam 9 vs 63, Japan 17 vs 47, Kenya 7 vs 47, Algeria 9 vs 58.
- Descent is rare but large: China 75 vs 34, Canada 27 vs 13, Australia 25 vs 8, Pakistan 11 vs 7. The United Kingdom (34 vs 4 or 221) and Indonesia (23 vs 7 or 45) sit between tiers.

Per-country rows are in `outputs/countries.csv`.

## Conclusion

Outcome 2 of "what would change our mind", with outcome 3 as a minority case:

- **"Choose an official tier" covers about a third of the reference scale** (512 of 1,370 regions, 31 countries) — the large federations whose first-level units are identities in their own right.
- **For three quarters of countries the reference scale is reached only by grouping first-level units** (142 countries, 629 regions). Taking first-level units everywhere would give about 3,600 regions, 2.6 times the reference. So the central design question of Stage 2 is the source and rule of grouping: official groupings above the first level where they exist (statistical regions, NUTS-like tiers), a published travel hierarchy, or a threshold rule that merges units.
- **A descending rule is needed for a handful of very large units** (China, Canada, Australia, Pakistan; 138 regions).
- The world totals do not validate anything by themselves: per-country agreement is what has to be measured.

This supports no rule yet. It says where Stage 2 experiments should go next: test grouping sources on countries of the "groups" class, and keep one federation and one "descends" country as controls.

## Status

Concluded 2026-10-03.
