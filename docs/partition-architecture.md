# Partition architecture

The normative requirements are in [spec.md](spec.md), especially R009 and R039–R043. This document is a short implementation-oriented map of those rules.

Canonical Travel Regions has one published output: an exhaustive, mutually exclusive, single-level partition. The project constructs that output in two internal stages.

## Stage 1: Mandatory Separation

Stage 1 identifies hard boundaries that no final region may cross. It asks whether two territorial units must be separated under a selected hard-boundary profile. Q001's P1, P2, and P3 are competing Stage 1 hypotheses.

The positive compatibility outcome is `hard_compatible`. It means both units have complete and equal signatures across all hard dimensions required by the profile and no mandatory-separation certificate applies. It does not assign the units to one final region. Open-world outcomes remain valid when evidence or model semantics are incomplete.

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
