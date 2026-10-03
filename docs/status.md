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
- "Administers" (narrows Q007): the authority whose bodies in practice decide whether a civilian may be in the area (access control) — in practice meaning on the ground: its officers can admit a civilian, refuse one and remove one; rules issued for an area that cannot be enforced there do not count; if that cannot tell the neighbours apart, the one providing civil administration to residents; otherwise nobody. Both are register facts with sources; the result is computed. Agreed in principle; the owner asked for duration and stability to be defined first (a short military presence must not count).
- Islets disputed for the sea around them (`islets_for_maritime_zone`, 18 areas): a group with resident civilians (`inhabited` = yes in the register: today the Paracel and the Spratly Islands) is a region, outlined by its coastlines; the others are special places, their land going with whoever holds it. To settle when the rule is recorded: a group held in parts by several parties with no line between the parts (the Spratlys) has no single country in the default view, and what happens when the last residents leave belongs to the release-stability question.
- Areas another state claims on paper only (`paper_claim`, 47 areas): the same test as for islets. Such an area is a region if a supported point of view puts it in another country and it has resident civilians; otherwise it is a special place and its land goes with the holder. Areas with their own ISO 3166-1 entry stay regions regardless; a claim that no supported point of view shows gives only a marker.
- Entry of an uncontested regime (#20): a part of a country becomes a region because of its own entry rule only when the rule is in force at two yearly releases in a row. A stated expiry or "pilot" label is ignored. When the rule is suspended or ends, the region stays, marked as having no special rule at present, and is merged back if the rule has not returned after three years (the same number as the waiting time for contested control). The same holds for any boundary that lost its basis, including an islet group or claimed area whose last residents left.
- Releases (#20): one a year, for the situation at the end of the year; between releases the set of regions does not change, and only errors of ours are corrected.
- Editions of ISO 3166-1 and Natural Earth (#19): the canon is pinned to stated editions and moves to a new one only by the owner's decision at a release, after seeing what it would change.
- Geometry (owner, 2026-10-03): the lists above say which places are separate and whose they are; they are not the only source of outlines. The substrate must be extensible: where it has no fitting unit (South Ossetia is poorly cut in GADM), a custom geometry is added as needed, from a cited source of the line the parties state. How such geometries are sourced, pinned and versioned is not designed yet.
- Zones with no single holder (`own_regime`: UN buffer and separation zones, demilitarised zones, condominiums): a region with no country if civilians live there and the parties state its outline (the UN Buffer Zone in Cyprus, the Korean DMZ, the UNDOF area); otherwise a special place. Nothing is split between the neighbours.
- Leased areas and bases (`lease_or_base`): the country is the lessor's, since the parties agree whose land it is; the area is a region only where entry follows its own rules (Baikonur, Guantanamo Bay), and the lessee is named. A leased road or piece of a port with no population and no entry rule of its own is not a region.
- Special places are objects inside their parent region (owner, 2026-10-03): tickable, shown with the region that holds them, and not counted as regions. The owner expects TYR to carry them as a category of their own, something like "border curiosities"; this applies to every case above that is not a region (line disputes, undelimited stretches, uninhabited islets and claimed rocks, uninhabited zones, small leases). To be raised with TYR as an importer need, not changed from here.
- Recently resolved disputes (`resolved_recently`) need no rule of their own: the agreed outcome is taken over at the next release, and the place may stay as a special place.
- CR-W amendment A1 (#17): a rule for travellers in transit is not a witness; only trips to the place as a destination are compared, and a transit regime's territorial limits are an overlay.
- A [register of disputed and special-status areas](../data/disputed-areas/README.md) holds the facts that such rules read; no fact is entered from memory, each carries its source and quoted passage. Its facts were re-entered from sources on 2026-10-03 (1,067 facts, every passage found in its source); the doubts raised on the way are in its [review list](../data/disputed-areas/REVIEW.md).
- **The waiting time is three years** (#20): an area taken by force is unsettled and stays attributed to its last settled holder; the canon accepts the new holder after three consecutive quiet calendar years. The rule has no original or rightful holder (owner: who held an area first is often disputed, and some conflicts run for decades with long pauses): a retaking is a change like any other. What matters is that the side that lost the area has stopped trying to get it back: shown by three quiet years, or at once by an explicit act of that side (agreement, accepted ruling, renunciation of the claim, or ceasing to exist) — nothing weaker counts. The status creates no regions: an unsettled area becomes a region of its own when CR-W separates it (a source shows that entry there follows other rules) and at acceptance at the latest; until then it stays inside the region of the party it is attributed to, marked. While fighting moves the line, nothing is delimited at all: the regions touched carry a flag that part of them is unsettled (owner's proposal), and an area with the status exists only once the parties state a line. The status and its paths are as in the [settling rule](proposals/settling-rule.md); the points listed as open there are still to be confirmed.

**Open, in the order they will be asked:**

1. Stability (#20), one parameter at a time. The waiting time and the acts that end a contest are decided (above). Holding an area in fact is enough for acceptance; there is no separate condition about civil administration (decided). The settling rule is complete except for the release interval. **Next for stability: changes nobody contests** ([release stability](proposals/release-stability.md)), with evidence in the [regime-lifetimes experiment](../experiments/regime-lifetimes/README.md) — entry and exit are decided (above); the yearly release is decided (above); still open here: how new editions of ISO 3166-1 and Natural Earth are adopted (also item 3).
2. Disputed and special-status areas (#19), remaining kinds. Islets, paper claims and zones with no single holder are decided (above). Leases and resolved disputes are settled (above), so every kind in the register has a treatment; de facto states and occupied areas are covered by the settling rule. The register's [review list](../data/disputed-areas/REVIEW.md) feeds this: areas to split, merge or drop, and kinds that the sources do not support.
3. **Next: where outlines come from** — a design for custom geometries (sources, pinning, versioning) for areas the substrate cannot represent; needs a check of which sources carry the outlines of the register's areas (only 23 of 210 are linked to Natural Earth and 10 to Wikidata so far). Also to confirm: the registry rule sits in Stage 1, so Stage 2 cannot cross it either.
4. Consumer contract (#27): confirm the remaining requirements — delivery through TYR's file import, not tied to one substrate, stability between releases.
5. CR-W amendments (#17), one by one: transit is decided (above); **current question: a rule's scope must be a whole named unit**; whole-territory permits separate; organised-group classes; one rule spanning several units.
6. Product profile and evidence levels (#22): no boundary inside a country cell without a cited witness; "cited" versus "audited".
7. Release format for TYR and the importer gaps to raise there.
8. Frozen Q001 package in Russian (#29): leave as history or publish an English snapshot.
9. Stage 2 direction (#28): grouping source and level-selection rule — after the Stage 1 decisions.

## Experiments

Concluded on 2026-10-03 unless marked.

- [World Stage 1 draft](../experiments/stage1-world-draft/README.md) (#22): 278 registry cells + 26 cited CR-W cells = 304. Count-only, secondary evidence.
- [Stage 2 scale survey](../experiments/stage2-scale-survey/README.md) (#28): the reference scale needs grouping of first-level units in 142 of 183 countries.
- [Wikivoyage composition check](../experiments/stage2-wikivoyage-composition/README.md) (#28): regions resolve to official units without drawing in about half of the test countries.
- [Control duration](../experiments/control-duration/README.md) (#20): a third of occupations since 1946 ended within two years; fighting over territory resumes within ten years in a third of cases after two quiet years, a sixth after five.
- [Regime lifetimes](../experiments/regime-lifetimes/README.md) (#20): of 55 territory-specific entry regimes started since 2000, 4 ended within two years outside the 2020 closures; suspended regimes mostly resumed within two to four years. Collected passages not re-checked.
- [Settling-rule back-test](../experiments/settling-rule/README.md) (#20): on 78 seizures by states and 40 breakaway entities, raising the wait from 2 to 3 years is the last step that removes reversals by force; the map at the end of 2024 is the same for 1 to 3 years.

## Next step

After decisions 1–3: bind the Stage 1 draft's cells to substrate units and build the first release package in the proposed format. For Stage 2: a prototype on the countries where composition resolves (Thailand, Japan, Algeria, Iran, Nigeria, Malaysia), and a rule for choosing the level where no published level fits the scale.
