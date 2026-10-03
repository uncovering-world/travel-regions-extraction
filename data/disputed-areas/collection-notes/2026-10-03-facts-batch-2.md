# Batch 2 — sourcing notes (read 2026-10-03)

183 rows for 35 areas in `out-2.csv`. Every quote was cut by script (`build2.py`) from the saved page text in `pages/` and re-checked by `selfcheck2.py` (substring of the saved page, single paragraph, allowed values). Nothing was taken from the `lead_*` columns.

Sources: English Wikipedia at pinned revisions (`evidence=secondary`) for almost everything. Primary pages used: UNFICYP "About the buffer zone" (cyprus-buffer-zone: kind, origin, on_the_ground, inhabited, traveller_access) and UK FCDO travel advice on gov.uk (diego-garcia, gaza-strip, falkland-islands: traveller_access). The gov.uk and UNFICYP pages are unpinned and will change; no archive copy was stored.

General limits of this pass:

- `traveller_access` is missing for 26 of 35 areas: the pages read do not state an entry regime. A travel advisory "against all travel" (FCDO on Crimea) was not treated as an access value.
- Several quotes are infobox fragments (areas of Crimea, Diego Garcia, Falklands, Ghajar, Golan; Golan population), not sentences.
- Values converted from the quoted unit: dokdo 19 ha -> 0.19; ghajar 246 ha -> 2.46; hans-island 130 ha -> 1.3.
- One quote may serve several fields of the same area (parties/kind/origin).

## Per area

**crimea** — not sourced: traveller_access. Lead confirmed.

**croatia-serbia-danube-pockets** — not sourced: inhabited (the page says "uninhabited and frequently flooded" only of the Yugoslav period), traveller_access. area_km2 = 100 is one of several figures on the page ("up to 140", "100 on the eastern bank", "100 in total, 90% on the eastern bank"). The page notes Vukovar Island is visited by boat from Vukovar with no border controls (2006 local agreement) — not entered, it concerns one island.

**cyprus-buffer-zone** — complete. Parties from Wikipedia; the rest from UNFICYP. Access is `restricted` for the zone in general, but UNFICYP says civilians enter the villages / Civil Use Areas freely — the area is internally mixed.

