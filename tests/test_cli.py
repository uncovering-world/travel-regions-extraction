from ctr_evaluator.cli import main


def test_cli_returns_nonzero_for_unknown_comparison(capsys) -> None:
    assert main(["evaluate", "--comparison", "C999", "--profile", "P1"]) == 2
    assert "unknown comparison id" in capsys.readouterr().err


def test_cli_fixture_success(capsys) -> None:
    assert main(["validate-fixtures"]) == 0
    assert '"status": "PASS"' in capsys.readouterr().out
