# Historical boundary datasets: CShapes 2.0 and Cliopatria

**Research note, not normative.** Issue: [#30](https://github.com/uncovering-world/travel-regions-extraction/issues/30) (a canon for every year from 2000). Compiled on 2026-10-22 for the owner's question whether CShapes 2.0, and then Cliopatria, can help the canon; sources were opened and the data downloaded that day.

How to read it:

- A quote or a field name means the source states it.
- **[C]** marks a check made on the downloaded data during this review, not a published figure.
- **[I]** marks an inference of the review.

## Question

Can either dataset serve the canon as (a) a geometry source, (b) a source of facts about who holds an area, or (c) a dated list of country-level changes for the yearly series of #30? An answer of "yes" to (a) or (b) would make it a candidate input under R045/D039; "yes" to (c) would make it a cross-check for #30.

## CShapes 2.0

Publisher: International Conflict Research, ETH Zürich. Read 2026-10-22.

- Scope, from the [dataset page](https://icr.ethz.ch/data/cshapes/): "CShapes 2.0 maps the borders and capitals of independent states and dependent territories from 1886 to 2019". Two variants follow the Gleditsch–Ward or the Correlates of War list of states. Border changes "were coded based on the Territorial Change Dataset by Tir et al (1998)". Licence: "Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License".
- End of coverage, from the [ChangeLog](https://icr.ethz.ch/data/cshapes/ChangeLog.txt): "2020-06-07 (2.0) * Updated CShapes until December 31, 2019." No later version is listed.
- Coding rules, from the [codebook](https://icr.ethz.ch/data/cshapes/CShapes-2.0_Codebook.pdf) (a coders' guide by G. Schvitz, dated 2018-12-21): "we only code de jure changes in territory and sovereignty"; excluded are "Territorial changes below 10'000 sqkm", unrecognised exchanges that were later reversed, "de-facto secession[s] … that lacked international support and recognition", and wartime changes reversed after the war; where maps conflict "due to conflicting territorial claims … we opted for the map that corresponded most to the region's current borders". The guide lists the fields `status`, `ruledby` and `b_def`.
- Paper: Schvitz et al. 2022, "Mapping The International System, 1886-2017: The CShapes 2.0 Dataset", *Journal of Conflict Resolution* 66(1):144–61.

Checks on the downloaded GeoJSON (`CShapes-2.0.geojson`, 710 rows):

- [C] The published file has no `status`, `ruledby` or `b_def` fields — only name, area, capital, `gwcode` and dates.
- [C] 181 units are in force on 2019-12-31, with about 195,000 vertices in all.
- [C] Not every place is covered: no Andorra, Monaco, Liechtenstein, San Marino, Vatican, Seychelles, Samoa or Tonga. Denmark measures 42,630 km², so Greenland is not in it, under Denmark or on its own. China's polygon is unchanged from 1950 to 2019, and there are no separate Hong Kong or Macao rows. Western Sahara is Morocco's from 1979 (ChangeLog, 2011-05-03: "Coded Western Sahara entirely as part of Morocco as of August 5, 1979").
- [C] Crimea moves to Russia on 2014-03-18: Ukraine goes from 597,503 to 571,667 km². That does not match the codebook's "only de jure" wording.
- [C] Thirteen rows start between 2000 and 2019: Saudi Arabia and Yemen in 2000, Indonesia and East Timor in 2002, Myanmar in 2005 (same area; the capital changes from Rangoon to Naypyidaw), Serbia and Montenegro in 2006, Serbia and Kosovo in 2008, Sudan and South Sudan in 2011, Russia and Ukraine in 2014.

## Cliopatria (Seshat)

Publisher: Seshat Global History Databank. Read 2026-10-22.

- Scope, from the [Seshat docs page](https://seshat-global-history-databank.readthedocs.io/en/latest/cliopatria.html) and the [repository README](https://github.com/Seshat-Global-History-Databank/cliopatria): "worldwide polities from 3400BCE to 2024CE"; "only one version of the territory held by past polities"; rows carry `Name`, `FromYear`, `ToYear` (integer years), `Area`, `Type` (POLITY or RELATION), `Wikipedia`, `Wikidata`, `SeshatID`, `Components` and `MemberOf`. Licence (`LICENSE.md`): CC BY 4.0. Latest release v0.2.1, published 2026-10-03.
- Construction, from the paper (Bennett et al. 2025, *Scientific Data* 12:247, [doi:10.1038/s41597-025-04516-9](https://doi.org/10.1038/s41597-025-04516-9)): the dataset was traced from a set of raster images (Tollefson, "508 World Maps", 2014) drawn in a Robinson projection; "we automatically smoothed the resulting polygons and their shared borders to a 0.07° resolution"; "With rare exceptions … polities occupy at least 5000 km² and have a duration of at least 50 years"; "The image set began in 3400BCE and ended in 2014CE but we extended the dataset to 2024CE"; the images depict years "irregularly".

Checks on the downloaded data (`cliopatria_polities_only_v021.geojson` from the v0.2.1 zip, 13,797 rows):

- [C] After 1990 the rows start only in the frame years 1992, 1996, 2000, 2006, 2014 and 2024, so South Sudan (independent in 2011) first appears in 2014. 195 POLITY rows are in force in 2024.
- [C] Point tests (approximate points inside each city; the coordinates were not checked against a source) give these errors in 2024: Stepanakert falls in Armenia (also in 2000–2020), Bamako in the "Mali Federation", Vaduz in Switzerland. Laayoune, Dakhla and Sukhumi fall in no polity. Malé and Apia fall in nothing, since those islands are missing.
- [C] Between 2014 and 2023 Simferopol lies in both Ukraine and the Russian Federation, so the polygons overlap.
- [C] Names in force in 2024 include "Kingdom of Great Britain", "Estado Novo", "Mujahideen" and "Gaza/Hamas".

## What this means for the canon [I]

1. **Geometry: neither.** Both are country-level and coarse (CShapes about 195k vertices for the world; Cliopatria smoothed to 0.07°, about 8 km), would not align with the GADM substrate, and leave places uncovered. Cliopatria also has overlaps. CShapes' NC-SA licence would also carry over to any derived data.
2. **Facts about who holds an area: neither.** Each records one answer per place, chosen by its own convention: CShapes' Western Sahara and Crimea, Cliopatria's Nagorno-Karabakh and its gaps. Under D065 the canon builds points of view from sourced claims. At most these datasets are leads, in the same role as Natural Earth.
3. **A cross-check for #30: CShapes slightly, Cliopatria no.** CShapes gives a day-dated list of large country-level changes from 2000 to 2019. That can catch a missed large event in the yearly series. Its 10,000 km² threshold drops almost every case the canon actually turns on: exclaves, the Baikonur plots, Hans Island, the Cooch Behar enclaves. Nothing after 2019 is covered, and the dates still have to come from the treaties and acts themselves. Cliopatria's frame years are too sparse after 1990 to date anything.
4. Cliopatria's `Wikidata` ids per polity and period could help match historical names. Nothing in the canon needs that now.

## Not retrieved or not checked

- The full CShapes 2.0 paper (JCR) and the per-country documentation the codebook describes; whether the Crimea coding is explained there.
- The Correlates of War variant of CShapes; only the default GeoJSON was examined.
- The Zenodo record of Cliopatria; the GitHub release v0.2.1 was used.
