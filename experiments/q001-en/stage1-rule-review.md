# Q001 — Stage 1 rule review

Subsequent decision of the user: **only CR-W** is accepted in `S1-core-v1`; CR-J — well-defined normative candidate, not adopted. See the [adoption record](stage1-core-adoption.md). The rest of the text is kept as historical analysis, including the former recommendation W OR J; it is not the current accepted norm.

Date of the review: 2026-09-12. Status: **candidate analysis; normative changes not applied**.

Recommendation: **B — Q001 can be narrowed**. The minimal candidate is a proven territorial difference of hard TravelDecision **OR** a proven independent final admission competence. Exclude undefined territorial/legal identity from the proposed production profile. Do not add a separate control separator now: proven admission/access consequences are already covered by the first ground, a structured actual admission jurisdiction — by the second. The residual questions of legal status, access and control remain explicitly limited to Q006/Q005/Q007/Q008/Q009.

This is a proposal, not the adoption of a new norm. It does not guarantee all of D004/D007 and does not declare Q001 closed. The [machine-readable companion](stage1-rule-candidates.yaml) contains the same rules, evidence gates, rejected alternatives and synthetic distinguishing cases; the existing evaluator does not execute this file.

## 1. Problem statement

Stage 1 forbids certain points from being together in any final region. It does not determine the independence of a destination and is not obliged to distinguish all future final regions. Stage 2 can only refine the Stage 1 partition; its algorithm is not studied here. Basis: [spec R008–R011, R038–R043](../../docs/spec.md), [D023–D030](../../docs/decisions.md), [architecture](../../docs/partition-architecture.md).

The question of Q001 is which **positively provable properties** it is sufficient to declare hard. The objectivity of a factual predicate does not by itself prove the normative necessity of a split: a measurable difference of time zones is objective too. It must be explicitly justified why the chosen dimension has to be homogeneous inside a Stage 1 cell.

The review analyses the existing snapshot 2026-09-11: 49 comparisons, 56 supporting units, 55 evidence records, 147 profile results. Sources: [comparisons](comparisons.yaml), [evidence](evidence.json), [source limitations](sources.json), [data gaps](data-gaps.md), [contract](evaluator-contract.md), [results](results/evaluator-results.json), [run summary](results/run-summary.md). The references E##/S## below relate to the Q001 dataset, not to the identically named references in the spec/decision log. New geographic facts were not collected; the existing statements were not upgraded in status and are not considered an independent check of the current law as of the date of the review. Crimea is present in D006/D013 and [adversarial T059/T060](../../data/adversarial-test-set.csv), but **has no factual unit/comparison in these 49 Q001 cases**.

Basis of the artifacts: repository commit `6ad56e16e3744c8ae98266408ac13a7717c9000f`; evaluator `0.2.0`; spec `0.2.0-draft`; recorded factual-input SHA-256 `fd4875e773731a4533549d3526ef54c4a0945c4ca84d8045214a517ebba61831`.

| Profile | must_separate | hard_compatible | separation_not_proven | model_unresolved | data_unknown |
|---|---:|---:|---:|---:|---:|
| P1 | 4 | 0 | 41 | 1 | 3 |
| P2 | 8 | 0 | 1 | 1 | 39 |
| P3 | 8 | 0 | 0 | 41 | 0 |

P1 certificates: C007, C029, C030, C042. P2 additionally receives C001, C008, C009, C012. No real pair has a proven complete P1 equivalence: **the set contains no proven counterexample "P1 equality + different jurisdictions"**. Therefore the difference of the counters does not prove the superiority of P2. P3 gave no additional split; its 0 terminal `data_unknown` is explained by the priority of the model blocker, not by the disappearance of unknown facts. In the old [summary](summary.md) C001/P1 is given as `separation_not_proven`; the current contract/results give `data_unknown` because of the provisional E01. The review uses the latest result, the source files are not corrected.

## 2. Evaluation criteria

A rule is assessed on four independent layers: whether the predicate is defined; whether its inputs are proven; whether the hard consequence follows from the chosen norm; whether the scope of the certificate is sufficient for the stated boundary. A product regression replaces none of these layers.

| Criterion | Verifiable test |
|---|---|
| Operational definability | Typed necessary premises, explicit true/false/unknown/model-unresolved; the words "special", "independent" are unfolded through verifiable relations. |
| External verifiability | Each premise has evidence, a locator, the competence of the source, a territorial and a temporal scope; an assertion in the dataset does not by itself replace proof. |
| Name blindness | Rename the territories, authorities and their IDs bijectively while preserving the relations; the result is isomorphic. No special values for specific countries. |
| Universality | The same proof gives the same outcome in unitary, federal, dependent and de facto arrangements. The absence of data does not exempt from the test. |
| Political independence | Claim, recognition count and label do not take part in the computation. The applicable law and the factual exercise are documented separately. |
| Temporal stability | One snapshot is reproducible; a change of signboard/office does not change the competence; a real change of the norm may change the result. Constancy of the geometry over time is not promised. |
| Minimality | Each additional ground distinguishes at least one formal case that the other grounds intentionally admit. |
| Over-/under-splitting | There are negative counterexamples; the classes of differences that the rule does not preserve are stated explicitly. |
| Open world | A witness that was not found and an independence that was not proven do not become equality or split. |
| Architecture | No destination intuition, no automatic island or administrative status; Stage 2 preserves every proven Stage 1 separator. |

"Does not split on the given factor" below means only the absence of a certificate from this factor. It is not `hard_compatible`, not a merge and not a final assignment.

## 3. P1 assessment

### 3.1. Sufficiency and necessity

**A proven difference of an already defined hard traveller-facing dimension is sufficient for Mandatory Separation.** If two places require different territorial admissions/documents/permissions in one admissible context, a single hard signature for them is wrong. The word hard is necessary here: a difference in ticket price, queue, flight or access to a building does not become hard merely because it affects the trip.

The statement "regime difference is necessary but not sufficient" does not fit logically. In P1 a witness that has passed all the gates is **sufficient**, and a true difference of decisions is a necessary condition of precisely a regime-based split. In the broader Stage 1 with P2 it is **not necessary**: the competences may be different under identical rules. There are good grounds to consider **P1 as a complete set of rules insufficient** if the product requires preserving independent responsibility for territorial admission; this is a separate normative choice, not a consequence of a passport that was found. Destination separateness is not an argument against P1 as a Stage 1 foundation at all.

Given proven equality of all included outputs, P1 systematically does not distinguish:

- Different final admission jurisdictions that coordinate the same rules; the independence of their future decisions is not a current regime witness.
- Territories with a different constitutional, dependency or international status that does not change the scoped TravelDecision.
- Different civil/military controllers, if all the included admission/legal-access outcomes are the same and decision-maker identity is not included in the outputs.
- Islands, autonomies, administrative areas, remote parts and destinations with one hard signature. For Stage 1 this is intentional indistinguishability.
- Customs/biosecurity-only, activity/site-access and decisions outside the approved traveller scope, if they are not included in the hard dimensions. Here Q004/Q005 is required, not an extension by the name of a territory.

