# Canonical Travel Regions — decision log

Версия: 0.3.0-draft. Дата: 2026-09-12. Связанные документы: [spec.md](spec.md), [open-questions.md](open-questions.md).

Текущее нормативное решение о Stage 1 — D032–D037. Предыдущие research/experimental записи сохраняют историю, но не отменяют более позднее явно принятое CR-W-only ядро. D004–D007 остаются accepted product constraints.

## Как читать журнал

`accepted` используется только для явного требования пользователя. `tentative` означает предложение исследования или новую формализацию, принятую только как гипотезу этой спецификации. `unresolved` означает противоречие или недостаточно определённое модельное решение. Просьба исправить форматирование исследования не считается согласием со всеми его выводами. Исследование не является протоколом пользовательского утверждения.

## Источники исходных решений

| Source ID | Материал | Что действительно доступно |
|---|---|---|
| S01 | Пользователь, «Правила разбиения территорий», 2026-09-10 | Видимая исходная реплика: одноярусное непересекающееся полное разбиение, условная независимость, учитывать въезд; UK overseas отдельно; Réunion не объединять с France, Crimea с Ukraine, Western Sahara с Morocco в travel-смысле |
| S02 | «Глобальное одноуровневое разбиение мира на travel-territories», 2026-09-10 | Полностью прочитан отчёт, 985 строк; Library ID libfile_d734666989b48191ae91201e44ad6d07. Разделы «Критерии выделения», «Спорные, заморские и интеграционные случаи», temporal/provenance |
| S03 | «Глобальное одноярусное разбиение мира на travel territories», 2026-09-11 | Полностью прочитан отчёт, 2203 строки; Library ID libfile_d2bdf9e1b63c8191b5014d5ea8f0be2b. Добавляет отдельный territorial identity criterion и алгоритм safe merge |
| S04 | «Разница Кодекс и Ворк», 2026-09-11 | Видны пользовательские реплики о Linux, продолжении исследования, экспериментах и созданном Project; поиском найден фрагмент ответа ассистента от 19:16:20 UTC о Project/Work → спецификация/данные → git/Codex. Полного транскрипта нет |
| S05 | Текущее пользовательское задание, 2026-09-11 | Прямое требование четырёх файлов, стабильных rule IDs, falsifiability, 50–100 adversarial cases и запрет подгонки под желаемый список |
| N01 | Настоящая формализация | Новые инженерные предложения этого выпуска. Они не приписываются предыдущим разговорам |

Library ID приведены для точного поиска исходных отчётов. Внешние первичные источники E01–E04 и границы их проверки приведены в spec.md. S02/S03 фиксируют историю предложений; их географические утверждения не становятся автоматически актуальными проверенными фактами.

## Решения, подтверждённые пользователем

### D001 — Полное одноуровневое разбиение

- Решение: географическая область покрытия должна разбиваться полностью и без пересечений на один уровень территорий.
- Rationale: одна и та же посещённая точка не должна одновременно относиться к нескольким учитываемым территориям.
- Правила: R001–R005.
- Контраргументы: иерархия удобна для навигации и агрегирования, но её можно хранить вне canonical partition.
- Статус: accepted.
- Основание: S01, S05. Состав самого universe остаётся Q003, не accepted.

### D002 — Travel perspective и режим въезда

- Решение: условную самостоятельность оценивать с позиции путешественника; как минимум учитывать режим въезда.
- Rationale: государственная принадлежность не полностью описывает условия посещения.
- Правила: R006, R007, R011, R012.
- Контраргументы: «влияет на путешествие» без ограничения масштаба ведёт до парковок, охраняемых зон и отдельных объектов.
- Статус: accepted в части цели и включения въезда; конкретные пороги/достаточность отдельных факторов tentative.
- Основание: S01. Слово «как минимум» не означает согласия на любой customs/permit split.

### D003 — Воспроизводимость и проверка противоречий

