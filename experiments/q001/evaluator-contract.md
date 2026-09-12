# Experiment Q001 — evaluator contract

Статус: implementation-ready contract для `spec.md` 0.1.1-draft и factual snapshot 2026-09-11. Контракт не выбирает между P1/P2/P3 и не назначает canonical regions.

## 1. Основные предикаты

### `must_separate(A, B, profile)`

Истинен только при наличии достаточного положительного основания, запрещающего A и B находиться в одном canonical travel region данного profile.

Для regime-based split достаточно witness `C`, если одновременно выполнено:

1. `C` входит в scope R007;
2. evidence для контекста и обоих решений достаточно и действует на `as_of`;
3. `HardTravelDecision(A,C) != HardTravelDecision(B,C)` по hard dimension profile;
4. различие относится к территориальному scope, а не только к local overlay или детали конкретной точки входа;
5. witness не имеет статуса provisional, conflicted или unknown.

P2 дополнительно принимает independently verified различие `final_admission_jurisdiction`. P3 может дополнительно принимать identity discriminator, но этот discriminator пока не определён.

### `may_merge(A, B, profile)`

Истинен только при достаточном положительном доказательстве эквивалентности A и B по всем hard dimensions profile:

```text
may_merge(A,B,P) :=
    signature_complete(A,P)
    and signature_complete(B,P)
    and signatures_equal(A,B,P) = true
    and no applicable must_separate certificate
```

`may_merge` не является отрицанием `must_separate`. Следующие импликации запрещены:

```text
no witness found  => may_merge
unknown           => false
not must_separate => may_merge
```

## 2. Signature completeness

Каждая dimension имеет тип, scope и одно состояние:

| Состояние | Семантика | Допустимо для complete signature |
|---|---|---|
| `known_value` | Evidence-backed конкретное значение или нормализованное множество значений | да |
| `known_absence` | Evidence-backed утверждение, что применимого значения/требования нет | да |
| `unknown` | Значение не установлено или evidence недостаточно | нет |
| `not_applicable` | Dimension неприменима по указанному rule-based основанию | да |
| `unresolved_model_semantics` | Модель не определяет, как вычислять или сравнивать dimension | нет |

Пустое поле не означает `known_absence`. `not_applicable` не выводится из отсутствия записи. Для обоих состояний требуется rationale; для `known_absence` требуется положительное evidence.

Completeness доказывается не перебором нескольких traveller examples, а evidence-backed применимостью нормализованных policy/scope records ко всей hard dimension внутри зафиксированного profile и R007 scope. Конечная выборка совпавших решений сама по себе signature не завершает.

```text
signature_complete(A, P) = true
```

тогда и только тогда, когда:

- перечень обязательных dimensions P определён;
- каждая dimension A имеет состояние `known_value`, `known_absence` или обоснованное `not_applicable`;
- evidence соответствует времени, scope и требуемому уровню достаточности;
- нет нерешённого source conflict, меняющего значение dimension.

```text
signatures_equal(A, B, P)
```

возвращает `true | false | unknown`:

- `true`: обе signatures complete, все обязательные typed dimensions равны;
- `false`: обе стороны сравнимы и хотя бы одна обязательная dimension доказанно различается;
- `unknown`: хотя бы одна signature incomplete либо сравнение dimension не определено.

Две `not_applicable` равны только для одной и той же dimension и совместимого rationale. `known_absence` не равно `unknown`; сравнение `known_absence` с `not_applicable` не нормализуется автоматически.

### Минимальный рабочий состав profiles

Этот состав нужен для Q001 evaluator, но не закрывает Q002/Q004/Q005/Q009.

- P1 `regime_only`: `admission_decision_scope`, `visa_scope`, `document_scope`, `relevant_hard_permits`; также `route_dependent_hard_decisions`, если они включены в конкретную версию profile.
- P2 `jurisdiction`: все P1 dimensions плюс `final_admission_jurisdiction` и признак самостоятельности конечного решения.
- P3 `jurisdiction_plus_identity`: все P2 dimensions плюс `identity_discriminator`.

