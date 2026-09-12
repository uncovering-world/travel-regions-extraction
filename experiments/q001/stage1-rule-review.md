# Q001 — Stage 1 rule review

Последующее решение пользователя: принят **только CR-W** в `S1-core-v1`; CR-J — well-defined normative candidate, not adopted. См. [adoption record](stage1-core-adoption.md). Остальной текст сохранён как исторический анализ, включая прежнюю рекомендацию W OR J; она не является текущей принятой нормой.

Дата review: 2026-09-12. Статус: **candidate analysis; normative changes not applied**.

Рекомендация: **B — Q001 can be narrowed**. Минимальный кандидат — доказанная территориальная разница hard TravelDecision **OR** доказанная самостоятельная конечная admission competence. Неопределённую territorial/legal identity исключить из предлагаемого production profile. Отдельный control separator сейчас не добавлять: доказанные admission/access consequences уже покрываются первым основанием, структурированная фактическая admission jurisdiction — вторым. Остаточные вопросы legal status, доступа и контроля остаются явно ограниченными Q006/Q005/Q007/Q008/Q009.

Это предложение, а не принятие новой нормы. Оно не гарантирует все D004/D007 и не объявляет Q001 закрытым. [Machine-readable companion](stage1-rule-candidates.yaml) содержит те же правила, evidence gates, отвергнутые альтернативы и синтетические различающие случаи; существующий evaluator этот файл не исполняет.

## 1. Problem statement

Stage 1 запрещает совместное нахождение некоторых точек в любом final region. Он не определяет самостоятельность destination и не обязан различать все будущие final regions. Stage 2 может только уточнять Stage 1 partition; его алгоритм здесь не исследуется. Основание: [spec R008–R011, R038–R043](../../docs/spec.md), [D023–D030](../../docs/decisions.md), [architecture](../../docs/partition-architecture.md).

Вопрос Q001 — какие **положительно доказуемые свойства** достаточно объявить hard. Объективность фактического предиката сама по себе не доказывает нормативную необходимость split: измеримое различие часовых поясов тоже объективно. Нужно явно обосновать, почему выбранная dimension должна быть однородной внутри Stage 1 cell.

Review анализирует существующий snapshot 2026-09-11: 49 comparisons, 56 supporting units, 55 evidence records, 147 profile results. Источники: [comparisons](comparisons.yaml), [evidence](evidence.json), [source limitations](sources.json), [data gaps](data-gaps.md), [contract](evaluator-contract.md), [results](results/evaluator-results.json), [run summary](results/run-summary.md). Ссылки E##/S## ниже относятся к Q001 dataset, а не к одноимённым ссылкам в spec/decision log. Новые geographic facts не собирались; существующие statements не повышались в статусе и не считаются независимой проверкой актуального права на дату review. Crimea присутствует в D006/D013 и [adversarial T059/T060](../../data/adversarial-test-set.csv), но **не имеет factual unit/comparison в этих 49 Q001 cases**.

Основание артефактов: repository commit `6ad56e16e3744c8ae98266408ac13a7717c9000f`; evaluator `0.2.0`; spec `0.2.0-draft`; recorded factual-input SHA-256 `fd4875e773731a4533549d3526ef54c4a0945c4ca84d8045214a517ebba61831`.

| Profile | must_separate | hard_compatible | separation_not_proven | model_unresolved | data_unknown |
|---|---:|---:|---:|---:|---:|
| P1 | 4 | 0 | 41 | 1 | 3 |
| P2 | 8 | 0 | 1 | 1 | 39 |
| P3 | 8 | 0 | 0 | 41 | 0 |

P1 certificates: C007, C029, C030, C042. P2 дополнительно получает C001, C008, C009, C012. Ни одна реальная пара не имеет доказанной полной P1 equivalence: **в наборе нет доказанного контрпримера «P1 equality + разные jurisdictions»**. Поэтому разница счётчиков не доказывает превосходство P2. P3 не дал дополнительного split; его 0 terminal `data_unknown` объясняется приоритетом model blocker, а не исчезновением неизвестных фактов. В старом [summary](summary.md) C001/P1 указан как `separation_not_proven`; актуальные contract/results дают `data_unknown` из-за provisional E01. В review используется последний результат, исходные файлы не исправляются.

## 2. Evaluation criteria

Правило оценивается по четырём независимым слоям: определён ли предикат; доказаны ли его inputs; следует ли hard consequence из выбранной нормы; достаточен ли scope сертификата для заявленной границы. Product regression не заменяет ни один из этих слоёв.

| Критерий | Проверяемый тест |
|---|---|
| Operational definability | Типизированные необходимые premises, явные true/false/unknown/model-unresolved; слова «особый», «самостоятельный» раскрыты через проверяемые отношения. |
| External verifiability | Каждая premise имеет evidence, locator, компетенцию источника, territorial и temporal scope; assertion в dataset сама не заменяет доказательство. |
| Name blindness | Биективно переименовать территории, authorities и их ID с сохранением отношений; результат изоморфен. Никаких special values для конкретных стран. |
| Universality | Одинаковое доказательство даёт одинаковый исход в unitary, federal, dependent и de facto arrangements. Отсутствие данных не освобождает от теста. |
| Political independence | Claim, recognition count и label не участвуют в вычислении. Применимое право и factual exercise документируются раздельно. |
| Temporal stability | Один snapshot воспроизводим; смена вывески/офиса не меняет competence; действительное изменение нормы может менять результат. Постоянство геометрии во времени не обещается. |
| Minimality | Каждое дополнительное основание различает хотя бы один формальный случай, который остальные основания намеренно допускают. |
| Over-/under-splitting | Есть отрицательные контрпримеры; явно указаны классы различий, которые правило не сохраняет. |
| Open world | Ненайденный witness и недоказанная независимость не становятся equality либо split. |
| Architecture | Никакой destination intuition, автоматической островности/административности; Stage 2 сохраняет каждый доказанный Stage 1 separator. |

«Не делит по данному фактору» ниже означает только отсутствие сертификата от этого фактора. Это не `hard_compatible`, не merge и не final assignment.

## 3. P1 assessment

### 3.1. Достаточность и необходимость

**Доказанное различие уже определённой hard traveller-facing dimension достаточно для Mandatory Separation.** Если два места требуют разных territorial admissions/documents/permissions в одном допустимом контексте, единая hard signature для них неверна. Слово hard здесь необходимо: разница цены билета, очереди, рейса или доступа в здание не становится hard просто потому, что влияет на путешествие.

Утверждение «regime difference необходимо, но недостаточно» логически не подходит. В P1 прошедший все gates witness **достаточен**, а истинная разница решений является необходимым условием именно regime-based split. В более широком Stage 1 с P2 она **не необходима**: компетенции могут быть разными при тождественных правилах. Хорошие основания считать **P1 как полный набор правил недостаточным** есть, если продукт требует сохранять самостоятельную ответственность за territorial admission; это отдельный нормативный выбор, а не следствие найденного паспорта. Destination separateness вообще не аргумент против P1 как Stage 1 foundation.

P1 систематически не различает при доказанном равенстве всех включённых outputs:

- Разные конечные admission jurisdictions, координирующие одинаковые правила; независимость их будущих решений не является текущим regime witness.
- Территории с разным constitutional, dependency или international status, который не меняет scoped TravelDecision.
- Разные civil/military controllers, если все включённые admission/legal-access outcomes одинаковы и decision-maker identity не включена в outputs.
- Острова, автономии, административные области, remote parts и destinations с одной hard signature. Для Stage 1 это намеренная неразличимость.
- Customs/biosecurity-only, activity/site-access и решения вне утверждённого traveller scope, если они не включены в hard dimensions. Здесь требуется Q004/Q005, а не расширение по имени территории.