None of these classes means that a specific pair in the dataset is already recognised as equal.

### 3.2. Existential witness semantics

Keep the existential quantifier, but define its operands:

```text
W(A,B,t) := exists C in S_v, d in H_v:
    eligible(C) AND comparable_trip(C,A,B)
    AND territorial_effect(d,A,B,C)
    AND standing_rule_at_t(d,A,B)
    AND proven(D_d(A,C,t) != D_d(B,C,t))
```

`S_v` is the versioned R007 scope; `H_v` is the closed list of hard outputs of the chosen candidate profile. `D` means normatively determined requirements/admissibility, not a forecast of the discretionary decision of a specific officer. `proven` requires both sides, all influencing exceptions and the same time. An unknown decision is not compared as a value. Two lawful discretionary possibilities with different realised outcomes do not yet prove a difference of regime.

`C` must be a consistent class of civilian short-term visit: the relevant citizenships, documents, residence/authorisations, purpose, duration, history and mode/class of route are fixed. A person who has already made the trip is not needed. A refusal in A is admissible as the answer to the query; requiring actually permitted entry to **both** sides would mean excluding the main negative admission witnesses. An artificial combination of incompatible documents/statuses does not create a witness.

For reproducibility the decisions are compared as functions on a **common** domain of contexts, not on different samples of visitors to A and B. A missing airport does not become "admission denied". `entry_point` is normalised into a proven class of procedure; a mismatch of the carrier name or of coordinates is not an independent dimension. The territorial force of a permission and the physical place where it is issued are stored separately.

With S/H/t fixed, the existential semantics is mathematically stable: complete decision functions are equal under an equivalence relation, a counterexample refutes the equality. A positive certificate is preserved when consistent evidence is added to the same snapshot. A correction of a fact, a change of the norm, of the scope or of the date may revoke it in a new version. This is not a violation of R041, which relates to refinement between the stages of **one** version.

### 3.3. Rare contexts and the absence of a frequency threshold

Yes, one rare document, special authorisation or narrow travel-history class is able to create a boundary that affects all users of the partition. This is the deliberate price of the requirement of homogeneity for the whole of S. The frequency of use of a document does not determine its legal effect; the condition "rare" must not be turned into an exception for an inconvenient case.

R007 already includes rare documents and special permits. Therefore rarity is not by itself a defect of P1. If a class of trips does not belong to the purpose of the product, that is a question of S/R007/Q002. If the difference is tied to an object or an entry event, that is the H/territorial gate, Q005/Q009. If the problem is precisely that **a valid hard witness inside S occurs too rarely**, it is impossible to remove the split while keeping full homogeneity of S. The scope or the homogeneity requirement will have to be changed honestly.

The proposed way without a frequency threshold: keep all documentarily admissible classes inside the civilian short-stay S; admit only class-based norms in effect that have a territorial admission/stay effect. A one-off decision by the name of a specific person, the arbitrariness of an officer or a one-off accident do not form an independent hard dimension. This is an explicit restriction on the kind of norm, not a restriction on the size of the class. A class may have one actual holder; arbitrary personal IDs are not admitted in the predicate. The equivalence of complete functions is not derived from a list of "typical passports".

The residual risk does not disappear: a narrow but standing and territorial norm will still give a split. If this is unacceptable, existential P1 and the desired degree of generalisation are incompatible; a frequency threshold would only hide this choice.

### 3.4. What the available witnesses showed

| Cases | Established in the current evaluator | Limitation for the candidate |
|---|---|---|
| C029/C030, E28 | A different visa requirement for one fully specified class, Jamaica ordinary passport. | A direct example of W; does not require a definition of jurisdiction or identity. |
| C007, E10/E19 | The Jersey ferry exception changes the admissible document; the evaluator accepts the witness. | The legal force of a document exception for territorial entry may be hard even under a route condition. A separate region must not be created out of a ferry terminal. The same logical class of trip and a territorial effect are needed, not only carrier practice. The temporal standing/event semantics is to be checked separately when the new gate is applied. |
| C042, E07/E08/E44 | A PAP is required in the destination scope, the ordinary reference is outside the schedule. | Not the conclusion "every whole administrative unit with a permit is a region". A legal territorial presence restriction is a hard candidate; a whole-unit label alone does not close Q005. In addition, the endpoint `in` is a reference scope: the witness does not prove the separation of **the whole of India** and an area that is part of it. |
| C018, E26 | The French overseas destination-visa distinction is documented; a complete traveller witness has not been assembled. | A good explanatory mechanism for D005; the current `separation_not_proven` is not upgraded to a split. |

## 4. P2 assessment

### 4.1. Is jurisdiction an independent hard ground?

**Recommended: yes, under the strict functional definition below.** The reason: a cell must have one system of final territorial responsibility for ordinary admission, regardless of today's coincidence of visa policy. This is the normative homogeneity of an additional dimension. It is consistent with the direction of R011/D025, but is not logically derived from P1 and is not considered an already finally accepted formalisation of R011.

Arguments for: the same requirements may be in effect in different independent competences; one side has no right to take an admission decision for the other. A common visa or mutual recognition of leave does not destroy the reserved territorial competence. The rule survives the unification of passport requirements and a change of the servicing office. The criterion can be checked from the allocation of powers without a country/recognition label.

Arguments against: this adds a boundary that the current traveller outcome may not require; institutional structure is harder to document than a visa requirement. The notion "final" wrongly pulls either towards the last officer or towards the supreme legislator/court. Federal, shared and extraterritorial arrangements may have several roles and a common apex. If the model values exclusively the current outputs, this additional split is redundant; a promise of possible future policy divergence does not prove a current necessity. Therefore the usefulness of P2 is a chosen invariant of responsibility, not a statement about an inevitable future difference.

### 4.2. Operational definition: independent_final_admission_jurisdiction

Define `admission_competence` as a **legal capacity**, not the name of a body, an officer, a visa issuer, a sovereign or an administrative unit. One person/body may act in two capacities; many offices may exercise one capacity. "Legal" here means a documented norm of the applicable operational legal order; it is not a statement of the internationally recognised sovereignty of that order.

For a scope X a dossier with six positively proven premises (J1–J6) is required:

