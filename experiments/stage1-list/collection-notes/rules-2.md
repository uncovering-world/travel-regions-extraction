# rules-out-2 — notes

All sources were fetched on 2026-10-03. Saved texts are in `r2pages/`, the URL-to-file map is `r2manifest.tsv`,
rows are built by `build2.py` and checked by `selfcheck_rules2.py` (127 rows, 0 failing: every quote is a
whitespace-normalised verbatim substring of the saved text of its source).

Conventions: `in_force` is `yes`/`no`; the date of the passage it rests on is given below per row. Wikipedia is cited
at a pinned `oldid` and is always `secondary`. `primary` is used only for the authority's own page or the official text
(BOE, MHA, Bureau of Immigration, law.moj.gov.tw, CGREG / gob.ec, imi.gov.my, Ascension Island Government and its e-visa
portal, tristandc.com, foreigner.rangamati.gov.bd, state.gov as a party to the Bering Strait agreement).

The web-search budget of the session ran out before primary texts could be searched for Tibet, Mount Athos, Phu Quoc,
Kish and Baikonur; those rows rest on secondary sources. Sources that refused the fetch: EUR-Lex (HTTP 202 challenge),
hellenicparliament.gr and mfa.gr (403), commonlii and refworld (403), travel.state.gov (403), the Bandarban DC circular
PDF (connection reset).

## Per row

**bd-chittagong-hill-tracts** — 6 of 7. Not a unit: the name covers three districts (second level) of Chittagong
Division, and the permission is given per district (the primary page is Rangamati's only; Bandarban and Khagrachhari
pages were not reached). `start_date` not established: The Daily Star (2015) only says the general requirement of
district-administration permission existed "just like before" a January 2015 circular. `in_force` rests on the
Rangamati online-permission site, which is undated. Lead says "via local operator": not confirmed — the Rangamati site
takes applications from the visitor. Under the owner's rule this looks out of scope (not a unit, not detached).

**cn-tibet** — 5 of 7, all secondary (Wikipedia). `detached` has no passage (irrelevant for a top-level unit).
`start_date` not established. Scope warning: the permit is obtainable only through a guided tour by a Tibet-based
agency, so it is not open to an independent visitor. The `in_force` sentence carries a "better source needed" tag on
Wikipedia.

**ec-galapagos** — 6 of 7, rule fields primary (CGREG FAQ quoting LOREG art. 44; gob.ec procedure page quoting art. 29
of the migration and residence regulation). `start_date` not established: no fetched text dates the TCT; an ABG
resolution on FAOLEX cites the LOREG as "Registro Oficial Suplemento 520 de 11 de junio de 2014", which is not the
start of the card and was not used. Lead confirmed (60 days per year, applies to Ecuadorians too).

**es-melilla** — 7 of 7, rule fields primary (BOE-A-1994-7586, declaration on Ceuta and Melilla in the Final Act).
`own_rule` = `list`: the declaration covers Ceuta and Melilla together. Lead's "1991" is the signature date; the BOE
gives entry into force 1 March 1994. `in_force` rests on the Wikipedia Melilla article (present tense); whether the
Nador exemption is still applied in practice was not checked against a current official source. Applies to Moroccan
residents of Nador, not to visitors in general.

**gr-mount-athos** — 6 of 7, all secondary (Wikipedia; the Constitution and the Pilgrims' Bureau page could not be
fetched). `unit_level` = `top_level` on the passage "autonomous region in Greece"; the page on Greek administrative
divisions says it is "self-governing, excluded from the Kallikratis Plan", i.e. outside the regions scheme rather than
one of the regions. Not detached (rest of the peninsula is an ordinary municipality). `start_date` not established.

