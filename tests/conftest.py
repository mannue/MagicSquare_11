"""Shared fixtures and constants for Magic Square TDD tests."""

from __future__ import annotations

from typing import Any

import pytest

# AC-FR-01-01 contract (PRD §8.1 INVALID_SIZE — shape guard only)
AC_FR_01_01 = "AC-FR-01-01"
INVALID_SIZE_CODE = "INVALID_SIZE"
INVALID_SIZE_MESSAGE = "Grid must be 4x4."

# Out of scope for AC-FR-01-01 (must not appear as expected codes in shape suite)
FORBIDDEN_ERROR_CODES_AC_FR_01_01 = frozenset(
    {
        "E_INVALID_BLANK_COUNT",
        "E_INVALID_VALUE_RANGE",
        "E_DUPLICATE_NON_ZERO",
        "E_UNSOLVABLE_COMBINATION",
        "INVALID_BLANK_COUNT",
        "INVALID_VALUE_RANGE",
        "DUPLICATE_NON_ZERO",
    }
)


def make_grid(rows: int, cols: int, fill: int = 1) -> list[list[int]]:
    """Build a rows×cols integer matrix for shape boundary tests."""
    return [[fill for _ in range(cols)] for _ in range(rows)]


# --- Report/09 §3.2 G0~G3 (RED placeholder — uncomment for GREEN Arrange) ---
# G0_COMPLETE = [
#     [16, 3, 2, 13],
#     [5, 10, 11, 8],
#     [9, 6, 7, 12],
#     [4, 15, 14, 1],
# ]
# G1_STEP_A = [
#     [1, 14, 15, 4],
#     [12, 0, 6, 9],
#     [8, 11, 0, 5],
#     [13, 2, 3, 16],
# ]
# G2_REVERSE = [
#     [16, 3, 2, 13],
#     [5, 0, 11, 8],
#     [9, 6, 0, 12],
#     [4, 15, 14, 1],
# ]
# G3_UNSOLVABLE = [
#     [3, 16, 2, 13],
#     [5, 0, 11, 8],
#     [9, 6, 0, 12],
#     [4, 15, 14, 1],
# ]
#
# @pytest.fixture
# def grid_g0() -> list[list[int]]:
#     return [row[:] for row in G0_COMPLETE]


@pytest.fixture
def boundary_validator() -> Any:
    """BoundaryValidator instance (RED: module may not exist yet)."""
    from src.boundary.validator import BoundaryValidator

    return BoundaryValidator()


@pytest.fixture
def resolve_use_case() -> Any:
    """ResolveMagicSquareUseCase with injectable domain collaborator (RED stub)."""
    from unittest.mock import MagicMock

    from src.control.use_cases.resolve_magic_square import ResolveMagicSquareUseCase

    domain_spy = MagicMock()
    return ResolveMagicSquareUseCase(domain_resolver=domain_spy), domain_spy
