# Canonical Travel Regions — рабочая спецификация

Версия: 0.2.0-draft. Дата: 2026-09-12. Статус: экспериментальная спецификация, не утверждённая мировая классификация.

## Основание и границы достоверности

Документ опирается на пользовательское задание от 10 сентября, текущее задание, две прочитанные версии Deep Research и найденный фрагмент архитектурного обсуждения. Источники и степень принятия решений перечислены в [decisions.md](decisions.md). Полный транскрипт архитектурного диалога не восстановлен. Конкретный язык реализации, СУБД, геометрический движок и поставщик геоданных не считаются выбранными.

Исследования расходятся: первая версия преимущественно определяет территории через travel regimes, вторая добавляет самостоятельную territorial identity. Формулировка «минимальная практически полезная территория» не задаёт однозначного алгоритма: произвольное дальнейшее дробление тоже сохраняет однородность. Здесь предлагается **наиболее крупное разбиение, сохраняющее все обоснованные обязательные различия**. Это новая формализация, а не ранее принятое решение.

Каждый нормативный пункт имеет неизменяемый ID. `accepted` означает прямое требование пользователя; `tentative` — рабочую гипотезу, действующую внутри эксперимента; `unresolved` — предикат, для которого пока нельзя честно выдать окончательное решение. Статусы правил не являются оценкой достоверности географических фактов. Ссылки Qxxx ведут в [open-questions.md](open-questions.md).

## Цель, universe и partition

### R001 — Назначение системы [accepted]

Система строит воспроизводимое одноуровневое разбиение пространства для учёта и планирования путешествий. Она должна объяснять каждое разделение ссылками на общие правила и входные факты. На этом этапе результатом служат спецификация и контрпримеры, а не окончательный список мира.

### R002 — Явный universe [tentative; Q003]

Universe задаётся отдельной версионируемой маской U, а не списком стран и не перечнем доступных туристам мест. Рабочий профиль `LAND_V0`: вся постоянная суша на опубликованную эпоху береговой линии, включая острова, пустыни, закрытые территории, искусственную намытую сушу и Антарктиду. Внутренние воды включаются отдельной маской. Заземлённый ледниковый покров входит; плавающий морской лёд, шельфовые ледники, морские воды, воздушное пространство и подземные объёмы пока вне этого профиля. Пограничные типы features должны быть явно размечены, а не выпадать при загрузке.

LAND_V0 — ограничение первого эксперимента, **не утверждение, что все возможные путешествия ограничены сушей**. Буквальное покрытие поверхности Земли требует другого universe и решения Q003. Сборка без опубликованной маски, эпохи и определения shoreline считается неполной.

### R003 — Exhaustive coverage [accepted]

Для фиксированных U и момента t объединение регионов равно U. Любая точка U назначается ровно одному региону. Отсутствие населения, разрешения на посещение, признанного суверена или геоданных не освобождает от требования покрытия. Эксперимент может показать неразрешённый участок, но не выдавать его за завершённую каноническую классификацию.

### R004 — Mutually exclusive regions [accepted]

Множества точек регионов попарно не пересекаются. В файловом представлении замкнутые полигоны могут иметь общие рёбра и вершины; владение этими точками устанавливает R029. Пересечение положительной площади запрещено. Ненулевой overlap нельзя скрывать порядком отрисовки.

### R005 — Single-level hierarchy [accepted]

Между одновременно действующими canonical regions запрещены отношения включения parent/child. Политические сущности, архипелаги, исторические области, disputed areas и policy areas существуют в других типах объектов. Связи с ними допускают many-to-many и пересечения. Историческая связь predecessor/successor не является иерархией текущих регионов.

Stage 1 and Stage 2 are construction stages, not levels in the published ontology. Only the Stage 2 output is the final Canonical Travel Regions partition, and that output remains single-level.

### R006 — Определение canonical travel region [tentative; Q001]

Canonical travel region — непустой класс точек U в опубликованном Stage 2 разбиении, имеющий стабильную идентичность, геометрию на момент t и явные связи с применимыми travel policies, legal-status records и control records. Внутри класса не остаётся доказанного обязательного разделения по выбранной версии спецификации. Условия поездки вычисляются без неявного наследования от другого canonical region.