1. **J1 — Constitutive allocation.** A law, treaty, order or other normative instrument in effect allocates ordinary civilian admission/refusal and the right to condition or terminate stay for X. The clauses, capacity, holder and chain of powers are stated. A permit issuer, a staffing structure and border guarding do not prove this separately.
2. **J2 — Territorial legal effect.** A decision taken in this capacity creates/terminates a permission or denial of entry/stay with its own described geographical scope. The scope is not limited to the working district of an office, to port servicing or to an activity/visit to an object. Separate national admission titles may have a common layer of recognition; all their effects must be described.
3. **J3 — Reserved ordinary competence.** In the scheme in effect this capacity can finally accept or refuse in at least one nonempty class-based ordinary civilian admission/stay matter for X without the necessary individual assent of another admission capacity. A legal mechanism of territorial refusal/termination of stay must exist. Unlimited discretionary freedom or a separate legislative power is not required; mandatory rights of travellers and a common policy law are compatible with competence.
4. **J4 — Non-substitution.** An admission/leave granted by another capacity for its territory does not by itself give it the power to take a decision for X or to cancel a reserved territorial refusal of X. Both the exceptions and the recognition arrangements are documented. If an ordinary superior can take/replace this decision as part of a single admission administration and a single admission title, the subordinate offices are one jurisdiction. If a common body acts in a separate capacity of X, this is not a decision of capacity B for X.
5. **J5 — Attribution, delegation and review closure.** The full relevant chain `acts_for`, `case_substitution`, `required_assent`, `judicial_review`, `recognises_leave` is normalised. Delegation of **execution** does not create a new capacity. The legislative establishment of a separate territorial competence can create one: the possibility of a future repeal of the constitutive law is not equal to the right of a superior to replace a specific decision under the law in effect. Judicial review of legality, a common constitutional apex and treaty constraints do not by themselves unite capacities. An unresolved overlap of powers is unknown, not "two countries". The absence of delegation/substitution is proven by a positive allocation/override audit, not by the absence of search results.
6. **J6 — Effective territorial application.** At t the entry into force of the allocation and its application to X are established. For a de facto arrangement independent observations of ordinary civilian admission/enforcement, consistent with the published scheme, are needed in addition. A claimant's self-description alone or a map of military positions is not enough. The holder or a separate office is not obliged to be physically located in X.

`J(X,C,t)` is the canonicalised structure of the applicable capacities and veto/assent relations for C after execution is collapsed into `acts_for`. It may be a joint structure; an unsorted list of names of bodies is not a signature. Different members of one joint arrangement do not each receive a territory. `J(A) != J(B)` is proven if there is a capacity satisfying J1–J6 that has an independent territorial legal effect/reserved competence on one side and provably does not have the corresponding competence on the other, or if the proven structure of mandatory assent differs. A common structure rewritten with new IDs must be isomorphic to the old one.

The final predicate `J(A,B,t)` requires evidence-backed different normalised competence structures, one traveller scope/time and compatible scopes A/B. The names/numbers of normative acts serve as locators, not as values for comparison: two documents may establish one competence. A real case of different outcomes is not required: that would be a return to P1. Independence from every parent sovereign is not required: that would exclude part of the dependencies by the structure of supreme power.

J1–J6 are proven for the separating competence that is used and for all relations able to change its independence/scope. It is not required to complete every extraneous dimension before accepting such a certificate. But `hard_compatible` needs a full coverage audit of both competence structures: the insufficiency of a proof of difference is not a proof of the same competence.

This is a maximally strict **sufficient** test, not one promised to be universally complete. An undescribed shared arrangement may remain unknown; the absence of an own veto does not prove full equality of all the other hard dimensions. Machine evaluation is possible after normalisation of the legal premises; the review does not claim that natural-language law turns into J1–J6 automatically and without interpretation. The dossier must allow an independent verifier to reproduce each normalisation.

### 4.3. Check of the criteria and of the current evidence

| Criterion | Assessment of strict P2 |
|---|---|
| Operational definability | Passes conditionally with J1–J6 and the graph of capacities. A bare `authority_a != authority_b` fails the test. |
| External verifiability | Verifiable in principle; allocation, delegation, override and effect clauses are needed, not only visitor guidance. An incomplete dossier remains unknown. |
| Name blindness | Passes when relations/capacities are compared and renaming is consistent. A country-type lookup is forbidden. |
| Temporal stability | More robust to policy coincidence and office reorganisation than P1; a real transfer of competence changes J. No guarantee of "a boundary forever". |
| Universality | One test for all arrangements, including an independent subnational admission competence; such a province is a split precisely by competence. Joint cases may be unresolved. |
| Political bias | Reduced by role-based evidence and the absence of a recognition gate; the risks of source selection and of interpretation of the applicable order remain. A controlling authority must not be considered automatically the lawful sovereign. |
| Over-splitting | High for office-based P2; J2/J4/J5 block an office/delegation split. Preserving different capacities with equal policy is an intentional additional split. |
| Under-splitting | Will not preserve a dependency/legal-status boundary under a common competence and equal D. The high evidence bar increases unknown; this is not a proven merge. |
| Independence from current visa coincidence | Passes: identical tables, a common visa issuer and mutual recognition of permissions do not replace the analysis of reserved competence. |

The current P2 certificates C001 (E02/E03), C008 (E18), C009 (E18/E21), C012 (E23) were accepted **by the old contract**. E18 contains a direct statement of own jurisdictions; E20 for C007 contains more specific statutory powers. But short records do not automatically give a full J1–J6 dossier. In particular, E23 "local officers issue the permit" does not by itself prove non-substitution; E02/E03 "national border authorities" does not document the whole override chain. The new candidate will require a premise audit of all such certificates, without changing the factual truth/status of these records. In this review there is **no new recomputation and no promise to keep the number 8**.

Counterexamples: two regional offices of one national service with a common admission title are not J; a common visa-processing contractor of two provably independent capacities is not a ground to consider them one; one global apex court does not make all the admission capacities under it the same; enforcement by a different patrol proves neither J3 nor J4.

## 5. P3 assessment

**P3 in its current form is unfit for production Stage 1.** `territorial/legal identity` has no general machine predicate, and adding the names of territories would only hide the under-definition. The 41 `model_unresolved` are a correct refusal of the evaluator to guess this predicate, not 41 proven independent territories.

| Attempted definition | Why it does not satisfy the whole set of requirements |
|---|---|
| Own legal personality / separate constitutional entity | A precisely formalised legal personality covers municipalities and other public bodies; a general "special constitutional position" does not determine admission significance. Adding "sufficiently external" brings back an unknown predicate. |
| ISO code / dependency / autonomy / dispute | Machine-convenient, but these are forbidden proxies. A classifier code does not prove a hard travel difference; a single label gives a blanket category split. |
| Separate legal system / own legislation | Ordinary provinces also have general law differences. A restriction to admission law specifically either leads to P1/J or leaves a non-travel-related hard rule that must be justified separately. |
| International status from an external list | May be a reproducible **registry-relative** rule, but requires a normative choice of the registry, competence, coverage and scope. The UN decolonization list is not a general definition of all dependencies/disputes/occupation cases. An external curated list does not become non-curated because another organisation maintains it. |
| Stable separate admission institutions | Has operational meaning after J1–J6; this is P2, it adds no separate P3 dimension. |
| Historically separate / important / recognisable territory | No machine semantics; the choice of well-known examples becomes a hidden oracle. Destination identity belongs to another stage. |

It cannot be proven that **any future** legal-status rule is impossible. A narrower conclusion can be drawn: an available general definition that simultaneously meets all the stated conditions and adds an independent ground to W/J does not exist now. An exact legal predicate with a stated competent act and consequences can be proposed in Q006; its adoption will be a new normative decision, not a decoding of the word identity.

