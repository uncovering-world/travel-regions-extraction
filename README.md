# Canonical Travel Regions

Working specification and experimental data for building a reproducible, single-level partition of the world into canonical travel regions.

The project does not yet contain a final world partition and does not select a winner among profiles P1, P2, and P3.

## Repository contents

- `docs/spec.md` — normative specification;
- `docs/decisions.md` — decision log and current statuses;
- `docs/open-questions.md` — unresolved model questions;
- `data/adversarial-test-set.csv` — adversarial corpus for future experiments;
- `experiments/q001/` — the complete Experiment Q001 factual dataset, evaluator contract, fixtures, provenance, and validation artifacts.

## Validate Q001

```bash
cd experiments/q001
python3 validate.py
```

The expected result for the current snapshot is `PASS`, with 49 comparisons, 56 factual units, and four verified regime-witness comparisons.

The reference evaluator implements `experiments/q001/evaluator-contract.md`. Interpret real-data outcomes together with their explicit data and model blockers.

## Reference pairwise evaluator

The minimal open-world evaluator implements profiles P1, P2, and P3. It emits pairwise outcomes only and does not build a world partition.

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

A complete three-profile run updates deterministic artifacts under `experiments/q001/results/`. See `docs/evaluator-implementation.md` for adapter decisions and limitations of the current factual schema.
