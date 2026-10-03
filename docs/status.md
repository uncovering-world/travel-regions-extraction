# Status

Updated: 2026-10-03.

## Focus

The goal is a first release of the canon for Track Your Regions: Stage 1 cells bound to units, then Stage 2 regions at traveller scale. Proposals and first experiments exist for every open decision; the owner is deciding them one at a time.

## Decision queue

Decisions are taken one at a time in conversation with the owner; this list is the backlog of questions so that none is lost. Proposals in `docs/proposals/` hold the options and evidence.

**Decided on 2026-10-03 and recorded** in [decisions.md](decisions.md), [spec.md](spec.md) and [open-questions.md](open-questions.md):

- D038 / R045 — reference registry: Stage 1 refines ISO 3166-1 and the Natural Earth national points of view (#19); D039 — pinned editions, changed only by the owner's decision at a release.
- D040 / R026 (amended) — Antarctica: one Stage 1 cell, divided in Stage 2 by access; claims stay an overlay.
- D041 / R046 — special places are tickable objects inside their parent region, not regions; to be raised with TYR as an importer need.
- D042 / R047 — outlines only from lines the parties state; the substrate is extensible with cited custom geometries (design open: Q013).
- D043 / R048, R049 — the holder of an area and the settling rule (three quiet years, explicit acts, no original holder, moving lines flagged) (#20).
- D044–D048 / R050–R054 — by kind: border-line disputes are special places; islets and paper claims are regions where civilians live; zones with no single holder are regions where civilians live and the parties state an outline; leases follow the lessor; resolved disputes are taken over at the next release.
- D049 / R055 — yearly releases; an uncontested entry rule enters after two consecutive releases and leaves three years after it ends (#20).
- D050 / R056 — CR-W amendments: transit, scope test, whole-unit presence permits, group-only and local-border-traffic rules, tour-operator rules, held areas, fees (#17).
- D051 / R057 — product profile `S1-product-v1`: no witness, no boundary; "cited" evidence enters a release (#22).
- Rejected: D052 (tying small disputed areas to the substrate, or a bare area threshold), D053 (the original-holder path).
- A [register of disputed and special-status areas](../data/disputed-areas/README.md) holds the facts that such rules read; no fact is entered from memory, each carries its source and quoted passage. Its facts were re-entered from sources on 2026-10-03 (1,067 facts, every passage found in its source); the doubts raised on the way are in its [review list](../data/disputed-areas/REVIEW.md).

**Not recorded as adopted** — agreed only in principle, or left open, on 2026-10-03; kept as open questions:

- An islet group held in parts by several parties with no line between them has no single country in the default view — to settle (Q016).
- One rule over several top-level units: a known rough case of the scope test (D050); one region per unit or one for their union — Q015.

**Open, in the order they will be asked:**

1. Stability (#20), one parameter at a time. The waiting time and the acts that end a contest are decided (above). Holding an area in fact is enough for acceptance; there is no separate condition about civil administration (decided). The settling rule is recorded (D043, R049). **Next for stability: changes nobody contests** ([release stability](proposals/release-stability.md)), with evidence in the [regime-lifetimes experiment](../experiments/regime-lifetimes/README.md) — entry and exit, the yearly release and registry editions are decided and recorded (D049, D039); still open here: release mechanics (Q019).
2. Disputed and special-status areas (#19), remaining kinds. Islets, paper claims, zones with no single holder, leases and resolved disputes are recorded (D044–D048, D054); de facto states and occupied areas are covered by the settling rule (D043). Still open: unclaimed land and undelimited stretches (Q017) and areas with no single holder that are not regions (Q016). The register's [review list](../data/disputed-areas/REVIEW.md) feeds this: areas to split, merge or drop, and kinds that the sources do not support.
3. **Next: where outlines come from** — a design for custom geometries (sources, pinning, versioning) for areas the substrate cannot represent; needs a check of which sources carry the outlines of the register's areas (only 23 of 210 are linked to Natural Earth and 10 to Wikidata so far). Design question recorded as Q013. The registry rule is recorded as sitting in Stage 1 (D038), as the decision's wording says; the owner had also asked to confirm this explicitly.
4. Consumer contract (#27): confirm the remaining requirements — delivery through TYR's file import, not tied to one substrate, stability between releases.
5. CR-W amendments (#17): recorded (D050, R056). Left as a known rough case: one rule over several top-level units (Q015).
6. Product profile (#22): recorded (D051, R057).
7. Release format for TYR and the importer gaps to raise there.
8. Frozen Q001 package (#29): done — an English copy is in `experiments/q001-en/`; the Russian original is untouched and remains the record. The translation was machine-made and only spot-checked.
9. Stage 2 direction (#28): grouping source and level-selection rule — after the Stage 1 decisions.

## Experiments

Concluded on 2026-10-03 unless marked.

- [World Stage 1 draft](../experiments/stage1-world-draft/README.md) (#22): 278 registry cells + 26 cited CR-W cells = 304. Count-only, secondary evidence.
- [Stage 2 scale survey](../experiments/stage2-scale-survey/README.md) (#28): the reference scale needs grouping of first-level units in 142 of 183 countries.
- [Wikivoyage composition check](../experiments/stage2-wikivoyage-composition/README.md) (#28): regions resolve to official units without drawing in about half of the test countries.
- [Control duration](../experiments/control-duration/README.md) (#20): a third of occupations since 1946 ended within two years; fighting over territory resumes within ten years in a third of cases after two quiet years, a sixth after five.
- [Stage 1 as a list](../experiments/stage1-list/README.md) (#22): the rules decided on 2026-10-03 give 316 regions (296 with nothing open), 90 special places and 20 missing facts after three rounds of fact collection; the ties between the register, the map features and UCDP conflicts are judgements by name and are its weakest input.
- [Regime lifetimes](../experiments/regime-lifetimes/README.md) (#20): of 55 territory-specific entry regimes started since 2000, 4 ended within two years outside the 2020 closures; suspended regimes mostly resumed within two to four years. Collected passages not re-checked.
- [Settling-rule back-test](../experiments/settling-rule/README.md) (#20): on 78 seizures by states and 40 breakaway entities, raising the wait from 2 to 3 years is the last step that removes reversals by force; the map at the end of 2024 is the same for 1 to 3 years.

## Next step

The Stage 1 list is built: 320 regions, 307 with nothing open, 87 special places, two facts missing; entry rules are now found by a scripted discovery (`data/entry-rules/`), repeated yearly. Next: outlines for places the substrate cannot represent (Q013), the binding to substrate units, and the release package for TYR.