Ни один из этих классов не означает, что конкретная пара в dataset уже признана равной.

### 3.2. Existential witness semantics

Сохранить квантор существования, но определить его operands:

```text
W(A,B,t) := exists C in S_v, d in H_v:
    eligible(C) AND comparable_trip(C,A,B)
    AND territorial_effect(d,A,B,C)
    AND standing_rule_at_t(d,A,B)
    AND proven(D_d(A,C,t) != D_d(B,C,t))
```

`S_v` — версионированный scope R007; `H_v` — закрытый перечень hard outputs выбранного candidate profile. `D` означает нормативно определяемые требования/допустимость, а не прогноз discretionary решения конкретного офицера. `proven` требует обе стороны, все влияющие exceptions и одинаковое время. Неизвестное решение не сравнивается как значение. Две законные discretionary возможности с разными реализованными исходами ещё не доказывают разницу regime.

`C` должен быть непротиворечивым классом гражданского краткосрочного посещения: фиксируются релевантные гражданства, документы, residence/authorisations, цель, длительность, history и способ/класс маршрута. Не нужен уже совершивший поездку человек. Отказ в A допустим как ответ запроса; требовать фактически разрешённого въезда **в обе** стороны означало бы исключить основные negative admission witnesses. Искусственная комбинация несовместимых документов/статусов witness не создаёт.

Для воспроизводимости решения сравниваются как функции на **общем** домене контекстов, а не на разных выборках посетителей A и B. Отсутствующий аэропорт не становится «admission denied». `entry_point` нормализуется в доказанный класс процедуры; несовпадение имени перевозчика или координат не является самостоятельной dimension. Территориальная сила разрешения и физическое место его оформления хранятся отдельно.

При фиксированных S/H/t existential semantics математически устойчива: полные функции решений равны по equivalence relation, контрпример опровергает равенство. Положительный сертификат сохраняется при добавлении согласованного evidence в тот же snapshot. Исправление факта, изменение нормы, scope или даты может его отозвать в новой версии. Это не нарушение R041, который относится к refinement между стадиями **одной** версии.

### 3.3. Редкие контексты и отсутствие frequency threshold

Да, один редкий документ, special authorisation или узкий travel-history class способен создать границу, затрагивающую всех пользователей partition. Это осознанная цена требования однородности для всего S. Частота использования документа не определяет его legal effect; условие «редкий» нельзя превращать в исключение для неудобного case.

R007 уже включает rare documents и special permits. Поэтому редкость сама по себе не дефект P1. Если класс поездок не относится к назначению продукта — это вопрос S/R007/Q002. Если различие связано с объектом или entry event — это H/territorial gate, Q005/Q009. Если проблема состоит именно в том, что **валидный hard witness внутри S слишком редко встречается**, убрать split, сохранив полную однородность S, невозможно. Потребуется честно изменить scope либо требование однородности.

Предлагаемый способ без частотного порога: оставить все документально допустимые классы внутри civilian short-stay S; допускать только class-based действующие нормы с territorial admission/stay effect. Разовое решение по имени конкретного лица, произвол офицера или разовая авария не образуют самостоятельную hard dimension. Это явное ограничение вида нормы, а не ограничение размера класса. Класс может иметь одного фактического носителя; произвольные personal IDs в предикате не допускаются. Эквивалентность полных функций не выводится из списка «типичных паспортов».

Остаточный риск не исчезает: узкая, но standing и territorial норма всё равно даст split. Если это неприемлемо, existential P1 и желаемая степень обобщения несовместимы; frequency threshold лишь скрыл бы этот выбор.

### 3.4. Что показали имеющиеся witnesses

| Cases | Установлено в текущем evaluator | Ограничение для candidate |
|---|---|---|
| C029/C030, E28 | Разный visa requirement для одного полностью заданного класса Jamaica ordinary passport. | Прямой пример W; не требует определения jurisdiction или identity. |
| C007, E10/E19 | Jersey ferry exception меняет admissible document; evaluator принимает witness. | Юридическая сила document exception для territorial entry может быть hard даже при условии маршрута. Нельзя создать отдельный region из ferry terminal. Нужен одинаковый логический класс поездки и territorial effect, а не только carrier practice. Временную standing/event семантику отдельно проверить при применении нового gate. |
| C042, E07/E08/E44 | PAP требуется в destination scope, ordinary reference находится вне schedule. | Не вывод «каждый whole administrative unit с permit — region». Правовая territorial presence restriction — кандидат hard; один whole-unit label Q005 не закрывает. Кроме того, endpoint `in` — reference scope: witness не доказывает разделение **всей India** и входящей в неё области. |
| C018, E26 | French overseas destination-visa distinction документировано; complete traveller witness не собран. | Хороший объясняющий механизм для D005; current `separation_not_proven` не повышается до split. |

## 4. P2 assessment

### 4.1. Является ли jurisdiction самостоятельным hard основанием?

**Рекомендуется да, при строгом функциональном определении ниже.** Причина: cell должна иметь одну систему конечной территориальной ответственности за обычный admission, независимо от сегодняшнего совпадения visa policy. Это нормативная однородность дополнительной dimension. Она согласуется с направлением R011/D025, но не выводится логически из P1 и не считается уже окончательно принятой формализацией R011.

Аргументы за: одинаковые требования могут действовать в разных независимых компетенциях; одна сторона не вправе принять admission decision за другую. Общая visa или mutual recognition of leave не уничтожают reserved territorial competence. Rule переживает унификацию паспортных требований и смену обслуживающего офиса. Критерий можно проверять по распределению полномочий без country/recognition label.

Аргументы против: это добавляет границу, которой текущий traveller outcome может не требовать; institutional structure сложнее документировать, чем visa requirement. Понятие «final» ошибочно тянет либо к последнему офицеру, либо к верховному законодателю/суду. Federal, shared и extraterritorial arrangements могут иметь несколько ролей и общий apex. Если модель ценит исключительно текущие outputs, этот дополнительный split избыточен; обещание возможной будущей policy divergence не доказывает текущую необходимость. Поэтому полезность P2 — выбранный инвариант ответственности, а не утверждение о неизбежной будущей разнице.

### 4.2. Operational definition: independent_final_admission_jurisdiction

Определить `admission_competence` как **юридическую capacity**, а не название органа, officer, visa issuer, sovereign или administrative unit. Один человек/орган может действовать в двух capacities; много офисов могут реализовывать одну capacity. Под «юридической» здесь понимается документированная норма применимого operational legal order; это не утверждение международно признанного суверенитета этого порядка.

Для scope X требуется dossier с шестью положительно доказанными premises (J1–J6):