- Решение: перейти от исследования к воспроизводимым экспериментам; не составлять сейчас финальную мировую карту и не подгонять правила под список.
- Rationale: общие критерии должны допускать опровержение.
- Правила: R001, R008, R033–R036.
- Контраргументы: конкретные примеры нужны как product constraints; следует сохранять их, а не считать любой ожидаемый исход запрещённым.
- Статус: accepted.
- Основание: S04, S05. Детальная структура manifest — N01, tentative.

### D004 — Британские заморские территории учитывать отдельно

- Решение: не считать British Overseas Territories обычной частью UK в travel partition.
- Rationale: явный пример желаемой условной территориальной самостоятельности.
- Правила: R010, R018, R026.
- Контраргументы: «каждая отдельно» не задаёт split внутри составной территории; Antarctic claims нельзя превратить в перекрывающиеся canonical cells. Crown Dependencies пользователь здесь отдельно не утверждал.
- Статус: accepted как исходное требование; универсальное применение и Antarctic exception unresolved, см. D016, Q001.
- Основание: S01. S03 расширяет это до общей identity model, но расширение не подтверждено пользователем.

### D005 — Réunion отделяется от metropolitan France

- Решение: Réunion не входит в один обычный travel region с европейской территорией Франции.
- Rationale: S01 задаёт явный пример; S02/S03 связывают его с territorial entry scope. E01 подтверждает различие Schengen applicability.
- Правила: R012, R019.
- Контраргументы: часть путешественников пользуется общими правами; это не устраняет различий для остальных. Отдельность от метрополии не доказывает, что Réunion нельзя объединить с каким-либо другим overseas компонентом.
- Статус: accepted для отношения к метрополии. «Ровно один самостоятельный регион Réunion» не утверждён.
- Основание: S01; S02/S03, соответствующие разделы; E01/E02. Réunion находится в EU customs territory, поэтому таможенное исключение нельзя использовать как ложное основание.

### D006 — Crimea не обычная travel territory Ukraine

- Решение: не включать Crimea в один обычный travel region с остальной Украиной.
- Rationale: S01 задаёт различие с позиции посещения. Это не отрицание юридического суверенитета Украины.
- Правила: R015, R022, R024.
- Контраргументы: отдельность travel region от Ukraine не говорит, должна ли территория объединяться с ordinary Russia и где именно проводить границу; контроль и правила меняются во времени.
- Статус: accepted только для исходного различения. Остальные выводы D013 tentative.
- Основание: S01; S02/S03 содержат более сильную рекомендацию, чем сама реплика пользователя.

### D007 — Western Sahara не ordinary Morocco

- Решение: Западная Сахара не должна исчезать в обычной travel territory Morocco.
- Rationale: явный пример пользователя; требуется сохранять travel-самостоятельность спорной области.
- Правила: R022, R024; возможное, пока нерешённое основание R010.
- Контраргументы: общий admission/control regime по одну сторону спорной границы может не давать witness для split с Morocco. UN status сам по себе по R016 недостаточен. Это реальное напряжение между требованием и режимной моделью.
- Статус: accepted как product constraint; общий механизм unresolved (Q006).
- Основание: S01. Требование о двух cells по Berm — отдельное D014, не принятое пользователем.

## Предложения исследований, не подтверждённые как окончательные решения

### D008 — Раздельные identity, legal status, control и traveller reality

- Решение: хранить независимые слои и не сводить их к country.
- Rationale: одна физическая поездка может быть допустима фактически и недопустима по праву другой релевантной юрисдикции.
- Правила: R017, R022–R024, R034, R037.
- Контраргументы: сложнее схема и отображение; нужно различать юридическую оценку и заявленный claim, чтобы не уравнивать их автоматически.
- Статус: tentative, сильное согласованное предложение S02/S03.
- Основание: S02 «Формальная модель», S03 «Суверенитет, claims и признание».

### D009 — Общие визовые пространства являются overlays

- Решение: EU/Schengen/CTA не становятся родительскими canonical territories; общие policies переиспользуются.
- Rationale: пересекающиеся scopes нельзя уложить в одно дерево.
- Правила: R005, R011, R012, R017.
- Контраргументы: сам запрет merge по общей визе не доказывает, какие территории сохранять отдельно. Нужна admission jurisdiction или определённая identity.
- Статус: tentative, с прямой опорой на accepted R005.
- Основание: S02/S03, примеры France/Germany и Crown Dependencies.

