# Land GADM 4.1 does not draw

## Question

Which land does the release's substrate leave out? GADM 4.1 lacks some islands (Chichijima, Fatu Hiva, Rocas Atoll, Malpelo, San Pedro Mártir were found by hand on 2026-11-19, see [the boundary providers note](../../docs/research/2026-11-19-boundary-providers.md)). A traveller's pin on such land lies in no region. This experiment lists all of it at once, instead of one island at a time, so that the release can add what matters through own geometries (D062; an empty `donors` adds land only where GADM has none, D074 (4)).

Runs under the product profile `S1-product-v1`. Assumes no pending proposal.

## Related

D062, D074 (R060), D074 (4) (the land rule); issue #22 (release draft); `docs/status.md` (open item "islands GADM 4.1 does not draw").

## What would change our mind

- If the missing land is a handful of islands, they are added by hand as own geometries, as planned.
- If it is thousands of pieces with real area, adding them one by one is wrong, and a general rule is needed (the land source's attribution for land no unit draws). That is an owner's choice.
- If a missing piece lies near a catalogue point (R060's test: within 1 km), it must be added before the first release whatever its size.

## Method

Every polygon part of World Polygons 11.4 (layer `DoS_WP_11_4`, the land-only source pinned in `data/custom-geometries/sources.json`) of at least `MIN_KM2` is tested at a point inside it against GADM 4.1's units (the GeoPackage's R-tree, then point-in-polygon). Parts that no unit contains, and that no own geometry's land file covers, are tested again by area: the part minus every GADM unit and own land file that meets it; it is missing land if at least half of it, and at least `MIN_KM2`, is uncovered (a single point can fall in a lagoon GADM leaves out: the first run counted the Chatham Islands and Orkney this way). Each is listed with its World Polygons country (`GENC_3`, `ISO_3166_1`), area and point, and the number of TYR catalogue points (`~/tyr-exports/real-points-2026-11-19.csv`, read only) within 1 km of it.

```bash
nice -n 10 flock ~/.cache/tyr-heavy.lock uv run --no-project --with shapely --with pyproj python experiments/missing-land/run.py
```

Outputs: `outputs/missing.csv` (every missing part) and `outputs/summary.json`.

## Result

Run of 2026-11-23 (`outputs/summary.json`). Of 203,744 World Polygons parts of at least 0.01 km², **88,219 parts with 11,903 km² of land** are not drawn by GADM 4.1 (or by an own land file). By size of the uncovered land:

| uncovered km² | parts |
|---|---:|
| under 0.1 | 74,542 |
| 0.1 to 1 | 12,490 |
| 1 to 10 | 1,072 |
| 10 and more | 115 |

The most land is in Canada (2,645 km², 26,914 parts, mostly small Arctic islands), Indonesia (1,064), Greenland (1,016), Russia (838), Bangladesh (637, coastal chars), Norway, the United States, Finland and Chile. The largest single pieces: the Prince Edward Islands (South Africa, 297 km²), Enggano (Indonesia, 246 km² uncovered), Bangladesh's coastal chars, Valdés-area coast of Argentina, Tokelau's atolls, Fatu Hiva (83 km²), Chichijima (24 km²).

160 parts (161 km²) lie within 1 km of a catalogue point. Most of them are not islands but harbour and reclaimed coast that World Polygons draws and GADM's coastline leaves out (Venice, Trieste, Helsinki, Karlskrona, Tromsø, Stavanger, Panama City's old town); the rest are islands (Fatu Hiva, Chichijima, Small Zayatsky in the Solovetsky Islands, Bahrain's reclaimed land).

## Conclusion

The missing land is not a handful of islands: it is tens of thousands of pieces, a thousand of them over 1 km², and much of it is coastline that differs between the two sources rather than islands. Adding them one by one as own geometries is the wrong tool. A general rule for land no GADM unit draws is needed; that is the owner's choice (a proposal, not adopted). The 160 parts near catalogue points must be covered before the first release whatever rule is chosen (R060).

## Status

Concluded; the rule is waiting for the owner.