1. **J1 — Constitutive allocation.** Действующий закон, договор, order или иной нормативный instrument распределяет обычный civilian admission/refusal и право обусловить либо прекратить stay для X. Указываются clauses, capacity, holder и цепочка полномочий. Permit issuer, кадровая структура и охрана границы по отдельности этого не доказывают.
2. **J2 — Territorial legal effect.** Решение, принятое в этой capacity, создаёт/прекращает permission или denial of entry/stay с собственным описанным geographical scope. Scope не ограничен рабочим округом офиса, портовым обслуживанием или занятием/посещением объекта. Раздельные national admission titles могут иметь общий слой признания; все их эффекты должны быть описаны.
3. **J3 — Reserved ordinary competence.** В действующей схеме эта capacity может окончательно принять или отказать в хотя бы одном непустом class-based обычном civilian admission/stay matter для X без необходимого индивидуального assent другой admission capacity. Должен существовать правовой механизм территориального отказа/прекращения stay. Не требуется неограниченная discretionary свобода или отдельная законодательная власть; обязательные права travellers и общий policy law совместимы с competence.
4. **J4 — Non-substitution.** Admission/leave, выданное другой capacity для её территории, само по себе не даёт ей полномочия вынести решение за X или отменить reserved territorial refusal X. Документируются и исключения, и recognition arrangements. Если обычный начальник может принять/заменить это решение как часть единой admission administration и единого admission title, нижестоящие offices — одна jurisdiction. Если общий орган действует в отдельной capacity X, это не решение capacity B за X.
5. **J5 — Attribution, delegation and review closure.** Нормализована полная релевантная цепочка `acts_for`, `case_substitution`, `required_assent`, `judicial_review`, `recognises_leave`. Делегирование **исполнения** не создаёт новую capacity. Законодательное учреждение отдельной territorial competence может её создать: возможность будущей отмены constitutive law не равна праву начальника заменить конкретное решение по действующему праву. Судебная проверка законности, общий конституционный apex и treaty constraints сами по себе не объединяют capacities. Нерешённое пересечение полномочий — unknown, не «две страны». Отсутствие delegation/substitution доказывается положительным allocation/override audit, не отсутствием результатов поиска.
6. **J6 — Effective territorial application.** На t установлены вступление allocation в силу и её применение к X. Для de facto arrangement дополнительно нужны независимые наблюдения обычного civilian admission/enforcement, согласующиеся с опубликованной схемой. Одного самоописания claimant или карты военных позиций недостаточно. Holder или отдельный офис не обязан быть физически расположен в X.

`J(X,C,t)` — канонизированная структура применимых capacities и отношений veto/assent для C после схлопывания исполнения в `acts_for`. Это может быть joint structure; несортированный список названий органов не является signature. Разные members одного совместного arrangement не получают каждый территорию. `J(A) != J(B)` доказано, если есть capacity, удовлетворяющая J1–J6, которая имеет самостоятельный territorial legal effect/зарезервированную competence на одной стороне и доказанно не имеет соответствующей competence на другой, либо различается доказанная структура обязательного assent. Общая переписанная структура с новыми ID должна быть изоморфна старой.

Итоговый predicate `J(A,B,t)` требует evidence-backed разных нормализованных competence structures, одного traveller scope/time и совместимых scopes A/B. Имена/номера нормативных актов служат locators, а не значениями для сравнения: два документа могут устанавливать одну competence. Не требуется реального случая разных outcomes: это было бы возвращением к P1. Не требуется независимости от всякого parent sovereign: это исключило бы часть зависимостей по устройству верховной власти.

J1–J6 доказываются для используемой separating competence и всех отношений, способных изменить её independence/scope. Не требуется завершить каждую постороннюю dimension прежде, чем принять такой сертификат. Но для `hard_compatible` нужен полный coverage audit обеих competence structures: недостаточность доказательства различия не есть доказательство одинаковой competence.

Это максимально строгий **достаточный**, не обещанный универсально полный тест. Неописанное shared arrangement может остаться unknown; отсутствие собственного veto не доказывает полное равенство всех остальных hard dimensions. Machine evaluation возможна после нормализации юридических premises; review не заявляет, что natural-language law автоматически и без interpretation превращается в J1–J6. Досье должно позволять независимому проверяющему воспроизвести каждую нормализацию.

### 4.3. Проверка критериев и текущего evidence

| Критерий | Оценка строгого P2 |
|---|---|
| Operational definability | Условно проходит с J1–J6 и графом capacities. Голое `authority_a != authority_b` проваливает тест. |
| External verifiability | Проверяем в принципе; нужны allocation, delegation, override и effect clauses, не только visitor guidance. Неполное досье остаётся unknown. |
| Name blindness | Проходит при сравнении relations/capacities и согласованном переименовании. Country-type lookup запрещён. |
| Temporal stability | Более устойчив к policy coincidence и office reorganisation, чем P1; реальная transfer of competence меняет J. Никакой гарантии «граница навсегда». |
| Universality | Один тест для всех arrangements, включая самостоятельную subnational admission competence; такая province split именно по competence. Joint cases могут быть unresolved. |
| Political bias | Снижается role-based evidence и отсутствием recognition gate; остаются риски source selection и интерпретации применимого order. Нельзя считать controlling authority автоматически законным sovereign. |
| Over-splitting | Высок у office-based P2; J2/J4/J5 блокируют office/delegation split. Сохранение разных capacities с равной policy — намеренный дополнительный split. |
| Under-splitting | Не сохранит dependency/legal-status boundary при общей competence и равных D. Высокий evidence bar увеличивает unknown; это не доказанное merge. |
| Independence from current visa coincidence | Проходит: одинаковые таблицы, общий visa issuer и взаимное признание разрешений не заменяют анализ reserved competence. |

Текущие P2 certificates C001 (E02/E03), C008 (E18), C009 (E18/E21), C012 (E23) приняты **старым контрактом**. E18 содержит прямое указание own jurisdictions; E20 для C007 содержит более конкретные statutory powers. Но короткие records не дают автоматически полного J1–J6 dossier. Особенно E23 «местные officers выдают permit» сам по себе не доказывает non-substitution; E02/E03 «national border authorities» не документирует всю цепочку override. Новый candidate потребует premise audit всех таких certificates, без изменения factual truth/status этих records. В этом review **нет нового пересчёта и нет обещания сохранить число 8**.

Контрпримеры: два региональных офиса одного national service с общим admission title — не J; общий visa-processing contractor двух доказанно самостоятельных capacities — не основание их считать одной; одна global apex court не делает все подведомственные admission capacities одинаковыми; enforcement by a different patrol не доказывает ни J3, ни J4.

## 5. P3 assessment

**P3 в текущем виде непригоден для production Stage 1.** `territorial/legal identity` не имеет общего machine predicate, а добавление названий территорий только скроет недоопределённость. 41 `model_unresolved` — корректный отказ evaluator угадать этот predicate, а не 41 доказанная самостоятельная территория.

| Попытка определения | Почему не удовлетворяет всему набору требований |
|---|---|
| Own legal personality / separate constitutional entity | Точно формализованный legal personality охватывает municipalities и другие public bodies; общее «особое конституционное положение» не определяет admission significance. Добавление «достаточно внешняя» возвращает неизвестный predicate. |
| ISO code / dependency / autonomy / dispute | Машинно удобно, но это запрещённые proxies. Код классификатора не доказывает hard travel difference; один label даёт blanket category split. |
| Separate legal system / own legislation | Общие law differences есть и у ordinary provinces. Ограничение именно admission law либо ведёт к P1/J, либо оставляет не travel-related hard rule, который нужно отдельно обосновать. |
| International status from an external list | Может быть воспроизводимым **registry-relative** правилом, но требует нормативного выбора registry, компетенции, покрытия и scope. UN decolonization list не является общим определением всех dependencies/disputes/occupation cases. Внешний curated список не становится non-curated оттого, что его ведёт другая организация. |
| Stable separate admission institutions | Имеет операциональный смысл после J1–J6; это P2, отдельной P3 dimension не добавляет. |
| Historically separate / important / recognisable territory | Нет machine semantics; выбор известных примеров становится скрытым oracle. Destination identity относится к другой стадии. |