Canonical означает «однозначный результат при фиксированных правилах, фактах и параметрах», а не «единственно правильное природное деление». Отдельная территория не означает отдельного государства. Регионы могут иметь MultiPolygon-геометрию.

## Formal construction procedure

### R007 — Контекст путешественника и проверяемое различие [tentative; Q002]

Контекст C содержит гражданства, документы и их типы, резидентство, цель, длительность, предыдущие поездки, маршрут, точку въезда, способ транспорта, сопровождаемые товары/животных и дату. Базовая область эксперимента: гражданские краткосрочные посещения, включая редкие документы и специальные разрешения; работа, переселение, дипломатические и военные миссии не образуют первичный split. Ограничение длительности задаётся применимой политикой, а не универсальными 90 днями.

TravelDecision различает admission, требуемое разрешение, принимаемые документы, условия пребывания/выезда, обязательные процедуры, физическую доступность и законность по каждой релевантной юрисдикции. Для split по различию условий нужен **witness**: конкретный допустимый C и два назначения A/B, для которых отличается существенное решение. Маршрут сравнивают по одинаковому классу поездки; само различие координат destination или названий аэропортов не является witness.

### R008 — Сертификат обязательного разделения [tentative]

`must_separate(A,B,profile)` and `hard_compatible(A,B,profile)` are independent Stage 1 predicates. `must_separate` means sufficient positive evidence forbids A and B from occupying one final canonical travel region under the selected profile. `hard_compatible` means positive evidence establishes equivalence across the profile's complete hard signature and no mandatory-separation certificate applies. It means only that Stage 1 requires no boundary between A and B. It does not decide whether Stage 2 places them in one final region. `not must_separate` does not imply `hard_compatible`.

Каждое `must_separate(A,B,profile)` содержит rule_id, profile, географический scope A/B, as_of, проверенные предпосылки, факты с источниками и либо witness R007, либо разрешённое выбранным profile институциональное основание R010/R011. Для regime-based split witness должен входить в scope R007, относиться к hard dimension, иметь достаточное evidence и не сводиться к local overlay или детали конкретной точки входа. Слов «особый», «удалённый», «существенный» без операционального доказательства недостаточно. Неизвестная предпосылка остаётся неизвестной, а не превращается в false.

`must_separate(A,B)` означает, что ни один итоговый регион не содержит точки обеих областей. Это не обещает, что A целиком станет ровно одним регионом: возможен дополнительный split внутри A.

### R009 — Two-stage partition construction [accepted; Q001, Q005, Q012]

1. Fix U, time, rule profile, and facts. Build candidate geometries without using desired output names.
2. Build their common geometric refinement as technical atoms. These atoms are not user-visible regions.
3. Stage 1 computes the coarsest partition that satisfies every accepted mandatory-separation constraint. For each atom, evaluate the selected profile's hard signature as specified by R038.
4. `signature_complete(A,profile)` is true only when every required profile dimension has an evidence-backed `known_value`, `known_absence`, or justified `not_applicable` state. `unknown` and `unresolved_model_semantics` make the signature incomplete.
5. `signatures_equal(A,B,profile)` can be true only when both signatures are complete and every typed hard dimension is equal. A finite set of traveller examples cannot prove completeness.
6. `hard_compatible` requires complete equal hard signatures and no applicable `must_separate` certificate. Absence of a witness, an empty search result, and `not must_separate` are not positive compatibility evidence.
7. Stage 2 processes each Stage 1 cell independently and may subdivide it using destination-partition semantics. Stage 2 may never combine points from different Stage 1 cells.
8. The final canonical partition is the Stage 2 output. Stage 1 output is an internal construction boundary, not a final region assignment.

Hard-signature equality must be an equivalence relation, and Stage 1 must be order-independent. If hard constraints permit multiple coarsest partitions, the Stage 1 result is unresolved; names and political labels cannot break the tie. The rule for selecting the destination partition within each Stage 1 cell remains open in Q012.

### R010 — Самостоятельная territorial identity [unresolved; Q001]