До закрытия `Q001.identity` dimension `identity_discriminator` имеет `unresolved_model_semantics`; evaluator не выводит её из названия, ISO-кода, автономии, островного положения или типа зависимости.

## 3. Input

Evaluator получает один immutable input bundle:

```yaml
spec_version: string
dataset_version: string
as_of: date
profile:
  id: P1 | P2 | P3
  version: string
  hard_dimensions: []
  traveller_scope_ref: R007
factual_units:
  - id: string
    dimensions: {}
comparison:
  id: Cxxx
  a: factual_unit_id
  b: factual_unit_id
  candidate_witnesses: []
  relevant_rules: []
  evaluator_data_blockers:
    - id: stable_machine_id
      kind: missing_fact | source_conflict | verification_status
      profiles: [P1, P2, P3]
      evidence_refs: []
evidence_records: []
```

- `profile` фиксирует exact набор hard dimensions; одного имени P1/P2/P3 без версии недостаточно для воспроизводимой сборки.
- `factual_units` содержат типизированные значения и состояния, но не canonical verdict.
- `comparison` ссылается на endpoints по ID. Имена и political labels не являются входом в решение.
- `comparison.evaluator_data_blockers` is the typed source for comparison-level `data_unknown` semantics. Every entry has a stable ID, blocker kind, explicit profile applicability, and optional evidence references.
- Human-readable `blocked_by` prose is diagnostic documentation only. `blocked_by` prose is not an evaluator blocker, is never parsed by the adapter, and cannot by itself produce `data_unknown`.
- `evidence_records` содержат status, temporal scope, source refs и locators. Порядок записей не значим.
- `spec_version` обязателен; evaluator не смешивает правила разных версий.

## 4. Output

```yaml
comparison_id: Cxxx
profile: P1
result: must_separate | may_merge | separation_not_proven | model_unresolved | data_unknown | rule_conflict
applied_rules: []
witnesses: []
signature:
  a_complete: true | false
  b_complete: true | false
  equal: true | false | unknown
blocked_by_data: []
blocked_by_model: []
evidence_refs: []
explanation: string
```

- `comparison_id`: стабильный ID входного сравнения.
- `profile`: exact profile ID, согласованный с версией во входе.
- `result`: один terminal pairwise outcome из раздела 5.
- `applied_rules`: отсортированный набор реально применённых Rxxx; потенциально релевантные, но не применённые правила сюда не входят.
- `witnesses`: нормализованные sufficient witnesses, поддерживающие `must_separate`. Для остальных outcomes массив пуст. Отклонённые candidates отражаются в explanation/blocks.
- `signature.a_complete` и `b_complete`: результаты `signature_complete`.
- `signature.equal`: результат `signatures_equal`; значение `true` возможно только при двух complete signatures.
- `blocked_by_data`: стабильные machine-readable IDs конкретных missing/conflicted records или dimensions. A comparison-level ID must come from `evaluator_data_blockers`; prose in `blocked_by` is not a substitute.
- `blocked_by_model`: стабильные Qxxx/predicate IDs, например `Q001.identity`.
- `evidence_refs`: отсортированное объединение evidence, реально использованного для outcome и signature assessment.
- `explanation`: короткое детерминированное объяснение без вывода из имён территорий.

Даже при `must_separate` signature может быть incomplete: witness является достаточным контрпримером равенству. При `may_merge` обе completeness flags обязаны быть true, а `equal` — true.

## 5. Outcomes и приоритет

Evaluator применяет следующий порядок; внутри шага записи сортируются по stable ID.

