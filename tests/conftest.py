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
