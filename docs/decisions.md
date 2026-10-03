# Canonical Travel Regions — decision log

Version: 0.4.0-draft. Date: 2026-10-03. Related documents: [spec.md](spec.md), [open-questions.md](open-questions.md).

The current normative decisions on Stage 1 are D032–D037, extended by the owner's decisions of 2026-10-03, D038–D053: a reference registry of countries, Antarctica, special places, outlines, the settling rule for contested control, the treatment of each kind of disputed area, yearly releases, amendments to CR-W and the product profile. Earlier research/experimental entries preserve the history but do not override them. D004–D007 remain accepted product constraints.

## How to read the log

`accepted` is used only for an explicit requirement of the user. `tentative` means a research proposal or a new formalisation, accepted only as a hypothesis of this specification. `unresolved` means a contradiction or an insufficiently defined model decision. A request to fix the formatting of a research report does not count as agreement with all of its conclusions. A research report is not a record of user approval.

## Sources of the original decisions

| Source ID | Material | What is actually available |
|---|---|---|
| S01 | User, "Rules for partitioning territories", 2026-09-10 | The visible original message: a single-tier, non-overlapping, complete partition, conditional independence, take entry into account; UK overseas separately; do not merge Réunion with France, Crimea with Ukraine, Western Sahara with Morocco in the travel sense |
| S02 | "A global single-level partition of the world into travel-territories", 2026-09-10 | The report was read in full, 985 lines; Library ID libfile_d734666989b48191ae91201e44ad6d07. Sections "Delineation criteria", "Disputed, overseas and integration cases", temporal/provenance |
| S03 | "A global single-tier partition of the world into travel territories", 2026-09-11 | The report was read in full, 2203 lines; Library ID libfile_d2bdf9e1b63c8191b5014d5ea8f0be2b. Adds a separate territorial identity criterion and a safe merge algorithm |
| S04 | "The difference between Codex and Work", 2026-09-11 | Visible are the user's messages about Linux, continuing the research, experiments and the created Project; a search found a fragment of the assistant's answer of 19:16:20 UTC about Project/Work → specification/data → git/Codex. There is no full transcript |
| S05 | The current user assignment, 2026-09-11 | A direct requirement for four files, stable rule IDs, falsifiability, 50–100 adversarial cases and a ban on fitting to a desired list |
| N01 | The present formalisation | New engineering proposals of this release. They are not attributed to previous conversations |

The Library IDs are given for exact lookup of the original reports. The external primary sources E01–E04 and the limits of their verification are given in spec.md. S02/S03 record the history of proposals; their geographic statements do not automatically become current verified facts.

## Decisions confirmed by the user

### D001 — Complete single-level partition

- Decision: the geographic area of coverage must be partitioned completely and without overlaps into a single level of territories.
- Rationale: one and the same visited point must not belong to several counted territories at the same time.
- Rules: R001–R005.
- Counterarguments: a hierarchy is convenient for navigation and aggregation, but it can be stored outside the canonical partition.
- Status: accepted.
- Basis: S01, S05. The composition of the universe itself remains Q003, not accepted.

### D002 — Travel perspective and entry regime

- Decision: assess conditional separateness from the traveller's point of view; at a minimum, take the entry regime into account.
- Rationale: state affiliation does not fully describe the conditions of a visit.
- Rules: R006, R007, R011, R012.
- Counterarguments: "affects travel" without a limit on scale leads all the way to car parks, guarded zones and individual sites.
- Status: accepted as regards the goal and the inclusion of entry; the specific thresholds/sufficiency of individual factors are tentative.
- Basis: S01. The words "at a minimum" do not mean agreement to any customs/permit split.

### D003 — Reproducibility and checking for contradictions

- Decision: move from research to reproducible experiments; do not compile a final world map now and do not fit the rules to a list.
- Rationale: general criteria must be open to refutation.
- Rules: R001, R008, R033–R036.
- Counterarguments: concrete examples are needed as product constraints; they should be kept, rather than treating every expected outcome as forbidden.
- Status: accepted.
- Basis: S04, S05. The detailed structure of the manifest is N01, tentative.

### D004 — Count British overseas territories separately

- Decision: do not treat British Overseas Territories as an ordinary part of the UK in the travel partition.
- Rationale: an explicit example of the desired conditional territorial separateness.
- Rules: R010, R018, R026.
- Counterarguments: "each one separately" does not define a split inside a composite territory; Antarctic claims cannot be turned into overlapping canonical cells. The user did not separately approve Crown Dependencies here.
- Status: accepted as an original requirement; universal application and the Antarctic exception are unresolved, see D016, Q001.
- Basis: S01. S03 extends this to a general identity model, but the extension is not confirmed by the user.
- Note, 2026-10-03: territories with their own ISO 3166-1 entry are separated through the reference registry (D038, R045). The Antarctic exception is now an explicit convention (D040): the British Antarctic Territory stays inside the single Antarctic Stage 1 cell.

### D005 — Réunion is separated from metropolitan France

- Decision: Réunion does not belong to one ordinary travel region together with the European territory of France.
- Rationale: S01 gives an explicit example; S02/S03 link it to the territorial entry scope. E01 confirms the difference in Schengen applicability.
- Rules: R012, R019.
- Counterarguments: some travellers enjoy common rights; this does not remove the differences for the others. Separateness from the metropole does not prove that Réunion cannot be merged with some other overseas component.
- Status: accepted for the relationship to the metropole. "Exactly one separate region Réunion" is not approved.
- Basis: S01; S02/S03, the corresponding sections; E01/E02. Réunion is within the EU customs territory, so a customs exception cannot be used as a false basis.

### D006 — Crimea is not an ordinary travel territory of Ukraine

- Decision: do not include Crimea in one ordinary travel region together with the rest of Ukraine.
- Rationale: S01 sets a distinction from the point of view of a visit. This is not a denial of Ukraine's legal sovereignty.
- Rules: R015, R022, R024.
- Counterarguments: the separateness of the travel region from Ukraine does not say whether the territory must be merged with ordinary Russia or where exactly to draw the boundary; control and rules change over time.
- Status: accepted only for the original distinction. The remaining conclusions of D013 are tentative.
- Basis: S01; S02/S03 contain a stronger recommendation than the user's message itself.

