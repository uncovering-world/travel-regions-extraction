# Canonical Travel Regions — decision log

Version: 0.3.0-draft. Date: 2026-09-12. Related documents: [spec.md](spec.md), [open-questions.md](open-questions.md).

The current normative decision on Stage 1 is D032–D037. Earlier research/experimental entries preserve the history but do not override the later, explicitly accepted CR-W-only core. D004–D007 remain accepted product constraints.

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

### D014 — Splitting Western Sahara by operational control

- Decision: S02/S03 propose at least two areas on the two sides of the Berm, linked by a common dispute_id.
- Rationale: different actual conditions of control and access.
- Rules: R015, R022, R024, R028, R030.
- Counterarguments: a map of the Berm is not identical to an exact current map of control; buffer/restricted strips and changes of control may require a different refinement. Two areas do not prove the separation of the western part from Morocco.
- Status: tentative. Exactly two final cells are not approved.
- Basis: the corresponding sections of S02/S03. E03 confirms only the legal-status layer.

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
- Status: tentative; reconciliation with the literal "each UKOT separately" is unresolved.
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

## CR-W core adoption

### D032 — CR-W is accepted as the current production Stage 1 core

- Decision: `S1-core-v1` uses only CR-W — a proven hard territorial TravelDecision discontinuity with G-SCOPE/G-CONTEXT/G-HARD/G-TIME/G-EVIDENCE from the review. One valid class-based witness is sufficient regardless of frequency; there is no frequency threshold.
- Rationale: proven different territorial decisions are incompatible with a single accepted hard decision function. A certificate that has not been found does not prove equality; `hard_compatible` requires positive complete equality of all accepted dimensions on the same S/t.
- Rules: R007–R009, R012, R031, R038, R039, R044.
- Status: accepted. Q001 narrowed/resolved for regime-based mandatory separation; the Stage 1 semantics as a whole are not declared complete.
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

### D037 — Historical profiles and current production are separated

- Decision: P1/P2/P3 keep the historical contract `0.2.0-draft`, profile version `q001-0.2.0` and evaluator serialization `0.2.0`. The new `S1-core-v1` has its own proof input, evaluator version `s1-core-1.0.0` and spec `0.3.0-draft`. The old P1 results are not renamed into production results; the factual dataset and the old result files are not changed.
- Rationale: the historical witness schema does not contain a full CR-W gate audit; carrying it over requires a new versioned certificate. J/identity are not inherited into production completeness.
- Rules: R008, R033, R035, R038, R044.
- Status: accepted implementation consequence of D032–D034.
- Basis: the user's explicit reproducibility requirement of 2026-09-12.
