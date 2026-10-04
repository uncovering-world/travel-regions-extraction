# Canonical Travel Regions — working specification

Version: 0.4.1-draft. Date: 2026-10-04. Status: CR-W is accepted as the current production Stage 1 core, amended on 2026-10-03 (R056); Stage 1 also refines a reference registry of countries (R045) and applies rules for disputed and special-status areas (R046–R054); releases are yearly and built under the product profile `S1-product-v1` (R055, R057). The full Stage 1 semantics and the world classification are not complete.

Changes in 0.4.0-draft: R045–R059 added from the owner's decisions of 2026-10-03 and 2026-10-04 (D038–D064); R009, R014, R016, R026, R039 and, by D055, R048 amended in place; dated notes added to R007, R010, R013, R015, R017–R019, R022–R025, R027, R028, R030–R032, R038, R044; check V011 added. The evaluator's `SPEC_VERSION` stays `0.3.0-draft`: its input contract and checks are unchanged (see the note under R044).

## Basis and limits of reliability

The document relies on the user's assignment of 10 September, the current assignment, the two versions of Deep Research that were read, and the fragment of the architectural discussion that was found. The sources and the degree to which decisions are accepted are listed in [decisions.md](decisions.md). The full transcript of the architectural dialogue has not been recovered. A specific implementation language, DBMS, geometry engine and geodata provider are not considered chosen.

The research versions diverge: the first version defines territories predominantly through travel regimes, the second adds an independent territorial identity. The wording "minimal practically useful territory" does not define an unambiguous algorithm: arbitrary further subdivision also preserves homogeneity. What is proposed here is **the coarsest partition that preserves all justified mandatory distinctions**. This is a new formalisation, not a previously accepted decision.

Each normative item has an immutable ID. `accepted` means a direct requirement of the user; `tentative` — a working hypothesis that holds within the experiment; `unresolved` — a predicate for which a final decision cannot yet honestly be issued. Rule statuses are not an assessment of the reliability of geographic facts. Qxxx references lead to [open-questions.md](open-questions.md).

## Purpose, universe and partition

### R001 — Purpose of the system [accepted]

The system builds a reproducible single-level partition of space for recording and planning travel. It must explain every separation by references to general rules and input facts. At this stage the result is the specification and counterexamples, not a final list of the world.

### R002 — Explicit universe [tentative; Q003]

The universe is defined by a separate versioned mask U, not by a list of countries and not by an enumeration of places accessible to tourists. Working profile `LAND_V0`: all permanent land at the published coastline epoch, including islands, deserts, closed territories, artificial reclaimed land and Antarctica. Inland waters are included by a separate mask. The grounded ice sheet is included; floating sea ice, ice shelves, marine waters, airspace and underground volumes are for now outside this profile. Borderline feature types must be explicitly labelled rather than dropped on loading.

LAND_V0 is a limitation of the first experiment, **not a claim that all possible travel is confined to land**. Literal coverage of the Earth's surface requires a different universe and a decision on Q003. A build without a published mask, epoch and shoreline definition is considered incomplete.

### R003 — Exhaustive coverage [accepted]

For fixed U and moment t the union of the regions equals U. Every point of U is assigned to exactly one region. The absence of population, of permission to visit, of a recognised sovereign or of geodata does not exempt from the coverage requirement. An experiment may show an unresolved area, but must not pass it off as a completed canonical classification.

### R004 — Mutually exclusive regions [accepted]

The point sets of the regions are pairwise disjoint. In the file representation closed polygons may share edges and vertices; ownership of these points is established by R029. An intersection of positive area is forbidden. A nonzero overlap must not be hidden by drawing order.

### R005 — Single-level hierarchy [accepted]

Parent/child inclusion relations between simultaneously valid canonical regions are forbidden. Political entities, archipelagos, historical areas, disputed areas and policy areas exist in other object types. Links to them allow many-to-many and intersections. The historical predecessor/successor link is not a hierarchy of current regions.

Stage 1 and Stage 2 are construction stages, not levels in the published ontology. Only the Stage 2 output is the final Canonical Travel Regions partition, and that output remains single-level.

### R006 — Definition of a canonical travel region [tentative; Q001]

A canonical travel region is a nonempty class of points of U in the published Stage 2 partition that has a stable identity, a geometry at moment t and explicit links to the applicable travel policies, legal-status records and control records. Inside the class no proven mandatory separation remains under the chosen version of the specification. Trip conditions are computed without implicit inheritance from another canonical region.

Canonical means "an unambiguous result given fixed rules, facts and parameters", not "the only correct natural division". A separate territory does not mean a separate state. Regions may have MultiPolygon geometry.

## Formal construction procedure

### R007 — Traveller context and verifiable difference [tentative; Q002]

For the current `S1-core-v1` the accepted gates of R044 apply: a single versioned civilian short-stay scope, a consistent nonempty class-based C, a matched logical trip and all influencing exceptions. One admissible rare class is sufficient without a frequency threshold. A refusal outcome on one side is admissible; an actually completed trip and permitted entry to both sides are not required. Normative requirements/admissibility are compared, not different discretionary decisions of officers. The full set of future traveller contexts remains Q002.

Context C contains citizenships, documents and their types, residency, purpose, duration, previous trips, route, point of entry, mode of transport, accompanied goods/animals and date. The baseline scope of the experiment: civilian short-term visits, including rare documents and special permissions; work, settlement, diplomatic and military missions do not form a primary split. The duration limit is set by the applicable policy, not by a universal 90 days.

TravelDecision distinguishes admission, the required authorisation, the accepted documents, the conditions of stay/exit, mandatory procedures, physical accessibility and legality under each relevant jurisdiction. A split based on a difference in conditions needs a **witness**: a concrete admissible C and two destinations A/B for which a material decision differs. The route is compared for the same class of trip; a mere difference in destination coordinates or airport names is not a witness.

Note, 2026-10-03 (D050): R056 narrows which classes are witnesses — transit, organised-group-only and local-border-traffic classes are not; a rule that admits visitors only through a tour operator is.

### R008 — Certificate of mandatory separation [tentative]

`must_separate(A,B,profile)` and `hard_compatible(A,B,profile)` are independent Stage 1 predicates. `must_separate` means sufficient positive evidence forbids A and B from occupying one final canonical travel region under the selected profile. `hard_compatible` means positive evidence establishes equivalence across the profile's complete hard signature and no mandatory-separation certificate applies. It means only that Stage 1 requires no boundary between A and B. It does not decide whether Stage 2 places them in one final region. `not must_separate` does not imply `hard_compatible`.

Each `must_separate(A,B,profile)` contains rule_id, versioned profile/traveller scope, the geographic scope of A/B, as_of, verified premises and facts with sources. In production `S1-core-v1` only a CR-W certificate under R044 with all five gates is sufficient. The institutional grounds of R011 are available only to the historical experiments P2/P3, not to the current production profile. Absence of a CR-W certificate is not `hard_compatible`. An unknown premise remains unknown and does not turn into false.

`must_separate(A,B)` means that no final region contains points of both areas. This does not promise that A as a whole becomes exactly one region: an additional split inside A is possible.

### R009 — Two-stage partition construction [accepted; Q001, Q005, Q012; amended by D038, D050, D051]

