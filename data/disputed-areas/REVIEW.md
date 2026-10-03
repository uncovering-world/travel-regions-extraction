# Open review points after the sourcing of 2026-10-03

Not register facts. This is the list of doubts raised while the register's facts were re-entered from sources: kinds that differ from the first census, areas that may need to be split, merged or dropped, places where events have overtaken the sources, and contradictions between sources. Nothing here has been decided, and `areas.csv` was not changed because of it.

How to read it: sections 5 to 7 below are the report of the agent that merged the collected facts, kept in its own words ("I", "my reading" are that agent's). Section 7 relays the notes of the six collecting agents and was not checked again. Statements about events are what the pages read on 2026-10-03 said.

When a point is settled — by the owner, or by reading a better source — change the register through the routine in [UPDATING.md](UPDATING.md) and remove the point from this list.

## 5. Kinds

### 5a. Kind differs from the seed lead — 14 areas, imported as the agents gave them

Every passage below verifies. "Support" is my reading of whether the passage shows the kind as UPDATING.md defines it.

| Area | Lead → imported | Passage rests on | Support (my reading) |
|---|---|---|---|
| `al-fashaga` | line_position → paper_claim | "Sudan retained administrative control" under a 2008 compromise; both claim | fair; the page is a stub, the agent asks for the "Al-Fashaga conflict" article to be read |
| `chagos` | paper_claim → occupied_or_annexed | ICJ 2019 and ITLOS 2021: the UK has an obligation to return the islands | fair; `lease_or_base` also arguable for the base — owner's call |
| `durand-line` | line_position → paper_claim | Afghanistan refuses to recognise the line and claims Pashtun territories of Pakistan | fair; the agent doubts it is an area at all |
| `glorioso-islands` | islets_for_maritime_zone → paper_claim | controlled by France, claimed by Comoros and Madagascar | fair, but **inconsistent** with `tromelin` and `scattered-islands-mozambique-channel`, which kept islets_for_maritime_zone |
| `heglig` | line_position → paper_claim | "claimed by both … but administered by Sudan" | fair; overtaken by events (7c) |
| `ilemi-triangle` | no_agreed_boundary → paper_claim | Kenya has de facto control; dispute arose from the 1914 treaty line | fair, but **docs/status.md names Ilemi as an example of `no_agreed_boundary`** |
| `kafia-kingi` | paper_claim → occupied_or_annexed | infobox "de jure South Sudan / de facto Sudan"; due to go to South Sudan under the 2005 CPA | weak: infobox of a page tagged "neutrality disputed" |
| `marie-byrd-land` | no_agreed_boundary → unclaimed | "an unclaimed region of Antarctica" | good; follows the kind added at 15:50 |
| `mazraat-deir-al-ashayer` | line_position → no_agreed_boundary | "no fully formalized border demarcation … overlapping claims" | fair; its `parties` row (Lebanon administers, Syria claims) reads as paper_claim |
| `perejil` | paper_claim → own_regime | "the island remains unoccupied but claimed by both sides" | weak: unoccupied is not a regime; the island's own article says "administered by Spain" |
| `point-20` | line_position → no_agreed_boundary | the border outside the 1995 agreement "has not been determined" | good |
| `pratas` | islets_for_maritime_zone → de_facto_state | a sentence of the list about Taiwan, Penghu, Kinmen and Matsu | **weak: the passage does not name Pratas**; the kind follows the `kinmen-matsu` convention |
| `prevlaka` | line_position → own_regime | 2002 agreement "demilitarized Prevlaka", still temporary | good; the page carries an "update needed since 2006" banner |
| `rukwanzi-semliki` | line_position → own_regime | New Vision, December 2007: the two states "have demilitarised" the island | stale: nothing newer was found |

### 5b. Kind corrected after the import — 2 areas

`bir-tawil` and `gornja-siga` were collected under the kinds in force before `unclaimed` was split from `no_agreed_boundary`. Their passages say "claimed by neither country" and "left unclaimed by both Croatia and Serbia", so their kind is now `unclaimed`.

### 5c. No kind imported — 3 areas (from the notes)

- `armistice-no-mans-lands` — nothing read says how these strips are regarded today; the lead's occupied_or_annexed is unsupported.
- `bhutanese-enclaves-tibet` — no source says Bhutan still claims the exclaves; the lead's paper_claim is unsupported.
- `doi-lang` — Wikipedia's list has a row with an empty description; no passage to quote, so neither `parties` nor `kind`.

### 5d. Kinds kept as the lead with a caveat stated by the agent (from the notes)

The main ones: `undof-zone` (own_regime; occupied since 8 December 2024), `tunbs`, `sveta-gera`, `yenga`, `strovilia` (each could be occupied_or_annexed), `tigri`, `susta` (could be paper_claim), `wadi-halfa-salient` (could be line_position), `tiwinza`, `suleyman-shah-tomb`, `moldauhafen`, `palanca-road` (not leases with foreign jurisdiction in the strict sense), `sudan-south-sudan-other-border-areas` (could be no_agreed_boundary), `wake-island`, `machias-seal-island` (could be islets_for_maritime_zone), `yalu-tumen-islands`, `kinmen-matsu` (de_facto_state by convention; paper_claim fits equally), `azad-kashmir`, `isla-brasilera`, `isla-suarez`, `kuril-islands`, `northern-cyprus`, `paracel-islands`, `scattered-islands-mozambique-channel`, `hatay` (resolved_recently on a weak passage), `akrotiri-dhekelia` (retained sovereignty, not a lease).

### 5e. Kinds whose passage shows a dispute or a feature but not the kind (my reading, all 207 kind rows read)

No kind is contradicted by its own passage except the two in 5b and, arguably, `kpeaba` (line_position; the quoted sentence reports that both governments rejected any "conflit frontalier"). Thin support: `bajo-nuevo`, `bosnia-serbia-drina`, `caspian-islets-ukatny`, `conejo-island`, `dokdo`, `estonia-russia-border`, `guinea-liberia-makona`, `hatay`, `india-china-middle-sector`, `kula-kangri`, `nepal-china-humla`, `ntem-island`, `okpara-villages`, `otangav`, `palanca-road`, `paracel-islands`, `pratas`, `roc-legacy-claims`, `sudan-south-sudan-other-border-areas`, `suleyman-shah-tomb`, `three-pagodas-pass`, `tromelin`, `varosha`, `yalu-tumen-islands`. The agents flagged most of these themselves.

## 6. What I did not verify

- **That a value follows from its passage.** `verify_quotes.py` proves the passage is on the page, nothing more. Beyond that I read all 207 `kind` rows, all 50 `traveller_access` rows, the 45 `inhabited` rows valued `no` or `garrison_only`, recomputed the 21 converted areas, and read a fixed sample of 40 rows across all fields. I found no value contradicted by its passage other than the cases in 5b and 5e. The other rows — most of `parties`, `origin`, `on_the_ground` and `inhabited = yes`, about 650 — were not read by me.
- **Whether a passage is still true.** Several rest on dated statements (7c). 44 sources are live pages without a pinned revision (gov.uk ×21, ICJ ×4, taaf.fr, vayla.fi, sysselmesteren.no, doi.gov ×2 each, and eleven single pages); none has an archived copy in `sources.csv`'s `note`, which UPDATING.md asks for when a page is likely to change. They verified today; they can stop verifying when the page changes.
- **Evidence levels.** I did not judge them. 54 rows are `primary`; of the 23 from gov.uk, only `diego-garcia`, `falkland-islands` and `south-georgia-south-sandwich` quote the administering government; the other 20 are the UK's travel advice about a third party's territory (list in appendix C). The two `news.un.org` rows are a UN News explainer, the seven ICJ rows are the Registry's case overviews, not the judgments. The agents say so in their notes.
- **The Factbook rows (35).** They cite a third-party GitHub mirror of the CIA Factbook at a commit of 2023-05-25; the CIA's own pages were not opened by anyone.
- **Anything in section 7.** It is relayed from the notes.
- Not checked at all: `areas.csv` names and scopes against the sources, `discovery-map.csv`, the Natural Earth and Wikidata links.

## 7. Questions for the owner, from the notes (nothing in `areas.csv` was changed)

### 7a. Disputes that may be settled or not live — candidates for `ignore` or retirement

Settled before 2015 according to a source the agent read (`resolved_recently` would not apply):

- `fasht-ad-dibal-qitat-jaradah` — the Bahrain–Qatar relations article and the Qit'at Jaradah article say the ICJ settled it on 16 March 2001 (Jaradah to Bahrain, Fasht ad Dibal to Qatar); Wikipedia's list still shows both as Bahrain-controlled and disputed. The imported `origin` records the 2001 settlement; the imported kind describes the former dispute.
- `kula-kangri` — "The claim was relinquished in the 1980s"; or fold into `bhutan-china-north`.
- `sindabezi` — the only narrative source (a self-published history site) says the 1994–95 dispute ended with the border confirmed along the deep-water channel.
- `saudi-kuwait-neutral-zone` — the border article says the partition was ratified in 1969–70 and the border finalised then; the list and the Factbook date the settlement to 2019 (imported: resolved_recently, 2019).
- `bhutanese-enclaves-tibet` — occupied by China in 1959; no current Bhutanese claim found.
- `yalu-tumen-islands` — Wikipedia: the 1962 treaty and 1964 protocol allocated every islet; the 2023 Factbook: "certain islands … are in dispute".
- `migingo` — Wikipedia: Uganda accepted in 2009 that the island is Kenyan, leaving only waters in dispute; the 2023 Factbook: both claim the island.

Possibly not a live dispute, or too thin to tell: `libya-niger-tummo` (the Factbook's Libya entry says the boundary "has never been disputed"), `libya-algeria-claim` (Factbook only, "dormant"), `okpara-villages`, `lunkinda-pweto` (one article says the enclave was ceded to DR Congo), `otangav` (a 2023 Cambodia–Laos demarcation treaty), `thai-lao-land-border-villages`, `three-pagodas-pass`, `point-20`, `estonia-russia-border` (no official claim), `hatay` (dormant paper claim or resolved?), `badme` (sources disagree whether the 2018 handover happened), `swains-island` (the claim is a 2006 draft constitution of Tokelau), `congo-river-islands` (no island named anywhere), `bosnia-serbia-drina` (one table cell), `guinea-liberia-makona`, `ntem-island`, `kpeaba`, `nepal-china-humla`, `doi-lang`.

Not areas, or not disputes: `durand-line` and `ethiopia-somalia-provisional-line` (lines); `roc-legacy-claims` (a bundle of about 25 territories, several already in the register); `antarctic-peninsula-overlap` (inside `antarctica`, same regime); `svalbard`, `tin-bigha`, `tiwinza`, `tort-kocho-road` (treaty regimes, no dispute — in scope as special-status areas, listed for completeness).

### 7b. Areas to split, merge or re-scope

Split or re-scope:

- `armistice-no-mans-lands` — Latrun, the Jerusalem no-man's-land and Mount Scopus do not share one set of facts.
- `israeli-posts-south-lebanon` — the 2024 positions (about 10 km², a footnote) versus the 2026 zone of 570–600 km².
- `india-china-middle-sector` — Barahoti alone is a demilitarised plain (own_regime); Chumar belongs to Ladakh, not the middle sector.
- `ta-muen-thom-emerald-triangle` — at least three places (Ta Muen Thom, Ta Krabey/Ta Khwai, Chong Bok), more named in the crisis article.
- `sudan-south-sudan-other-border-areas` — five places, one of which (Kaka) no page names; or merge into the Abyei / Kafia Kingi / Heglig row of the list.
- `thai-lao-land-border-villages` — the three villages of 1984 and Ban Romklao of 1987–88.
- `mont-blanc-summit` — Mont Blanc, Dôme du Goûter, and the Col du Géant as a third place.
- `pedra-branca` — South Ledge is still unresolved; Pedra Branca and Middle Rocks are settled.
- `rukwanzi-semliki` — nothing describes the Semliki valley part.
- `doumeira` — mainland hill versus the island (different status under the 1900 protocol).
- `dragonja` — drop or split off "other Slovenia–Croatia segments" (`sveta-gera` is already an area; Mura).
- `gazakh-exclaves` — two separate exclaves.
- `kinmen-matsu` — Wuqiu differs; the facts entered are Kinmen only.
- `moldovan-held-left-bank` — two groups of villages on opposite banks.
- `spratly-islands` — by occupying state.
- `roc-legacy-claims` — retire or split.
- `yenga` — the list has a second row for the left bank of the Moa/Makona.
- `citrana-naktuka` — a second unresolved Oecusse piece (Área Cruz) and Batek Island; `isla-portillos` — Harbor Head Lagoon; `kherson-occupied` — Kinburn Spit lies in Mykolaiv Oblast.
- Names that promise more than the sources cover: `bhutan-china-north` (Beyul Khenpajong not found), `bhutan-china-west` ("western Haa", "Sinchulung"), `caspian-islets-ukatny` (only Ukatny), `kyrgyz-uzbek-border` (Ungar-Too), `russian-ranges-kazakhstan` ("and others"), `gornja-siga` ("other west-bank pockets"), `migingo`, `mbanie`, `machias-seal-island` (figures for the main island only), `marie-byrd-land` and `antarctic-peninsula-overlap` (the meridians in the names are not sourced).

Merge, duplicate or overlap:

- `antarctic-peninsula-overlap` ⊂ `antarctica`; `mazraat-deir-al-ashayer` ⊂ `lebanon-syria-undelimited`; `kula-kangri` ⊂ `bhutan-china-north`.
- `croatia-serbia-danube-pockets`, `gornja-siga`, `sarengrad-vukovar-islands` — one dispute, three areas; the first and third use the same passage for `kind`.
- `transnistria`, `transnistria-security-zone`, `moldovan-held-left-bank` — the security zone consists of localities held by one side or the other (Bender included).
- `israeli-held-southern-syria` and `undof-zone` — treated by the page as one occupation; `israeli-posts-south-lebanon` and `shebaa-farms`.
- `ankoko-island` and `essequibo`; `bajo-nuevo` and `serranilla` (one row each in Wikipedia's list).
- `taiwan` — the area figure 36,193 km² includes `kinmen-matsu`, `pratas` and the ROC-held South China Sea islands.
- `somaliland` and `sool-sanaag-cayn`; `west-bank` and `east-jerusalem` (is East Jerusalem inside the West Bank figure?).
- `kyrgyz-tajik-border` and `tort-kocho-road`; `india-bangladesh-enclaves` and `tin-bigha`; `ladakh-lac-buffer-zones` and `demchok`.
- `south-korea-claimed-by-dprk` mirrors `north-korea-claimed-by-rok`.
- New candidates seen in sources, not in the register: Saatse Boot (Estonia), the Uzbek enclave of Jangail ("existed until 2026").

### 7c. Areas overtaken by events (facts already ageing)

- `israeli-posts-south-lebanon` — ground invasion from 16 March 2026; Netanyahu on 15 June 2026: forces stay in "the Lebanon security buffer zone". The area's name and scope no longer match.
- `undof-zone`, `israeli-held-southern-syria`, `golan-heights` — Israel entered the UNDOF zone on 8 December 2024 and still holds it; talks since June 2025, no outcome on the pages read.
- `heglig` — the article's lead says "administered by Sudan", its body that the Rapid Support Forces seized the area on 8 December 2025. Both are in the register (`parties` versus `on_the_ground`).
- `chagos`, `diego-garcia` — treaty with Mauritius signed 22 May 2025, ratification on hold in 2026; four Chagossians settled on Île du Coin in February 2026, so `inhabited = garrison_only` is already slightly out of date.
- `gaza-strip` — governance after the October 2025 plan only partly captured; `traveller_access = closed` rests on a statement about leaving Gaza dated May 2024.
- `ta-muen-thom-emerald-triangle`, `preah-vihear` — fighting in July and December 2025, ceasefire of 27 December 2025, land border suspended; who holds the ground around Preah Vihear is not stated.
- `gibraltar` — treaty signed 14 July 2026 removing routine controls at the land frontier; entry into force not stated.
- `south-korea-claimed-by-dprk` — North Korea's constitution amended on 23 March 2026; `dokdo` — no resident civilians since March 2026.
- `abu-musa`, `tunbs` — the pages mention a "2026 Iran war"; no change of control reported.
- `ceuta` — unrest in summer 2026 after a mass border breach.
- `oyster-pond` — French law of 22 July 2026 approves ratification; the Netherlands still to ratify; not in force (imported: resolved_recently).
- `kyrgyz-tajik-border`, `tort-kocho-road` — agreement of 13 March 2025; ratification status unclear on the pages read.
- `mbanie` — ICJ judgment of 19 May 2025; handover by Gabon not confirmed. `tiran-sanafir` — handover possibly incomplete. `belize-guatemala-claim`, `sapodilla-cayes` — ICJ cases pending (Guatemala admitted as intervener on 19 March 2026).
- `somaliland` — recognised by Israel on 26 December 2025.
- `luhansk-occupied`, `donetsk-occupied`, `kherson-occupied`, `zaporizhzhia-occupied` — control described as of 2022; where `inhabited` is given it rests on statements of 2017 to 2022.
- `suleyman-shah-tomb` — the tomb was moved in February 2015 to a third site; `moldauhafen` — the lease ends in 2028.
- `ladakh-lac-buffer-zones`, `demchok` — the October 2024 patrolling agreement; what remains of the zones is not established.
- Stale by the date of the passage: `ghajar` access (September 2022), `three-pagodas-pass` access (2011 at the latest), `rukwanzi-semliki` (2007), `sabanerwa` (2006), `citrana-naktuka` (early 2024), `yenga` (2021), `wake-island` (an old Interior Department page).

### 7d. Contradictions between sources that the register now carries or hides

- Who administers: `heglig`, `klek-skolj` (three Wikipedia infoboxes disagree), `perejil` ("administered by Spain" versus "unoccupied"), `rukwanzi-semliki`, `susta`, `lake-nyasa-islands`, `lawa-headwaters` (nobody named), `chile-peru-land-triangle` (both claim to patrol), `varosha` (Northern Cyprus versus the Turkish army).
- Who claims: `bajo-nuevo` and `serranilla` (Colombia, Jamaica, United States, Honduras, Nicaragua — a different set in the article, the infobox, the list and the Factbook), `rockall` (Iceland and Denmark are parties to the seabed dispute only), `shebaa-farms` (Syria's position), `sool-sanaag-cayn` (Puntland).
- Whether it is over: `badme`, `fasht-ad-dibal-qitat-jaradah`, `migingo`, `lunkinda-pweto`, `saudi-kuwait-neutral-zone`, `yenga`, `libya-niger-tummo`, `yalu-tumen-islands`, `nepal-china-humla`.
- Figures: `koalou` (68 km² entered; 7.75 km² in the list), `siachen` (2,500 entered; 700 to 9,600 elsewhere), `susta` (50 entered; 148.6 implied by the text), `libya-niger-tummo` (25,000 entered; 19,400 on Wikipedia), `rincon-de-artigas` (237 versus 273), `shaksgam`, `south-ossetia`, `svalbard`, `west-bank`, `golan-heights`; `chile-peru-land-triangle` and `sabanerwa` have figures that cannot be read as an area and were not entered.
- Habitation: `tunbs`, `varosha`, `la-guera` (no value entered because the page contradicts itself); `artsvashen`, `aksai-chin`, `spratly-islands` (entered `yes` although the same page also says "largely abandoned", "nearly uninhabitable", "largely uninhabited").
- Inconsistent treatment between batches: for the same gov.uk statement about entering Ukrainian territory through a point Ukraine does not control, `kherson-occupied` has `traveller_access = closed`, while `luhansk-occupied` and `zaporizhzhia-occupied` have no value; `glorioso-islands` versus the other French islands (5a).

## 8. Facts on who holds an area (added 2026-10-03)

The fields `holder`, `holder_since` and `stated_outline` were collected for 29 contested areas; every passage is found in its source. No act ending a contest was found for any of them. Weak rows, as the collectors reported them and not checked again:

- `holder_since`: `la-guera` (an infobox line; a Polisario presence is reported in 2015), `kokkina` ("1964 or earlier"), `western-sahara-moroccan-controlled` (1979 recorded, 1987 the alternative), `kosovo` (1999, the UN administration, not 2008), `abkhazia` (1993 for most of the area, Kodori in 2008), `donetsk-occupied` and `zaporizhzhia-occupied` (a map caption).
- `holder`: `kafia-kingi` (undated sentence in an article tagged as disputed), `gazakh-exclaves` (a section tagged as unsourced), `somaliland` (the east is held by another party).
- `stated_outline`: `shebaa-farms` (a UN cartographer's definition, not a party's line), `crimea` (a geographic sentence), `artsvashen`, `karki`, `gazakh-exclaves` (a general passage on Soviet-era borders), `transnistria` (the Security Zone), `luhansk-occupied` (the parties disagree on control), `kherson-occupied` and `israeli-held-southern-syria` (recorded as a moving line although the sources describe fairly static ones). None found for `kinmen-matsu`, `pratas`, `somaliland`.
- Scope: `israeli-posts-south-lebanon` no longer matches what its name says; problems also noted for `ghajar`, `east-jerusalem`, `crimea`, `la-guera`, `ankoko-island`.