### D007 — Western Sahara is not ordinary Morocco

- Decision: Western Sahara must not disappear into the ordinary travel territory of Morocco.
- Rationale: an explicit example from the user; the travel separateness of the disputed area must be preserved.
- Rules: R022, R024; a possible, as yet unresolved basis in R010.
- Counterarguments: a common admission/control regime on one side of the disputed boundary may give no witness for a split from Morocco. UN status by itself is insufficient under R016. This is a real tension between the requirement and the regime model.
- Status: accepted as a product constraint; the general mechanism is unresolved (Q006).
- Basis: S01. The requirement of two cells along the Berm is a separate D014, not accepted by the user.

## Research proposals not confirmed as final decisions

### D008 — Separate identity, legal status, control and traveller reality

- Decision: store independent layers and do not reduce them to country.
- Rationale: one physical trip may be permissible in fact and impermissible under the law of another relevant jurisdiction.
- Rules: R017, R022–R024, R034, R037.
- Counterarguments: the schema and the display are more complex; a legal assessment and an asserted claim must be distinguished, so as not to equate them automatically.
- Status: tentative, a strong concordant proposal of S02/S03.
- Basis: S02 "Formal model", S03 "Sovereignty, claims and recognition".

### D009 — Common visa areas are overlays

- Decision: EU/Schengen/CTA do not become parent canonical territories; common policies are reused.
- Rationale: overlapping scopes cannot be fitted into a single tree.
- Rules: R005, R011, R012, R017.
- Counterarguments: the prohibition on merging by a common visa does not by itself prove which territories to keep separate. An admission jurisdiction or a defined identity is needed.
- Status: tentative, directly supported by accepted R005.
- Basis: S02/S03, the examples of France/Germany and the Crown Dependencies.

### D010 — Additional criterion of territorial identity

- Decision: S03 proposes separating external territorial jurisdictions even when travel regimes are identical.
- Rationale: to satisfy the UKOT constraint and avoid turning the list of visits into a pure map of visas.
- Rules: R010, R018–R021.
- Counterarguments: "separate" is defined through the desired result; the difference between Åland and Sicily, between a remote island and an overseas jurisdiction, is unclear. A registry cannot be justified by the registry itself.
- Status: unresolved.
- Basis: S03 "A separate territorial identity criterion". S02 relies on this factor less strongly; this is a substantive change, not only formatting.

### D011 — Customs/biosecurity as a conditional hard split

- Decision: S02/S03 propose a split where the traveller has substantial obligations.
- Rationale: an identical visa may hide mandatory declarations and import restrictions.
- Rules: R013, R016, R017.
- Counterarguments: the same criterion may fragment Tasmania, Hawaii, California and a multitude of internal quarantine zones; the notion of substantiality is not defined.
- Status: unresolved for the general criterion.
- Basis: the criteria tables of S02/S03. A deficiency of the model cannot be closed by one additional customs document.
- Note, 2026-10-03: a mandatory fee or purchase on arrival does not separate (D050, R056); customs and biosecurity formalities as such remain Q004.

### D012 — MultiPolygon and no automatic island split

- Decision: geographic disconnectedness by itself does not create a region.
- Rationale: physical shape is not obliged to change the admission jurisdiction.
- Rules: R009, R021.
- Counterarguments: an island can be a separate unit of travel without formalities; this is a question of identity, not of poor transport data.
- Status: tentative.
- Basis: S02 "Enclaves, exclaves", S03 safe merge.

### D013 — Crimea separate from ordinary Russia as well

- Decision: S02/S03 recommend a separate disputed cell Crimea/Sevastopol, merged neither with ordinary Ukraine nor with ordinary Russia.
- Rationale: the legal routes, the applicable legal restrictions and the conflicting status/control profile differ.
- Rules: R008, R012, R022, R024.
- Counterarguments: separate control explains the boundary with Ukraine, but not automatically the one with Russia. A territorial legal-route witness or a general identity criterion is needed. Whether Crimea/Sevastopol is one cell or two is also not decided.
- Status: tentative.
- Basis: S02 "Crimea", S03 "Crimea"; do not extend the accepted status of D006.
- Note, 2026-10-03: under the reference registry (D038) an area that a declared perspective attributes differently from the others is a cell of its own, which in the first world draft gives Crimea a cell separate from both Ukraine and Russia; its attribution follows the settling rule (D043). This entry itself is not promoted.

### D014 — Splitting Western Sahara by operational control

- Decision: S02/S03 propose at least two areas on the two sides of the Berm, linked by a common dispute_id.
- Rationale: different actual conditions of control and access.
- Rules: R015, R022, R024, R028, R030.
- Counterarguments: a map of the Berm is not identical to an exact current map of control; buffer/restricted strips and changes of control may require a different refinement. Two areas do not prove the separation of the western part from Morocco.
- Status: tentative. Exactly two final cells are not approved.
- Basis: the corresponding sections of S02/S03. E03 confirms only the legal-status layer.
- Note, 2026-10-03: the reference registry (D038) separates the parts that declared perspectives attribute differently; outlines come only from lines the parties state (D042).

### D015 — Check St Helena / Ascension / Tristan da Cunha separately

- Decision: one constitutional unit may not be atomic for the travel model.
- Rationale: the research reports point to different territorial admission/permit systems of the components.
- Rules: R011, R012, R018.
- Counterarguments: three names do not prove three final regions; the competences and scope of each component must be compared, including the permits of uninhabited islands.
- Status: tentative.
- Basis: S02/S03, the UKOT sections. S02 explicitly states the need to check Tristan da Cunha.

### D016 — Antarctica initially as a treaty-space cell

- Decision: one provisional cell for the chosen Antarctic universe; claims separately, stations as access objects.
- Rationale: overlapping claims cannot be turned into mutually exclusive regions without an additional rule.
- Rules: R002–R005, R014, R026.
- Counterarguments: one treaty regime does not prove one destination identity; territorial protected areas have permits. The land universe does not coincide with the Treaty Area. An explicit limitation of D004 is required for the British Antarctic Territory.
- Status: tentative; reconciliation with the literal "each UKOT separately" is unresolved. Superseded by D040 (2026-10-03).
- Basis: S02/S03 "Antarctica"; E04. It is not an exception accepted by the user.

