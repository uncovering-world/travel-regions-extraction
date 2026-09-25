# Data already collected by others: what can be reused

Checked on 13 September 2026. An addition to the pilot at the user's request: a survey of data sources, not an import of their geographic claims. The ten-target limit in `sources.json` applies to the three geographic dossiers; the pages of this survey are counted separately by the links below. No full databases or paid APIs were downloaded, no accounts were created and no terms of use were circumvented.

## Short conclusion

There is no need to search for everything from scratch. There is a professional aggregator of rules and there are ready-made passport matrices. But this survey **did not establish a source that at once gives open rights to the data we need, current coverage of the relevant territories and sufficient evidence for our boundaries**. This is a limitation of the candidates checked, not a claim that no such source exists anywhere.

| Candidate | What it already collects | Access and reuse | Proposed role |
|---|---|---|---|
| IATA / Timatic | Document requirements for travel, not only a passport ranking | An API and a user-facing check exist; an open licence for bulk export was not established | Candidate licensed source of detailed requirements |
| Henley Passport Index | Passport-to-destination mappings reduced to a ranking | The methodology is public; an open machine-readable export with rights was not established | Pointer for discovery, not proof that regimes are equal |
| Passport Index | Source of the passport matrices used by the repositories below | The site itself could not be read; reuse terms were not checked | Candidate after access and rights are checked |
| GitHub: Passport Index Dataset / Data | Ready-made CSV; the successor also JSON | The authors state MIT; the provenance of the data needs a separate check | Format example and a potential source of research hints |

## What could be checked

**IATA / Timatic.** This is an aggregator of state requirements and operational information, not an independent legislator of visa rules. IATA describes a network of government and airline sources and a process for checking updates. For travellers there is the Travel Centre; for integration, the AutoCheck API, which takes documents and the trip into account. This is much closer to our input data than a passport ranking. However, checking whether documents are acceptable for carriage by air must not automatically become a legal decision about admission to a territory. [Timatic: product and sources](https://www.iata.org/en/services/compliance/timatic/), [AutoCheck](https://www.iata.org/en/services/compliance/timatic/autocheck/).

The pages read did not show terms for open bulk export, rights to publish a derived database, or a price for our use case. Contacting the vendor is proposed; no request was sent. The per-passenger saving quoted on the AutoCheck page is not an API tariff. Before choosing, we need to establish coverage of individual territories and internal permit zones, retention of versions and sources, rights to archive and derive data, and the cost. The marketing claim "all countries and airports" does not prove this.

**Henley.** The methodology describes 199 passports and 227 destinations, IATA data with additional checks, and monthly updates. The final score merges several modes of admission; it is built for a given ordinary passport and a short trip under a number of assumptions. The ranking therefore loses some of the distinctions we need. A public methodology does not establish rights to export the database. [Methodology and limitations](https://www.henleyglobal.com/passport-index/methodology).

**Passport Index.** Reading the [home page](https://www.passportindex.org/) and [about.php](https://www.passportindex.org/about.php) returned 403; an attempt to open `https://www.passportindex.org/terms.php` also returned no text. That last address was a guess; its existence and content were not established. So the site's own terms, freshness, API and detailed coverage are not confirmed here. What is said below about it as a source of exports comes from the READMEs of the authors of those exports, not from a licence of the site owner that we read. An access error means neither a ban on nor permission for reuse.

**Ready-made matrices on GitHub.** The older [ilyankou/passport-index-dataset](https://github.com/ilyankou/passport-index-dataset) reports that it is archived and was last updated on 12 January 2025. It points to [imorte/passport-index-data](https://github.com/imorte/passport-index-data), whose README states 17 February 2026, 199 countries, CSV/JSON, statuses and permitted stay lengths. That is the date declared by the authors, not an independent check of every cell's freshness. The successor states explicitly that it scrapes Passport Index and is licensed under [MIT](https://github.com/imorte/passport-index-data/blob/main/LICENSE). That licence does not by itself confirm a chain of permissions from the original data owner; it remains unverified until any bulk import. The described schema contains no evidence or effective dates per cell. Coverage of Greenland, Réunion and Tibet in particular was not checked; the number of countries is no guarantee of coverage.

## How this could fit our work

A proposal, not a new normative model:

1. Choose a dataset by rights, provenance, version and coverage; do not import before that check. Pin a specific commit or snapshot, not a link to a moving branch.
2. Use a matrix to find **candidate differences**: the same passport, two territories, comparable conditions. Names and ISO codes are lookup keys, not grounds for a boundary.
3. For a candidate, find the detailed rule and confirm both sides, durations, documents, residence permits and exceptions. AI may propose extractions and links; that does not automatically give it the status of verified proof.
4. Keep the result in the format of our dossiers. Only a complete verified conclusion can be passed to the existing evaluator. Code helps to detect missing evidence and to reproduce a conclusion, but it does not fill the gaps.

Matching matrix columns do not prove identical rules. A missing territory does not automatically inherit the data of its "parent" country. Different labels may be different encodings of the same requirement. Neither an aggregator's list of destinations nor a passport ranking becomes our canon.

## The next check before any import

For one dataset: establish rights to the source data and to derived publication, read the schema and update history, check that the three pilot territories are present, and compare a few cells with the official pages already read. A negative result is a useful outcome: the dataset is unfit for import or good only for navigation. If rights are unclear, continue with targeted official dossiers rather than a bulk export "just in case".

This complements, and does not replace, the pilot's next step: bringing one difference to a reproducible proof. The cost of APIs, AI and human review is not measured here; a separate study of how to organise an AI-assisted process remains a task of its own.
