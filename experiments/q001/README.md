# Experiment Q001 — factual dataset

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

Каждое содержательное поле имеет `evidence_refs`, а каждое evidence — `source_refs`, locator, статус и observed_as_of. `unknown` означает отсутствие установленного значения; пустые ссылки допустимы только у unknown или описания выбранной экспериментальной scope. `false` относится только к указанной размерности и не означает merge. Описание географии задаёт предмет исследования; оно не является точным operational polygon.

`regime_difference=true` требует конкретного контекста и различающего компонента решения. «Visa exempt» не означает гарантированный admission. Наличие схожего правила для одного паспорта не даёт `regime_difference=false`: R009 запрещает доказывать глобальную эквивалентность конечной выборкой. Общие визовые различия без завершённой проверки nationality exceptions оставлены unknown с объяснением. Отсутствие witness даёт не merge, а `separation_not_proven`, `data_unknown` или `model_unresolved` в зависимости от blocker. `may_merge` требует отдельно доказанной полной равной hard signature.

Для P2 различаются местный офис национального ведомства и самостоятельная юрисдикция, принимающая окончательное решение. Разные визовые надписи, парламент или статус constituent country сами по себе её не доказывают. `distinct_operational_control` может относиться к civil/military функции; сравнение C032 не устанавливает две immigration jurisdictions.

## Blind protocol

Evaluator получает только `blind-comparisons.yaml`, без `blind-answer-key.json`, source-index или полного набора. Названия, исходные IDs и имена ведомств заменены согласованными алиасами; source URLs и названия документов исключены из payload. Сохранены типы полей, значения, неопределённость, даты, условия и provenance graph. Структурно уникальное правило всё ещё может быть узнаваемо — анонимизация не гарантирует невозможность догадки. Ключ нужен только исследователю для сопоставления outcomes.

## Evaluator boundary

`must_separate` и `may_merge` независимы. P1 принимает verified hard witness; P2 дополнительно принимает independently verified разные final admission jurisdictions; P3 не угадывает identity и возвращает `model_unresolved` с `Q001.identity`, если P1/P2 уже не доказали split. Q006 остаётся только для disputed/occupied/international-status distinctions.

## Ограничения

Это проверяемый исследовательский snapshot с явными gaps, не полностью подтверждённый справочник поездок. Часть обязательных disputed cases намеренно остаётся заблокированной: ни отсутствие источника, ни политический статус не заполняются догадкой. Дата проверки страницы не делает историческое наблюдение 2023–2025 актуальной картой 2026. Полный список ограничений — в data-gaps.md. Спецификация формализует контракт, но evaluator не реализован, profiles не ранжированы, canonical verdicts отсутствуют.
