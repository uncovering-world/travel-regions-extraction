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

See `run.py` (Python ≥ 3.11, standard library). From the repository root:

```bash
python3 experiments/stage2-scale-survey/run.py
```

## Result

Not run yet.

## Conclusion

Pending.

## Status

Planned: set up 2026-10-03.
