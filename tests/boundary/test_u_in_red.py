"""FR-01~05 Boundary input Full RED — U-IN-04~08 (Report/09).

U-IN-01~03: covered by AC-FR-01-01 (tests/boundary/test_validator_shape_ac_fr_01_01.py).
"""

from __future__ import annotations

from typing import Any

import pytest

from tests.conftest import (
    DUPLICATE_NON_ZERO_CODE,
    DUPLICATE_NON_ZERO_MESSAGE,
    G0_COMPLETE,
    INVALID_BLANK_COUNT_CODE,
    INVALID_BLANK_COUNT_MESSAGE,
    INVALID_VALUE_RANGE_CODE,
    INVALID_VALUE_RANGE_MESSAGE,
    copy_grid,
    grid_g1_with_cell,
    grid_with_three_blanks,
)

pytestmark = pytest.mark.boundary


def _assert_validation_failure(result: Any, code: str, message: str) -> None:
    assert result.success is False
    assert result.error.code == code
    assert result.error.message == message


class TestUIn07BlankCountZero:
    """U-IN-07 — blank count 0 returns E_INVALID_BLANK_COUNT (AC-FR-01-02)."""

    def test_u_in_07_blank_count_zero_returns_e002(
        self, boundary_validator: Any
    ) -> None:
        # Given — G0 complete board (zero blanks)
        grid = copy_grid(G0_COMPLETE)
        # When
        result = boundary_validator.validate(grid)
        # Then — AC-FR-01-02, PRD §13
        _assert_validation_failure(
            result, INVALID_BLANK_COUNT_CODE, INVALID_BLANK_COUNT_MESSAGE
        )


class TestUIn08BlankCountThree:
    """U-IN-08 — blank count 3 returns E_INVALID_BLANK_COUNT (AC-FR-01-02)."""

    def test_u_in_08_blank_count_three_returns_e002(
        self, boundary_validator: Any
    ) -> None:
        # Given — 4×4 with three 0 cells
        grid = grid_with_three_blanks()
        # When
        result = boundary_validator.validate(grid)
        # Then — AC-FR-01-02, PRD §13
        _assert_validation_failure(
            result, INVALID_BLANK_COUNT_CODE, INVALID_BLANK_COUNT_MESSAGE
        )


class TestUIn04ValueRange:
    """U-IN-04 — value not in {0} ∪ {1..16} returns E_INVALID_VALUE_RANGE."""

    def test_u_in_04_value_17_returns_e004(self, boundary_validator: Any) -> None:
        # Given — G1 with cell value 17
        grid = grid_g1_with_cell(0, 0, 17)
        # When
        result = boundary_validator.validate(grid)
        # Then — AC-FR-01-03, PRD §13
        _assert_validation_failure(
            result, INVALID_VALUE_RANGE_CODE, INVALID_VALUE_RANGE_MESSAGE
        )

    def test_u_in_06_value_minus_one_returns_e004(
        self, boundary_validator: Any
    ) -> None:
        # Given — G1 with cell value -1
        grid = grid_g1_with_cell(0, 0, -1)
        # When
        result = boundary_validator.validate(grid)
        # Then — AC-FR-01-03, PRD §13
        _assert_validation_failure(
            result, INVALID_VALUE_RANGE_CODE, INVALID_VALUE_RANGE_MESSAGE
        )


class TestUIn05DuplicateNonZero:
    """U-IN-05 — duplicate non-zero returns E_DUPLICATE_NON_ZERO."""

    def test_u_in_05_duplicate_non_zero_returns_e005(
        self, boundary_validator: Any
    ) -> None:
        # Given — G1 with duplicate non-zero 6 at (0,0) and (1,2)
        grid = grid_g1_with_cell(0, 0, 6)
        # When
        result = boundary_validator.validate(grid)
        # Then — AC-FR-01-04, PRD §13
        _assert_validation_failure(
            result, DUPLICATE_NON_ZERO_CODE, DUPLICATE_NON_ZERO_MESSAGE
        )