### D010 — Дополнительный критерий territorial identity

- Решение: S03 предлагает отделять внешние территориальные юрисдикции даже при одинаковых travel regimes.
- Rationale: выполнить UKOT constraint и избежать превращения списка посещений в чистую карту виз.
- Правила: R010, R018–R021.
- Контраргументы: «самостоятельная» определяется через желаемый результат; непонятно отличие Åland от Sicily, remote island от overseas jurisdiction. Нельзя обосновать registry самим registry.
- Статус: unresolved.
- Основание: S03 «Отдельный territorial identity criterion». S02 слабее опирается на этот фактор; это содержательное изменение, не только форматирование.

### D011 — Customs/biosecurity как условный hard split

- Решение: S02/S03 предлагают split при существенных обязанностях путешественника.
- Rationale: одинаковая виза может скрывать обязательные декларации и ограничения ввоза.
- Правила: R013, R016, R017.
- Контраргументы: тот же критерий может дробить Tasmania, Hawaii, California и множество внутренних карантинных зон; понятие существенности не определено.
- Статус: unresolved для общего критерия.
- Основание: таблицы критериев S02/S03. Недостаток модели нельзя закрыть одним дополнительным таможенным документом.

### D012 — MultiPolygon и отсутствие автоматического island split

- Решение: географическая несвязность сама по себе не создаёт регион.
- Rationale: физическая форма не обязана менять admission jurisdiction.
- Правила: R009, R021.
- Контраргументы: остров может быть отдельной единицей путешествий без формальностей; это вопрос identity, а не плохих данных о транспорте.
- Статус: tentative.
- Основание: S02 «Анклавы, эксклавы», S03 safe merge.

### D013 — Crimea отдельно также от ordinary Russia

- Решение: S02/S03 рекомендуют отдельную disputed cell Crimea/Sevastopol, не объединённую ни с ordinary Ukraine, ни с ordinary Russia.
- Rationale: различаются legal routes, применимые правовые ограничения и конфликтный status/control profile.
- Правила: R008, R012, R022, R024.
- Контраргументы: separate control объясняет границу с Ukraine, но не автоматически с Russia. Нужны территориальный legal-route witness или общий identity criterion. Одна или две cells Crimea/Sevastopol тоже не решено.
- Статус: tentative.
- Основание: S02 «Крым», S03 «Крым»; не расширять статус accepted D006.

### D014 — Разделение Western Sahara по operational control

- Решение: S02/S03 предлагают как минимум две области по сторонам Berm, связанные общим dispute_id.
- Rationale: разные фактические условия контроля и доступа.
- Правила: R015, R022, R024, R028, R030.
- Контраргументы: карта Berm не тождественна точной актуальной карте контроля; буферные/ограниченные полосы и изменения контроля могут потребовать иного уточнения. Две области не доказывают отделения западной части от Morocco.
- Статус: tentative. Ровно две итоговые cells не утверждены.
- Основание: соответствующие разделы S02/S03. E03 подтверждает только legal-status layer.

### D015 — St Helena / Ascension / Tristan da Cunha проверять раздельно

- Решение: одна конституционная единица может не быть атомарной для travel model.
- Rationale: исследования указывают на разные территориальные admission/permit systems компонентов.
- Правила: R011, R012, R018.
- Контраргументы: три наименования не доказывают три конечных региона; необходимо сравнить компетенции и scope каждого компонента, включая permits необитаемых островов.
- Статус: tentative.
- Основание: S02/S03, разделы UKOT. S02 прямо оговаривает необходимость проверки Tristan da Cunha.

### D016 — Antarctica первоначально как treaty-space cell

- Решение: одна provisional cell для выбранного антарктического universe; claims отдельно, станции как access objects.
- Rationale: overlapping claims нельзя превратить в взаимно исключающие regions без дополнительного правила.
- Правила: R002–R005, R014, R026.
- Контраргументы: один treaty regime не доказывает одну destination identity; территориальные protected areas имеют permits. Land universe не совпадает с Treaty Area. Требуется явное ограничение D004 для British Antarctic Territory.
- Статус: tentative; согласование с буквальным «каждая UKOT отдельно» unresolved.
- Основание: S02/S03 «Антарктида»; E04. Не является принятым пользователем исключением.

