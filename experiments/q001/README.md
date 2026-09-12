# Experiment Q001 — factual dataset

Historical P1/P2/P3 experiment; facts and recorded results remain unchanged. Current production adoption is **CR-W only**, profile `S1-core-v1`, not a reinterpretation of these results. CR-J is well-defined but not adopted; P3 is non-production/model-unresolved, not Stage 2. See [stage1-core-adoption.md](stage1-core-adoption.md) for the decision and separate proof input contract.

Срез проверки: **11 сентября 2026**. Набор предназначен для сравнения трёх гипотез, а не для выбора canonical regions.

- **P1 — regime_only:** существенный TravelDecision witness в scope R007.
- **P2 — jurisdiction:** P1 плюс самостоятельная окончательная admission jurisdiction.
- **P3 — jurisdiction_plus_identity:** P2 плюс ещё не определённый критерий identity.

## Состав и запуск

49 сравнений; 56 вспомогательных factual units, включая reference scopes, status object и overlays. Число «cases» считается по сравнениям, а не по всем опорным единицам. Все обязательные группы присутствуют. 12 сравнений включены в blind set.

`facts/*.json` содержит записи с обязательными категориями. `comparisons.yaml` и `blind-comparisons.yaml` используют JSON-синтаксис — валидное подмножество YAML 1.2; их можно читать стандартным JSON parser. `evidence.json` хранит короткие атомарные утверждения, `sources.json` — источники, даты и ограничения. `route-matrix.json` отдельно показывает маршруты Western Sahara. `evaluator-contract.md` задаёт open-world semantics, а `evaluator-fixtures.yaml` — regression fixtures для реализации. `validate.py` проверяет связность и основные инварианты.

```bash
python3 validate.py
```

## Метод

Прочитаны project spec.md, decisions.md и open-questions.md; adversarial-test-set.csv не использовался как factual authority. Поля строятся по прочитанным источникам: закон/официальная процедура приоритетны; для disputed control разделены официальный claim, независимое сообщение и UN наблюдение. При недоступном полном тексте индексированный excerpt отмечен provisional, а не выдан за полный аудит.

Scope: гражданское краткосрочное посещение, nationality/document/residence/route context. Работа, дипломатическая служба и военная миссия не создают положительных witnesses. Наблюдения MINURSO используются лишь как свидетельства operational restrictions, не как правила туристического допуска.

Каждое содержательное поле имеет `evidence_refs`, а каждое evidence — `source_refs`, locator, статус и observed_as_of. `unknown` означает отсутствие установленного значения; пустые ссылки допустимы только у unknown или описания выбранной экспериментальной scope. `false` относится только к указанной размерности и не означает `hard_compatible`. Описание географии задаёт предмет исследования; оно не является точным operational polygon.

`regime_difference=true` требует конкретного контекста и различающего компонента решения. «Visa exempt» не означает гарантированный admission. Наличие схожего правила для одного паспорта не даёт `regime_difference=false`: R009 запрещает доказывать глобальную эквивалентность конечной выборкой. Общие визовые различия без завершённой проверки nationality exceptions оставлены unknown с объяснением. Отсутствие witness даёт не положительную совместимость, а `separation_not_proven`, `data_unknown` или `model_unresolved` в зависимости от blocker. `hard_compatible` требует отдельно доказанной полной равной hard signature.

Для P2 различаются местный офис национального ведомства и самостоятельная юрисдикция, принимающая окончательное решение. Разные визовые надписи, парламент или статус constituent country сами по себе её не доказывают. `distinct_operational_control` может относиться к civil/military функции; сравнение C032 не устанавливает две immigration jurisdictions.

## Blind protocol

Evaluator получает только `blind-comparisons.yaml`, без `blind-answer-key.json`, source-index или полного набора. Названия, исходные IDs и имена ведомств заменены согласованными алиасами; source URLs и названия документов исключены из payload. Сохранены типы полей, значения, неопределённость, даты, условия и provenance graph. Структурно уникальное правило всё ещё может быть узнаваемо — анонимизация не гарантирует невозможность догадки. Ключ нужен только исследователю для сопоставления outcomes.

## Evaluator boundary

`must_separate` и `hard_compatible` независимы. P1 принимает verified hard witness; P2 дополнительно принимает independently verified разные final admission jurisdictions; P3 не угадывает territorial/legal identity и возвращает `model_unresolved` с `Q001.identity`, если P1/P2 уже не доказали split. Q006 остаётся только для disputed/occupied/international-status distinctions.

Q001 is a Stage 1 Mandatory Separation experiment. A `hard_compatible` result means only that the selected profile requires no hard boundary; it does not assign a final canonical region. P3 is a Stage 1 territorial/legal identity hypothesis, not a Stage 2 destination-identity evaluator.

Comparison `blocked_by` strings are human-readable diagnostics and have no terminal evaluator semantics. A comparison-level missing fact produces `data_unknown` only when represented by a typed `evaluator_data_blockers` entry with a stable ID and explicit profile applicability, or when it follows from another structured status such as provisional witness evidence.

## Ограничения

This is a verifiable research snapshot with explicit gaps, not a fully confirmed travel reference. Some required disputed cases intentionally remain blocked: neither absent sources nor political status are filled by inference. A page check date does not turn a 2023–2025 observation into a current 2026 map. See `data-gaps.md` for the full limitations. The reference evaluator is implemented, but profiles remain unranked, Stage 2 is undefined, and no canonical verdicts exist.
