# Q001 evaluator run summary

- Evaluator version: `0.2.0`
- Spec version: `0.2.0-draft`
- Dataset snapshot: `2026-09-11`
- Fixtures: 15/15 passed

## Result counts

| Profile | must_separate | hard_compatible | separation_not_proven | model_unresolved | data_unknown | rule_conflict |
|---|---:|---:|---:|---:|---:|---:|
| P1 | 4 | 0 | 41 | 1 | 3 | 0 |
| P2 | 8 | 0 | 1 | 1 | 39 | 0 |
| P3 | 8 | 0 | 0 | 41 | 0 | 0 |

## Certificates and blockers

- P1 sufficient split certificates: C007, C029, C030, C042
- P1 blocked by data: C001, C032, C040
- P1 blocked by model: C013
- P2 sufficient split certificates: C001, C007, C008, C009, C012, C029, C030, C042
- P2 blocked by data: C002, C003, C005, C006, C010, C011, C014, C015, C016, C017, C018, C019, C020, C021, C022, C023, C024, C025, C026, C027, C028, C031, C032, C033, C034, C035, C036, C037, C038, C039, C040, C041, C043, C044, C045, C046, C047, C048, C049
- P2 blocked by model: C013
- P3 sufficient split certificates: C001, C007, C008, C009, C012, C029, C030, C042
- P3 blocked by data: C002, C003, C005, C006, C010, C011, C014, C015, C016, C017, C018, C019, C020, C021, C022, C023, C024, C025, C026, C027, C028, C031, C032, C033, C034, C035, C036, C037, C038, C039, C040, C041, C043, C044, C045, C046, C047, C048, C049
- P3 blocked by model: C002, C003, C004, C005, C006, C010, C011, C013, C014, C015, C016, C017, C018, C019, C020, C021, C022, C023, C024, C025, C026, C027, C028, C031, C032, C033, C034, C035, C036, C037, C038, C039, C040, C041, C043, C044, C045, C046, C047, C048, C049
- `hard_compatible` produced: no

## Representative classification comparison

No representative classification mismatches were found; documented results and typed blockers agree with executable evaluator semantics.

The evaluator emits Stage 1 pairwise outcomes only. `hard_compatible` does not assign a final canonical region, and this artifact contains no canonical region assignments.