### D017 — Закрытые территории не исключаются из покрытия

- Решение: хранить visitability отдельно, включая uninhabited/closed.
- Rationale: открытие территории не должно создавать ранее отсутствовавшую Землю.
- Правила: R002, R003, R025.
- Контраргументы: исходное «возможное для посещения пространство» допускает более узкое прочтение universe.
- Статус: tentative; Q003.
- Основание: S02 restricted destinations; S03 «Closed и occupied areas».

### D018 — Временные факты, provenance и bitemporality

- Решение: разделять время действительности и время знания, сохранять source_scope и историю.
- Rationale: воспроизводить старые ответы и исправлять историю без потери audit trail.
- Правила: R031–R034.
- Контраргументы: дорого для первого эксперимента; полный operational SLA из исследования не нужен, пока нет production engine.
- Статус: tentative.
- Основание: S02 temporal rules; S03 «Provenance на уровне факта». Ежедневное обновление не считается обязательством проекта.

### D019 — Work/исследование и git/эксперименты

- Решение: архитектурный ответ предлагал перейти от Project/Work/Deep Research к спецификации и данным, затем к git repository и воспроизводимым экспериментам с Codex.
- Rationale: обсуждение правил и повторяемые вычисления нуждаются в разных рабочих артефактах.
- Правила: R001, R033, R037.
- Контраргументы: это организация работы, не выбор конкретного GIS stack. Можно выполнять анализ разными инструментами.
- Статус: tentative для инструментария; желание экспериментов accepted D003.
- Основание: S04, найденный фрагмент ассистента; не полный transcript. Репозиторий, Python/Go, PostGIS и конкретные datasets не утверждались в доступном материале.

## Новые формализации этого выпуска

### D020 — Coarsest partition вместо неопределённого «минимального атома»

- Решение: строить общее уточнение границ и объединять по полной hard signature; все неразрешённые предикаты показывать явно.
- Rationale: однородность сама по себе допускает бесконечное дробление; нужен merge criterion и проверка независимости от порядка.
- Правила: R006–R010, R035.
- Контраргументы: равенство всех policies невозможно доказать выборкой; identity discriminator пока не определён.
- Статус: tentative.
- Основание: N01, развивает safe merge S03. Это не готовый алгоритм построения всей Земли.

### D021 — Пересекающиеся hard boundaries уточняются, не перезаписываются

- Решение: blanket precedence stack S02 не используется для стирания одной обязательной границы другой.
- Rationale: immigration scope и control boundary могут пересекаться; обе должны сохраниться.
- Правила: R009, R028–R030.
- Контраргументы: при разных источниках одной линии всё равно нужен resolution policy. Отказ от last-wins не решает source conflict автоматически.
- Статус: tentative.
- Основание: N01; явное отклонение от рекомендованного precedence S02, согласующееся с common-refinement идеей S03.

### D022 — CSV как набор assertions, а не каталог признанных регионов

- Решение: фиксировать comparison target, premises, basis, factual verification и model issues отдельно от expected outcome.
- Rationale: split с метрополией не означает один атом; отрицательный фактор не доказывает merge; интуиция не должна становиться тестовым oracle.
- Правила: R008, R034–R036.
- Контраргументы: многие реальные случаи останутся conditional до фактологической работы. Это допустимая граница этапа.
- Статус: tentative для схемы; adversarial-подход accepted по S05.
- Основание: N01.

## Two-stage architecture decisions

### D023 — Final regions remain single-level

- Decision: the published Canonical Travel Regions output remains one exhaustive, mutually exclusive, single-level partition.
- Rationale: construction stages must not become a user-visible parent/child ontology.
- Rules: R003–R005, R043.
- Status: accepted.
- Basis: explicit user architecture decision, 2026-09-12.

### D024 — Construct the partition in two refinement stages