A typical failure mode: choose politically prominent places → pick heterogeneous labels for them → call the union of the labels territorial identity → fix the expected outcomes. Blind IDs at the last step will not correct this: the curated selection is already built into the extraction/registry. With full equality of the admissible inputs any deterministic name-blind rule is obliged to return the same result. Therefore requirements to preserve separateness **without W/J** cannot be satisfied by a hidden P3. Recommendation: do not include undefined identity in the new core; keep P3 as an archived experimental hypothesis. The existing P3 evaluator remains unchanged.

## 6. Accepted-constraint regression analysis

Accepted constraints remain requirements for regression. They are not source facts and not `must_separate` derivations by themselves. "Not disappear" has to be distinguished as preservation of information in legal/control objects, as a distinction in the final partition and as a mandatory Stage 1 boundary. The first does not guarantee the second, the second does not necessarily require the third. A transfer to Stage 2 is possible only as a localisation of a final-output requirement; it is not promised here that a future Stage 2 will meet it.

| Constraint and evidence | Explained by P1? | Explained by P2? | Is P3 or another mechanism needed? | Regression verdict |
|---|---|---|---|---|
| D005: Réunion / metropolitan France; C018, E26/E27 | Yes as a mechanism: applicable destination visa/document difference. The snapshot has no complete verified C, current P1 = `separation_not_proven`. | P2 includes the same W; an own independent jurisdiction is not proven and is not needed given W. | P3 is not needed. Neither the overseas label nor the VAT exclusion replaces an admission witness. | Explainable by a general rule, the application is still conditional on data. Separateness from the metropole does not mean one whole final region or separateness from all overseas parts. |
| D004: British Overseas Territories / ordinary UK; C010–C012 | May explain specific cases; the Bermuda nationality witness and the Gibraltar comparison are not completed in the snapshot. W does not follow from the UKOT category. | C012/Falklands has a current P2 split; strict J requires an audit of E23. For C010/C011 the final competence is unknown; offices and checks do not prove independence. | A blanket "every UKOT is separate" is not derived. Undefined P3 does not solve the problem; other general hard rules are not yet defined. | The requirement is covered only partially. D004 cannot be declared met on the basis of three cases or of the Crown Dependencies (C007–C009 are a different class). If the complete W/J signatures of a UKOT are equal to those of the UK, mandatory Stage 1 separateness conflicts with the core. |
| D007: Western Sahara / ordinary Morocco; the key pair C031 west / Morocco | E39 establishes only the coincidence of one passport rule, E40 — qualified access limitations without a sufficient witness. Neither a split nor full equality is proven. | Final jurisdiction unknown; coarse Moroccan administration proves neither J equality nor difference. The west/east contrast does not carry over to west/Morocco. | The requirement to separate west even under equal W/J needs a new explicit legal-status rule (Q006) or a change of the requirement; the current P3 is unfit. | The main unresolved conceptual conflict: the core **does not guarantee** D007. Preserving a dispute overlay does not fulfil the requirement of a separate final region. It must not be silently declared resolved by Stage 2. |
| D006: Crimea / ordinary Ukraine; D013 and T059 separately from the Q001 facts | If a difference of applicable civilian admission/legal routes in exact scopes is proven, W explains the requirement. There are no such facts in Q001. | If different operative admission capacities are proven, J explains the boundary independently of recognition. A separate "Crimean" capacity is not needed: the capacities actually applicable on both sides are compared. | P3 is not logically required for the original D006. The distinction from ordinary Russia is the stronger **tentative D013**, not part of the accepted D006. | An explainable operational mechanism; factual validation is absent. Do not derive current geometry or "Crimea = exactly one cell" from the accepted assertion. |

An additional D004/D016 conflict already exists in the decisions: a literal separate British Antarctic claim sector, overlapping claims and the proposal of one Antarctic cell cannot all be accepted at once as ready canonical polygons. Neither "one treaty" nor "UKOT" proves an admission boundary. The review does not accept D016 as an exception and does not choose an Antarctic partition; this conflict remains Q011 together with the corresponding Q003/Q005.

The strict formulation of the conflict with the objective model: **if** the complete hard decision functions and competence structures of A/B are equal, the coarsest Stage 1 under the core has no ground to separate A/B. A requirement of a mandatory Stage 1 boundary in the same case is incompatible with the core. In the current data equality is not proven, therefore this is a conflict of the normative guarantee, not an already established factual `rule_conflict`. If D004/D007 are read only as final-output constraints, their fulfilment remains undemonstrated; they do not automatically become hard rules and are not considered lifted.

## 7. Disputed-territory analysis

### 7.1. Separate types and admissible consequences

| Type of fact | What it establishes | Admissible Stage 1 consequence |
|---|---|---|
| Claim | The position of an actor regarding a territory. | By itself no split; does not assign a controller, applicable law or geometry. |
| Recognition | The position of a third party on status/authority. | By itself no split; a change in the number of recognisers under the former W/J changes nothing. |
| International legal status | An attributed legal qualification by a competent instrument/body with its own scope. | Stored independently of claims; in the core the label itself is insufficient. A proven traveller legal consequence may give W. A status-only separator requires a separate norm of Q006. |
| De facto civil control | Who actually administers certain civil functions, where and when. | Evidence for effective application and investigation of admission/access. A difference of civil administrator is by itself not yet J or W. |
| Military control | Positions, use of force, military holding/restriction. | By itself not a civilian admission jurisdiction. A proven territorial civilian prohibition may give W after the scope/time gates; a patrol or a mine hazard does not give it automatically. |
| Admission authority | Who takes the territorial admission/stay decision, and in which capacity. | J under J1–J6; W under a difference of conditions. Distinguish issuer, officer, capacity and enforcement. |
| Civilian route/access regime | The conditions of lawful or actually enforced civilian entry/presence for the given C/route. | W, if it is an accepted hard territorial dimension and both sides and validity are proven. The absence of a flight/road or an advisory is not W. |

The hypothesis that `disputed=true` by itself **is not** a Mandatory Separation rule is supported. It is necessary for claim blindness: a new claim without an operational/legal-travel change must not create a boundary. International legal status is not equated with an arbitrary claim, but an automatic hard effect does not follow from this difference either.

The alternative "stable distinct actual control / applicable admission / civilian legal-access system is sufficient" requires decomposition. A difference of admission/legal-access with a proven territorial effect is sufficient as W. A different institutional civilian admission competence is sufficient as J, including confirmed de facto arrangements. **A difference of actual controller without one of these consequences is insufficient**: otherwise a municipal change of administration, a military sector or different police forces become a new hard dimension by an implicit rule.