Нельзя доказать невозможность **любого будущего** legal-status rule. Можно заключить более узко: доступного общего definition, одновременно выполняющего все поставленные условия и добавляющего независимое основание к W/J, сейчас нет. Exact legal predicate с указанным компетентным актом и последствиями можно предложить в Q006; его adoption будет новым нормативным решением, а не расшифровкой слова identity.

Типичный failure mode: выбрать политически заметные места → подобрать им неоднородные labels → назвать объединение labels territorial identity → закрепить expected outcomes. Blind IDs на последнем шаге этого не исправят: curated selection уже встроена в extraction/registry. При полном равенстве допустимых inputs любой детерминированный name-blind rule обязан вернуть одинаковый результат. Поэтому требования сохранить отдельность **без W/J** нельзя удовлетворить скрытым P3. Рекомендация: не включать undefined identity в новый core; сохранить P3 как архивную экспериментальную гипотезу. Существующий P3 evaluator остаётся неизменным.

## 6. Accepted-constraint regression analysis

Accepted constraints остаются требованиями для regression. Это не source facts и не `must_separate` derivations сами по себе. «Не исчезнуть» нужно различать как сохранение информации в legal/control objects, как отличие в final partition и как обязательную Stage 1 границу. Первое не гарантирует второе, второе не обязательно требует третьего. Перенос в Stage 2 возможен только как локализация final-output requirement; здесь не обещается, что будущий Stage 2 его выполнит.

| Constraint и evidence | Объясняется P1? | Объясняется P2? | Нужен P3 или другой механизм? | Regression verdict |
|---|---|---|---|---|
| D005: Réunion / metropolitan France; C018, E26/E27 | Да как механизм: applicable destination visa/document difference. В snapshot нет complete verified C, current P1 = `separation_not_proven`. | P2 включает тот же W; собственная независимая jurisdiction не доказана и не нужна при W. | P3 не нужен. Ни overseas label, ни VAT exclusion не заменяют admission witness. | Объяснимо общим правилом, применение ещё conditional по данным. Отдельность от метрополии не означает один целый final region или отдельность от всех overseas частей. |
| D004: British Overseas Territories / ordinary UK; C010–C012 | Может объяснить конкретные случаи; Bermuda nationality witness и Gibraltar comparison в snapshot не завершены. Из категории UKOT W не следует. | C012/Falklands имеет current P2 split; строгий J требует audit E23. C010/C011 final competence unknown; offices и checks не доказывают independence. | Blanket «всякая UKOT отдельно» не выводится. Undefined P3 не решает проблему; другие general hard rules пока не определены. | Покрытие требования лишь частичное. D004 нельзя объявить выполненным на основании трёх cases или Crown Dependencies (C007–C009 — другой класс). Если у UKOT полные W/J signatures равны UK, обязательная Stage 1 отдельность конфликтует с core. |
| D007: Western Sahara / ordinary Morocco; ключевая пара C031 west / Morocco | E39 устанавливает только совпадение одного passport rule, E40 — qualified access limitations без достаточного witness. Ни split, ни полное равенство не доказаны. | Final jurisdiction unknown; coarse Moroccan administration не доказывает ни J equality, ни difference. West/east contrast не переносится на west/Morocco. | Для требования отделять west даже при равных W/J нужен новый explicit legal-status rule (Q006) либо изменение требования; текущий P3 непригоден. | Главный нерешённый conceptual conflict: core **не гарантирует** D007. Сохранение dispute overlay не исполняет требование отдельного final region. Нельзя молча объявить его решённым Stage 2. |
| D006: Crimea / ordinary Ukraine; D013 и T059 отдельно от Q001 facts | Если доказано различие applicable civilian admission/legal routes в точных scopes, W объясняет требование. В Q001 таких фактов нет. | Если доказаны разные operative admission capacities, J объясняет границу независимо от recognition. Отдельная «Crimean» capacity не нужна: сравниваются реально применимые capacities по обе стороны. | P3 для исходного D006 логически не требуется. Отличие от ordinary Russia — более сильное **tentative D013**, не часть accepted D006. | Объяснимый operational mechanism; factual validation отсутствует. Не выводить current geometry или «Crimea = ровно одна cell» из accepted assertion. |

Дополнительный конфликт D004/D016 уже существует в decisions: literal separate British Antarctic claim sector, overlapping claims и предложение одной Antarctic cell нельзя одновременно принимать как готовые canonical polygons. Ни «один договор», ни «UKOT» не доказывает admission boundary. Review не принимает D016 как исключение и не выбирает Antarctic partition; этот конфликт остаётся Q011 вместе с соответствующими Q003/Q005.

Строгая формулировка конфликта с objective model: **если** полные hard decision functions и competence structures A/B равны, coarsest Stage 1 по core не имеет основания отделять A/B. Требование обязательной Stage 1 границы в том же случае несовместимо с core. В текущих данных равенство не доказано, поэтому это конфликт нормативной гарантии, а не уже установленный factual `rule_conflict`. Если D004/D007 трактуются только как final-output constraints, их исполнение остаётся непоказанным; они не становятся автоматически hard rules и не считаются снятыми.

## 7. Disputed-territory analysis

### 7.1. Раздельные типы и допустимые следствия

| Тип факта | Что он устанавливает | Допустимое Stage 1 следствие |
|---|---|---|
| Claim | Позицию актора относительно территории. | Сам по себе никакого split; не назначает controller, applicable law или geometry. |
| Recognition | Позицию третьей стороны о статусе/власти. | Сам по себе никакого split; изменение числа признающих при прежних W/J ничего не меняет. |
| International legal status | Атрибутированную правовую квалификацию компетентным instrument/body с собственным scope. | Хранится независимо от claims; в core сам label недостаточен. Доказанное traveller legal consequence может дать W. Status-only separator требует отдельной нормы Q006. |
| De facto civil control | Кто фактически управляет определёнными гражданскими функциями, где и когда. | Evidence для effective application и investigation admission/access. Само отличие civil administrator ещё не J или W. |
| Military control | Позиции, применение силы, военное удержание/ограничение. | Сам по себе не civilian admission jurisdiction. Доказанная territorial civilian prohibition может дать W после scope/time gates; патруль или mine hazard не даёт его автоматически. |
| Admission authority | Кто и в какой capacity принимает territorial admission/stay decision. | J при J1–J6; W при разнице условий. Отличать issuer, officer, capacity и enforcement. |
| Civilian route/access regime | Условия законного или фактически исполняемого civilian entry/presence для данного C/route. | W, если это принятая hard territorial dimension, доказаны обе стороны и действительность. Отсутствие рейса/дороги или advisory — не W. |

Гипотеза `disputed=true` само по себе **не является** Mandatory Separation rule — поддерживается. Она необходима для claim blindness: новый claim без operational/legal-travel изменения не должен создавать границу. International legal status не приравнивается к произвольному claim, но автоматического hard effect из этой разницы тоже не следует.

Альтернатива «stable distinct actual control / applicable admission / civilian legal-access system достаточно» требует разложения. Разница admission/legal-access с доказанным territorial effect достаточна как W. Разная институциональная civilian admission competence достаточна как J, включая подтверждённые de facto arrangements. **Разница actual controller без одного из этих следствий недостаточна**: иначе муниципальная смена управления, военный сектор или разные полицейские forces становятся новым hard dimension по неявному правилу.

