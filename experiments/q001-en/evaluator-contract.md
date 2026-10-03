# Experiment Q001 — evaluator contract

Historical non-production contract for P1/P2/P3. Its algorithms, fixture semantics and recorded results remain pinned to `0.2.0-draft`; references to R011/R010 below describe that historical spec. Current production uses only CR-W in `S1-core-v1`, with a separate [adoption and input contract](stage1-core-adoption.md). P3 remains model-unresolved where identity matters and is not the Stage 2 destination model. No historical P1 result is automatically a current CR-W certificate.

Status: implementation-ready Stage 1 contract for `spec.md` 0.2.0-draft and the factual snapshot 2026-09-11. The contract does not choose between P1/P2/P3 and does not assign canonical regions.

Q001 is primarily a Stage 1 Mandatory Separation experiment. Its profiles test hard-boundary hypotheses based on regime, jurisdiction, and potentially territorial/legal identity. They do not produce the complete canonical travel partition and do not model Stage 2 destination identity. A `hard_compatible` pair may still be divided by Stage 2.

## 1. Basic predicates

### `must_separate(A, B, profile)`

True only when there is a sufficient positive ground forbidding A and B from being in one canonical travel region of the given profile.

For a regime-based split a witness `C` is sufficient if all of the following hold at once:

1. `C` is within the R007 scope;
2. the evidence for the context and for both decisions is sufficient and in effect at `as_of`;
3. `HardTravelDecision(A,C) != HardTravelDecision(B,C)` on a hard dimension of the profile;
4. the difference relates to admission to A/B as destinations as a whole, not to a `LocalAccessDecision` for a local overlay, a separate point, a route or an activity inside a common admission jurisdiction;
5. the witness does not have the status provisional, conflicted or unknown.

The coincidence of a local overlay with a whole administrative unit and its area do not change this test. Border-security, military, conservation, object-, route- and activity-specific permits are rejected as a split witness until the evidence shows that the permit regulates ordinary civilian admission to the candidate territory as a destination as a whole.

P2 additionally accepts an independently verified difference of `final_admission_jurisdiction`. P3 may additionally accept an identity discriminator, but this discriminator is not yet defined.

### `hard_compatible(A, B, profile)`

True only with sufficient positive proof of the equivalence of A and B across all hard dimensions of the profile:

```text
hard_compatible(A,B,P) :=
    signature_complete(A,P)
    and signature_complete(B,P)
    and signatures_equal(A,B,P) = true
    and no applicable must_separate certificate
```

`hard_compatible` is not the negation of `must_separate` and is not a decision to merge final canonical regions. The following implications are forbidden:

```text
no witness found  => hard_compatible
unknown           => false
not must_separate => hard_compatible
```

## 2. Signature completeness

Each dimension has a type, a scope and one state:

| State | Semantics | Admissible for a complete signature |
|---|---|---|
| `known_value` | An evidence-backed concrete value or normalised set of values | yes |
| `known_absence` | An evidence-backed statement that there is no applicable value/requirement | yes |
| `unknown` | The value is not established or the evidence is insufficient | no |
| `not_applicable` | The dimension is inapplicable on the stated rule-based ground | yes |
| `unresolved_model_semantics` | The model does not define how to compute or compare the dimension | no |

An empty field does not mean `known_absence`. `not_applicable` is not derived from the absence of a record. Both states require a rationale; `known_absence` requires positive evidence.

Completeness is proven not by going through several traveller examples, but by the evidence-backed applicability of normalised policy/scope records to the whole hard dimension within the fixed profile and R007 scope. A finite sample of coinciding decisions does not by itself complete the signature.

```text
signature_complete(A, P) = true
```

if and only if:

- the list of mandatory dimensions of P is defined;
- each dimension of A has the state `known_value`, `known_absence` or a justified `not_applicable`;
- the evidence matches the time, the scope and the required level of sufficiency;
- there is no unresolved source conflict that changes the value of a dimension.

```text
signatures_equal(A, B, P)
```

returns `true | false | unknown`:

- `true`: both signatures are complete, all mandatory typed dimensions are equal;
- `false`: both sides are comparable and at least one mandatory dimension provably differs;
- `unknown`: at least one signature is incomplete or the comparison of a dimension is not defined.

Two `not_applicable` are equal only for one and the same dimension and a compatible rationale. `known_absence` is not equal to `unknown`; the comparison of `known_absence` with `not_applicable` is not normalised automatically.

