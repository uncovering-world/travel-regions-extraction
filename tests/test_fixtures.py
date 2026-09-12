from ctr_evaluator.fixtures import validate_fixtures


def test_all_contract_fixtures_pass() -> None:
    report = validate_fixtures()
    assert report.fixture_count == 15
    assert report.failures == ()