Вторая версия исследования предлагает запрещать слияние устойчивых внешних территориальных юрисдикций даже при равных travel policies. Общего проверяемого определения «внешней» и «самостоятельной» идентичности пока нет. Ни ISO-код, ни собственный флаг, ни туристическая известность его не заменяют.

В эксперименте можно сравнить `regime_only`, `jurisdiction` и `jurisdiction_plus_identity`, но identity-aware profile обязан публиковать общий identity predicate или конкретный registry с основаниями. Ручной registry — явная гипотеза, не автоматически выведенное правило. Пока `Q001.identity` не закрыт, evaluator не угадывает identity по имени, статусу, ISO-коду или типу территории: когда outcome зависит от identity, он возвращает `model_unresolved` с `blocked_by_model: [Q001.identity]`.

### R011 — Immigration / admission jurisdiction [tentative]

Разные самостоятельные территориальные органы с конечной компетенцией решать обычный допуск, отказ и условия пребывания требуют split. Делегированное консульское представительство, отдельный офис и разная форма штампа не являются отдельной юрисдикцией. Нужно различать visa issuer, admission authority и enforcement authority. Совпадение краткосрочной визовой политики не отменяет институционального различия.

### R012 — Visa / immigration scopes [tentative]

Разные территориальные области действия визы, ETA, разрешения на въезд или допустимых документов требуют split, если выполнены R007/R008 и речь идёт о допуске на территорию, а не об отдельном объекте внутри неё. Достаточен один документированный класс путешественников; различие не обязано затрагивать большинство. Изменение требований одновременно по всей области обновляет policy, но не обязательно геометрию. Общая виза сама по себе не требует merge.

### R013 — Customs, biosecurity, fiscal scope [unresolved; Q004]

Таможенная территория, территория НДС, акцизная территория и биосанитарная зона — разные признаки. Один не выводится из другого. Рабочая гипотеза для эксперимента: обязательное декларирование сопровождаемого багажа, досмотр/карантин или ограничения ввоза при обычном перемещении через устойчивую территориальную границу могут требовать split; различие местной ставки налога недостаточно.

Не решено, почему этот тест должен отделять, например, специальную островную зону, но не каждую внутреннюю биосанитарную зону большого государства. Пока граница класса не определена, `customs-only` и `biosecurity-only` случаи дают `model_unresolved`, а не автоматический split. Customs никогда не подменяет immigration.

### R014 — Destination permits и специальные зоны [unresolved; Q005]

Разрешение, регулирующее доступ к месту внутри уже доступной traveller-facing admission jurisdiction, по умолчанию является spatial access overlay, а не основанием split. К этому классу относятся билеты и бронирования, пограничные и военные зоны, охраняемые объекты, локальные заповедники, закрытые маршруты и activity-specific permits. Их геометрия может пересекать административные границы или совпадать с целым муниципалитетом, районом и даже субъектом: площадь и совпадение с административной единицей сами по себе не превращают overlay в canonical region.

Такое локальное различие не является witness R007 между содержащей территорией и остальной частью той же admission jurisdiction: оно отвечает на `LocalAccessDecision(point_or_route,C,t)` после общего допуска, а не на `TravelDecision(destination,C,t)` о допуске в самостоятельное назначение. Overlay хранит собственные geometry, purpose, affected traveller classes, permit issuer и validity. Для пограничной или иной режимной зоны отдельно фиксируется, относится ли разрешение ко всей зоне, только к внутренней полосе, конкретному маршруту или виду деятельности.

Кандидатом split остаётся разрешение, которое регулирует обычный гражданский допуск в candidate territory как в назначение целиком, а не доступ к месту, маршруту или деятельности внутри неё. Общая проверяемая граница между whole-destination permit и крупным spatial overlay пока не определена. Размер площади, посещаемость, длительность разрешения и административный ранг не объявляются скрытыми порогами. Если исход зависит от этой границы, результат `model_unresolved`.

### R015 — De facto control [tentative; Q007]

Разные устойчивые фактические системы допуска и принуждения, меняющие въезд, документы, маршрут или физическое пересечение, требуют split по документированному operational scope. Простая смена подразделения, патруля или муниципальной администрации недостаточна. Контроль имеет вид деятельности и может быть совместным; вектор контролирующих полномочий предпочтительнее единственного поля controller. Неопределённая или подвижная зона контроля не превращается в точную линию без оговорки R030.

