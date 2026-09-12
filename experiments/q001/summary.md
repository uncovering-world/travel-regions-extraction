# Experiment Q001 — краткие результаты

Подготовлены 49 сравнений, 56 factual units, 55 атомарных evidence records и 52 источника; 12 сравнений анонимизированы. Канонические регионы не назначены.

| Тип проверки | Полезные случаи | Что именно можно проверить |
|---|---|---|
| Общая visa policy, самостоятельная admission | UK / Guernsey; UK / Isle of Man | Потенциальное расхождение P1 и P2: jurisdiction подтверждена, но P1 неизвестен, а не доказан false. |
| Обычные соседние государства | Germany / France | Разные final authorities; LTV может разрушить предположение «Schengen значит P1-equivalent». Legal witness пока provisional. |
| Конкретное visa/document различие | UK / Jersey; Aruba / Curaçao; Curaçao / Bonaire | Проверяемые witnesses в обычном гражданском scope. Само различие не выбирает profile. |
| Налоговый scope при общей admission | Finland / Åland | Требует Q004; конкретные багажные формальности ещё не замкнуты. |
| Geography/autonomy без найденного witness | Portugal / Madeira, Azores; Italy / Sicily | Отрицательные контроли против автоматического split; unknown не обозначает эквивалентность. |
| Permit всей территории и local overlay | India / Arunachal; India / Ladakh; China / TAR | Q005/Q009. PAP всей Arunachal подтверждён; Ladakh proposal не подменяет действующее частичное регулирование. TAR positive candidate требует более полного baseline witness. |
| Status object и operational zones | Western Sahara / west / east / Berm | Q006/Q007; единый международный объект, coarse operational evidence и unknown admission нельзя сворачивать в поле country. |
| Disputed control без civilian regime evidence | Aksai Chin; Shaksgam; Siachen | Пока заблокированы отсутствием access/admission и точной современной geometry; claim не даёт ответа. |

В `comparisons.yaml` только четыре сравнения получили `regime_difference=true`, каждое с конкретным контекстом и различающим компонентом решения. Остальные сохраняют установленные факты и явные условия, которых не хватает для такого вывода. Ни одному сравнению не присвоено глобальное `regime_difference=false`.

Evaluator теперь формально open-world. `must_separate` доказывается достаточным certificate; `may_merge` требует отдельного положительного доказательства полной равной hard signature. Поэтому `no witness found`, `unknown` и `not must_separate` никогда не преобразуются в merge.

Representative run по существующим фактам показывает ожидаемую асимметрию:

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

Полные reasons, blockers и evidence refs приведены в `evaluator-contract.md`. Это evaluator outcomes, не canonical region assignments.

P3 пока нельзя завершить без определения `Q001.identity`, если P1/P2 уже не доказали split. Для disputed/occupied/international-status distinction дополнительно применяется Q006; обычные identity cases ссылаются на Q001. Набор позволяет тестировать устойчивость будущего evaluator к названиям, missing evidence, историческим данным и смешению разрешений с юрисдикцией; он не доказывает победу P1/P2/P3.