The broad `legality_under(each relevant jurisdiction)` has a separate danger: the word relevant may mean "everyone who has made a claim". Then a declared claimant prohibition imperceptibly turns claims into separators. For the proposed core, take legal obligations whose applicability to C is confirmed independently of the disputed claim: the operational territorial admission law in effect, or a documented personal/document jurisdiction with a direct trip rule. Store `issuer/capacity`, applicability basis, legal consequence and factual enforcement separately. If the ground of applicability to C or to the disputed territory itself requires an unresolved choice of legal authority, this is Q006/model-unresolved, not an invented universal legality. A claim without such a norm changes nothing; a new actually applicable traveller obligation may change W even under the former control. A general economic agreement/sanctions label without a scoped civilian consequence is insufficient.

### 7.2. Cases of the material already present

| Case | What is actually in the snapshot | Admissible general mechanism and remaining gap |
|---|---|---|
| Western Sahara west / Morocco, C031 | E36 qualified UN-status record; E37 coarse administration with observation 2025-09-30; E39 a common bounded British-passport rule; E40 qualified access limitations. | W is possible given a concrete territorial legal/access witness; J — given a different competence. Neither is proven. If both turn out equal, the separateness of west requires a status-only decision on Q006; the internal west/east boundary does not solve the problem. |
| Western Sahara west / east/south, C032 | E37/E38 civil/military observations; the restrictions on MINURSO are not tourist admission; east civilian routes/admission unknown. Current P1/P2 `data_unknown`. | Different ordinary civilian admission systems could give W/J. `distinct_operational_control=true` in the comparison is insufficient. Do not derive exactly two cells, the current exact Berm line or an east immigration authority from military observations. |
| Western Sahara status object / zones / Berm, C033–C035 | `ws` is an international-status object; the zones/overlay may overlap. E41 establishes a mine/military hazard, not a legal polygon. | Not ordinary disjoint endpoints for `must_separate`. Operational scopes and typed overlays are needed; a status object is not placed in a partition next to its own parts. |
| Crimea / ordinary Ukraine | Only the accepted D006, the tentative explanation D013 and an unverified adversarial assertion; a Q001 dossier is absent. | Conditional W/J makes it possible to explain the original constraint without a recognition rule. Current control or a legal route is not asserted here. The application gap is facts and scope/time. |
| Crimea / ordinary Russia | The stronger tentative D013, without a Q001 factual comparison. | Control different from ordinary Ukraine logically says nothing about a difference from Russia. Its own W/J certificate is needed; if they are equal, the same status-only Q006 gap remains as for west/Morocco. The compared side must not be substituted. |
| Aksai Chin / China, C040 | E50 — historical control/claim description 2023-08; E09 — a general non-open-area permit norm without a list covering Aksai Chin; civilian routes/admission/current geometry unknown. | A proven ordinary territorial civilian prohibition/permit could give W; a military controller different from the claimant does not explain a split from the same controlling system. Neither a claim, nor the word restricted, nor unknown access permits creating a separate cell. If W/J are equal, the remainder is Q006. |
| Jammu and Kashmir / India, C036; Ladakh / India, C037 | E07/E08 — protected-area schedule; E49 qualified curfews/advice; E43 existing partial PAP and a **proposal** of an all-UT PAP. | A proven permit effect relates to its legal scope, not to the whole administrative area. A proposal does not become a W in effect; a local curfew requires the Q008/Q009 gates. No blanket dispute split. |
| Gilgit-Baltistan / Pakistan, C038; AJK / Pakistan, C039; AJK / GB, C048 | E45/E46 qualified registration/district permissions; E47 historical 2019 waiver; E53 provisional administrative-side observations. | A comparable territorial entry/presence permission may give W; a trekking activity permit by itself does not. Current effective scope/authority is needed, not a substitution of the 2019 NOC for today's equivalence. J is not yet established. |
| Tibet / China, C041 | E48 verified permit/organised-tour requirement; the ordinary baseline witness is not completed. | Check the legal territorial presence effect and the ordinary baseline for W; the organised-tour condition is separate from a ticket/activity permit. Autonomy does not prove J; identity does not complete the missing baseline. |
| Arunachal Pradesh / India reference, C042 | E07/E08/E44 give the current evaluator PAP certificate; the E50 control/claim record is historical and is not needed by this witness. | W uses the territorial permit mechanism; claim blindness is checked by removing E50/claim labels while keeping E07/E08/E44. The scope of the certificate is ordinary reference vs PAP scope, not India as a whole. |
| Siachen / Ladakh, C043 | E54 qualified **base camp** publication 2023; E55 military presence report 2024; glacier access/geometry unknown. | The base camp is not equal to the glacier; a unit military presence is not J. Q007/Q005/Q008 are retained, the absence of civilian access is not equated with a proven territorial legal prohibition. |
| Shaksgam / Aksai Chin, C044; Shaksgam / GB, C045 | E51 — verified **claim statement**; E52 qualified control description; E50 historical and E53 provisional. | A verified statement about a claim is not verified sovereignty or civilian competence. A difference of the compared control sides does not replace an admission dossier. W/J are not proven; identity does not close the law/access and geometry gaps. |
| LoC/LAC affected areas, C046/C047/C049 | Reference scopes and overlays are mixed; there is no single proven civilian regime of the whole strip. | Use the scope of the specific permit/prohibition/competence; not a claim line or a blanket boundary-zone identity. Military and administrative maps do not give a legal access effect automatically. |

For Western Sahara the routes are already separated in the [route-matrix](route-matrix.json). The E42 Morocco–Algeria closure does not carry over to Algeria→east/south, Mauritania→east/south or west→east. `no ordinary route established` is an unknown, not `all civilian access prohibited`. Neither a planned road, nor an entry stamp, nor an advisory buffer establishes a new admission jurisdiction.

Thus, additional geographic facts could unblock W/J in individual cases. They **do not answer** the remaining normative question: is it required to preserve international-legal separateness under full operational equivalence. This is the exact subject of Q006, not a reason to search endlessly for one more travel witness for an expected name.

## 8. Candidate Stage 1 rule set

### 8.1. One minimal recommended core

```text
candidate_core_v1 := CR-W OR CR-J

CR-W := proven hard territorial TravelDecision discontinuity
CR-J := proven independent final territorial admission competence difference
```

`OR` means the sufficiency of one certificate, not the necessity of both. This is a **candidate P2 with stricter gates**, not identical to the existing P2 implementation. Neither `territorial_identity`, nor `disputed`, nor a bare `controller_id` enters the core signature. The proposed `CR-C` control-only separator is not included: qualifying access consequences belong to CR-W, qualifying admission institutions — to CR-J; an independent remainder is not defined.

### 8.2. Common scope, evidence and temporal gates

**G-SCOPE.** The certificate contains nonempty disjoint scopes A/B, or two disjoint fragments inside the original reference objects. The stated decisions/competence are homogeneous on each certified fragment. A witness between two points does not prove that no points of two large heterogeneous objects can be in one cell. R008 cannot be literally applied to overlapping A/B: a point of their intersection cannot be separated from itself. An administrative polygon is admissible only as an evidence-backed exact scope/proxy with a stated precision. Unknown geometry is not drawn in; a partial certificate is not passed off as a full partition.

