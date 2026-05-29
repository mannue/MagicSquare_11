"""FR-01~05 Domain RED skeletons — D-VAL-01~06 (Report/09). Domain Mock forbidden."""

from __future__ import annotations

import pytest

pytestmark = pytest.mark.entity


class TestDVal01MagicSquareComplete:
    """D-VAL-01 — is_magic_square(G0) is True."""

    def test_d_val_01_g0_complete_magic_square_true(self) -> None:
        # Given — matrix = G0
        # from src.entity.rules.magic_square_validator import is_magic_square
        # When — valid = is_magic_square(matrix)
        pytest.fail("RED: D-VAL-01 — G0 complete grid returns True")


class TestDVal02RowSumMismatch:
    """D-VAL-02 — row sum mismatch returns False."""

    def test_d_val_02_g0_row_sum_mismatch_false(self) -> None:
        # Given — G0 with one row sum altered (e.g. [0][0]=99)
        # When — valid = is_magic_square(matrix)
        pytest.fail("RED: D-VAL-02 — row sum mismatch returns False")


class TestDVal03ColumnSumMismatch:
    """D-VAL-03 — column sum mismatch returns False."""

    def test_d_val_03_g0_column_sum_mismatch_false(self) -> None:
        # Given — G0 with one column sum altered
        # When — valid = is_magic_square(matrix)
        pytest.fail("RED: D-VAL-03 — column sum mismatch returns False")


class TestDVal04DiagonalMismatch:
    """D-VAL-04 — diagonal sum mismatch returns False."""

    def test_d_val_04_g0_diagonal_sum_mismatch_false(self) -> None:
        # Given — G0 with main diagonal sum altered
        # When — valid = is_magic_square(matrix)
        pytest.fail("RED: D-VAL-04 — diagonal sum mismatch returns False")


class TestDVal05ValueSetViolation:
    """D-VAL-05 — out-of-range or duplicate on complete board returns False."""

    def test_d_val_05_g0_value_17_false(self) -> None:
        # Given — G0 with cell value 17
        # When — valid = is_magic_square(matrix)
        pytest.fail("RED: D-VAL-05 — value 17 on board returns False")

    def test_d_val_05_g0_duplicate_non_zero_false(self) -> None:
        # Given — G0 with duplicate non-zero
        # When — valid = is_magic_square(matrix)
        pytest.fail("RED: D-VAL-05 — duplicate non-zero returns False")


class TestDVal06ZeroInCompleteGrid:
    """D-VAL-06 — zero in otherwise complete grid returns False."""

    def test_d_val_06_g0_with_zero_cell_false(self) -> None:
        # Given — G0 with [0][0]=0
        # When — valid = is_magic_square(matrix)
        pytest.fail("RED: D-VAL-06 — zero in complete grid returns False")