### D017 — Closed territories are not excluded from coverage

- Decision: store visitability separately, including uninhabited/closed.
- Rationale: the opening of a territory must not create Earth that was previously absent.
- Rules: R002, R003, R025.
- Counterarguments: the original "space that can be visited" admits a narrower reading of the universe.
- Status: tentative; Q003.
- Basis: S02 restricted destinations; S03 "Closed and occupied areas".

### D018 — Temporal facts, provenance and bitemporality

- Decision: separate the time of validity from the time of knowledge, and preserve source_scope and history.
- Rationale: to reproduce old answers and correct history without losing the audit trail.
- Rules: R031–R034.
- Counterarguments: expensive for a first experiment; the full operational SLA from the research is not needed while there is no production engine.
- Status: tentative.
- Basis: S02 temporal rules; S03 "Provenance at the level of the fact". Daily updating is not considered an obligation of the project.

### D019 — Work/research and git/experiments

- Decision: the architectural answer proposed moving from Project/Work/Deep Research to a specification and data, then to a git repository and reproducible experiments with Codex.
- Rationale: discussion of the rules and repeatable computations need different working artifacts.
- Rules: R001, R033, R037.
- Counterarguments: this is an organisation of the work, not a choice of a specific GIS stack. The analysis can be carried out with different tools.
- Status: tentative for the tooling; the wish for experiments is accepted D003.
- Basis: S04, the found fragment of the assistant; not a full transcript. A repository, Python/Go, PostGIS and specific datasets were not approved in the available material.

## New formalisations of this release

### D020 — Coarsest partition instead of an undefined "minimal atom"

- Decision: build the common refinement of the boundaries and merge by the full hard signature; show all unresolved predicates explicitly.
- Rationale: homogeneity by itself admits infinite fragmentation; a merge criterion and a check of independence from order are needed.
- Rules: R006–R010, R035.
- Counterarguments: the equality of all policies cannot be proven by sampling; the identity discriminator is not yet defined.
- Status: tentative.
- Basis: N01, develops the safe merge of S03. This is not a ready algorithm for constructing the whole Earth.

### D021 — Intersecting hard boundaries are refined, not overwritten

- Decision: the blanket precedence stack of S02 is not used to erase one mandatory boundary with another.
- Rationale: an immigration scope and a control boundary may intersect; both must be preserved.
- Rules: R009, R028–R030.
- Counterarguments: when one line has different sources, a resolution policy is still needed. Giving up last-wins does not resolve a source conflict automatically.
- Status: tentative.
- Basis: N01; an explicit departure from the recommended precedence of S02, consistent with the common-refinement idea of S03.

### D022 — CSV as a set of assertions, not a catalogue of recognised regions

- Decision: record the comparison target, premises, basis, factual verification and model issues separately from the expected outcome.
- Rationale: a split from the metropole does not mean a single atom; a negative factor does not prove a merge; intuition must not become the test oracle.
- Rules: R008, R034–R036.
- Counterarguments: many real cases will remain conditional until the fact-finding work is done. This is an acceptable limit of the stage.
- Status: tentative for the schema; the adversarial approach is accepted under S05.
- Basis: N01.

## Two-stage architecture decisions

### D023 — Final regions remain single-level

- Decision: the published Canonical Travel Regions output remains one exhaustive, mutually exclusive, single-level partition.
- Rationale: construction stages must not become a user-visible parent/child ontology.
- Rules: R003–R005, R043.
- Status: accepted.
- Basis: explicit user architecture decision, 2026-09-12.

### D024 — Construct the partition in two refinement stages

- Decision: construct the final partition through Stage 1 Mandatory Separation followed by Stage 2 Destination Partition.
- Rationale: hard travel boundaries and destination semantics answer different questions and require different evidence.
- Rules: R009, R039–R041.
- Status: accepted.
- Basis: explicit user architecture decision, 2026-09-12.

### D025 — Stage 1 establishes mandatory hard boundaries

- Decision: Stage 1 finds boundaries the final partition may not cross, using only accepted hard dimensions.
- Rationale: admission, legal/access, jurisdiction, and materially relevant control differences can require separation without deciding destination structure.
- Rules: R007–R017, R039.
- Status: accepted.
- Basis: explicit user architecture decision, 2026-09-12.

### D026 — Stage 2 only subdivides Stage 1 cells

- Decision: `Stage2Partition refines Stage1Partition`; Stage 2 cannot merge across a Stage 1 boundary.
- Rationale: mandatory separation must be monotonic through construction.
- Rules: R009, R041.
- Status: accepted.
- Basis: explicit user architecture decision, 2026-09-12.

### D027 — Stage 2 introduces destination semantics

- Decision: destination identity, geographic and itinerary coherence, gateway structure, and related destination concepts are first-class Stage 2 inputs.
- Rationale: the final travel partition must be able to distinguish destinations even when Stage 1 finds no hard boundary.
- Rules: R040.
- Status: accepted; algorithm unresolved in Q012.
- Basis: explicit user architecture decision, 2026-09-12.

### D028 — `hard_compatible` is not a final merge decision

- Decision: rename the Q001 outcome `may_merge` to `hard_compatible`.
- Rationale: complete and equal hard signatures establish only that Stage 1 requires no boundary; Stage 2 may still split the units.
- Rules: R008–R009, R035, R038.
- Status: accepted.
- Basis: explicit user terminology correction, 2026-09-12.

### D029 — Territorial/legal identity differs from destination identity

- Decision: territorial/legal identity remains a possible unresolved Stage 1 separator, while destination identity belongs to Stage 2.
- Rationale: institutional status and coherent travel-destination meaning are separate predicates. P3 addresses only the former.
- Rules: R010, R040, R042.
- Status: accepted distinction; territorial/legal predicate and destination algorithm remain unresolved.
- Basis: explicit user architecture decision, 2026-09-12.

### D030 — Finer subdivisions are outside project scope

- Decision: subdivisions finer than the Stage 2 canonical destination partition are outside this repository's ontology.
- Rationale: an external finer-granularity product must not distort either construction stage.
- Rules: R043.
- Status: accepted.
- Basis: explicit user scope decision, 2026-09-12.

