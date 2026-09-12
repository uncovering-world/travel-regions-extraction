# Reference evaluator implementation notes

This document distinguishes the current normative `S1-core-v1` evaluator from the historical Q001 engine. Neither builds geometry, assigns canonical regions or implements Stage 2.

## Current normative evaluator

`core.evaluate_core` and CLI `evaluate-core --input PATH` implement the CR-W-only profile, spec `0.3.0-draft`, evaluator version `s1-core-1.0.0`. The input contract is in [stage1-core-adoption.md](../experiments/q001/stage1-core-adoption.md). Every accepted certificate must pass all five R044 gates with verified, applicable, temporally valid evidence, both decisions and relevant exceptions. No frequency filter, jurisdiction separator, identity dimension or label-derived boundary exists in this path.

Gate records are externally grounded normalized proof attestations. The evaluator checks their state, provenance and applicability envelope; it does not infer truth from a URL, interpret natural-language laws, verify source contents or prove geometry from scope IDs. A producer must justify every gate conjunct, including nonempty/disjoint/homogeneous scopes, class coherence, route matching, exceptions and territorial/standing classification. Missing proof remains unknown. The checked-in example is synthetic and asserts no geographic fact.

Core completeness requires separately evidenced full coverage and equal normalized hard functions for all seven accepted dimensions, at one scope/time. It never consumes historical synthetic completeness tokens or requires CR-J/identity. A verified certificate takes precedence over unrelated unknowns; a contradicting positive full-equality proof creates a data/source conflict requiring resolution. Output goes to stdout and cannot rewrite historical result files. The public historical `Profile` enum deliberately remains exactly P1/P2/P3; core identification is separate.

## Historical engine

Version 0.2.0 implements the historical Q001 pairwise contract for spec 0.2.0-draft. Its serialization version and profile definitions remain pinned for reproduction; the paragraphs below describe that historical behavior, not current production adoption.

## Contract mapping

The package uses immutable dataclasses for factual unit references, dimensions, evidence, witnesses, blockers, derivations, comparisons, signature assessments, and outputs. `Profile`, `DimensionState`, and `EvaluatorResult` are string enums. Three-valued signature equality has a separate enum so an incomplete comparison cannot collapse to Boolean false.

P1 has the four required base dimensions named by the contract: admission-decision scope, visa scope, document scope, and relevant hard permits. The synthetic DSL may explicitly add the route-dependent hard-decision dimension. P2 adds final admission jurisdiction. P3 adds the unresolved identity discriminator.

Terminal outcomes follow the contract order: normative rule conflict, sufficient split certificate, model blocker, data blocker, complete equal signature, and finally separation not proven. Output sets are deduplicated and sorted. Explanations use stable IDs and rule concepts; factual-unit display names are not present in the evaluation model.

## Q001 adapter

The adapter parses the JSON-syntax `.yaml` files with the standard library. It preserves literal booleans, `"unknown"`, null/missing values, evidence status, and unresolved model questions.

A Q001 regime witness is accepted only when its structured status is `verified`, its decisions differ, its dimension is a hard territorial dimension, and every referenced evidence record is verified. A structured `independent_admission_jurisdiction: true` assertion is accepted for P2/P3 only when the linked admission evidence extracted from the two factual units is present and verified. Local offices, issuer descriptions, control records, and political labels are not converted into jurisdiction certificates.

The current factual schema contains sampled facts but no whole-signature completeness attestations. The adapter therefore keeps real Q001 signatures incomplete and produces no `hard_compatible` result. It does not derive completeness from prose, names, or a finite set of examples.

`hard_compatible` is the positive Stage 1 compatibility outcome. It does not assign endpoints to one final canonical region because Stage 2 may subdivide any Stage 1 cell. The public predicate, enum member, fixtures, and generated output use the new term. The fixture-input parser temporarily accepts `may_merge` as an alias for a rule derivation to read pre-0.2 synthetic input; it never emits that spelling.

Comparison-level missing facts affect terminal semantics only through `evaluator_data_blockers`. Each entry supplies a stable ID, a typed kind, explicit profile applicability, and optional evidence references. The legacy `blocked_by` strings remain diagnostic prose and are never parsed by the adapter. This distinction allows an incomplete equivalence explanation to remain `separation_not_proven` while a concrete typed missing fact produces `data_unknown`.

P3 adds `Q001.identity` after no P1/P2 split is found. It also adds Q006 only when the comparison's structured `model_questions` includes Q006. Q004 is retained as a P1/P2/P3 model blocker for the supplied customs/fiscal comparison. Q005 and Q009 are not automatically blockers because the contract's representative cases show that merely listing those questions does not establish that the outcome depends on them.

P3's identity discriminator concerns unresolved territorial/legal identity. It does not represent Stage 2 destination identity.

## Determinism and generated artifacts

Comparisons, profiles, rule IDs, witnesses, blockers, and evidence references are sorted before serialization. The generated JSON includes 147 results when all three profiles run. Its aggregate factual-input hash is SHA-256 over each sorted relative filename, a zero byte, and that file's binary SHA-256 digest. The hash covers `facts/*.json`, `evidence.json`, `sources.json`, `source-index.md`, `route-matrix.json`, and `comparisons.yaml`.

## Representative alignment

C001/P1 is documented as `data_unknown`. Its candidate witness and E01 are provisional, so fixture F013 and outcome precedence identify `E01.status` as a concrete verification blocker. The evaluator precedence is unchanged.

C032 and C040 now carry explicit `evaluator_data_blockers` for the missing facts already documented in the snapshot. The adapter consumes these records without comparison-specific logic. Representative result and blocker checks are generated from the contract and currently report no mismatches.
