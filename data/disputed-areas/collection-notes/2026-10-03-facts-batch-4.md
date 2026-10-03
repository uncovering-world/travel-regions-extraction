# Batch 4 — sourcing notes (read 2026-10-03)

170 rows for 35 areas in `out-4.csv`. Every area has `parties` and `kind`; no area is empty. Every quote was cut by script (`build4.py`) out of a page saved in this session; nothing was typed from memory. The lead columns were used only to decide which pages to open.

## Sources used

| Source | Rows | Evidence | Remark |
|---|---|---|---|
| English Wikipedia, pinned revisions | 135 | secondary | 45 pages |
| German / French Wikipedia, pinned revisions | 5 | secondary | 3 pages: Moselle condominium, Moldauhafen, France–Vanuatu boundary |
| CIA World Factbook, "Disputes - international", via the `factbook/factbook.json` mirror pinned to commit `588c5b5084ee9c5e7ed0666c7be8f692c0329f56` | 19 | secondary | 16 country entries. **Snapshot of 2023-05-25**: statements are more than three years old. The CIA's own page was not opened; the mirror is a third-party copy |
| gov.uk foreign travel advice (Mayotte, Azerbaijan, North Korea, Cyprus) | 4 | primary | Official text, but of a third government, not of the administering authority |
| canada.ca (Machias Seal Island Migratory Bird Sanctuary) | 2 | primary | Administering authority |
| doi.gov and fws.gov (Navassa) | 3 | primary | Administering authority |
| senat.fr (French government's explanatory statement on the Saint-Martin border agreement, 25 February 2026) | 2 | primary | Party to the agreement |

Read but not quoted: 11 further gov.uk pages (Ukraine, Moldova, France, Spain and others); the French National Assembly's legislative file on the Saint-Martin agreement; 38 further Wikipedia pages and 30 further Factbook entries. All fetched pages are in `pages/` (official pages and Factbook entries carry the prefix `b4_`); `fetchlog-4.txt` maps each saved file to its URL; `b4pages/` keeps a private copy of each Wikipedia page keyed by revision id.

Could not be fetched as text and therefore not used: UN Security Council resolution 1680 and the UN press release on it (bot challenge on press.un.org and docs.un.org); the ICJ judgment of 19 May 2025 (PDF only; the case page lists documents without stating the outcome); the official English text of the Republic of Korea's constitution (script-rendered sites).

## Self-check

`selfcheck4.py`:

- **Check A (the required one)**: quote, whitespace-normalised, is a substring of the saved page text of its `source_url` and of the private copy of the cited revision; at least 15 characters; within one paragraph; allowed values; one row per (area, field). Result: 170 rows, 0 failing, **0 dropped**.
- **Check B (extra)**: re-opens every `source_url` the way `data/disputed-areas/verify_quotes.py` does and applies its `squash()`. Result after rework: 0 not found.

**Finding for the whole register, not only this batch.** `fetch_page.py` removes footnote markers with `\[\s*\d+\s*\]`, but `verify_quotes.py` removes only `\[\d+\]`. In the HTML the marker is `[ 12 ]` with spaces, so the verifier keeps it. A quote that runs across a footnote marker therefore passes a check against the helper's text and is reported "not found" by `verify_quotes.py`. In the first build of this batch 24 of 170 rows were affected; I re-cut them so that no quote crosses a marker (which is why some quotes are a single sentence or a clause). Quotes in other batches that span two sentences are likely to hit the same problem. The repository was not touched.

## General limits

- `traveller_access` is sourced for 9 areas only, `inhabited` for 15, `area_km2` for 17. Where a page did not state it, the field is absent.
- `area_km2` values converted from the source's unit: Machias Seal Island 8 ha, Mbanié 30 ha, Migingo 2,000 m², Moldauhafen 28,500 m², Mont Blanc 65 ha + 10 ha (sum of two figures in one sentence). Libyan claims are "about" figures.
- Infobox fragments (short, but verbatim): Machias `area_km2`, Matthew and Hunter `area_km2`, North Korea `inhabited`, Northern Cyprus `parties` and `inhabited`, Olivenza `inhabited`, Paracel `inhabited`.
- Rows quoted from "List of territorial disputes" are table cells. The O'Tangav cell names the area and Stung Treng Province but not Laos; Laos stands in the neighbouring "claimants" cell, which is too short to quote.
- **The kinds changed while this batch was running.** The task said "nine kinds"; commit `65d6f03` (2026-10-03, 15:50) added a tenth, `unclaimed`, to UPDATING.md and `build.py`, and narrowed `no_agreed_boundary` to stretches where a boundary must exist between states that each hold territory on their side. I followed the file as it now stands: Marie Byrd Land is `unclaimed`; the two Lebanon–Syria areas stay `no_agreed_boundary` and fit the narrowed definition. If the merge expects only nine kinds, that one row is the exception.

## Per area

**lebanon-syria-undelimited** — not sourced: `inhabited`, `traveller_access`, `area_km2`. Lead confirmed (`no_agreed_boundary`). `parties` rests on the 2023 Factbook. The Wikipedia article on resolution 1680 (2006) says the Council encouraged Syria to answer Lebanon's request to delineate the common border; no later demarcation agreement appears on the pages read. `on_the_ground` is about clashes in early 2025, not about who administers which section.

**libya-algeria-claim** — not sourced: `origin`, `on_the_ground`, `inhabited`, `traveller_access`. The only source is the 2023 Factbook (entries for Algeria and for Libya, same wording, "dormant"). The Wikipedia pages "Algeria–Libya border", "Algeria–Libya relations", "Foreign relations of Libya" and "Foreign relations of Algeria" do not mention the claim at all. Weakly sourced; whether Libya still shows the claim on its maps is unverified.

**libya-niger-tummo** — not sourced: `origin`, `on_the_ground`, `inhabited`, `traveller_access`. **Sources contradict each other and the lead.** Factbook, Niger entry: Libya claims about 25,000 sq km in the Tummo region, dormant. Factbook, Libya entry, same snapshot: "the boundary is poorly defined but has never been disputed by either country". Wikipedia "Foreign relations of Niger": Libya "has in the past claimed" about 19,400 km². `area_km2` = 25000 follows the Factbook because it names Tummo; 19,400 is the other figure. "Libya–Niger border" says a 1955 Franco-Libyan treaty recognised the existing boundary and does not mention a claim. This may not be a live dispute.

**logoba-moyo** — not sourced: `inhabited`, `traveller_access`, `area_km2`. Lead confirmed. The `on_the_ground` sentence is undated; its paragraph runs from 2005 to a presidential meeting of November 2010 with no agreement, and nothing later is given for this place. The 2023 Factbook lists "South Sudan-Uganda: none identified". The relations page also reports a clash on 27 October 2020 near Pogee, Magwi County — a different stretch of the same border.

**luhansk-occupied** — not sourced: `traveller_access`, `area_km2`. Lead confirmed. "Russian occupation of Luhansk Oblast" redirects to "Luhansk People's Republic". The oblast's area (26,684 km²) is on the page but is not the area of the occupied part, so it was not entered. The sentence after the `on_the_ground` quote says the claim of full control was repeated in April 2026 and denied by Ukraine. gov.uk says entering Ukrainian territory through a crossing not controlled by Ukraine is illegal under Ukrainian law and lists "all land border crossings and seaports in Luhansk region"; that is the claimant's rule, not an entry regime of the controlling authority, so no `traveller_access` was entered. `inhabited` rests on a December 2017 figure.

**lunkinda-pweto** — not sourced: `inhabited`, `traveller_access`, `area_km2`. Lead kind kept (`line_position`: different readings of the 1894 treaty). **Contradiction:** the Chiengi article says the Lunchinda enclave was "eventually … ceded to DR Congo by Zambia", which would end the dispute; the 2023 Factbook says a boundary commission "continues discussions" and Zambia claims the triangle; the Wikipedia list keeps it as ongoing and adds that Zambia deployed troops on the Congolese side in March 2020. The "Luapula Province border dispute" article carries several maintenance banners (more citations needed, may need rewriting, may be confusing). The list has two rows (Chiengi / Lunchinda-Pweto; right bank of the Lunkinda River); the sources describe one triangle, so one area seems right.

**machias-seal-island** — all fields sourced. Lead kind kept (`paper_claim`): both sides argue from treaties and occupation. The page also says the dispute began in 1971 with a US protest against Canadian maritime jurisdiction and that the island lies in the lobster "grey zone", so `islets_for_maritime_zone` is a defensible reading. `inhabited` = `garrison_only`: the only residents are two rotating Canadian Coast Guard lightkeepers (civilian staff, kept there "for sovereignty purposes" according to the page). `traveller_access` = `restricted` from the Canadian government page: permission must be sought from Fisheries and Oceans Canada; entry is forbidden in June and July except through two permitted tour operators. Wikipedia adds that Canada does not enforce border law on American visitors. North Rock is not covered by any figure.

**margherita-peak** — not sourced: `origin`, `inhabited`, `traveller_access`, `area_km2`. Lead confirmed. Both rows rest on one sentence of the 2023 Factbook, which the Wikipedia list repeats word for word. The "Mount Stanley" article does not mention a dispute and calls the mountain the highest of both countries. `on_the_ground` describes the range, not the summit.

**marie-byrd-land** — not sourced: `inhabited`, `traveller_access`. **Kind differs from lead** (`no_agreed_boundary` → `unclaimed`) only because UPDATING.md now has a separate kind for land no state claims; the page calls it "an unclaimed region of Antarctica". The page says Marie Byrd Land stretches from 158°W to 103°24'W, that the part west of 150°W belongs to the Ross Dependency claimed by New Zealand, and that the 1,610,000 km² figure for the unclaimed territory includes Eights Coast "immediately east of Marie Byrd Land". The limits 90°W–150°W in the area name were not found on the page read. No passage says outright that there is no permanent population; the page mentions a US station reopened in 2009–2010, a summer camp and a closed Russian station.

**matthew-hunter** — not sourced: `traveller_access`. Lead confirmed. `kind` rests on a sentence of French Wikipedia (the dispute matters for Vanuatu's exclusive economic zone); the English article gives no motive. The 2023 Factbook adds a French naval landing in January 2019 and tension over French fishing vessels in November 2021. The two islands lie 70 km apart.

**mayotte** — all fields sourced. Lead confirmed. `kind` quotes the Factbook's Comoros entry, whose subject (Comoros) is implied by the entry. Wikipedia's sentence "Comoros continues to claim the island" carries a "needs update" tag; the `parties` row uses a different sentence. `traveller_access` = `open` from gov.uk (visa-free visits for British nationals).

**mazraat-deir-al-ashayer** — not sourced: `origin`, `traveller_access`, `area_km2`. **Kind differs from lead** (`line_position` → `no_agreed_boundary`): the village article says there is "no fully formalized border demarcation" here and speaks of overlapping claims; no source shows an agreed line whose position is disputed. The Wikipedia list's own wording (administered by Lebanon, claimed by Syria) would read as `paper_claim`. The list places the village in Lebanon's Zahlé District, the article in Rashaya District. The article describes two adjoining villages of the same name, a Lebanese one (about 1,100 inhabitants, 26 km²) and a Syrian one "also known locally as Mazraat Deir al-Ashayer", so it is unclear which of them the list means; 26 km² was not entered. This area is a named instance of `lebanon-syria-undelimited`.

**mbanie** — not sourced: `traveller_access`. Lead confirmed (`resolved_recently`, ICJ, 19 May 2025). Whether Gabon has withdrawn its soldiers and handed the islands over is not stated on the pages read. `area_km2` = 0.3 is Mbanié alone; Conga and Cocoteros are not measured. The judgment itself was not opened (PDF), so nothing is `primary`.

**mekong-islands** — not sourced: `on_the_ground`, `inhabited`, `traveller_access`, `area_km2`. Lead kind kept. Both rows rest on the 2023 Factbook ("as of 2018" in the Laos entry). No source names the islands or says who holds them. Wikipedia says a 1926 convention settled the islets and that demarcation was still under way in 2018.

**melilla** — all fields sourced. Lead confirmed. `traveller_access` = `open` rests on scheduled ferry and air links (Wikipedia); the same page says movements between Melilla and the rest of the EU follow specific Schengen rules, and gov.uk's entry-requirements page for Spain says nothing about Melilla. Wikipedia mentions that Morocco closed the customs office at the border in 2018.

**migingo** — not sourced: `traveller_access`. Lead kind kept. **Sources contradict each other on whether Uganda still claims the island.** Wikipedia: Uganda began to claim it in 2008; a joint survey in 2009 found the island 510 m on the Kenyan side; Uganda's government then said the island was Kenyan but nearby waters Ugandan, lowered its flag and withdrew. 2023 Factbook: "Uganda and Kenya both claim Migingo Island", joint demarcation begun in 2021. The Wikipedia list keeps it as ongoing, together with Lolwe, Oyasi, Remba, Ringiti and Sigulu, about which nothing was found. If Wikipedia is right, the island question was settled in 2009 and only waters remain in dispute. `inhabited` and `area_km2` are for Migingo alone and date from 2009.

**minerva-reefs** — not sourced: `inhabited`, `traveller_access`, `area_km2`. Lead confirmed. The page calls the reefs "two submerged atolls" used as anchorages by private yachts; it does not say "uninhabited" or state an entry rule, so both fields are absent. It reports a Tongan offer of July 2014 to trade the reefs for the Lau Group, with no outcome.

**moldauhafen** — not sourced: `inhabited`, `traveller_access`. Lead kind kept, with a caveat: the page says the lease "now has the character of a private contract" between the City of Hamburg and the Czech Republic, so there may be no foreign jurisdiction at all, which the definition of `lease_or_base` requires. The lease ends in 2028; Hamburg plans a new district on the site and talks about a replacement site are under way (German Wikipedia). Area: 28,500 m² for Moldauhafen and Saalehafen (English page), 30,000 m² (German page). Peutehafen, which was bought and not leased, is outside the figure.

**moldovan-held-left-bank** — not sourced: `traveller_access`, `area_km2`. Lead kind kept. **Possible split and overlap.** Varnița and Copanca lie on the west bank according to the page, so "left bank" fits only the Dubăsari villages; the list has two rows. All these places lie inside the security zone under the Joint Control Commission, which the register holds as a separate area; by the tie-break rule a distinct regime would outrank the paper claim. The Cocieri article says the commune can be reached from Moldova proper only by ferry and that Transnistrian checkpoints charge fees on the roads out. `inhabited` rests on Cocieri alone.

**mont-blanc-summit** — not sourced: `inhabited`, `traveller_access`. Lead confirmed. **Possible split:** the page names two distinct disputed areas (Mont Blanc 65 ha, Dôme du Goûter 10 ha); the Col du Géant is a third place with a similar dispute, described in its own article in a section tagged as citing no sources. `area_km2` = 0.75 covers the first two only.

**moselle-condominium** — not sourced: `inhabited`, `traveller_access`, `area_km2`. Lead confirmed. Area was not entered because the German page gives two partial figures in different paragraphs: 6.20–6.21 km² for the Rhineland-Palatinate part and 103 ha for the Saarland part. The condominium covers bridges and about 15 river islands; the Grevenmacher and Stadtbredimus locks are excluded. The 1984 border treaty was not opened.

**nagorno-karabakh** — not sourced: `inhabited`. Lead confirmed. The page says almost the entire Armenian population was removed; no current population figure. `traveller_access` = `restricted` rests on gov.uk: visiting Khankendi and neighbouring areas "without the permission of the Azerbaijani authorities" can lead to refusal of entry; gov.uk also advises against all but essential travel to these districts. `area_km2` is the former autonomous oblast.

**navassa** — all fields sourced. Lead confirmed. `traveller_access` = `closed` from the administering agency ("closed to the public"); Wikipedia says visitors need the agency's permission and records a permit for a radio expedition in 2015, which would read as `restricted`. Area: 5.4 km² (Wikipedia); the Department of the Interior page says "three square miles". Haitian fishers camp on the island.

**nepal-china-humla** — not sourced: `inhabited`, `traveller_access`, `area_km2`. Lead kind kept. **Sources differ on the facts:** the 2023 Factbook says China "may have constructed 11 buildings in Nepal's Humla region in 2021"; Wikipedia says a leaked Nepali report found the buildings on the Chinese side, but a fence round a border pillar and an attempted canal and road on Nepali soil. Wikipedia adds that Nepal's government tends to deny or play down disputes with China. "More than 150 ha" is a politicians' claim, not an area. Lapcha is not named in the dispute passages.

**noktundo** — not sourced: `inhabited`, `traveller_access`. Lead confirmed. Single short article.

**north-korea-claimed-by-rok** — all fields sourced. Lead confirmed. In `parties`, "North Korea (administers)" is carried by the neighbouring sentence, quoted under `on_the_ground`; a footnote marker between the two sentences prevented one quote. The constitution is quoted through Wikipedia, not from an official text. The list's settled table says North Korea dropped its own claim to the South in 2026; that is the mirror dispute and does not change this row. `traveller_access` = `restricted`; gov.uk also says the borders have been closed to general entry since 2020, with limited tourism restarting.

**northern-cyprus** — all fields sourced. Lead confirmed. `de_facto_state` and `occupied_or_annexed` both fit the page's wording; chosen by what a visitor meets. `traveller_access` = `open` from gov.uk (any crossing point may be used); the same page says the Republic of Cyprus treats entry through the north as illegal entry.

**ntem-island** — not sourced: `origin`, `on_the_ground`, `inhabited`, `traveller_access`, `area_km2`. Lead kind kept, weakly. The only source is the 2023 Factbook, which calls it a "sovereignty dispute … over an island". The island is not named, and who holds it is not said. No Wikipedia article on the Cameroon–Equatorial Guinea border exists.

**okpara-villages** — not sourced: `on_the_ground`, `traveller_access`, `area_km2`. Lead kind kept, weakly. One stub sentence states the dispute; the villages are not named. The 2023 Factbook lists "Nigeria-Benin: none identified" and its Benin entry does not mention the villages. This may not be a live dispute.

**olivenza** — not sourced: `traveller_access`, `area_km2`. Lead confirmed. The infobox area (430.1 km²) and population (11,742) are for the municipality of Olivenza alone; Táliga is separate, so no area was entered. The stretch of border here is undemarcated, with the Guadiana as the de facto border.

**orange-river-boundary** — not sourced: `inhabited`, `traveller_access`, `area_km2`. Lead confirmed. The 2023 Factbook agrees with Wikipedia and adds that the 1994 Surveyors-General agreement was never signed or ratified and that the line may affect diamond mining rights. `on_the_ground` lists the crossing points; no source says how the river itself is policed.

**otangav** — not sourced: `on_the_ground`, `inhabited`, `traveller_access`, `area_km2`. Lead kind kept, weakly. The name O'Tangav appears only in the list's table cell; no article describes the place. **Possibly resolved:** the border page says Cambodia and Laos signed a border demarcation treaty on 13 February 2023 and have since been installing markers; it does not say what this means for O'Tangav. The 2017 incident quoted for `kind` is not tied to O'Tangav by the page.

**oyster-pond** — not sourced: `inhabited`, `area_km2`. Lead confirmed, with a caveat: the agreement was concluded on 26 May 2023 but was not yet in force. Wikipedia: the French National Assembly approved ratification on 16 July 2026 and the Netherlands had still to ratify. The National Assembly's file (read, not quoted) shows French Law no. 2026-645 of 22 July 2026. The Wikipedia list still says, "as of July 2026", that neither government had approved. Dutch ratification was not checked. The French text says the Netherlands claimed the whole pond and France half.

**palanca-road** — not sourced: `inhabited`, `traveller_access`, `area_km2`. Lead kind kept, with a caveat: the page says both that Moldova undertook in 2001 to transfer "control and sovereignty" and that in 2012 the road became "property of Ukraine within the territory of Moldova". Which holds is not settled by this source; the treaty was not opened. Length 7.7 km; no area.

**paracel-islands** — all fields sourced. Lead kind kept; the census itself noted it could be `paper_claim`. The body sentence on residents carries a "failed verification" tag, so `inhabited` rests on the infobox ("Over 1,000 (2014)"). `traveller_access` = `restricted` describes Chinese tourists applying for a cruise; nothing is said about foreigners.

## Duplicates, overlaps and splits

- `mazraat-deir-al-ashayer` lies inside `lebanon-syria-undelimited`.
- `moldovan-held-left-bank` lies inside the Dniester security zone and joins two separate groups of villages on opposite banks.
- `mont-blanc-summit` covers three places.
- `migingo`, `mbanie`, `matthew-hunter` and `machias-seal-island` each name several islands; figures cover only the main one (Matthew and Hunter: both).
- Possibly not live disputes: `libya-niger-tummo`, `okpara-villages`, `migingo` (island itself), `lunkinda-pweto`, `otangav`.
