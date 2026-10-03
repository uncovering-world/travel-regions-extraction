# Binding Stage 1 regions to GADM units

**Experiment, not the canon.** Open question [Q013](../../docs/open-questions.md) (binding to substrate units); issue [#22](https://github.com/uncovering-world/travel-regions-extraction/issues/22).

## Question

Track Your Regions draws regions from GADM 4.1 (`gadm_410.gpkg`, see its `db/` scripts). For each of the 317 regions of the [Stage 1 list](../stage1-list/README.md):

1. Can it be written as a set of whole GADM units, and at which level?
2. Which regions cut through GADM units, or have no GADM unit at all, so that they need a custom geometry (D042, D056)?
3. Does a region's GADM country (`GID_0`) agree with the country the canon attributes it to, and where does GADM's own `GOVERNEDBY` / `SOVEREIGN` / `DISPUTEDBY` record differ?

Only attributes are read, no geometry: a match of names or codes is a candidate binding, not proof that outlines agree. GADM's data stay local (its licence forbids redistribution); only unit identifiers are written to this repository.

## Related

R028, R030, R045, R047; D042, D056; Q013; [outline-source survey](../outline-sources/README.md).

## What would change our mind

Written before the first run.

1. **GADM is a sufficient substrate for Stage 1** if all but a handful of regions bind to whole GADM units by code or exact name, and the rest are small places.
2. **Name matching is not enough** if more than about a tenth of the non-ISO regions match only by an ambiguous or approximate name; then bindings are a reviewed input, like the register's ties.
3. **GADM's country attribution conflicts with the canon** wherever a region's `GID_0` is not its canon country; if this happens for more than the known disputed areas, the canon cannot inherit GADM's country tree and must carry its own.

## Method

```bash
python3 experiments/gadm-binding/run.py   # reads ../track-your-regions/deployment/gadm_410.gpkg, or $GADM_GPKG
```

- **Data.** GADM 4.1 (`gadm_410.gpkg`, 2,759,749,632 bytes, sha256 in `outputs/summary.json`), the consumer's local copy; only attribute columns are read, nothing is copied.
- **Binding.** ISO entries by ISO alpha-3 = `GID_0`. GADM's own pseudo-countries (`ZNC`, `XKO`, `Z01`…) by GADM's `NAME_0` (`inputs/gadm_codes.csv`). Other regions by an exact match of the folded place name against GADM names at levels 1–3, within the country where the region's census row gives one. Then a review of every non-ISO binding: `inputs/reviewed.csv` holds 23 decisions made by reading GADM's names (e.g. Hong Kong and Macau are first-level units of China in GADM; three exact-name matches were wrong: San Andrés matched municipalities of that name elsewhere, Azad Kashmir's pseudo-country also holds Gilgit-Baltistan, Kinmen without Matsu).
- **Not done.** Outlines are not compared: a binding says the region is made of these GADM units by name, not that their outline is the region's stated line.

## Result

317 regions.

| Kind of region | Regions | Bound to whole GADM units | Need a custom geometry |
|---|---|---|---|
| ISO 3166-1 entries | 249 | 249 (247 by code; Hong Kong and Macau are GADM units of China) | 0 |
| Entry rules (incl. areas held by another party) | 32 | 31 | 1: Socotra |
| Registry cells | 11 | 6 | 5: South Ossetia, Western Sahara west of the berm, East Jerusalem, Shebaa Farms, Somaliland (Natural Earth has its outline) |
| Residents test | 21 | 11 | 10: the 1949 no-man's-lands, the Cyprus buffer zone, Ilemi, Koalou, the Korean DMZ, the southern Kurils, Rukwanzi–Semliki, the Dniester Security Zone, the UNDOF area, Varosha |
| Leases held by the lessee | 2 | 0 | 2: Baikonur, Guantanamo Bay |
| Unclaimed land | 2 | 0 | 2: Bir Tawil, Gornja Siga |
| **Total** | **317** | **297** | **20** |

Regions bound to whole GADM units but not as the country GADM attributes them to: Crimea and Sevastopol (GADM: Ukraine), Abkhazia (Georgia), Transnistria (Moldova), Golan (Israel), Abyei (Sudan), Kinmen and Matsu (Taiwan, `TWN.1_1`). Their GADM units sit inside another GADM country, so an ISO region's binding is "its `GID_0` minus the units bound to separated regions".

GADM pseudo-countries no region claims: Kaurik, Lapthal, Sang (India–China middle sector, special places in the canon; their land goes to the holder), Shaksgam Valley, Pa-li-chia-ssu, and the Caspian Sea. Each has to be assigned to a region explicitly.

## Conclusion

1. *Largely met.* 297 of 317 regions (94%) bind to whole GADM units. The 20 that do not are small or contested places — exactly where custom geometries were expected (D042, D056): zones, leases, unclaimed pockets, South Ossetia, East Jerusalem, Western Sahara west of the berm, the southern Kurils, Socotra.
2. *Met.* Name matching alone is not enough: of 30 non-ISO regions an automatic match bound, three were wrong. Bindings are a reviewed input.
3. *Met, as expected.* GADM's country tree differs from the canon's for the contested areas it carries as units. The canon must carry its own attribution and express ISO regions as GADM countries minus the separated units, plus explicit assignments for GADM's leftover pseudo-countries.

## Revision, 2026-10-04: where GADM puts the disputed places

The owner recalled that GADM mishandles a glacier on the China–India–Pakistan border; the first run could not see it, because it read names only and Siachen is not a region of the canon but a special place whose land goes with its holder (R046, R058). `check_points.py` now tests, for each of the 99 features of Natural Earth's disputed-areas layer, which GADM unit contains the feature's label point (`LABEL_X`, `LABEL_Y`), with a pure-Python point-in-polygon test over the GeoPackage (`gadm_points.py`). Output: `outputs/disputed_points.csv`. One point per place: this shows where GADM puts the place, not whether its line follows the stated one.

```bash
python3 experiments/gadm-binding/check_points.py
```

**GADM puts the place with another country than the one that holds it** (by Natural Earth's note and the register):

| Place | Held by | GADM puts it in |
|---|---|---|
| Siachen Glacier | India (register) | `Z06.6_1` Gilgit-Baltistan, Pakistan-administered |
| Demchok | India (Natural Earth: "Admin. by India") | `Z08` (Xizang), a GADM unit of China |
| Bhutan's north-western valleys | Bhutan (Natural Earth) | `CHN.29_1` Xizang, China |
| Near Om Parvat (Kalapani) | India (Natural Earth) | `NPL.3_1`, Nepal |
| Halayib Triangle | Egypt (Natural Earth) | `SDN.11_1` Red Sea, Sudan |
| Bir Tawil | nobody (unclaimed) | `EGY.2_1` Al Bahr al Ahmar, Egypt |

**GADM has no polygon at the place at all** (21 features): Bajo Nuevo, Sapodilla Cayes, Hans Island, Doumeira Island, Peñón de Alhucemas, Bassas da India, Europa, Glorioso, Juan de Nova, Matthew and Hunter, Mbanié, the British Indian Ocean Territory's label point, Rockall, the Dragonja mouth, the Senkaku/Pinnacle Islands, Dokdo, the Spratly Islands' label point, Wake, Bird Island, Scarborough Reef, Serranilla. A visit recorded on one of them falls into no GADM unit, so no region can count it unless the canon adds a geometry.

**Other observations.** Shaksgam (`Z02`) and the Indian-held middle-sector pockets (`Z05`, `Z09`) are GADM pseudo-countries that must be assigned to their holders' regions. Natural Earth's label point for the Kuril Islands lies in Kostroma Oblast, a data error in that layer (like the Barbados attribution found earlier); its feature must not be located by its label point.

**What this changes.** Binding by names is not enough even where every name matches: GADM's land assignment has to be checked against the canon's holder for every special place and marker, and land GADM does not cover has to be added. Both need geometry, not only attributes.

## Status

Concluded 2026-10-04 (revised the same day).