**G-CONTEXT.** The version of S keeps civilian short-stay, rare documents and class-based special permissions; it excludes work/settlement/diplomatic/military missions from the primary split. The scope must not be changed separately for a specific pair. The conditions of C and the policy exceptions are explicitly checked; there is no selection by frequency, by the name of a person or by desired destination.

**G-HARD.** The core includes the following decision outputs when they have the legal effect of the territorial admission/stay of a person: accepted travel document; visa/ETA/territorial admission authorisation requirement and validity; eligibility/prohibition of entry; general conditions/duration/termination of civilian stay; permit to enter/be present in a territorial scope; class-based legal entry/exit-route obligation. Names of documents, officer labels, stamps and office logistics are not outputs. A physical border procedure is not by itself hard; a normative obligation affecting territorial admission may be hard.

A territorial presence permit is defined through the **object of the regulated act**: the rule forbids entry/presence to the corresponding class of persons in the described scope as such. A site/activity permit regulates the use of an object, facility, service or activity and does not by itself change the territorial admission/stay title. The issuer may be common; a permit boundary may lie inside a province. **Neither size nor coverage of a whole administrative unit is proof.** For border parks/reserves/base/exclusion zones where the text equally admits both interpretations there is no automatic answer: dependency `Q005/Q009`, `model_unresolved`. This is an intentionally narrow sufficient core, not a claim to have closed the whole region/overlay boundary. Customs/biosecurity/fiscal differences separately remain Q004.

**G-TIME.** The proposed sufficient stability test: a constitutive/standing instrument is in effect at t, regulates repeatable classes of admissions/presence and is not activated exclusively by a specific incident/emergency/event order. "Standing" does not mean older than N days or without expiry: a new jurisdiction that has entered into force qualifies at once, a normative sunset clause does not by itself exclude being in effect. A one-day closure because of an event, a single patrol, a temporary quarantine order or a weather hazard are kept as overlays in this candidate. A prolonged emergency measure does not become standing because of the days it has lasted. If it is impossible to prove the type of the measure, or there are only de facto observations without an institutional rule, candidate stability is not established; Q008/Q007. This is a new proposed convention of institutional kind, not a proven complete theory of stability. It may leave long severe restrictions as overlays — the explicit price of a narrow core.

**G-EVIDENCE.** Each premise needs a source record, a locator/excerpt, the competence of the source for precisely this premise, as-of/validity, geographic scope and a sufficient assessment. Guidance, claim statement, historical observation and constitutional law are not interchangeable. The verification "the source said X" does not prove a stronger Y. A source conflict is kept as a data blocker. Evidence-backed derivations are admitted with published steps; the creation of a new empirical record is not required in this review and is not performed.

### 8.3. Separators and intentional limits

| ID | Operational predicate | Evidence requirements | Why hard | Counterexamples / intentionally does not separate |
|---|---|---|---|---|
| CR-W | G-SCOPE/G-CONTEXT/G-HARD/G-TIME/G-EVIDENCE are met; there exists one admissible matched C and a hard d with provably different D on A/B. | The applicable norms of both sides, a nonempty context, all influencing exemptions, the specific differing output, territorial effect, standing basis/time and scope certificate. | One hard decision function cannot correctly describe both sides. | Coincidence of D under different names of bodies; different queues/ports/carriers without a territorial legal effect; named individual decisions; closed-by-weather; undefined permit overlays; status-only difference. |
| CR-J | The common applicable gates and J1–J6; the normalised final admission competence structures on A/B provably differ in one S/t. | Constitutive allocation, territorial legal effects, reserved decision powers, non-substitution/override audit, attribution/delegation/review graph, effective application; for de facto — civilian operational corroboration. | The accepted candidate invariant: one cell does not hide two independent systems of final territorial admission responsibility. | Several local offices, a common visa contractor, stamps, administrative autonomy without competence; different legal-status labels with one competence; military-only control. |

CR-W and CR-J are two separate sufficient ways of proof: one competence may introduce different territorial document rules (W without J); on the assumption of complete equal D, different independent capacities give only J. Their actual irreducible independence for the final S/H is **not proven** by the current set. If S/H includes all territorially specific leave/refusal histories and permissions, a constitutive difference sometimes makes it possible to derive W; such a case does not prove additional coverage by P2. If, however, `HardTravelDecision` directly includes the identity of the decision-maker, J can be written inside one formula, but the normative addition of an institutional dimension does not disappear because of that.

Therefore "minimal" here means two explicitly justified certificate types without a third undefined identity/control ground. It is not a theorem about the minimal number of independent axioms under any future traveller scope. To assert the strict extra expressiveness of P2, the synthetic "complete equal D, different J" must be reconciled with the exact S/H; D equality cannot be postulated while ignoring the legal-travel witness that follows from J.

### 8.4. Equality, unknown and construction

The complete candidate signature is `Sigma(X) = (D_X over S/H, J_X over S)`, together with proven scope/time applicability and completeness. Two signatures are equal only after a positive coverage audit of all included dimensions and competence relations; identical policy IDs are sufficient only given proven common applicability and the absence of different exceptions. It is not required to enumerate people endlessly: the common applicability of one normative set and the coverage of its predicates can be proven. Several coinciding witnesses or an empty list of permits do not give such a proof.

The absence of a CR-W/CR-J certificate creates neither a boundary nor compatibility. The order of the contract is kept: normative conflict → sufficient split → consequential model blocker → concrete data blocker → complete equal signature → separation not proven. The uncertainty of another factor does not cancel a ready split. The rejected identity/control-only predicates are excluded from the new core, therefore they do not by themselves block its equality; an unresolved classification of a potentially hard permission or of legitimacy/applicability still blocks. Compatibility is always marked with the candidate profile/version and is not passed off as the fulfilment of D004/D007 or of a broader future Stage 1.

Even a correct pairwise separator does not yet define the coarsest partition under incompleteness: if only A≠B is proven and the relations of C are unknown, both `{A,C}|{B}` and `{A}|{B,C}` are compatible. One must not be chosen by name, nor the connected components of the "no prohibition" graph be considered equality classes. Complete function/structure equality is transitive; `separation_not_proven` is not. Therefore the review does not build a partition and does not promise a complete release from the current 147 results.

### 8.5. Invariant audit

| Invariant | Check of the candidate | Result / limit |
|---|---|---|
| Name blindness | Germany→A, France→B; rename the authority IDs and clauses references consistently, keep the allocation and D. | Outcome unchanged; hard IDs must not encode curated inclusion. |
| Claim blindness | Add/remove claim and recognition labels under the former independently applicable D/J. | Outcome unchanged. A new proven legal obligation is a change of D, not a pure change of claim. |
| No destination leakage | Madeira gains tourist renown under the former D/J. | There is no new Stage 1 certificate; the final classification is not determined. |
| No island rule | Make an equal-signature scope an island/archipelago without other changes. | There is no new certificate; MultiPolygon is admissible on hard dimensions. |
| No administrative-boundary rule | Bavaria/Tuscany/an ordinary province receives a new administrative label or office. | There is no new certificate. A proven own final admission competence gives J by the same test as everywhere. |
| Open world | Remove the evidence of one mandatory premise or replace the equality audit with a sample. | Automatically neither split nor equality; the corresponding blocker/incomplete signature. |
| Monotonicity | Any later subdivision crosses a proven Stage 1 certificate. | Such a Stage 2 output is inadmissible; every cell must lie in one Stage 1 cell. Changes between temporal releases are considered separately. |