## Local access overlays

### D031 — Local restricted-regime zones do not create a split

- Decision: border, military, nature-protection, site-specific, route-specific and activity-specific restrictions inside a common admission jurisdiction are modelled as spatial access overlays and do not by themselves create a canonical region.
- Rationale: they change the local access of an already admitted traveller, not admission to a separate territorial destination. The coincidence of an overlay with an administrative district or a federal subject does not change its semantics.
- Rules: R007, R008, R014, R017.
- Counterarguments: some permits cover a candidate territory as a whole and in practice function as destination admission. A general predicate for separating such cases remains Q005.
- Status: tentative; the direction is directly confirmed for Russian border zones, generalisation to all types of restricted-regime zones requires the Q005 check.
- Basis: the user's clarification of 12 September 2026.
- ID history: during integration D031 was assigned instead of the duplicate D017 from upstream; the original D017 on the coverage of closed territories is preserved.
- Note, 2026-10-03: D050 adopts the Q005 convention — a standing permit requirement for presence in a whole top-level or detached unit separates that unit; a permit for part of a unit, a border band or district, a list of places or a closed town stays a marker, as this entry says.

## CR-W core adoption

### D032 — CR-W is accepted as the current production Stage 1 core

- Decision: `S1-core-v1` uses only CR-W — a proven hard territorial TravelDecision discontinuity with G-SCOPE/G-CONTEXT/G-HARD/G-TIME/G-EVIDENCE from the review. One valid class-based witness is sufficient regardless of frequency; there is no frequency threshold.
- Rationale: proven different territorial decisions are incompatible with a single accepted hard decision function. A certificate that has not been found does not prove equality; `hard_compatible` requires positive complete equality of all accepted dimensions on the same S/t.
- Rules: R007–R009, R012, R031, R038, R039, R044.
- Status: accepted. Q001 narrowed/resolved for regime-based mandatory separation; the Stage 1 semantics as a whole are not declared complete. Amended by D050 (2026-10-03): which classes are witnesses, which differences are hard, and which scopes qualify.
- Basis: the user's explicit normative decision of 2026-09-12, after the Q001 Stage 1 rule review.

### D033 — CR-J is defined but not accepted

- Decision: CR-J has the status **well-defined normative candidate; not adopted**. The full definition of J1–J6 in the review/candidate YAML is preserved unabridged for a future experiment/decision. CR-J is not a separator and not a mandatory signature dimension of production `S1-core-v1`.
- Rationale: CR-J can create a mandatory boundary when the current traveller-facing hard functions are equal; institutional responsibility is a normative choice in its own right, not proven by a current travel discontinuity. Additional empirical coverage is not proven by the current 49 cases.
- Rules: R011, R038, R044.
- Status: accepted deferral; adoption of CR-J unresolved in Q001.
- Basis: the user's explicit decision of 2026-09-12. This entry differs from the recommendation in the historical review to accept W OR J.

### D034 — Undefined territorial/legal identity is excluded from production

- Decision: **territorial/legal identity alone is not an accepted Stage 1 hard separator**. Undefined identity is not part of the production or production-candidate hard semantics. P3 is a historical, non-production, model-unresolved profile, not a Stage 2 destination model.
- Rationale: there is no general operational predicate; labels, a registry and politically salient place lists do not replace it. A future explicit legal-status rule requires a separate decision on Q006.
- Rules: R010, R038, R042, R044.
- Status: accepted. The historical P3 sufficient P1/P2 outcomes and identity blockers are preserved as results of the old experiment.
- Basis: the user's explicit decision of 2026-09-12.

### D035 — Claims, disputes, control and category labels are insufficient

- Decision: a disputed flag, a claim, different recognition/controller/military control, dependency, autonomy, overseas and island labels do not on their own create a Stage 1 split. Only their proven actual hard territorial travel consequences can support CR-W.
- Rationale: a fact about status/control does not prove a difference in D; they are kept in their own factual layers and in unresolved Q006/Q007/etc., without a hidden hard dimension.
- Rules: R015, R016, R018, R022–R024, R039, R044.
- Status: accepted.
- Basis: the user's explicit decision of 2026-09-12.

### D036 — Accepted product regressions are not hardcoded rules

- Decision: D004/D005/D006/D007 are not removed and not downgraded. Their status is accepted product regression constraint, distinct from a currently derivable Stage 1 rule. If CR-W does not guarantee a constraint, an explicit open conflict/requirement is kept.
- Rationale: a general rule must not be derived from a desired answer. For Réunion there is a regime mechanism, but a complete witness has not been assembled in the snapshot; a blanket UKOT guarantee does not follow from CR-W; Crimea has no Q001 factual dossier; Western Sahara west / Morocco has no proven CR-W. No special cases, no claimed resolution through Stage 2, and no substituting a dispute overlay for a separate region.
- Rules: R008, R009, R018, R022, R024, R044; the remainder of Q006/Q011 and the relevant data/model gaps.
- Status: accepted distinction; the accepted constraints remain open in the part that is not proven.
- Basis: the user's explicit decision of 2026-09-12.
- Note, 2026-10-03: with the reference registry (D038) D004–D007 are expected to be derived, not hardcoded — D004 and D005 through ISO 3166-1 entries, D006 and D007 through ISO entries and areas that declared perspectives attribute differently ([Stage 1 as a list](../experiments/stage1-list/README.md), a draft without geometry). The British Antarctic Territory is covered by the explicit convention D040. The constraints stay open until a release check (V011) confirms the derivation.

### D037 — Historical profiles and current production are separated

- Decision: P1/P2/P3 keep the historical contract `0.2.0-draft`, profile version `q001-0.2.0` and evaluator serialization `0.2.0`. The new `S1-core-v1` has its own proof input, evaluator version `s1-core-1.0.0` and spec `0.3.0-draft`. The old P1 results are not renamed into production results; the factual dataset and the old result files are not changed.
- Rationale: the historical witness schema does not contain a full CR-W gate audit; carrying it over requires a new versioned certificate. J/identity are not inherited into production completeness.
- Rules: R008, R033, R035, R038, R044.
- Status: accepted implementation consequence of D032–D034.
- Basis: the user's explicit reproducibility requirement of 2026-09-12.

