# CR-W amendments — proposal

**Status: proposal, not adopted.** Issue: [#17](https://github.com/uncovering-world/travel-regions-extraction/issues/17). Evidence: the [world Stage 1 draft](../../experiments/stage1-world-draft/README.md) and its census of 116 territory-specific entry regimes (secondary evidence for most rows).

## Question

CR-W (R044) is adopted and stays the core. Applied to real regimes it produces good cells (Jeju, Sabah, Rapa Nui, Zanzibar) and artefacts (transit areas, border bands, site lists). Which general predicates remove the artefacts without removing the good cells? This serves Q002 (traveller contexts), Q005 (permit or overlay) and Q009 (spatial dependency inside a region).

## What the census shows

Without any amendment the census gives 55 CR-W cells; with the three amendments below, 26.

| Kind of scope | Examples | Rows in force and cited |
|---|---|---|
| A whole named unit with its own entry rule | Jeju, Hainan, Phu Quoc, Sabah, Sarawak, Zanzibar, Rapa Nui, Galápagos, San Andrés, Ascension, Puntland | 18 |
| A whole named unit under a presence permit | Tibet, Sikkim, Arunachal Pradesh, Gorno-Badakhshan, Chukotka, Mount Athos, Tristan da Cunha | 8 |
| A band, zone or part of a unit | Russian and Indian border zones, Nepal's restricted areas, Eritrea outside Asmara | most of the 28 removed |
| A list of sites, ports or parcels | Aegean islands of the Greek express visa, cruise ports, indigenous lands, closed cities | the rest of the 28 |
| A transit regime | China's 240-hour permitted areas | 1 scope (dozens of units) |

## Proposed amendments

**A1 — Transit is not a witness.** G-CONTEXT compares the same logical trip *to* each of the two scopes as a destination. A class whose trip is defined by onward travel to a third territory is not a witness; the territorial limits of a transit regime are an overlay (R017, R027).
*Keeps:* Hainan, Jeju (a visit to that place). *Removes:* China's transit areas.
*Counterexample to watch:* a "transit" visa that in practice allows a ten-day visit — the class is still defined by onward travel, so it stays an overlay; the stay it permits is recorded as an overlay property.

**A2 — The scope is a territorial unit named by the rule.** G-SCOPE is satisfied only when the rule itself defines its territorial scope as a named unit or an explicit set of whole named units. A scope defined by distance from a line, by a list of sites, ports or terminals, by a class of parcels, or by "parts of" a unit is an overlay.
*Keeps:* every row of the first two kinds above. *Removes:* border bands, site lists, the US Border Crossing Card zone, cruise-port schemes.
*Counterexamples to watch:* (a) the Greek express visa is issued for one named island at a time — a list of whole named units, so by the letter of A2 each island would qualify; (b) a rule over several whole units (Mexico's Regional Visitor Card covers five states) — A2 keeps it and the cell is the union of the units, which looks odd as a region.

**A3 — Whole-territory presence permits separate (a convention).** A standing rule that makes presence in a whole named unit conditional on a permit for a civilian short-stay class is a hard difference in `permission_to_enter_or_be_present_in_territorial_scope`. This is the explicit convention Q005 asks for; R014's overlay default continues to cover everything that is not a whole named unit.
*Effect:* 8 cells. The alternative — permits never separate — loses Tibet, Sikkim, Athos and Gorno-Badakhshan, which every travel list treats as places of their own.
*Counterexample to watch:* Chukotka's permit reportedly excludes one district; a unit "with exceptions" is then not whole, and A2 decides.

## Questions the census raised that the amendments do not answer

1. **Organised-group classes.** Guilin and Xishuangbanna are visa-free only for tour groups from ASEAN countries. Is "member of an organised group" a civilian short-stay class under G-CONTEXT, or a logistics condition? Proposed: a class defined by the mode of organisation of the trip is not a witness — the same reasoning as A1.
2. **Narrow nationality classes over several units** (southern Mexico for four nationalities). D032 says one class suffices and frequency does not matter; changing that is not proposed. Whether the union of five states is one cell is a Stage 1 geometry question: proposed yes, and Stage 2 may refine it.
3. **Resolution.** Clipperton and Tristan da Cunha show CR-W cells need the same resolution rule as registry cells ([registry proposal](reference-registry.md), parameter 2).
4. **Mandatory purchases and fees.** Zanzibar's compulsory insurance and the Galápagos and Fernando de Noronha fees: is a payment an entry condition (hard) or a fiscal formality (Q004)? The census treats separate immigration control and stay limits as hard and fees as not; Zanzibar is in the baseline through its separate control, not its insurance.
5. **Evidence.** Only 4 of the 26 cells rest on an official page read directly. Under the [proposed product profile](product-profile.md) "cited" is enough to enter a release; raising the 22 others to an official source is ordinary research, not an audit.

## Effects on existing items if adopted

R044's G-CONTEXT and G-SCOPE rows gain A1 and A2; R014 gains A3 as the adopted whole-unit convention and Q005 narrows to units "with exceptions"; R027 is referenced by A1; Q002 narrows (transit and organised-group classes settled if question 1 is decided); adversarial rows T106 and T107 change from research hypotheses to rule inferences.

## Recommendation

Adopt A1, A2 and A3 together, and decide question 1 (organised groups) with them. Leave questions 2–4 open until geometry exists for the draft.
