"""FR-01~05 Solver RED skeletons — D-SOL-01~04 (Report/09). Domain Mock forbidden."""

from __future__ import annotations

import pytest

pytestmark = [pytest.mark.control, pytest.mark.entity]


class TestDSol01StepASuccess:
    """D-SOL-01 — G1 small-first Step A success."""

    def test_d_sol_01_g1_step_a_returns_2_2_7_3_3_10(self) -> None:
        # Given — matrix = G1
        # from src.control.use_cases.solve_partial_magic_square import solution
        # When — result = solution(matrix)
        # Then (GREEN) — [2, 2, 7, 3, 3, 10]
        pytest.fail("RED: D-SOL-01 — G1 Step A success [2,2,7,3,3,10]")


class TestDSol02StepBReverse:
    """D-SOL-02 — G2 Step A fail, Step B reverse success."""

    def test_d_sol_02_g2_reverse_success(self) -> None:
        # Given — matrix = G2 (Report/09 §3.2; placeholder until fixture wired)
        # When — result = solution(matrix)
        pytest.fail("RED: D-SOL-02 — G2 TBD")


class TestDSol03Unsolvable:
    """D-SOL-03 — G3 both attempts fail."""

    def test_d_sol_03_g3_raises_unsolvable_domain_error(self) -> None:
        # Given — matrix = G3
        # When — solution(matrix)
        # Then (GREEN) — UnsolvableDomainError
        pytest.fail("RED: D-SOL-03 — G3 both steps fail with UnsolvableDomainError")


class TestDSol04OutputContract:
    """D-SOL-04 — success payload length and 1-index coordinates."""

    def test_d_sol_04_g1_result_length_six_and_one_index(self) -> None:
        # Given — matrix = G1
        # When — result = solution(matrix)
        # Then (GREEN) — len==6; r,c in [1,4]; n1,n2 in {7,10}
        pytest.fail("RED: D-SOL-04 — G1 result length 6 and 1-index coordinates")