1. `rule_conflict`: две совместимые нормативные derivations требуют несовместимых terminal outcomes при одном наборе принятых фактов. Конфликт источников здесь не классифицируется.
2. `must_separate`: существует sufficient certificate P1/P2/P3. Более поздние undefined dimensions не отменяют уже доказанный split.
3. `model_unresolved`: undefined model predicate может изменить terminal outcome. Для P3 после отсутствия достаточного P1/P2 split это как минимум `Q001.identity`.
4. `data_unknown`: конкретный unknown или unresolved source conflict блокирует обязательную dimension либо проверку candidate certificate. Он используется, когда проблема локализована в данных, а не просто когда открытый поиск не доказал всеобщую эквивалентность.
5. `may_merge`: обе signatures complete и equal; отдельного split-certificate нет.
6. `separation_not_proven`: split-certificate отсутствует, но условия `may_merge` не выполнены, и более специфичный blocker выше не применим. Это открытый, не терминально-отрицательный результат.

Authoritative evidence records, дающие разные значения одной dimension в совместимых temporal/scope условиях, создают `source_conflict` в data assessment и обычно ведут к `data_unknown`. `rule_conflict` возникает только после нормализации фактов, когда конфликтуют сами правила.

## 6. Profile algorithms

### P1 — `regime_only`

```text
if sufficient verified hard regime witness exists:
    must_separate
else if model semantics for a required P1 dimension are unresolved:
    model_unresolved
else if a concrete data blocker prevents required assessment:
    data_unknown
else if both P1 signatures are complete and equal:
    may_merge
else:
    separation_not_proven
```

### P2 — `jurisdiction`

Сначала применяются все основания P1. Затем independently verified разные final admission jurisdictions дают `must_separate` по R011, даже при одинаковой visa policy. `may_merge` требует complete/equal P1 signature и complete/equal jurisdiction dimensions.

### P3 — `jurisdiction_plus_identity`

Все sufficient основания P1/P2 сохраняются. Если они не дали `must_separate`, outcome зависит от ещё не определённого identity discriminator и возвращается:

```yaml
result: model_unresolved
blocked_by_model:
  - Q001.identity
```

Для disputed/occupied/international-status distinctions дополнительно указывается Q006, если именно этот тип identity участвует. P3 не содержит hidden manual list.

## 7. Determinism requirements

Evaluator обязан быть:

- deterministic: одинаковый нормализованный bundle даёт byte-equivalent semantic output;
- order-independent: перестановка factual/evidence/rule records не меняет результат;
- symmetric для pairwise semantics: swap A/B меняет только ориентированные поля witness, но не result;
- name-blind: names, country labels и display order не участвуют в predicate;
- explicit about unknown: missing/null/empty не нормализуются в false или absence;
- fail-closed для merge: неполная signature никогда не даёт `may_merge`.

## 8. Representative Q001 classifications

Это применение контракта к уже собранным фактам, а не изменение factual evidence и не назначение canonical regions.

