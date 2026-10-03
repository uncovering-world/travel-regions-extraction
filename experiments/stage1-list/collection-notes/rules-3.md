# rules-out.csv — notes (read 2026-10-03)

14 rows. Saved source texts: `facts3/src/*.txt` (index in `src/index.tsv`) and `sourcing/pages/*.txt` (Wikipedia, pinned). Rebuild and self-check: `python3 build.py` (every quote is an exact substring of its saved source text; 14 kept, 0 dropped).

Limits of this run: the WebSearch budget of the session was exhausted, so nothing could be searched for. Only known URLs, links cited by Wikipedia and guessable official addresses were fetched. Most gaps below are "no source found without search", not "no such rule".

## Caveats on rows written

- **mx-southern-border-tvr (4 rows)** — the INM page refuses curl (bot challenge), so it was read in Chrome and the page body was saved by hand to `src/mx-inm-tvr.txt`. The substring check against that file is therefore not independent; re-read the page before adopting. The page is dated 03 March 2022 and was live today; `in_force=yes` rests on the page still being published, not on a dated statement. `own_rule=list` because the card's scope is given as a list of five named states; change to `own` if the group itself is treated as the rule's subject.
- **cn-hainan start_date** — 2018-05-01 is the start of the 59-country, 30-day regime (Wikipedia; Xinhua 18 Apr 2018, saved as `src/cn-xinhua-0418.txt`, says "from May 1" and that booking through a travel agency was then a condition). Earlier group-only regimes existed (Xinhua: 15-day group visa-free "since 2000", five countries added 2010). When the travel-agency condition was dropped is stated only by Wikipedia (July 2019); the NIA July 2019 press text (`src/cn-nia-1111338.txt`) widens purposes but I found no sentence on agencies in it.
- **cn-hainan in_force** — the NIA page "外国人区域性入境免签政策" is dated 2026-08-20 and lists the Hainan rule first; the quote is the page's lead-in sentence, the rule itself is in the applies_to quote.
- **sh-saint-helena start_date** — the Ordinance came into force in two steps (L.N. 2/2012 and L.N. 15/2012); which sections started on which date was not read. The value keeps both dates.
- **kr-jeju start_date** — Wikipedia only ("Refugees on Jeju Island"); no Korean official text read.
- **vn-phu-quoc start_date** — weakest row. The quote says "starting March 10"; the year 2014 comes from the article's dateline ("27/02/2014") in the same saved text. Wikipedia (Phú Quốc, oldid 1377392805) says "Since March 2014". Decision 80/2013/QD-TTg itself was not read.

## Not established (no row)

- **cn-tibet start_date** — Wikipedia pages read give no date for the Tibet Travel Permit; only "Foreign tourists were first permitted to visit in the 1980s".
- **ec-galapagos start_date** — the FAQ cites "Art.44 de la LOREG" without a date; the LOREG text could not be fetched (guessed PDF address failed).
- **gr-mount-athos start_date** — no dated statement of when the permit or the ban on women took effect. "diamonitirion ("access permit") from 1978" in Wikipedia is an image caption, not a start date; not used.
- **in-minicoy-maldivians start_date** — nothing beyond the undated Wikipedia sentence.
- **iq-kurdistan start_date** — no clean date. Candidates, not written: Wikipedia (Visa policy of Iraq, oldid 1371157882) "As March 1 2023, all travelers traveling to the Kurdistan Region of Iraq will require a visa"; Fragomen note dated March 2, 2023, "The Kurdistan Regional Government launched an electronic visa portal" (no launch date given). Neither says when the Region's own visa regime began.
- **my-labuan start_date, in_force** — no text read names Labuan. The Immigration Act text (lowpartners.com copy) and two Immigration Department pages name only Sabah and Sarawak; gov.uk describes East Malaysia as "made up of the states of Sabah and Sarawak". Absence of Labuan in these texts is not evidence that Labuan has no control. The AGC official Act page did not return the Act.
- **sh-tristan-da-cunha start_date** — tristandc.com gives no date or ordinance.
- **tj-gbao start_date** — mfa.tj page (re-read; its TLS certificate does not verify) gives no date.
- **az-nakhchivan in_force** — no current source on the Iranian exemption. Context only: gov.uk Azerbaijan (read today) says "The land borders between Iran and Azerbaijan, and Georgia and Azerbaijan are temporarily closed." Wikipedia "Visa policy of Azerbaijan" (oldid 1376563946) does not mention Nakhchivan at all.
- **ye-socotra applies_to** — nothing better than operators. travel.state.gov is behind a bot check (not bypassed). Canada, Germany, UK, Ireland, NZ advisories say nothing on tour-only access.
- **tz-zanzibar what_it_requires (immigration check from the mainland)** — no passage found in gov.uk, Canada, Ireland or NZ advisories or the Wikipedia pages; immigration.go.tz did not load.

## Contradictions with what is recorded

- **cn-hainan** — the lead (`crw_scopes.csv`) and Wikipedia say 59 countries; NIA (2026-08-20) says 61 ("61国人员入境海南30天免签政策"). The lead's "144 h" for Hong Kong/Macao groups matches NIA's "停留时间不超过6天".
- **mx-southern-border-tvr unit_level** — the recorded quote says "the four Southern States" (Wikipedia, Guatemalan citizens); INM names five: Campeche, Chiapas, Tabasco, Quintana Roo, Yucatán. The recorded applies_to (Guatemalans only) is narrower than INM: "¿Eres guatemalteco, beliceño, salvadoreño u hondureño", plus permanent residents of those four countries. The 2012 Lineamientos (DOF 08/11/2012, `src/mx-dof-lin.txt`) still said Guatemalans and Belizeans, three days, "regiones fronterizas" — an older state of the rule.
- **tz-zanzibar** — recorded: insurance is a Zanzibar-specific condition for all visitors to Zanzibar. gov.uk (read today): "All visitors to mainland Tanzania and Zanzibar, except residents, must have mandatory inbound travel insurance" and "You only need to buy insurance for your first port of entry, either mainland Tanzania or Zanzibar." So the mainland now has the same kind of requirement, and a visitor arriving from the mainland may not need the Zanzibar cover. Canada says the same (NIC for the mainland, ZIC for Zanzibar).
- **iq-kurdistan in_force=yes** — Wikipedia (same revision) also says: "As of September 2025, the Iraqi federal government's 'e-Visa Portal' is solely responsible for providing visas for foreign visitors", while visit.gov.krd is still live (© 2026). Unresolved.
- **ye-socotra** — Canada (modified 2025-12-04): "Yemeni authorities don’t issue visas at ports of entry", and Socotra "Since 2020 ... has been under the de facto control of a separatist group". This sits beside, not against, the operator-arranged Socotra permit; Germany mentions a January 2026 episode when leaving Socotra was impossible for days.
