"""Golden Master regression tests for Magic Square Solver output."""

from __future__ import annotations

import pytest

from tests.golden_master.approve import (
    approve_golden_master,
    assert_approved_scenario,
)
from tests.golden_master.scenarios import (
    SCENARIO_BY_NAME,
    assert_reverse_fallback_combination,
    assert_small_first_combination,
    assert_success_contract,
    parse_solution_payload,
    run_scenario,
)

pytestmark = [pytest.mark.golden_master, pytest.mark.boundary]


@pytest.fixture
def gm_scenario(request: pytest.FixtureRequest):
    """Resolve a Golden Master scenario by section name."""
    name = request.param
    return SCENARIO_BY_NAME[name]


class TestGoldenMasterMagicSquareDocument:
    """Full baseline approve check for all scenarios."""

    def test_golden_master_full_document(self) -> None:
        """Approve entire tests/golden_master_expected.txt against current output."""
        status, diff_text = approve_golden_master(auto_create=True)

        if status == "created":
            pytest.skip("Golden Master baseline created on first run; re-run to verify.")

        assert status == "matched", (
            "Golden Master full document mismatch.\n"
            f"{diff_text}\n"
            "________________________________________"
        )


class TestGoldenMasterMagicSquare:
    """Per-scenario Golden Master tests (GM-TC-01 ~ GM-TC-05)."""

    @pytest.mark.parametrize(
        "gm_scenario",
        ["normal_success"],
        indirect=True,
        ids=["GM-TC-01"],
    )
    def test_gm_tc_01_normal_combination_success(self, gm_scenario) -> None:
        """GM-TC-01: attempt-1 success, int[6], row-major, 1-index."""
        assert_approved_scenario(gm_scenario)

        body = run_scenario(gm_scenario)
        output_line = body.splitlines()[body.splitlines().index("Output:") + 1]
        payload = parse_solution_payload(output_line)

        assert_success_contract(gm_scenario, payload)
        assert_small_first_combination(gm_scenario, payload)

    @pytest.mark.parametrize(
        "gm_scenario",
        ["reverse_success"],
        indirect=True,
        ids=["GM-TC-02"],
    )
    def test_gm_tc_02_reverse_combination_success(self, gm_scenario) -> None:
        """GM-TC-02: attempt-2 reverse fallback success."""
        assert_approved_scenario(gm_scenario)

        body = run_scenario(gm_scenario)
        output_line = body.splitlines()[body.splitlines().index("Output:") + 1]
        payload = parse_solution_payload(output_line)

        assert_success_contract(gm_scenario, payload)
        assert_reverse_fallback_combination(gm_scenario, payload)

    @pytest.mark.parametrize(
        "gm_scenario",
        ["invalid_blank_count"],
        indirect=True,
        ids=["GM-TC-03"],
    )
    def test_gm_tc_03_invalid_blank_count(self, gm_scenario) -> None:
        """GM-TC-03: blank count != 2 returns E_INVALID_BLANK_COUNT."""
        assert_approved_scenario(gm_scenario)

        body = run_scenario(gm_scenario)
        error_line = body.splitlines()[body.splitlines().index("Error:") + 1]
        assert error_line == gm_scenario.expect_error

    @pytest.mark.parametrize(
        "gm_scenario",
        ["duplicate_number"],
        indirect=True,
        ids=["GM-TC-04"],
    )
    def test_gm_tc_04_duplicate_number(self, gm_scenario) -> None:
        """GM-TC-04: duplicate non-zero returns E_DUPLICATE_NON_ZERO."""
        assert_approved_scenario(gm_scenario)

        body = run_scenario(gm_scenario)
        error_line = body.splitlines()[body.splitlines().index("Error:") + 1]
        assert error_line == gm_scenario.expect_error

    @pytest.mark.parametrize(
        "gm_scenario",
        ["no_valid_solution"],
        indirect=True,
        ids=["GM-TC-05"],
    )
    def test_gm_tc_05_no_valid_magic_square(self, gm_scenario) -> None:
        """GM-TC-05: both combinations fail returns UnsolvableDomainError."""
        assert_approved_scenario(gm_scenario)

        body = run_scenario(gm_scenario)
        error_line = body.splitlines()[body.splitlines().index("Error:") + 1]
        assert error_line == gm_scenario.expect_error
