# Stage 1 CR-W core adoption

Decision date: 2026-09-12. Normative spec: `0.3.0-draft`. Decisions: D032–D037. Rule: R044. Current production profile: **`S1-core-v1`**, version `1`. This record applies the user's explicit normative decision after the [historical review](stage1-rule-review.md); it does not rewrite that review's recommendation to consider W OR J.

## Adoption outcome

```text
Current Stage 1 mandatory separator set = {CR-W}

exists C in civilian-short-stay-v1, d in accepted hard dimensions:
    G-SCOPE AND G-CONTEXT AND G-HARD AND G-TIME AND G-EVIDENCE
    AND proven(HardTravelDecision_d(A,C,t) != HardTravelDecision_d(B,C,t))
```

A verified CR-W certificate is sufficient for `must_separate`. One valid class-based witness is sufficient regardless of frequency. No frequency threshold is introduced. Absence of a certificate is not `hard_compatible`; positive complete equality across all **accepted** hard dimensions is required.

| Item | Current status |
|---|---|
| CR-W | Accepted production core, subject to all five gates in [spec R044](../../docs/spec.md#r044--cr-w-proven-hard-territorial-traveldecision-discontinuity-accepted-d032). |
| CR-J | **Well-defined normative candidate; not adopted.** Full J1–J6 retained verbatim in [review §4.2](stage1-rule-review.md#42-operational-definition-independent_final_admission_jurisdiction) and `jurisdiction_definition` in [candidate YAML](stage1-rule-candidates.yaml). |
| Undefined territorial/legal identity | Alone is not an accepted Stage 1 hard separator; excluded from production and production-candidate hard semantics. |
| P1/P2/P3 | Historical non-production experiment profiles. Old results are not new core results. |
| P3 specifically | Model-unresolved wherever outcome depends on identity; existing sufficient historical P1/P2 splits are preserved. Not the Stage 2 destination model. |
| Labels | Dispute, claim, recognition, controller, military control, dependency, autonomy, overseas and island labels are independently insufficient. Proved actual hard territorial travel consequences may contribute to CR-W evidence. |

CR-J could create a mandatory boundary while current hard decision functions are equal. That is a separate normative choice about institutional responsibility, not a demonstrated current travel discontinuity. This patch neither adopts CR-J nor weakens its six premises. Historical candidate recommendations and synthetic NX predictions using W OR J are not the adopted production rule set. In particular, a coherent complete-equal-D/different-J input does **not** split in the current core solely because J differs.

## Product constraints and residual questions

D004–D007 retain their accepted status. An **accepted product regression constraint** is not automatically a **currently derivable Stage 1 rule**.

| Constraint | What CR-W currently establishes or fails to guarantee |
|---|---|
| D005 Réunion / metropolitan France | A general visa/document mechanism is available, but C018 lacks a completed verified traveller witness; no new certificate is asserted here. |
| D004 British Overseas Territories | A blanket category guarantee does not follow from CR-W. Historical P2 C012 is not a CR-W certificate. Current facts may support individual future gate audits; the class label is insufficient. |
| D006 Crimea / ordinary Ukraine | Operational admission/legal-access differences could support CR-W; Crimea has no factual dossier in the 49-case Q001 dataset. The stronger comparison to ordinary Russia is tentative D013, not accepted D006. |
| D007 Western Sahara / ordinary Morocco | C031 west/Morocco has no completed CR-W. Internal west/east control differences do not prove separation from ordinary Morocco. At complete hard-D equality the status-preservation requirement remains a normative conflict with a CR-W-only boundary guarantee. |

No constraint is deleted, downgraded, encoded as an exception, fulfilled merely by an overlay, or assumed solved by Stage 2. Lack of a certificate does not prove that a constraint is factually impossible; it leaves the guarantee unresolved. Q001 is narrowed and resolved for regime-based separation, with CR-J adoption still an explicit normative question. Q002 traveller scope, Q004 customs/biosecurity, Q005 permits/overlays, Q006 legal-status preservation, Q007 control structures, Q008 temporal stability, Q009 spatial dependency and Q011 category/product guarantees remain open in their residual scope. Q003/Q010/Q012 are also unaffected.

## Evaluator paths and reproducibility

| Path | Rules and version | Input and outputs |
|---|---|---|
| Historical `evaluate`, `evaluate-all`, `validate-fixtures` | P1/P2/P3, profile `q001-0.2.0`, contract/spec `0.2.0-draft`, historical engine serialization `0.2.0`. | Existing factual bundle, witnesses, fixtures and 147 results retain their meanings. The historical `Profile` enum is unchanged. |
| Current `evaluate-core --input PATH` | `S1-core-v1`, version `1`, evaluator `s1-core-1.0.0`, spec `0.3.0-draft`. | Explicit normalized CR-W proofs in schema `s1-core-input-v1`; separately versioned JSON emitted only to stdout. No writes to `results/`. |

The former P1 witness schema cannot prove all new scope/context/time/evidence gates. No adapter silently promotes existing `verified` witnesses to current core certificates. The production input is a proof interface, not a new geographic dataset or a claim that all real cases have been audited. Normative core acceptance does not imply a complete production world partition.

```bash
PYTHONPATH=src python3 -m ctr_evaluator evaluate-core --input experiments/q001/stage1-core-example.json
```

The checked-in example is explicitly **synthetic**, with stipulated proofs and no geographic claims. It is also the base pytest fixture for the core's adversarial variations. For real use the producer must provide source-grounded normalized proofs. The evaluator does not research law, read source contents, validate geometry from IDs, or automatically establish the legal truth of a gate assertion. Provenance must refer to reproducible source versions/snapshots, not merely an unversioned URL.

## Current proof input contract

Required top-level fields: `schema_version: s1-core-input-v1`, `profile: S1-core-v1`, `traveller_scope: civilian-short-stay-v1`, nonempty `comparison_id`, ISO `as_of`, and `scopes: {a: scope_id, b: scope_id}`. The two scope IDs must differ; actual nonemptiness, disjointness and homogeneous effects require G-SCOPE evidence. `certificates`, `evidence`, `signatures` and descriptive `metadata` may be absent; absence never means an equality proof. Labels and Stage 2 suggestions in metadata are ignored.

Each certificate contains:

- Unique `id`, `status: verified`, a `dimension` from the accepted hard list, and `scope_a`, `scope_b`, `as_of`, `traveller_scope` matching the bundle.
- `rule_kind: standing_class_rule | constitutive_rule`. Explicit incident/emergency/event/named-individual rules cannot split. An unknown kind blocks certification. Standing classification has no age threshold; validity intervals are still checked.
- `context` with a nonempty `id`, `purpose: civilian_short_stay`, `class_basis: class_rule`, nonempty `trip_class` and an `attributes` object. Attributes must contain every decision-relevant document, residence, authorisation, history, duration and route predicate; the exact set follows the applicable norms. G-CONTEXT attests coherence/nonemptiness, matched logical trip, full relevant attributes and exceptions. Incompatible combinations, raw coordinate differences, out-of-scope purposes or individually named permissions are not qualifying contexts. Denial on one side is a valid decision; no actual successful trip is required.
- All five named `gates`, each `{state, evidence_refs}`. `proven_true` means **all conjuncts of that R044 gate** have source-grounded proof; it is not an unchecked short-hand for territorial importance. `proven_false` rejects the candidate as sufficient when evidenced; missing/`unknown` creates a data blocker; `model_unresolved` creates a model blocker. Missing evidence for either true or false remains unknown.
- `decision_a` and `decision_b`, each `{state, value?, evidence_refs, rationale?}`. States are `known_value`, `known_absence`, `not_applicable`, `unknown`, `unresolved_model_semantics`. `known_value` requires a concrete normalized semantic value; null/empty/unknown components are not decision values. `known_absence` requires positive evidence. `not_applicable` requires a rule rationale and evidence. Both sides must be proved and differ. Output names, IDs and random discretionary outcomes are not semantic differences by themselves.

Accepted dimensions, fixed by R044 and `core.HARD_DIMENSIONS`:

```text
accepted_travel_document
visa_eta_admission_authorisation_requirement
territorial_authorisation_validity
entry_eligibility_or_prohibition
civilian_stay_conditions_duration_or_termination
permission_to_enter_or_be_present_in_territorial_scope
independently_applicable_legal_entry_or_exit_route_obligation
```

`G-HARD` attests territorial legal effect, including independently established applicability rather than bare claims. Site/activity/facility/logistics differences do not qualify even with a permit or whole-province overlay geometry. Ambiguous territorial-presence/overlay classification remains Q005/Q009; accepted dimension **naming alone** does not pass the gate. Customs/biosecurity is not silently added to the hard list.

`evidence` is a mapping from reference IDs to records with `status: verified`, nonempty `source_ref`, `locator`, `source_competence`, `valid_from`, optional `valid_to`, exact `traveller_scope`, and arrays `scopes` and `contexts`. Every cited record must be verified and applicable at `valid_from <= t < valid_to` (null upper bound is open). Records must match the context or declare full `contexts: [all]`; their territorial coverage collectively supports each required scope. Each reference must have relevant scope/context applicability; missing/provisional/conflicted/unknown records cannot certify a gate. Separate sources can support the two sides. Observation/retrieval dates do not replace effective dates. Additional proof/excerpt/observation metadata may be retained by the producer, but must not substitute for these fields.

Evidence content, source competence, gate entailment and semantic normalization remain auditable upstream responsibilities. Passing the schema check is not independent verification of law or geography. A single statement about an office or claim cannot honestly attest a stronger territorial decision merely because all record fields were filled.

## Positive compatibility contract

Optional `signatures.a` / `signatures.b` each contain `coverage: {state, evidence_refs}` and `dimensions: {dimension: decision_record}` for **every** accepted hard dimension. The evidence for coverage and dimension normal forms must cover all contexts in S (`contexts: [all]`) for the corresponding scope at t, including all relevant exceptions and hard-scope/time applicability. Coverage attests completeness of those full functions, not coverage of a finite example list. A symbolic common policy expression can prove equality only when its complete common applicability is proved; arbitrary equal tokens are not evidence.

Normalized values are compared deterministically as typed JSON (object key order ignored; array order is semantic and must be normalized upstream). `known_absence` and `not_applicable` are distinct states; N/A rationale participates in equality. CR-J, identity, controllers and unadopted dimensions do not participate, even if supplied alongside accepted dimensions. No historical synthetic completeness token is consumed by this path.

Outcomes follow positive-proof discipline: sufficient CR-W → `must_separate`; otherwise consequential undefined gate/dimension → `model_unresolved`; concrete missing/conflicted proof → `data_unknown`; complete positive equal signatures → `hard_compatible`; otherwise → `separation_not_proven`. An accepted certificate survives unrelated unknowns. A positive full-equality proof contradicting a positive certificate is a data/source conflict, returned as `data_unknown` with `certificate_signature.source_conflict`, and must be reconciled before use. The core has no API for injecting arbitrary rule derivations or product constraints as certificates. Invalid schema/version/duplicate certificate IDs yield input errors.

Output includes profile/spec/evaluator versions, traveller scope, as-of, comparison ID, result, applied rule IDs, accepted witness IDs, signature assessments, data/model blockers, evidence references and rejected certificate diagnostics. Arrays are deterministic. No canonical region assignments, Stage 2 inputs, world partition or curated exception tables are produced.

## Validation scope

Run the full pytest suite, historical Q001 validator and historical fixture validation. The new pytest fixtures exercise all five gates, one rare witness, provisional/conflicted/missing sources, both decisions, site/activity/logistics exclusions, claims/control/jurisdiction labels, positive coverage, name/order/swap invariance, time/scope matching, and Stage 2 irrelevance. Deterministic checks compare rebuilt historical objects against the checked-in 147-result artifact without rewriting it and compare repeat core outputs. Package checksum verification covers updated documentation and the new adoption/example artifacts. Factual inputs, sources, comparisons, witness records, existing fixtures and historical result files remain unchanged.
