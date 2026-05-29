"""Shared fixtures and constants for Magic Square TDD tests."""

from __future__ import annotations

from typing import Any

import pytest

# AC-FR-01-01 contract (PRD §8.1 INVALID_SIZE — shape guard only)
AC_FR_01_01 = "AC-FR-01-01"
INVALID_SIZE_CODE = "INVALID_SIZE"
INVALID_SIZE_MESSAGE = "Grid must be 4x4."

# FR-01~05 Boundary contract (PRD §13)
INVALID_BLANK_COUNT_CODE = "E_INVALID_BLANK_COUNT"
INVALID_BLANK_COUNT_MESSAGE = "빈칸(0)은 정확히 2개여야 합니다."
INVALID_VALUE_RANGE_CODE = "E_INVALID_VALUE_RANGE"
INVALID_VALUE_RANGE_MESSAGE = "값은 0 또는 1~16 범위여야 합니다."
DUPLICATE_NON_ZERO_CODE = "E_DUPLICATE_NON_ZERO"
DUPLICATE_NON_ZERO_MESSAGE = "0을 제외한 값은 중복될 수 없습니다."

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

# Report/09 §3.2 — G0~G3 Given SSOT
G0_COMPLETE: list[list[int]] = [
    [16, 3, 2, 13],
    [5, 10, 11, 8],
    [9, 6, 7, 12],
    [4, 15, 14, 1],
]
G1_STEP_A: list[list[int]] = [
    [1, 14, 15, 4],
    [12, 0, 6, 9],
    [8, 11, 0, 5],
    [13, 2, 3, 16],
]
G2_REVERSE: list[list[int]] = [
    [16, 3, 2, 13],
    [5, 0, 11, 8],
    [9, 6, 0, 12],
    [4, 15, 14, 1],
]
G3_UNSOLVABLE: list[list[int]] = [
    [3, 16, 2, 13],
    [5, 0, 11, 8],
    [9, 6, 0, 12],
    [4, 15, 14, 1],
]

G1_EXPECTED_SOLUTION: list[int] = [2, 2, 7, 3, 3, 10]
G2_EXPECTED_SOLUTION: list[int] = [2, 2, 10, 3, 3, 7]


def make_grid(rows: int, cols: int, fill: int = 1) -> list[list[int]]:
    """Build a rows×cols integer matrix for shape boundary tests."""
    return [[fill for _ in range(cols)] for _ in range(rows)]


def copy_grid(grid: list[list[int]]) -> list[list[int]]:
    """Return a deep copy of a 4×4 integer grid."""
    return [row[:] for row in grid]


def grid_with_three_blanks() -> list[list[int]]:
    """G1 derivative with three blank cells (U-IN-08)."""
    grid = copy_grid(G1_STEP_A)
    grid[0][0] = 0
    return grid


def grid_g1_with_cell(row: int, col: int, value: int) -> list[list[int]]:
    """G1 derivative with a single cell replaced."""
    grid = copy_grid(G1_STEP_A)
    grid[row][col] = value
    return grid


def grid_g0_with_cell(row: int, col: int, value: int) -> list[list[int]]:
    """G0 derivative with a single cell replaced."""
    grid = copy_grid(G0_COMPLETE)
    grid[row][col] = value
    return grid


@pytest.fixture
def grid_g0() -> list[list[int]]:
    return copy_grid(G0_COMPLETE)


@pytest.fixture
def grid_g1() -> list[list[int]]:
    return copy_grid(G1_STEP_A)


@pytest.fixture
def grid_g2() -> list[list[int]]:
    return copy_grid(G2_REVERSE)


@pytest.fixture
def grid_g3() -> list[list[int]]:
    return copy_grid(G3_UNSOLVABLE)


@pytest.fixture
def boundary_validator() -> Any:
    """BoundaryValidator instance."""
    from src.boundary.validator import BoundaryValidator

    return BoundaryValidator()


@pytest.fixture
def resolve_use_case() -> Any:
    """ResolveMagicSquareUseCase with injectable domain collaborator."""
    from unittest.mock import MagicMock

    from src.control.use_cases.resolve_magic_square import ResolveMagicSquareUseCase

    domain_spy = MagicMock()
    return ResolveMagicSquareUseCase(domain_resolver=domain_spy), domain_spy
