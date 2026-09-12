# Experiment Q001 changelog

## 2026-09-12 — open-world evaluator semantics

### Semantic changes

- Разделены независимые предикаты `must_separate(A,B,profile)` и `may_merge(A,B,profile)`.
- Запрещены closed-world выводы `no witness found => regimes equal => merge`, `unknown => false` и `not must_separate => may_merge`.
- Введены pairwise outcomes `must_separate`, `may_merge`, `separation_not_proven`, `model_unresolved`, `data_unknown`, `rule_conflict` и их deterministic precedence.
- Определены `signature_complete` и `signatures_equal`, включая состояния `known_value`, `known_absence`, `unknown`, `not_applicable`, `unresolved_model_semantics`.
- Формализованы минимальные P1/P2/P3 signatures. P2 принимает independently verified различие final admission jurisdiction как split; P3 блокируется `Q001.identity`, если P1/P2 уже не доказали split.
- Добавлена R038; точечно уточнены R008, R009, R010, R035, R037 и проверки V004/V009/V010.
- Добавлены implementation contract, 15 machine-readable fixtures и representative classifications для 13 обязательных comparisons.

### Cleanup only

- В `comparisons.yaml` и соответствующем blind payload обычные identity cases переведены с ошибочной ссылки Q006 на Q001.
- Q006 оставлена только у comparisons, где участвует disputed/occupied/international-status distinction; у них Q001 сохраняется как общий identity question.
- В README, summary и data-gaps выровнена терминология Q001/Q006 и добавлены ссылки на evaluator artifacts.
- Обновлены версия/дата документов до 0.1.1-draft / 2026-09-12.

### Factual records intentionally unchanged

- Не менялись `facts/*.json`.
- Не менялись `evidence.json`, `sources.json`, `source-index.md` и `route-matrix.json`.
- Не добавлялись территории, comparisons, sources или traveller witnesses.
- Не менялись значения `regime_difference`, `independent_admission_jurisdiction`, `distinct_operational_control`, сами witness contexts и evidence status.
- Representative evaluator outcomes являются производными от существующего snapshot и не записаны как новые factual evidence или canonical verdicts.
