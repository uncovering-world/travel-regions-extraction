# Common names of regions (R062, D076)

The name a traveller reads, beside the formal name in `regions.csv` `name` (ISO 3166-1's English short name for coded regions, which can carry a claim: "Taiwan, Province of China").

- `cldr-48.0.0-en-territories.json` — Unicode CLDR 48.0.0, English territory names, copied unchanged from https://raw.githubusercontent.com/unicode-org/cldr-json/48.0.0/cldr-json/cldr-localenames-full/main/en/territories.json (read 2026-11-21; sha256 158c1d575308f7e46912edbeda435c8fe2ef5dad280798231f3a432e406b1807; Unicode License v3). The common name of a region with an ISO 3166-1 code is CLDR's plain name for that code; where that name carries a qualifier ("SAR" or a " - " suffix) it is the `-alt-short` form, else the `-alt-variant` form (D077): Hong Kong, Macao, Congo (DRC), Congo (Republic). It covers all 248 coded regions of the draft.
- `common_names.csv` — regions without a code (`area/`, `rule/`) whose register name is a description rather than a name: the title of the English Wikipedia article (or redirect) on that place, checked on 2026-11-21 through the Wikipedia API. A region not listed keeps its register name as its common name.