### R016 — Что само по себе недостаточно для split [tentative]

Административная граница, автономия, язык, этничность, религия, валюта, флаг, часовой пояс, ISO-код, политическое признание, территориальная претензия, отдельный штамп, островной статус, удалённость, туристическая идентичность, узнаваемость destination, itinerary usefulness и транспортное неудобство сами по себе не создают Stage 1 `must_separate`. Это не запрет split по другим hard основаниям и не запрет Stage 2 subdivision по destination semantics. Отрицательный тест означает «данный фактор недостаточен», а не «все остальные факторы отсутствуют».

### R017 — Overlays и независимость правил [tentative]

EU/Schengen/CTA и другие общие пространства — переиспользуемые versioned policies. Claims, признание, advisories, санкции, временные санитарные ограничения, маршруты, локальные access zones допускают собственную геометрию и пересечения. Поиск применимого overlay обязан учитывать точку/маршрут/C/t, а не только region_id.

Наличие overlay не отменяет hard split R011/R012/R015. Иначе любое неоднородное пространство можно было бы объявить одним регионом с произвольными вложенными проверками. Однородность R006 относится к утверждённым hard dimensions, не ко всем возможным местным правилам.

## Категории территорий

### R018 — Dependent territories [tentative; Q001]

Зависимость создаёт political relation и кандидата для анализа. Нельзя наследовать правила метрополии без подтверждённой ссылки на общий policy. Самостоятельная admission jurisdiction требует split по R011; статус зависимости без неё упирается в R010. Одна зависимая территория может содержать несколько регионов. Требование пользователя про UKOT сохраняется в D004 как product constraint, но конфликтующие claims не могут нарушать R004.

### R019 — Overseas territories [tentative; Q001]

Заморские части проверяются по отдельности независимо от формы конституционной связи: department, collectivity, overseas country и т. п. Расстояние от метрополии и принадлежность к семейству «French overseas»/«British overseas» недостаточны для конкретного merge или split. Неэквивалентные immigration scopes требуют разделения с метрополией по R012; взаимное объединение заморских частей проверяется отдельно.

### R020 — Autonomous regions [tentative]

Автономия не означает отдельный регион. Проверяются реальные полномочия допуска, разрешения, таможенные и специальные режимы. Одинаковый тест применяется к автономиям любых государств; политическая заметность не служит исключением. Åland, Hong Kong и Sicily — кандидаты с потенциально разными основаниями, а не один класс ожидаемого исхода.

### R021 — Geographically isolated territories [tentative; Q001]

Остров, эксклав и необходимость транзита через соседнее государство сами по себе не требуют Stage 1 split. При доказанной равной hard signature Stage 1 допускает MultiPolygon. Route graph сохраняет путь через другие регионы. Stage 2 may still split an island or remote area when future destination-partition rules justify it; that decision does not alter territorial/legal identity under R010.

### R022 — Disputed territories [tentative; Q006]

Спор создаёт самостоятельный объект dispute с геометрией и юридическими позициями, но не автоматически canonical region. Различие lawful routes, территориального допуска или фактического доступа может дать split по R012/R015. Признание и claim polygon не присваивают точки. Требование сохранить спорную область отдельно даже без этих различий остаётся unresolved Q006.

### R023 — De facto states [tentative]

Самостоятельная фактическая система территориального допуска оценивается по R011/R015 независимо от числа признающих государств. Контрпример: одинаковая граница и admission regime при изменившемся признании должны сохранять partition. Название государства и заявленный им весь контур не заменяют геометрию фактического scope.

### R024 — Occupation и disputed control [tentative; Q006, Q007]

De jure sovereignty/legal status, de facto control и traveller reality хранятся отдельно. Первое включает нормативное основание и позицию компетентного источника, а не только взаимозаменяемый список претензий. Второе описывает исполнение на местности. Третье содержит физический доступ и legality_under каждой релевантной юрисдикции; фактический пропуск не доказывает законности маршрута.