У broad `legality_under(each relevant jurisdiction)` есть отдельная опасность: слово relevant может означать «каждый, кто сделал claim». Тогда заявленный claimant prohibition незаметно превращает claims в separators. Для proposed core брать legal obligations, применимость которых к C подтверждена независимо от спорного claim: действующее operational territorial admission право или документированная персональная/документная jurisdiction с прямым правилом поездки. Хранить `issuer/capacity`, applicability basis, legal consequence и factual enforcement отдельно. Если основание применимости к C или самой disputed территории требует нерешённого выбора legal authority, это Q006/model-unresolved, а не придуманное universal legality. Claim без такой нормы ничего не меняет; новая реально применимая traveller obligation может менять W даже при прежнем control. Общее экономическое соглашение/санкционный label без scoped civilian consequence недостаточны.

### 7.2. Cases уже присутствующего материала

| Case | Что действительно есть в snapshot | Допустимый general mechanism и оставшийся gap |
|---|---|---|
| Western Sahara west / Morocco, C031 | E36 qualified UN-status record; E37 coarse administration с observation 2025-09-30; E39 общий bounded British-passport rule; E40 qualified access limitations. | W возможен при конкретном territorial legal/access witness; J — при различной competence. Ни то ни другое не доказано. Если оба окажутся равны, отдельность west требует status-only решения Q006; internal west/east boundary не решает задачу. |
| Western Sahara west / east/south, C032 | E37/E38 civil/military observations; restrictions on MINURSO не являются tourist admission; east civilian routes/admission unknown. Current P1/P2 `data_unknown`. | Разные ordinary civilian admission systems могли бы дать W/J. `distinct_operational_control=true` в comparison недостаточно. Не выводить ровно две cells, текущую exact Berm line или east immigration authority из военных observations. |
| Western Sahara status object / zones / Berm, C033–C035 | `ws` — international-status object; zones/overlay могут пересекаться. E41 устанавливает mine/military hazard, не legal polygon. | Не обычные disjoint endpoints для `must_separate`. Нужны operational scopes и typed overlays; status object не помещается в partition рядом с собственными частями. |
| Crimea / ordinary Ukraine | Только accepted D006, tentative explanation D013 и unverified adversarial assertion; Q001 dossier отсутствует. | Conditional W/J позволяет объяснить исходный constraint без recognition rule. Здесь не утверждается current control или legal route. Gap применения — факты и scope/time. |
| Crimea / ordinary Russia | Более сильная tentative D013, без Q001 factual comparison. | Контроль, отличный от ordinary Ukraine, логически ничего не говорит об отличии от Russia. Нужен свой W/J certificate; если они равны, остаётся тот же status-only Q006 gap, что у west/Morocco. Нельзя подменить сравниваемую сторону. |
| Aksai Chin / China, C040 | E50 — historical control/claim description 2023-08; E09 — общая non-open-area permit норма без списка Aksai Chin; civilian routes/admission/current geometry unknown. | Доказанный ordinary territorial civilian prohibition/permit мог бы дать W; другой military controller по сравнению с claimant не объясняет split с тем же controlling system. Ни claim, ни слово restricted, ни unknown access не разрешают создать отдельную cell. Если W/J равны, остаток Q006. |
| Jammu and Kashmir / India, C036; Ladakh / India, C037 | E07/E08 — protected-area schedule; E49 qualified curfews/advice; E43 existing partial PAP и **предложение** all-UT PAP. | Доказанный permit effect относится к его legal scope, не ко всей административной области. Proposal не становится действующим W; local curfew требует Q008/Q009 gates. Нет blanket dispute split. |
| Gilgit-Baltistan / Pakistan, C038; AJK / Pakistan, C039; AJK / GB, C048 | E45/E46 qualified registration/district permissions; E47 historical 2019 waiver; E53 provisional administrative-side observations. | Сопоставимый territorial entry/presence permission может дать W; trekking activity permit сам по себе не даёт. Нужны current effective scope/authority, а не подмена 2019 NOC сегодняшней equivalence. J пока не установлен. |
| Tibet / China, C041 | E48 verified permit/organised-tour requirement; ordinary baseline witness не завершён. | Проверить legal territorial presence effect и ordinary baseline для W; organised-tour условие отдельно от ticket/activity permit. Автономия не доказывает J; identity не завершает недостающую baseline. |
| Arunachal Pradesh / India reference, C042 | E07/E08/E44 дают current evaluator PAP certificate; E50 control/claim record historical и не нужен этому witness. | W использует territorial permit mechanism; claim blindness проверяется удалением E50/claim labels при сохранении E07/E08/E44. Scope certificate — ordinary reference vs PAP scope, не India целиком. |
| Siachen / Ladakh, C043 | E54 qualified **base camp** publication 2023; E55 military presence report 2024; glacier access/geometry unknown. | Base camp не равен glacier; unit military presence не J. Q007/Q005/Q008 сохраняются, отсутствие гражданского доступа не приравнивается к доказанной территориальной legal prohibition. |
| Shaksgam / Aksai Chin, C044; Shaksgam / GB, C045 | E51 — verified **claim statement**; E52 qualified control description; E50 historical и E53 provisional. | Verified statement о claim не есть verified sovereignty или civilian competence. Различие сравниваемых control sides не заменяет admission dossier. W/J не доказаны; law/access и geometry gaps не закрывает identity. |
| LoC/LAC affected areas, C046/C047/C049 | Смешаны reference scopes и overlays; нет единого доказанного civilian regime всей полосы. | Использовать scope конкретного permit/prohibition/competence; не claim line или blanket boundary-zone identity. Военные и administrative карты не дают legal access effect автоматически. |

Для Western Sahara маршруты уже разделены в [route-matrix](route-matrix.json). E42 Morocco–Algeria closure не переносится на Algeria→east/south, Mauritania→east/south или west→east. `no ordinary route established` — неизвестность, а не `all civilian access prohibited`. Ни planned road, ни entry stamp, ни advisory buffer не устанавливают новую admission jurisdiction.

Таким образом, дополнительные geographic facts могли бы разблокировать W/J в отдельных случаях. Они **не отвечают** на оставшийся normative вопрос: требуется ли сохранять международно-правовую отдельность при полной operational equivalence. Это точный предмет Q006, а не повод бесконечно искать ещё один travel witness для ожидаемого имени.

## 8. Candidate Stage 1 rule set

### 8.1. Один минимальный рекомендуемый core

```text
candidate_core_v1 := CR-W OR CR-J

CR-W := proven hard territorial TravelDecision discontinuity
CR-J := proven independent final territorial admission competence difference
```

`OR` означает достаточность одного сертификата, не необходимость обоих. Это **candidate P2 with stricter gates**, не идентичный existing P2 implementation. Ни `territorial_identity`, ни `disputed`, ни голый `controller_id` не входят в core signature. Предлагаемый `CR-C` control-only separator не включён: qualifying access consequences относятся к CR-W, qualifying admission institutions — к CR-J; независимый остаток не определён.

### 8.2. Общие scope, evidence и temporal gates

**G-SCOPE.** Сертификат содержит nonempty disjoint scopes A/B, либо два disjoint fragments внутри исходных reference objects. Указанные решения/competence однородны на каждом сертифицируемом фрагменте. Witness между двумя точками не доказывает, что никакие точки двух крупных heterogeneous objects не могут находиться в одной cell. На перекрывающиеся A/B нельзя буквально применить R008: точку их пересечения невозможно отделить от самой себя. Administrative polygon допустим только как evidence-backed exact scope/proxy с заявленной точностью. Неизвестная geometry не дорисовывается; partial certificate не выдаётся за полный partition.

