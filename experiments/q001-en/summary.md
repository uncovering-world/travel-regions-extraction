# Experiment Q001 — brief results

49 comparisons, 56 factual units, 55 atomic evidence records and 52 sources have been prepared; 12 comparisons are anonymised. Canonical regions are not assigned.

| Type of check | Useful cases | What exactly can be checked |
|---|---|---|
| Common visa policy, independent admission | UK / Guernsey; UK / Isle of Man | A potential divergence of P1 and P2: the jurisdiction is confirmed, but P1 is unknown, not proven false. |
| Ordinary neighbouring states | Germany / France | Different final authorities; LTV can break the assumption "Schengen means P1-equivalent". The legal witness is provisional for now. |
| A concrete visa/document difference | UK / Jersey; Aruba / Curaçao; Curaçao / Bonaire | Verifiable witnesses in the ordinary civilian scope. The difference itself does not choose a profile. |
| Tax scope under common admission | Finland / Åland | Requires Q004; the specific baggage formalities are not yet closed. |
| Geography/autonomy without a witness found | Portugal / Madeira, Azores; Italy / Sicily | Negative controls against an automatic split; unknown does not denote equivalence. |
| Whole-territory permit and local overlay | India / Arunachal; India / Ladakh; China / TAR | Q005/Q009. The PAP for the whole of Arunachal is confirmed; the Ladakh proposal does not replace the current partial regulation. The TAR positive candidate requires a more complete baseline witness. |
| Status object and operational zones | Western Sahara / west / east / Berm | Q006/Q007; a single international object, coarse operational evidence and unknown admission must not be collapsed into a country field. |
| Disputed control without civilian regime evidence | Aksai Chin; Shaksgam; Siachen | Blocked for now by the absence of access/admission and of exact current geometry; a claim gives no answer. |

In `comparisons.yaml` only four comparisons received `regime_difference=true`, each with a concrete context and a distinguishing component of the decision. The others keep the established facts and the explicit conditions that are missing for such a conclusion. No comparison is assigned a global `regime_difference=false`.

The evaluator is now formally open-world. `must_separate` is proven by a sufficient certificate; `hard_compatible` requires a separate positive proof of a complete equal hard signature. Therefore `no witness found`, `unknown` and `not must_separate` are never converted into positive Stage 1 compatibility.

Q001 tests Stage 1 mandatory-boundary profiles. It does not construct the complete canonical travel partition; Stage 2 may later subdivide a `hard_compatible` pair using destination semantics.

The representative run on the existing facts shows the expected asymmetry:

| Comparison | P1 | P2 | P3 |
|---|---|---|---|
| Germany / France | `separation_not_proven` | `must_separate` | `must_separate` |
| Italy / Sicily; Portugal / Madeira; France / Réunion | `separation_not_proven` | `data_unknown` | `model_unresolved` |
| UK / Guernsey; UK / Isle of Man | `separation_not_proven` | `must_separate` | `must_separate` |
| UK / Jersey | `must_separate` | `must_separate` | `must_separate` |
| Finland / Åland | `model_unresolved` (Q004) | `model_unresolved` | `model_unresolved` |
| Morocco / Western Sahara west | `separation_not_proven` | `data_unknown` | `model_unresolved` |
| Western Sahara west / east | `data_unknown` | `data_unknown` | `model_unresolved` |
| India / Arunachal Pradesh | `must_separate` | `must_separate` | `must_separate` |
| China / Tibet Autonomous Region | `separation_not_proven` | `data_unknown` | `model_unresolved` |
| China / Aksai Chin | `data_unknown` | `data_unknown` | `model_unresolved` |

The full reasons, blockers and evidence refs are given in `evaluator-contract.md`. These are evaluator outcomes, not canonical region assignments.

P3 cannot yet be completed without a definition of `Q001.identity` if P1/P2 have not already proven a split. For a disputed/occupied/international-status distinction Q006 applies in addition; ordinary identity cases refer to Q001. The set makes it possible to test the robustness of a future evaluator to names, missing evidence, historical data and the conflation of permits with jurisdiction; it does not prove a victory of P1/P2/P3.
