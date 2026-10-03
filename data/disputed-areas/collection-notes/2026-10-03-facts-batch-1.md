# Batch 1 — sourcing notes (read 2026-10-03)

All 158 rows rest on English Wikipedia at pinned revisions (`evidence=secondary`). No official page was fetched in this pass, so no row is `primary`. Every quote was cut by script out of the saved page text (`build_out1.py`), and re-checked by `selfcheck_out1.py`: 0 rows failed, 0 dropped.

General limits of this pass:

- `traveller_access` is sourced for only four areas (Akrotiri and Dhekelia, Arunachal Pradesh, Baikonur, Ceuta). Wikipedia rarely states entry rules; these need the administering authority's pages.
- Several quotes are infobox fragments (short, but verbatim): Abkhazia `kind`, Aksai Chin / Arunachal / Ceuta / Chagos `area_km2`, Arunachal / Badme / Baikonur / Banc du Geyser / Conejo `inhabited`, Latrun and Conejo `parties`.
- Rows quoted from "List of territorial disputes" are table cells; the cell alone does not always name the area or the parties (see Bosnia–Serbia).

## Per area

**abkhazia** — not sourced: `traveller_access` (the page only says many governments advise against travel, which is not an entry rule). Lead confirmed.

**abu-musa** — not sourced: `traveller_access`. Lead confirmed. The page also says the island is "a possible US military objective in the 2026 Iran war" — on-the-ground status may be changing; re-check.

**abyei** — not sourced: `inhabited` (only historical statements about residents), `traveller_access`. Lead confirmed; the page calls it "effectively a condominium".

**akrotiri-dhekelia** — all fields sourced. `kind=lease_or_base` rests on "retained by the British under the 1960 treaty"; note it is retained sovereignty, not a lease — the kind's definition ("by lease or treaty") covers it only through the treaty. Cyprus's position is recorded as contesting the extent of UK sovereignty, not as a territorial claim.

**aksai-chin** — not sourced: `traveller_access`. `inhabited=yes` rests on "sparsely populated region with few settlements"; the same page calls it "nearly uninhabitable". Area is the infobox figure (38,000 km²).

**al-fashaga** — not sourced: `area_km2`, `inhabited`, `traveller_access`. **Kind differs from lead** (`line_position` → `paper_claim`): the page shows Sudanese administrative control with an Ethiopian claim and says Ethiopia never signed a treaty with Sudan over the territory; it does not show that both sides agree a line exists. The page is a stub; the "Al-Fashaga conflict" article should be read before this is relied on. Lead's "Sudan controls most since 2020" is only partly shown (Sudan expelled farmers and took Khor Yabis in 2020).

**ankoko-island** — not sourced: `area_km2`, `inhabited` (a military base and an airport are mentioned, but not whether civilians live there), `traveller_access`. Lead confirmed. Possible overlap with a wider Guyana–Venezuela (Essequibo) area if one exists in the register: the list groups "Guyana west of the Essequibo River and Ankoko Island" in one row.

**antarctic-peninsula-overlap** — only `parties` and `kind` sourced. The treaty-regime quote is about Antarctica as a whole. The sector limits 25°W–80°W in the area name are not sourced. **Likely duplicate/subset of `antarctica`**: it lies wholly inside the treaty area and has the same regime; consider keeping it only as a note on `antarctica`.

**antarctica** — not sourced: `area_km2` (the page gives 14,200,000 km² for the continent, which is not the same thing as the treaty area south of 60°S, so it was not entered), `inhabited` (the pages say "no permanent population" but 1,000–5,000 station staff; none of the three allowed values fits cleanly — decision needed), `traveller_access`. `parties` lists only the seven claimants, as quoted.

**armistice-no-mans-lands** — **no `kind`**: nothing read says how the status of these strips is regarded today, so `occupied_or_annexed` from the lead is not supported. `parties` comes from the Latrun infobox only ("Administered by Israel, Claimed by Israel and Palestine"); nothing was found for the Jerusalem no-man's-land or Mount Scopus parties. Not sourced: `area_km2`, `inhabited`, `traveller_access`. **Should be split or re-scoped**: the Mount Scopus page describes a pre-1967 Israeli exclave under UN supervision that "now lies within Jerusalem's Israeli municipal boundaries" — a different history from the Latrun no-man's-land; the three pieces do not share one set of facts.