1. Fix U, time, rule profile, and facts. Build candidate geometries without using desired output names.
2. Build their common geometric refinement as technical atoms. These atoms are not user-visible regions.
3. Stage 1 computes the coarsest partition that refines the reference registry (R045), applies the rules for disputed and special-status areas (R049–R054) and satisfies the accepted hard rules of the versioned profile (CR-W, R044 as amended by R056). A release is built under the product profile `S1-product-v1` (R057). Accepted product regression constraints without a derivation are reported as unresolved requirements, not inserted as hardcoded boundaries. For each atom, evaluate the profile's hard signature as specified by R038.
4. `signature_complete(A,profile)` is true only when every required profile dimension has an evidence-backed `known_value`, `known_absence`, or justified `not_applicable` state. `unknown` and `unresolved_model_semantics` make the signature incomplete.
5. `signatures_equal(A,B,profile)` can be true only when both signatures are complete and every typed hard dimension is equal. A finite set of traveller examples cannot prove completeness.
6. `hard_compatible` requires complete equal hard signatures and no applicable `must_separate` certificate. Absence of a witness, an empty search result, and `not must_separate` are not positive compatibility evidence.
7. Stage 2 processes each Stage 1 cell independently and may subdivide it using destination-partition semantics. Stage 2 may never combine points from different Stage 1 cells.
8. The final canonical partition is the Stage 2 output. Stage 1 output is an internal construction boundary, not a final region assignment.

Hard-signature equality must be an equivalence relation, and Stage 1 must be order-independent. If hard constraints permit multiple coarsest partitions, the Stage 1 result is unresolved; names and political labels cannot break the tie. The rule for selecting the destination partition within each Stage 1 cell remains open in Q012.

### R010 — Independent territorial identity [not accepted as a hard separator; Q001, Q006]

The second version of the research proposes forbidding the merging of stable external territorial jurisdictions even when travel policies are equal. There is as yet no general verifiable definition of "external" and "independent" identity. Neither an ISO code, nor a flag of its own, nor tourist renown substitutes for it.

Territorial/legal identity alone is not an accepted Stage 1 hard separator. Undefined identity is excluded from production and production-candidate semantics. P3 is retained only as a historical non-production, model-unresolved profile: when the result depends on identity it returns `model_unresolved` / `Q001.identity`; an already proven historical P1/P2 split is preserved. P3 is not a Stage 2 destination model. A registry, an ISO code and curated exceptions do not replace the predicate. A possible future precisely defined legal-status rule requires a separate decision on Q006; undefined identity does not block completeness of the current CR-W core.

Note, 2026-10-03 (D038): the reference registry of R045 separates countries and perspective-dependent areas. It is a declared product rule with a pinned external source, adopted by the owner, not an identity predicate; this item's statement that a registry does not replace an identity predicate still holds.

### R011 — Immigration / admission jurisdiction [well-defined normative candidate; not adopted]