This is a logical audit of the proposed predicates, not a run of a new evaluator. The existing implementation and fixtures were not changed.

## 9. Counterexamples and failure modes

| Failure mode | Counterexample | Required behaviour |
|---|---|---|
| "Only the office differs" | Two offices have different chiefs and statutory service districts, but the same admission title; the director can allocate and replace cases. | J4/J5 are not met; no CR-J. Do not consider a geographic office jurisdiction an independent territorial admission. |
| "The parent may some day repeal the law" | A constitutive instrument gives X its own capacity; the parent legislature may change the instrument, but the law in effect does not give capacity B the power to decide for X. | Do not reject J because of ultimate sovereignty. Competence is checked under the instrument **in effect**. |
| "A common minister/visa issuer is one jurisdiction" | One minister acts in two separate capacities or an external contractor serves them. | Analyse attribution, territorial effect and substitution; person/issuer equality is insufficient. |
| "A coordinated visa policy is one competence" | The complete D are equal, but two reserved capacities cannot take a decision for each other. | CR-J gives a split; this is exactly the additional normative choice of P2. |
| "The permit covers the province as a whole" | The same rules first cover half of a province, then the province is renamed/redrawn so that the permit scope coincides with it. | A change of administrative coincidence does not change the hard effect; the gate looks at the regulated act/scope. Otherwise C042 turns into a curated administrative rule. |
| "Any permit is territorial" | A mandatory permit for the use of a landing facility, for trekking or for a visit to a park. | The fact of a permit is by itself not a split. A site/activity effect is excluded; an ambiguous presence prohibition leaves Q005/Q009, with no guess by name/size. |
| "A rare document does not count" | The only actually used document of the class has a provably different territorial acceptance rule. | Given an admissible S and the other gates W still applies. Removing it by frequency is forbidden. |
| "Two officers refused differently" | One and the same norm admits discretion; different events give different outcomes. | Outcome events are not different policy functions. A proven difference in legal requirements/permissions is needed. |
| "No civilian routes — everything is closed" | The route has not been studied or the road is absent. | Unknown/transport facts do not become a legal prohibition; closed points remain in U. |
| "Stability = a long time" | A new standing admission capacity exists for one day; an emergency restriction lasts for years. | The first may pass G-TIME at once; the second does not pass merely because of age. This is a published candidate convention, not a universal resolution of Q008. |
| "A control boundary preserves the whole dispute" | X and Y inside a status object have different regimes; X and the ordinary territory Z of the same controller may have the same W/J. | X/Y separation does not prove X/Z. The Q006 remainder is not eliminated by the number of internal splits. |
| "Courts or recognition decide everything" | Two capacities have a common court; or a de facto authority is not recognised by third parties. | A common court is not equality; recognition count is not a gate. An unknown effective admission competence remains unknown. |
| "Verified evidence proves the whole conclusion" | E23 confirms permit issuance, E51 — that the claimant made a statement. | Do not upgrade them to non-substitution or internationally valid sovereignty. Premise-level proof is separate from source reliability. |
| "No boundary was found — they can be merged" | There is only a finite sample of common visa rules. | Signature incomplete; not `hard_compatible`. A proven difference is not transitive, an unproven difference is likewise not equality. |
| "An aggregate can be compared with its own part" | C033/C034 or the literal whole-India / Arunachal. | A disjoint scoped certificate is needed; do not allow impossible self-separation. A pairwise result is not yet a geometry instruction. |

### Minimal distinguishing experiment without new geographic facts

The next step is a **synthetic normative contract experiment**, described in the YAML as `normative_experiments`. It does not change the current fixtures and does not use real expected regions as an oracle. Two base record bundles have the same complete D function; only the attribution/competence structure changes:

Preliminary gate: check the logical compatibility of the premises of each bundle with the exact S/H, including the validity of another's leave, local refusal histories and recognition arrangements. If the stated J difference itself entails a difference of an included D, the bundle is not an equal-D counterexample and must be rejected as inconsistent, not counted in favour of P2. The expected values below are conditional on this gate; this is not a statement that a corresponding real pair exists.

1. **NX-01: independent capacities.** Two constitutive territorial titles, reserved powers, no ordinary cross-capacity substitution, effective scopes. P1 under positively complete D equality gives compatibility; the proposed core gives CR-J. This case isolates the normative usefulness of jurisdiction without a search for a rare visa witness.
2. **NX-02: offices.** Everything is the same at the level of staff/location, but there is one territorial title and a single substitutable administrative chain. The core does not give J; under full equality of the other dimensions — compatibility. The difference between NX-01/NX-02 must be explained by J1–J6, not by the labels "country/province".
3. **NX-03/NX-04: coincidence versus independence.** A common capacity with different standing visa rules gives W; different capacities with equal rules give J even with a common apex court/visa processor. This checks the minimality of both grounds.
4. **NX-05/NX-06: status/control only.** Under full equality of D/J the legal-status/claim labels change, or only the military patrol actor does. The core is compatible; no W/J. If a mandatory split is required, a separate rule and its general proof obligations must be named. The old accepted answer is not added as a derivation.
5. **NX-07/NX-08: evidence and permits.** Removing the J4 evidence leaves data unknown; a permit with unresolved territorial/site semantics leaves model unresolved. This checks that the strict predicate is not filled in by intuition.
6. **NX-09/NX-10: rarity and time.** A class-based rare document with a standing territorial difference gives W; a temporary event closure under otherwise complete equal core dimensions does not give a core split. The homogeneity requirements and the temporal convention become separately verifiable.

For each bundle repeat the bijective renaming of all territory/authority IDs, the permutation of the records and the A/B swap. All expected results are derived from the published candidate predicates; real constraints are used only for the coverage/conflict report. Acceptance criterion: precisely the institutional invariant of NX-01 is accepted or rejected; each of NX-02/NX-04 is explained by one J-definition; it is explicitly accepted that NX-05/NX-06 does not give a hard split without an additional rule. In a dispute about the extraction of J1–J6 the minimal additional action is a premise matrix over the **existing** E02/E03/E18/E20/E21/E23 with `entailed / not_entailed / unknown`, without new geographical research and without a requirement to keep the old counts.

This experiment cannot empirically prove that the product *ought* to like NX-01. It makes the normative choice concrete and checks the internal consistency that an increase in the number of geographic cases will not provide.

## 10. Q001 disposition

**B — Q001 can be narrowed.** The recommended decision for subsequent normative approval:

> Stage 1 requires separation given sufficient proof of a territorial hard TravelDecision discontinuity in the published civilian scope, or given sufficient proof of different independent final territorial admission competencies. Rare admissible classes are kept. Authority identity is established by legal capacity, territorial effect, reserved competence and non-substitution, with a separate proof of effective application. Undefined identity, dispute, dependency, autonomy and control labels are not additional hard dimensions.

| Part of the question | Result of the review | What remains |
|---|---|---|
| P1 as sufficient foundation | It is recommended to keep W and the existential witness; a frequency threshold is not needed. | Accept the exact S/H and the boundaries of territorial permits/routes, Q002/Q005/Q009; classify temporal measures, Q008. |
| P2 independent competence | A separate hard invariant J with J1–J6 is recommended; current visa equality does not hinder it. | Accept this normative choice; check the operational distinction on NX-01/NX-02 and the premise audit, do not declare the existing Boolean a full dossier. |
| P3 identity | Reject **in its current form** for production; do not replace with a registry/proxy. | Any future exact legal-status predicate must pass an independent justification and counterexamples, not supplement the vague P3. |
| Stable control | A bare controller difference is insufficient; W/J consequences are admissible without a recognition gate. | Shared/noninstitutional civilian control — Q007, stability — Q008, unresolved access classification — Q005/Q009. |
| Disputed-status preservation | Claim/dispute alone are rejected as a separator; D007 and the tentative D013 are not guaranteed under operational equality. | Q006: a separate legal-status hard rule or an explicit limitation of the guarantee; the D004 blanket and the Antarctic conflict are also Q011. |

**Why not A:** there is no consistent general way to guarantee the blanket D004/D007 and at the same time keep only W/J without exceptions; part of the hard/access/stability boundary still requires model semantics. The review proposes a strict sufficient core, but has not proven its completeness as the whole normative Stage 1. **Why not C:** the choice is substantially narrowed — vague identity and control-only do not receive production semantics, existential P1 is kept, P2 has a verifiable sufficient dossier, and the residual conflict is formulated on fully equal W/J inputs. "More data is needed" is not an answer to this conflict.

Status B here is a recommendation of the review. The [open questions](../../docs/open-questions.md), the normative spec, the decisions, the factual records and the current evaluator are not changed. Unfulfilled constraints are not closed automatically and are not transferred to Stage 2 on the promise of a future decision.

## 11. Required spec/decision changes

Below are concrete proposed patches for a separate approval stage; **they are not applied in this change**. The existing stable R/D IDs and the accepted user requirements are kept until the user explicitly changes them. New formalisations do not receive `accepted` merely because this review recommends them.

1. **R007/R012, Q002 — existential scope.** Clarify the text: "The certificate uses a nonempty consistent class-based civilian short-stay context, complete in the influencing predicates. The frequency of the class does not affect sufficiency. Defined hard requirements/permissions are compared, not individual discretionary events. The list of hard outputs, the excluded activity/site outputs and the version of the scope are published". Add a matched-route mapping and the rule that a refusal on one side is admissible as a witness outcome.
2. **R008/R009/R028/R038 — certificate scope.** Add: "The scope A/B of each separation certificate is nonempty and non-overlapping; the evidence proves the corresponding hard effect on the whole certified scope. Heterogeneous/reference/aggregate inputs require explicit fragments. One witness does not extend to the whole containing entity". Keep order independence, complete-signature equality and unresolved when there are several coarsest partitions. This is later contract/adapter work, not a patch of the implementation now.
3. **R011 — replace the brief independence with an operational definition.** Include J1–J6 from §4.2, the capacity/holder distinction, the normalized delegation/assent/review graph and a positive non-substitution audit. Explicitly exclude office, issuer, service district, patrol and merely legislative autonomy. State: "A common policy, recognition of leave, an apex court or ultimate parent legislative power do not by themselves establish equality of competence; attribution of the specific case powers is mandatory".
4. **R010/R038/R042, D010/D029, Q001.identity — take undefined P3 out of the proposed production core.** Text: "Territorial/legal identity does not enter the hard signature without a separately accepted operational rule. P3 is kept as an unresolved historical experimental profile; status-only hypotheses are considered in Q006. Registry/ISO/category flags do not replace a general predicate". Keep the accepted distinction of territorial/legal vs destination identity; do not touch the definition of Stage 2.
5. **R013/R014/R017/R027, Q004/Q005/Q009 — explicitly define the sufficient hard core and the unresolved edge.** Add the G-HARD regulated-act/territorial-effect gate: the port of processing is not equal to the scope of admission, a whole-province permit is not hard by administrative coincidence, site/activity outputs are excluded, an ambiguous territorial presence restriction gives a model blocker. Do not declare all parks overlays or all permits separators by name. Q004 remains a separate question.
6. **R015/R023/R024/R039, D008/D014, Q007 — control evidence.** Clarify: "A control observation is by itself not a hard separator; proven scoped admission/legal-access consequences under CR-W or effective independent admission competence under CR-J are sufficient. Civil, border, military and enforcement roles are separate; recognition is not a gate". If a third independent control predicate is needed, first define it beyond W/J and check the military/local-office counterexamples. Do not turn D014 into a requirement of exactly two cells.
7. **R016/R022/R024, D006/D007/D013, Q006 — status-only conflict.** Add an explicit regression matrix: D006 relates to the comparison with ordinary Ukraine; D013 with Russia is tentative; west/east does not prove west/Morocco. Proposed text of Q006: "Under complete equal W/J the core does not guarantee the separateness of a legal-status object. A separate general legal-status separator is required, or a change of the mandatory nature of this product constraint. Until a decision the constraint remains unclosed". Do not downgrade D007/D006 from accepted and do not consider a dispute overlay the fulfilment of the separate-region requirement.
8. **R018/R019/R026, D004/D016, Q011 — category guarantees.** Add: "Do not inherit metropolitan policy without evidence. An overseas/dependency label does not create a split. D004 blanket coverage is not proven by the core; Antarctic claims do not become cells from a category. D016 remains a proposal, not an accepted exception". Do not derive a conclusion for all UKOT from C012 or the Crown Dependencies.
9. **R031/R033, Q008 — candidate time convention.** Propose G-TIME as a sufficient standing/constitutive test without a duration/frequency threshold; incident measures remain overlays and do not become hard with age. Record the price of this choice for prolonged restrictions. Until adoption ambiguous temporal cases remain unresolved. Do not interpret R041 as a prohibition of a change of boundary between temporal releases.
10. **Q001, D020/D025 and evaluator-contract — disposition and version.** After adoption record Q001 as narrowed with the CR-W/CR-J core and the stated residual dependencies; the next experiment is NX-01–NX-10. The new profile/version must separate premise-level proof from current assertions. Do not retroactively change the spec version of the 147 results; any new certificates will require a new versioned derivation. `hard_compatible` remains a profile-relative positive Stage 1 outcome, not a final merge.

R003–R005, R040–R041 and D023–D028, in the part concerning the approved architecture, require no change. A new world partition, a Stage 2 implementation, new geographic facts, curated exceptions and automatic preservation of the old expected regions are not part of these patches.