**G-CONTEXT.** Версия S сохраняет civilian short-stay, rare documents и class-based special permissions; исключает work/settlement/diplomatic/military missions из primary split. Нельзя менять scope отдельно для конкретной пары. Условия C и исключения policy явно проверены; selection по частоте, имени лица или desired destination отсутствует.

**G-HARD.** В core входят следующие decision outputs, когда они имеют юридический эффект территориального допуска/пребывания лица: accepted travel document; visa/ETA/territorial admission authorisation requirement и validity; eligibility/prohibition of entry; general conditions/duration/termination of civilian stay; permit to enter/be present in a territorial scope; class-based legal entry/exit-route obligation. Названия документов, officer labels, штампы и office logistics не являются outputs. Пограничная физическая процедура сама по себе не hard; нормативная обязанность, влияющая на территориальный допуск, может быть hard.

Territorial presence permit определяется через **объект регулируемого действия**: правило запрещает entry/presence соответствующему классу лиц в описанном scope как таковое. Site/activity permit регулирует пользование объектом, facility, услугой или занятием и сам по себе не меняет territorial admission/stay title. Issuer может быть общим; permit boundary может лежать внутри province. **Ни размер, ни покрытие whole administrative unit не являются доказательством.** Для пограничных parks/reserves/base/exclusion zones, где текст одинаково допускает обе интерпретации, нет автоматического ответа: dependency `Q005/Q009`, `model_unresolved`. Это намеренно узкое sufficient ядро, а не заявление о закрытии всей границы region/overlay. Customs/biosecurity/fiscal differences отдельно остаются Q004.

**G-TIME.** Предлагаемый sufficient stability test: constitutive/standing instrument действует на t, регулирует повторяемые классы admissions/presence и не активирован исключительно конкретным incident/emergency/event order. «Standing» не означает старше N дней или без expiry: новая вступившая в силу jurisdiction подходит сразу, нормативная sunset clause сама по себе не исключает действие. Однодневное закрытие из-за события, единичный патруль, временный quarantine order или погодный hazard сохраняются как overlays в этом candidate. Продолжительная emergency мера не становится standing из-за прожитых дней. Если невозможно доказать тип меры или только de facto observations без institutional rule, candidate stability не установлена; Q008/Q007. Это новая предлагаемая конвенция institutional kind, а не доказанная полная теория устойчивости. Она может оставить долгие severe restrictions overlays — явная цена узкого core.

**G-EVIDENCE.** Для каждой premise нужны source record, locator/excerpt, компетенция источника именно по этой premise, as-of/validity, geographic scope и достаточный assessment. Guidance, claim statement, historical observation и constitutional law не взаимозаменяемы. Верификация «источник сказал X» не доказывает более сильное Y. Source conflict сохраняется как data blocker. Evidence-backed derivations допускаются с опубликованными steps; создание нового empirical record в этом review не требуется и не выполняется.

### 8.3. Сепараторы и намеренные пределы

| ID | Operational predicate | Evidence requirements | Почему hard | Контрпримеры / намеренно не разделяет |
|---|---|---|---|---|
| CR-W | G-SCOPE/G-CONTEXT/G-HARD/G-TIME/G-EVIDENCE выполнены; существует один admissible matched C и hard d с доказанно разными D на A/B. | Applicable нормы обеих сторон, nonempty context, все влияющие exemptions, конкретный differing output, territorial effect, standing basis/time и scope certificate. | Одна hard decision function не может верно описать обе стороны. | Совпадение D при разных именах органов; разные очереди/ports/carriers без territorial legal effect; named individual decisions; closed-by-weather; неопределённые permit overlays; status-only difference. |
| CR-J | Общие applicable gates и J1–J6; доказанно различаются нормализованные final admission competence structures на A/B в одном S/t. | Constitutive allocation, territorial legal effects, reserved decision powers, non-substitution/override audit, attribution/delegation/review graph, effective application; для de facto — civilian operational corroboration. | Принятый candidate invariant: одна cell не скрывает две самостоятельные системы final territorial admission responsibility. | Несколько local offices, общий visa contractor, штампы, административная автономия без competence; разные legal-status labels с одной competence; military-only control. |

CR-W и CR-J — два отдельных достаточных способа доказательства: одна competence может вводить разные territorial document rules (W без J); при допущении полных равных D разные independent capacities дают только J. Их фактическая неустранимая независимость для окончательного S/H **не доказана** текущим набором. Если S/H включает все территориально специфичные leave/refusal histories и разрешения, constitutive difference иногда позволяет вывести W; такой случай не доказывает дополнительного покрытия P2. Если же `HardTravelDecision` прямо включает identity decision-maker, J можно записать внутри одной формулы, но нормативное добавление institutional dimension от этого не исчезает.

Поэтому «минимальный» здесь означает два явно обоснованных certificate types без третьего неопределённого identity/control основания. Это не теорема о минимальном числе независимых axioms при любом будущем traveller scope. Для утверждения strict extra expressiveness P2 synthetic «полные равные D, разные J» должен быть согласован с exact S/H; нельзя постулировать D equality, одновременно игнорируя вытекающий из J legal-travel witness.

### 8.4. Equality, unknown и construction

Полная candidate signature — `Sigma(X) = (D_X over S/H, J_X over S)`, вместе с доказанными scope/time applicability и completeness. Две signatures равны только после positive coverage audit всех включённых dimensions и competence relations; одинаковые policy IDs достаточны лишь при доказанной общей применимости и отсутствии разных exceptions. Не требуется бесконечно перечислять людей: можно доказать общую применимость одного нормативного набора и покрытие его predicates. Несколько совпавших witnesses или пустой список permits такого доказательства не дают.

Отсутствие CR-W/CR-J certificate не создаёт ни boundary, ни compatibility. Сохраняется порядок contract: normative conflict → sufficient split → consequential model blocker → concrete data blocker → complete equal signature → separation not proven. Неопределённость другого фактора не отменяет готовый split. Из нового core исключены rejected identity/control-only predicates, поэтому они сами не блокируют его equality; нерешённая классификация потенциально hard permission или legitimacy/applicability всё ещё блокирует. Compatibility всегда помечается candidate profile/version и не выдаётся за исполнение D004/D007 или более широкого будущего Stage 1.

Даже правильный pairwise separator ещё не задаёт coarsest partition при неполноте: если доказано только A≠B, а отношения C неизвестны, совместимы и `{A,C}|{B}`, и `{A}|{B,C}`. Нельзя выбирать одну по названию или считать connected components графа «нет запрета» equality classes. Complete function/structure equality транзитивна; `separation_not_proven` — нет. Поэтому review не строит partition и не обещает complete release из текущих 147 результатов.

### 8.5. Invariant audit

| Invariant | Проверка candidate | Результат / предел |
|---|---|---|
| Name blindness | Germany→A, France→B; переименовать authority IDs и clauses references согласованно, сохранить allocation и D. | Outcome неизменен; hard IDs не должны кодировать curated inclusion. |
| Claim blindness | Добавить/удалить claim и recognition labels при прежних independently applicable D/J. | Outcome неизменен. Новый доказанный legal obligation — изменение D, а не чистое изменение claim. |
| No destination leakage | Madeira получает туристическую известность при прежних D/J. | Нового Stage 1 certificate нет; final classification не определяется. |
| No island rule | Сделать equal-signature scope островом/архипелагом без других изменений. | Нового сертификата нет; MultiPolygon допустим по hard dimensions. |
| No administrative-boundary rule | Bavaria/Tuscany/обычная province получает новый administrative label или office. | Нового сертификата нет. Доказанная собственная final admission competence даёт J по тому же тесту, что везде. |
| Open world | Удалить evidence одной обязательной premise или заменить equality audit выборкой. | Нет автоматически ни split, ни equality; соответствующий blocker/неполная signature. |
| Monotonicity | Любая later subdivision пересекает proven Stage 1 certificate. | Такой Stage 2 output недопустим; каждая cell должна лежать в одной Stage 1 cell. Изменения между временными releases рассматриваются отдельно. |

