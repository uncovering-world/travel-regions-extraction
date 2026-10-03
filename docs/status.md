# Status

Updated: 2026-10-03.

## Focus

The goal is a first release of the canon for Track Your Regions: Stage 1 cells bound to units, then Stage 2 regions at traveller scale. Proposals and first experiments exist for every open decision; the owner is deciding them one at a time.

## Decision queue

Decisions are taken one at a time in conversation with the owner; this list is the backlog of questions so that none is lost. Proposals in `docs/proposals/` hold the options and evidence.

**Decided on 2026-10-03, to be recorded in spec/decisions once question 2 is answered:**

- A region never crosses a country boundary under any supported perspective: Stage 1 refines ISO 3166-1 and the Natural Earth national points of view (#19).
- Antarctica: one cell in Stage 1; Stage 2 divides it by how and from where travellers reach it, also taking into account how people who work there see it; claims stay an overlay.
- Rejected for small disputed areas: tying them to the substrate (the substrate is not an authority) and a bare area threshold.
- Disputes about where a border line runs (`line_position` in the register) are not cells: the area belongs to the region of whoever administers it, and the dispute is a tickable special place on top of the map.
- A [register of disputed and special-status areas](../data/disputed-areas/README.md) holds the facts that such rules read; no fact is entered from memory, each carries its source and quoted passage. Its facts are being re-entered from sources.

**Open, in the order they will be asked:**

1. Disputed and special-status areas (#19), one kind at a time: areas with no agreed boundary; islets disputed for the sea around them; then the remaining kinds (own regime, lease or base, de facto state, occupied, paper claim).
2. Two consequences of the registry rule to confirm: it sits in Stage 1 (Stage 2 cannot cross it either); new ISO or Natural Earth editions change cells only at a release, by decision.
3. Consumer contract (#27): confirm the remaining requirements — delivery through TYR's file import, not tied to one substrate, stability between releases.
4. CR-W amendments (#17), one by one: transit is not a witness; a rule's scope must be a whole named unit; whole-territory permits separate; organised-group classes; one rule spanning several units.
5. Product profile and evidence levels (#22): no boundary inside a country cell without a cited witness; "cited" versus "audited".
6. Release stability policy (#20): how a changing regime enters and leaves a release; interval.
7. Release format for TYR and the importer gaps to raise there.
8. Frozen Q001 package in Russian (#29): leave as history or publish an English snapshot.
9. Stage 2 direction (#28): grouping source and level-selection rule — after the Stage 1 decisions.

## Experiments

All concluded on 2026-10-03; none active.

- [World Stage 1 draft](../experiments/stage1-world-draft/README.md) (#22): 278 registry cells + 26 cited CR-W cells = 304. Count-only, secondary evidence.
- [Stage 2 scale survey](../experiments/stage2-scale-survey/README.md) (#28): the reference scale needs grouping of first-level units in 142 of 183 countries.
- [Wikivoyage composition check](../experiments/stage2-wikivoyage-composition/README.md) (#28): regions resolve to official units without drawing in about half of the test countries.

## Next step

After decisions 1–3: bind the Stage 1 draft's cells to substrate units and build the first release package in the proposed format. For Stage 2: a prototype on the countries where composition resolves (Thailand, Japan, Algeria, Iran, Nigeria, Malaysia), and a rule for choosing the level where no published level fits the scale.
