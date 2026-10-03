# World Stage 1 draft

**Experiment, not the canon.** Cells here are a draft under proposals that are not adopted. Issue: [#22](https://github.com/uncovering-world/travel-regions-extraction/issues/22).

## Question

How many Stage 1 cells does the world have, and which, if Stage 1 is built as

1. **registry cells** — the coarsest partition that refines ISO 3166-1 and every Natural Earth point-of-view (POV) attribution, and
2. **CR-W splits** inside registry cells, taken at "cited" evidence level from a census of territory-specific entry regimes?

And how does the result move with each open choice: which perspectives are in the registry, and the pending CR-W amendments (transit, rule scope, whole-territory permits)?

Assumed proposals (none adopted): the reference-registry rule ([#19](https://github.com/uncovering-world/travel-regions-extraction/issues/19)); a product profile where a registry cell has no internal boundary without a CR-W witness and evidence is "cited" by default (#22); the CR-W amendments ([#17](https://github.com/uncovering-world/travel-regions-extraction/issues/17)) as parameters. Under the strict `S1-core-v1` none of these cells is certified.

The first run is count-only: a list of cells with their defining units, no geometry.

## Related

R009, R039, R041, R044; R014, D031, Q005 (permits and overlays); R027 (transit); D012 (non-contiguity does not split); D004–D007 (accepted product constraints); Q006, Q011. Consumer-contract proposal: [C2, C5](../../docs/proposals/consumer-contract.md).

## What would change our mind

Written before the first run.

1. **Is the registry enough for D004–D007?** If any accepted constraint is not derived by registry cells, the registry rule as proposed does not close #19 and needs another input or an explicit convention.
2. **Is Natural Earth usable as the perspective source?** If its POV attributes need more than a handful of documented corrections to give sensible cells, the registry needs another source or a curated list — which changes #19.
3. **How much does CR-W add?** If CR-W splits are under 5% of cells, Stage 1 is dominated by the registry, and legal-grade evidence work on CR-W has little effect on the partition; that supports "cited by default". If they are over 25%, evidence quality matters much more than the review assumed.
4. **Which amendment matters?** The amendment whose switch moves the total most should be decided first; if none moves it by more than a few cells, #17 can wait for Stage 2.
5. **Does the draft resemble a known list?** If the draft's cells that are parts of an ISO entry overlap poorly with the TCC entries that are parts of an ISO entry, either CR-W misses what travellers consider separate (work for Stage 2) or the reference list uses other criteria; either way the comparison says what Stage 2 must add. TCC is validation only; nothing is tuned toward it.

## Method

See `run.py` (Python ≥ 3.11, standard library). From the repository root:

```bash
python3 experiments/stage1-world-draft/run.py
```

## Result

Not run yet.

## Conclusion

Pending.

## Status

Planned: set up 2026-10-03.