Если внутри спорной/оккупированной области существуют разные существенные operational regimes, она делится по R015. Отделение всей области от обычной территории контролирующего государства требует отдельного сертификата. Сам факт occupation не задаёт точный contour и число cells. Нельзя автоматически использовать административную границу области вместо фактической линии контроля.

### R025 — Uninhabited и закрытые территории [tentative]

Все их точки, попадающие в U, участвуют в partition. `visitability = closed/restricted/unknown` — свойство, не основание исключения. Необитаемость не требует отдельного region_id. Отдельные permits проверяются по R014. Отсутствие подтверждённого контролёра кодируется явно; соседство не даёт права автоматически присоединять территорию.

### R026 — Antarctica [tentative; Q003, Q005]

Базовая гипотеза: одна canonical cell для включённой в U антарктической суши южнее 60°S; national claims остаются пересекающимися overlays. Это рабочий выбор, не вывод «один договор = один регион». Станции и защищённые участки первоначально являются access overlays. Национальная авторизация экспедиции, зависящая от организатора/маршрута, не делит географию сама по себе. Доказанная территориальная admission boundary возвращает вопрос R014.

Область действия договора включает больше, чем сушу: Treaty Area нельзя безусловно приравнивать к геометрии этой cell. Antarctic portions TAAF, British Antarctic Territory и иных заявленных секторов не создаются вторым слоем canonical polygons. Это явное ограничение общего требования об отдельных overseas territories (D004/D016), а не скрытое исключение.

### R027 — Transit, preclearance и погранпункты [tentative]

Airside, портовая процедура, иностранный preclearance и штамп относятся к EntryPoint/EntryEvent. Они не перемещают физическую географию в другое государство. Въезд в иммиграционном смысле и физическое присутствие раздельны. Контрпримером к split служит аэропорт с разными правилами transit и landside без самостоятельной территориальной юрисдикции.

## Геометрия, время, воспроизводимость

### R028 — Выбор границы по основанию split [tentative]

Граница берётся из scope доказанного разделения: admission scope для R012, operational line для R015, соответствующая boundary для активного customs/permit профиля. Administrative polygon разрешён только как документированный proxy с точностью и основанием. Нельзя подменять operational line линией признания, границей advisory или цветом политической карты.

Пересекающиеся обязательные границы уточняют друг друга. Правило «последний полигон побеждает» и blanket precedence из первой версии исследования здесь **не принимаются**: они могут стереть другое обязательное различие. Противоречивые описания одной границы проходят R030/R034. Утверждённого универсального ранжирования всех поставщиков нет.

### R029 — Топология и точки на границе [tentative]

Сборка фиксирует CRS, координатную точность, snap tolerance, правила antimeridian/poles и engine version. Polygon interiors не перекрываются. Для общей линии/вершины геометрический lookup выбирает минимальный region_id по байтовому лексикографическому порядку из всех incident regions и возвращает `on_boundary=true`. ID не вычисляется из display name. Правило техническое и не выражает суверенитет.

Checkpoint lookup не переопределяет territory(point): отдельный запрос возвращает departure_region и arrival_region. Случай нулевой площади не должен создавать отдельную cell. Ни sliver, ни остров меньше tolerance не удаляется молча: ошибка/изменение маски и площадь регистрируются. Допуск вычислений не разрешает произвольные географические пробелы.

### R030 — Неопределённые границы [tentative; Q007]

Хранятся исходная оценка границы, uncertainty geometry/precision, дата и альтернативы. Approximate assignment допустим в явно provisional release с quality flag; это единственный технический ответ, но не точное знание контроля. Если даже такой выбор не имеет обоснования, сборка возвращает неразрешённую область отдельно и не получает статус complete canonical release. Неизвестная область не является автоматически buffer state или terra nullius.

### R031 — Temporal model [tentative; Q008]

Факт, policy membership, geometry и control record имеют `valid_from <= t < valid_to`, где открытый конец обозначается null. Отдельно хранятся `recorded_from/recorded_to`: когда система знала эту версию факта. `retrieved_at` и `last_verified_at` не заменяют время истинности. Неизвестная effective date остаётся неизвестной, а не датой загрузки.

