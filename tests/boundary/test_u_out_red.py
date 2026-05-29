"""FR-01~05 Boundary output Full RED — U-OUT-01~03 (Report/09)."""

from __future__ import annotations

from typing import Any

import pytest

from tests.conftest import G1_EXPECTED_SOLUTION

pytestmark = pytest.mark.boundary


def _solve(grid: list[list[int]]) -> list[int]:
    """Invoke solver entry point (RED: module not implemented)."""
    from src.control.use_cases.solve_partial_magic_square import solution

    return solution(grid)


class TestUOutSuccessContract:
    """U-OUT — success int[6] output contract (G1 baseline)."""

    def test_u_out_01_success_result_length_six(self, grid_g1: list[list[int]]) -> None:
        # Given — valid matrix G1
        grid = grid_g1
        # When
        result = _solve(grid)
        # Then — FR-05, BR-11
        assert len(result) == 6

    def test_u_out_02_success_coordinates_one_indexed(
        self, grid_g1: list[list[int]]
    ) -> None:
        # Given — valid matrix G1
        grid = grid_g1
        # When
        result = _solve(grid)
        # Then — FR-05, BR-10
        assert result == G1_EXPECTED_SOLUTION
        assert all(1 <= result[i] <= 4 for i in (0, 1, 3, 4))

    def test_u_out_03_success_tuple_field_order(
        self, grid_g1: list[list[int]]
    ) -> None:
        # Given — valid matrix G1; expected [r1,c1,n1,r2,c2,n2]
        grid = grid_g1
        # When
        result = _solve(grid)
        # Then — FR-05, BR-11
        r1, c1, n1, r2, c2, n2 = result
        assert [r1, c1, n1, r2, c2, n2] == G1_EXPECTED_SOLUTION
        assert {n1, n2} == {7, 10}
