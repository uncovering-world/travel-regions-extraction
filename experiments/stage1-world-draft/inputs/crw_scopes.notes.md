# Census of sub-ISO territories with a territory-specific entry regime — notes

Read date for every row: 2026-10-03. Data: `census.csv` (116 rows, built by `build.py`; raw Wikipedia wikitext used for quotes is in `raw/`).

## How to read the evidence column

- `confirmed_primary` (9): an official or government page was fetched and states the rule. The fetch tool summarises pages, so the wording in the CSV is a close paraphrase, not a verified verbatim quote. Legal instruments themselves (decrees, acts) were **not** read for any row.
- `cited_secondary` (89): Wikipedia wikitext read directly (most rows), a news outlet, or another government's travel advice. For several of these Wikipedia's own footnote is weak (travel agency, blog); this is said in the row's notes.
- `unconfirmed` (16): forum/blog only, a search-result snippet only, or a prior-sample row that was not re-researched.
- `conflicted` (2): Lakshadweep, Azad Kashmir.
- The `since` column is the weakest: where no source stated a date, the value comes from background knowledge and is not verified (e.g. Rapa Nui 2018, Sabah/Sarawak 1963, Büsingen 1967, Baikonur 1995, Eritrea 2006, Mexico TVR 2012, Lakshadweep 1967). Treat `since` as a hint.
- The 23 prior-sample rows were carried over, not re-researched; their summaries restate the earlier sample plus whatever Wikipedia text was seen in passing.

## 1. Counts

By `regime_kind`:

| regime_kind | rows |
|---|---|
| permit_whole_territory | 35 |
| visa_exemption | 31 |
| own_visa_system | 15 |
| none | 11 |
| customs_or_tax_only | 8 |
| separate_immigration_control | 5 |
| visa_requirement | 4 |
| stay_limit | 4 |
| transit_only | 3 |

By `evidence`: cited_secondary 89, unconfirmed 16, confirmed_primary 9, conflicted 2.

By `unit_kind`: admin_unit 50, zone_or_band 21, site_list 15, island 14, de_facto_territory 12, class_of_parcels 4.

`whole_named_unit`: yes 78, no 38. `in_force_2026`: yes 81, unclear 32, no 3.

Note on `permit_whole_territory`: the label was used for every "permit to be present" regime, including ones whose scope is a band or a site list; `whole_named_unit` says whether the scope is actually a whole named unit. Only 18 of the 35 permit rows have `whole_named_unit = yes`.

## 2. Grouping against CR-W (inference, not adopted)

### A. Clear CR-W splits — a named unit as a whole, a standing rule, a class of visitors treated differently

Visa/stay rules scoped to a whole named unit:

- Prior sample: Jeju, Hainan, Phu Quoc, Rapa Nui, Galápagos, Sabah, Sarawak, (Labuan), Zanzibar, Batam/Bintan/Karimun.
- New: **San Andrés, Providencia and Santa Catalina** (CO; tourist card + 4-month cap, applies to Colombians too); **Mexico's five southern states** (TVR for GT/BZ/SV/HN — confirmed on gob.mx); **Kinmen, Matsu, Penghu** (TW; PRC nationals); **Ceuta, Melilla** (ES; Tetouan/Nador residents + exit checks); **Nakhchivan** (AZ; Iranians — status unclear); **Kish, Qeshm** (IR — status unclear); **Rason** (KP — status unclear); **Guilin, Xishuangbanna** (CN; ASEAN groups); **Shenzhen/Zhuhai/Xiamen** SEZ visas (CN; one city each); Korea's **Yangyang** and **Muan** group waivers (KR; whole provinces, renewed yearly, status unclear); **Chukotka for Alaska Natives** (RU; status unclear).
- One ISO code, several regimes: **SH** (Saint Helena / Ascension / Tristan da Cunha — three regimes, two confirmed on official sites); **SJ** (Svalbard visa-free / Jan Mayen permit).
- De facto territories with their own entry regime: Northern Cyprus, Abkhazia, South Ossetia, Transnistria, Somaliland, **Puntland** (new, 2025), Kosovo (under RS only by modelling choice), Crimea, **Socotra** (Socotra-only visa), Kurdistan Region (flagged: may have ended Sept 2025), Gaza (inside PS; emergency), eastern Libya (boundary not a named unit), AANES (ended 2026), Polisario zone (inside EH; unconfirmed), Wa State (unconfirmed).

### B. Rows that hinge on a "whole-territory permit" convention

A permit to be present, required of all foreigners (sometimes also citizens), covering a whole named unit. Whether this counts as a CR-W "presence decision" is a model choice.

- Prior sample: Arunachal Pradesh, Sikkim, Manipur, Mizoram, Nagaland (the last three toggle with yearly relaxations), Tibet, Mount Athos, Jan Mayen.
- New: **GBAO** (TJ), **Chukotka** (RU; confirmed on the okrug government site; Decree 470 reportedly excludes Bilibino district), **Lakshadweep** (IN; conflicted), **Chittagong Hill Tracts** (BD; three districts; status unclear), **Tristan da Cunha** (SH), **Clipperton** (FR; uninhabited), **Baikonur** (KZ; a city), **Mecca** (SA; class defined by religion), UM islands (whole ISO entry, so no split).
- Formerly whole-unit, now not: **Andaman & Nicobar** (30 islands opened 2018), **Azad Kashmir** and **Gilgit-Baltistan** (2019: reduced to border bands; AJK conflicted), Ladakh (parts only).