### Minimal working composition of the profiles

This composition is needed for the Q001 evaluator, but does not close Q002/Q004/Q005/Q009.

- P1 `regime_only`: `admission_decision_scope`, `visa_scope`, `document_scope`, `relevant_hard_permits`; also `route_dependent_hard_decisions`, if they are included in the specific version of the profile.
- P2 `jurisdiction`: all P1 dimensions plus `final_admission_jurisdiction` and the attribute of independence of the final decision.
- P3 `jurisdiction_plus_identity`: all P2 dimensions plus `identity_discriminator`.

Until `Q001.identity` is closed, the dimension `identity_discriminator` has `unresolved_model_semantics`; the evaluator does not derive it from a name, an ISO code, autonomy, island position or the type of dependency.

## 3. Input

The evaluator receives one immutable input bundle:

```yaml
spec_version: string
dataset_version: string
as_of: date
profile:
  id: P1 | P2 | P3
  version: string
  hard_dimensions: []
  traveller_scope_ref: R007
factual_units:
  - id: string
    dimensions: {}
comparison:
  id: Cxxx
  a: factual_unit_id
  b: factual_unit_id
  candidate_witnesses: []
  relevant_rules: []
  evaluator_data_blockers:
    - id: stable_machine_id
      kind: missing_fact | source_conflict | verification_status
      profiles: [P1, P2, P3]
      evidence_refs: []
evidence_records: []
```

- `profile` fixes the exact set of hard dimensions; the name P1/P2/P3 alone, without a version, is not enough for a reproducible build.
- `factual_units` contain typed values and states, but not a canonical verdict.
- `comparison` refers to the endpoints by ID. Names and political labels are not an input to the decision.
- `comparison.evaluator_data_blockers` is the typed source for comparison-level `data_unknown` semantics. Every entry has a stable ID, blocker kind, explicit profile applicability, and optional evidence references.
- Human-readable `blocked_by` prose is diagnostic documentation only. `blocked_by` prose is not an evaluator blocker, is never parsed by the adapter, and cannot by itself produce `data_unknown`.
- `evidence_records` contain status, temporal scope, source refs and locators. The order of the records is not significant.
- `spec_version` is mandatory; the evaluator does not mix rules of different versions.

## 4. Output

```yaml
comparison_id: Cxxx
profile: P1
result: must_separate | hard_compatible | separation_not_proven | model_unresolved | data_unknown | rule_conflict
applied_rules: []
witnesses: []
signature:
  a_complete: true | false
  b_complete: true | false
  equal: true | false | unknown
blocked_by_data: []
blocked_by_model: []
evidence_refs: []
explanation: string
```

- `comparison_id`: the stable ID of the input comparison.
- `profile`: the exact profile ID, consistent with the version in the input.
- `result`: one terminal pairwise outcome from section 5.
- `applied_rules`: the sorted set of the Rxxx actually applied; rules that are potentially relevant but not applied are not included here.
- `witnesses`: the normalised sufficient witnesses supporting `must_separate`. For the other outcomes the array is empty. Rejected candidates are reflected in explanation/blocks.
- `signature.a_complete` and `b_complete`: the results of `signature_complete`.
- `signature.equal`: the result of `signatures_equal`; the value `true` is possible only with two complete signatures.
- `blocked_by_data`: stable machine-readable IDs of the specific missing/conflicted records or dimensions. A comparison-level ID must come from `evaluator_data_blockers`; prose in `blocked_by` is not a substitute.
- `blocked_by_model`: stable Qxxx/predicate IDs, for example `Q001.identity`.
- `evidence_refs`: the sorted union of the evidence actually used for the outcome and the signature assessment.
- `explanation`: a short deterministic explanation with no inference from the names of territories.

Even with `must_separate` a signature may be incomplete: the witness is a sufficient counterexample to equality. With `hard_compatible` both completeness flags must be true, and `equal` must be true.

## 5. Outcomes and precedence

The evaluator applies the following order; within a step the records are sorted by stable ID.

