"""FR-01~05 Domain Full RED — D-VAL-01~06 (Report/09). Domain Mock forbidden."""

from __future__ import annotations

import pytest

from tests.conftest import grid_g0_with_cell

pytestmark = pytest.mark.entity


def _is_magic_square(grid: list[list[int]]) -> bool:
    from src.entity.rules.magic_square_validator import is_magic_square

    return is_magic_square(grid)


class TestDVal01MagicSquareComplete:
    """D-VAL-01 — is_magic_square(G0) is True."""

    def test_d_val_01_g0_complete_magic_square_true(
        self, grid_g0: list[list[int]]
    ) -> None:
        # Given — matrix = G0
        grid = grid_g0
        # When
        valid = _is_magic_square(grid)
        # Then — I1~I5
        assert valid is True


class TestDVal02RowSumMismatch:
    """D-VAL-02 — row sum mismatch returns False."""

    def test_d_val_02_g0_row_sum_mismatch_false(
        self, grid_g0: list[list[int]]
    ) -> None:
        # Given — G0 with row 0 sum altered
        grid = grid_g0_with_cell(0, 0, 99)
        # When
        valid = _is_magic_square(grid)
        # Then — I1
        assert valid is False


class TestDVal03ColumnSumMismatch:
    """D-VAL-03 — column sum mismatch returns False."""

    def test_d_val_03_g0_column_sum_mismatch_false(
        self, grid_g0: list[list[int]]
    ) -> None:
        # Given — G0 with column 0 sum altered
        grid = grid_g0_with_cell(1, 0, 99)
        # When
        valid = _is_magic_square(grid)
        # Then — I2
        assert valid is False


class TestDVal04DiagonalMismatch:
    """D-VAL-04 — diagonal sum mismatch returns False."""

    def test_d_val_04_g0_diagonal_sum_mismatch_false(
        self, grid_g0: list[list[int]]
    ) -> None:
        # Given — G0 with main diagonal sum altered
        grid = grid_g0_with_cell(0, 0, 99)
        # When
        valid = _is_magic_square(grid)
        # Then — I3
        assert valid is False


class TestDVal05ValueSetViolation:
    """D-VAL-05 — out-of-range or duplicate on complete board returns False."""

    def test_d_val_05_g0_value_17_false(self, grid_g0: list[list[int]]) -> None:
        # Given — G0 with cell value 17
        grid = grid_g0_with_cell(0, 0, 17)
        # When
        valid = _is_magic_square(grid)
        # Then — I4
        assert valid is False

    def test_d_val_05_g0_duplicate_non_zero_false(
        self, grid_g0: list[list[int]]
    ) -> None:
        # Given — G0 with duplicate non-zero (copy value from (1,0))
        grid = grid_g0_with_cell(0, 0, grid_g0[1][0])
        # When
        valid = _is_magic_square(grid)
        # Then — I4
        assert valid is False


class TestDVal06ZeroInCompleteGrid:
    """D-VAL-06 — zero in otherwise complete grid returns False."""

    def test_d_val_06_g0_with_zero_cell_false(
        self, grid_g0: list[list[int]]
    ) -> None:
        # Given — G0 with [0][0]=0
        grid = grid_g0_with_cell(0, 0, 0)
        # When
        valid = _is_magic_square(grid)
        # Then — I4, I7
        assert valid is False
