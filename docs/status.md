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
- Unclaimed land (`unclaimed`: Bir Tawil, the Danube west-bank pockets) is a cell of its own with no country; its outline is what the neighbours' own claim lines leave out. Areas where a boundary must exist but is not agreed (`no_agreed_boundary`: Siachen, Ilemi, Doklam, the Southern Patagonian Ice Field section, Lake Constance) are not cells: the land goes with whoever administers it and the place is a tickable special place. Agreed in principle; depends on the two definitions below.
- Principle: the outline of a special cell is never drawn here. It comes from lines the parties themselves state (claim, ceasefire, treaty or lease lines, coastlines); where there are none, there is no cell, only a special place.
- "Administers" (narrows Q007): the authority whose bodies in practice decide whether a civilian may be in the area (access control); if that cannot tell the neighbours apart, the one providing civil administration to residents; otherwise nobody. Both are register facts with sources; the result is computed. Agreed in principle; the owner asked for duration and stability to be defined first (a short military presence must not count).
- A [register of disputed and special-status areas](../data/disputed-areas/README.md) holds the facts that such rules read; no fact is entered from memory, each carries its source and quoted passage. Its facts are being re-entered from sources.

**Open, in the order they will be asked:**

1. Stability (#20), one parameter at a time. **Current question: the waiting time T** in the [settling rule](proposals/settling-rule.md) — an "unsettled" status for areas taken by force, with the canon accepting the new holder after T quiet years. The owner asked for a stronger basis than another list's practice, a state machine with examples, and the picture under different T; the [back-test](../experiments/settling-rule/README.md) and the [literature note](research/2026-10-03-settling-time-literature.md) answer that and point to T = 3. Then, from the same proposal: whether an unsettled area is a region of its own from the start; the original holder's return; evidence of a standing civil arrangement. Then, for changes nobody contests ([release stability](proposals/release-stability.md)): how a changing regime such as a visa rule enters and leaves a release, the release interval, whether a boundary that lost its basis is removed or kept, and how new editions of ISO 3166-1 and Natural Earth are adopted.
2. Disputed and special-status areas (#19), remaining kinds: islets disputed for the sea around them; then own regime, lease or base, de facto state, occupied, paper claim.
3. Two consequences of the registry rule to confirm: it sits in Stage 1 (Stage 2 cannot cross it either); new ISO or Natural Earth editions change cells only at a release, by decision.
4. Consumer contract (#27): confirm the remaining requirements — delivery through TYR's file import, not tied to one substrate, stability between releases.
5. CR-W amendments (#17), one by one: transit is not a witness; a rule's scope must be a whole named unit; whole-territory permits separate; organised-group classes; one rule spanning several units.
6. Product profile and evidence levels (#22): no boundary inside a country cell without a cited witness; "cited" versus "audited".
7. Release format for TYR and the importer gaps to raise there.
8. Frozen Q001 package in Russian (#29): leave as history or publish an English snapshot.
9. Stage 2 direction (#28): grouping source and level-selection rule — after the Stage 1 decisions.

## Experiments

All concluded on 2026-10-03; none active.

- [World Stage 1 draft](../experiments/stage1-world-draft/README.md) (#22): 278 registry cells + 26 cited CR-W cells = 304. Count-only, secondary evidence.
- [Stage 2 scale survey](../experiments/stage2-scale-survey/README.md) (#28): the reference scale needs grouping of first-level units in 142 of 183 countries.
- [Wikivoyage composition check](../experiments/stage2-wikivoyage-composition/README.md) (#28): regions resolve to official units without drawing in about half of the test countries.
- [Control duration](../experiments/control-duration/README.md) (#20): a third of occupations since 1946 ended within two years; fighting over territory resumes within ten years in a third of cases after two quiet years, a sixth after five.
- [Settling-rule back-test](../experiments/settling-rule/README.md) (#20): on 78 seizures by states and 40 breakaway entities, raising the wait from 2 to 3 years is the last step that removes reversals by force; the map at the end of 2024 is the same for 1 to 3 years.

## Next step

After decisions 1–3: bind the Stage 1 draft's cells to substrate units and build the first release package in the proposed format. For Stage 2: a prototype on the countries where composition resolves (Thailand, Japan, Algeria, Iran, Nigeria, Malaysia), and a rule for choosing the level where no published level fits the scale.