1. `rule_conflict`: two compatible normative derivations require incompatible terminal outcomes for one set of accepted facts. A conflict of sources is not classified here.
2. `must_separate`: a sufficient P1/P2/P3 certificate exists. Later undefined dimensions do not cancel an already proven split.
3. `model_unresolved`: an undefined model predicate can change the terminal outcome. For P3, after the absence of a sufficient P1/P2 split, this is at least `Q001.identity`.
4. `data_unknown`: a specific unknown or unresolved source conflict blocks a mandatory dimension or the check of a candidate certificate. It is used when the problem is localised in the data, not merely when an open search has not proven universal equivalence.
5. `hard_compatible`: both signatures are complete and equal; there is no separate split-certificate. This is only positive compatibility on the hard dimensions of Stage 1, not a final merge decision.
6. `separation_not_proven`: a split-certificate is absent, but the conditions of `hard_compatible` are not met, and no more specific blocker above applies. This is an open result, not a terminal negative one.

Authoritative evidence records that give different values of one dimension under compatible temporal/scope conditions create a `source_conflict` in the data assessment and usually lead to `data_unknown`. `rule_conflict` arises only after normalisation of the facts, when the rules themselves conflict.

## 6. Profile algorithms

### P1 — `regime_only`

```text
if sufficient verified hard regime witness exists:
    must_separate
else if model semantics for a required P1 dimension are unresolved:
    model_unresolved
else if a concrete data blocker prevents required assessment:
    data_unknown
else if both P1 signatures are complete and equal:
    hard_compatible
else:
    separation_not_proven
```

### P2 — `jurisdiction`

First all P1 grounds are applied. Then independently verified different final admission jurisdictions give `must_separate` under R011, even with the same visa policy. `hard_compatible` requires a complete/equal P1 signature and complete/equal jurisdiction dimensions.

### P3 — `jurisdiction_plus_identity`

All sufficient P1/P2 grounds are kept. If they have not given `must_separate`, the outcome depends on the not yet defined identity discriminator and the following is returned:

```yaml
result: model_unresolved
blocked_by_model:
  - Q001.identity
```

For disputed/occupied/international-status distinctions Q006 is indicated in addition, if it is this type of identity that is involved. P3 does not contain a hidden manual list.

The P3 discriminator concerns territorial/legal identity: institutional status, dependencies, constitutional territorial identity, and disputed or international status. It is not destination identity and P3 is not the future Stage 2 destination evaluator.

## 7. Determinism requirements

The evaluator must be:

- deterministic: the same normalised bundle gives byte-equivalent semantic output;
- order-independent: a permutation of the factual/evidence/rule records does not change the result;
- symmetric for pairwise semantics: an A/B swap changes only the oriented fields of the witness, but not the result;
- name-blind: names, country labels and display order do not take part in the predicate;
- explicit about unknown: missing/null/empty are not normalised into false or absence;
- fail-closed for hard compatibility: an incomplete signature never produces `hard_compatible`.

## 8. Representative Q001 classifications

This is an application of the contract to already collected facts, not a change of factual evidence and not an assignment of canonical regions.

For example, a future complete evaluation of Portugal mainland / Madeira or Italy / Sicily could return `hard_compatible` under a Stage 1 profile. That would mean only that the profile found no mandatory hard boundary. Stage 2 could still separate Madeira or Sicily as a travel destination.