**in-manipur, in-mizoram** — 7 of 7. `own_rule` = `list` (Bureau of Immigration list of ten areas). The MHA annex
(2018 and 2020 versions fetched) states the whole of both States was excluded from the Protected Area regime from
1 January 2011, extended "till 31.12.2022"; the re-imposition is attested only by The Diplomat (January 2025,
secondary), on which `in_force` rests. The MHA text of the December 2024 order was not found. The MHA annex says
notified areas may be visited "either in groups, or as a couple ..., or by individuals", so individuals are not
excluded in principle; Wikipedia's "groups of at least 2" and "registered travel agent" is a general summary.
Lead's "ILP for Indians since 2019" (Manipur) was not checked.

**in-sikkim** — 7 of 7, mostly primary. `own_rule` = `list`. Lead confirmed (partly Protected, partly Restricted).
The 1958/1963 orders are quoted from the MHA annex, not from the orders themselves.

**ir-kish** — 6 of 7, all secondary. `unit_level` = `lower`: the island lies in Bandar Lengeh County (Kish District)
of Hormozgan Province. `own_rule` = `list`: Wikipedia names Kish together with Qeshm and "other free trade zones"
(Arvand, Aras ...). Contradiction: the UK FCDO page (read now) says British travellers must arrange the visit through
an Iranian agency and have "confirmation that a visa will be issued on arrival" — not "without any visa"; Wikipedia's
visa-free sentence is dated "in 2022". `in_force` = `yes` is therefore weak: it shows a Kish-specific regime exists
now, not that the 14-day exemption for all is current. No Iranian official source was fetched. `start_date` not
established.

**kp-rason** — 6 of 7, all secondary (tour operators, NK News lead, Wikipedia). `unit_level` = `top_level` for the
special city; the rule is about the Rason SEZ. `in_force` = `no`: tourism to the zone suspended 5 March 2025 (Uri
Tours FAQ "as of 2026"; CultureRoad 2026 agrees); the permit rule itself is not reported abolished. Lead's "1990s" not
established. Scope warning: access ran only as agency tours. Lead article (NK News) is paywalled after two paragraphs.