**david-gareja** — not sourced: inhabited, traveller_access, area_km2 (the page gives 25 km2 for Azerbaijan's Keshikcidag reserve, which is not the disputed area). Who controls which part is not stated beyond "partially located on the territory of Azerbaijan". kind `line_position` rests on the delimitation passage.

**demchok** — not sourced: traveller_access. inhabited=yes rests on a 2005 newspaper excerpt quoted in the article's reference list (Indian-side village, 150 people) — weak and old. area 1,900 km2 is "Chinese sources".

**diego-garcia** — complete. The sources add to the lead: sovereignty-transfer treaty with Mauritius signed 22 May 2025, not ratified, ratification suspended in 2026 (BIOT article). The Diego Garcia article also mentions a "resettlement of Île du Coin" — a sign that BIOT outside Diego Garcia is changing; not followed up. The gov.uk access statement is for BIOT as a whole.

**doi-lang** — NO parties, NO kind. Only on_the_ground (a Thai national-park article that does not mention any dispute). Wikipedia's list of territorial disputes has a row "Doi Lang / Myanmar, Thailand" with an empty description, so there is no passage to quote; the Myanmar–Thailand border and relations articles do not mention Doi Lang. Needs a non-Wikipedia source or stays a gap.

**dokdo** — not sourced: origin (no sentence with the year South Korea took control was found). kind `islets_for_maritime_zone` rests on "rich fishing grounds that may contain large deposits of natural gas"; the page does not literally say the dispute is mainly about the sea. inhabited=`garrison_only`: staff and police, "no resident civilians" since March 2026. The page says North Korea has dropped its claim.

**donetsk-occupied** — not sourced: inhabited, traveller_access, area_km2. The title "Russian occupation of Donetsk Oblast" redirects to "Donetsk People's Republic". on_the_ground is dated (55% by June 2022); no current control figure on the page.

**doumeira** — not sourced: inhabited, traveller_access, area_km2. Eritrean occupation since June 2017 is Djibouti's accusation (article) / stated flatly in the list. Possible split: the 1900 protocol left Doumeira Island unassigned and demilitarised (closer to `no_agreed_boundary`/`own_regime` on paper), while the mainland hill is a `line_position` case. The article notes the two states agreed to normalise relations in September 2018; nothing later.

**dragonja** — not sourced: traveller_access, area_km2; who controls the left bank is not stated in a quotable sentence (lead said Croatia). Sources add: the 2017 PCA arbitration ruling, implemented by Slovenia on 29 Dec 2017 and rejected by Croatia. The lead name bundles "other Slovenia–Croatia segments" (Sveta Gera/Trdinov vrh — "dormant as of 2011", Mura) — these are separate places and probably should be split or dropped from this area.

**durand-line** — not sourced: on_the_ground, inhabited, traveller_access, area_km2. This is a line, not an area; area and inhabited do not apply. kind differs from lead (`line_position` -> `paper_claim`): the source says Afghanistan refuses to recognise the line at all and claims the Pashtun territories of Pakistan, i.e. it is not a disagreement about where an agreed line runs. Open to the owner's view; arguably not a register area at all.

**east-jerusalem** — not sourced: traveller_access. area 70 km2 is the West Bank territory added to the municipality in 1967 ("today referred to as East Jerusalem"); the page also gives other figures. Lead confirmed.

**eastern-ossetia-claim** — not sourced: traveller_access, area_km2. The Truso article says everyone must pass an interior checkpoint with documents — suggests `restricted`, but a permit is not stated, so left out. inhabited=yes rests on "only 29 people ... mostly seasonally" tagged [better source needed]; it covers the Truso Gorge only, not Ghuda/Kobi.

**essequibo** — not sourced: traveller_access. Sources add: Venezuela controls Ankoko Island (possible separate area), ICJ case accepted 18 Dec 2020, Venezuelan referendum Dec 2023.

**estonia-russia-border** — not sourced: on_the_ground, inhabited, traveller_access, area_km2. That Russia administers the areas is only implicit (Leningrad/Pskov oblasts), so the parties value does not give Russia a role. kind `paper_claim` rests on "The Estonian constitution still references the 1920 treaty as the border"; the same source says the unratified agreement renounces Estonian claims — consistent with the lead's "no official claim", and a reason to question whether this belongs in the register. The Estonia–Russia border article mentions a different live spot: the Saatse Boot, closed by Estonia in 2025 — candidate for a separate area.

**ethiopia-somalia-provisional-line** — not sourced: on_the_ground, inhabited, traveller_access, area_km2. A line, not an area. The parties quote is only the sentence naming the border; the article is thin and poorly written.

**falkland-islands** — complete. traveller_access=`open` rests on FCDO advice addressed to British nationals (visa-free, one month on arrival); entry rules for other nationalities were not read.

**fasht-ad-dibal-qitat-jaradah** — CONTRADICTION. The list of territorial disputes says both features are "controlled by Bahrain" and still disputed by Qatar. The Bahrain–Qatar relations article says the ICJ resolved the disputes on 16 March 2001, giving Qit'at Jaradah to Bahrain and Fasht Dibal to Qatar; the Qit'at Jaradah article agrees for Jaradah. I recorded parties/origin from the relations article. If that is right the dispute was settled in 2001 (before 2015), so by UPDATING.md the candidate should be `ignore`, not an area; `kind` is given only to describe the nature of the former dispute. No dedicated Wikipedia article on Fasht ad Dibal exists. inhabited=no is quoted for Qit'at Jaradah only (a 48 m2 cay at high tide). Should be checked against the ICJ judgment itself.

**gaza-strip** — complete, but fast-moving. Parties value lists Israel, the PA and Hamas from one paragraph; current governance (peace plan of Oct 2025, UNSC Res. 2803, Board of Peace) is only partly captured in on_the_ground. Population quote oddly says "As of 2010 ... just over 2 million". traveller_access=`closed` rests on FCDO: crossings out of Gaza closed to civilians since 6 May 2024 — it speaks of leaving, and the page may lag behind the 2025–26 arrangements.

**gazakh-exclaves** — not sourced: traveller_access, area_km2 (22 km2 is given for the Barkhudarly+Sofulu exclave only). Facts are stitched from three village articles; inhabited=no means "abandoned Azerbaijani village" (Barkhudarly). The Yukhari Askipara article adds that Pashinyan in 2024 acknowledged Azerbaijan's sovereignty over the villages. Two physically separate exclaves — could be split.

**gazakh-four-villages** — not sourced: on_the_ground, traveller_access, area_km2. Lead confirmed: returned to Azerbaijan 24 May 2024.

**ghajar** — complete. kind/parties follow the lead. traveller_access=`open` is as of September 2022 (IDF lifted restrictions); the page gives no status after the 2023–24 hostilities. area 2.46 km2 and population are for the whole village, not the northern part.

**gibraltar** — not sourced: traveller_access. Sources add: treaty signed 14 July 2026 (UK, Spain, Gibraltar, EU) removing routine controls at the land frontier and bringing Gibraltar into Schengen — whether it is in force is not stated. The parties quote gives the UK no explicit role (the page calls Gibraltar a British Overseas Territory elsewhere).

**gilgit-baltistan** — not sourced: traveller_access. The page says the Kashmir region is also disputed "between India and China since 1959"; no Chinese claim to Gilgit-Baltistan itself is stated.

**glorioso-islands** — not sourced: traveller_access. kind differs from lead (`islets_for_maritime_zone` -> `paper_claim`): the page does not say the claim is about the sea (it does give an EEZ of 48,350 km2 for 5 km2 of land, which is what the lead kind would rest on). By "what a person standing there would meet" it is a garrisoned nature reserve. Owner's call.

**golan-heights** — not sourced: traveller_access. area 1,800 km2 is the whole plateau; the page gives 1,150–1,500 km2 for the Israeli-held part depending on source. Sources add: in late 2024 Israeli forces took control of the UNDOF buffer zone (266 km2) on the Syrian side — a separate `own_regime` area if not already in the register; Colombia recognised Israeli sovereignty in 2026 (third state per infobox, second per the text — the page is inconsistent).

**gornja-siga** — not sourced: origin. traveller_access=`closed` is my reading of "Croatia has frequently blocked off access ... arrested for trying to enter"; `restricted` is arguable. Sources are the Liberland and Croatia–Serbia dispute articles. Same dispute as croatia-serbia-danube-pockets (other bank); the lead name "and other west-bank pockets" is not supported beyond "Pocket 3".

**guantanamo-bay** — complete. area 117 km2 is "land and water". Lead confirmed.

**guinea-liberia-makona** — not sourced: on_the_ground, inhabited, traveller_access, area_km2. The only source is the list entry (March 2026 incident, uncited in what I read); the Guinea–Liberia border article does not mention it and says both states confirmed the boundary in 1960. kind `line_position` is inferred from "the disputed location" on an agreed boundary — weak.

**halaib-triangle** — not sourced: traveller_access. Lead confirmed. Bir Tawil is mentioned as unclaimed (separate area).

**hans-island** — not sourced: traveller_access. Lead confirmed: split agreed 14 June 2022.

**hatay** — not sourced: traveller_access. kind `resolved_recently` rests on a weak passage: the list says the Syrian claim lasted until 2024 "as implied by the current logos" of Syrian ministries; the Hatay article only says the issue "has remained largely dormant" since the 2000s. No settlement instrument is cited. Could equally be a dormant `paper_claim`.

**heglig** — not sourced: traveller_access, area_km2. CONTRADICTION inside the article: the lead says "administered by Sudan", the body says the Rapid Support Forces seized the area on 8 Dec 2025, and references mention South Sudanese troops guarding the oil field under a tripartite deal. Recorded both (parties vs on_the_ground). kind differs from lead (`line_position` -> `paper_claim`): the source describes a place claimed by both and administered by one, not a disagreement over where an agreed line runs.

**ilemi-triangle** — not sourced: inhabited (only nomadic herders are mentioned), traveller_access. kind differs from lead (`no_agreed_boundary` -> `paper_claim`): the page describes a 1914 treaty line and Kenyan de facto control beyond it, with both states claiming; several lines were in fact defined (1914 line, Red Line, 1950 patrol line), so `line_position` is also arguable. Ethiopia makes no claim (confirmed).

## Duplicates / splits to consider

- croatia-serbia-danube-pockets and gornja-siga: two faces of one dispute; keep both only if the east-bank/west-bank difference in kind is wanted.
- dragonja: split off or drop "other Slovenia–Croatia segments".
- doumeira: mainland hill vs island have different treaty status.
- gazakh-exclaves: two separate exclaves.
- essequibo: Ankoko Island is Venezuelan-controlled.
- durand-line, ethiopia-somalia-provisional-line: lines rather than areas.
- fasht-ad-dibal-qitat-jaradah: likely settled in 2001 -> `ignore`.
- New candidates seen in sources: Saatse Boot (Estonia), UNDOF zone in the Golan.