- Decision: construct the final partition through Stage 1 Mandatory Separation followed by Stage 2 Destination Partition.
- Rationale: hard travel boundaries and destination semantics answer different questions and require different evidence.
- Rules: R009, R039–R041.
- Status: accepted.
- Basis: explicit user architecture decision, 2026-09-12.

### D025 — Stage 1 establishes mandatory hard boundaries

- Decision: Stage 1 finds boundaries the final partition may not cross, using only accepted hard dimensions.
- Rationale: admission, legal/access, jurisdiction, and materially relevant control differences can require separation without deciding destination structure.
- Rules: R007–R017, R039.
- Status: accepted.
- Basis: explicit user architecture decision, 2026-09-12.

### D026 — Stage 2 only subdivides Stage 1 cells

- Decision: `Stage2Partition refines Stage1Partition`; Stage 2 cannot merge across a Stage 1 boundary.
- Rationale: mandatory separation must be monotonic through construction.
- Rules: R009, R041.
- Status: accepted.
- Basis: explicit user architecture decision, 2026-09-12.

### D027 — Stage 2 introduces destination semantics

- Decision: destination identity, geographic and itinerary coherence, gateway structure, and related destination concepts are first-class Stage 2 inputs.
- Rationale: the final travel partition must be able to distinguish destinations even when Stage 1 finds no hard boundary.
- Rules: R040.
- Status: accepted; algorithm unresolved in Q012.
- Basis: explicit user architecture decision, 2026-09-12.

### D028 — `hard_compatible` is not a final merge decision

- Decision: rename the Q001 outcome `may_merge` to `hard_compatible`.
- Rationale: complete and equal hard signatures establish only that Stage 1 requires no boundary; Stage 2 may still split the units.
- Rules: R008–R009, R035, R038.
- Status: accepted.
- Basis: explicit user terminology correction, 2026-09-12.

### D029 — Territorial/legal identity differs from destination identity

- Decision: territorial/legal identity remains a possible unresolved Stage 1 separator, while destination identity belongs to Stage 2.
- Rationale: institutional status and coherent travel-destination meaning are separate predicates. P3 addresses only the former.
- Rules: R010, R040, R042.
- Status: accepted distinction; territorial/legal predicate and destination algorithm remain unresolved.
- Basis: explicit user architecture decision, 2026-09-12.

### D030 — Finer subdivisions are outside project scope

- Decision: subdivisions finer than the Stage 2 canonical destination partition are outside this repository's ontology.
- Rationale: an external finer-granularity product must not distort either construction stage.
- Rules: R043.
- Status: accepted.
- Basis: explicit user scope decision, 2026-09-12.

## Local access overlays

### D031 — Локальные режимные зоны не создают split

- Решение: пограничные, военные, природоохранные, объектовые, маршрутные и activity-specific ограничения внутри общей admission jurisdiction моделируются как spatial access overlays и сами по себе не создают canonical region.
- Rationale: они изменяют локальный доступ уже допущенного путешественника, а не допуск в самостоятельное территориальное назначение. Совпадение overlay с административным районом или субъектом не меняет его семантику.
- Правила: R007, R008, R014, R017.
- Контраргументы: некоторые разрешения охватывают candidate territory целиком и практически функционируют как destination admission. Общий predicate для отделения таких случаев остаётся Q005.
- Статус: tentative; прямо подтверждено направление для российских пограничных зон, универсализация на все типы режимных зон требует проверки Q005.
- Основание: пользовательское уточнение от 12 сентября 2026 года.
- История ID: при интеграции присвоен D031 вместо дублирующего D017 из upstream; исходный D017 о покрытии закрытых территорий сохранён.

## CR-W core adoption

### D032 — CR-W принят как текущее production Stage 1 ядро

- Решение: `S1-core-v1` использует только CR-W — proven hard territorial TravelDecision discontinuity с G-SCOPE/G-CONTEXT/G-HARD/G-TIME/G-EVIDENCE из review. Один valid class-based witness достаточен независимо от частоты; frequency threshold отсутствует.
- Rationale: доказанные разные territorial decisions несовместимы с единой принятой hard decision function. Ненайденный certificate не доказывает equality; `hard_compatible` требует positive complete equality всех принятых dimensions на одном S/t.
- Правила: R007–R009, R012, R031, R038, R039, R044.
- Статус: accepted. Q001 narrowed/resolved for regime-based mandatory separation; все Stage 1 semantics не объявляются complete.
- Основание: явное пользовательское normative decision от 2026-09-12, после Q001 Stage 1 rule review.