**mm-wa-state** — 4 of 7; weakest row. The only passage on entry ("A special permit is required to enter Wa State
from Myanmar") comes from a Wayback copy of a wiki mirror (hailam.miraheze.org); the current Wikipedia article has no
entry-rule text. Lead's "Wa travel pass at its own border gates; Myanmar visas not checked" and "1989" are not
established. `unit_level` = `lower`: only the northern part is recognised, as the Wa Self-Administered Division of
Shan State; the de facto territory is not a unit. `applies_to`, `start_date`, `in_force` have no passage.

**my-labuan** — 2 of 7 (status only). No fetched text gives Labuan an entry rule of its own: Part VII of the
Immigration Act defines "East Malaysian State" as Sabah or Sarawak and the Act text does not mention Labuan; the
Wikipedia Labuan article has no immigration-regime statement. Lead not established; a search snippet (not a fetched
passage) claimed Labuan is treated as part of West Malaysia for immigration — unverified.

**my-sarawak** — 7 of 7. The Act text (sections 62, 64, 66 and the commencement table) is quoted from a law-firm copy
(lowpartners.com), hence `secondary`; the official copies (commonlii, refworld) refused the fetch. `applies_to` is
primary (imi.gov.my on section 66). `own_rule` = `list`: Part VII applies to Sabah and Sarawak, each "as separate
unit" (s. 64). `detached` = `no`: Sarawak is on Borneo next to Sabah, though separated by sea from Peninsular
Malaysia. Lead confirmed.

**ru-chukotka-alaska-natives** — 7 of 7, rule fields primary (state.gov, undated page read now). Contradictions with
the lead: the agreement entered into force 10 July 1991 (the lead's "renewed 2015" is the reinstatement on the Alaska
side, mid-July 2015, per RFE/RL and Alaska Public Media; Wikipedia says "came into force on 17 July 2015"); and the
exemption covers designated rayons of Chukotka (Iultinsky, Providensky, Chukotsky, eastern Anadyrsky incl. Anadyr),
not the whole okrug. `in_force` rests on the present-tense State Department page; whether travel actually operates
since 2022 was not established. Out of scope by the owner's rule: applies only to qualifying residents with relatives.

**sh-ascension** — 6 of 7, rule fields primary (AIG immigration page, AIG e-visa FAQ). Lead confirmed, including the
list of nationalities not issued e-visas. `start_date` (lead "e-visa 2018") not established. `unit_level` =
`top_level` as an equal constituent part of the territory (Wikipedia, citing the 2009 Constitution Order).

**sh-tristan-da-cunha** — 6 of 7, rule fields primary (tristandc.com, page reviewed 2024-12-03). Lead confirmed.
`start_date` not established.

**sy-aanes** — 6 of 7, all secondary. `in_force` = `no`: the administration was integrated into the Syrian state on
20 August 2026 (Wikipedia); Rudaw (18 April 2026) reports Semalka transferred to Damascus and "Non-Syrians ... still
required to obtain a visa at the crossing". The former permit is described only by a tour operator's blog (May 2025).
Not a unit. Lead consistent; "c. 2013" not established.

**tw-kinmen, tw-penghu** — 7 of 7, rule fields primary (Regulations Governing the Trial Operation of Transportation
Links Between Kinmen/Matsu/Penghu and the Mainland Area, as amended 2018-07-17). `own_rule` = `list` (Kinmen, Matsu,
Penghu). `unit_level` = `top_level` on "county": Wikipedia calls Kinmen a "County of Fuchien Province", while the page
on Taiwan's administrative divisions says provinces are non-functional and the 22 counties and cities are the
subnational divisions. The 15-day figure is in Article 14 ("Travel: up to fifteen days per stay"). `start_date` is
secondary (Wikipedia Penghu). `in_force` is the rule on the ROC side; Wikipedia adds that PRC-side endorsements were
suspended from 2020 and as of October 2024 are issued only to Fujian/Shanghai residents for Kinmen and Matsu — Penghu
may be inoperative in practice. Applies to PRC nationals only.

**vn-phu-quoc** — 6 of 7, all secondary. The page at vietnamconsulateinhouston.org presents itself as a consulate
site but its official status could not be confirmed, so it is marked `secondary`. No legal text fetched (the copy of
Law 47/2014 found has no clause for coastal economic zones; a search snippet named Art. 12(3a) added by Law
51/2019 and Resolution 80/NQ-CP of 2020, effective 1 July 2020 — unverified). `unit_level` = `lower`: a special zone
of An Giang province since 2025 (the consulate page, 2023, still says Kien Giang). `start_date` not established.

**kz-baikonur** — 6 of 7, all secondary. `unit_level` = `top_level` rests only on a navigation-box line ("Special
status cities Almaty Astana Baikonur Shymkent") — weak. Two regimes appear: a Roscosmos permit (Wikipedia) and Kazakh
prior permission for a list of closed areas including Baikonur (UK FCDO, read now); `own_rule` = `own` follows the
first, the FCDO passage would make it `list`. Kursiv (9 June 2026) reports permit processing cut to 10 days. Scope
warning: Wikivoyage says the cosmodrome can be visited only on a guided tour. Lead's "1995 (lease)" not established.
Not detached within Kazakhstan.

## Rows that look out of scope under the owner's rule

- Not a whole top-level unit and not detached: bd-chittagong-hill-tracts, mm-wa-state, sy-aanes (also no longer in force).
- Smaller detached place named in a list, not its own rule: ir-kish.
- Rule not open to an independent visitor: cn-tibet (guided tour only), kp-rason (agency tours; suspended),
  kz-baikonur (tour operator in practice).
- Rule only for a narrow class of persons: es-melilla (Nador residents), ru-chukotka-alaska-natives (Alaska Native
  residents with relatives), tw-kinmen and tw-penghu (PRC nationals).
- No rule established: my-labuan.