```yaml
representative_evaluations:
  C001: # Germany / France
    P1: {result: data_unknown, because: provisional LTV candidate has a concrete verification-status blocker under fixture F013 and outcome precedence, blocked_by_data: [E01.status]}
    P2: {result: must_separate, because: independently verified final admission jurisdictions differ under R011, evidence_refs: [E02, E03]}
    P3: {result: must_separate, because: P2 already proves separation, evidence_refs: [E02, E03]}
  C002: # Italy / Sicily
    P1: {result: separation_not_proven, because: no verified witness and no complete equivalence audit}
    P2: {result: data_unknown, because: final jurisdiction comparison is provisional or incomplete, blocked_by_data: [final_admission_jurisdiction]}
    P3: {result: model_unresolved, blocked_by_model: [Q001.identity]}
  C014: # Portugal / Madeira
    P1: {result: separation_not_proven, because: matching sampled rules do not establish complete signatures}
    P2: {result: data_unknown, blocked_by_data: [final_admission_jurisdiction]}
    P3: {result: model_unresolved, blocked_by_model: [Q001.identity]}
  C008: # UK / Guernsey
    P1: {result: separation_not_proven, because: no fully specified hard regime witness and signatures are incomplete}
    P2: {result: must_separate, because: independently verified admission jurisdictions differ under R011, evidence_refs: [E18]}
    P3: {result: must_separate, because: P2 already proves separation, evidence_refs: [E18]}
  C009: # UK / Isle of Man
    P1: {result: separation_not_proven, because: no fully specified hard regime witness and signatures are incomplete}
    P2: {result: must_separate, because: independently verified admission jurisdictions differ under R011, evidence_refs: [E18, E21]}
    P3: {result: must_separate, because: P2 already proves separation, evidence_refs: [E18, E21]}
  C007: # UK / Jersey
    P1: {result: must_separate, because: verified accepted-document witness, evidence_refs: [E19]}
    P2: {result: must_separate, because: P1 witness and independently verified jurisdiction, evidence_refs: [E19, E20]}
    P3: {result: must_separate, because: P1/P2 already prove separation, evidence_refs: [E19, E20]}
  C018: # France / Reunion
    P1: {result: separation_not_proven, because: destination-visa distinction lacks a fully specified verified traveller witness}
    P2: {result: data_unknown, blocked_by_data: [final_admission_jurisdiction]}
    P3: {result: model_unresolved, blocked_by_model: [Q001.identity]}
  C013: # Finland / Aland
    P1: {result: model_unresolved, because: customs/fiscal distinction is not yet classified as a P1 hard dimension, blocked_by_model: [Q004]}
    P2: {result: model_unresolved, because: P1 customs semantics remain unresolved, blocked_by_model: [Q004]}
    P3: {result: model_unresolved, blocked_by_model: [Q001.identity, Q004]}
  C031: # Morocco proper / Western Sahara west
    P1: {result: separation_not_proven, because: one bounded matching passport rule is not complete regime equivalence}
    P2: {result: data_unknown, blocked_by_data: [final_admission_jurisdiction]}
    P3: {result: model_unresolved, blocked_by_model: [Q001.identity, Q006]}
  C032: # Western Sahara west / east
    P1: {result: data_unknown, blocked_by_data: [east_admission_rules, east_civilian_access]}
    P2: {result: data_unknown, blocked_by_data: [east_final_admission_jurisdiction]}
    P3: {result: model_unresolved, blocked_by_data: [east_admission_rules, east_civilian_access], blocked_by_model: [Q001.identity, Q006]}
  C042: # India / Arunachal Pradesh
    P1: {result: must_separate, because: verified whole-territory PAP witness, evidence_refs: [E07, E08, E44]}
    P2: {result: must_separate, because: P1 already proves separation, evidence_refs: [E07, E08, E44]}
    P3: {result: must_separate, because: P1 already proves separation, evidence_refs: [E07, E08, E44]}
  C041: # China / Tibet Autonomous Region
    P1: {result: separation_not_proven, because: permit candidate lacks a completed ordinary-baseline comparison}
    P2: {result: data_unknown, blocked_by_data: [final_admission_jurisdiction]}
    P3: {result: model_unresolved, blocked_by_model: [Q001.identity]}
  C040: # China / Aksai Chin
    P1: {result: data_unknown, blocked_by_data: [admission_rules, civilian_access, current_control_geometry]}
    P2: {result: data_unknown, blocked_by_data: [current_control_geometry, final_admission_jurisdiction]}
    P3: {result: model_unresolved, blocked_by_data: [admission_rules, civilian_access, current_control_geometry], blocked_by_model: [Q001.identity, Q006]}
```

Comments are display labels only; an implementation consumes comparison IDs and facts, not those names.

## 9. Fixture conventions

`evaluator-fixtures.yaml` использует компактный synthetic DSL:

- `complete:Sx` означает, что все обязательные dimensions данного profile представлены допустимыми состояниями и нормализуются в signature token `Sx`;
- `incomplete:<reason>` означает неполную signature и не является значением dimension;
- `known_value:X`, `known_absence:EV`, `not_applicable:RULE` и `source_conflict:A/B` соответствуют состояниям раздела 2;
- объект `expected` является subset oracle: реализация может вернуть дополнительные обязательные поля полного output contract, но не может изменить перечисленные значения;
- fixture с `input_variants` требует одинакового semantic outcome для каждого варианта.

Production input не обязан использовать эти строковые сокращения; он обязан сохранять ту же типизированную семантику.
