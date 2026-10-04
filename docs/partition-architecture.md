# Partition architecture

The normative requirements are in [spec.md](spec.md), especially R009, R039–R044 and R045–R058. This document is a short implementation-oriented map of those rules.

Canonical Travel Regions has one published output: an exhaustive, mutually exclusive, single-level partition. The project constructs that output in two internal stages.

## Stage 1: Mandatory Separation

Stage 1 identifies hard boundaries that no final region may cross. The current normative production profile is `S1-core-v1`: only CR-W, proven hard territorial TravelDecision discontinuity with G-SCOPE/G-CONTEXT/G-HARD/G-TIME/G-EVIDENCE. One coherent nonempty class-based civilian short-stay witness with matched context, standing territorial legal effect, proved decisions and applicable exceptions is sufficient, regardless of frequency.

CR-J remains a well-defined normative candidate, not adopted; its complete J1–J6 definition is preserved for later evaluation. Jurisdiction is not a required production signature dimension. Undefined territorial/legal identity alone is not an accepted hard separator. Claims, recognition, disputed/controller/military-control labels, dependency, autonomy, overseas and island labels do not independently split; actual hard travel consequences may support CR-W.

P1/P2/P3 are historical non-production Q001 profiles under their original contract, not aliases for the current core. P3 is model-unresolved where identity matters and is not the Stage 2 model. The current evaluator consumes separately versioned gate proofs; old P1 outcomes are not migrated without an audit.

The positive compatibility outcome is `hard_compatible`. It means both units have complete and equal signatures across all hard dimensions required by the profile and no mandatory-separation certificate applies. It does not assign the units to one final region. Open-world outcomes remain valid when evidence or model semantics are incomplete.

Absence of a CR-W certificate is not compatibility. Production completeness covers all accepted hard decision dimensions at the same versioned traveller scope and time, excluding CR-J/identity. Q001 is narrowed, not all Stage 1 semantics complete. See the [adoption record](../experiments/q001/stage1-core-adoption.md).

### Stage 1 as decided on 2026-10-03 (D038–D068)

Stage 1 boundaries come from three sources, and a release is built from them under the product profile `S1-product-v1` (R057):

1. **Reference registry** (R045). Stage 1 refines ISO 3166-1 and the countries' points of view, each built from the country's sourced claims (D064, D065; Natural Earth's national views are a lead, checked difference by difference), at pinned editions that change only by the owner's decision at a release. No region crosses a country boundary under a declared perspective, except the land of special places below. Antarctica is one Stage 1 cell; claims there are overlays (R026).
2. **Disputed and special-status areas** (R047–R054), read from the [register](../data/disputed-areas/README.md). The holder of an area is whoever can in practice admit, refuse and remove a civilian (R048). A forcible change of control is accepted after three quiet calendar years or an explicit act of the losing side; while the line moves nothing is delimited (R049). Border-line disputes are special places; islets and paper claims are regions where civilians live; zones with no single holder are regions where civilians live and the parties state an outline; leases follow the lessor and are regions only with entry rules of their own. Outlines are never drawn here: they come from lines the parties state (R047).
3. **CR-W** (R044 with the amendments of R056): transit, organised-group, local-border-traffic and fee rules do not separate; a tour-operator-only rule does; an entry rule separates a whole top-level unit or a detached unit with a rule written for it, and an area held by another party through the holder's own rule.

Inside a registry cell, no recorded witness means no boundary; the result is marked as assumed, not proved, and every boundary states its rule and evidence level (`cited` suffices). Places that are not regions are **special places** — tickable objects inside their parent region, not counted as regions (R046) — or **markers**. Releases are yearly, for the situation at the end of the year; a boundary from an uncontested entry rule enters after two consecutive releases and leaves three years after its rule ends (R055).

Open: Q002, Q004, Q005, Q007–Q011 (narrowed) and Q013–Q016, Q018–Q019 — outlines and custom geometries, the reading of the registry, scope-test details, areas with no single holder, special places in the consumer, and release mechanics. D004–D007 remain accepted product regressions; they are expected to follow from the registry and stay open until a release check (V011) confirms it.

## Stage 2: Destination Partition

Stage 2 receives each Stage 1 cell independently and may subdivide it using destination semantics. This allows destination distinctions such as an island, coherent cultural region, or self-contained itinerary area to be considered even when Stage 1 finds no hard boundary.

For example, Stage 1 compatibility between Portugal mainland and Madeira, Italy and Sicily, or the continental United States and Hawaii would not settle their final placement. Stage 2 could still separate those destinations. Regional candidates such as Tuscany, Bavaria, or Andalusia likewise belong to Stage 2 unless an independent hard rule already requires separation.

Stage 2 divides the Antarctic cell by how and from where travellers reach it (D040). The Stage 2 algorithm is otherwise unspecified. Q012 tracks the required definitions, evidence model, and deterministic selection rule. P3's unresolved territorial/legal identity predicate is not a destination-identity model.

## Refinement invariant

```text
Stage2Partition refines Stage1Partition
```

Every Stage 2 cell belongs to exactly one Stage 1 cell. Stage 2 may split a Stage 1 cell and may never merge across a Stage 1 boundary. The final canonical partition is the Stage 2 result.

Subdivisions finer than this destination partition are outside the project's ontology.
