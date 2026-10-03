# Batch 3 — sourcing notes (read 2026-10-03)

`out-3.csv`: 175 rows for 35 areas. Every area has `parties` and `kind`; no area is empty.
By field: parties 35, kind 35, origin 34, on_the_ground 33, inhabited 22, area_km2 12, traveller_access 4.
By evidence: 170 `secondary`, 5 `primary`. By source: English Wikipedia 161, German Wikipedia 4 (Lake Constance), Jeune Afrique 5 (Kpéaba, in French), International Court of Justice 3 (Isla Portillos), gov.uk travel advice 2 (Kosovo, Kherson). 55 distinct pages.

Nothing was taken from the lead columns or from memory. Every quote was cut by script (`build_out3.py`, anchors in `rows3.py`) out of the page text saved in this session, never typed.

## Checks run

- `selfcheck3.py` — the required check: each whitespace-normalised quote is inside one paragraph of the saved page text for its `source_url`. **175 of 175 pass; 0 rows dropped for failing it.**
- `e2e3.py` — the register's own `verify_quotes.py` functions (`page_text`, `squash`), re-fetching every source by its URL, cache redirected to the scratch directory: **174 found, 1 not found, 0 unreadable.**
- The one not found is `kafia-kingi / inhabited` ("Population • Estimate (2010) 16,000"): on the live page a citation marker sits between "(2010)" and "16,000".

**Defect in `verify_quotes.py` that the merge will hit in every batch.** `fetch_page.py` removes citation markers (`[ 12 ]`) from the saved text, so a quote copied from the saved text has none. `verify_quotes.squash()` removes only `\[\d+\]`, but its own tag-stripping turns a marker into `[ 12 ]` (with spaces), which that pattern does not match. Any quote that spans a marker is therefore reported "not found" although it is verbatim. Changing the pattern to `\[\s*\d+\s*\]` fixes it. Until then I chose marker-free spans for every row but the one above; the price is that some quotes are clauses, not whole sentences (listed under "Clause fragments").

Two rows were withdrawn in review as too weak, not because they failed a check: `india-china-middle-sector / inhabited` and `/ traveller_access` (see that area).

## Reading these rows

