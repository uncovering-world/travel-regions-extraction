# Product Stage 1 profile and evidence levels — proposal

**Status: adopted on 2026-10-03 as [D051](../decisions.md#d051--product-profile-no-witness-no-boundary-cited-evidence-enters-a-release) (R057).** Part of issue [#22](https://github.com/uncovering-world/travel-regions-extraction/issues/22).

## Question

`S1-core-v1` (R044) is an open-world definition: one verified witness separates, but two areas are `hard_compatible` only after positive proof that all seven hard dimensions are equal for every traveller context. In the Q001 experiment that proof was reached in 0 of 147 results, and no real certificate exists yet. A partition for Track Your Regions cannot wait for proofs of equality for every pair of places on Earth. What does the product build from?

## Proposal

Keep `S1-core-v1` unchanged as the strict definition, and add a second, named profile for building releases.

**Profile `S1-product-v1` (proposed):**

1. **Closed world inside a registry cell.** Within one cell of the reference registry ([proposal](reference-registry.md)) there is no Stage 1 boundary unless a CR-W witness is recorded. Absence of a witness is treated as no boundary, and the cell is marked `provisional` rather than `hard_compatible`.
2. **Evidence levels.** A witness carries one of:
   - `cited` — an official or otherwise competent source states the rule; locator, publisher and dates recorded; the five gates checked by the preparer, who may be an AI agent. Enough to enter a release.
   - `audited` — the full review of the [evidence-review protocol](../evidence-review/protocol.md) by a named human. Required only where sources conflict, where no primary source can be found, or where the owner asks.
   - `unconfirmed` / `conflicted` — recorded, never enough to split.
3. **Honest labelling.** A release states, per boundary, its rule and evidence level, and per cell whether it is provisional. Nothing built under this profile is presented as certified under `S1-core-v1`.

## Why two profiles rather than weakening the core

The strict core remains the meaning of "must separate": it is what an audit checks against, and its open-world outcomes (`unknown`, `model_unresolved`) stay available for analysis. The product profile is a declared default on top, so the difference between "proved" and "assumed for now" is visible instead of being lost.

## Counterexamples and what the profile does with them

| Case | Strict core | Product profile |
|---|---|---|
| Two provinces of one country, no recorded difference | `separation_not_proven` | One cell, provisional |
| Jeju against mainland South Korea, rule cited from the immigration service | no certificate until audited | Split, evidence `cited` |
| Tibet: a permit described by travel agencies, no legal instrument found | no certificate | No split; recorded as `unconfirmed`, candidate for an audit |
| Kurdistan Region of Iraq: sources conflict on which visa is accepted | `data_unknown` | No split; `conflicted`, candidate for an audit |
| Germany against France | no certificate (`data_unknown` in Q001) | Separate cells through the registry, no CR-W evidence needed |

## What adoption would change

A new R item defining the profile and the evidence levels; R038 gains a note that `S1-product-v1` is a declared closed-world default, not `hard_compatible`; the evidence-review protocol becomes the definition of `audited` only. D032 (CR-W as the core) is untouched.

## Open point

Whether an unconfirmed but widely reported regime (Tibet) should split provisionally. Proposed: no — a boundary needs at least `cited` evidence — because a wrong split is harder to undo for the consumer than a missing one.