### D033 — CR-J определён, но не принят

- Решение: CR-J имеет статус **well-defined normative candidate; not adopted**. Полное определение J1–J6 в review/candidate YAML сохраняется без сокращения для будущего experiment/decision. CR-J не separator и не обязательная signature dimension production `S1-core-v1`.
- Rationale: CR-J может создать mandatory boundary при равных current traveller-facing hard functions; institutional responsibility — самостоятельный нормативный выбор, не доказанный current travel discontinuity. Дополнительное empirical coverage не доказано текущими 49 cases.
- Правила: R011, R038, R044.
- Статус: accepted deferral; adoption of CR-J unresolved in Q001.
- Основание: явное пользовательское решение от 2026-09-12. Эта запись отличается от рекомендации принять W OR J в историческом review.

### D034 — Undefined territorial/legal identity исключена из production

- Решение: **territorial/legal identity alone is not an accepted Stage 1 hard separator**. Undefined identity не входит в production или production-candidate hard semantics. P3 — historical, non-production, model-unresolved profile, не Stage 2 destination model.
- Rationale: общего операционального predicate нет; labels, registry и politically salient place lists не заменяют его. Future explicit legal-status rule требует отдельного решения Q006.
- Правила: R010, R038, R042, R044.
- Статус: accepted. Historical P3 sufficient P1/P2 outcomes и identity blockers сохраняются как результаты старого эксперимента.
- Основание: явное пользовательское решение от 2026-09-12.

### D035 — Claims, disputes, control и category labels недостаточны

- Решение: disputed flag, claim, different recognition/controller/military control, dependency, autonomy, overseas и island labels самостоятельно не создают Stage 1 split. Только их доказанные actual hard territorial travel consequences могут поддержать CR-W.
- Rationale: факт о status/control не доказывает различие D; они сохраняются в собственных factual layers и unresolved Q006/Q007/etc., без скрытой hard dimension.
- Правила: R015, R016, R018, R022–R024, R039, R044.
- Статус: accepted.
- Основание: явное пользовательское решение от 2026-09-12.

### D036 — Accepted product regressions не являются hardcoded правилами

- Решение: D004/D005/D006/D007 не удаляются и не понижаются. Их статус — accepted product regression constraint, отличный от currently derivable Stage 1 rule. Если CR-W не гарантирует constraint, сохраняется явный незакрытый конфликт/requirement.
- Rationale: general rule нельзя выводить из desired answer. Для Réunion есть regime mechanism, но complete witness в snapshot не собран; blanket UKOT guarantee из CR-W не следует; Crimea не имеет Q001 factual dossier; Western Sahara west / Morocco не имеет доказанного CR-W. Никаких special cases, claimed resolution через Stage 2 или подмены отдельного региона dispute overlay.
- Правила: R008, R009, R018, R022, R024, R044; остаток Q006/Q011 и relevant data/model gaps.
- Статус: accepted distinction; accepted constraints остаются незакрытыми в недоказанной части.
- Основание: явное пользовательское решение от 2026-09-12.

### D037 — Historical profiles и current production разделены

- Решение: P1/P2/P3 сохраняют historical contract `0.2.0-draft`, profile version `q001-0.2.0` и evaluator serialization `0.2.0`. Новый `S1-core-v1` имеет собственный proof input, evaluator version `s1-core-1.0.0` и spec `0.3.0-draft`. Старые P1 results не переименовываются в production results; factual dataset и старые result files не изменяются.
- Rationale: historical witness schema не содержит полного CR-W gate audit; перенос требует нового versioned certificate. J/identity не наследуются в production completeness.
- Правила: R008, R033, R035, R038, R044.
- Статус: accepted implementation consequence of D032–D034.
- Основание: явное пользовательское требование воспроизводимости от 2026-09-12.