- **`primary` rows.** The three ICJ rows quote the Court's own case pages. The two gov.uk rows are marked `primary` as the task text prescribes for a government page, but they are the UK government's statement of the rules, written for British citizens, not the administering authority's own text.
- **Clause fragments** (verbatim and contiguous, cut at a citation marker): `islas-chafarinas / origin`, `/ on_the_ground`, `/ inhabited`; `indian-jammu-kashmir-ladakh / origin`; `israeli-held-southern-syria / on_the_ground` (ends mid-sentence); `israeli-posts-south-lebanon / inhabited`; `kosovo / origin`; `kosovo-montenegro-border / origin` and `/ on_the_ground` (two halves of one sentence); `kuril-islands / inhabited`.
- **Lead sentences entered from mid-sentence** (the quote starts after the article's name and its transliterations): `imia-kardak / inhabited`; `islas-chafarinas / area_km2`; `karki / kind`; `kinmen-matsu / kind`; `klek-skolj / parties` and `/ inhabited`; `kokkina / kind`.
- **Infobox fragments** (short, verbatim): `isla-santa-rosa / parties`; `isla-brasilera / area_km2`; `kafia-kingi / parties`, `/ inhabited`, `/ area_km2`; `kalapani / parties`; `karki / parties`; `kinmen-matsu / inhabited`; `koalou / inhabited`; `kokkina / parties`; `korean-dmz / traveller_access`; `kosovo / parties`; `la-guera / parties`, `/ kind`, `/ area_km2`.
- **Derived numbers.** `imia-kardak` 0.04 from "4.0 ha"; `kosovo-montenegro-border` 80 from "8,000 hectares"; `india-bangladesh-enclaves` 98.2 is the sum of the two figures in the one quoted sentence (2,880 ha + 6,940 ha).
- **Pages that Wikipedia itself flags.** "Needs more citations": Kokkina, La Güera, KaNgwane. "Neutrality disputed": Kafia Kingi. "Lacks inline citations": Lake Malawi territorial dispute. Stub: Isla Suárez.
- Sources that refused the fetch (HTTP 403) and were not used: `rfi.fr` (Kpéaba), `mofa.go.jp` (Northern Territories).
- `traveller_access` is sourced for four areas only. Wikipedia rarely states entry rules; the rest need the administering authority's pages.

## Where the sources contradict the lead

1. **`israeli-posts-south-lebanon` — the lead is overtaken by events.** The page read says Israel began a ground invasion on 16 March 2026 and "expanded its military occupation within Lebanon to a total of 570–600 square kilometers" by the April 2026 ceasefire, and that Netanyahu said on 15 June 2026 that forces will stay in "the Lebanon security buffer zone". The earlier "points" appear only in a footnote: "some 10 further square kilometers (3.9 sq mi) since 2024". The area's name and scope need a decision.
2. **`kula-kangri` — no live dispute in the sources.** "Bhutan once claimed Kula Kangri. The claim was relinquished in the 1980s, with Bhutan attributing it to a cartographic error." Settled before 2015, so `resolved_recently` does not apply and UPDATING.md's `ignore` reason ("a dispute settled before 2015") does.
3. **`kafia-kingi` — kind changed**, `paper_claim` → `occupied_or_annexed`. The page presents the area as "Country (de jure) South Sudan / Country (de facto) Sudan" and as due to go to South Sudan under the 2005 Comprehensive Peace Agreement.
4. **`lake-nyasa-islands` — administration.** The lead has Tanzania administering. The pages say "Malawi currently administers these waters"; nothing read says who runs the islands.
5. **`india-china-middle-sector` — Chumar is not in the middle sector.** The table in "Sino-Indian border dispute" places Chumar North and South in Ladakh; the middle sector is "between Uttarakhand and Himachal Pradesh".
6. **`isla-santa-rosa` — date.** The lead says Colombia contests since 2025; the page says the conflict "was renewed in 2024 and escalated in 2025".
7. **`lawa-headwaters` — administration.** The lead has France administering; no passage read says who runs the tract.

## Possible duplicates, overlaps and splits

- `kula-kangri` — retire, or fold into `bhutan-china-north`: the list row "Kula Kangri and mountainous areas to the west of this peak, plus the western Haa District" covers the whole Bhutan–China dispute.
- `israeli-posts-south-lebanon` — re-scope (2024 positions of about 10 km² versus the 2026 zone of 570–600 km²); the page's footnote counts `shebaa-farms` inside the same occupation.
- `israeli-held-southern-syria` and `undof-zone` — the page treats the buffer zone and the ground beyond it as one occupation ("Israel advanced within and beyond the UNDOF buffer zone").
- `kyrgyz-tajik-border` and `tort-kocho-road` — the road's neutral-zone status is the only on-the-ground fact found for the border area and belongs to the other area.
- `india-bangladesh-enclaves` and `tin-bigha` — the one enclave that remains, Dahagram–Angarpota, is reached by the Tin Bigha Corridor.
- `india-china-middle-sector` — Barahoti alone fits `own_regime` (a demilitarised plain patrolled by unarmed border police); the other pockets are Indian-held ground claimed by China. Consider splitting Barahoti off, and moving Chumar to a Ladakh area.
- `kinmen-matsu` — Wuqiu differs from Kinmen and Matsu in the sources (a township of 666 people defended by a garrison command, 133 km from the rest of Kinmen County). The facts entered for access and on-the-ground are Kinmen only.
- `isla-portillos` — the 2018 judgment leaves Harbor Head Lagoon and its sandbar to Nicaragua inside Costa Rican territory; possibly a place of its own.
- `ladakh-lac-buffer-zones` and `demchok` — the October 2024 patrolling agreement is mentioned without detail; which zones remain is not established.

## Per area

**imia-kardak** — not sourced: `traveller_access`. Kind as in the lead; the page calls the dispute "part of the larger Aegean dispute" over shelf, waters and airspace. The page names no administering party: both claim, and since 1996 there are "no military forces on the islets".

**india-bangladesh-enclaves** — not sourced: `traveller_access`. Lead confirmed: exchanged at midnight on 31 July 2015. `area_km2` covers the exchanged enclaves only; adverse-possession land (given in another paragraph) is not included.

**india-china-middle-sector** — not sourced: `inhabited`, `traveller_access`, `area_km2`. No single passage covers all pockets: `parties` is quoted for the Jadh Ganga / Nelang area, `origin` and `on_the_ground` for Barahoti; that India controls Kaurik and Shipki La is stated only in table cells. `kind` rests on a map caption naming Kaurik, Tashigang and Barahoti as "locations of differing perceptions" on the LAC. Withdrawn: `inhabited=yes` (the Nelang page says the villages "are inhabited by the Jadh Bhutia tribe" and, in the next sentence, that India evacuated them in 1962) and `traveller_access=restricted` (the only passage is in a Pulam Sumda paragraph tagged "citation needed"; the Nelang page says India "opened these areas for tourism" in 2015). The Barahoti page gives 750 km² for the area China disputes around Barahoti alone.

**indian-jammu-kashmir-ladakh** — not sourced: `traveller_access`, `area_km2` (the two infoboxes give 56,160 km² for Jammu and Kashmir and 59,146 km² for Ladakh; no single passage gives a total). `inhabited` rests on the 2011 census figure for Jammu and Kashmir only. Both page leads also name China as a disputant since 1959; the quoted passage for `parties` covers India and Pakistan. `paper_claim` is the nearest fit, as in the lead.

**isla-brasilera** — not sourced: `traveller_access`. `line_position` kept: both states count the island in their own municipality and Brazil's title rests on the 1851 Treaty. `paper_claim` is as defensible (Brazil "maintains full and effective sovereignty"). The page gives no date for the start of the dispute.

**isla-portillos** — `parties`, `kind`, `origin` are `primary` (ICJ). Not sourced: `on_the_ground`, `inhabited`, `traveller_access`, `area_km2`. Two judgments: 16 December 2015 (sovereignty) and 2 February 2018 (the boundary; Nicaragua to remove a military camp). Whether the camp was removed is not established.

**isla-santa-rosa** — not sourced: `traveller_access`, `area_km2`. Peru's foreign ministry holds that the island no longer exists separately and is part of Chinería Island. `kind` is quoted from the list of territorial disputes: Colombia argues the boundary is the deepest channel and the island emerged on its side.

**isla-suarez** — not sourced: `inhabited`, `traveller_access`, `area_km2`. The page is unclear on administration: "remains supposedly under Bolivian administration" (as of 2009) while Brazilians "hold most of the island's territory". `line_position` kept; the list's wording ("80 islands that are not assigned to any country") would also support `no_agreed_boundary`. Last dated status is 2009.

**islas-chafarinas** — not sourced: `traveller_access`. Lead confirmed. The page is inconsistent on the date: "Under Spanish control since 1847" and, in the history section, a Spanish taking of possession ahead of a French expedition of January 1848.

**israeli-held-southern-syria** — not sourced: `inhabited`, `traveller_access`, `area_km2` ("several hundred square miles" is not a number). Lead confirmed; infobox status "Ongoing", with a raid dated 3 May 2026. `origin` describes the invasion of the buffer zone; that Israel went beyond it, to the Syrian side of Mount Hermon, is in the infobox.

**israeli-posts-south-lebanon** — see contradiction 1. Not sourced: `traveller_access`, `area_km2` (a range). The facts describe the 2026 occupation. Fast-moving article; re-read before relying on it.

**junagadh** — not sourced: `traveller_access`, `area_km2`. Lead confirmed. `inhabited` rests on a 1948 figure (population 720,000). Manavadar appears only as a vassal state of Junagadh.

**kafia-kingi** — see contradiction 3. Not sourced: `traveller_access`. `inhabited` is the row the register's verifier will not find.

**kalapani** — not sourced: `inhabited` (infobox "Population • Total 50–100" does not say whether these are residents or border police), `traveller_access`, `area_km2` (35 km² for the Kalapani territory; "an additional 335 square kilometres" for Nepal's 2020 map up to Limpiyadhura; two passages, and the area covers both). Lead confirmed.

**kangwane-ingwavuma** — not sourced: `traveller_access`, `area_km2`. Lead confirmed. The source pages disagree on which part is which: the list sentence puts KwaZulu-Natal municipalities in "the former bantustan of KaNgwane", while the KaNgwane article says its territory became part of Mpumalanga and the Ingwavuma article ties Ingwavuma to KwaZulu. `inhabited` rests on Ingwavuma being a town.

**karki** — not sourced: `traveller_access`. Lead confirmed.

**kherson-occupied** — not sourced: `area_km2`. `traveller_access=closed` is an interpretation: the quoted rule says entry through a border point not controlled by Ukraine is illegal; it does not say that no other route exists. Kinburn Spit: its own page says it lies in Mykolaiv Oblast and was captured on 10 June 2022. Snihurivka: the page says the occupied Mykolaiv areas were retaken by 11 November 2022 "except for the Kinburn Peninsula"; Russia's annexation declaration included "small occupied areas of neighboring Mykolaiv Oblast". `inhabited` rests on a July 2022 report.

**kinmen-matsu** — not sourced: `area_km2` (three infoboxes: Kinmen 150.456, Matsu 29.60, Wuqiu 1.2 km²). `de_facto_state` follows the register's convention for territory governed from Taipei; the quote shows only that Kinmen is "a county of the Republic of China (Taiwan)", and on the definitions alone `paper_claim` fits equally. The list row quoted for `parties` also covers Pratas and the Vereker Banks.

**klek-skolj** — not sourced: `traveller_access`, `area_km2`. Wikipedia contradicts itself on administration: the border article says "Croatia continues to administer areas that the deal assigns to Bosnia and Herzegovina"; the islet infoboxes say "Administration Bosnia and Herzegovina"; the Klek infobox says "Bosnia and Herzegovina / Croatia". `on_the_ground` follows the border article. `inhabited=no` covers the two islets; the Klek infobox gives population "?".

**koalou** — not sourced: `traveller_access`. Lead confirmed. Area conflict: 68 km² in the Koalou article (entered), "7.75 km 2 triangular area" in the list of territorial disputes.

**kokkina** — not sourced: `traveller_access`, `area_km2`. Lead confirmed; the page says the exclave has functioned as a military camp since 1976.

**korean-dmz** — not sourced: `area_km2` (the page gives 250 km by about 4 km, no area). Lead confirmed. `inhabited=yes` rests on two villages inside the zone; the page describes the northern one as empty concrete shells.

**kosovo** — all seven fields. The same gov.uk page says Serbia does not treat the crossing points with Kosovo as international border crossings and that entry to Serbia from Kosovo without a Serbian entry stamp is likely to be refused.

**kosovo-montenegro-border** — not sourced: `inhabited`, `traveller_access`. Lead confirmed: signed 17 February 2018, ratified by Kosovo's parliament a month later, Čakor handed to Montenegro.

**kostajnica-island** — not sourced: `origin`, `inhabited`, `traveller_access`, `area_km2`. Lead confirmed. One paragraph in the border article is all Wikipedia has.

**kpeaba** — source is a Jeune Afrique news article of 23 December 2016. Not sourced: `traveller_access`, `area_km2`. `kind` is weakly supported: the article calls it a "conflit frontalier" but does not state either side's line, and reports that in 2013 both governments rejected the terms "conflit frontalier" and "différend territorial". The border article on Wikipedia does not mention the dispute.

**kula-kangri** — see contradiction 2. Not sourced: `inhabited`, `traveller_access`. `no_agreed_boundary` is kept only because "Bhutan's border with Tibet has never been officially recognised and demarcated". The 400 km² figure is for the area the source calls "Kula Khari".

**kuril-islands** — not sourced: `traveller_access`, `area_km2` (10,503.2 km² is the whole chain). Lead confirmed. The page also reports the US position that the islands "remain occupied territory under Russian control", which would point to `occupied_or_annexed`. The visa-free visits for former Japanese residents ended in 2022; that is not a general entry rule.

**kyrgyz-tajik-border** — not sourced: `traveller_access`, `area_km2`. Lead confirmed: agreement signed 21 February and 13 March 2025. Ratification: the relations article says Kyrgyzstan's parliament approved it; the border article still says both parliaments "still have to ratify" (stale); Tajik ratification is not confirmed by the pages read.

**kyrgyz-uzbek-border** — not sourced: `inhabited`, `traveller_access`, `area_km2`. Lead confirmed for Kempir-Abad and Barak; Ungar-Too is not mentioned in the pages read. The border article adds: "Until 2026, the Uzbek enclave of Jangail existed in Kyrgyzstan."

**la-guera** — not sourced: `inhabited`, `traveller_access`. The page contradicts itself on habitation: "ghost town", "technically abandoned", and an infobox population of 3,726 (2004). Whether a garrison is present is not stated. `area_km2` 87.8 is the infobox figure for La Güera, not a measured area of the western half of the peninsula.

**ladakh-lac-buffer-zones** — not sourced: `inhabited`, `traveller_access`, `area_km2`. The facts describe 2020–2022. Three articles say only that in October 2024 India announced "an agreement over patrolling arrangements"; the state of the zones after it is not established. Buffer zones are described for Galwan (PP 14), Gogra (PP 17A), Hot Springs and the north bank of Pangong Tso; none is described at Depsang.

**lake-constance** — not sourced: `inhabited`, `traveller_access`. Lead confirmed, from German Wikipedia (the English article's only sentence on the matter is tagged "citation needed"). The two legal views: division along the middle (Switzerland) and a condominium beyond 25 m depth (Austria).

**lake-nyasa-islands** — see contradiction 4. Not sourced: `inhabited`, `traveller_access`, `area_km2`. The sources describe a dispute over the boundary in the lake; the islands (Lundo, Mbamba) appear only in one sentence of the list of territorial disputes.

**lawa-headwaters** — not sourced: `on_the_ground`, `traveller_access`, `area_km2`. Lead kind confirmed: both accept the Lawa as the border and disagree which river is its source. The border article gives "an approximately 5,000 square mile disputed territory" (about 12,950 km²); not entered, to be compared with the machine area first. River names differ between the two pages (Litani / Itany for France's line, Marouini / Malani for Suriname's). A 2021 protocol fixed the boundary up to Antécume-Pata; "most of the Lawa dispute" remains as of 2025.

## Files

In `scratchpad/sourcing/`: `out-3.csv`, `out-3.notes.md`; `rows3.py` (values and anchors), `build_out3.py`, `selfcheck3.py`, `e2e3.py`; `fetchlog-3.txt` (page → pinned URL), `pages3.tsv` (non-Wikipedia URL → saved text); private copies of every page as fetched in `b3pages/` (keyed by revision id) and `pages/b3_*.html|txt`.
