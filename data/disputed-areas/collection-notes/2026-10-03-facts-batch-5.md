# Batch 5 — sourcing notes (read 2026-10-03)

`out-5.csv`: 190 rows for 35 areas. Every area has `parties`, `kind`, `origin` and `on_the_ground`; `inhabited` 22, `area_km2` 16, `traveller_access` 12. Nothing was entered from memory or from the `lead_*` columns: each row rests on a passage cut by script (`build5.py`) out of a page fetched in this session (`fetchlog-5.txt` lists every fetch and its URL).

Self-check (`build5.py`, repeated stand-alone by `selfcheck5.py`): 190 rows, 0 failed, 0 dropped. For each row the whitespace-normalised quote is a substring of the saved page text (`pages/<stem>.txt`) and, for Wikipedia, of a private snapshot of the cited revision (`b5pages/<oldid>__<stem>.txt`); it lies in one paragraph, has at least 15 characters and no ellipsis. In addition every source was re-opened the way `data/disputed-areas/verify_quotes.py` does (Wikipedia by `oldid`, other pages by plain GET with the verifier's User-Agent) and all 190 quotes were found with the verifier's `squash()`; no quote crosses a reference marker.

## Sources and evidence levels

- 163 rows: Wikipedia at pinned revisions (en 158, es 3, fr 2) — `secondary`.
- 9 rows: CIA World Factbook "Disputes - international", through the `factbook/factbook.json` mirror at the commit batch 4 pinned (2023-05-25) — `secondary`, and dated 2023.
- 8 rows: other secondary pages — New Vision, Kampala, 17 December 2007 (Rukwanzi, 2 rows); The New Humanitarian, 31 January 2006, through its Wayback copy because the live page returns 403 (Sabanerwa, 2 rows); tothevictoriafalls.com, a history site whose text is "adapted from" a 2017 book by Peter Roberts (Sindabezi, 4 rows — self-published, the weakest source in the batch).
- 10 rows `primary` (official pages): ICJ case pages 167 and 185 (Pedra Branca ×3, Sapodilla ×1); TAAF (Scattered Islands ×2, in French); Finnish Transport Infrastructure Agency / Väylä (Saimaa Canal ×2); Japan's Cabinet Secretariat (Senkaku ×1); UK FCDO travel advice (Somaliland ×1).
  - The ICJ texts quoted are the Registry's case overviews ("provided for information only"), not the judgments or orders themselves.
  - The FCDO page is a third government's description of Somaliland's entry practice, not Somaliland's own rule.
  - The Cabinet Secretariat page is one party's statement of its own control.
- Archived copies of the official pages were not recorded: the Wayback Machine answered 429 to every lookup at the end of the session. These pages (GOV.UK, TAAF, Väylä, ICJ) will change; add archive URLs when they are entered in `sources.csv`.
- Opened and saved but not quoted (available to raise evidence later): ICJ case 124 (Nicaragua v. Colombia — "The Court concluded that Colombia, and not Nicaragua, had sovereignty over the islands at … Serrana and Serranilla"), ICJ case 151 (Preah Vihear interpretation, 2013), ICJ case 130, Sovereign Limits "Zambia–Zimbabwe Land Boundary", MINURSO "Background", the second New Vision article on Rukwanzi, further Factbook country files.
- Official pages that could not be read: Japan MOFA (403), UN Peacekeeping UNMOP pages (404), Irish DFA Rockall page (moved), Taiwan Marine National Park Headquarters FAQ on Dongsha (JavaScript-only, also in its Wayback copy).

## General limits

- `traveller_access` is sourced for 12 areas only, and only two of them from an authority's own text (TAAF for the Scattered Islands, FCDO for Somaliland). Five are a judgement mapped from a descriptive sentence rather than an entry rule: Rockall, Rincón de Artigas, Šarengrad/Vukovar, Saimaa Canal, Senkaku (see each area).
- `area_km2` was entered only when the quoted figure is for the area as named in the register. Where the source gives a figure for one component only, it is in these notes and not in the CSV.
- Several `parties` values state a role that rests on another row's quote for the same area, not on the `parties` quote itself: `pratas` (Taiwan administers — `on_the_ground`), `sapodilla-cayes` (Belize administers, Guatemala and Honduras claim — `kind`, `origin`), `sarengrad-vukovar-islands` (Croatia claims — `kind`), `shaksgam` (China administers — `kind`), `serranilla` (Colombia holds — `on_the_ground`), `sool-sanaag-cayn` (holds most — `origin`), `penon-de-velez-de-la-gomera` (Spain holds — `on_the_ground`).
- Infobox fragments used as quotes (short but verbatim): Pratas, Rockall, Sakteng, Senkaku, Shaksgam, Siachen and Sool/Sanaag/Cayn `area_km2`; Siachen `parties`; Situngu `inhabited`.

## Kind differs from the lead (5 areas)

| area | lead | entered | why |
|---|---|---|---|
| `perejil` | paper_claim | own_regime | Two sources say the islet is unoccupied and claimed by both after a US-mediated return to the status quo ante; there is no administering state on the ground. The Perejil Island article itself says "administered by Spain" — the sources disagree. Owner's call. |
| `point-20` | line_position | no_agreed_boundary | The page says the boundary there "has not been determined"; Malaysia's line is a unilateral 1979 map. `paper_claim` is also arguable (Singapore administers the reclaimed land). |
| `pratas` | islets_for_maritime_zone | de_facto_state | The sources show a PRC claim to an island governed by the Republic of China, not a dispute over the surrounding sea; same reading as `kinmen-matsu` in batch 3. |
| `prevlaka` | line_position | own_regime | The page says the 2002 agreement "demilitarized Prevlaka" and that the arrangement "still has a temporary character". The seed notes already called this defensible. |
| `rukwanzi-semliki` | line_position | own_regime | A December 2007 report says the island was demilitarised and co-administered. Stale: nothing newer was found. |

## Per area

**pedra-branca** — not sourced: `area_km2`. Lead confirmed (`resolved_recently`): the ICJ ruled in 2008; Malaysia's 2017 revision and interpretation cases were discontinued by agreement in May 2018 (ICJ: order of 29 May 2018; the Wikipedia article says the withdrawal was on 30 May and that "the 10-year period had lapsed, putting the matter to rest"). South Ledge is still open: "The status of South Ledge remains unresolved" (Middle Rocks article), and the joint technical committee reached an impasse in November 2013 — consider splitting South Ledge from the two settled features. `inhabited=garrison_only` rests on Malaysia's Abu Bakar Maritime Base on Middle Rocks; nothing was found on who stays on Pedra Branca. `traveller_access=restricted` is Pedra Branca only (permit from the Maritime and Port Authority). Area available for Pedra Branca alone: "about 8,560 square metres (0.00856 km 2 ) at low tide".

**penon-de-alhucemas** — not sourced: `traveller_access`. Lead confirmed.

**penon-de-velez-de-la-gomera** — not sourced: `traveller_access`. Lead confirmed. Area converted from "about 1.9 ha".

**perejil** — not sourced: `traveller_access`. Kind differs from the lead, see table. Sources conflict on administration: Wikipedia "Under Spanish sovereignty, it is administered by Spain as one of the plazas de soberanía"; Factbook "both countries claim Isla Perejil (Leila Island), which remains unoccupied"; crisis article "the island remains unoccupied but claimed by both sides".

**pheasant-island** — all fields sourced. Lead confirmed. Area and `traveller_access` are from French Wikipedia (the English infobox figure has a reference marker inside it).

**point-20** — not sourced: `inhabited`, `traveller_access`, `area_km2`. Kind differs, see table. Whether the dispute is still live is not established: the page's latest facts are the 2003 ITLOS order and a later settlement of the reclamation case in which "the two countries reached an agreement not to deal with the issue".

**pratas** — all fields sourced. Kind differs, see table. `parties` quote covers only the PRC claim. `traveller_access=closed` rests on the Dongsha Atoll National Park article ("not open to tourism"), which cites the park headquarters; the official page could not be read. `inhabited=garrison_only` rests on a November 2020 figure (about 500 marines).

**preah-vihear** — not sourced: `inhabited`, `traveller_access`, `area_km2`. Lead confirmed. The list gives two figures, not one: a "promontory" of 0.3 km² awarded to Cambodia in 2013 and "an additional 4.3 km 2" still disputed. After the 2025 war the sources read here do not say who holds the ground around the temple or whether it can be visited; `on_the_ground` records only the ceasefire. The ICJ page for the 2013 interpretation is saved and could raise `parties` to primary.

**prevlaka** — not sourced: `traveller_access`. Kind differs, see table. The Wikipedia article carries an "update needed: what has happened since 2006?" banner; the Factbook (2023) adds that a Montenegrin official revived the dispute in October 2020.

**rincon-de-artigas** — all fields sourced. Lead confirmed. `traveller_access=open` is weak: it rests on "largely unmarked and unimpeded de facto international border", a sentence the English article sources to Google Maps (2014). Spanish Wikipedia's infobox says 273 km², its text and the other sources 237. `inhabited=yes` rests on the village (Thomaz Albornoz) built in the claimed zone.

**roc-legacy-claims** — not sourced: `inhabited`, `traveller_access`, `area_km2`; they have no meaning for this row. It is not an area but a bundle of about 25 unrelated territories, each ordinary territory of another state and several already in the register under their own ids. Suggest retiring it as an area or splitting it. The only parties named in the quotes are the ROC and the PRC.

**rockall** — all fields sourced. Lead partly contradicted: the sources name the United Kingdom (claims) and Ireland (never claimed sovereignty, rejects the UK claim) for the islet; Iceland "does not claim the rock itself" and Denmark claims continental-shelf rights for the Faroes — both are parties to the seabed dispute only ("Rockall Bank dispute" article, not quoted in the CSV). `traveller_access=expedition_only` is inferred from the landings record (146 people ever); no rule was found.

**rukwanzi-semliki** — not sourced: `traveller_access`, `area_km2`. Kind differs, see table; the co-administration is from a report of 17 December 2007 and the present state is unverified. The Wikipedia infobox says "Administration Democratic Republic of the Congo, Claimed by Uganda" and the text "On August 12, 2007, Congo occupied the area"; the Factbook (2023) says the island "is claimed by both countries". Figures for the island alone: "an area of 12 sqkm and home to about 3,000 people" (New Vision) against "approximately 1000 fishermen" (Wikipedia). Should be split: nothing read here describes the Semliki River valley except "tension and violence on Lake Albert over prospective oil reserves at the mouth of the Semliki River".

**russian-ranges-kazakhstan** — not sourced: `inhabited`, `traveller_access`, `area_km2`. Lead confirmed for Sary-Shagan. "And others" is not covered: the only other site named is the Kambala air base. On access the article contradicts itself ("In practice, the site is open to all who wish to visit it" / official permission "takes many months"), so nothing was entered. The 81,200 km² figure is the Soviet-era range, not the leased part.

**sabah** — not sourced: `traveller_access`, `area_km2`. Lead confirmed.

**sabanerwa** — not sourced: `inhabited`, `traveller_access`, `area_km2`. Lead confirmed. Both sources say "two-kilometre-square", which may mean 2 km² or 2 km by 2 km. "Rufunzo Valley" appears only in the title of the Wikipedia list row; the Factbook and the news report say Rukurazi valley. `on_the_ground` is from January 2006.

**sadr-free-zone** — not sourced: `traveller_access`, `area_km2`. Lead confirmed. The page says "Access is difficult even for Sahrawis", which is not an entry rule.

**saimaa-canal** — not sourced: `inhabited`, `area_km2`. Lead confirmed. `traveller_access=open` rests on an unsourced Wikipedia sentence (passports needed, no Russian visa for transit); the Väylä page speaks only of merchant vessels ("Access allowed to merchant vessels from all countries"). Re-check before use. The 2010 lease no longer includes Maly Vysotsky Island.

**sakteng** — not sourced: `inhabited`, `traveller_access`. Lead confirmed.

**sapodilla-cayes** — not sourced: `traveller_access`, `area_km2`. Lead confirmed. New: the ICJ case Belize v. Honduras is pending and Guatemala was admitted as a non-party intervener on 19 March 2026. The 15,618 ha in the infobox is the marine reserve, mostly sea.

**sarengrad-vukovar-islands** — not sourced: `inhabited`, `area_km2`. Lead confirmed. Overlaps `croatia-serbia-danube-pockets` (batch 2), which uses the same article and the same passage for `kind`. `traveller_access=open` describes Vukovar Island only (2006 local agreement, summer daytime, organised boats). Figures: Šarengrad "9 km 2"; the Vukovar infobox says 3.2 ha with a length of 3,800 m, which cannot both be right.

**saudi-kuwait-neutral-zone** — not sourced: `inhabited`, `traveller_access`. Lead confirmed, with a contradiction: the "Kuwait–Saudi Arabia border" article says the partition was ratified in 1969–70, "at which point the Kuwait-Saudi border was finalised"; the list and the Factbook put the settlement in 2019. If the first is right this was settled long before 2015. The 5,770 km² is the former zone without Qaruh and Umm al Maradim.

**saudi-uae-border** — not sourced: `inhabited`, `traveller_access`, `area_km2`. Lead confirmed.

**scarborough-shoal** — not sourced: `area_km2` (the 150 km² figure includes the lagoon). Lead confirmed.

**scattered-islands-mozambique-channel** — not sourced: `area_km2`. Lead confirmed; `paper_claim` is equally defensible and is what batch 2 chose for `glorioso-islands`. The `origin` quote is about Bassas da India; the `on_the_ground` quote is about Juan de Nova. Per-island areas: TAAF gives Europa 30 km² and Juan de Nova 5 km²; English Wikipedia gives 28, 4.8 and 20 ha of islets for Bassas da India.

**senkaku** — all fields sourced. Lead confirmed. `traveller_access=closed` although the page's word is "restricted": the same sentence says landing requests are denied even to local authorities.

**serranilla** — not sourced: `traveller_access`, `area_km2`. Lead partly contradicted: the article names Colombia, Jamaica and the United States and says Honduras's claim was resolved by treaty; the Wikipedia list says Honduras "continues to claim the two banks in its constitution"; the Factbook (2023) lists Colombia, Honduras, Nicaragua, Jamaica and the US. The list treats Bajo Nuevo and Serranilla as one row (`bajo-nuevo` is in batch 1).

**shaksgam** — not sourced: `inhabited`, `traveller_access`. Lead confirmed. The infobox says 5,180 km², the lead sentence "approximately 5,200".

**shebaa-farms** — not sourced: `inhabited`, `traveller_access`. Lead contradicted on Syria: the article's lead says "Syria agrees with [the Lebanese] position", while a later paragraph says Assad declared in 2011 that both areas "were Syrian territory and not Lebanese". The 22 km² is given for Shebaa Farms; the page calls the Kafr Shuba Hills the northern part of the farms (in a sentence tagged "citation needed") and gives the length as both 9 km and 11 km.

**siachen** — all fields sourced. Lead confirmed. Area figures vary: 2,500 km² (entered), 2,550, 2,600, about 700 for the glacier system alone, and 9,600 in the Wikipedia list.

**sindabezi** — not sourced: `inhabited`, `traveller_access`, `area_km2`. The one narrative source says the dispute (1994–95) ended: "It was eventually confirmed that the line of the border ran along the deep-water channel", with no date. If so it was settled well before 2015 and the area is a candidate for `ignore`; `resolved_recently` could not be supported. Sovereign Limits (saved, not quoted) says the two governments "are currently working towards resolving several disputed islands in the Zambezi River". The Wikipedia list row carries only the two country names and "Tourist island on the Zambezi River".

**sir-creek** — not sourced: `traveller_access`, `area_km2`. Lead confirmed.

**situngu** — not sourced: `traveller_access`, `area_km2`. Lead confirmed. The article's source for the 2018 treaty is titled "Namibia revives treaty with Botswana" (March 2022), so ratification may have come later; not checked.

**somaliland** — all fields sourced. Lead confirmed; add Israel's recognition of 26 December 2025. The area entered (176,120 km²) is the claimed territory; a footnote on the same page gives about 152,483 km² under de facto control after 2023. FCDO advises against all travel except to three regions; `open` reflects the visa on arrival at Hargeisa only.

**sool-sanaag-cayn** — not sourced: `traveller_access`. Lead partly contradicted: Puntland does not hold the area together with the North Eastern State; it "does not recognize the existence" of that state and claims the same land. The 24,642 km² is the infobox figure for the North Eastern State. Overlaps `somaliland`, whose claimed area includes it.