**artsvashen** — not sourced: `traveller_access`. Lead confirmed. `inhabited=yes` rests on "the village has now been settled by Azerbaijanis", while the same page also says "largely abandoned" — internally inconsistent source.

**arunachal-pradesh** — not sourced: `origin`, `on_the_ground`. `traveller_access=restricted` rests on a sentence tagged "citation needed" in Wikipedia — raise to a primary source (Indian government permit rules). China's claim covers "nearly four-fifths", not the whole state.

**aves-island** — not sourced: `traveller_access`. Lead confirmed: the page says sovereignty disputes are "now resolved" and that the open question is island-versus-rock status. `inhabited=garrison_only` rests on the 1978 base "permanently inhabited by a group of scientists and military personnel" (past tense; current staffing not confirmed). Area 3.36 ha = 0.0336 km², with the page noting a range of 0.65–4.5 ha.

**azad-kashmir** — not sourced: `traveller_access`. `kind=paper_claim` is the nearest fit, but the page calls it "a nominally self-governing entity" not represented in Pakistan's parliament — not quite "ordinary territory of the administering state". The list row covers "Azad Kashmir and Gilgit-Baltistan" together.

**azerbaijani-held-armenian-border-areas** — not sourced: `area_km2` (the page gives a range, 50–215 km², so no single number was entered), `inhabited`, `traveller_access`. Lead confirmed.

**badme** — not sourced: `area_km2`, `on_the_ground`, `traveller_access`. **Sources disagree on whether the handover happened**: the Badme article says Ethiopia "announced plans to withdraw from Badme and cede it" (June 2018); the list of disputes says "The territory was handed over to Eritrea" and files it as resolved in 2018. `kind=resolved_recently` follows the list; actual control on the ground (also after the Tigray War) is unverified.

**baikonur** — not sourced: `area_km2` (the city infobox gives 57 km² for the city only; the area is "cosmodrome and city", so it was not entered). Lead confirmed.

**bajo-nuevo** — not sourced: `area_km2`, `traveller_access`. **Parties differ from lead**: the article's lead names Colombia, Jamaica and the United States; the infobox names only the United States as claimant; the list of disputes names Colombia, Honduras and the United States and says Jamaica and Nicaragua have recognised Colombia. Honduras's constitutional claim appears only in the list. The row records the article's own sentence; this needs a decision on which claimants to list. `kind` quote shows only that it is an uninhabited reef, not the maritime motive.

**banc-du-geyser** — not sourced: `area_km2`, `traveller_access`. Lead confirmed. The page is tagged as needing more citations.

**baqoura-ghamr** — not sourced: `area_km2`, `inhabited`, `traveller_access`. Lead confirmed (`resolved_recently`). The "full Jordanian control since 10 November 2019" quote is from the Baqoura (Island of Peace) page; for Al-Ghamr the Tzofar page only says Jordan called its decision "final and decisive" — the Al-Ghamr handover date is unverified.

**belize-guatemala-claim** — not sourced: `inhabited`, `traveller_access`. Lead confirmed. Area 12,272 km² is the Sibun–Sarstoon claim (about 53% of Belize), not Belize as a whole. ICJ oral arguments began November 2025; decision pending.

**bhutan-china-north** — not sourced: `on_the_ground`, `inhabited`, `area_km2`, `traveller_access`. Only Pasamlung and Jakarlung are named in the sources read; **Beyul Khenpajong does not appear** in them. The Doklam page gives 495 km² for a "central region" in China's 1996 offer, but does not name these valleys, so it was not entered. The page reports at least 22 Chinese villages "inside of disputed territory" without saying which sector.

