> **Translation note.** This is an English translation, made on 2026-10-03, of the frozen package [`experiments/q001/`](../q001/) as of git tag `q001-baseline`. The Russian original is the record. This copy is not an input to any tool, and it is not validated by the original scripts: `validate.py` is not copied here; the command below refers to the original package.

# Experiment Q001 — factual dataset

Historical P1/P2/P3 experiment; facts and recorded results remain unchanged. Current production adoption is **CR-W only**, profile `S1-core-v1`, not a reinterpretation of these results. CR-J is well-defined but not adopted; P3 is non-production/model-unresolved, not Stage 2. See [stage1-core-adoption.md](stage1-core-adoption.md) for the decision and separate proof input contract.

Check snapshot: **11 September 2026**. The set is intended for comparing three hypotheses, not for choosing canonical regions.

- **P1 — regime_only:** a material TravelDecision witness in the R007 scope.
- **P2 — jurisdiction:** P1 plus an independent final admission jurisdiction.
- **P3 — jurisdiction_plus_identity:** P2 plus an identity criterion that is not yet defined.

## Composition and running

49 comparisons; 56 supporting factual units, including reference scopes, a status object and overlays. The number of "cases" is counted by comparisons, not by all supporting units. All mandatory groups are present. 12 comparisons are included in the blind set.

`facts/*.json` contains records with the mandatory categories. `comparisons.yaml` and `blind-comparisons.yaml` use JSON syntax — a valid subset of YAML 1.2; they can be read with a standard JSON parser. `evidence.json` stores short atomic statements, `sources.json` — sources, dates and limitations. `route-matrix.json` separately shows the Western Sahara routes. `evaluator-contract.md` sets the open-world semantics, and `evaluator-fixtures.yaml` — the regression fixtures for the implementation. `validate.py` checks referential consistency and the main invariants.

```bash
python3 validate.py
```

## Method

The project spec.md, decisions.md and open-questions.md were read; adversarial-test-set.csv was not used as a factual authority. The fields are built from the sources that were read: law/official procedure take priority; for disputed control the official claim, the independent report and the UN observation are kept apart. Where the full text is unavailable, the indexed excerpt is marked provisional and is not passed off as a full audit.

Scope: a civilian short-term visit, nationality/document/residence/route context. Work, diplomatic service and a military mission do not create positive witnesses. The MINURSO observations are used only as evidence of operational restrictions, not as rules of tourist admission.

Each substantive field has `evidence_refs`, and each evidence — `source_refs`, a locator, a status and observed_as_of. `unknown` means the absence of an established value; empty references are admissible only for unknown or for the description of the chosen experimental scope. `false` refers only to the stated dimension and does not mean `hard_compatible`. The description of the geography sets the subject of the study; it is not an exact operational polygon.

`regime_difference=true` requires a concrete context and a distinguishing component of the decision. "Visa exempt" does not mean guaranteed admission. The existence of a similar rule for one passport does not give `regime_difference=false`: R009 forbids proving global equivalence by a finite sample. General visa differences without a completed check of nationality exceptions are left unknown with an explanation. The absence of a witness gives not positive compatibility but `separation_not_proven`, `data_unknown` or `model_unresolved`, depending on the blocker. `hard_compatible` requires a separately proven complete equal hard signature.

For P2 a local office of a national agency is distinguished from an independent jurisdiction that takes the final decision. Different visa endorsements, a parliament or the status of a constituent country do not by themselves prove it. `distinct_operational_control` may refer to a civil/military function; comparison C032 does not establish two immigration jurisdictions.

## Blind protocol

The evaluator receives only `blind-comparisons.yaml`, without `blind-answer-key.json`, the source-index or the full set. Names, original IDs and names of agencies are replaced with consistent aliases; source URLs and document titles are excluded from the payload. Field types, values, uncertainty, dates, conditions and the provenance graph are preserved. A structurally unique rule may still be recognisable — anonymisation does not guarantee that guessing is impossible. The key is needed only by the researcher for matching outcomes.

## Evaluator boundary

`must_separate` and `hard_compatible` are independent. P1 accepts a verified hard witness; P2 additionally accepts independently verified different final admission jurisdictions; P3 does not guess territorial/legal identity and returns `model_unresolved` with `Q001.identity` if P1/P2 have not already proven a split. Q006 remains only for disputed/occupied/international-status distinctions.

Q001 is a Stage 1 Mandatory Separation experiment. A `hard_compatible` result means only that the selected profile requires no hard boundary; it does not assign a final canonical region. P3 is a Stage 1 territorial/legal identity hypothesis, not a Stage 2 destination-identity evaluator.

Comparison `blocked_by` strings are human-readable diagnostics and have no terminal evaluator semantics. A comparison-level missing fact produces `data_unknown` only when represented by a typed `evaluator_data_blockers` entry with a stable ID and explicit profile applicability, or when it follows from another structured status such as provisional witness evidence.

## Limitations

This is a verifiable research snapshot with explicit gaps, not a fully confirmed travel reference. Some required disputed cases intentionally remain blocked: neither absent sources nor political status are filled by inference. A page check date does not turn a 2023–2025 observation into a current 2026 map. See `data-gaps.md` for the full limitations. The reference evaluator is implemented, but profiles remain unranked, Stage 2 is undefined, and no canonical verdicts exist.