Это логический аудит предложенных предикатов, не запуск нового evaluator. Existing implementation и fixtures не менялись.

## 9. Counterexamples and failure modes

| Failure mode | Контрпример | Требуемое поведение |
|---|---|---|
| «Только office отличается» | Два офиса имеют разные chiefs и statutory service districts, но одинаковый admission title; director может распределять и заменять cases. | J4/J5 не выполнены; нет CR-J. Не считать географический office jurisdiction самостоятельным territorial admission. |
| «Parent может когда-нибудь отменить закон» | Constitutive instrument даёт X собственную capacity; parent legislature может изменить instrument, но действующее право не даёт capacity B решать за X. | Не отклонять J из-за ultimate sovereignty. Проверяется competence **по действующему** instrument. |
| «Общий minister/visa issuer — одна jurisdiction» | Один minister действует в двух раздельных capacities или external contractor обслуживает их. | Анализировать attribution, territorial effect и substitution; person/issuer equality недостаточно. |
| «Согласованная visa policy — одна competence» | Полные D равны, но две reserved capacities не могут принять решение друг за друга. | CR-J даёт split; это ровно дополнительный нормативный выбор P2. |
| «Разрешение охватывает province целиком» | Те же правила сначала охватывают половину province, затем province переименована/перекроена так, что permit scope совпал с ней. | Смена administrative coincidence не меняет hard effect; gate смотрит regulated act/scope. Иначе C042 превращается в curated administrative rule. |
| «Любой permit — territorial» | Обязательное разрешение на использование landing facility, trekking или посещение парка. | Сам факт permit не split. Site/activity effect исключён; неоднозначный presence prohibition оставляет Q005/Q009, без догадки по имени/размеру. |
| «Редкий документ не считается» | Единственный реально используемый документ класса имеет доказанно другое territorial acceptance rule. | При admissible S и остальных gates W всё равно применяется. Убирать его по частоте запрещено. |
| «Два офицера отказали по-разному» | Одна и та же норма допускает discretion; разные события дают разные исходы. | Outcome events не являются разными policy functions. Нужна доказанная difference in legal requirements/permissions. |
| «Нет гражданских маршрутов — всё закрыто» | Маршрут не исследован либо дорога отсутствует. | Unknown/transport facts не становятся legal prohibition; закрытые точки остаются в U. |
| «Стабильность = давно» | Новая standing admission capacity существует один день; emergency restriction длится годы. | Первая может пройти G-TIME сразу; второе не проходит только из-за возраста. Это published candidate convention, не универсальное решение Q008. |
| «Control boundary сохраняет весь dispute» | X и Y внутри status object имеют разные regimes; X и обычная территория Z того же controller могут иметь одинаковые W/J. | X/Y separation не доказывает X/Z. Остаток Q006 не устраняется количеством internal splits. |
| «Суды или recognition всё решают» | Две capacities имеют общий court; либо de facto authority не признана третьими сторонами. | Общий court не equality; recognition count не gate. Неизвестная effective admission competence остаётся неизвестной. |
| «Verified evidence доказывает весь вывод» | E23 подтверждает permit issuance, E51 — что claimant сделал statement. | Не повышать их до non-substitution либо internationally valid sovereignty. Premise-level proof отдельно от source reliability. |
| «Не нашлось boundary — можно объединить» | Имеется только конечная выборка общих visa rules. | Signature incomplete; не `hard_compatible`. Доказанная разница не транзитивна, недоказанность различия также не equality. |
| «Можно сравнить aggregate со своей частью» | C033/C034 либо буквальный whole-India / Arunachal. | Нужен disjoint scoped certificate; не разрешать impossible self-separation. Pairwise result — ещё не geometry instruction. |

### Минимальный различающий experiment без новых geographic facts

Следующий шаг — **synthetic normative contract experiment**, описанный в YAML как `normative_experiments`. Он не изменяет текущие fixtures и не использует реальные expected regions как oracle. Два базовых record bundles имеют одинаковую полную D function; меняется только attribution/competence structure:

Предварительный gate: проверить логическую совместимость предпосылок каждого bundle с exact S/H, включая validity чужого leave, local refusal histories и recognition arrangements. Если заявленное J difference само влечёт различие включённого D, bundle не является equal-D counterexample и должен быть отклонён как неконсистентный, а не засчитан за P2. Expected ниже условны на этот gate; это не утверждение существования соответствующей реальной пары.

1. **NX-01: independent capacities.** Два constitutive territorial titles, reserved powers, no ordinary cross-capacity substitution, effective scopes. P1 при положительно полной D equality даёт compatibility; proposed core даёт CR-J. Этот случай изолирует нормативную полезность jurisdiction без поиска редкого visa witness.
2. **NX-02: offices.** Всё то же на уровне staff/location, но один territorial title и единая substitutable administrative chain. Core не даёт J; при полном равенстве остальных dimensions — compatibility. Отличие NX-01/NX-02 должно объясняться J1–J6, а не labels «country/province».
3. **NX-03/NX-04: совпадение против независимости.** Общая capacity с различными standing visa rules даёт W; разные capacities с равными rules дают J даже при общей apex court/visa processor. Это проверяет минимальность обоих оснований.
4. **NX-05/NX-06: status/control only.** При полном равенстве D/J меняются legal-status/claim labels либо только military patrol actor. Core совместим; никакого W/J. Если требуется mandatory split, должно быть названо отдельное правило и его general proof obligations. Старый accepted answer не добавляется как derivation.
5. **NX-07/NX-08: evidence и permits.** Удаление J4 evidence оставляет data unknown; permit с нерешённой territorial/site semantics оставляет model unresolved. Это проверяет, что строгий predicate не заполняется intuition.
6. **NX-09/NX-10: редкость и время.** Class-based редкий документ с standing territorial difference даёт W; temporary event closure при остальных complete equal core dimensions не даёт core split. Требования однородности и temporal convention становятся проверяемыми отдельно.

Для каждого bundle повторить биективное переименование всех territory/authority IDs, перестановку записей и A/B swap. Все expected результаты выводятся из опубликованных candidate predicates; реальные constraints используются только для отчёта о coverage/conflict. Acceptance criterion: принят или отвергнут именно институциональный инвариант NX-01; каждый из NX-02/NX-04 объясняется одним J-definition; явно принято, что NX-05/NX-06 не даёт hard split без дополнительного правила. При споре об извлечении J1–J6 минимальное дополнительное действие — premise matrix по **существующим** E02/E03/E18/E20/E21/E23 с `entailed / not_entailed / unknown`, без нового geographical research и без требования сохранить старые counts.

Этот experiment не может эмпирически доказать, что продукту *должна* нравиться NX-01. Он делает нормативный выбор конкретным и проверяет внутреннюю согласованность, которой не даст увеличение числа geographic cases.

## 10. Q001 disposition

**B — Q001 can be narrowed.** Рекомендуемое решение для последующего нормативного утверждения:

