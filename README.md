# Canonical Travel Regions

Рабочая спецификация и экспериментальные данные для построения воспроизводимого одноуровневого разбиения мира на canonical travel regions.

Проект пока не содержит окончательного мирового partition и не выбирает победителя между профилями P1/P2/P3.

## Состав

- `docs/spec.md` — нормативная спецификация;
- `docs/decisions.md` — журнал решений и их статусов;
- `docs/open-questions.md` — нерешённые вопросы модели;
- `data/adversarial-test-set.csv` — adversarial corpus для последующих экспериментов;
- `experiments/q001/` — полный factual dataset, evaluator contract, fixtures, provenance и validation artifacts Experiment Q001.

## Проверка Q001

```bash
cd experiments/q001
python3 validate.py
```

Ожидаемый результат текущего snapshot: `PASS`, 49 comparisons, 56 factual units и четыре verified regime-witness comparisons.

Следующий этап — реализовать reference evaluator по `experiments/q001/evaluator-contract.md`, сначала добиться прохождения всех fixtures и только затем прогонять P1/P2/P3 на реальных comparisons.
