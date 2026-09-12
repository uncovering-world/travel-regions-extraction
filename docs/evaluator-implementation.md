# Reference evaluator implementation notes

Version 0.1.1 implements the pairwise contract for spec 0.1.1-draft. It does not build geometry, assign canonical regions, or select a profile.

## Contract mapping

The package uses immutable dataclasses for factual unit references, dimensions, evidence, witnesses, blockers, derivations, comparisons, signature assessments, and outputs. `Profile`, `DimensionState`, and `EvaluatorResult` are string enums. Three-valued signature equality has a separate enum so an incomplete comparison cannot collapse to Boolean false.

P1 has the four required base dimensions named by the contract: admission-decision scope, visa scope, document scope, and relevant hard permits. The synthetic DSL may explicitly add the route-dependent hard-decision dimension. P2 adds final admission jurisdiction. P3 adds the unresolved identity discriminator.

Terminal outcomes follow the contract order: normative rule conflict, sufficient split certificate, model blocker, data blocker, complete equal signature, and finally separation not proven. Output sets are deduplicated and sorted. Explanations use stable IDs and rule concepts; factual-unit display names are not present in the evaluation model.

## Q001 adapter

The adapter parses the JSON-syntax `.yaml` files with the standard library. It preserves literal booleans, `"unknown"`, null/missing values, evidence status, and unresolved model questions.

A Q001 regime witness is accepted only when its structured status is `verified`, its decisions differ, its dimension is a hard territorial dimension, and every referenced evidence record is verified. A structured `independent_admission_jurisdiction: true` assertion is accepted for P2/P3 only when the linked admission evidence extracted from the two factual units is present and verified. Local offices, issuer descriptions, control records, and political labels are not converted into jurisdiction certificates.

The current factual schema contains sampled facts but no whole-signature completeness attestations. The adapter therefore keeps real Q001 signatures incomplete and produces no `may_merge` result. It does not derive completeness from prose, names, or a finite set of examples.

Comparison-level missing facts affect terminal semantics only through `evaluator_data_blockers`. Each entry supplies a stable ID, a typed kind, explicit profile applicability, and optional evidence references. The legacy `blocked_by` strings remain diagnostic prose and are never parsed by the adapter. This distinction allows an incomplete equivalence explanation to remain `separation_not_proven` while a concrete typed missing fact produces `data_unknown`.

P3 adds `Q001.identity` after no P1/P2 split is found. It also adds Q006 only when the comparison's structured `model_questions` includes Q006. Q004 is retained as a P1/P2/P3 model blocker for the supplied customs/fiscal comparison. Q005 and Q009 are not automatically blockers because the contract's representative cases show that merely listing those questions does not establish that the outcome depends on them.

## Determinism and generated artifacts

Comparisons, profiles, rule IDs, witnesses, blockers, and evidence references are sorted before serialization. The generated JSON includes 147 results when all three profiles run. Its aggregate factual-input hash is SHA-256 over each sorted relative filename, a zero byte, and that file's binary SHA-256 digest. The hash covers `facts/*.json`, `evidence.json`, `sources.json`, `source-index.md`, `route-matrix.json`, and `comparisons.yaml`.

## Representative alignment

C001/P1 is documented as `data_unknown`. Its candidate witness and E01 are provisional, so fixture F013 and outcome precedence identify `E01.status` as a concrete verification blocker. The evaluator precedence is unchanged.

C032 and C040 now carry explicit `evaluator_data_blockers` for the missing facts already documented in the snapshot. The adapter consumes these records without comparison-specific logic. Representative result and blocker checks are generated from the contract and currently report no mismatches.
