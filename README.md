# Canonical Travel Regions

Working specification and experimental data for building a reproducible, single-level partition of the world into canonical travel regions — the region canon for [Track Your Regions](https://github.com/uncovering-world/track-your-regions).

The partition is constructed in two internal stages. Stage 1 establishes mandatory hard boundaries. Stage 2 may subdivide each Stage 1 cell using destination semantics. The invariant `Stage2Partition refines Stage1Partition` prevents later work from crossing a mandatory boundary. These stages are not a user-visible hierarchy; the Stage 2 output is the single-level canonical partition.

The current normative Stage 1 production profile is **`S1-core-v1`**, containing only **CR-W: proven hard territorial TravelDecision discontinuity**, subject to all five proof gates in spec R044. CR-J remains a well-defined normative candidate, not adopted. Undefined territorial/legal identity is excluded; P1/P2/P3 remain historical non-production experiment profiles. No final world partition is produced.

## Repository contents

- `AGENTS.md` — invariants, skills and validation for coding agents;
- [docs/status.md](docs/status.md) — current focus, decisions waiting for the owner, active experiments, next step;
- [GitHub Issues](https://github.com/uncovering-world/travel-regions-extraction/issues) and [project 3](https://github.com/orgs/uncovering-world/projects/3) — task register and dedicated Canonical Travel Regions board;
- [docs/workflow.md](docs/workflow.md) — how work is done and where results land; project skills in `.agents/skills/` (`.claude/skills` links there);
- [docs/reviews/](docs/reviews/) — non-normative reviews of the project;
- `docs/spec.md` — normative specification;
- `docs/decisions.md` — decision log and current statuses;
- `docs/open-questions.md` — unresolved model questions;
- `docs/partition-architecture.md` — concise guide to the two-stage construction model;
- `data/adversarial-test-set.csv` — adversarial corpus for future experiments;
- `experiments/q001/` — the complete Experiment Q001 factual dataset, evaluator contract, fixtures, provenance, and validation artifacts.
- `experiments/q001/stage1-core-adoption.md` — CR-W adoption, residual questions, accepted-regression gaps and the separate current evaluator input contract.
- [Source-to-explanation pilot](experiments/source-pilot/README.md) — readable Denmark/Greenland, France/Reunion and Tibet dossiers, fresh source observations, exceptions and precise research gaps; not production certificates.

## Working toward the canon

The owner and coding agents work in conversation: each question gets the means it needs — a decision, a discussion, desk research, an experiment or code. Results land in fixed places with fixed markings; see [docs/workflow.md](docs/workflow.md). Normative documents change only through an explicit owner decision. Stage 2 design and experiments are allowed; no Stage 2 rule is adopted yet. Start from [docs/status.md](docs/status.md).

## Current Stage 1 core

```bash
PYTHONPATH=src python3 -m ctr_evaluator evaluate-core --input experiments/q001/stage1-core-example.json
```

The example is a synthetic proof fixture, not geographic evidence. Real inputs require an explicit versioned CR-W gate audit: nonempty disjoint scopes, matched civilian short-stay context, territorial legal effect, standing rule at the comparison time, and verified evidence for both decisions and relevant exceptions. One valid witness is sufficient regardless of class frequency. A missing certificate does not imply `hard_compatible`; positive full equality is required only across accepted hard decision dimensions. Jurisdiction and identity are not completeness requirements.

Claims, dispute/control/military labels, dependency, autonomy, overseas and island status cannot split by themselves. D004–D007 remain accepted product regressions, even where CR-W does not guarantee them. Q001 is narrowed; Q002/Q004/Q005/Q006/Q007/Q008/Q009/Q011 remain open in their residual scope. Stage 2 is not implemented.

## Validate Q001

```bash
cd experiments/q001
python3 validate.py
```

The expected result for the current snapshot is `PASS`, with 49 comparisons, 56 factual units, and four verified regime-witness comparisons.

The reference evaluator implements `experiments/q001/evaluator-contract.md`. Interpret real-data outcomes together with their explicit data and model blockers.

## Historical Q001 reference evaluator

The historical evaluator implements P1/P2/P3 under contract/spec `0.2.0-draft`, preserving evaluator `0.2.0` serialization and the 147 recorded outputs. These profiles are not the current normative production profile. Historical P1 certificates lack the full new gate audit and are not automatically CR-W certificates. P3 is non-production and model-unresolved where identity matters, preserving already sufficient historical P1/P2 splits; it is not a Stage 2 destination evaluator. `hard_compatible` is always profile-relative and never a final-region merge instruction.

Python 3.11 or newer is required. For a development installation:

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -e .
```

Run the evaluator and its tests with:

```bash
python -m ctr_evaluator validate-fixtures
python -m ctr_evaluator evaluate --comparison C001 --profile P1
python -m ctr_evaluator evaluate-all --profile P1
python -m ctr_evaluator evaluate-all --profiles P1,P2,P3
python -m pytest
```

Set another Q001 directory with the global option before the subcommand:

```bash
python -m ctr_evaluator --q001-dir path/to/q001 evaluate-all --profiles P1,P2,P3
```

A complete historical three-profile run writes deterministic artifacts under `experiments/q001/results/`; `evaluate-core` only emits its separately versioned JSON to stdout and never writes those artifacts. See `docs/evaluator-implementation.md` for both paths and the limits of evidence normalization.