```yaml
representative_evaluations:
  C001: # Germany / France
    P1: {result: data_unknown, because: provisional LTV candidate has a concrete verification-status blocker under fixture F013 and outcome precedence, blocked_by_data: [E01.status]}
    P2: {result: must_separate, because: independently verified final admission jurisdictions differ under R011, evidence_refs: [E02, E03]}
    P3: {result: must_separate, because: P2 already proves separation, evidence_refs: [E02, E03]}
  C002: # Italy / Sicily
    P1: {result: separation_not_proven, because: no verified witness and no complete equivalence audit}
    P2: {result: data_unknown, because: final jurisdiction comparison is provisional or incomplete, blocked_by_data: [final_admission_jurisdiction]}
    P3: {result: model_unresolved, blocked_by_model: [Q001.identity]}
  C014: # Portugal / Madeira
    P1: {result: separation_not_proven, because: matching sampled rules do not establish complete signatures}
    P2: {result: data_unknown, blocked_by_data: [final_admission_jurisdiction]}
    P3: {result: model_unresolved, blocked_by_model: [Q001.identity]}
  C008: # UK / Guernsey
    P1: {result: separation_not_proven, because: no fully specified hard regime witness and signatures are incomplete}
    P2: {result: must_separate, because: independently verified admission jurisdictions differ under R011, evidence_refs: [E18]}
    P3: {result: must_separate, because: P2 already proves separation, evidence_refs: [E18]}
  C009: # UK / Isle of Man
    P1: {result: separation_not_proven, because: no fully specified hard regime witness and signatures are incomplete}
    P2: {result: must_separate, because: independently verified admission jurisdictions differ under R011, evidence_refs: [E18, E21]}
    P3: {result: must_separate, because: P2 already proves separation, evidence_refs: [E18, E21]}
  C007: # UK / Jersey
    P1: {result: must_separate, because: verified accepted-document witness, evidence_refs: [E19]}
    P2: {result: must_separate, because: P1 witness and independently verified jurisdiction, evidence_refs: [E19, E20]}
    P3: {result: must_separate, because: P1/P2 already prove separation, evidence_refs: [E19, E20]}
  C018: # France / Reunion
    P1: {result: separation_not_proven, because: destination-visa distinction lacks a fully specified verified traveller witness}
    P2: {result: data_unknown, blocked_by_data: [final_admission_jurisdiction]}
    P3: {result: model_unresolved, blocked_by_model: [Q001.identity]}
  C013: # Finland / Aland
    P1: {result: model_unresolved, because: customs/fiscal distinction is not yet classified as a P1 hard dimension, blocked_by_model: [Q004]}
    P2: {result: model_unresolved, because: P1 customs semantics remain unresolved, blocked_by_model: [Q004]}
    P3: {result: model_unresolved, blocked_by_model: [Q001.identity, Q004]}
  C031: # Morocco proper / Western Sahara west
    P1: {result: separation_not_proven, because: one bounded matching passport rule is not complete regime equivalence}
    P2: {result: data_unknown, blocked_by_data: [final_admission_jurisdiction]}
    P3: {result: model_unresolved, blocked_by_model: [Q001.identity, Q006]}
  C032: # Western Sahara west / east
    P1: {result: data_unknown, blocked_by_data: [east_admission_rules, east_civilian_access]}
    P2: {result: data_unknown, blocked_by_data: [east_final_admission_jurisdiction]}
    P3: {result: model_unresolved, blocked_by_data: [east_admission_rules, east_civilian_access], blocked_by_model: [Q001.identity, Q006]}
  C042: # India / Arunachal Pradesh
    P1: {result: must_separate, because: verified whole-territory PAP witness, evidence_refs: [E07, E08, E44]}
    P2: {result: must_separate, because: P1 already proves separation, evidence_refs: [E07, E08, E44]}
    P3: {result: must_separate, because: P1 already proves separation, evidence_refs: [E07, E08, E44]}
  C041: # China / Tibet Autonomous Region
    P1: {result: separation_not_proven, because: permit candidate lacks a completed ordinary-baseline comparison}
    P2: {result: data_unknown, blocked_by_data: [final_admission_jurisdiction]}
    P3: {result: model_unresolved, blocked_by_model: [Q001.identity]}
  C040: # China / Aksai Chin
    P1: {result: data_unknown, blocked_by_data: [admission_rules, civilian_access, current_control_geometry]}
    P2: {result: data_unknown, blocked_by_data: [current_control_geometry, final_admission_jurisdiction]}
    P3: {result: model_unresolved, blocked_by_data: [admission_rules, civilian_access, current_control_geometry], blocked_by_model: [Q001.identity, Q006]}
```

Comments are display labels only; an implementation consumes comparison IDs and facts, not those names.

## 9. Fixture conventions

`evaluator-fixtures.yaml` uses a compact synthetic DSL:

- `complete:Sx` means that all mandatory dimensions of the given profile are represented by admissible states and are normalised into the signature token `Sx`;
- `incomplete:<reason>` means an incomplete signature and is not the value of a dimension;
- `known_value:X`, `known_absence:EV`, `not_applicable:RULE` and `source_conflict:A/B` correspond to the states of section 2;
- the `expected` object is a subset oracle: an implementation may return additional mandatory fields of the full output contract, but may not change the listed values;
- a fixture with `input_variants` requires the same semantic outcome for each variant.

Production input is not obliged to use these string abbreviations; it is obliged to keep the same typed semantics.

For transitional compatibility, implementation version 0.2 accepts the legacy string `may_merge` only when parsing an input rule derivation. Fixtures, generated output, APIs, and canonical documentation use `hard_compatible`.
