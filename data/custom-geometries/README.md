# The canon's own geometries

Outlines the canon needs where the substrate (GADM 4.1) cannot represent a place (R047, D059, D062): one GeoJSON file per place, each with its source, whose line it is, and its licence in its properties. **Status: a draft built on 2026-10-04 for review; the choices marked below are proposals, not decisions.**

## The rule (D062, R047)

Sources are ranked by whose line they draw:

1. a line one of the parties publishes itself (an official national boundary dataset, a map annexed to a treaty or ceasefire agreement);
2. a line the parties agreed, drawn precisely by a neutral publisher (here: the US Department of State's World Polygons);
3. OpenStreetMap;
4. Natural Earth v5.1.2.

A place takes the highest-ranked source that has a polygon of it. The files are the source's geometry unmodified: every input is already WGS84 longitude/latitude, so nothing is reprojected; where a source draws a place as several features they are merged by a plain union; an OpenStreetMap relation is assembled from its member ways (outer rings minus inner rings). Nothing is cut out of a larger feature and nothing is clipped. Two exceptions are explicit in `sources.json`: an outline drawn from the boundary points a document lists (a transcription in `documents/`, straight lines between the points, river edges along a pinned OSM river line, the areas the document excludes cut out), and a clipping mask (`extend`) unioned with a source's polygon so that the clip to the donors takes all donor land on one side of the source's outline; a mask's edges are never boundaries.

**Clipping is the consumer's job.** GADM's licence forbids redistribution, so the clip to the substrate is not done in these files. `donors` lists the regions (ids of `experiments/release-draft/release/regions.csv`) whose GADM units a place may take land from. The consumer keeps the part of a geometry that lies on the donors' GADM units, on the receiving region's own units, or on no GADM unit at all (islets GADM lacks), and drops the rest, so a place never takes land from a neighbour that is not a donor. An empty `donors` means the place only adds land where GADM has none.

## Files

- `sources.json` — the maintained input: pinned inputs (URL, sha256, version, licence, date read) and, per place, the input and features used, the rank, whose line it is, and notes.
- `sources.csv` — the same per-place table, readable; written by `build.py`.
- `<place>.geojson` — one per place; properties repeat the row and add the sha256 of the input, the operation applied and the source features' own attributes.
- `build.py` — rebuilds the GeoJSON files and `sources.csv` from the pinned inputs. Inputs are downloaded into `cache/` (gitignored) and checked against their sha256; a changed upstream file stops the build. OpenStreetMap is read by an Overpass attic query at 2026-10-04T06:57:51Z and cached in a canonical form (elements sorted, the server's run-time header dropped), so a fresh download hashes the same. The State Department's 3.5 GB `WorldPolygons11_4.gpkg` is extracted from its 2.4 GB zip by HTTP range requests, or taken from `CTR_WORLDPOLYGONS_GPKG` after its sha256 is checked. `koalou.geojson` is kept as accepted (D061) and only its sha256 is checked.

```bash
python3 data/custom-geometries/build.py           # needs shapely 2
python3 data/custom-geometries/build.py --check   # rebuild in memory, compare byte for byte
```

Built and checked with shapely 2 / GEOS from the project's scratch environment; a different GEOS may write the unions' vertices in a different order.

## Places

| Rank | Place → region | Whose line | Licence |
|---|---|---|---|
| 1 | `south-ossetia` → area/south-ossetia | Georgia's official unit "Provisional Administration" (GE48), COD-AB | CC BY-IGO |
| 1 | `ye-socotra` → rule/ye-socotra | Yemen's governorate of Socotra (YE32), COD-AB | CC BY-IGO |
| 1 | `koalou` → area/koalou | Burkina Faso's and Benin's national outlines: the land both include (D061) | CC BY-IGO |
| 1 | `baikonur` → area/baikonur | the lease treaty's Appendix 2 (Plot No. 1, 31 boundary points, as restated in 2017), transcribed in `documents/`; river edges along OSM's Syr Darya | official treaty text; river edges ODbL 1.0 |
| 2 | `armistice-no-mans-lands` → area/armistice-no-mans-lands | 1949 armistice lines, US DoS | US government work |
| 2 | `korean-dmz` → area/korean-dmz | 1953 Armistice MDL and DMZ limits, US DoS | US government work |
| 2 | `undof-zone` → area/undof-zone | 1974 disengagement lines A and B, US DoS | US government work |
| 2 | `guantanamo-bay` → area/guantanamo-bay | lease boundary, US DoS | US government work |
| 2 | `bir-tawil` → area/bir-tawil, `halaib-triangle` → EG | the political boundary (Egypt's) and the administrative boundary (Sudan's), US DoS | US government work |
| 2 | `ilemi-triangle` → area/ilemi-triangle | Kenya–South Sudan administrative and provisional boundaries, US DoS | US government work |
| 2 | 14 islets: `sapodilla-cayes`, `hans-island`, `doumeira-island`, `bassas-da-india`, `europa-island`, `glorioso-islands`, `juan-de-nova`, `matthew-hunter`, `mbanie`, `biot`, `senkaku`, `dokdo`, `scarborough-shoal`, `wake` | the coastline, US DoS | US government work |
| 3 | `cyprus-buffer-zone`, `gornja-siga`, `kuril-islands`, `somaliland`, `kalapani` → IN | OpenStreetMap mappers | ODbL 1.0 |
| 3 | `siachen`, `demchok` → area/indian-jammu-kashmir-ladakh | OSM (Siachen's outline is a later Natural Earth edition imported into OSM, extended east by a clipping mask to GADM's NJ9842–Karakoram Pass line, since India holds the whole glacier; Demchok is OSM's India-controlled western sector) | ODbL 1.0 |
| 3 | `bhutan-china-north` → BT | OSM: Bhutan-controlled part of the northern disputed area | ODbL 1.0 |
| 3 | `bajo-nuevo`, `serranilla` → CO; `penon-de-alhucemas` → ES; `rockall` → GB; `bird-island` → VE | OSM coastlines | ODbL 1.0 |
| 4 | `east-jerusalem`, `shebaa-farms`, `western-sahara-moroccan-controlled` | Natural Earth editors | public domain |

Each row of `sources.csv` gives the publisher, URL, version, feature ids and notes.

### Licences

- **ODbL 1.0** (OpenStreetMap contributors; share-alike — a database made from these files must stay under ODbL): `bajo-nuevo`, `bhutan-china-north`, `bird-island`, `cyprus-buffer-zone`, `demchok`, `gornja-siga`, `kalapani`, `kuril-islands`, `penon-de-alhucemas`, `rockall`, `serranilla`, `siachen`, `somaliland`; the river edges of `baikonur`.
- **US government work**, not subject to US copyright (17 U.S.C. § 105; World Polygons metadata): the 21 rank-2 files.
- **CC BY-IGO** (HDX COD-AB; attribution required): `south-ossetia`, `ye-socotra`, `koalou`.
- **Official treaty text**, no licence stated: the boundary points of `baikonur`.
- **Public domain** (Natural Earth): `east-jerusalem`, `shebaa-farms`, `western-sahara-moroccan-controlled`.

## Readings of the rule to review

- **Rank 2 for the State Department.** Its World Polygons are used where the line is an armistice, disengagement or lease line, and for islets, where the line is the coastline nobody contests. Bir Tawil, Halayib and Ilemi are bounded by two lines where, on this reading, the parties dispute which one is the boundary rather than where each runs; they are ranked 2 on that reading, which is not verified. Its polygons for Siachen, Demchok and Kalapani are its own lines between unagreed claims, so they are not used. For Guantanamo and Wake the United States is a party, but the dataset disclaims being the US view, so they stay at rank 2.
- **No cutting.** Where the State Department draws a place only as a part of a bigger polygon (the southern Kurils inside Japan, Bajo Nuevo and Serranilla inside Colombia, Rockall inside the United Kingdom, Aves inside Venezuela, Peñón de Alhucemas inside the plazas de soberanía, the Mount Scopus enclave inside Israel), that part was not cut out; the next rank was used. The Mount Scopus enclave (about 1 km²) is therefore missing from `armistice-no-mans-lands`.
- **Not used as constructions:** Somalia's five north-western regions as Somaliland; OSM's Western Sahara minus the SADR-held part as the Moroccan-controlled part.

## Contradictions and open places

- **Two parties, two lines** — the canon does not choose; it cuts along both (R045). Checked on 2026-10-04:
  - East Jerusalem: the area between Israel's municipal boundary (Ministry of Interior layer `muni_il`) and the 1949 line (US State Department) is 67.1 km², within 1% of the Natural Earth polygon used here (66.6 km²); inhabited. Kept as is; the municipal layer's licence is not stated, so it is not copied here.
  - Dragonja: the 2017 award puts the boundary on the river, which is also Croatia's line; on land the two lines differ only by slivers about 9 m wide. The Natural Earth strip, which moved 0.58 km² from Slovenia to Croatia, was removed; GADM's units stand.
  - Kalapani: Nepal's 2020 line (geoBoundaries' digitisation, CC BY 4.0) and India's line (State Department) enclose 415 km² with seasonal villages (Gunji, Kuti, Nabi). How it is treated is the owner's question (a line dispute under D044, but a supported point of view, Nepal's, puts it in Nepal).
- **Bhutan (northwest valleys):** Natural Earth's polygon lies where the State Department has China and overlaps none of OSM's Bhutan–China disputed areas. The file is OSM's Bhutan-held northern disputed area; it lies in GADM's Bhutan already, so the 1,220 km² of Tibet stay with Tibet. That it is the register's Pasamlung/Jakarlung is unverified.
- **Demchok:** the canon's input gives Natural Earth's whole 2,268 km² "Demchok" to India's region; the register says each side holds its side of the Line of Actual Control. The file is OSM's India-controlled western sector (533 km²); the whole sector (OSM relation 2713466, about 1,474 km²) is the alternative.
- **Natural Earth's names swapped:** its "Bajo Nuevo" feature lies at Serranilla and its "Serranilla" at Bajo Nuevo. The membership rows of the two Natural Earth ids should be swapped when they point to these files.
- **Assignments the register contradicts:** Hans Island has been split between Canada and Greenland since 2022 (the canon gives all of it to GL); Mbanié belongs to Equatorial Guinea per the ICJ's 2025 judgment (the canon gives it to GA).

## Checks

`build.py --check` after emptying `cache/` re-downloaded every input except the World Polygons file (taken from a verified local copy), matched every pinned sha256, and reproduced all files byte for byte.