## Decisions of 2026-10-03

Taken one at a time in conversation with the owner; the backlog and its order are in [status.md](status.md). Issues: [#17](https://github.com/uncovering-world/travel-regions-extraction/issues/17), [#19](https://github.com/uncovering-world/travel-regions-extraction/issues/19), [#20](https://github.com/uncovering-world/travel-regions-extraction/issues/20), [#22](https://github.com/uncovering-world/travel-regions-extraction/issues/22). Named places in these entries are examples the owner used, not rules.

### D038 — No region crosses a country boundary under a supported perspective

- Decision: Stage 1 refines a declared reference registry — ISO 3166-1 and the national points of view of Natural Earth. A region never crosses a country boundary under any supported perspective. The rule sits in Stage 1, so Stage 2 cannot cross it either (R041).
- Rationale: the consumer needs every region inside one country under each perspective it supports, so that "regions of a country" can be read from the canon (consumer contract C2, C3; TYR #770, #771). CR-W cannot guarantee that: it separates only where entry rules differ, so a microstate with no entry regime of its own would merge with its neighbour. ISO 3166-1 alone has no cell for Crimea, Kosovo, Northern Cyprus, Somaliland, Abkhazia, South Ossetia or the Sovereign Base Areas; with the national points of view the first world draft derives D004–D007 except the Antarctic case (settled by D040).
- Rules: R045; R009, R016, R039 amended; notes on R010, R018, R019, R022, R023, R028; check V011.
- Counterarguments: the registry is a product declaration, not a legal proof; which disputes become cells depends on a dataset's columns, and Natural Earth's attributes contain opaque codes and at least one error, so names and attributions cannot be taken from it unchecked (Q014). The alternatives were CR-J, which needs a J1–J6 legal proof per pair and does not separate areas where perspectives disagree, and a curated list of names, which R008 and D036 reject. Small perspective-dependent areas are not handled by a size floor or by the substrate (D052) but by kind (D044–D047); where those make an area a special place, its land stays in its holder's region even though a perspective places it elsewhere.
- Status: accepted.
- Basis: owner decision, 2026-10-03; [reference-registry proposal](proposals/reference-registry.md); [world Stage 1 draft](../experiments/stage1-world-draft/README.md); [consumer contract](proposals/consumer-contract.md) (proposal).

### D039 — The canon is pinned to stated editions of its reference lists

- Decision: the canon is pinned to stated editions of ISO 3166-1 and Natural Earth, and moves to a new edition only by the owner's decision at a release, after seeing what the new edition would change.
- Rationale: a new edition can add, remove or reattribute cells; the consumer needs regions that change only for a stated reason (consumer contract C7).
- Rules: R045, R055.
- Counterarguments: the canon can lag behind a change that both lists already show, by up to a release.
- Status: accepted.
- Basis: owner decision, 2026-10-03; [reference-registry proposal](proposals/reference-registry.md), parameter 4; [release stability proposal](proposals/release-stability.md).

### D040 — Antarctica is one Stage 1 cell, divided in Stage 2 by access

- Decision: the Antarctic land in U is one cell in Stage 1. Stage 2 divides it by how and from where travellers reach it, also taking into account how people who work there see it. National claims stay an overlay and create no region, including where a declared perspective of the registry would attribute a sector to a claimant.
- Rationale: overlapping claims cannot become mutually exclusive regions (R004), and the Treaty preserves positions on claims without settling them (E04). How travellers reach the continent is a destination question, which belongs to Stage 2.
- Rules: R026 amended; R045 (qualification 3); Q003, Q011, Q012 annotated. Supersedes D016.
- Counterarguments: the British Antarctic Territory and the Antarctic parts of other claimants are not regions, so the literal "each British overseas territory separately" of D004 does not hold there. This is an explicit, named convention adopted by the owner (Q011), not a derived rule. The Stage 2 criteria are not yet operational.
- Status: accepted.
- Basis: owner decision, 2026-10-03; [reference-registry proposal](proposals/reference-registry.md), parameter 3.

### D041 — Special places are objects inside their parent region

- Decision: places that the rules do not make regions but that matter to travellers — border-line disputes, undelimited stretches, uninhabited islets and claimed rocks, uninhabited zones, small leases — are special places: tickable, shown with the region that holds them, and not counted as regions. The owner expects Track Your Regions to carry them as a category of their own, something like "border curiosities"; this is raised with TYR as an importer need, not changed from here.
- Rationale: a hardcore traveller seeks such places out, but most have no outline that the parties state (D042) and no residents; as regions they would add cells the canon cannot delimit. As objects they stay visible without breaking the partition.
- Rules: R046; R050–R054, R056.
- Counterarguments: a special place adds nothing to region totals, and a consumer without a category for them loses them. Its land may lie in a region that a declared perspective attributes to another country (Q018).
- Status: accepted.
- Basis: owner decision, 2026-10-03.

### D042 — Outlines come from lines the parties state; the substrate is extensible

- Decision: the outline of a special cell is never drawn here. It comes from lines the parties themselves state — claim, ceasefire, treaty or lease lines, coastlines; where there are none, there is no cell, only a special place. The registry and the register say which places are separate and whose they are; they are not the only source of outlines. The substrate must be extensible: where it has no fitting unit, a custom geometry is added as needed, from a cited source of the line the parties state.
- Rationale: a line drawn here would be the project's own judgement of a dispute; a front line moves. The canon must not depend on one substrate, which is weak in places (consumer contract C6; South Ossetia is poorly cut in GADM).
- Rules: R047; notes on R028, R030.
- Counterarguments: some distinct places have no stated line and remain special places only. Stated lines are published unevenly and in different forms. How custom geometries are sourced, pinned and versioned is not designed (Q013).
- Status: accepted.
- Basis: owner decision, 2026-10-03 (the outline principle and the statement on geometry); [Stage 1 as a list](../experiments/stage1-list/README.md).

### D043 — The holder of an area, and the settling rule for contested control

- Decision: (1) An area's holder is the party whose officers can in practice admit a civilian, refuse one and remove one; rules that cannot be enforced there do not count. Holding in fact is enough; there is no separate condition about civil administration. (2) An area taken by force, with a claim by the new holder and within an outline the parties state, is unsettled and stays attributed to its last settled holder. The canon accepts the new holder after three consecutive quiet calendar years, or at once when the side that lost the area stops contesting by an explicit act — an agreement, an accepted ruling, a renunciation of the claim, or ceasing to exist; nothing weaker counts. (3) There is no original or rightful holder: a retaking is a change like any other (D053). (4) The status creates no regions: an unsettled area becomes a region through the registry or CR-W, and at acceptance at the latest. (5) While fighting moves the line, nothing is delimited; the regions touched carry a flag (the owner's proposal). The status and its paths are as in the settling-rule proposal.
- Rationale: on 78 seizures by states and 40 breakaway entities since 1945, raising the wait from two to three years is the last step that removes reversals by force; beyond three, waiting removes only changes later ended by agreement, at a growing cost; the picture at the end of 2024 is the same for one to three years. Who held an area first is often disputed, and some conflicts run for decades with long pauses. An act has a date and a document; "can no longer act" would be a judgement of ours. Holding in fact applies to uninhabited areas too: 16 of the 39 seizures accepted at three years are uninhabited, and a condition about administration for residents could never be met there.
- Rules: R048, R049; notes on R015, R024, R030; Q007, Q008 narrowed.
- Counterarguments: each step in the back-test rests on two to four cases, with year precision and one author's dataset per population; two years is defensible as the literature's convention. Acceptance by time can be read as accepting the result of force; the canon records whose officers a visitor meets, and the other side stays a claimant. The tie from areas to UCDP conflicts is a judgement by name and is the clock's weakest input. What applies when the holder test cannot tell the parties apart is open (Q016).
- Status: accepted.
- Basis: owner decision, 2026-10-03; [settling-rule proposal](proposals/settling-rule.md); [settling-rule back-test](../experiments/settling-rule/README.md); [control-duration experiment](../experiments/control-duration/README.md); [literature note](research/2026-10-03-settling-time-literature.md). The earlier definition of "administers", with civil administration as a fallback, was agreed only in principle; its fallback is in Q016.

### D044 — Disputes about where a border line runs are special places

- Decision: an area whose register kind is `line_position` is not a cell. The land belongs to the region of whoever holds it, and the dispute is a tickable special place on top of the map.
- Rationale: both sides agree that a border exists and disagree only on where it runs; a cell would be a region bounded by the very line in dispute, with no outline the parties share.
- Rules: R050; R046.
- Counterarguments: a declared perspective that shows the strip as another country's is not honoured by the region boundary there (R045, qualification 2; Q018).
- Status: accepted.
- Basis: owner decision, 2026-10-03; [register of disputed areas](../data/disputed-areas/README.md).

### D045 — Islets and paper claims: regions only where civilians live

- Decision: an islet group disputed for the sea around it (`islets_for_maritime_zone`) with resident civilians (`inhabited` = `yes`) is a region, outlined by its coastlines; the others are special places, their land going with whoever holds it. An area another state claims on paper only (`paper_claim`) is a region if a supported perspective puts it in another country and it has resident civilians; otherwise it is a special place and its land goes with the holder. Areas with their own ISO 3166-1 entry stay regions regardless; a claim that no supported perspective shows gives only a marker.
- Rationale: where people live under one party while another claims the place, a visitor meets a distinct situation; an uninhabited rock is better kept visible as a special place than as a cell. Residents are a sourced register fact, and coastlines are outlines the parties do not contest.
- Rules: R051; R045, R046, R055.
- Counterarguments: the test turns on one register fact and on which perspectives are declared. A group held in parts by several parties with no line between the parts has no single country in the default view; how that is handled was left to be settled when the rule is recorded and is open (Q016). When the last residents leave, the region follows the exit rule of D049.
- Status: accepted.
- Basis: owner decision, 2026-10-03; [Stage 1 as a list](../experiments/stage1-list/README.md).

### D046 — Zones with no single holder

- Decision: an area of kind `own_regime` — a UN buffer or separation zone, a demilitarised zone, a condominium — is a region with no country if civilians live there and the parties state its outline; otherwise it is a special place. Nothing is split between the neighbours.
- Rationale: such a zone is run by neither neighbour as ordinary territory; splitting it along a midline would draw a line the parties never stated (D042).
- Rules: R052; R046, R047.
- Counterarguments: for an uninhabited zone or one without a stated outline, the decision does not say which region holds its land (Q016).
- Status: accepted.
- Basis: owner decision, 2026-10-03.

### D047 — Leased areas and bases belong to the lessor's country

- Decision: for an area of kind `lease_or_base` the country is the lessor's, since the parties agree whose land it is; the area is a region only where entry follows its own rules (examples: Baikonur, Guantanamo Bay), and the lessee is named. A leased road or piece of a port with no population and no entry rule of its own is not a region; it is a special place.
- Rationale: a lease is an agreed arrangement, not a dispute over whose land it is; what a visitor meets is decided by whether entry differs.
- Rules: R053; R046, R056.
- Counterarguments: whether a leased area has its own entry rule is often poorly documented; four leased sites still lack that fact in the list build.
- Status: accepted.
- Basis: owner decision, 2026-10-03; [Stage 1 as a list](../experiments/stage1-list/README.md).

### D048 — Recently resolved disputes need no rule of their own

- Decision: for an area of kind `resolved_recently` the agreed outcome is taken over at the next release, and the place may stay as a special place.
- Rationale: an agreed settlement is the explicit act of D043 and a fact like any other.
- Rules: R054.
- Counterarguments: when a resolved dispute stays a special place is not stated (Q018).
- Status: accepted.
- Basis: owner decision, 2026-10-03.

### D049 — Yearly releases; when an uncontested boundary enters and leaves

- Decision: one release a year, for the situation at the end of the year; between releases the set of regions does not change, and only errors of ours are corrected. A part of a country becomes a region because of its own entry rule only when the rule is in force at two yearly releases in a row; a stated expiry or "pilot" label is ignored. When the rule is suspended or ends, the region stays, marked as having no special rule at present, and is merged back if the rule has not returned after three years — the same number as the waiting time for contested control. The same holds for any boundary that lost its basis, including an islet group or claimed area whose last residents left.
- Rationale: of 55 territory-specific entry regimes started since 2000, 4 ended within two years outside the 2020 closures; a second cut-off halves the short-lived entries, a third adds nothing. Stated expiries were mostly outlived and early endings were not announced, so a rule's stated duration is a poor guide. Suspended regimes usually came back within two to four years, so a suspension should not remove a boundary at once. The consumer needs regions that hold still (consumer contract C7).
- Rules: R055; notes on R031, R032; Q008, Q010 narrowed.
- Counterarguments: every new regime waits a year; a release can show a region whose rule has lapsed, for up to three years (it is marked). The regime collection under-counts ended regimes. The release-stability proposal's exit after two cut-offs, its de-minimis rule and its correspondence tables were not decided (Q019).
- Status: accepted.
- Basis: owner decision, 2026-10-03; [release stability proposal](proposals/release-stability.md); [regime-lifetimes experiment](../experiments/regime-lifetimes/README.md).

### D050 — CR-W amendments: transit, scope, presence permits, group, border-traffic and operator rules, held areas, fees

- Decision:
  1. A rule for travellers in transit is not a witness; only trips to the place as a destination are compared, and a transit regime's territorial limits are an overlay (proposal A1).
  2. A place with its own entry rule is a region only if it is a whole top-level unit of its country, or a smaller but detached unit — an island or an exclave — that has a rule written for it, not a line in a list. Everything else is an object inside its region, marked (border bands and districts, lists of islands or ports, closed towns, single valleys). This replaces proposal A2.
  3. A standing rule that makes presence in a whole unit conditional on a permit for an ordinary visitor separates that unit, for the same kinds of unit as in item 2; a permit for part of a unit stays a marker (proposal A3; the convention Q005 asks for).
  4. A rule that applies only to organised groups is not a witness; only a rule for an independent visitor separates. Group schemes are markers.
  5. A rule only for residents of a neighbouring area across the border (local border traffic) is not a witness; it is a marker.
  6. A rule under which a place can be reached only through a tour operator is a witness, because it closes the place to an independent visitor.
  7. For an area held by another party, the holder's own entry rule, with an outline the parties state, is the witness; the test of item 2 is not applied.
  8. A mandatory fee or purchase on arrival does not separate; only rules on who may enter and for how long do (visa, permit, separate control, stay limit). Fees are markers. This answers Q004 for entry.
- Rationale: applied to 116 real regimes, CR-W without amendments produced artefacts — transit areas, border bands, lists of sites — next to good cells; the census went from 55 cells to 26 under the first proposal. Transit, group, border-traffic and fee rules describe how a trip is organised or paid for, not who may be in the place. The owner found A2 too coarse: a list of whole border districts would have passed it. Whole-unit permits keep places that every travel list treats as their own; a tour-operator-only rule closes a place to an independent visitor, which a group concession does not.
- Rules: R056; R014, R044 amended; notes on R007, R013, R017, R027; Q002, Q004, Q005, Q009 narrowed.
- Counterarguments: one rule over several top-level units separates each of them, which looks odd as a set of regions (a known rough case, Q015). "Top-level" and "detached" need an operational source (Q015). The line between a tour-operator rule and a group concession must be read from each rule's text. The amendments narrow what a producer may attest under the gates; they do not change the evaluator's input contract.
- Status: accepted.
- Basis: owner decision, 2026-10-03; [CR-W amendments proposal](proposals/crw-amendments.md); [world Stage 1 draft](../experiments/stage1-world-draft/README.md); [Stage 1 as a list](../experiments/stage1-list/README.md).

### D051 — Product profile: no witness, no boundary; "cited" evidence enters a release

- Decision: releases are built with "no witness, no boundary": inside a country a boundary exists only where a rule with a source is recorded, and the rest is marked as assumed, not proved. A witness at the level "cited" (source, passage and dates; may be prepared by the agent) is enough for a release; review by a named person is for conflicting or missing primary sources, or on the owner's request. The strict core stays as the definition of a proved boundary; every boundary in a release states its rule and evidence level.
- Rationale: under the strict core two areas are compatible only after positive proof of equality in all seven hard dimensions for every traveller context; the Q001 experiment reached that in 0 of 147 results. A release cannot wait for that. Two profiles keep "proved" and "assumed for now" apart instead of weakening the core.
- Rules: R057; note on R038.
- Counterarguments: a cited witness prepared by an agent can be wrong; the evidence level is published so the consumer can see it. A place whose rule is widely reported but has no cited source (the proposal's example: a permit described only by travel agencies) gets no boundary until a source is found. Treating evidence below "cited" as insufficient follows the proposal's text; the owner's statement names only "cited" as sufficient.
- Status: accepted.
- Basis: owner decision, 2026-10-03; [product profile proposal](proposals/product-profile.md).

### D052 — Rejected: tying small disputed areas to the substrate, or a bare area threshold

- Decision: two ways of deciding which small perspective-dependent areas become cells are rejected: (a) an area that no substrate unit can represent is attached to the administering cell and marked; (b) an area below a fixed size (the first world draft used 100 km²) is not a cell.
- Rationale: the substrate is not an authority — whether a boundary dataset happens to have a unit says nothing about the place. A size threshold cuts arbitrarily: in the first draft it removed Akrotiri (78 km²) and kept Dhekelia (102 km²). Both are replaced by the treatment by kind (D044–D047).
- Rules: none; R045 qualification 2 and R050–R053 apply instead.
- Counterarguments: both options are simple and need no register facts; the kind-based treatment depends on the register's `kind` and `inhabited` facts, which still have gaps.
- Status: rejected.
- Basis: owner decision, 2026-10-03; [reference-registry proposal](proposals/reference-registry.md), parameter 2; [world Stage 1 draft](../experiments/stage1-world-draft/README.md).

### D053 — Rejected: taking a retaking by the "original holder" over at once

- Decision: an earlier draft of the settling rule took a retaking by an area's original holder over at once. Rejected.
- Rationale: who held an area first is often disputed, and some conflicts run for decades with long pauses. Where no waiting is needed, the reason is that the other side stopped trying — the dispute over Nagorno-Karabakh ended with the dissolution of Artsakh — not that the first holder came back. Under the adopted rule a retaking is a seizure like any other (Thule Island: accepted as held by Argentina in 1979, retaken by British troops in 1982, accepted as held by the United Kingdom in 1985).
- Rules: R049 (no original holder).
- Counterarguments: a state that recovers its own territory waits as long as a conqueror unless the other side stops contesting by an act.
- Status: rejected.
- Basis: owner decision, 2026-10-03; [settling-rule proposal](proposals/settling-rule.md).

### D054 — Unclaimed land and boundaries that are not agreed

- Decision: land that no state claims (register kind `unclaimed`) is a region of its own attributed to no country; its outline is what the neighbours' own claim lines leave out. An area where a boundary must exist but no line is agreed (`no_agreed_boundary`) is not a region: its land goes with its holder (R048) and the place is a special place (R046).
- Rationale: unclaimed land is a distinct place nobody administers, and its extent follows from lines the parties state, so no outline is drawn here (R047). Where a boundary is merely undefined, the area will be somebody's once a line exists, and the parties state no outline for it.
- Rules: R058.
- Counterarguments: the outline of unclaimed land depends on two claim lines that can change; an undelimited stretch held by nobody in practice falls to the fallback of R048.
- Status: accepted.
- Basis: owner decision, 2026-10-03 (agreed in principle, confirmed once D042 and D043 were adopted); [status](status.md); [register kinds](../data/disputed-areas/UPDATING.md).

### D055 — Holder when access control cannot tell the parties apart

- Decision: where the test of R048 (whose officers can admit, refuse and remove a civilian) cannot tell the parties apart, the holder is the party that provides civil administration to the residents; if there is none, the area has no holder.
- Rationale: completes the definition of "administers" agreed in principle together with the access-control test, once its stability guards (R049) were settled.
- Rules: R048 (amended).
- Counterarguments: civil administration can be split as well (a condominium); then the area has no holder and R052 applies if it qualifies.
- Status: accepted.
- Basis: owner decision, 2026-10-03 (agreed in principle, confirmed after R049 was adopted).

### D056 — Outline sources: every available dataset, the canon being part of Track Your Regions

- Decision: outlines of regions may come from any of Natural Earth, GADM, OpenStreetMap, and custom geometries digitised from cited documents. The canon is part of the Track Your Regions project, which already uses GADM; the licences of these datasets are taken as they apply to that project.
- Rationale: the [outline-source survey](../experiments/outline-sources/README.md) found that Natural Earth covers every ISO entry and registry cell but few small places; OpenStreetMap covers almost everything; ten regions (mostly leases and zones) have no outline in any of them. Using all sources keeps custom work to those few.
- Rules: R047 (amended).
- Counterarguments: GADM's licence allows non-commercial use and forbids redistribution without permission; OpenStreetMap's (ODbL) requires derived data to be distributed under the same licence. Geometry from them follows those terms wherever it is published.
- Status: accepted.
- Basis: owner decision, 2026-10-04; [outline-source survey](../experiments/outline-sources/README.md); Q013.

### D057 — A leased area or base is a region when its holder is not the lessor

- Decision: a leased area or base (register kind `lease_or_base`) is a region when its holder (R048) — the party whose officers in practice admit, refuse and remove a civilian — is a state other than the lessor. Otherwise it stays in the lessor's region as a special place. The region is attributed to the lessor's country and names its holder.
- Rationale: R053 asked for "entry rules of its own" and the list build read that as a recorded entry rule with a source, so a base whose entry another state controls (Guantanamo Bay) fell to a special place for want of a document. The holder test already defines who decides entry and applies to every lease alike; a property lease where the lessor's officers still decide entry (the Czech lots in the Port of Hamburg, as expected) stays a special place.
- Rules: R053 (amended).
- Counterarguments: uninhabited military sites held by another state become regions too (expected for the Russian ranges in Kazakhstan); the holder of each lease has to be sourced.
- Status: accepted.
- Basis: owner decision, 2026-10-04; [Stage 1 as a list](../experiments/stage1-list/README.md).

### D058 — A leased area held by the lessee is a region only if civilians live there

- Decision: amends D057. A leased area or base is a region when its holder (R048) is a state other than the lessor **and** civilians live there (register fact `inhabited` = yes). Otherwise it is a special place in the lessor's region.
- Rationale: under D057 alone a road section and a guarded tomb held by another state became regions; the owner wanted small sites like these to be curiosities. Size thresholds were rejected earlier (D052), and "a destination in its own right" could not be checked from a source without excluding Guantanamo Bay, which has no travel-guide article. The residents test is the one already used for islets, paper claims and zones with no single holder (R051, R052).
- Rules: R053 (amended).
- Counterarguments: an uninhabited site that travellers do visit in its own right is a curiosity, not a region; the result depends on the register's `inhabited` facts, which are missing for many small sites (missing means special place).
- Status: accepted.
- Basis: owner decision, 2026-10-04; [Stage 1 as a list](../experiments/stage1-list/README.md).

### D059 — Custom geometries: Natural Earth first, more detailed sources place by place

- Decision: where the substrate cannot represent a place as the canon needs (no unit, land given to another country than its holder, no polygon at all), the canon's own geometry is the polygon of Natural Earth v5.1.2's disputed-areas layer, the edition the registry uses. OpenStreetMap or a Commons map is used where Natural Earth has nothing, and an outline is digitised from a cited document where no source has one. A more detailed source replaces Natural Earth for a place one at a time, after a check that it follows the line the parties state, and at a release.
- Rationale: the [custom-geometry survey](../experiments/custom-geometry-sources/README.md) found a Natural Earth polygon for 41 of 47 such places; Natural Earth is pinned, public domain and consistent with the registry. Its 1:10 million scale matters only where travellers come close to a small place's edge.
- Rules: R047 (amended).
- Counterarguments: near the edge of a small place a visit point can fall on the wrong side until a detailed source replaces Natural Earth there.
- Status: accepted.
- Basis: owner decision, 2026-10-04; [custom-geometry survey](../experiments/custom-geometry-sources/README.md); [GADM binding](../experiments/gadm-binding/README.md); Q013.