> Stage 1 требует separation при достаточном доказательстве territorial hard TravelDecision discontinuity в опубликованном civilian scope либо при достаточном доказательстве разных самостоятельных конечных territorial admission competencies. Rare admissible classes сохраняются. Authority identity устанавливается по legal capacity, territorial effect, reserved competence и non-substitution, с отдельным доказательством effective application. Неопределённые identity, dispute, dependency, autonomy и control labels не являются дополнительными hard dimensions.

| Часть вопроса | Результат review | Что остаётся |
|---|---|---|
| P1 как sufficient foundation | Рекомендуется сохранить W и existential witness; частотный порог не нужен. | Принять exact S/H и границы territorial permits/routes, Q002/Q005/Q009; классифицировать temporal measures, Q008. |
| P2 independent competence | Рекомендуется отдельный hard invariant J с J1–J6; current visa equality ему не мешает. | Принять этот нормативный выбор; проверить operational distinction на NX-01/NX-02 и premise audit, не объявлять existing Boolean полным dossier. |
| P3 identity | Отклонить **в текущем виде** для production; не заменять registry/proxy. | Любой будущий exact legal-status predicate должен пройти самостоятельное обоснование и counterexamples, а не дополнять vague P3. |
| Stable control | Голый controller difference недостаточен; W/J consequences допустимы без recognition gate. | Shared/noninstitutional civilian control — Q007, stability — Q008, unresolved access classification — Q005/Q009. |
| Disputed-status preservation | Claim/dispute alone отвергнуты как separator; D007 и tentative D013 не гарантированы при operational equality. | Q006: отдельный legal-status hard rule или явное ограничение гарантии; D004 blanket и Antarctic conflict также Q011. |

**Почему не A:** нет согласованного общего способа одновременно гарантировать blanket D004/D007 и сохранить только W/J без исключений; часть hard/access/stability boundary ещё требует model semantics. Review предлагает strict sufficient core, но не доказал его полноту как всего нормативного Stage 1. **Почему не C:** выбор существенно сужен — vague identity и control-only не получают production semantics, P1 existential сохранён, P2 имеет проверяемый sufficient dossier, а остаточный конфликт сформулирован на полностью равных W/J inputs. «Нужно больше данных» не является ответом на этот конфликт.

Статус B здесь является рекомендацией review. [Open questions](../../docs/open-questions.md), normative spec, decisions, factual records и current evaluator не изменены. Неисполненные constraints не закрыты автоматически и не перенесены в Stage 2 под обещание будущего решения.

## 11. Required spec/decision changes

Ниже конкретные предлагаемые patches для отдельного этапа утверждения; **в этом изменении не применены**. Существующие stable R/D IDs и accepted пользовательские требования сохраняются, пока пользователь явно не меняет их. Новые формализации не получают `accepted` только потому, что этот review их рекомендует.

1. **R007/R012, Q002 — existential scope.** Уточнить текст: «Сертификат использует непустой непротиворечивый class-based civilian short-stay context, полный по влияющим predicates. Частота класса не влияет на достаточность. Сравниваются определённые hard requirements/permissions, а не индивидуальные discretionary events. Список hard outputs, исключённые activity/site outputs и версия scope публикуются». Добавить matched-route mapping и правило, что refusal одной стороны допустим как witness outcome.
2. **R008/R009/R028/R038 — certificate scope.** Добавить: «Scope A/B каждого separation certificate непустой и непересекающийся; evidence доказывает соответствующий hard effect на всём сертифицируемом scope. Heterogeneous/reference/aggregate inputs требуют явных fragments. Один witness не распространяется на whole containing entity». Сохранить order independence, complete-signature equality и unresolved при нескольких coarsest partitions. Это последующая contract/adapter работа, не patch implementation сейчас.
3. **R011 — заменить краткую самостоятельность operational definition.** Включить J1–J6 из §4.2, capacity/holder distinction, normalized delegation/assent/review graph и positive non-substitution audit. Явно исключить office, issuer, service district, patrol и merely legislative autonomy. Указать: «Общая policy, recognition of leave, apex court или ultimate parent legislative power сами по себе не устанавливают равенства competence; обязательна атрибуция конкретных case powers».
4. **R010/R038/R042, D010/D029, Q001.identity — вывести undefined P3 из proposed production core.** Текст: «Territorial/legal identity не входит в hard signature без отдельного принятого operational rule. P3 сохраняется как нерешённый исторический experimental profile; status-only hypotheses рассматриваются в Q006. Registry/ISO/category flags не подменяют general predicate». Сохранить принятое различие territorial/legal vs destination identity; не трогать definition Stage 2.
5. **R013/R014/R017/R027, Q004/Q005/Q009 — явно определить достаточное hard ядро и нерешённый край.** Добавить G-HARD regulated-act/territorial-effect gate: port of processing не равен scope admission, whole-province permit не hard по administrative coincidence, site/activity outputs исключены, неоднозначная territorial presence restriction даёт model blocker. Не объявлять все parks overlays либо все permits separators по имени. Q004 остаётся отдельным вопросом.
6. **R015/R023/R024/R039, D008/D014, Q007 — control evidence.** Уточнить: «Control observation само по себе не hard separator; достаточны доказанные scoped admission/legal-access consequences по CR-W либо effective independent admission competence по CR-J. Civil, border, military и enforcement roles раздельны; recognition не gate». Если нужен третий самостоятельный control predicate, сначала определить его сверх W/J и проверить military/local-office counterexamples. D014 не превращать в требование ровно двух cells.
7. **R016/R022/R024, D006/D007/D013, Q006 — status-only conflict.** Добавить явную regression matrix: D006 относится к сравнению с ordinary Ukraine; D013 с Russia tentative; west/east не доказывает west/Morocco. Предлагаемый текст Q006: «При полных равных W/J core не гарантирует отдельности legal-status object. Требуется отдельный general legal-status separator либо изменение обязательности этого product constraint. До решения constraint остаётся незакрытым». Не снижать D007/D006 с accepted и не считать dispute overlay выполнением separate-region requirement.
8. **R018/R019/R026, D004/D016, Q011 — category guarantees.** Добавить: «Не наследовать metropolitan policy без evidence. Overseas/dependency label не создаёт split. D004 blanket coverage не доказано core; Antarctic claims не становятся cells из категории. D016 остаётся предложением, а не принятой exception». Не выводить вывод для всех UKOT из C012 или Crown Dependencies.
9. **R031/R033, Q008 — candidate time convention.** Предложить G-TIME как sufficient standing/constitutive test без duration/frequency threshold; incident measures остаются overlays, не становятся hard от возраста. Зафиксировать цену этого выбора для prolonged restrictions. До adoption неоднозначные temporal cases остаются unresolved. R041 не интерпретировать как запрет изменения boundary между временными releases.
10. **Q001, D020/D025 и evaluator-contract — disposition и версия.** После adoption записать Q001 как narrowed с CR-W/CR-J core и указанными остаточными dependencies; следующий experiment — NX-01–NX-10. Новый profile/version должен отделять premise-level proof от current assertions. Не задним числом менять spec version у 147 results; любые новые certificates потребуют новой versioned derivation. `hard_compatible` остаётся profile-relative положительным Stage 1 outcome, не final merge.

R003–R005, R040–R041 и D023–D028 в части утверждённой архитектуры изменения не требуют. Новая world partition, Stage 2 implementation, новые geographic facts, curated exceptions и автоматическое сохранение старых expected regions в эти patches не входят.
