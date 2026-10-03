# Canonical Travel Regions — open questions of the model

Version: 0.3.0-draft. Date: 2026-09-12.

The order reflects the potential scale of change to the world map: from a change in the definition of almost all regions to changes in individual classes and in history. These are model questions. "Which document is required now?" and "Where does the line run on date t?" are data tasks, not separate items of this list.

## Q001 — Narrowed: CR-W accepted; CR-J normative adoption remains open

**Status: narrowed; resolved for regime-based mandatory separation.** Rules R007–R012, R038/R039/R044; decisions D032–D037. The current production Stage 1 core is `S1-core-v1`, CR-W only, with all five gates. One admissible witness is sufficient regardless of frequency; the absence of a certificate is not equality.

The open remainder of Q001: whether to accept CR-J as an independent institutional responsibility dimension when current hard D may be equal. CR-J is a well-defined normative candidate, not adopted; J1–J6 are fully preserved in [review §4.2](../experiments/q001/stage1-rule-review.md#42-operational-definition-independent_final_admission_jurisdiction) and the [candidate YAML](../experiments/q001/stage1-rule-candidates.yaml). A separate normative decision is needed, not additional geographic facts for the sake of a preferred outcome.

Undefined territorial/legal identity is rejected from the production and production-candidate core. `Q001.identity` is kept as a historical P3 model blocker, not as a mandatory production dimension. P3 is non-production/model-unresolved and is not the Stage 2 destination model. Possible preservation of exact legal status without CR-W remains Q006; a curated registry is not permitted by this decision.

P1/P2/P3 remain historical profiles whose results are not reinterpreted as `S1-core-v1`. D004–D007 are kept as accepted product regressions; if CR-W does not guarantee them, the conflict/requirement remains explicit, without automatic transfer to Stage 2. Residual Q002/Q004/Q005/Q006/Q007/Q008/Q009/Q011 remain open; the architectural Q012 is not resolved here either.

**Next distinguishing experiment:** synthetic NX-01/NX-02/NX-04 from the review — independent capacities versus offices/shared apex under fully identical D, with a check that these premises are compatible with exact S/H. **Closure criterion for the remainder:** explicitly accept or reject the additional institutional invariant CR-J with J1–J6 and generic counterexamples. This does not declare the full Stage 1 semantics complete. [Adoption record](../experiments/q001/stage1-core-adoption.md).

## Q002 — For which set of travellers and which decisions is homogeneity needed?

**Impact: almost all visa/permit/document boundaries.** R007, R011–R014, R038.

"An ordinary traveller" does not define a set: a citizen, a resident, a refugee, a holder of an emergency document, a researcher, a yachtsman and a tourist may have different rights. Is a split required for one rare class? Should long stays, work, medical and diplomatic trips be included? Dependence on the route may also be non-territorial.

The part resolved by D032/R044: in the accepted civilian-short-stay-v1, one valid class-based witness is sufficient without a frequency threshold, including rare documents; S must not be changed for the sake of an individual case. The remainder is the exact applicability and the extension of the context/hard-output domain, not a repeated choice of a frequency threshold.

Options: universality for all persons/purposes; a fixed civilian short-stay scope; typical profiles with explicitly acknowledged incompleteness. The specification provisionally chooses the second option and allows rare documents. The domain C must not be changed for the sake of a convenient result in an individual case. Completeness applies only to the explicitly chosen profile and scope: it does not mean knowledge of all conceivable traveller contexts outside them.

**Experiment:** run one and the same geographic set for an ordinary passport, several citizenships, a refugee document, a residence permit, arrival by yacht and a long stay. **Closure criterion:** the formal scope C and the list of hard outputs are published; it is known which differences intentionally remain overlays.

## Q003 — What does it mean to cover the whole travel space?

**Impact: a huge part of the Earth's surface and all boundary features.** R002–R004, R025, R026; D001, D016, D017.

A destination-only universe requires a definition of destination and changes with accessibility. Land-only excludes travel by sea and over shelf ice. The full surface requires a partition of the ocean, the high seas, ice and ambiguous coastal features. Air and underground travel would require a different dimensionality, not new land polygons.

The relation of the territorial sea to land needs to be defined: does it belong to the same region, to a separate maritime region, or is it outside the universe? An EEZ must not automatically be treated as the same kind of territory. Antarctica land and the Treaty Area are also distinct. LAND_V0 is an explicit temporary limitation of the experiment.

**Experiment:** inland lake, South Pole, ice shelf, ocean cruise point, low-tide reef, reclaimed island, closed island. **Closure criterion:** for each physical type, inclusion and the principle of classification are defined, independently of sovereignty and accessibility.

## Q004 — Do customs and biosecurity really divide canonical geography?

**Impact: from a few special territories to a large number of internal zones.** R013, R016, R017; D011.

A choice is needed between a mandatory split by traveler-facing formalities, all such formalities as overlays, or a limited class of external customs jurisdictions. The problem is not whether there is a declaration on a particular island: even knowing all the rules, the boundary of the class has to be explained.

**Experiment:** Åland, Canary Islands, Ceuta/Melilla, Heligoland, Büsingen, Livigno, Tasmania, Hawaii, California. First compare the formalities without names and political statuses. **Closure criterion:** one test applies to external and internal zones; if an identity correction is needed, the dependence on Q001 is explicit.

## Q005 — Where does a region end and an access overlay begin?

**Impact: thousands of permit areas, parks, bases and protected islands.** R009, R014, R017, R025–R027.

If every mandatory permit is sufficient, a multitude of objects will become regions of their own. If all permits are overlays, many restricted destinations are lost. The word destination by itself does not solve the problem. Area or number of visitors create an arbitrary scale unless approved as a product parameter.

R014 already excludes local border, military, nature-conservation, site-specific, route-specific and activity-specific restrictions from the sufficient grounds for a split. This remains true even if the overlay coincides with a whole district or federal subject: administrative scale is not a criterion. The open part of Q005 is now narrower: which general predicate distinguishes such an overlay from a permission for ordinary civilian admission into the candidate territory as a destination as a whole.

**Experiment:** Mount Athos, Tibet, Galápagos, Lord Howe Island, North Sentinel Island, Montserrat exclusion zone, Antarctic protected area, an ordinary national park and airport airside. **Closure criterion:** a scope-level predicate or an honestly approved convention of size/institution, not a list of exceptions by name.

## Q006 — Should a legal dispute preserve a separate identity without travel discontinuity?

**Impact: all disputed/occupied areas and the residual regions of controlling states.** R010, R016, R022, R024; D006, D007, D013, D014.

Different de facto authority inside a disputed area justifies an internal split. It does not prove separation from the ordinary territory of the same controller. Claims are declared overlays, but D007 requires that Western Sahara not be dissolved into Morocco. One must not quietly add "disputed=true" to the hard signature and keep asserting that a dispute divides nothing.

Options: only proven access/legal-route consequences; an independent international-status identity criterion; a separate product class of disputed territories with explicit inclusion rules. In the third option it has to be explained what distinguishes a significant dispute from any border claim.

**Experiment:** the western part of Western Sahara vs Morocco; Crimea vs ordinary Russia; Golan vs Israel; Aksai Chin vs China; an unenforced claim to ordinary territory. **Closure criterion:** D006/D007 are explained by a general norm, or it is recorded which accepted constraint is incompatible with the chosen model.

## Q007 — How to represent joint, gradual and shifting control?

**Impact: conflict zones and the precision of the overall partition.** R015, R024, R028–R030.

Who controls entry, who patrols at night, who administers civilian affairs and who applies the law are not always one actor. Even with perfect observations, a binary controller may not exist. A choice is needed: a vector of functions, a primary control role, or special zones of joint regime.

A separate question: is a complete point-wise assignment mandatory as a computational convention, or must it also mean confident knowledge? The specification allows a provisional assignment with uncertainty, but not an invented factual contour.

**Experiment:** West Bank Areas A/B/C, Gaza, Cyprus buffer zone, UNDOF area, Siachen, Ukraine frontline. **Closure criterion:** a model of control functions and the behaviour for an uncertain strip are defined; an observation update does not pass it off as a change of sovereignty.

## Q008 — What stability is needed for a new boundary to change the partition?

**Impact: the map over time, especially sanitary restrictions and conflicts.** R012, R015, R017, R031.

A "temporary measure" may last for years, while a new permanent jurisdiction has so far existed for one day. A threshold of 30/90/365 days would be a model decision, not a fact. It has to be decided whether we assess the intended duration, the institutional nature, the actual duration, or a combination with hysteresis.

R044 adopts a narrow sufficient standing/constitutive gate for CR-W without an age threshold; incident/emergency measures are not promoted by duration. The remainder of Q008 is ambiguous institutional classification and fuller temporal semantics; the question is not closed.

**Experiment:** one scope with restrictions for 1 day, 3 months and an indefinite period; a change of control with identical travel consequences; a new admission jurisdiction with a published start date. **Closure criterion:** the stability predicate does not require knowledge of the future and defines split/merge events without exceptions by country.

## Q009 — How much spatial dependence is admissible inside one region?

**Impact: the number of cells after intersecting all scopes.** R006–R009, R014, R017, R027.

If TravelDecision may refer to coordinates arbitrarily through overlays, the whole Earth can be left as one region. If coordinates are forbidden altogether, one airport with several procedures destroys homogeneity. Hard dimensions, invariant inside a region, and soft dimensions, for which internal geography is allowed, need to be defined.

**Experiment:** a common admission regime plus different entry points, transit procedures, local permits and a customs zone crossing a control boundary. **Closure criterion:** an identical signature guarantees exactly the enumerated homogeneity; overlays are not used to bypass mandatory splits.

## Q010 — When does region_id change and how are visits recomputed?

**Impact: historical sets and user accounting, not necessarily the number of today's regions.** R031–R033.

After a small change of a boundary, both identities can be kept. After a part is carved out, a successor is usually needed. But the quantitative boundary between these events is not defined. The percentage of area should not be used as a hidden criterion.

Provisional hypothesis: split/merge create new IDs; a rename and a digitization correction keep the ID. It is not decided how to treat "the same territory" after a change of status, nor how to map a visit in the past onto the modern set.

**Experiment:** rename; coastline correction; transfer of an enclave; division of an admission jurisdiction; merging of two regions; late correction of an old line. **Closure criterion:** an event taxonomy and rules for historical/current visit views are published without loss of the original evidence.

## Q011 — Are explicit product conventions admissible?

**Impact: honesty and manageability of exceptions, especially Antarctic/identity cases.** R008, R010, R026, R035; D004, D016.

A fully derived map may contradict the intuitive requirements of the project. A managed list of conventions is technically admissible, but it changes the meaning of falsifiability: what is then checked is conformance to the rules and the published conventions, not only to independent facts.

**Experiment:** try to satisfy literal UKOT-separateness, non-overlap and a single Antarctic cell simultaneously. **Closure criterion:** either a general rule removes the conflict, or the conventions are approved as a separate part of the model with an ID, rationale, domain and tests. Until then such exceptions must not be accepted silently.

## Q012 — How does Stage 2 determine the destination partition?

**Impact: the final Canonical Travel Regions partition inside every Stage 1 cell.** Rules R009 and R040–R042; decisions D024, D026, D027, and D029.

Stage 2 must treat destination semantics as first-class inputs while producing a deterministic, exhaustive, mutually exclusive refinement. Candidate factors include geographic coherence, destination identity, itinerary coherence, gateway or travel-graph structure, cultural-regional coherence, and stable traveller-facing destination concepts. Their definitions, interactions, thresholds, evidence requirements, and temporal behavior are not yet specified.

The open question is how to choose a reproducible destination partition without using desired territory names as hidden labels or allowing arbitrary subdivision. The solution must preserve `Stage2Partition refines Stage1Partition`. Q001/P3 cannot be used as a substitute because territorial/legal identity and destination identity are separate concepts.

**Closure criterion:** publish a name-blind Stage 2 contract with typed inputs, deterministic conflict and uncertainty behavior, refinement tests, and adversarial cases. This patch does not choose that contract.

## What is intentionally not included in this list

Exact visa scopes of islands, the state of border crossing points, the current line of control, coastline quality and the availability of authoritative polygons are tasks of collecting and verifying facts. They are marked in the CSV as `evidence_status`/`premises`. Resolving them may unblock the application of an already defined rule, but does not automatically answer Q001–Q012.

The first useful experiment should compare several explicitly named profiles on one small set of facts. The main indicators: violated accepted constraints, the number of unresolved outcomes, the number of unjustified splits, the number of regions and the sensitivity of the result to a change of profile. Reducing unresolved by manually assigning the "correct" regions is not progress of the model.