Lookup задаёт world_time и release_id/knowledge_time. Историческая коррекция создаёт новую версию знаний, не переписывая опубликованный результат. Смена визового требования без изменения hard territorial scopes не требует нового region_id.

### R032 — Идентичность при split/merge [tentative; Q010]

Для чистого переименования и исправления оцифровки сохраняется region_id, меняется revision. При семантическом split старый ID закрывается, все новые регионы получают новые ID и `split_from`. При merge создаётся новый ID с `merged_from`. Старые ID не используются повторно. Пограничный перенос площади между сохраняющимися юрисдикциями меняет geometry revision и журнал события; если изменяется сама территориальная идентичность, применяется split/merge. Где проходит эта граница, проверяется Q010.

Событие посещения хранит время и географическое evidence отдельно от region_id на момент записи; пересчёт по новой карте не должен молча переписывать историю пользователя.

### R033 — Build manifest [tentative]

Воспроизводимая сборка фиксирует spec_version/hash, профиль, U/version/hash, world_time, knowledge cutoff, source snapshots/hashes, нормализованные facts, identity registry при наличии, code revision, зависимости/engine, геометрические параметры, test-set version/hash. Внешний URL без сохранённой версии не обеспечивает повторяемости. Детерминированная сериализация и порядок записей обязательны. Эксперимент на части мира явно публикует собственную test universe и не заявляет глобальное coverage.

### R034 — Provenance и неопределённость [tentative]

Каждый существенный факт содержит value, source locator, excerpt или reference, source_scope, временные поля и assessment. Различаются `model_unresolved`, `data_unknown`, `source_conflict`, `temporal_uncertainty`, `geometry_uncertainty`, `implementation_error`. Юридический источник, наблюдение контроля и правило перевозчика имеют разные компетенции; официальность сама по себе не делает источник пригодным для любого вопроса. Конфликт не снимается большинством ссылок. Claims и международно-правовая оценка также не смешиваются.

### R035 — Контракт эксперимента и falsification [tentative]

Stage 1 pairwise evaluator по каждой проверке возвращает comparison_id, profile, result, applied_rules, witnesses, completeness/equality signature, blocked_by_data, blocked_by_model, evidence_refs, explanation, spec_version и dataset_version. Его outcomes: `must_separate`, `hard_compatible`, `separation_not_proven`, `model_unresolved`, `data_unknown`, `rule_conflict`. `hard_compatible` is only a positive Stage 1 compatibility result, never a final-region merge instruction. `separation_not_proven` означает только отсутствие достаточного split-certificate при недоказанной hard compatibility; это не отрицание существования различия. `data_unknown` означает, что конкретная неизвестность или конфликт evidence блокирует оценку обязательной dimension. `rule_conflict` зарезервирован для несовместимых нормативных выводов, а не для простого расхождения источников.

Adversarial dataset может дополнительно использовать structural outcomes `no_split_on_stated_factor`, `must_refine` и `overlay_only`; они не являются pairwise ответами `hard_compatible`. Ни `separation_not_proven`, ни последние structural outcomes не считаются доказательством hard compatibility.

Гипотеза опровергнута, если при подтверждённых предпосылках нарушены её предсказания или accepted constraints. Неожиданный outcome регистрируется до изменения правила. Изменение правила применяется ко всему набору и сопровождается пересмотром контрпримеров, а не исключением по названию территории.

### R036 — Семантика adversarial dataset [tentative]

CSV содержит специально трудные **кандидаты/области тестирования**, включая вложенные aggregate/component cases; строки не являются готовыми регионами и не образуют partition. `parent_or_claimant` — описательная связь, не parent region и не исчерпывающая юридическая оценка.

`expected_result` — машинный outcome. `comparison_target` определяет, относительно чего он ожидается. `assertion` уточняет проверку; `premises` отделяет условные факты. `expectation_basis` принимает `user_constraint`, `rule_inference`, `conditional_rule`, `research_hypothesis`, `model_gap`, `intuition`. `confidence` оценивает обоснованность этого ожидания (high/medium/low), а `evidence_status` отдельно обозначает проверку фактов. Высокая уверенность в model_unresolved — не высокая уверенность в отдельности территории.

