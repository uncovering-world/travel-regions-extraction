# Trying the procedure on the Denmark / Greenland dossier

14 September 2026. A demonstration for [#12](https://github.com/uncovering-world/travel-regions-extraction/issues/12) following the [draft procedure](protocol.md).

**Outcome: keep the package as `candidate`; do not issue a `verified` certificate.** This is an AI walkthrough of the completeness of the existing material, not an independent review of the legislation. No human reviewer is appointed and there is no signature. No new external sources were read for this walkthrough.

It is based on the local [dossier](../../experiments/source-pilot/cases/greenland.md) and the [in-depth audit of 13 September](../../experiments/source-pilot/audits/greenland-2026-09-13.md). What is said below about legislation reports the content of that research package; it does not claim a new check of the facts. The source files, observations and Q001 are unchanged.

## Subject of the intended review

| Field | Value and limit |
|---|---|
| Comparison | A research continuation of C017; not a transfer of its historical result. |
| Profile / traveller scope | `S1-core-v1` / `civilian-short-stay-v1`. |
| Class | `greenland-tourist-witness-v2` from the audit: an adult national of Bangladesh only, an ordinary passport, a suitable uniform multiple-entry type C visa, a seven-day tourist trip; the alternative documents and privileges listed in the audit are absent. Non-emptiness and completeness of the context are not yet proven. |
| A / B | European Denmark without Greenland and the Faroe Islands / Greenland. Textual research scopes; no certification claimed. |
| t | For the demonstration we propose 2026-09-13, the date of the original reading. This is an explicitly chosen date for the intended comparison, not the date the rules took effect and not proof of their applicability. |
| Dimension | `territorial_authorisation_validity`. |
| Candidate D(A) / D(B) | The package's assumption: the visa covers A and does not cover B. These are not `known_value` values for production and not a comparison of final border-officer decisions. |
| Review / signature | AI walkthrough; no human review. No certified manifest of the proof. |

## Walking through the conditions

| Condition | What the source package already has | Why full confirmation stops |
|---|---|---|
| G-SCOPE | The audit distinguishes European Denmark from Greenland and excludes comparing the whole kingdom with its part. | Verifiable fixing of non-emptiness, disjointness and the same visa effect within each scope is incomplete. The absence of a polygon is not by itself a reason to refuse. |
| G-CONTEXT | The class, visa type, trip length and excluded exemption grounds are refined; the C visa is separated from D visas and residence permits. | Recognition of the specific passport type, the feasibility of a suitable visa and all conditions of the logical trip are unchecked. The attribute "lawfully issued" does not replace proof that the class is non-empty. |
| G-HARD | The dossier ties the difference to the territorial effect of the document and to the right of entry and stay. | The mechanism looks suitable for the accepted dimension, but it is a research interpretation. The reviewer has not yet confirmed the whole legal chain and its applicability. The label "Greenland" certifies nothing by itself. |
| G-TIME | The audit cites the 2025 consolidation, the April 2026 guide and the updated web instructions. | The check of amendments and applicable exemptions at the chosen t is incomplete. Edition and reading dates do not fill validity automatically. |
| G-EVIDENCE | There are links, locators, short excerpts, a table of exception groups and explicit limitations. | Not all material versions are stored; the applicability of exceptions and both sides are not signed off by a human. Order no. 1545 was not retrieved and its relation to Greenland is not established. Unavailable text cannot be treated as read, or as a necessary basis in advance. |

For every gate the demonstration's outcome is: confirmation incomplete. This does not claim that a gate is refuted, and it is not an evaluator result.

## Two places where the procedure prevents a false promotion

**Quotation → stronger conclusion.** The audit quotes § 4 of the consolidation about a visa for "other foreigners". Such an excerpt does not prove that the chosen class falls under "other" at t: the exceptions, their legal basis and temporal applicability are needed. Even confirming that the quotation is accurate does not allow signing the whole D(B).

**Transferring exceptions between territories.** According to the audit, the ministry guide makes the application of its general sections in Greenland conditional on the same legal basis. The table of Danish exemptions therefore remains a checklist. If the origin of a rule is not established, that is `unknown`; if two applicable sources give incompatible answers, both are kept with `conflict`. This walkthrough does not claim an actual conflict between sources.

## Minimum sequence before a signature

1. Agree the responsibility and competence profile under #12; before a real review, record the reviewer and their confirmation of participation.
2. In separate, authorised evidence work, fix the package version, scopes and t; store the material sources and prove the chain of exemptions in force. Investigate the unavailable order only once its relevance is established.
3. Check the non-emptiness of the given class, the document and the route conditions; complete the exception matrix and the proof of both D. Do not extend the work to all nationalities of the world.
4. A human reads the sources and fills in the matrix of all gate components. Only then does the package become `reviewed`, possibly with a negative or incomplete outcome.
5. If all conditions are confirmed, sign the exact version and scope of the conclusion; then separately prepare and check a current-core input. If a gap remains, keep it and stop the promotion. The reference set belongs to #13 and is not created here.

## Checking the procedure's behaviour on control situations

This is a manual check of the proposal's logic, not new geographic claims and not automated code tests.

| Situation | Expected behaviour |
|---|---|
| All JSON fields filled by AI, no human read the sources | `candidate`; a schema PASS does not give `verified`. |
| A human confirmed a quotation, the applicability of exceptions remains unknown | The narrow quotation can be confirmed; the certificate is not promoted. A completed documented review may have the outcome "insufficient data". |
| Two genuinely applicable sources conflict | Keep both and the reason for the conflict; do not pick the majority or the convenient conclusion. |
| A source was retrieved today, the start of effect is not established | Do not substitute the retrieval date; G-TIME is not confirmed. |
| A package proved one admissible rare difference across all gates | No frequency threshold is needed; after a signed review, `verified` is possible. |
| The candidate is refuted or no evidence is found | Do not derive `hard_compatible`. |
| All sources read, but the permit/overlay semantics are undefined | Keep Q005/Q009 and `model_unresolved`; the reviewer's competence does not replace adopting a rule. |
| A translation error is found in a confirmed package | Record a withdrawal or replacement and the affected results; the new version goes through review, the earlier history is kept. |

This walkthrough shows that the procedure can record where confirmation stops. It does not prove the quality of a future human review and does not close the listed gaps of the source dossier.
