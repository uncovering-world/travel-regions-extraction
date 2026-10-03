# Updating the discovery of entry rules

Once a year, before a release (R055):

1. `python3 data/entry-rules/discover.py --latest --prefill` — moves every pin to the current revision, regenerates `candidates.csv` and `DISCOVERY.md`, and adds a map row for each new candidate (with census ids where the place name matches a census row of the same country; these are marked "prefill by name match; to be reviewed").
2. Go through `DISCOVERY.md` → "Candidates not accounted for". For each, read the passage and, where needed, the article and the rule it cites:
   - **`ignore` with a reason** when the passage is not a rule for part of the country: a port of entry, airport or border crossing named in a country-wide rule; a transit rule (R056: transit is not a witness); a rule for organised groups only or for residents of a border area; a place named only as an example or as a consulate's seat. Keep reasons short and reusable ("port of entry", "transit only", "group-only rule", "border residents only", "country-wide rule").
   - **A census id** when the rule is already in the census.
   - **A new census row** when the passage points to a rule for part of the country that the census lacks. Add it to the census with its source; then check it against the text of the rule itself and record what it says in `experiments/stage1-list/inputs/entry_rule_facts.csv` (each value with a source and a verbatim passage). A Wikipedia sentence is a lead, not the rule.
3. Review prefilled name matches; correct or confirm them (remove the "to be reviewed" note).
4. `python3 data/entry-rules/discover.py --check` and `python3 -m pytest -q`; then rerun `python3 experiments/stage1-list/run.py`.

Rules that apply everywhere: nothing from memory; a census row needs a source; a fact in `entry_rule_facts.csv` needs a verbatim passage; an `ignore` needs a reason.

What this discovery does not find, by design: rules not mentioned in the English "Visa policy of …" articles (domestic permits that only national-language sources describe, rules for citizens of the country itself), and places the articles do not link. Other sources can be added to `sources.json` if they are pinned the same way.
