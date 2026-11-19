# Boundary providers beyond GADM and OSM: a survey for the canon

Desk research, read 2026-11-19 (every "read" date below is 2026-11-19 unless stated). **Status: research input, not a decision.** Written by a research subagent; the main session re-checked one claim on the pinned World Polygons 11.4 (layer DoS_WP_11_4: Chichijima, Fatu Hiva, Rocas Atoll, Malpelo and San Pedro Mártir lie on its land, Roca Partida does not, 2026-11-19). The other facts carry the subagent's quotes and are not re-verified. CShapes 2.0 and Cliopatria are covered in `docs/research/2026-10-22-historical-boundary-datasets.md` and are not repeated here.

Each entry has three parts: **Facts** (quoted from the provider's own pages or files), **Probe** (what the downloaded data actually contains, from a point test described below) and **Inference** (my reading, not verified).

## How the probe was done

I downloaded the files listed under each source into the scratchpad and tested them with shapely 2.2. For each test point I asked which polygon contains it, or which lies within 0.05° of it for islands. The test points came from the English Wikipedia coordinates API (read 2026-11-19):

| Point | lon, lat |
|---|---|
| Chichijima | 142.2083, 27.0667 |
| Fatu Hiva | −138.6333, −10.4833 |
| Rocas Atoll | −33.8167, −3.8667 |
| Malpelo | −81.6076, 4.0033 |
| Roca Partida | −112.065, 18.9972 |
| San Pedro Mártir | −112.3069, 28.3803 |
| Ledra Street, Nicosia | 33.3614, 35.1744 (also 35.1790 N and 35.1700 S) |
| Lake Erie | (−81.6, 41.75), (−83.3, 41.85), (−79.3, 42.6), (−81.0, 42.2). I chose these points myself as open water on the US side. That side is an inference from the map, not checked against the international boundary. |

A hit within 0.05° shows that the dataset has *a* polygon there. It does not show that the shape is good.

## Probe summary

| Source | Chichijima | Fatu Hiva | Rocas | Malpelo | Roca Partida | S. Pedro Mártir | N. Cyprus as its own unit | Lake Erie split among states |
|---|---|---|---|---|---|---|---|---|
| geoBoundaries gbOpen ADM1/ADM0 (commit 9469f09) | yes (Tokyo) | yes (ADM0) | no | no | ADM0 only (0.004°) | no | no (6 districts of the Republic) | no (states end at the shore) |
| geoBoundaries CGAZ ADM0 | yes | yes (FRA) | no | yes | no | no | no (one "Cyprus") | – |
| FAO GAUL 2024 L1 v2.0 | yes (Tokyo) | yes (no ADM1: "Administrative Unit Not Available") | no | no | yes (Colima, ~0.03 km²) | no | no ("Lefkosia" spans both sides) | no (one "Waterbody" unit) |
| OCHA COD-AB (BRA, COL, MEX) | no COD | no COD | no | no | no | no | no COD | no COD |
| Eurostat GISCO CNTR 2024 01M | yes | yes | yes | yes | no | yes | no (one "Cyprus") | – |
| US DoS World Polygons 11.4 (repo cache) | yes | yes | yes (0.003°) | yes | no | yes | no (one "Cyprus") | – |
| Japan MLIT N03 2025 (Tokyo) | yes (小笠原村) | – | – | – | – | – | – | – |
| US Census TIGER/Line 2025 states | – | – | – | – | – | – | – | **yes** (all four points inside OH, MI or NY) |

"–" means not applicable or not tested.

## Sources

### 1. geoBoundaries (William & Mary geoLab): gbOpen, gbHumanitarian, gbAuthoritative, CGAZ
**Facts**
- Licence. The [GitHub README](https://github.com/wmgeolab/geoBoundaries) calls it "an online, open license (CC BY 4.0 / ODbL) resource"; "the only requirement for use is acknowledgement". The licence is set per country file. The API returned:
  - JPN, CYP, COL ADM1: "OpenStreetMap, Wambacher", "Open Data Commons Open Database License 1.0"
  - USA ADM1: "United States Census Bureau, MAF/TIGER Database", "Public Domain"
  - FRA ADM1: IGN, "Etalab Open License 2.0"
  - BRA ADM1: "Creative Commons Attribution 2.5 Generic"
  - MEX ADM1: INEGI, "CC BY 3.0 IGO"
  - MEX ADM0: "geoBoundaries, World Bank", CC BY 4.0, year represented 2012
  - PYF ADM0: "raster2polygon from Sentinel-2 10m Land Cover … 2021", CC BY 4.0
- Release types ([API docs](https://wmgeolab.github.io/gbWeb/api.html)): "For most users, we suggest using gbOpen, as it is CC-BY 4.0 compliant"; "gbHumanitarian files are mirrored from UN OCHA, but may have less open licensure"; "gbAuthoritative files are mirrored from UN SALB, and cannot be used for commerical [sic] purposes".
- Versions. Releases are numbered 6.0.0 (14 Sep 2023), 5.0.0 (19 Dec 2022) and earlier, "to facilitate future research replication" (README). The API has only a `current` endpoint: `https://www.geoboundaries.org/api/current/[RELEASE-TYPE]/[ISO]/[ADM]/`. Each `gjDownloadURL` it returns points at a fixed git commit, for example `.../raw/9469f09/releaseData/gbOpen/JPN/ADM1/...`. Builds are dated Dec 2023 to Feb 2024.
- Disputed areas. In the per-country files, each country is drawn as it represents itself, and "two countries may overlap in the case of contested boundaries" (README). CGAZ is "clipped to international boundaries (US Department of State), with gaps filled between borders" (README). In CGAZ "disputed areas are removed and replaced with polygons following US Department of State definitions" and "extensive simplification is performed" ([global downloads](https://www.geoboundaries.org/globalDownloads.html)).

**Probe:** see the summary table. The CGAZ ADM0 shapefile in the release zip is dated 2024-04-20.

**Inference**
- A gbOpen-based base layer would mix licences country by country, many of them ODbL. Pinning by commit hash fits the consumer's "each provider pinned at an edition".
- CGAZ is too simplified for a base layer and draws disputed areas by the State Department's lines, which the repo already reads directly. It adds nothing for the concrete cases.
- The Kalapani line in `data/custom-geometries` is already taken from geoBoundaries.

### 2. FAO GAUL 2024 (Global Administrative Unit Layers)
**Facts**
- Catalogue page ([L1 record](https://data.apps.fao.org/catalog/iso/34f97afc-6218-459a-971d-5af1162d318a)): "Administrative boundaries (level 1) – GAUL 2024", "v.2.0", published 2024-12-19, last updated 29 Jul 2025, CC BY 4.0, EPSG:4326, no stated scale. Downloads are `GAUL_2024_L1.zip` (324 MB) and `GAUL_2024_L2.zip`. A `GAUL_2024_L0.zip` returned HTTP 404, so there is no ADM0 file.
- FAO's [release page](https://www.fao.org/agroinformatics/training-and-resources/data-sets/data-set-detail/global-gaul-new-2024-release/en) (14/04/2025): "Country boundaries were processed against UN official recognized borders (UN-map 2018)".
- `GAUL2024TermsOfUse.pdf` (in the zip):
  - "You may access, download, create copies, adapt, use and re-disseminate the GAUL dataset subject to the Creative Commons Attribution-4.0 International licence"
  - but (§6) it "may include data provided by third parties which may not be redistributed or reused without the consent of the original data provider".
- `GAUL_2024_L1_Metadata.xlsx` (in the zip) names the source of each country:
  - Cyprus and Mexico: "Second Administrative Level Boundaries (SALB) programme 2024 … SALB Terms of Use"
  - Brazil, Colombia, Japan: HDX COD-AB, CC BY-IGO
  - USA: "USGS National Boundary Dataset"
  - French Polynesia: "Administrative boundaries not available"
- The changelog in the zip has dated corrections (5/2/2025 release, 1/4, 20/6 and 01/7/2025 updates). The editions are not separately versioned files.
- Google's [Earth Engine catalogue](https://developers.google.com/earth-engine/datasets/catalog/FAO_GAUL_2025_level1) lists a "GAUL 2025" series. I found no FAO page for a 2025 edition (**unverified**).

**Probe**
- Disputed areas are units of their own with x-codes: xAC Aksai Chin, xAB Abyei, xJK Jammu And Kashmir, xIT Ilemi Triangle, xJL and xxx ("Disputed Area"), xAP Arunachal Pradesh (map_code IND).
- India has four "Disputed (… & …)" units along state lines.
- Taiwan is "Taiwan Province of China" and has no ADM1 units. Western Sahara (ESH) has no ADM1 units.
- There is no Northern Cyprus unit.

**Inference**
- GAUL is a single UN-aligned view that sets disputed areas apart. It is a good cross-check against R045's reference registry, but it is not a multi-view source.
- CC BY 4.0 is the headline licence, but SALB's non-commercial terms seem to apply to the Cyprus and Mexico parts. The SALB terms themselves could not be read, so this is **unverified**.

### 3. UN Geospatial (UNmap) and UN SALB
**Facts**
- All `un.org/geospatial` pages returned HTTP 403 to the fetcher, and `salb.un.org` redirects there. See *Failed retrievals*.
- What is known comes only through others: geoBoundaries says SALB "cannot be used for commerical purposes" (above), and GAUL's L0 lines follow "UN-map 2018" (above).
- A search snippet of a UNEP GRID metadata record for UNmap said outside users are limited to the purpose granted and "intellectual property over the Data shall at all times vest with the United Nations". I could not open the record itself (404), so this is **unverified**.

**Inference:** not usable for redistributed geometry. It may serve as a reference for what the UN shows. GAUL is the practical, open proxy.

### 4. OCHA COD-AB (HDX)
**Facts**
- HDX lists 169 `cod-ab-*` datasets through its CKAN API. There is no COD for JPN, CYP, USA, PYF or FRA; GAUL cites a `cod-ab-jpn` that HDX no longer finds.
- "Global – Subnational Administrative Boundaries" (CC BY-IGO, modified 2026-11-02) covers "level 1-4 boundaries … for 114 countries / territories" in three variants: Edge-Matched ("aligned to fit international boundaries"), Original and Extended. Which international line they are matched to is not stated in that text (**unverified**).
- Country editions:
  - BRA: IBGE 2020, "reviewed … January 2025"
  - COL: MGN, "version 02", reviewed 20 Nov 2024
  - MEX: "version 02", reviewed 20 Dec 2024

**Probe:** the BRA, COL and MEX ADM1 files lack Rocas, Malpelo, Roca Partida and San Pedro Mártir.

**Inference:** this remains the right rank-1 source where it exists (as for South Ossetia and Socotra). It does not help any of the cases here.

### 5. Eurostat GISCO, Countries (CNTR)
**Facts**
- Editions 2024, 2020, 2016, 2013, 2010, 2006 and 2001. Public scales are 01M, 03M, 10M, 20M and 60M ([page](https://ec.europa.eu/eurostat/web/gisco/geodata/administrative-units/countries)).
- Metadata PDF ([link](https://gisco-services.ec.europa.eu/distribution/v2/countries/countries-2024-metadata.pdf); its content is the 2020 record): "Generalised dataset derived from EuroGeographics, Turkstat and UN-FAO GI data. The dataset may be used and distributed if: The source … is acknowledged, AND The data is not used for commercial purpose, AND The original geometry is generalised to the equivalent of a scale of 1:1.000.000 or smaller."

**Probe:** CNTR_RG_01M_2024 (59 MB) has Rocas, Malpelo, San Pedro Mártir, Chichijima and Fatu Hiva. It lacks Roca Partida, and Cyprus is one feature.

**Inference:** the non-commercial clause probably rules it out unless TYR is non-commercial. TYR's status was not checked.

### 6. World Bank Official Boundaries (WB GAD)
**Facts**
- [Catalogue](https://datacatalog.worldbank.org/search/dataset/0038272/World-Bank-Official-Boundaries): "License: Creative Commons Attribution 4.0"; version "3 (Latest)"; files "Last Updated: Oct 21, 2026"; each download "includes Admin 0, 1, 2, Non-Determined Legal Status Areas (NDLSA), and an ocean mask". It also publishes a maintenance log (`20260710_GAD_v2_Maintenance_Log.xlsx`).
- [GEE community catalogue](https://gee-community-catalog.org/projects/wb_gad/) (secondary): "ADM0_complete contains both ADM0 and NDLSA … polygons, while the standard ADM0 file excludes NDLSA polygons".
- [Space2Stats docs](https://worldbank.github.io/DECAT_Space2Stats/sub_tasks/admin_bounds.html): "digitized at a 1:250,000 scale" (high resolution).

**Probe:** none. The catalogue API answered HTTP 429 four times and the page shows no file URLs.

**Inference:** this is the most promising open (CC BY 4.0), multi-level alternative base layer that is not built from OSM. It should be downloaded and probed. How it treats disputed areas and whether it draws small islands are **unverified**.

### 7. Overture Maps, divisions theme
**Facts**
- [Guide](https://docs.overturemaps.org/guides/divisions/): "derived from a conflation of two community sources", namely OSM and geoBoundaries; "published under the ODbL license"; `division_area` has `is_land` and `is_territorial`; released monthly with GERS IDs.
- [Attribution page](https://docs.overturemaps.org/attribution/) also lists Esri Community Maps and LINZ, both CC BY 4.0.
- [Schema](https://docs.overturemaps.org/schema/reference/divisions/division/): `perspectives` with modes `accepted_by` and `disputed_by`. Without it, a division "is not known to be disputed from any political perspective".
- [Release calendar](https://docs.overturemaps.org/release-calendar/): latest release `2026-11-18.0`. Releases are kept for a "maximum of 60 days (two monthly releases)".

**Inference**
- Its points-of-view model is the closest to R045's. But it is ODbL, mostly OSM, and the project would have to archive each pinned release itself.
- It probably repeats OSM's line in Nicosia. Not probed, **unverified**.

### 8. Who's On First
**Facts**
- [Licences](https://whosonfirst.org/docs/licenses/): "linking back to the License is required". Data is "both an original work and a modification of existing open data", and sources are licensed per source.
- [Hierarchies](https://whosonfirst.org/docs/hierarchies/): "places we know to be disputed [have] a place type of disputed … parented … by two or more countries".

**Inference:** geometry comes from mixed sources and the editions are not formal. It is weak as a pinned provider. Its disputed-area records may be useful as a cross-check only.

### 9. National agencies for the concrete cases
**Japan, MLIT National Land Numerical Information N03 (行政区域データ)**
- [Page](https://nlftp.mlit.go.jp/ksj/gml/datalist/KsjTmplt-N03-2025.html): reference date "2025年1月1日時点". The source is "国土地理院「数値地図（国土基本情報）」". Licence label "オープンデータ（CC_BY_4.0）". National files exist for 2014–2025, and a 2026 edition is announced.
- [Terms](https://nlftp.mlit.go.jp/ksj/other/agreement_01.html): "商用利用も可能です" (commercial use is allowed). Adapted data must state 「…を加工して作成」 ("created by processing …").
- Probe: `N03-20250101_13.geojson` (Tokyo) has Chichijima inside 小笠原村 (Ogasawara village), with many island parts nearby.

**United States, Census TIGER/Line 2025 states (`tl_2025_us_state.zip`, [www2.census.gov](https://www2.census.gov/geo/tiger/TIGER2025/STATE/))**
- Metadata: "not copyrighted … free to use … acknowledgement must be given to the U.S. Census Bureau". The boundaries are "for statistical data collection and tabulation purposes only … not legal".
- Probe: all four Lake Erie points fall inside Ohio, Michigan or New York. AWATER: Ohio 10.27e9 m², Pennsylvania 3.40e9, New York 19.26e9, Michigan 103.86e9.
- Inference: TIGER/Line, not the clipped cartographic files, splits the lake among the states up to the international line. geoBoundaries' USA layer ends at the shore.

**Cyprus, Department of Lands and Surveys / INSPIRE**
- The DLS geocatalogue record returned 404 and the INSPIRE geoportal did not resolve.
- A search snippet says the INSPIRE Administrative Units download carries "no conditions apply" (**unverified**). Its districts are those of the Republic, so they would not give the Green Line (**inference**).
- UNFICYP publishes deployment maps as PDF and JPG only (UN Geospatial, per search; **unverified**). A shapefile "Cyprus UN Buffer Zone, 2005" (GfK MACON) is listed by Princeton as "Restricted" ([GeoDiscovery](https://geodiscovery.uwm.edu/catalog/princeton-r494vm705), not opened).

**Mexico, INEGI Marco Geoestadístico**
- A 2025 INEGI technical norm (per search) says the framework covers continental and island territory. INEGI also has a "Territorio Insular Mexicano 1:50 000" product.
- The page `inegi.org.mx/temas/mg/` rendered empty. Licence, edition and island coverage are **unverified**.

**Brazil (IBGE), Colombia (IGAC/DANE), French Polynesia:** not checked. These are candidates for Rocas, Malpelo and Fatu Hiva at rank 1 (**unverified**).

## What helps each concrete case (inference)

| Case | Best candidate found | Rank under D062 (proposal) |
|---|---|---|
| Nicosia Green Line | No national or UN dataset found that draws the line as open vectors. GAUL, CGAZ, GISCO and World Polygons all draw one Cyprus. OSM (work under way in the repo cache) remains the only vector source. | 3 |
| Ogasawara (Chichijima etc.) | MLIT N03 2025, Japan's own line, CC BY 4.0 compatible | 1 |
| Fatu Hiva, Rocas, Malpelo, San Pedro Mártir | US DoS World Polygons 11.4 coastline, already pinned in the repo (as for the 14 islets) | 2 |
| Roca Partida | Not in World Polygons or GISCO. GAUL 2024 (Colima part, ~0.03 km²; source SALB, licence doubtful) or gbOpen MEX ADM0 (CC BY 4.0). Otherwise OSM or Natural Earth. | 3 or 4 |
| Lake Erie split | US Census TIGER/Line 2025 states, US government work | 1 |

## Failed retrievals
- `un.org/geospatial/en/salb`, `un.org/geospatial/node/2699`, the SALB Terms of Use PDF (redirects to un.org): HTTP 403. A curl retry was refused by the session's permission policy and was not pursued.
- UNEP GRID GeoNetwork UNmap records: 404. `wesr-search.unep.org` UNmap record: 502.
- `data.apps.fao.org/catalog/dataset/global-administrative-unit-layers-gaul`: 404 (the ISO record worked).
- World Bank catalogue API (`datacatalogapi.worldbank.org`): 429, four tries.
- DLS Cyprus geocatalogue item: 404. `inspire-geoportal.ec.europa.eu`: DNS failure.
- `inegi.org.mx/temas/mg/`: rendered without content.
- GISCO "countries-2024-metadata.pdf" contains the 2020 record. No separate 2024 terms were found.

## Ranked shortlist (recommendation, not adopted)
1. **US DoS World Polygons 11.4** (already pinned). Use it now for Fatu Hiva, Rocas, Malpelo and San Pedro Mártir, at the same rank and in the same way as the existing 14 islets. Public domain; no new provider needed.
2. **US Census TIGER/Line (yearly edition, e.g. 2025)**. Use it for the Lake Erie split, and more generally for US states whose waters matter. Public domain; pin by year and sha256.
3. **Japan MLIT N03 (dated edition, e.g. 2025-01-01)**. Use it for the Ogasawara Islands at rank 1. CC BY 4.0 compatible, commercial use allowed, and processing must be stated. It also suggests checking each country's national agency (IBGE, IGAC, INEGI) as the rank-1 route for other missing islands.
4. **World Bank Official Boundaries v3 (Oct 2026)**. The strongest candidate for an open (CC BY 4.0), non-OSM second base layer at ADM0 to ADM2, with NDLSA as a separate category. Download and probe it before relying on it.
5. **FAO GAUL 2024 v2.0 and geoBoundaries gbOpen (commit-pinned)**. Use them as cross-checks of ADM1 units and of the UN's view of disputed areas, not as a base layer:
   - GAUL has no ADM0 file and has per-country third-party licence exceptions (SALB for CYP and MEX).
   - gbOpen mixes licences country by country, much of it ODbL from OSM.