Проверка условной строки сначала подтверждает premises. Непроверенные premises дают `data_unknown`; это не failure правила. `no_split_on_stated_factor` не равен доказанному merge. `must_separate` не равен «ровно одна cell». Вывод из интуиции должен иметь basis=intuition, low confidence и не быть release gate. Для спорных мест требуется датированный factual snapshot перед запуском, а не интерпретация CSV как актуальной карты фронта.

### R037 — Структура минимальных данных [tentative]

Минимальные типы: RegionRevision; PoliticalEntity; LegalStatusRecord; Claim; ControlRecord; Policy/PolicyMembership; SpatialOverlay; BoundaryEvidence; SourceSnapshot; DecisionCertificate; SignatureAssessment; BuildManifest. Каждый temporal record ссылается на immutable evidence. RegionRevision содержит region_id, revision, names, geometry_ref, validity, signature_ref, provenance и quality. Каждая signature dimension хранит одно из состояний `known_value`, `known_absence`, `unknown`, `not_applicable`, `unresolved_model_semantics`; значение и evidence обязательны там, где они применимы. `known_absence` — положительно подтверждённое отсутствие, а не пустое поле. `not_applicable` содержит rule-based обоснование. Списки ссылок могут быть пустыми только при явном `unknown`, `not_applicable` или `unresolved_model_semantics`. Поле country не заменяет независимые отношения. Полноценный visa engine не требуется для первого эксперимента: достаточно проверяемых policies и witness cases.

### R038 — Open-world pairwise evaluator [tentative; Q001, Q002]

Pairwise evaluator работает в открытом мире: `no witness found != hard_compatible`, `unknown != false`, `not must_separate != hard_compatible`. Порядок проверки терминальных оснований детерминирован: (1) выявить конфликт нормативных derivations; (2) принять достаточный `must_separate` certificate; (3) вернуть `model_unresolved`, если неопределённый model predicate может изменить результат; (4) вернуть `data_unknown`, если конкретная data problem не позволяет оценить обязательную dimension; (5) принять `hard_compatible` только по полной равной signature; (6) иначе вернуть `separation_not_proven`.

Рабочие profiles для Experiment Q001:

- `P1 regime_only`: hard admission-decision scope, visa/document scope, релевантные hard permits и включённые profile route-dependent hard differences. Проверенный hard witness даёт `must_separate`; полные равные P1 signatures дают `hard_compatible`; отсутствие witness само по себе ничего не доказывает.
- `P2 jurisdiction`: P1 плюс final admission jurisdiction. Независимо подтверждённые разные конечные admission jurisdictions дают `must_separate`, даже если текущая visa policy совпадает. Merge требует равенства P1 signature и jurisdiction dimensions.
- `P3 jurisdiction_plus_identity`: P2 плюс identity discriminator. До закрытия `Q001.identity` P3 не содержит скрытого списка территорий; если P1/P2 уже не дали достаточный `must_separate`, зависимость от identity возвращает `model_unresolved`.

Этот минимальный состав signature нужен для реализации evaluator, но не закрывает вопросы о полном множестве hard outputs, customs, permits, route dependence и identity.

## Two-stage architecture

### R039 — Stage 1 Mandatory Separation [accepted]

Stage 1 establishes boundaries that the final partition may not cross. It considers only explicitly defined hard dimensions, including accepted traveller-facing admission, document, territorial legal/access, final-admission-jurisdiction, and materially relevant stable-control rules. Tourism identity, cultural identity, administrative subdivision, autonomy, island status, remoteness, transport inconvenience, destination recognizability, and itinerary usefulness do not create a Stage 1 boundary without an independent hard rule.

### R040 — Stage 2 Destination Partition [accepted; Q012]

Stage 2 receives each Stage 1 cell independently and may subdivide it using destination semantics such as geographic coherence, destination identity, itinerary coherence, travel graph or gateway structure, cultural-regional coherence, and stable traveller-facing destination concepts. These are first-class inputs to the final partition. This version does not define their algorithm, weights, thresholds, or completeness test.

### R041 — Monotonic refinement [accepted]

Let `Stage1Partition` and `Stage2Partition` be partitions of the same universe U. The required invariant is:

