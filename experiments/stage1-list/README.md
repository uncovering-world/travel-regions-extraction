# Stage 1 as a list, under the rules decided on 2026-10-03

**Experiment, not the canon.** Issues: [#22](https://github.com/uncovering-world/travel-regions-extraction/issues/22), [#19](https://github.com/uncovering-world/travel-regions-extraction/issues/19), [#17](https://github.com/uncovering-world/travel-regions-extraction/issues/17).

## Question

The owner's decisions of 2026-10-03 (recorded in [docs/status.md](../../docs/status.md), not yet in the spec) give every kind of disputed or special-status area a treatment and narrow which entry rules make a region. Applied to the data already in the repository, without geometry:

1. Which regions, special places and markers result, and how many of each?
2. For which places can the rules not be applied because a fact is missing, and which fact?

Assumes those decisions as the rule set, and the product profile "no witness, no boundary" with evidence level "cited". No geometry and no binding to a substrate; the list is a draft.

## Related

R044; D004–D007; the [first world draft](../stage1-world-draft/README.md), whose registry cells and census of entry rules are inputs; the [register of disputed areas](../../data/disputed-areas/README.md); the [settling rule](../../docs/proposals/settling-rule.md).

## What would change our mind

Written before the first run.

1. If most places of the kinds that depend on a register fact (residents, who holds the area, a recorded entry rule) cannot be decided, the next step is collecting those facts, not geometry.
2. If the count of regions moves far from the first draft's 304 in either direction, the decided rules behave differently from what was assumed when they were chosen, and the cases behind the difference go back to the owner.
3. If accepted product constraints D004–D007 do not come out of the rules, a rule is missing.
4. If many registry cells cannot be tied to a register area, or the reverse, the two lists describe the world differently and need to be reconciled before a release.

## Method

```bash
python3 experiments/stage1-list/run.py
```

`run.py` reads the 249 ISO entries and 29 registry cells of the first world draft (Natural Earth points of view, areas of 100 km² and more), its census of 116 entry rules, and the register's 210 areas, and applies the decided treatment per kind. `inputs/links.csv` ties 34 register areas to an ISO entry, a registry cell or a census row, each with the basis of the tie; the ties were made by name and by the registry's own notes, not from a source, and are the weakest input. Where a rule needs a fact the data does not hold, the place gets the cautious outcome and a row in `outputs/gaps.csv`.

Not applied, because the facts are missing everywhere: the settling rule's attribution (who holds an area and since when), and the two-part test for entry rules (a top-level unit, or a detached place with a rule of its own). Places that depend on them are listed as regions with an open point.

## Result

| | Count |
|---|---|
| Regions | 322 |
| — ISO 3166-1 entries | 249 |
| — from an entry rule (candidates) | 42 |
| — registry cells where points of view differ | 16 |
| — residents test (islets, paper claims, zones with no single holder) | 12 |
| — unclaimed land | 3 |
| Regions with nothing open | 258 |
| Special places | 95 |
| Markers | 141 |
| Missing facts | 193 |

Missing facts, by what is missing: a tie from a paper claim to a registry cell, or confirmation that no supported point of view shows it (38); whether a unit with its own entry rule is top-level (29); who holds a contested area and since when, any act ending the contest, its UCDP conflict (28); for areas held by another party, a stated outline or entry rule, or confirmation that the line still moves (19); entry rules not confirmed in force (18) or without a start date (15); whether a leased area has its own entry rule (10); whether an island's rule is its own (10); whether civilians live there (9); registry cells with no register area (7); entry rules with no cited source (6); areas with no kind (3).

## Conclusion

A draft list, not a canon.

1. *Facts first.* Of 73 regions that do not come from an ISO entry, 64 have an open point. The next step is collecting the named facts, not geometry.
2. *Count.* 322 against the first draft's 304; the difference is not meaningful while 42 entry-rule regions are candidates that the two-part test has not been applied to.
3. *Accepted constraints.* D004 and D005 hold through ISO entries, D006 through the registry cell for Crimea, D007 through the ISO entry for Western Sahara and the registry cell for the part Morocco administers.
4. *The two lists do not line up yet.* Only 34 of 210 register areas are tied to anything, and 7 of 29 registry cells have no register area. They have to be reconciled before a release.

## Second run, 2026-10-03: with the facts the first run asked for

Two collections were added the same day, each fact with a quoted passage: who holds 29 contested areas and since when (now in the register, passages re-opened and found), and what the texts of 43 entry rules say (`inputs/entry_rule_facts.csv`; the collectors' own check found every passage, they were **not re-opened here**).

| | First run | Second run |
|---|---|---|
| Regions | 322 | 315 |
| — from an entry rule | 42 | 34 |
| Regions with nothing open | 258 | 279 |
| Special places | 95 | 94 |
| Missing facts | 193 | 127 |

- Entry rules that no longer make a region: places that are neither a top-level unit nor a detached place with a rule of its own (Kish, Qeshm, Matsu, the Chittagong Hill Tracts), and rules found not in force (Rason, north-east Syria, Russia's former regional e-visas).
- Five contested areas are recorded with a moving line (the four occupied Ukrainian oblasts and Israeli-held southern Syria): no region, a flag on the regions they touch.
- Still open: ties from paper claims to the registry (38); the UCDP conflict for each contested area, without which quiet years cannot be counted (27); start dates of entry rules (11); entry rules of leased areas (10); residents (9); registry cells with no register area (7).

Points raised by the texts and settled by the owner the same day:

- A rule only for residents of a neighbouring area is not a witness (`inputs/not_a_witness.csv`: the Chukotka–Alaska arrangement, the Ceuta and Melilla exemption). After this the run gives 312 regions, 31 of them from an entry rule.
- A rule under which a place can be reached only through a tour operator is a witness: it closes the place to an independent visitor (Socotra, Baikonur). The Socotra passage is an operator's page and needs a better source.
- Not an open point: the federal list names the whole Chukotka okrug, so its permit covers a whole top-level unit.
- Still unsourced: Zanzibar's own immigration check (only its insurance was found).

## Third run, 2026-10-03: quiet years and small map features

- `data/disputed-areas/ucdp-links.csv` ties 29 contested areas to UCDP conflicts by territory name; with the holder's start year the settling rule's clock (three quiet years) now runs, using the code of the [settling-rule back-test](../settling-rule/README.md). Examples: Northern Cyprus accepted 1977, Crimea 2017 (active conflict), Kosovo 2002, South Ossetia 2011.
- `inputs/links.csv` now also ties register areas to the twenty Natural Earth features under 100 km² that the first draft set aside, so the residents test applies to them. A paper claim that corresponds to no feature of the pinned edition is a marker; that reading rests on matching names, not on a source.

Result: 316 regions (285 with nothing open), 95 special places, 60 missing facts. Left: areas held by another party with neither a registry cell nor an entry rule (14); start dates of entry rules (11); residents (10); entry rules of leased areas (10); five registry cells with no register area (two in eastern Ukraine, one in Bhutan, two small ones in India).

Weak points of this run: the ties to conflicts and to map features are judgements by name; several `holder_since` values hold no single year or a contested one (see the register's review list), and the clock is only as good as they are.

## Fourth run, 2026-10-03: the remaining gaps

Two more collections (residents and access for register areas; start dates and current force of entry rules; Hainan checked in full), the five loose registry cells tied to register areas, and two readings applied:

- An area held by another party with neither a registry cell nor an entry rule of the holder stays inside its region, marked, under "no witness, no boundary".
- For an area held by another party, the holder's own entry rule is the witness; the test for units of one country (top-level, or detached with a rule of its own) is not applied to it. The owner confirmed this reading the same day; it makes Transnistria and Kinmen regions.

Result: 316 regions, 296 with nothing open; 90 special places; 20 missing facts: start dates of eight long-standing entry rules (Tibet, Galápagos, Mount Athos, Minicoy, Kurdistan, Labuan, Tristan da Cunha, Gorno-Badakhshan), whether two rules are in force (Nakhchivan, Labuan), access to four leased sites, residents of two areas, the kind of two areas, and who holds two areas since when. The collectors ran out of web searches; these need another pass.

The entry-rule passages were checked by their collectors only, not re-opened here.

## Fifth run, 2026-10-03

A last collection found 13 of 22 remaining facts (start dates of the rules for Mount Athos, Tristan da Cunha, Galápagos, Labuan and Kurdistan; Labuan and Nakhchivan in force; holders of the Bhutanese enclaves; residents of the Ilemi Triangle and the Tort-Kocho road; the kind of the armistice lines). One passage (since when Kafia Kingi has been held) was not found on re-check and was dropped.

Result: 317 regions, 302 with nothing open; 90 special places; 11 missing facts, none of which changes whether a place is a region: access to four leased sites (kept as special places), start dates of three long-standing rules (Tibet, Gorno-Badakhshan, Minicoy), residents of one area, the kind of Doi Lang, and since when Kafia Kingi has been held.

The list of entry rules is still the one-off census of 116 rows; a scripted discovery of rules is being built in `data/entry-rules/`.

## Sixth run, 2026-10-04

- Nine of the last ten facts found, one dropped on re-check; two facts remain missing (access to the Tomb of Suleyman Shah; since when Kafia Kingi has been held, where the holder itself is in doubt).
- The scripted discovery in `data/entry-rules/` read 183 visa-policy articles and gave 432 candidates; after triage, four rules the census lacked were checked against their texts and added to the census (`experiments/stage1-world-draft/inputs/crw_scopes.csv` now serves as the living census; that experiment's own outputs are unchanged). One of them makes a region: Macquarie Island (a detached island with a rule of its own). The others do not: Ashmore and Cartier (the rule covers zones, not the whole territory), Kwajalein (US defence sites only), Punjab and Kerala (a visa-on-arrival exclusion that is no longer in force).
- A census row marked as not covering a whole unit no longer separates even when its checked facts would allow it.

Result: 322 regions, 309 with nothing open; 87 special places; 2 missing facts.

Correction the same day: two register areas inside Antarctica (the overlapping Peninsula claims and Marie Byrd Land) had come out as regions; Antarctica is one cell (D040). The list build now treats any area tied to an ISO entry the same way instead of naming four areas in its code. After the correction: 320 regions, 307 with nothing open.

## Correction, 2026-10-04: leased areas

The list build had treated a leased area as a region whenever access to it was restricted or closed. R053 asks for an entry rule of its own, and a closed or fenced site is not one (a closed military site is an object inside its region, R056). The owner spotted the result in the Port of Hamburg's Czech lots. Now a lease is a region only with a recorded entry rule that is a witness: Baikonur. Moldauhafen, the Russian ranges in Kazakhstan, Tiwinza, Diego Garcia and Guantanamo Bay are special places; for Guantanamo no entry rule is recorded yet. After the correction: 315 regions, 302 with nothing open, 92 special places, one missing fact.

## Leases under D057, 2026-10-04

The owner replaced R053's test: a lease is a region when its holder is a state other than the lessor (D057). Holders of the eleven leases were collected with sources and are in the register; `inputs/lease_holders.csv` reads each as lessor, lessee, split or shared, with the register's holder as basis. Regions now: Baikonur, Guantanamo Bay (the United States inside the base), the Palanca road section (Ukraine) and the Tomb of Suleyman Shah (Turkish troops); Akrotiri and Dhekelia stay regions through the registry. Special places: Moldauhafen, Saimaa Canal, Diego Garcia (inside its ISO entry) — held by the lessor; Tin Bigha (shared); the Russian ranges (split); Tiwinza (holder dropped on re-check).

Result: 319 regions, 306 with nothing open; 88 special places; 2 missing facts.

## Leases under D058, 2026-10-04

The owner added the residents test to leases (D058): a lease held by the lessee is a region only if civilians live there. Baikonur and Guantanamo Bay stay regions; the Palanca road section and the Tomb of Suleyman Shah become special places. The register's `inhabited` value for Guantanamo Bay was corrected from `garrison_only` to `yes`: its own passage counts "civilian employees, and family members" among about 6,100 residents.

Result: 317 regions, 304 with nothing open; 90 special places; 2 missing facts.

Correction the same day: Varosha had come out as a region (a zone with no single holder) because the register recorded it as `own_regime` from a UN resolution calling for UN administration. Its own passage says it is under the control of Northern Cyprus; it is re-kinded and now stays, marked, inside the land Northern Cyprus holds. Result: 316 regions, 303 with nothing open; 90 special places.

## Line disputes under D063, 2026-10-04

The owner extended the residents test to line disputes (D063): where a supported point of view puts the area between the lines in another country and civilians live there, it is a region. Demchok, Kalapani (415 km² between Nepal's 2020 line and India's; villages Gunji, Kuti, Nabi) and Rincón de Artigas become regions. `inputs/links.csv` gains a `pov_feature` column (the Natural Earth feature whose points of view differ, for Kalapani); Dragonja's link to Natural Earth's pre-2017 feature is dropped because the award line and Croatia's line coincide on land. `inputs/no_outline.csv` keeps Rukwanzi–Semliki and the Dniester Security Zone special places (R047).

Result: 317 regions, 304 with nothing open; 89 special places; 3 missing facts (none changes whether a place is a region).

## Points of view from claims, under D064-D069, 2026-10-04

Natural Earth's points of view are now a lead (D065): whether an area's points of view differ is read from `inputs/claims.csv`, which reads the register's own facts (parties, holder, on the ground) into the codes of the holder and of the parties that claim the area — ISO 3166-1 countries, Kosovo, and the de facto states that are regions (D069); a claim counts until renounced by an act in force (D068) and may rest on a secondary source (D067). The reading was drafted by an agent from the register only, every `basis_text` checked to occur verbatim in the cited fact, and reviewed: leases do not set the sovereign lessor against the lessee (Baikonur, Russian ranges, Guantanamo, Tiwinza, Palanca road), and the Sahrawi Republic is not coded as EH. 140 rows note something unclear, mostly a holder the facts do not name.

Code changes: a claim of a party other than the holder replaces the Natural Earth cell in every branch; a claim to a whole ISO 3166-1 entry changes only whose it is under the claimant's view, while a part of an entry separates when one party other than the entry's holder holds it (`entry_holder` in `inputs/links.csv`; Antarctica stays one cell); an area that is part of another register area with the same holder and claims goes with that area (`part_of`: Bender, Varosha, Strovilia, Kokkina); a claim on a lease takes the residents test (D058). `outputs/natural_earth_lead.csv` lists where Natural Earth and the claims disagree.

Result: 345 regions (28 more than before: Essequibo, Halayib, Abu Musa, Sabah, Junagadh, KaNgwane and Ingwavuma, Moldovan-held left-bank villages, Eastern Ossetia claim, Sool-Sanaag-Cayn, Heglig, occupied areas such as Artsvashen, Karki, the Gazakh exclaves, Ghajar, Israeli posts in southern Lebanon, Kafia Kingi, and ten inhabited line disputes); 98 special places; 115 markers; 13 missing facts. Natural Earth separates six areas no recorded claim supports (Bir Tawil, the Cyprus buffer zone and Guantanamo, which are regions by other rules; Hans Island, Nagorno-Karabakh, Tiran and Sanafir); Western Sahara west of the berm separates as a part of an ISO entry held by Morocco. The new regions still need outlines the parties state (R047) and bindings to the substrate; until they have them they are not in the release.

Outlines for the new regions, 2026-10-04: three agents searched the ranked sources for each of the 28 (proposals checked and entered in `data/custom-geometries` and `experiments/gadm-binding/inputs/reviewed.csv`). Thirteen have a stated outline (Essequibo, Junagadh, Abu Musa, La Güera, the Moldovan-held left-bank communes, Kafia Kingi, Artsvashen, Karki, the Gazakh exclaves, Ghajar, Ankoko, the Lawa headwaters, Tigri); Halayib already had one. Twelve have none and become special places under R047 (`inputs/no_outline.csv`): Isla Santa Rosa, Naktuka, Kpeaba, the Okpara villages, Three Pagodas Pass, Yenga, KaNgwane and Ingwavuma, the Eastern Ossetia claim, Sool-Sanaag-Cayn, Heglig, and the Azerbaijani-held border areas of Armenia. The Israeli-held area in southern Lebanon is a flag, its line still moving (R049). The Philippine claim covers the whole of Sabah (Republic Act 5446, section 2), which is already the region `rule/my-sabah`: that region carries the claim as the Philippines' point of view (`part_of`). Migingo stays a gap: its holder is unclear. Holders were added to the register for Naktuka and the Lawa headwaters. Result: 332 regions.

Pressed claims under D070 and D071, 2026-10-05: a paper claim with residents is a region only if the claimant took official steps in at least two distinct years of the last ten (`experiments/claim-activity/inputs/steps.csv`). Olivenza and the Ilemi Triangle become special places; Heglig, Noktundo and the Libyan claims were special places or notes already. Result: 330 regions in the list (329 in the release, Saint Helena's entry having no land of its own).

## Status

Running again under D064-D069 (2026-10-04): points of view from claims; outlines of the new regions pending.
