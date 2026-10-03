# Canonical Travel Regions — open questions of the model

Version: 0.4.0-draft. Date: 2026-10-03. Changes in 0.4.0-draft: Q006 closed; Q001–Q005 and Q007–Q012 annotated or narrowed by the owner's decisions of 2026-10-03 (D038–D053); Q013–Q019 added; Q017 closed and Q016 narrowed by D054–D055.

The order reflects the potential scale of change to the world map: from a change in the definition of almost all regions to changes in individual classes and in history. These are model questions. "Which document is required now?" and "Where does the line run on date t?" are data tasks, not separate items of this list.

## Q001 — Narrowed: CR-W accepted; CR-J normative adoption remains open

**Status: narrowed; resolved for regime-based mandatory separation.** Rules R007–R012, R038/R039/R044; decisions D032–D037. The current production Stage 1 core is `S1-core-v1`, CR-W only, with all five gates. One admissible witness is sufficient regardless of frequency; the absence of a certificate is not equality.

The open remainder of Q001: whether to accept CR-J as an independent institutional responsibility dimension when current hard D may be equal. CR-J is a well-defined normative candidate, not adopted; J1–J6 are fully preserved in [review §4.2](../experiments/q001/stage1-rule-review.md#42-operational-definition-independent_final_admission_jurisdiction) and the [candidate YAML](../experiments/q001/stage1-rule-candidates.yaml). A separate normative decision is needed, not additional geographic facts for the sake of a preferred outcome.

Undefined territorial/legal identity is rejected from the production and production-candidate core. `Q001.identity` is kept as a historical P3 model blocker, not as a mandatory production dimension. P3 is non-production/model-unresolved and is not the Stage 2 destination model. Possible preservation of exact legal status without CR-W remains Q006; a curated registry is not permitted by this decision.

P1/P2/P3 remain historical profiles whose results are not reinterpreted as `S1-core-v1`. D004–D007 are kept as accepted product regressions; if CR-W does not guarantee them, the conflict/requirement remains explicit, without automatic transfer to Stage 2. Residual Q002/Q004/Q005/Q006/Q007/Q008/Q009/Q011 remain open; the architectural Q012 is not resolved here either.

Note, 2026-10-03: the reference registry (D038, R045) separates states, dependencies with their own ISO 3166-1 entry and perspective-dependent areas without a legal proof per pair, which removes most of the cases CR-J was meant for. The CR-J remainder stays open.

**Next distinguishing experiment:** synthetic NX-01/NX-02/NX-04 from the review — independent capacities versus offices/shared apex under fully identical D, with a check that these premises are compatible with exact S/H. **Closure criterion for the remainder:** explicitly accept or reject the additional institutional invariant CR-J with J1–J6 and generic counterexamples. This does not declare the full Stage 1 semantics complete. [Adoption record](../experiments/q001/stage1-core-adoption.md).

## Q002 — For which set of travellers and which decisions is homogeneity needed?

**Impact: almost all visa/permit/document boundaries.** R007, R011–R014, R038.

"An ordinary traveller" does not define a set: a citizen, a resident, a refugee, a holder of an emergency document, a researcher, a yachtsman and a tourist may have different rights. Is a split required for one rare class? Should long stays, work, medical and diplomatic trips be included? Dependence on the route may also be non-territorial.

The part resolved by D032/R044: in the accepted civilian-short-stay-v1, one valid class-based witness is sufficient without a frequency threshold, including rare documents; S must not be changed for the sake of an individual case. The remainder is the exact applicability and the extension of the context/hard-output domain, not a repeated choice of a frequency threshold.

Options: universality for all persons/purposes; a fixed civilian short-stay scope; typical profiles with explicitly acknowledged incompleteness. The specification provisionally chooses the second option and allows rare documents. The domain C must not be changed for the sake of a convenient result in an individual case. Completeness applies only to the explicitly chosen profile and scope: it does not mean knowledge of all conceivable traveller contexts outside them.

Narrowed, 2026-10-03 (D050, R056): a class whose trip is defined by onward travel to a third territory (transit), a class defined by travelling in an organised group, and a class of residents of a neighbouring border area are not witness classes; a rule that admits visitors only through a tour operator is a witness. The rest of this question stands.

**Experiment:** run one and the same geographic set for an ordinary passport, several citizenships, a refugee document, a residence permit, arrival by yacht and a long stay. **Closure criterion:** the formal scope C and the list of hard outputs are published; it is known which differences intentionally remain overlays.

## Q003 — What does it mean to cover the whole travel space?

**Impact: a huge part of the Earth's surface and all boundary features.** R002–R004, R025, R026; D001, D016, D017.

A destination-only universe requires a definition of destination and changes with accessibility. Land-only excludes travel by sea and over shelf ice. The full surface requires a partition of the ocean, the high seas, ice and ambiguous coastal features. Air and underground travel would require a different dimensionality, not new land polygons.

The relation of the territorial sea to land needs to be defined: does it belong to the same region, to a separate maritime region, or is it outside the universe? An EEZ must not automatically be treated as the same kind of territory. Antarctica land and the Treaty Area are also distinct. LAND_V0 is an explicit temporary limitation of the experiment.

Note, 2026-10-03 (D040): the Antarctic land in U is one Stage 1 cell, with claims as overlays (R026); which physical types of Antarctica belong to U is still this question.

**Experiment:** inland lake, South Pole, ice shelf, ocean cruise point, low-tide reef, reclaimed island, closed island. **Closure criterion:** for each physical type, inclusion and the principle of classification are defined, independently of sovereignty and accessibility.

## Q004 — Do customs and biosecurity really divide canonical geography?

**Impact: from a few special territories to a large number of internal zones.** R013, R016, R017; D011.

A choice is needed between a mandatory split by traveler-facing formalities, all such formalities as overlays, or a limited class of external customs jurisdictions. The problem is not whether there is a declaration on a particular island: even knowing all the rules, the boundary of the class has to be explained.

Narrowed, 2026-10-03 (D050, R056): answered for entry payments — a mandatory fee or purchase on arrival does not separate, and only rules on who may enter and for how long do (visa, permit, separate control, stay limit); fees are markers. Customs and biosecurity formalities as such remain open. The owner's wording ("only rules on who may enter and for how long") points to their not separating either; that reading is to be confirmed, not assumed.

**Experiment:** Åland, Canary Islands, Ceuta/Melilla, Heligoland, Büsingen, Livigno, Tasmania, Hawaii, California. First compare the formalities without names and political statuses. **Closure criterion:** one test applies to external and internal zones; if an identity correction is needed, the dependence on Q001 is explicit.

## Q005 — Where does a region end and an access overlay begin?

**Impact: thousands of permit areas, parks, bases and protected islands.** R009, R014, R017, R025–R027.

If every mandatory permit is sufficient, a multitude of objects will become regions of their own. If all permits are overlays, many restricted destinations are lost. The word destination by itself does not solve the problem. Area or number of visitors create an arbitrary scale unless approved as a product parameter.

R014 already excludes local border, military, nature-conservation, site-specific, route-specific and activity-specific restrictions from the sufficient grounds for a split. This remains true even if the overlay coincides with a whole district or federal subject: administrative scale is not a criterion. The open part of Q005 is now narrower: which general predicate distinguishes such an overlay from a permission for ordinary civilian admission into the candidate territory as a destination as a whole.

Narrowed, 2026-10-03 (D050, R014, R056): the owner adopted the convention this question asks for. A standing rule that makes presence in a whole unit conditional on a permit for an ordinary visitor separates that unit, if the unit is a whole top-level unit of its country or a smaller detached unit with a rule written for it; a permit for part of a unit, a border band, a list of places, a closed town or a single valley stays a marker. Open: the operational definition of the units and a rule covering several top-level units (Q015).

**Experiment:** Mount Athos, Tibet, Galápagos, Lord Howe Island, North Sentinel Island, Montserrat exclusion zone, Antarctic protected area, an ordinary national park and airport airside. **Closure criterion:** a scope-level predicate or an honestly approved convention of size/institution, not a list of exceptions by name.

## Q006 — Should a legal dispute preserve a separate identity without travel discontinuity?

**Status: closed, 2026-10-03 (D038, D043–D048).** A dispute is kept separate when a declared perspective of the reference registry places the area in another country (R045), subject to the treatment by kind: border-line disputes are special places (R050); islets and paper claims are regions where civilians live (R051); zones with no single holder are regions where civilians live and the parties state an outline (R052); leases follow the lessor (R053). A claim no declared perspective shows gives a marker. This explains D006 and D007 by a general norm, the closure criterion below; whether the release build confirms the derivation is check V011, not this question. The text below is kept for history.

**Impact: all disputed/occupied areas and the residual regions of controlling states.** R010, R016, R022, R024; D006, D007, D013, D014.

Different de facto authority inside a disputed area justifies an internal split. It does not prove separation from the ordinary territory of the same controller. Claims are declared overlays, but D007 requires that Western Sahara not be dissolved into Morocco. One must not quietly add "disputed=true" to the hard signature and keep asserting that a dispute divides nothing.

Options: only proven access/legal-route consequences; an independent international-status identity criterion; a separate product class of disputed territories with explicit inclusion rules. In the third option it has to be explained what distinguishes a significant dispute from any border claim.

**Experiment:** the western part of Western Sahara vs Morocco; Crimea vs ordinary Russia; Golan vs Israel; Aksai Chin vs China; an unenforced claim to ordinary territory. **Closure criterion:** D006/D007 are explained by a general norm, or it is recorded which accepted constraint is incompatible with the chosen model.

## Q007 — How to represent joint, gradual and shifting control?

**Impact: conflict zones and the precision of the overall partition.** R015, R024, R028–R030.

Who controls entry, who patrols at night, who administers civilian affairs and who applies the law are not always one actor. Even with perfect observations, a binary controller may not exist. A choice is needed: a vector of functions, a primary control role, or special zones of joint regime.

A separate question: is a complete point-wise assignment mandatory as a computational convention, or must it also mean confident knowledge? The specification allows a provisional assignment with uncertainty, but not an invented factual contour.

Narrowed, 2026-10-03 (D043, R048, R049): the holder of an area is the party whose officers can in practice admit, refuse and remove a civilian; rules that cannot be enforced there do not count; parts held by different parties have their own holders. A forcible change of control follows the settling rule, and while fighting moves the line no area is delimited and the regions touched carry a flag. Open: what applies when the holder test cannot tell the parties apart (Q016), and joint regimes beyond the zones of R052.

**Experiment:** West Bank Areas A/B/C, Gaza, Cyprus buffer zone, UNDOF area, Siachen, Ukraine frontline. **Closure criterion:** a model of control functions and the behaviour for an uncertain strip are defined; an observation update does not pass it off as a change of sovereignty.

## Q008 — What stability is needed for a new boundary to change the partition?

**Impact: the map over time, especially sanitary restrictions and conflicts.** R012, R015, R017, R031.

A "temporary measure" may last for years, while a new permanent jurisdiction has so far existed for one day. A threshold of 30/90/365 days would be a model decision, not a fact. It has to be decided whether we assess the intended duration, the institutional nature, the actual duration, or a combination with hysteresis.

R044 adopts a narrow sufficient standing/constitutive gate for CR-W without an age threshold; incident/emergency measures are not promoted by duration. The remainder of Q008 is ambiguous institutional classification and fuller temporal semantics; the question is not closed.

Narrowed, 2026-10-03 (D043, D049): stability is handled at release level. A boundary from an uncontested entry rule enters after two consecutive yearly releases and leaves three years after the rule ends (R055); a forcible change of control is accepted after three quiet calendar years or an explicit act (R049). G-TIME is unchanged. Open: the classification of emergency and incident measures under G-TIME, and the counting details of Q019.

**Experiment:** one scope with restrictions for 1 day, 3 months and an indefinite period; a change of control with identical travel consequences; a new admission jurisdiction with a published start date. **Closure criterion:** the stability predicate does not require knowledge of the future and defines split/merge events without exceptions by country.

## Q009 — How much spatial dependence is admissible inside one region?

**Impact: the number of cells after intersecting all scopes.** R006–R009, R014, R017, R027.

If TravelDecision may refer to coordinates arbitrarily through overlays, the whole Earth can be left as one region. If coordinates are forbidden altogether, one airport with several procedures destroys homogeneity. Hard dimensions, invariant inside a region, and soft dimensions, for which internal geography is allowed, need to be defined.

Narrowed, 2026-10-03 (D050, R056): transit limits, group-only and local-border-traffic schemes, fees, permits for part of a unit and entry rules whose scope fails the scope test are markers inside a region, not boundaries.

**Experiment:** a common admission regime plus different entry points, transit procedures, local permits and a customs zone crossing a control boundary. **Closure criterion:** an identical signature guarantees exactly the enumerated homogeneity; overlays are not used to bypass mandatory splits.

## Q010 — When does region_id change and how are visits recomputed?

**Impact: historical sets and user accounting, not necessarily the number of today's regions.** R031–R033.

After a small change of a boundary, both identities can be kept. After a part is carved out, a successor is usually needed. But the quantitative boundary between these events is not defined. The percentage of area should not be used as a hidden criterion.

Provisional hypothesis: split/merge create new IDs; a rename and a digitization correction keep the ID. It is not decided how to treat "the same territory" after a change of status, nor how to map a visit in the past onto the modern set.

Note, 2026-10-03 (D049, R055): the set of regions changes only at a yearly release. Correspondence tables and a de-minimis rule are Q019.

**Experiment:** rename; coastline correction; transfer of an enclave; division of an admission jurisdiction; merging of two regions; late correction of an old line. **Closure criterion:** an event taxonomy and rules for historical/current visit views are published without loss of the original evidence.

## Q011 — Are explicit product conventions admissible?

**Impact: honesty and manageability of exceptions, especially Antarctic/identity cases.** R008, R010, R026, R035; D004, D016.

A fully derived map may contradict the intuitive requirements of the project. A managed list of conventions is technically admissible, but it changes the meaning of falsifiability: what is then checked is conformance to the rules and the published conventions, not only to independent facts.

Narrowed, 2026-10-03: the owner adopted explicit conventions with IDs and rationale — the reference registry as a declared product rule (D038), one Antarctic Stage 1 cell (D040), and whole-unit presence permits (D050). Further conventions still need their own decision; none may be added silently.

**Experiment:** try to satisfy literal UKOT-separateness, non-overlap and a single Antarctic cell simultaneously. **Closure criterion:** either a general rule removes the conflict, or the conventions are approved as a separate part of the model with an ID, rationale, domain and tests. Until then such exceptions must not be accepted silently.

## Q012 — How does Stage 2 determine the destination partition?

**Impact: the final Canonical Travel Regions partition inside every Stage 1 cell.** Rules R009 and R040–R042; decisions D024, D026, D027, and D029.

Stage 2 must treat destination semantics as first-class inputs while producing a deterministic, exhaustive, mutually exclusive refinement. Candidate factors include geographic coherence, destination identity, itinerary coherence, gateway or travel-graph structure, cultural-regional coherence, and stable traveller-facing destination concepts. Their definitions, interactions, thresholds, evidence requirements, and temporal behavior are not yet specified.

The open question is how to choose a reproducible destination partition without using desired territory names as hidden labels or allowing arbitrary subdivision. The solution must preserve `Stage2Partition refines Stage1Partition`. Q001/P3 cannot be used as a substitute because territorial/legal identity and destination identity are separate concepts.

Note, 2026-10-03 (D040): the Antarctic Stage 1 cell is divided in Stage 2 by how and from where travellers reach it, also taking into account how people who work there see it; the operational criteria belong to this question.

**Closure criterion:** publish a name-blind Stage 2 contract with typed inputs, deterministic conflict and uncertainty behavior, refinement tests, and adversarial cases. This patch does not choose that contract.

## Q013 — How are outlines and custom geometries sourced, pinned and versioned?

**Impact: every cell the substrate cannot represent.** R028, R047; D042.

R047 says where an outline comes from — a line the parties state — and that the substrate is extended with a custom geometry where it has no fitting unit. It does not say which sources carry such lines, how a geometry is digitised from them and pinned, how its version relates to the release and to the substrate's version, or how a cell is bound to substrate units when it does exist. As of 2026-10-03 only 23 of the register's 210 areas are linked to Natural Earth and 10 to Wikidata.

Narrowed on 2026-10-04 by D056: the sources are Natural Earth, GADM, OpenStreetMap and custom geometries from cited documents; left open is how a geometry is pinned and versioned and how a region is bound to substrate units.

**Closure criterion:** a design that, for each cell, names its geometry source and version, reproduces the geometry from a pinned input, and reports a cell whose substrate has no fitting unit instead of approximating it silently (consumer contract C6).

## Q014 — Which attributions make up the declared perspectives, and how are errors in them handled?

**Impact: which perspective-dependent areas become cells.** R045; D038, D039.

D038 declares ISO 3166-1 and the national points of view of Natural Earth. Not decided: whether Natural Earth's default attribution is also a declared perspective (the first world draft counted it); how features that equal a whole ISO 3166-1 entry, opaque codes for "shown as disputed" and plain errors in Natural Earth's columns are treated; and whether names may be taken from it (the proposal: attribution only, not names).

**Closure criterion:** a published reading of the pinned editions that lists each perspective, each correction with its source, and the resulting cells.

## Q015 — Scope test details: what is a top-level or detached unit, and what does a rule over several units give?

**Impact: which entry rules make regions.** R014, R056; D050.

The scope test of R056 needs: a source for a country's top-level units that is not tied to one substrate; what counts as detached (an island, an exclave) and as "a rule written for it, not a line in a list"; and what a unit "with exceptions" is. One rule over several top-level units satisfies the test for each of them (the owner's known rough case: five Mexican states under one card); whether that gives one region per unit or one region for their union is not decided — CR-W gives no witness between them.

