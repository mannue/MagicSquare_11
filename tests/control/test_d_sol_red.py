"""FR-01~05 Solver Full RED — D-SOL-01~04 (Report/09). Domain Mock forbidden."""

from __future__ import annotations

import pytest

from tests.conftest import G1_EXPECTED_SOLUTION, G2_EXPECTED_SOLUTION

pytestmark = [pytest.mark.control, pytest.mark.entity]


def _solution(grid: list[list[int]]) -> list[int]:
    from src.control.use_cases.solve_partial_magic_square import solution

    return solution(grid)


class TestDSol01StepASuccess:
    """D-SOL-01 — G1 small-first Step A success."""

    def test_d_sol_01_g1_step_a_returns_2_2_7_3_3_10(
        self, grid_g1: list[list[int]]
    ) -> None:
        # Given — matrix = G1
        grid = grid_g1
        # When
        result = _solution(grid)
        # Then — I8
        assert result == G1_EXPECTED_SOLUTION


class TestDSol02StepBReverse:
    """D-SOL-02 — G2 Step A fail, Step B reverse success."""

    def test_d_sol_02_g2_reverse_success(self, grid_g2: list[list[int]]) -> None:
        # Given — matrix = G2
        grid = grid_g2
        # When
        result = _solution(grid)
        # Then — I9
        assert result == G2_EXPECTED_SOLUTION


class TestDSol03Unsolvable:
    """D-SOL-03 — G3 both attempts fail."""

    def test_d_sol_03_g3_raises_unsolvable_domain_error(
        self, grid_g3: list[list[int]]
    ) -> None:
        # Given — matrix = G3
        from src.entity.errors import UnsolvableDomainError

        grid = grid_g3
        # When / Then — I10
        with pytest.raises(UnsolvableDomainError):
            _solution(grid)


class TestDSol04OutputContract:
    """D-SOL-04 — success payload length and 1-index coordinates."""

    def test_d_sol_04_g1_result_length_six_and_one_index(
        self, grid_g1: list[list[int]]
    ) -> None:
        # Given — matrix = G1
        grid = grid_g1
        # When
        result = _solution(grid)
        # Then — I8, BR-10~11
        assert len(result) == 6
        r1, c1, n1, r2, c2, n2 = result
        assert all(1 <= coordinate <= 4 for coordinate in (r1, c1, r2, c2))
        assert {n1, n2} == {7, 10}
