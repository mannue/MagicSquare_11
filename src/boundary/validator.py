"""Boundary input validation for magic square grids."""

from __future__ import annotations

from typing import Any

from src.boundary.errors import BoundaryErrorDetail, ValidationFailure, ValidationSuccess

_INVALID_SIZE_CODE = "INVALID_SIZE"
_INVALID_SIZE_MESSAGE = "Grid must be 4x4."
_INVALID_BLANK_COUNT_CODE = "E_INVALID_BLANK_COUNT"
_INVALID_BLANK_COUNT_MESSAGE = "빈칸(0)은 정확히 2개여야 합니다."
_INVALID_VALUE_RANGE_CODE = "E_INVALID_VALUE_RANGE"
_INVALID_VALUE_RANGE_MESSAGE = "값은 0 또는 1~16 범위여야 합니다."
_DUPLICATE_NON_ZERO_CODE = "E_DUPLICATE_NON_ZERO"
_DUPLICATE_NON_ZERO_MESSAGE = "0을 제외한 값은 중복될 수 없습니다."
_REQUIRED_BLANK_COUNT = 2
_MIN_CELL_VALUE = 1
_MAX_CELL_VALUE = 16


class BoundaryValidator:
    """Validates grid shape and input contract before Control/Domain."""

    def validate(self, grid: Any) -> ValidationFailure | ValidationSuccess:
        if (
            grid is None
            or len(grid) != 4
            or not all(len(row) == 4 for row in grid)
        ):
            return ValidationFailure(
                success=False,
                error=BoundaryErrorDetail(
                    code=_INVALID_SIZE_CODE,
                    message=_INVALID_SIZE_MESSAGE,
                ),
            )
        blank_count = sum(cell == 0 for row in grid for cell in row)
        if blank_count != _REQUIRED_BLANK_COUNT:
            return ValidationFailure(
                success=False,
                error=BoundaryErrorDetail(
                    code=_INVALID_BLANK_COUNT_CODE,
                    message=_INVALID_BLANK_COUNT_MESSAGE,
                ),
            )
        for row in grid:
            for cell in row:
                if cell != 0 and (
                    cell < _MIN_CELL_VALUE or cell > _MAX_CELL_VALUE
                ):
                    return ValidationFailure(
                        success=False,
                        error=BoundaryErrorDetail(
                            code=_INVALID_VALUE_RANGE_CODE,
                            message=_INVALID_VALUE_RANGE_MESSAGE,
                        ),
                    )
        non_zero_values = [cell for row in grid for cell in row if cell != 0]
        if len(non_zero_values) != len(set(non_zero_values)):
            return ValidationFailure(
                success=False,
                error=BoundaryErrorDetail(
                    code=_DUPLICATE_NON_ZERO_CODE,
                    message=_DUPLICATE_NON_ZERO_MESSAGE,
                ),
            )
        return ValidationSuccess()