CR-J remains a well-defined normative candidate, not adopted. Its full six-part definition J1–J6 is preserved in [review §4.2](../experiments/q001/stage1-rule-review.md#42-operational-definition-independent_final_admission_jurisdiction) and [candidate schema](../experiments/q001/stage1-rule-candidates.yaml): constitutive allocation, territorial legal effect, reserved ordinary competence, non-substitution, attribution/delegation/review closure and effective territorial application. No premise is abridged. Capacity is not equal to an office, visa issuer, enforcement actor or sovereign label.

CR-J may require a boundary where the current hard decision functions are identical; this is a separate normative choice about institutional responsibility. It is not accepted as a current travel discontinuity and is not part of the production hard signature/completeness. Historical P2/P3 retain the former experimental R011 semantics. Proven traveller consequences of institutional facts may support CR-W, but a difference in competences does not by itself give a production split.

### R012 — Visa / immigration scopes [tentative]

Different territorial visa/ETA/permit/document applicability requires a split given a verified CR-W certificate under R044, including all five gates, both proven sides of the decision and relevant exceptions. One valid class-based witness is sufficient regardless of the frequency of the class. A common visa does not prove full hard equality. A change of requirements simultaneously across the whole area updates the policy, but not necessarily the geometry.

### R013 — Customs, biosecurity, fiscal scope [unresolved; Q004]

The customs territory, the VAT territory, the excise territory and the biosecurity zone are different attributes. One is not derived from another. Working hypothesis for the experiment: mandatory declaration of accompanied baggage, inspection/quarantine or import restrictions on ordinary movement across a stable territorial boundary may require a split; a difference in the local tax rate is not sufficient.

It is not resolved why this test should separate, for example, a special island zone but not every internal biosecurity zone of a large state. Until the boundary of the class is defined, `customs-only` and `biosecurity-only` cases give `model_unresolved`, not an automatic split. Customs never substitutes for immigration.

This is the unresolved state of an additional experimental hard rule. In `S1-core-v1` an independent customs/biosecurity dimension is not accepted and is not required for completeness; such a label alone does not block positive equality of the accepted dimensions. If a specific alleged CR-W effect has an unresolved hard classification, the blocker of the corresponding gate is retained.

Note, 2026-10-03 (D050): a mandatory fee or purchase on arrival is not a separator; it is recorded as a marker (R056). Customs and biosecurity formalities as such remain Q004.

### R014 — Destination permits and special zones [unresolved; Q005; amended by D050]

Amendment, 2026-10-03 (D050, R056): a standing rule that makes presence in a whole unit conditional on a permit for an ordinary visitor (a civilian short-stay class) separates that unit, for the units that pass the scope test of R056 — a whole top-level unit of its country, or a smaller detached unit with a rule written for it. This is the explicit convention Q005 asks for. A permit for a part of a unit stays a marker, and the overlay default below continues to cover everything else.

In current production only a territorial legal effect that has passed G-HARD and the other gates of R044 gives CR-W. The unresolved boundary between territorial presence permit and spatial overlay remains Q005/Q009, even if the permit is verified. Whole administrative scope, the size and the name of the destination do not close the gate.

A permit that regulates access to a place inside an already accessible traveller-facing admission jurisdiction is by default a spatial access overlay, not a ground for a split. This class includes tickets and bookings, border and military zones, guarded facilities, local nature reserves, closed routes and activity-specific permits. Their geometry may cross administrative boundaries or coincide with an entire municipality, district and even a federal subject: area and coincidence with an administrative unit do not by themselves turn an overlay into a canonical region.

Such a local difference is not an R007 witness between the containing territory and the rest of the same admission jurisdiction: it answers `LocalAccessDecision(point_or_route,C,t)` after general admission, not `TravelDecision(destination,C,t)` about admission to an independent destination. An overlay stores its own geometry, purpose, affected traveller classes, permit issuer and validity. For a border zone or another restricted-regime zone it is recorded separately whether the permit applies to the whole zone, only to an inner strip, to a specific route or to a type of activity.

A permit that regulates ordinary civilian admission to the candidate territory as a destination as a whole, rather than access to a place, route or activity inside it, remains a split candidate. A general verifiable boundary between a whole-destination permit and a large spatial overlay is not yet defined. Size of area, visitor numbers, duration of the permit and administrative rank are not declared to be hidden thresholds. If the outcome depends on this boundary, the result is `model_unresolved`.

### R015 — De facto control [tentative; Q007]

A control label or a difference in military control does not by itself require a split. Control evidence may support CR-W if it proves an actual hard territorial travel consequence and all gates of R044, including territorial legal effect and standing rule. A difference in physical coercion without a defined hard consequence is not added as a hidden dimension; civil, military, border and enforcement roles remain separate, shared/noninstitutional control is Q007, temporal uncertainty is Q008. Uncertain operational geometry does not turn into a precise line without R030.

Note, 2026-10-03 (D043): who holds an area is defined by R048 (the party that can in practice admit, refuse and remove a civilian), and a forcible change of control changes the canon's attribution only under the settling rule R049. A label still does not split by itself.

### R016 — What is not sufficient for a split by itself [tentative; amended by D038]

Amendment, 2026-10-03 (D038): an entry of ISO 3166-1 and a country boundary under a declared perspective of the reference registry do separate, through R045 — not as a CR-W `must_separate`, but as a declared registry boundary. A territorial claim separates only where a declared perspective shows it, and then subject to R050–R054. The statements below about an ISO code, a claim and recognition apply to everything else: ISO 3166-2 and other codes, and claims or recognition that no declared perspective shows.

Accepted for current production: `disputed=true`, `claim exists`, `recognition differs`, `controller label differs`, `military control differs`, dependency label, autonomous status, overseas status and island status **are not independently sufficient separators**. Their actual hard territorial travel consequences may take part in CR-W evidence; labels do not become signature dimensions. Accepted product regressions D004–D007 are kept separately from derivable hard rules.

An administrative boundary, autonomy, language, ethnicity, religion, currency, flag, time zone, ISO code, political recognition, territorial claim, a separate stamp, island status, remoteness, tourism identity, destination recognisability, itinerary usefulness and transport inconvenience do not by themselves create a Stage 1 `must_separate`. This is not a prohibition of a split on other hard grounds, nor a prohibition of Stage 2 subdivision by destination semantics. A negative test means "this factor is insufficient", not "all other factors are absent".

### R017 — Overlays and independence of rules [tentative]

EU/Schengen/CTA and other common areas are reusable versioned policies. Claims, recognition, advisories, sanctions, temporary sanitary restrictions, routes and local access zones may have their own geometry and may intersect. The search for an applicable overlay must take the point/route/C/t into account, not only region_id.

The presence of an overlay does not cancel a verified CR-W split under R044. Otherwise any heterogeneous space could be declared one region with arbitrary nested checks. The homogeneity of R006 refers to the approved hard dimensions, not to all possible local rules. CR-J is not accepted; historical R011 splits do not substitute for the current production norm.

Note, 2026-10-03 (D040, D050): the territorial limits of a transit regime, group-only schemes, local border traffic schemes, fees on arrival, permits for part of a unit and entry rules whose scope fails R056's scope test are markers (R046), that is, overlays in the sense of this item. Antarctic claims stay overlays (R026).

## Categories of territories

### R018 — Dependent territories [tentative; Q001]

Dependency creates a political relation and a candidate for analysis. Metropolitan policies must not be inherited without evidence. In the current core a split requires CR-W; an independent admission jurisdiction without it remains the non-adopted CR-J candidate, dependency/overseas status is not a separator. D004 is retained as an accepted product regression constraint, but is not guaranteed by CR-W and is not hardcoded. One dependent territory may contain several regions; claims cannot violate R004.

Note, 2026-10-03 (D038): a dependent territory with its own ISO 3166-1 entry is separated through the reference registry (R045); the dependency label itself still does not separate. The British Antarctic Territory stays inside the Antarctic cell (R026, D040).

### R019 — Overseas territories [tentative; Q001]

Overseas parts are checked individually regardless of the form of the constitutional link: department, collectivity, overseas country, etc. Distance from the metropole and membership of the "French overseas"/"British overseas" family are insufficient for a specific merge or split. Non-equivalent immigration scopes require separation from the metropole under R012; merging overseas parts with one another is checked separately.

Note, 2026-10-03 (D038): an overseas part with its own ISO 3166-1 entry is separated through R045 regardless of its immigration scope.

### R020 — Autonomous regions [tentative]

Autonomy does not mean a separate region. What is checked is the real powers of admission, permits, customs and special regimes. The same test is applied to the autonomies of any state; political prominence does not serve as an exception. Åland, Hong Kong and Sicily are candidates with potentially different grounds, not one class of expected outcome.

### R021 — Geographically isolated territories [tentative; Q001]

An island, an exclave and the need to transit through a neighbouring state do not by themselves require a Stage 1 split. Given a proven equal hard signature, Stage 1 allows a MultiPolygon. The route graph preserves the path through other regions. Stage 2 may still split an island or remote area when future destination-partition rules justify it; that decision does not alter territorial/legal identity under R010.

### R022 — Disputed territories [tentative; Q006]

A dispute creates a dispute object with geometry and legal positions, but not automatically a canonical region or a Stage 1 boundary. A proven territorial admission/legal-route/access consequence may give CR-W under R044; dispute/claim/recognition are not sufficient by themselves. A claim polygon does not assign points. The requirement to keep a legal-status area separate without CR-W remains unresolved Q006, and the accepted D006/D007 do not turn into rules and are not considered satisfied by overlays or by a future Stage 2.

Note, 2026-10-03 (D038, D044–D048): a disputed area is separated where a declared perspective of the reference registry places it in another country (R045), and the register of disputed and special-status areas decides by kind whether an area is a region, a special place or a marker (R050–R054). D006 and D007 are expected to follow from R045; they stay accepted constraints until a release check confirms it (D036).

### R023 — De facto states [tentative]

The de facto system of territorial admission is assessed under CR-W/R044 regardless of the number of recognising states. The independence of admission competence is assessed separately as the non-adopted CR-J candidate of R011. Counterexample: the same hard decisions as before, with recognition having changed, do not give a new split. The name of a state and a claim contour do not replace operational scope.

Note, 2026-10-03 (D038, D043, D050): a de facto state is separated where a declared perspective shows it (R045), or by the holder's own entry rule for the area with an outline the parties state (R056, rule for held areas), and at the latest when the canon accepts its holder under R049.

### R024 — Occupation and disputed control [tentative; Q006, Q007]

De jure sovereignty/legal status, de facto control and traveller reality are stored separately. The first includes the normative basis and the position of a competent source, not merely an interchangeable list of claims. The second describes enforcement on the ground. The third contains physical access and legality_under each relevant jurisdiction; being let through in fact does not prove the legality of the route.

If a CR-W discontinuity is proven inside an area, the corresponding scopes are separated under R044. Separation from the ordinary territory of the same controller requires its own CR-W certificate; an internal control boundary does not replace it. D006 concerns ordinary Ukraine, D013 about ordinary Russia remains tentative; D007 is not guaranteed in the absence of CR-W. International legal status is stored independently of claims, but the label itself is not a hard dimension. Legal applicability to C must be proven independently of a bare claim, otherwise Q006. Neither occupation nor military control automatically defines a contour or the number of cells.

Note, 2026-10-03 (D043): the canon's attribution of an area whose control changed by force follows the settling rule R049; while the line moves, no area is delimited and the regions touched carry a flag.

### R025 — Uninhabited and closed territories [tentative]

All their points that fall within U take part in the partition. `visitability = closed/restricted/unknown` is a property, not a ground for exclusion. Being uninhabited does not require a separate region_id. Separate permits are checked under R014. The absence of a confirmed controller is encoded explicitly; adjacency does not give the right to attach a territory automatically.

Note, 2026-10-03 (D045, D046): for register areas of kind `islets_for_maritime_zone`, `paper_claim` and `own_regime`, resident civilians are one condition of being a region (R051, R052); an uninhabited area of those kinds is a special place. For islets and paper claims its land goes with its holder, not with a neighbour by adjacency; for zones with no single holder the region that takes the land is open (Q016).

### R026 — Antarctica [Stage 1 part accepted; D040; Q003, Q012]

Amendment, 2026-10-03 (D040): Stage 1 has one cell for the Antarctic land included in U south of 60°S. National claims remain overlays; they create no Stage 1 boundary, including where a declared perspective of the reference registry (R045) would attribute a sector to a claimant. Stage 2 divides the cell by how and from where travellers reach it, also taking into account how people who work there see it; the operational criteria are part of Q012. This is an explicit convention adopted by the owner (Q011), not a derivation.

Original baseline (2026-09-12), kept for history: one canonical cell for the Antarctic land included in U south of 60°S; national claims remain overlapping overlays. This is a working choice, not the conclusion "one treaty = one region". Stations and protected sites are initially access overlays. National authorisation of an expedition, which depends on the organiser/route, does not by itself divide geography. A proven territorial admission boundary brings back the question of R014.

The area of application of the treaty includes more than land: the Treaty Area must not be unconditionally equated with the geometry of this cell. The Antarctic portions of TAAF, British Antarctic Territory and other claimed sectors are not created as a second layer of canonical polygons. This is an explicit limitation of the general requirement about separate overseas territories (D004/D016), not a hidden exception.

### R027 — Transit, preclearance and border crossing points [tentative]

For CR-W, the place of processing is distinguished from the territorial legal effect. A matched logical route class may condition a territorial document/admission rule; the names of the port and of the carrier, the queue and processing logistics do not by themselves split. Site/activity/entry-event differences do not satisfy G-HARD without a proven territorial effect; the absence of a route is not encoded as a legal refusal.

Airside, the port procedure, foreign preclearance and the stamp belong to EntryPoint/EntryEvent. They do not move physical geography into another state. Entry in the immigration sense and physical presence are separate. A counterexample to a split is an airport with different transit and landside rules without an independent territorial jurisdiction.

Note, 2026-10-03 (D050): a class whose trip is defined by onward travel to a third territory is not a CR-W witness, and a transit regime's territorial limits are an overlay (R056).

## Geometry, time, reproducibility

### R028 — Choice of boundary by the ground of the split [tentative]

In production the boundary is taken from the certified CR-W scope. G-SCOPE requires nonempty disjoint scopes and a proven effect on each fragment being certified; heterogeneous/overlapping reference objects first require explicit disjoint fragments. A witness between points does not prove blanket separation of the containing entities. An administrative polygon is allowed only as a documented proxy with its accuracy and basis. A claim line, an advisory buffer and a military map do not replace a scope certificate.

Intersecting mandatory boundaries refine one another. The rule "the last polygon wins" and the blanket precedence from the first version of the research are **not accepted** here: they can erase another mandatory distinction. Contradictory descriptions of one boundary go through R030/R034. There is no approved universal ranking of all providers.

Note, 2026-10-03 (D038, D042): registry boundaries come from the pinned editions of R045. The outline of a cell for a register area or a held area is a line the parties themselves state, never one drawn here (R047); where the substrate has no fitting unit, a custom geometry from a cited source of that line is added. How such geometries are sourced, pinned and versioned is Q013.

### R029 — Topology and points on the boundary [tentative]

The build fixes the CRS, coordinate precision, snap tolerance, antimeridian/poles rules and engine version. Polygon interiors do not overlap. For a shared line/vertex the geometric lookup chooses the minimal region_id in byte-wise lexicographic order among all incident regions and returns `on_boundary=true`. The ID is not computed from the display name. The rule is technical and does not express sovereignty.

Checkpoint lookup does not override territory(point): a separate query returns departure_region and arrival_region. A zero-area case must not create a separate cell. Neither a sliver nor an island smaller than the tolerance is removed silently: the error/mask change and the area are recorded. Computational tolerance does not permit arbitrary geographic gaps.

### R030 — Uncertain boundaries [tentative; Q007]

The original estimate of the boundary, uncertainty geometry/precision, the date and the alternatives are stored. Approximate assignment is admissible in an explicitly provisional release with a quality flag; this is a single technical answer, but not exact knowledge of control. If even such a choice has no justification, the build returns the unresolved area separately and does not receive the status of a complete canonical release. An unknown area is not automatically a buffer state or terra nullius.

Note, 2026-10-03 (D042, D043): a front line is never drawn. While fighting moves the line, no area is delimited; the regions touched keep their attribution and carry a flag (R049).

### R031 — Temporal model [tentative; Q008]

For the current CR-W the sufficient G-TIME of R044 is accepted: an effective-at-t standing class-based or constitutive instrument, not activated exclusively by a specific incident/emergency/event. There is no age/duration threshold: a new standing jurisdiction/rule may take effect immediately; expiry does not by itself exclude a norm; a long emergency restriction does not become standing through age. An undetermined classification remains Q008. Revision between releases does not violate R041 on the refinement of the stages of one version.

A fact, policy membership, geometry and control record have `valid_from <= t < valid_to`, where an open end is denoted by null. `recorded_from/recorded_to` are stored separately: when the system knew this version of the fact. `retrieved_at` and `last_verified_at` do not replace the time of truth. An unknown effective date remains unknown, not the date of loading.

A lookup specifies world_time and release_id/knowledge_time. A historical correction creates a new version of knowledge without rewriting the published result. A change of a visa requirement without a change of hard territorial scopes does not require a new region_id.

Note, 2026-10-03 (D049): this item and G-TIME describe facts at a date t; they are unchanged. Which factual changes reach the consumer is decided at the level of yearly releases (R055): a boundary created by an uncontested entry rule enters only after two consecutive releases and leaves only after three years without the rule; contested control follows R049.

### R032 — Identity under split/merge [tentative; Q010]

For a pure renaming and a digitisation correction the region_id is kept and the revision changes. On a semantic split the old ID is closed, and all new regions receive new IDs and `split_from`. On a merge a new ID with `merged_from` is created. Old IDs are not reused. A boundary transfer of area between persisting jurisdictions changes the geometry revision and the event log; if the territorial identity itself changes, split/merge applies. Where this boundary lies is examined in Q010.

A visit event stores the time and the geographic evidence separately from the region_id at the time of recording; recalculation against a new map must not silently rewrite the user's history.

Note, 2026-10-03 (D049): the set of regions changes only at a yearly release (R055); between releases only errors of ours are corrected. Correspondence tables and a de-minimis rule for geometry corrections are not decided (Q019).

### R033 — Build manifest [tentative]

A reproducible build fixes spec_version/hash, the profile, U/version/hash, world_time, knowledge cutoff, source snapshots/hashes, normalised facts, the identity registry if present, code revision, dependencies/engine, geometric parameters, test-set version/hash. An external URL without a saved version does not ensure repeatability. Deterministic serialisation and record order are mandatory. An experiment on a part of the world explicitly publishes its own test universe and does not claim global coverage.

### R034 — Provenance and uncertainty [tentative]

Each material fact contains value, source locator, excerpt or reference, source_scope, temporal fields and assessment. The following are distinguished: `model_unresolved`, `data_unknown`, `source_conflict`, `temporal_uncertainty`, `geometry_uncertainty`, `implementation_error`. A legal source, an observation of control and a carrier rule have different competences; being official does not by itself make a source suitable for any question. A conflict is not resolved by a majority of references. Claims and international-law assessment are likewise not mixed.

### R035 — Experiment contract and falsification [tentative]

The Stage 1 pairwise evaluator returns, for each check, comparison_id, profile, result, applied_rules, witnesses, completeness/equality signature, blocked_by_data, blocked_by_model, evidence_refs, explanation, spec_version and dataset_version. Its outcomes: `must_separate`, `hard_compatible`, `separation_not_proven`, `model_unresolved`, `data_unknown`, `rule_conflict`. `hard_compatible` is only a positive Stage 1 compatibility result, never a final-region merge instruction. `separation_not_proven` means only the absence of a sufficient split-certificate while hard compatibility is unproven; it is not a denial that a difference exists. `data_unknown` means that a specific unknown or conflict of evidence blocks the evaluation of a mandatory dimension. `rule_conflict` is reserved for incompatible normative conclusions, not for a simple divergence of sources.

An adversarial dataset may additionally use the structural outcomes `no_split_on_stated_factor`, `must_refine` and `overlay_only`; they are not pairwise `hard_compatible` answers. Neither `separation_not_proven` nor the latter structural outcomes are considered proof of hard compatibility.

A hypothesis is refuted if, with confirmed premises, its predictions or the accepted constraints are violated. An unexpected outcome is recorded before the rule is changed. A rule change is applied to the whole set and is accompanied by a review of the counterexamples, not by an exception by territory name.

### R036 — Semantics of the adversarial dataset [tentative]

The CSV contains deliberately difficult **candidates/test areas**, including nested aggregate/component cases; the rows are not ready-made regions and do not form a partition. `parent_or_claimant` is a descriptive link, not a parent region and not an exhaustive legal assessment.

`expected_result` is the machine outcome. `comparison_target` defines relative to what it is expected. `assertion` refines the check; `premises` separates out conditional facts. `expectation_basis` takes the values `user_constraint`, `rule_inference`, `conditional_rule`, `research_hypothesis`, `model_gap`, `intuition`. `confidence` assesses how well-founded this expectation is (high/medium/low), and `evidence_status` separately denotes the verification of facts. High confidence in model_unresolved is not high confidence in the separateness of a territory.

Checking a conditional row first confirms the premises. Unverified premises give `data_unknown`; this is not a failure of the rule. `no_split_on_stated_factor` is not equal to a proven merge. `must_separate` is not equal to "exactly one cell". A conclusion from intuition must have basis=intuition, low confidence and must not be a release gate. For disputed places a dated factual snapshot is required before a run, rather than an interpretation of the CSV as a current map of the front line.

### R037 — Minimal data structure [tentative]

The minimal types: RegionRevision; PoliticalEntity; LegalStatusRecord; Claim; ControlRecord; Policy/PolicyMembership; SpatialOverlay; BoundaryEvidence; SourceSnapshot; DecisionCertificate; SignatureAssessment; BuildManifest. Each temporal record refers to immutable evidence. RegionRevision contains region_id, revision, names, geometry_ref, validity, signature_ref, provenance and quality. Each signature dimension stores one of the states `known_value`, `known_absence`, `unknown`, `not_applicable`, `unresolved_model_semantics`; a value and evidence are mandatory where they are applicable. `known_absence` is a positively confirmed absence, not an empty field. `not_applicable` contains a rule-based justification. Lists of references may be empty only with an explicit `unknown`, `not_applicable` or `unresolved_model_semantics`. The country field does not replace independent relations. A full-fledged visa engine is not required for the first experiment: verifiable policies and witness cases are enough.

### R038 — Open-world pairwise evaluator [tentative; Q001, Q002]

The pairwise evaluator works in an open world: `no witness found != hard_compatible`, `unknown != false`, `not must_separate != hard_compatible`. The order in which terminal grounds are checked is deterministic: (1) detect a conflict of normative derivations; (2) accept a sufficient `must_separate` certificate; (3) return `model_unresolved` if an undefined model predicate can change the result; (4) return `data_unknown` if a specific data problem does not allow a mandatory dimension to be evaluated; (5) accept `hard_compatible` only on a complete equal signature; (6) otherwise return `separation_not_proven`.

Historical non-production profiles for Experiment Q001 (contract/spec `0.2.0-draft`, evaluator `0.2.0`; previous outcomes are not reinterpreted):

- `P1 regime_only`: hard admission-decision scope, visa/document scope, relevant hard permits and the route-dependent hard differences included in the profile. A verified hard witness gives `must_separate`; complete equal P1 signatures give `hard_compatible`; the absence of a witness by itself proves nothing.
- `P2 jurisdiction`: P1 plus final admission jurisdiction. Independently confirmed different final admission jurisdictions give `must_separate`, even if the current visa policy coincides. A merge requires equality of the P1 signature and of the jurisdiction dimensions.
- `P3 jurisdiction_plus_identity`: P2 plus an identity discriminator. Until `Q001.identity` is closed, P3 does not contain a hidden list of territories; if P1/P2 have not already given a sufficient `must_separate`, dependence on identity returns `model_unresolved`.

This minimal composition of the signature is needed to implement the evaluator, but does not close the questions about the full set of hard outputs, customs, permits, route dependence and identity.

The current normative production profile is **`S1-core-v1`**, separator set **`[CR-W]`**, spec `0.3.0-draft`, R044. It is not a renaming of historical P1. Production completeness requires positive full equality only of the accepted hard decision dimensions of R044 on one S/t/scope; CR-J, undefined identity and control/status labels are not required. A certificate that was not found is not equal to `hard_compatible`. An unresolved relevant accepted dimension/gate keeps the model/data blocker; excluded identity does not by itself block production. Neither historical results nor sampled policies are considered a new production audit.

Note, 2026-10-03 (D051): releases are built under the product profile `S1-product-v1` (R057), which treats the absence of a recorded witness inside a registry cell as no boundary and marks the result as assumed. That is a declared closed-world default for building releases, not `hard_compatible`; `S1-core-v1` remains the definition of a proved boundary.

## Two-stage architecture

### R039 — Stage 1 Mandatory Separation [accepted; amended by D038, D050, D051]

Stage 1 establishes boundaries that the final partition may not cross. Its current production core is only CR-W under R044 and all five proof gates. Amendment, 2026-10-03: Stage 1 also refines the reference registry (R045) and applies the rules for disputed and special-status areas (R049–R054); CR-W is read with the amendments of R056; releases are built under `S1-product-v1` (R057). The pairwise `S1-core-v1` evaluator remains CR-W only. Final admission competence CR-J is a well-defined normative candidate, not adopted. Undefined territorial/legal identity, claims, recognition, dispute, control actors, military control, dependency, autonomy, overseas and island labels are not independent hard separators. Tourism/cultural/destination identity, administrative subdivision, remoteness, transport inconvenience and itinerary usefulness do not enter this evaluator. Accepted product constraints remain regressions even where the current core cannot derive them.

### R040 — Stage 2 Destination Partition [accepted; Q012]

Stage 2 receives each Stage 1 cell independently and may subdivide it using destination semantics such as geographic coherence, destination identity, itinerary coherence, travel graph or gateway structure, cultural-regional coherence, and stable traveller-facing destination concepts. These are first-class inputs to the final partition. This version does not define their algorithm, weights, thresholds, or completeness test.

### R041 — Monotonic refinement [accepted]

Let `Stage1Partition` and `Stage2Partition` be partitions of the same universe U. The required invariant is:

```text
Stage2Partition refines Stage1Partition
```

Equivalently, every Stage 2 cell is a subset of exactly one Stage 1 cell. If Stage 1 requires A and B to be separate, no later construction step may merge them. Stage 2 can only split Stage 1 cells.

### R042 — Territorial/legal identity and destination identity [accepted; Q001, Q006, Q012]

Territorial/legal identity concerns institutional status: separate legal or status entities, disputed international status, dependencies, constitutional territorial identity, and similar questions. Undefined territorial/legal identity alone is not accepted and is excluded from production and production-candidate hard semantics (D034). A future explicitly defined legal-status rule would require a separate decision; Q001 is narrowed and Q006 remains open. Destination identity concerns a coherent independent travel destination, traveller perception, itinerary structure, geography, and destination self-containment. It belongs to Stage 2. Neither concept implies the other, and historical non-production P3 does not model destination identity.

### R043 — Project boundary [accepted]

This repository covers Stage 1 Mandatory Separation, Stage 2 Destination Partition, and their final single-level Canonical Travel Regions partition. Any finer subdivision beyond that canonical destination partition is outside this project's ontology and must not influence Stage 1 or Stage 2 rules.

### R044 — CR-W: proven hard territorial TravelDecision discontinuity [accepted; D032]

Current production profile: `S1-core-v1`. **A verified CR-W certificate is sufficient for `must_separate`.**

```text
exists C in S_v, d in H_v:
    G-SCOPE AND G-CONTEXT AND G-HARD AND G-TIME AND G-EVIDENCE
    AND proven(HardTravelDecision_d(A,C,t) != HardTravelDecision_d(B,C,t))
```

| Gate | Accepted sufficient requirements |
|---|---|
| G-SCOPE | Nonempty non-overlapping certified A/B or disjoint fragments; a proven identical relevant effect inside each scope. Not a blanket conclusion about heterogeneous/overlapping containing objects. Geometry uncertainty is preserved. |
| G-CONTEXT | One versioned traveller scope `civilian-short-stay-v1` and one t; a coherent nonempty civilian short-stay class, a matched logical trip, all influencing attributes and exceptions are fixed. Rare documents and class-based special permissions are included; work/settlement/diplomatic/military primary purposes are excluded. No frequency threshold or named-person selection. |
| G-HARD | The difference in an accepted hard dimension has a territorial legal entry/presence/stay/exit effect. Site/activity/facility/route logistics and a processing event are not sufficient by themselves. Whole administrative coverage does not prove hard classification; permit/overlay ambiguity remains Q005/Q009. An independently applicable legal obligation is not derived from a claim alone. |
| G-TIME | A class-based standing/constitutive rule is in effect at t and is not exclusively an incident/emergency/event measure. Effective date, observation and retrieval are separate; there is no age threshold and no requirement to know the future. If the type of the measure is not determined — Q008. |
| G-EVIDENCE | Both sides of D are proven, relevant exceptions are taken into account. Each premise contains verified source/locator, source competence, territorial/context scope and validity at t. Missing, provisional, conflicted and unknown evidence are insufficient. A verified statement is not upgraded to a stronger legal conclusion. |

Hard dimensions `H_v` (complete functions on one `S_v`, not samples): `accepted_travel_document`; `visa_eta_admission_authorisation_requirement`; `territorial_authorisation_validity`; `entry_eligibility_or_prohibition`; `civilian_stay_conditions_duration_or_termination`; `permission_to_enter_or_be_present_in_territorial_scope`; `independently_applicable_legal_entry_or_exit_route_obligation`. Goods/customs/biosecurity dimensions are not added by this list (Q004). The names of the authority and of output documents are not semantic values by themselves. Decisions describe legal requirements/admissibility, not random officer outcomes.

One witness that has passed the gates is sufficient regardless of the number of members of the class. **Absence of a CR-W certificate is not `hard_compatible`.** Compatibility requires positive complete coverage/equality evidence across all H_v for both scopes on one S/t, including exceptions, and the absence of an applicable certificate. Unknown is neither equality nor split. CR-J and identity completeness are not required. An excluded label is not a blocker by itself; a consequential unresolved hard predicate remains a blocker. If a full equality audit contradicts a verified certificate, the input requires conflict resolution, not an automatic merge.

This is the accepted sufficient core, not the completion of all Stage 1 semantics. Q002/Q004/Q005/Q006/Q007/Q008/Q009/Q011 remain open in the residual part. D004–D007 are retained as accepted product regressions with no guarantee of deriving them from CR-W, with no special-case rules and with no promise to resolve them through Stage 2.

Note, 2026-10-03 (amended by D050): R056 narrows what a producer of gate proofs may attest under G-CONTEXT (transit, organised-group-only and local-border-traffic classes are not witnesses; tour-operator-only access is), G-HARD (fees and purchases on arrival are not hard; whole-unit presence permits are) and G-SCOPE (the scope test for units of one country, and the witness for held areas). The five gates, the hard dimensions `H_v` and the evaluator's input contract are unchanged: gate records remain producer attestations, so the evaluator, its `SPEC_VERSION` and its tests are not changed. With D038 (R045) the registry, not CR-W, is what derives D004–D007; they stay accepted constraints until a release check confirms them (D036). Of the residual questions listed above, Q006 is closed and Q002, Q004, Q005, Q007, Q008, Q009 and Q011 are narrowed (see [open-questions.md](open-questions.md)).

## Registry, disputed areas and releases

Items R045–R057 record the owner's decisions of 2026-10-03 (D038–D053). They use the [register of disputed and special-status areas](../data/disputed-areas/README.md) as their factual input: its `kind`, `inhabited`, `holder`, `holder_since`, `contest_ended_by` and `stated_outline` fields, each a sourced fact. Rules read those fields; names of places appear only as examples.

### R045 — Reference registry [accepted; D038, D039]

The **declared perspectives** are ISO 3166-1 and the national points of view of Natural Earth, each at a pinned edition stated in the build manifest (R033). Each declared perspective P assigns land to countries; land that P assigns to no country is P's remainder. The canon's own attribution under R049 is treated as one more perspective for this rule.

```text
for every declared perspective P and every Stage 1 cell s:
    s lies within exactly one country of P, or within P's remainder
```

Because Stage 2 refines Stage 1 (R041), no final region crosses a country boundary under any declared perspective. The registry adds boundaries only; CR-W and R049–R054 may separate further inside its classes. It is a declared product rule with an external source, not an identity predicate (R010) and not a CR-W certificate.

Decided qualifications:

1. An area with its own ISO 3166-1 entry is always a region.
2. An area that R050–R054 make a special place creates no boundary, even where a declared perspective places it in another country: its land stays in the region of its holder (D045, D052). How the consumer learns that perspective's attribution is part of Q018.
3. Antarctic claims create no boundary (R026).

**Editions.** The canon is pinned to stated editions of ISO 3166-1 and Natural Earth. It moves to a new edition only by the owner's decision at a release, after a report of what the new edition would change (R055). Which Natural Earth attributions count as declared perspectives in detail, and how errors in its attributes are handled, is Q014.

Amended by D064: the supported points of view also include, for every party to a dispute in the register that has no Natural Earth view, that party's own view built from its sourced claim.

Amended by D065: every country's point of view is built from its sourced claims (a law, its constitution, an official map or a government statement). Natural Earth's national points of view are a lead: each difference between them is checked against the country's claims, and a difference that no sourced claim supports cuts no boundary. What counts as a sourced claim and how unchecked differences are treated is Q020.

Amended by D067: a claim may rest on a reliable secondary source that reports it, with the quoted passage; its evidence level is recorded and shown with the region it creates, and the claimant's own document replaces the secondary source when found.

### R046 — Special places and markers [accepted; D041]

A **special place** is an object with its own location or outline that is not a region. It is tickable, it is shown with the region that holds its land (its parent region), it is not counted as a region, and it does not change the partition. A **marker** is a recorded note on a region or a boundary — an overlay in the sense of R017 — and is neither a region nor a special place.

Which places become special places or markers is stated by R049–R056: border-line disputes, undelimited stretches, uninhabited islets and claimed rocks, uninhabited zones with no single holder and small leases are special places; entry rules that fail R056 are markers. How the consumer carries special places is Q018.

### R047 — Outlines come from lines the parties state [accepted; D042]

The outline of a cell created for an area of the register, or for an area held by a party other than the one the surrounding region is attributed to, is never drawn by this project. It is a line the parties themselves state: a claim line, a ceasefire or armistice line, a treaty or lease line, or a coastline. A front line is never an outline. Where no such line exists, there is no cell: the place is a special place (R046), or, for an area whose control changed by force, the flag of R049 applies.

The registry and the register say which places are separate and whose they are; they are not the only source of outlines. The substrate is extensible: where it has no unit that fits the stated line, a custom geometry is added from a cited source of that line. Outlines may be taken from Natural Earth, GADM or OpenStreetMap, or digitised from a cited document; the licences of these datasets apply as they do to Track Your Regions, of which the canon is part (amended by D056). Where the substrate cannot represent a place as the canon needs, the canon's geometry is Natural Earth's polygon, else OpenStreetMap or a Commons map, else an outline digitised from a cited document; a more detailed source replaces Natural Earth place by place after review, at a release (amended by D059). Sources are ranked by whose line they draw: a party's own published line, then an agreed line drawn by a neutral publisher, then OpenStreetMap, then Natural Earth; every own geometry is clipped to the substrate units of the regions it takes land from (amended by D062). How geometries are pinned and versioned is Q013.

Amended by D066: where the holder of land is known (R048) but no party publishes the line up to which it holds, the land is divided between the holders by the best available line of actual control, in the source order above, with the source recorded; the line has held since a ceasefire (a moving front does not qualify, R049) and only decides which region the land goes to. The project draws no polygon for the purpose.

### R048 — The holder of an area [accepted; D043]

`holder(area, t)` is the party whose officers can in practice admit a civilian to the area, refuse one and remove one at t. Rules a party issues for an area but cannot enforce there do not count. Where parts of an area are held by different parties, each part has its own holder. Holding in fact is enough, for inhabited and uninhabited areas alike; there is no separate condition about civil administration. The holder and the date from which it has held the area without interruption are register facts with a source and a quoted passage; attribution is computed from them. Where this test cannot tell the parties apart, the holder is the party that provides civil administration to the residents; if there is none, the area has no holder (amended by D055).

### R049 — Unsettled areas and the settling time [accepted; D043, D053]

**When it applies.** All three must hold; otherwise the canon's attribution does not change.

1. *Force*: a party takes control of the area without the consent of the party the canon attributes it to.
2. *Claim*: the new holder asserts the area as its own or as a separate entity.
3. *Stated outline*: any boundary involved is a line the parties state (R047).

**States.** A *settled* area is attributed to its holder. An *unsettled* area is attributed to its last settled holder, and a release says that it is unsettled, since when, who holds it, and, while quiet, how many of the required quiet years have passed. *Active conflict* is a flag of its own, shown in any state while the conflict over the area has a conflict-year in the UCDP/PRIO Armed Conflict Dataset (25 or more battle-related deaths). The tie from an area to its conflicts is a maintained input of the register.

**Clock.** T = 3. Each full calendar year after the year of the seizure adds one if it has no active conflict over the area, and resets the clock to zero if it has.

**Paths.**

| Path | Condition | Effect |
|---|---|---|
| Acceptance by time | T quiet calendar years in a row under the same holder | Attribution moves to the holder; the other side stays a claimant |
| Acceptance by an act | The side that lost the area stops contesting by an explicit act: an agreement, an accepted ruling, a renunciation of the claim, or that party ceasing to exist; a dated, sourced fact. Nothing weaker counts | Attribution moves at the next release, without waiting |
| Return | Control goes back to the party the canon attributes the area to | None |
| Fighting without change of control | Active conflict, same holder | Flag only |

There is no original or rightful holder: a party that retakes an area the canon attributes to someone else is a new holder like any other.

**While the line moves.** When control changes over part of a region and the held part has no outline the parties state, no area is delimited and no region is created, even if entry to that part follows other rules. The regions it touches keep their attribution and carry a flag that part of them is unsettled, held by whom and since when, with active conflict while it applies. Once the parties state a line, the held part becomes an unsettled area and the clock applies.

**The status creates no regions.** An unsettled area becomes a region of its own only through the registry (R045) or CR-W (R044, R056, including the witness for held areas), and at acceptance at the latest, because its attribution then differs from the rest of its former region; a strip between two neighbours then moves into the neighbour's region instead. Until then it stays inside the region of the party it is attributed to, marked.

**First release.** The attribution of each contested area is found by applying this rule to its record: the holder whose control the other side last stopped contesting. Only the last settled holder is needed.

### R050 — Disputes about where a border line runs [accepted; D044]

An area whose register `kind` is `line_position` is not a cell. Its land belongs to the region of its holder (R048), and the dispute is a special place (R046). Where its holders' line of control is not published, D066 (R047) says how the land is divided.

Amended by D063: such an area is a region of its own when a supported point of view (R045) puts it in another country and civilians live there, attributed to its holder; otherwise the rule above applies.

### R051 — Islets and paper claims: the residents test [accepted; D045]

*Resident civilians* means the register's `inhabited` = `yes`; `garrison_only` and `no` do not count.

1. An area of kind `islets_for_maritime_zone` with resident civilians is a region, outlined by its coastlines. Otherwise it is a special place, and its land goes with its holder.
2. An area of kind `paper_claim` is a region if a declared perspective (R045) places it in a country other than its holder's and it has resident civilians. If a declared perspective shows the claim and the area has no resident civilians, it is a special place and its land goes with its holder. A claim that no declared perspective shows gives only a marker.
3. An area with its own ISO 3166-1 entry is a region regardless of this test.

An islet group held in parts by several parties with no line between the parts is Q016. When the last residents leave, R055 applies.

### R052 — Zones with no single holder [accepted; D046]

An area of kind `own_regime` (a buffer, separation or demilitarised zone, a condominium) is a region attributed to no country in the canon's attribution if civilians live there and the parties state its outline (R047). Otherwise it is a special place. The zone is never split between the neighbouring parties. Which region takes the land of such a special place is Q016.

### R053 — Leased areas and bases [accepted; D047]

An area of kind `lease_or_base` is attributed to the lessor's country, since the parties agree whose land it is; the lessee is recorded on it. It is a region when its holder (R048) is a state other than the lessor and civilians live there; otherwise it stays in the lessor's region as a special place (amended by D057, which replaced the test "entry follows rules of its own", and D058, which added the residents test).

### R054 — Recently resolved disputes [accepted; D048]

An area of kind `resolved_recently` needs no rule of its own: the agreed outcome is taken over at the next release, and the place may stay as a special place. When it does is part of Q018.

### R055 — Releases and changes nobody contests [accepted; D039, D049]

1. **Two layers.** Facts at a date t, and CR-W evaluated on them, stay as in R031 and R044 (G-TIME is unchanged). A **release** is the canon for the situation at the end of a calendar year. There is one release a year. Between releases the set of regions does not change; only errors of ours are corrected.
2. **Entry.** A part of a country becomes a region because of its own entry rule only when the rule is in force at two consecutive yearly releases. A stated expiry date or a "pilot" label is ignored.
3. **Exit.** When such a rule is suspended or ends, the region stays, marked as having no special rule at present, and is merged back if the rule has not returned after three years. The same holds for any boundary that lost its basis, including an islet group or a claimed area whose last residents left (R051, R052).
4. **Editions** of ISO 3166-1 and Natural Earth change only as R045 says.
5. Contested control follows R049, not this item.

How the three years are counted against releases, correspondence tables between releases and a de-minimis rule for geometry corrections are Q019.

### R056 — CR-W amendments: witnesses and scopes [accepted; D050]

These amend how R044's gates are read. One valid class suffices regardless of frequency (D032), as before.

1. **Transit is not a witness** (G-CONTEXT). Only trips to each place as a destination are compared. A class whose trip is defined by onward travel to a third territory is not a witness; the territorial limits of a transit regime are an overlay (R017, R027).
2. **Organised-group rules are not witnesses** (G-CONTEXT). A rule that applies only to organised groups does not separate; only a rule for an independent visitor does. Group schemes are markers.
3. **Local border traffic is not a witness** (G-CONTEXT). A rule only for residents of a neighbouring area across the border is a marker.
4. **Tour-operator-only access is a witness** (G-CONTEXT, G-HARD). A rule under which a place can be reached only through a tour operator closes it to an independent visitor, unlike a concession for groups.
5. **Payments do not separate** (G-HARD). A mandatory fee or purchase on arrival is not a hard difference; only rules on who may enter and for how long do (a visa, a permit, a separate control, a stay limit). Fees are markers.
6. **Scope test for units of one country** (G-SCOPE). A place with its own entry rule is a region only if it is (a) a whole top-level unit of its country, or (b) a smaller but detached unit — an island or an exclave — with a rule written for it, not a line in a list. Everything else is a marker inside its region: border bands and districts, lists of islands or ports, closed towns, single valleys. One rule over several top-level units, and the operational definition of the units, are Q015.
7. **Whole-unit presence permits** (G-HARD). A standing rule that makes presence in a whole unit conditional on a permit for an ordinary visitor is a hard difference in `permission_to_enter_or_be_present_in_territorial_scope` and separates that unit, for the units that pass item 6. A permit for part of a unit stays a marker (R014).
8. **Held areas** (G-SCOPE). For an area held (R048) by a party other than the one that claims it as its ordinary territory, the holder's own entry rule for the area, with an outline the parties state (R047), is the witness; item 6 is not applied.

### R057 — Product profile `S1-product-v1` and evidence levels [accepted; D051]

Releases are built under `S1-product-v1`:

1. **No witness, no boundary.** Inside a registry cell there is a Stage 1 boundary only where a rule with a source is recorded (R044 with R056, or R049–R054). The rest is marked as assumed, not proved; it is not `hard_compatible`.
2. **Evidence levels.** `cited`: a source states the rule, with locator, publisher, quoted passage and dates, and the gates are checked by the preparer, who may be an AI agent; enough for a release. `audited`: review by a named person, required where sources conflict, where no primary source can be found, or on the owner's request. Evidence below `cited` does not create a boundary in a release.
3. **Labelling.** Every boundary in a release states its rule and its evidence level. Nothing built under this profile is presented as certified under `S1-core-v1`, which stays the definition of a proved boundary.

## Checks that the first build must implement

| Check ID | Rules | Property checked |
|---|---|---|
| V001 | R002–R004 | union(regions) == U; no overlap of positive area; empty regions are forbidden |
| V002 | R005 | No current canonical parent/child and no duplicate aggregate cells |
| V003 | R028–R030 | Shared edges, vertices, holes, the antimeridian and the poles have a deterministic lookup |
| V004 | R007–R009, R038 | Every hard split has a certificate; `hard_compatible` has a complete equal signature; permuting the inputs does not change the result |
| V005 | R016–R017 | Renaming, new claims, a change of advisory and the opening of a flight do not by themselves change the partition |
| V006 | R011–R012, R044 | Production: different jurisdiction alone is not a split and not dimension completeness; CR-W is checked separately. Historical P2/P3 retain the R011 regression; a delegated issuer does not create a production split |
| V007 | R022–R026 | Legal status and control are independent; overlapping Antarctic claims do not give overlapping regions |
| V008 | R031–R033 | One manifest reproduces an identical result; a historical correction is available separately; no overlap of intervals within one revision stream |
| V009 | R034–R038 | unknown does not turn into false; the absence of a witness does not become `hard_compatible`; unresolved is not counted as the definition of a region |
| V010 | R008–R010, R038 | The same facts under substituted country names give an isomorphic result; the manual registry is shown separately |
| V011 | R045, R050–R054 | For each declared perspective and the canon's attribution, every region lies within at most one country; each exception is the land of a special place under R050–R054, listed with its rule |

These checks are specified here, but the geometry pipeline is not yet implemented. In this release the structure of the CSV and the links between documents have been checked.

## Verified external reference sources

This is a spot check of the basic distinctions, not a re-verification of all the examples in the research. Date accessed: 2026-09-11.

- E01: [France-Visas — France in the Schengen area](https://www.france-visas.gouv.fr/en/la-france-dans-l-espace-schengen). Confirms the exclusion of the non-European French territories from Schengen; the separateness of Réunion from the metropole is consistent with R012. It does not follow from this that all overseas parts are mutually separate.
- E02: [European Commission — Territorial Scope](https://taxation-customs.ec.europa.eu/taxation/vat/vat-directive/how-does-vat-work/territorial-scope_en). EU/customs/VAT/excise are different scopes. Réunion is part of the EU customs territory, but not of the common VAT/excise territory. In the original paraphrases this must not be shortened to "Réunion is outside the EU customs territory".
- E03: [UN — Western Sahara](https://www.un.org/dppa/decolonization/en/nsgt/western-sahara). Confirms UN Non-Self-Governing Territory status, but does not define the current operational geometry and does not prove a two-part division.
- E04: [Antarctic Treaty Secretariat — Antarctic Treaty](https://www.ats.aq/e/antarctictreaty.html) and the [text of the treaty](https://documents.ats.aq/keydocs/vol_1/vol1_2_at_antarctic_treaty_e.pdf). Article IV preserves positions on claims; Article VI describes the area south of 60°S. The choice of one land cell is our modelling hypothesis, not a requirement of the treaty; on 2026-10-03 the owner adopted it for Stage 1 as an explicit convention (D040).

### R058 — Unclaimed land and boundaries that are not agreed [accepted; D054]

An area that no state claims is a region attributed to no country; its outline is the part that the neighbours' own claim lines leave out (R047). An area where a boundary must exist between states that each hold territory on their side, but no line is agreed or defined for that stretch, is not a region: its land goes with its holder (R048) and the area is a special place (R046).

### R059 — Release package [accepted; D060]

A release consists of: TYR's world-view import tree (`canon.json`: country, then region, with names and Wikidata ids); `regions.csv` (one row per region: identifier, name, Wikidata id, basis, country under each declared perspective); `membership.csv` (one row per region and substrate unit: region, substrate and version, unit identifier); `geometry/` (the canon's own geometries, R047, with source and licence); and `manifest.json` (release identifier, cutoff date, rule and registry versions, input hashes, correspondence to the previous release). Files are sorted and deterministic.
