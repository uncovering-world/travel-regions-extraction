# facts8: notes

Read on 2026-10-04. 16 rows: 11 in `register-out.csv` (tasks 3–5) and 5 in `rules-out.csv` (tasks 1–2). Every task has at least one row. The rows are proposals for the register, not adopted facts.

Files: `get.py URL name` fetches a page with curl, saves the raw bytes and a text version in `pages/`, and logs the URL in `manifest.tsv`. PDFs go through `pdftotext -layout`. `curl -k` was needed for mfa.tj, whose certificate chain does not verify. `build.py` cuts each quote from the saved text between two anchors, so every quote is copied from the text and not retyped. `selfcheck.py` checks both CSVs.

## Self-check

`python3 selfcheck.py` checks every row. The quote must be at least 15 characters, with no line break, citation marker or ellipsis, and must be a substring of the saved text. Whitespace is normalised before the comparison.

Result: 16 of 16 pass and nothing was dropped. 14 quotes match the saved text exactly. Two match only after whitespace normalisation, because the sentence wraps across lines in a PDF: the UN Panel report (Kafia Kingi) and the tajtrade.tj copy of the Tajik border law. Each stays within one paragraph. The UN quote has no hyphenation. The tajtrade quote has none either.

Two sources are PDFs: the UN report and tajtrade.tj. `data/disputed-areas/verify_quotes.py` cannot read a PDF, so their saved text must be placed in its cache by hand before import.

## 1. cn-tibet / start_date (Tibet Travel Permit)

Found: two rows, both from 1989, neither a Chinese government text.

- `1989`, from the US State Department report to Congress of 2020-08-05: "In accordance with a 1989 central government regulation, international visitors … were required to obtain an official confirmation letter issued by the TAR government". This is a foreign government's description. The regulation's Chinese title and number were not found.
- `1989-03-08`, from TAR People's Government Order No. 4 under the Lhasa martial law, in an English translation hosted by Tibet Justice Center: "aliens cannot enter the area without permission". It covers only the martial-law area of Lhasa and not the whole TAR. The martial law was lifted on 1990-05-01, according to the CPC archive page (cpc.people.com.cn). So this is the earliest dated rule found, not proof that today's permit descends from it. Marked `primary` because it is the text of the order, but it is a translation on an NGO site, and the Chinese original was not found.

Queries and sites tried:

- Chinese:
  - 外国人入藏 旅游 管理 规定 入藏函 历史 1980年代 通知
  - "入藏函" 始于 由来
  - 国家旅游局 关于 外国旅游者 进藏 通知
  - 西藏自治区旅游管理条例 外国人 入藏 批准
  - 西藏自治区志 旅游志
  - 1989年 规定 外国人 赴西藏 旅游 须经 批准 国家旅游局 公安部
  - "入藏批准函" 1989/1990/1992
  - 西藏自治区人民政府令 1989 戒严 外国人
  - 1990 解除戒严 外国游客 恢复接待
- Pages read:
  - gwytb.gov.cn (Taiwan Affairs Office, 2017, sourced to the TAR government): describes the 入藏旅游批准函 but gives no date.
  - cpc.people.com.cn page on the 1989 State Council martial-law order: says nothing about foreigners.
  - Baidu Baike 入藏函: empty response.
  - lasa.xzdw.gov.cn (Lhasa party committee page on tourism history): empty response.
  - MJIB (Taiwan) study of TAR tourism 1978–1993: no permit date.
  - Travel-agency pages in the search results (qnly, ctsxz, xzcits, tibetcti and others): none dates the permit.
- English:
  - The State Department report (used).
  - Tibet Justice Center (used).
  - tpprc.org's copy of the martial-law decree: the domain is now a gambling spam site. Nothing from it was used.

## 2. tj-gbao / start_date (GBAO permit)

Found: the legal act. It is the Law of the Republic of Tajikistan "On the State Border" of **1997-08-01, No. 481**, Article 19. Foreign citizens and stateless persons may not enter the border zone without permission of the Ministry of Foreign Affairs and the internal-affairs bodies. The official text on mmk.tj, the National Legal Information Centre, gives this sentence with the note "(Қонуни ҶТ аз 25.07.2005 № 101". The tajtrade.tj Russian text marks it "в редакции Закона РТ от 25.07.2005г.N101".

