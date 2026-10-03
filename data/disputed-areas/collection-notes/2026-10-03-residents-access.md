# register-out.csv — notes (sources read 2026-10-03)

12 rows: `inhabited` 8, `traveller_access` 3, `kind` 1, `parties` 0, `holder_since` 0.

Self-check (`reg/build.py`): each source was re-fetched (Wikipedia by `oldid`, other pages by URL), stripped
and normalised the way `verify_quotes.py` does, and every quote is a substring of its source: 12 of 12.
A stricter check (quote does not span a citation marker or a paragraph/table-cell break) passes for 11;
the exception is `moselle-condominium` (see below). The web search budget of the session was exhausted
before this task started, so sources were limited to Wikipedia (pinned revisions, found through its own
search API) and pages whose URL was known or guessable. That is why most gaps below remain.

## Rows that are weak — read before importing

- `diego-garcia / traveller_access = closed` (primary, biot.gov.io). The register already has `restricted`
  (gov.uk); the importer will refuse this row until the old one is deleted. The passage says access to
  Diego Garcia is only for people connected to the base or the administration; the same page says permits
  for the rest of BIOT are paused since 31 March 2026. `closed` is my reading for an ordinary visitor.
- `tin-bigha / traveller_access = open`. The passage says open 24 hours "for Bangladeshis in the enclave";
  it does not state the rule for any other visitor, nor who checks (the Dahagram–Angarpota article says the
  BSF controls the gates, but tagged "citation needed").
- `palanca-road / traveller_access = open`. Ukrainian Wikipedia: Ukrainian jurisdiction, road-traffic
  control only, no border or customs control on the transferred section. Secondary and undated; wartime
  practice not checked.
- `ladakh-lac-buffer-zones / inhabited = garrison_only`. The passage is about the Depsang Plains only, one
  of the four friction areas the entry covers.
- `shaksgam / inhabited = no`. The passage says "mostly uninhabited", in passing, in the Kashmir conflict
  article. The Shaksgam River article says yak herdsmen from Shimshal use the area as winter pasture.
- `minerva-reefs / inhabited = no`. Inferred from "two submerged atolls"; no passage says "uninhabited".
- `caspian-islets-ukatny / inhabited = no`. Covers Ukatny only; nothing found for Zhestky and Maly
  Zhemchuzhny (no Wikipedia articles).
- `moselle-condominium / inhabited = no`. The quote "Bevölkerung unbewohnt" is an infobox label and its
  value: two adjacent table cells, not a sentence. It matches after whitespace normalisation.
- `antarctic-peninsula-overlap / inhabited = yes`. Rests on Villa Las Estrellas (families of base staff, a
  school until 2018); whether that counts as resident civilians is a judgment.
- `abyei / inhabited = yes`. The passage speaks of "the residents of the Abyei Area" in a legal context; no
  population figure was found. UNISFA pages (primary) only mention displacement in 2011.
- `bhutanese-enclaves-tibet / kind = occupied_or_annexed`. The passage says China annexed Darchen in 1959;
  nothing found saying that Bhutan still claims the enclaves or that others regard them as occupied.
  `paper_claim` is the alternative if a current Bhutanese claim is sourced.

## Not established (no row)

inhabited
- `ilemi-triangle`: the article only describes nomadic herders (Turkana, Toposa, Nyangatom) moving through
  and grazing; by the rule that seasonal use is not "yes", no row. Lead: Kibish division, Turkana County
  (population 6,056 in a table of the Turkana County article) — whether it lies inside the triangle is not
  stated there.
- `tort-kocho-road`: 24.kg and the Tort-Kocho article describe a 10 m roadbed with a security strip at a
  road junction; nothing about residents.

traveller_access
- `akrotiri-dhekelia`, `guantanamo-bay`, `saimaa-canal`: the register already has secondary rows; no primary
  passage found. sbaadministration.org home page and gov.uk Cyprus advice say nothing on entry to the SBAs;
  the US Navy installation site and travel.state.gov refused the request (403); the vayla.fi pages give the
  inspection points but no visa rule.
- `moldauhafen`: neither the English nor the German article says anything about public access.
- `russian-ranges-kazakhstan`: contradictory and not about the leased part. Sary Shagan article: "In
  practice, the site is open to all who wish to visit it" (about unguarded abandoned sites) and "From 2005,
  entry into the city of Priozersk is carried out without a permit"; Priozersk article: "The town is closed
  to visits by foreign citizens."
- `suleyman-shah-tomb`: only statements about the pre-2015 site (visitors had to carry passports; reopened
  to visits after the 2007 fortification agreement). Nothing on the present site near Ashme.
- `tiwinza`: Spanish Wikipedia "Tiwinza (Perú)" (oldid 169256370) says the road from Ecuador was agreed in
  2022 and "Todavía no se han construido monumentos ni se ha desminado el área" — a condition, not an
  access rule.

kind and parties
- `armistice-no-mans-lands`: parties already in the register (Latrun). For kind, the Latrun article says
  "occupied by Jordan at the edge of a no man's land between the armistice lines" (1949–1967) and under
  Israeli control since 1967; no passage says how the areas are regarded today, and the entry covers three
  different places. Left open rather than choosing between `occupied_or_annexed` and `paper_claim`.
- `doi-lang`: the only statement is a table row in "List of territorial disputes" (oldid 1377757742):
  cells "Doi Lang", "Myanmar", "Thailand", no description. Not a passage; no row for parties or kind. No
  English or Thai Wikipedia article on the dispute was found.
- `bhutanese-enclaves-tibet / parties`: already in the register.

holder_since
- `kafia-kingi`: no date of uninterrupted holding can be stated. Sources agree the area was transferred to
  Darfur in 1960 (Rift Valley Institute, "The Kafia Kingi Enclave", 2010: "In 1960 it was transferred to
  Darfur"; its landing page https://riftvalley.net/publication/kafia-kingi-enclave/: "currently under the
  administration of South Darfur state, in Sudan"), but the Kafia Kingi article says South Sudanese forces
  "have briefly controlled large portions", "South Sudan–Sudan relations" (oldid 1377684449) says "largely
  … controlled ever since then [2005] by Sudanese forces", and "Geography of South Sudan" says South
  Sudanese troops "were present there for several times". None dates the last interruption.

## Housekeeping
- Working files are in `facts3/reg/` (fetch log `wiki.log`, saved pages in `web/`, `wiki/`, `vcache/`).
- `facts3/wiki.log` belongs to another task running in the same directory; one early command of mine
  truncated and wrote to it before I switched to `reg/`. Its content from that moment may be incomplete.