**bhutan-china-west** — not sourced: `inhabited`, `traveller_access`. Area 269 km² is "the northwest … including Doklam, Sinchulumpa, Dramana and Shakhatoe" as of 1999; "western Haa" and "Sinchulung" from the area name are not named as such. `on_the_ground` covers Doklam only.

**bhutanese-enclaves-tibet** — **no `kind`**: the sources say China occupied the exclaves in 1959; none of them says Bhutan still claims them, so the lead's "residual claim" and `paper_claim` are not supported. Khochar is named only in the list of disputes; Darchen in both. Not sourced: `on_the_ground`, `inhabited`, `area_km2`, `traveller_access`. If no current claim can be sourced, this may be a candidate for `ignore` (settled in fact before 2015) rather than an area.

**bir-tawil** — not sourced: `on_the_ground`, `traveller_access`. Lead confirmed. `inhabited=no` rests on "no permanent settlements"; the infobox says "Transient populations".

**bosnia-serbia-drina** — weakest area of the batch. The only statement is the list's table cell "Sections along the Drina in dispute."; the parties stand in a neighbouring cell, not in the quote. `kind=line_position` rests on the border article describing the border as running along the Drina — it shows a border exists there, not what the disagreement is. Not sourced: everything else. The border article mentions no dispute at all.

**bukit-jeli** — not sourced: `inhabited`, `traveller_access`. Lead confirmed. Area: 42 hectares (0.42 km²).

**burkina-niger-border** — not sourced: `on_the_ground`, `inhabited`, `area_km2`, `traveller_access`. Lead confirmed, with one wrinkle: the list says the ruling was implemented in 2015 but gives the end year as 2016.

**caspian-islets-ukatny** — only Ukatny has an article; Zhestky and Maly Zhemchuzhny appear there only as nearby islands, not as disputed. Who actually administers the island is not stated ("According to Russia administratively this island belongs to the Astrakhan Oblast"). `kind=islets_for_maritime_zone` rests on "It lies in an offshore oil producing area" — thin. Not sourced: `origin`, `on_the_ground`, `inhabited`, `area_km2` (14.9 km² is Ukatny alone). The page carries a clean-up tag.

**ceuta** — all fields sourced. `traveller_access=open` rests on the description of the road checkpoint and ferries, not on an entry rule; raise to a primary source. The page reports unrest in summer 2026 after a mass border breach.

**chagos** — not sourced: `traveller_access`. **Kind differs from lead** (`paper_claim` → `occupied_or_annexed`): the page says the ICJ (2019) and ITLOS (2021) both stated the UK has an obligation to return the islands, which fits "controlled by one state, widely regarded as another's" better than "ordinary territory"; the Diego Garcia base would also support `lease_or_base` — owner's call. Lead's "Maldives (objects)" not found. Treaty signed 22 May 2025, ratification "indefinitely on hold". New: the infobox lists a "Chagossian Government (unrecognised)" as claimant, and four Chagossians settled on Île du Coin in February 2026, so `inhabited=garrison_only` is already slightly out of date.

**chile-peru-land-triangle** — not sourced: `inhabited`, `area_km2`, `traveller_access`. **Lead's "Chile (controls)" is not supported**: the page says both countries claim to patrol the area. The page gives the triangle as "37,610 km 2" — clearly an error (the figure can only be square metres), so no area was entered.

**citrana-naktuka** — not sourced: `area_km2` (1,069 ha is given for Naktuka alone; the area also covers other Oecusse segments), `traveller_access`. Status is moving: agreement in principle 2019, rejected by Timor-Leste's parliament; poles placed November 2023; treaty signing of 26 January 2024 did not happen. Nothing later than early 2024 was found. The page names a second unresolved Oecusse piece (Área Cruz, 142.7 ha, Passabe) and Batek Island — possible separate areas.

**conejo-island** — not sourced: `on_the_ground`, `area_km2`, `traveller_access`. Lead confirmed. `origin` has no year in the quoted sentence (the 1992 ICJ ruling is in the sentence before it).

**congo-river-islands** — only `parties` and `kind`. No island is named in either source; the border article says only that the river segment "is poorly defined, and has been the subject of territorial disputes". The area has no identifiable extent.
