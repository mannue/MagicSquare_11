"""Boundary input validation for magic square grids."""

from __future__ import annotations

from typing import Any

from src.boundary.errors import BoundaryErrorDetail, ValidationFailure

_INVALID_SIZE_CODE = "INVALID_SIZE"
_INVALID_SIZE_MESSAGE = "Grid must be 4x4."


class BoundaryValidator:
    """Validates grid shape and input contract before Control/Domain."""

    def validate(self, grid: Any) -> ValidationFailure:
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
        raise NotImplementedError("validation beyond shape guard not implemented")