So the current wording dates from **2005-07-25**. The 1997 original wording of Article 19 was not found. It may already have required a permit; this is unverified.

The link to GBAO comes from mfa.tj, whose consular service stamps "иҷозати сафар ба минтақаи наздисарҳадии Вилояти Мухтори Кӯҳистони Бадахшон" (a travel permit for GBAO's border region) into foreign passports.

The 2005 date agrees with the earlier finding that US consular sheets mention travel authorization for GBAO from 2005.

No act was found that says the whole of GBAO is border zone. Article 17 sets the zone "as a rule" within 25 km of the border, by Government decision. The Government decision that sets the zone's limits was not found.

Queries and sites tried:

- Russian:
  - постановление Правительства РТ пограничная зона ГБАО разрешение иностранных граждан
  - "Горно-Бадахшанской автономной области" "специальное разрешение" пограничный режим
  - "пограничном режиме" положение
  - Закон "О Государственной границе" статья 19
  - Закон № 101 от 25.07.2005
- Tajik:
  - иҷозатнома ВМКБ шаҳрвандони хориҷӣ қарори Ҳукумат минтақаи сарҳадӣ
  - "режими сарҳадӣ" низомнома
  - mfa.tj ВМКБ иҷозат
- Read:
  - mmk.tj border law (used).
  - tajtrade.tj Russian PDF (used).
  - base.spinform.ru (table of contents only).
  - continent-online.com: the 2017 visa rules (ППРТ No. 31) are paywalled.
  - mfa.tj pages 75 (used), 94 (visa legal bases; no GBAO) and the Berlin embassy page on Badakhshan (no permit text).

## 3. suleyman-shah-tomb / traveller_access

Found: one weak row, `restricted`. Hürriyet/AA reported on 2015-07-18 that the General Staff brought two soldiers' families to the border, and they then visited the Eşme site, receiving information from the commanders on duty. It shows civilians entering only when the military brings them. No public visiting rule, MSB statement or recent civilian visit was found.

Leads, not used as rows:

- Rudaw Türkçe (2026-01-21) says the tomb moved to Eşme was "daha sonra yeniden eski yerine nakledilmişti" (later moved back to its old place). This conflicts with the register's current site and with MSB statements of 2024–25 that a move back would be "evaluated". It is unverified and should be checked.
- Masrawy (2024-12-17): the SDF commander was ready to keep "the road to the site open". That is about the route, not civilian access.

Queries and sites tried:

- Turkish:
  - Süleyman Şah Türbesi Eşme ziyaret izin ziyaretçi
  - "Süleyman Şah Türbesi" ziyaret 2025
  - Süleyman Şah Saygı Karakolu ziyaretçi kabul sivil
  - "ziyarete kapalı"/"ziyaretçi kabul"
  - 2026 Karakozak geri taşınma
  - MSB açıklama
  - "Süleyman Şah Türbesi'ni ziyaret etti" dernek/vatandaşlar
  - msb.gov.tr nöbet değişimi ziyaret
- Read:
  - Hürriyet tag pages for Eşme, Saygı Karakolu and Süleyman Şah Türbesi.
  - The Hürriyet article of 2015-07-18 (used).
  - Rudaw Türkçe 2026-01-21.
  - Ekşi Sözlük p. 8 (nothing).
  - bianet (empty page).
- Arabic:
  - ضريح سليمان شاه آشمة زيارة 2025
  - Masrawy (read).

## 4. kafia-kingi / holder, holder_since

Found:

- **Holder: the Rapid Support Forces.**
  - Radio Tamazuj Arabic (2026-10-02, datelined Kafia Kingi) reports "قائد قوات الدعم السريع بمنطقة كفيا قنجي" (the RSF commander of the Kafia Kingi area) and a Kafia Kingi police director who speaks of "السودان الجديد", the RSF-led administration's term. This is the most recent evidence.
- **Since: late August 2024.**
  - UN Panel of Experts on the Sudan, S/2025/239, para. 68, primary: "In late August, RSF regiments crossed the border into Western Bahr el Ghazal, Raja County, seizing control of Kafia Kinji …". The report covers 2024; its summary begins "In 2024".
  - The Raja County commissioner (South Sudan), via Eye Radio (2024-09-03) and Radio Tamazuj English (2024-09-04), confirms the date. The RSF presence began after the Sudanese army withdrew from the border. South Sudan's army (SSPDF) disputed the occupation claims for areas it controls.

Conflict:

- Khatt30 (2026-06-15) places Kafia Kingi in South Darfur, "under RSF control since 2023". Grammatically that phrase refers to the state.
- XCEPT (2025, found earlier) says the RSF expelled the SAF from the tri-border area "by mid-2023".
- One reading: South Darfur fell to the RSF in 2023, and the enclave itself was taken in August 2024. That reading is an inference.

Note: the UN and the commissioner describe Kafia Kingi as lying in South Sudan's Raja County. That is South Sudan's de jure claim, already in the register.

Queries and sites tried:

- Arabic:
  - كافي كنجي حفرة النحاس قوات الدعم السريع سيطرة
  - "كفيا كنجي" الدعم السريع
  - "كافي كنجي" الدعم السريع 2023
- English:
  - "Kafia Kingi" RSF Panel of Experts 2024
  - Raja County commissioner Kafia Kingi RSF
- Read:
  - khatt30.com
  - 3ayin.com (route description only)
  - Radio Tamazuj ar/en
  - Eye Radio
  - UN S/2025/239 via ecoi.net

## 5. russian-ranges-kazakhstan / traveller_access

The register's `closed` stands for the leased range itself, but the area needs to be split from the town.

- **Range: `closed`.**
  - Article 22 of the RF–RK Agreement on Sary-Shagan (20 January 1995, as amended to 2015-04-16; meganorm.ru): the range is a "режимный объект" (regime facility). Its regime measures are organised by the range command in the order set in the Russian Armed Forces. Admission is only for the listed Kazakh and Russian units, industry organisations and officials, and third-country nationals by separate agreement.
  - Russian Wikipedia's "unguarded, de facto open" remark was not confirmed by any official or recent source.
- **Town of Priozersk: open.**
  - The Kazakh Government decree of 2001-01-31 No. 153 (uchet.kz) listed "Город Приозерск, поселок Гульшад - до 2006 года" among territories closed to foreigners. The decree was repealed by decree No. 1170 of 2008-12-12.
  - The 2008 list, marked "Действующий" on uchet.kz (database as of 2024-01) and prg.kz, has only Gvardeyskiy and Baikonyr with Karmakshy and Kazaly.
  - zakon.kz (2026-07-23): the town has been open for free entry since 2005.
  - Tengrinews (2021-11-18, first-hand): the checkpoint was abolished in the 2000s, and no notification is needed.

Caveats:

- uchet.kz and prg.kz are legal databases, not the official adilet.zan.kz. Adilet is a JavaScript page that returned no text, and it answered 429 to repeated requests. The Wayback Machine was "temporarily offline" during this session.
- The 2008 list gives end years of 2015. Whether a newer list exists was not checked.
- The town and the range are different areas. Whether the register should treat Priozersk as part of `russian-ranges-kazakhstan` is a modelling question for the owner.

Queries and sites tried:

- Russian:
  - Приозерск режим въезда пропуск иностранцы Сары-Шаган
  - акимат Приозерск въезд порядок пропуск
  - Приозерск закрытый город статус въезд иностранцев 2025
  - перечень территорий закрытых для посещения иностранцами Казахстан Приозерск
  - "временно закрытых для посещения иностранцами" изменения
- Read:
  - zakon.uchet.kz: the 1994 MVD instruction V940000113_, which also lists Priozersk and Balkhash-9 as closed but is superseded; the 2013 border-zone pass rules P1300000734, which are not relevant because Priozersk is not in the border zone; and the decrees of 2001 and 2008.
  - prg.kz and adilet.zan.kz (no text).
  - zakon.kz 2026 and Tengrinews 2021.
  - The treaty text saved by facts7.
- Kazakh-language sources and the Kazakh Ministry of Defence site were not reached.

## Weakest rows

- `suleyman-shah-tomb / traveller_access = restricted`: a single 2015 instance of a military-arranged family visit, more than ten years old.
- `cn-tibet / start_date`: neither row is a Chinese text. The 1989-03-08 order covers only the Lhasa martial-law area.
- `tj-gbao / start_date = 2005-07-25`: this dates the current wording, not the first requirement. The 1997 text is unknown.
- `kafia-kingi / holder_since`: the 2023 and 2024 dates conflict, as explained above.