```text
Stage2Partition refines Stage1Partition
```

Equivalently, every Stage 2 cell is a subset of exactly one Stage 1 cell. If Stage 1 requires A and B to be separate, no later construction step may merge them. Stage 2 can only split Stage 1 cells.

### R042 — Territorial/legal identity and destination identity [accepted; Q001, Q006, Q012]

Territorial/legal identity concerns institutional status: separate legal or status entities, disputed international status, dependencies, constitutional territorial identity, and similar questions. It may become a Stage 1 hard separator only through an explicit accepted rule; Q001/Q006 remain unresolved. Destination identity concerns a coherent independent travel destination, traveller perception, itinerary structure, geography, and destination self-containment. It belongs to Stage 2. Neither concept implies the other, and P3 does not model destination identity.

### R043 — Project boundary [accepted]

This repository covers Stage 1 Mandatory Separation, Stage 2 Destination Partition, and their final single-level Canonical Travel Regions partition. Any finer subdivision beyond that canonical destination partition is outside this project's ontology and must not influence Stage 1 or Stage 2 rules.

## Проверки, которые должна реализовать первая сборка

| Check ID | Правила | Проверяемое свойство |
|---|---|---|
| V001 | R002–R004 | union(regions) == U; нет overlap положительной площади; пустые регионы запрещены |
| V002 | R005 | Нет текущих canonical parent/child и дублирующих aggregate cells |
| V003 | R028–R030 | Общие рёбра, вершины, дырки, antimeridian и полюса имеют детерминированный lookup |
| V004 | R007–R009, R038 | Каждый hard split имеет сертификат; `hard_compatible` имеет полную равную signature; перестановка входов не меняет результат |
| V005 | R016–R017 | Переименование, новые claims, смена advisory и открытие рейса сами по себе не меняют partition |
| V006 | R011–R012 | Общая visa policy не стирает разные admission jurisdictions; смена visa issuer при делегации не создаёт split |
| V007 | R022–R026 | Legal status и control независимы; overlapping Antarctic claims не дают overlapping regions |
| V008 | R031–R033 | Один manifest воспроизводит идентичный результат; историческая коррекция доступна отдельно; нет overlap интервалов одной revision stream |
| V009 | R034–R038 | unknown не превращается в false; отсутствие witness не становится `hard_compatible`; unresolved не засчитывается как определение региона |
| V010 | R008–R010, R038 | Одинаковые факты под заменёнными названиями стран дают изоморфный результат; ручной registry показан отдельно |

Эти проверки здесь специфицированы, но геометрический pipeline ещё не реализован. В этом выпуске проверены структура CSV и ссылки между документами.

## Проверенные внешние опорные источники

Это точечная проверка базовых различий, не повторная проверка всех примеров исследований. Дата обращения: 2026-09-11.

- E01: [France-Visas — France in the Schengen area](https://www.france-visas.gouv.fr/en/la-france-dans-l-espace-schengen). Подтверждает исключение неевропейских французских территорий из Schengen; отдельность Réunion от метрополии согласуется с R012. Из этого не следует взаимная отдельность всех overseas частей.
- E02: [European Commission — Territorial Scope](https://taxation-customs.ec.europa.eu/taxation/vat/vat-directive/how-does-vat-work/territorial-scope_en). EU/customs/VAT/excise — разные scopes. Réunion входит в EU customs territory, но не в общую VAT/excise territory. В исходных пересказах нельзя сокращать это до «Réunion вне таможенной территории ЕС».
- E03: [UN — Western Sahara](https://www.un.org/dppa/decolonization/en/nsgt/western-sahara). Подтверждает UN Non-Self-Governing Territory status, но не задаёт актуальную operational geometry и не доказывает двухчастное разбиение.
- E04: [Antarctic Treaty Secretariat — Antarctic Treaty](https://www.ats.aq/e/antarctictreaty.html) и [текст договора](https://documents.ats.aq/keydocs/vol_1/vol1_2_at_antarctic_treaty_e.pdf). Article IV сохраняет позиции по claims; Article VI описывает область южнее 60°S. Выбор одной land cell является нашей модельной гипотезой, а не требованием договора.