**Closure criterion:** generic definitions with counterexamples, and a decision on rules over several units.

## Q016 — Areas with no single holder that are not regions

**Impact: special places in buffer zones, divided islet groups and undecidable control.** R048, R051, R052; D043, D045, D046.

Two cases have no decided outcome: (a) an islet group held in parts by several parties with no line between the parts — it has no single country in the canon's attribution; (b) a zone of kind `own_regime` that is not a region (no residents or no stated outline) — which region takes its land, given that the zone is never split between the neighbours; (c) — an area where the holder test of R048 cannot tell the parties apart — was closed by D055 (civil administration, otherwise no holder).

**Closure criterion:** a rule for each case that keeps R003/R004 and draws no line the parties do not state (R047).

## Q017 — Unclaimed land and areas with no agreed boundary

**Closed on 2026-10-03 by D054 (R058).** The owner confirmed the treatment agreed in principle once the outline principle (D042) and the holder test (D043) were adopted.

## Q018 — How are special places carried and attributed?

**Impact: every special place and how the consumer shows it.** R045, R046, R054; D041, D044, D048.

Open: how Track Your Regions carries special places (the owner expects a category of their own, something like "border curiosities"; to be raised with TYR as an importer need, not changed from here); how a declared perspective's attribution of a special place's land is reported when the land lies in a region of another country; what happens to a special place whose land lies in more than one region; and when a recently resolved dispute stays a special place.

**Closure criterion:** a release format for special places and the matching TYR importer need, with the attribution of each special place per perspective.

## Q019 — Release mechanics not yet decided

**Impact: the consumer's view of change between releases.** R032, R055; D049.

D049 fixes the yearly release, entry after two consecutive releases and exit after three years without the rule. Not decided: how the three years are counted against releases (calendar years from the suspension, or year-end cut-offs without the rule); whether releases ship a correspondence table between identifiers; whether a de-minimis rule applies to geometry corrections (the proposal: 1% of a region's area); and how a correction of an error of ours between releases is published.

**Closure criterion:** the owner decides each point, recorded in R055 or R032.

## What is intentionally not included in this list

Exact visa scopes of islands, the state of border crossing points, the current line of control, coastline quality and the availability of authoritative polygons are tasks of collecting and verifying facts. They are marked in the CSV as `evidence_status`/`premises`. Resolving them may unblock the application of an already defined rule, but does not automatically answer Q001–Q012.

The first useful experiment should compare several explicitly named profiles on one small set of facts. The main indicators: violated accepted constraints, the number of unresolved outcomes, the number of unjustified splits, the number of regions and the sensitivity of the result to a change of profile. Reducing unresolved by manually assigning the "correct" regions is not progress of the model.
