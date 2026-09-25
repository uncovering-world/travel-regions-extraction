---
name: ctr-experiment
description: Use when a Canonical Travel Regions question depends on how rules behave over many cases or on data — building a draft partition, applying a rule to real territories, comparing parameters, reference lists or sources — rather than on one fact or on the owner's preference.
---

# Experiments

A rough estimate the owner asks for can be answered in the conversation first. Open an experiment folder when the result will be reused, compared across runs or feed a decision. Read the related issue first (e.g. #22 for the world Stage 1 draft).

## Layout

`experiments/<slug>/` with a short kebab-case slug. `q001/` and `source-pilot/` are frozen baselines — never write into them.

- `README.md` — sections below.
- `run.py` — Python ≥ 3.11, standard library first; run from the repository root; may import `ctr_evaluator` with `PYTHONPATH=src`. List any added dependency in the README.
- `inputs/` — small curated inputs, committed. Each states its source; copied reference data names its primary source and version; facts not verified in this experiment are marked (`cited`, `unconfirmed`, `conflicted`).
- `cache/` — external downloads, gitignored. The script fetches them; URL, version, retrieval date and sha256 are recorded in a committed file (README or `inputs/sources.json`), and the script warns on a checksum mismatch.
- `outputs/` — always commit a small deterministic summary (`summary.json`: totals, per-cell counts, input checksums); bulky outputs are regenerated.

Runs are deterministic: fixed ordering, seeds and tie-breaks.

## README sections

- **Question** — including every pending proposal the experiment assumes (with its issue) and the profile it runs under (`S1-core-v1` or a named product profile).
- **Related** — R/D/Q items and issue.
- **What would change our mind**
- **Method** — with the command to reproduce.
- **Result** — numbers and tables.
- **Conclusion** — what it supports and what it does not.
- **Status** — planned, running, concluded or abandoned.

Commit the README with **Question** and **What would change our mind** before the first run. If they change later, keep the original and add a dated revision.

## Judge the whole result

For anything partition-like, report:

- number of cells; cells per registry cell (and per sovereign if a mapping is declared);
- the size distribution; gaps and overlaps;
- accepted product regressions (D004–D007);
- agreement with reference lists at the matching scale — TCC for Stage 1, NomadMania and Wikivoyage for Stage 2 — with version and retrieval date, as validation only;
- sensitivity to each parameter; what changed against the previous run.

Unknown counts are reported as bounds or as unknown, never filled in; a metric that cannot be computed yet is listed with the reason. A pairwise check alone does not tell whether the partition is good.

The conclusion is a proposal; normative changes go through `ctr-decide`. When the status changes, update `docs/status.md`, commit and push.

## Red flags

- Hand-editing outputs until they look right — change the rule or a parameter and rerun.
- Presenting experimental cells as the canon.
- Tuning against a reference list and then reporting agreement with it as validation.
