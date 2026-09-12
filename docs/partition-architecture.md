# Partition architecture

The normative requirements are in [spec.md](spec.md), especially R009 and R039–R044. This document is a short implementation-oriented map of those rules.

Canonical Travel Regions has one published output: an exhaustive, mutually exclusive, single-level partition. The project constructs that output in two internal stages.

## Stage 1: Mandatory Separation

Stage 1 identifies hard boundaries that no final region may cross. The current normative production profile is `S1-core-v1`: only CR-W, proven hard territorial TravelDecision discontinuity with G-SCOPE/G-CONTEXT/G-HARD/G-TIME/G-EVIDENCE. One coherent nonempty class-based civilian short-stay witness with matched context, standing territorial legal effect, proved decisions and applicable exceptions is sufficient, regardless of frequency.

CR-J remains a well-defined normative candidate, not adopted; its complete J1–J6 definition is preserved for later evaluation. Jurisdiction is not a required production signature dimension. Undefined territorial/legal identity alone is not an accepted hard separator. Claims, recognition, disputed/controller/military-control labels, dependency, autonomy, overseas and island labels do not independently split; actual hard travel consequences may support CR-W.

P1/P2/P3 are historical non-production Q001 profiles under their original contract, not aliases for the current core. P3 is model-unresolved where identity matters and is not the Stage 2 model. The current evaluator consumes separately versioned gate proofs; old P1 outcomes are not migrated without an audit.

The positive compatibility outcome is `hard_compatible`. It means both units have complete and equal signatures across all hard dimensions required by the profile and no mandatory-separation certificate applies. It does not assign the units to one final region. Open-world outcomes remain valid when evidence or model semantics are incomplete.

Absence of a CR-W certificate is not compatibility. Production completeness covers all accepted hard decision dimensions at the same versioned traveller scope and time, excluding CR-J/identity. Q001 is narrowed, not all Stage 1 semantics complete. Q002/Q004/Q005/Q006/Q007/Q008/Q009/Q011 remain open. D004–D007 remain accepted product regressions; unresolved guarantees are neither hardcoded nor assumed solved by Stage 2. See the [adoption record](../experiments/q001/stage1-core-adoption.md).

## Stage 2: Destination Partition

Stage 2 receives each Stage 1 cell independently and may subdivide it using destination semantics. This allows destination distinctions such as an island, coherent cultural region, or self-contained itinerary area to be considered even when Stage 1 finds no hard boundary.

For example, Stage 1 compatibility between Portugal mainland and Madeira, Italy and Sicily, or the continental United States and Hawaii would not settle their final placement. Stage 2 could still separate those destinations. Regional candidates such as Tuscany, Bavaria, or Andalusia likewise belong to Stage 2 unless an independent hard rule already requires separation.

The Stage 2 algorithm is intentionally unspecified. Q012 tracks the required definitions, evidence model, and deterministic selection rule. P3's unresolved territorial/legal identity predicate is not a destination-identity model.

## Refinement invariant

```text
Stage2Partition refines Stage1Partition
```

Every Stage 2 cell belongs to exactly one Stage 1 cell. Stage 2 may split a Stage 1 cell and may never merge across a Stage 1 boundary. The final canonical partition is the Stage 2 result.

Subdivisions finer than this destination partition are outside the project's ontology.