### C. Artefacts — rules whose scope is not a named unit

- Transit: China 240-hour areas, Saatse Boot, Saimaa Canal.
- Bands: US BCC zone, Russia border zone (incl. Kurils), Decree 470 partial areas, Kaliningrad restricted districts, India PAP belts (Himachal, Uttarakhand, Rajasthan, J&K), Ladakh PAP valleys, Nepal restricted areas (ward-level), Turkmenistan restricted zones, Eritrea outside Asmara, Lebanon south of the Litani, Papua interior (SKJ), Torres Strait Protected Zone, Brest–Grodno zone (district list; confirmed), Algeria "Great South" (wilaya list, itinerary-based; confirmed), Golden Triangle SEZ, former Mexican northern border zone (ended).
- Site lists: South Sinai resorts, Iran mainland free zones, Pearl River Delta city list, China cruise coastal provinces, Russia 72-hour ports, ZATO closed cities, Greek "express visa" islands (12 named islands, one island per visa), Azerbaijan liberated territories (confirmed), Bhutan border towns, Sinuiju.
- Parcel classes: Brazil indigenous lands (confirmed), Australian Aboriginal land (NT trusts, APY Lands), Vietnam coastal economic zones (legal class; only Phu Quoc designated as far as found).

Two artefact rows sit close to group A and may deserve an explicit ruling: the **Greek Aegean islands** (each visa is valid for one whole named island) and **South Sinai** (a standing rule for a large class of visitors, but scoped to a resort strip rather than the governorate).

### D. Customs/tax-only or no differential (negatives)

- Customs/tax only: Büsingen, Livigno, Heligoland, Åland (has its own ISO code AX, so out of scope anyway), Canary Islands, Leticia tourist fee, Fernando de Noronha (TPA; borderline — see leads), Aqaba ASEZA (fee waiver; unconfirmed).
- No differential found: Madeira, Azores, Sicily, Bonaire/Saba/Sint Eustatius (BQ — one common policy), Bougainville, Lord Howe Island (bed cap), Niihau (private land), Akrotiri & Dhekelia (follows Cyprus for short stays), Hengqin (nothing found), Gilgit-Baltistan (post-2019), Mexican northern border zone (abolished).

## 3. Excluded on purpose

- Territories with their own ISO 3166-1 code: Hong Kong, Macau, US territories, French overseas departments/collectivities, **French Southern Territories (TF)**, Norfolk Island, Åland (AX; kept only as a negative control), Faroe, Greenland, Crown Dependencies, Gibraltar.
- War-time control lines (Russian-occupied parts of Ukraine other than Crimea; Sudan; Myanmar conflict areas; Houthi-held Yemen): not standing non-emergency rules; not listed.

## 4. Leads not resolved

1. **Kurdistan Region (prior sample)** — Wikipedia says the federal e-visa portal has been "solely responsible" since September 2025, yet still describes a KRG e-visa. Needs a primary check; it may no longer be a split.
2. **Lakshadweep** — is there still a foreigner-specific Restricted Area Permit, or only the UT entry permit that applies to all non-islanders? Sources disagree.
3. **Azad Kashmir** — 2019 federal abolition of the NOC vs. current operator advice that an NOC is still needed.
4. **Ceuta/Melilla** — the legal texts (Schengen Borders Code Art. 41; 1991 accession declaration) could not be fetched; whether the Tetouan/Nador exemption is applied in practice since the 2022 border reopening is unverified.
5. **Aqaba ASEZA** — only forums and blogs; no official page found.
6. **Fernando de Noronha** — is there a legal maximum stay or only a progressive tax? State law not read.
7. **San Andrés** — decree text (2762/1991) could not be fetched; 4-month cap is from press.
8. **Socotra** — who issues the visa in law, and whether control changed in early 2026.
9. **Wa State, Polisario zone, Golden Triangle SEZ, Lebanon south of the Litani, Minicoy for Maldivians** — anecdotal evidence only.
10. **Iran free zones, Rason, Sinuiju, Nakhchivan (Iranians), Chukotka–Alaska, Russia 72-hour ports, Korea Yangyang/Muan** — rule documented, current operation unknown.
11. **Manipur/Mizoram/Nagaland** — whether the PAP regime is currently imposed or relaxed.
12. **Hengqin** — no visitor-entry regime found; Macau–Hengqin arrangements for mainland residents not investigated.
13. Not investigated at all: Chile–Peru Arica–Tacna convention, EU/other local border traffic zones as a class, Japan–Russia Kuril visa-free exchanges (believed ended 2022), Guna Yala (Panama), Afghanistan provincial permits, Sri Lanka Northern Province clearance (believed ended), Boten SEZ (Laos), Thai/Malaysian/Myanmar border-pass zones, Sabah's ESSZONE.

## 5. Failed retrievals

- `eur-lex.europa.eu` (Schengen Borders Code) — empty body.
- `europarl.europa.eu` question E-9-2022-000911 — empty body.
- `leh.nic.in/requiring-protected-area-permit/` — 404.
- `mfa.gr` visa page — 403. `nt.gov.au` land permits — 403.
- `suin-juriscol.gov.co` (Decreto 2171/2001) — TLS error.
- `dfat.gov.au` Torres Strait Treaty — timeout.
- `immigration.gov.tw` carrier guide PDF — image-only, unreadable.
- `en.wikipedia.org` pages "Visa policy of Crimea", "Visa policy of Western Sahara", "Travel permits in Tibet" — do not exist.
