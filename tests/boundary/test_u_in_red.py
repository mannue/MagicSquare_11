"""FR-01~05 Boundary input RED skeletons — U-IN-04, U-IN-05 (Report/09).

U-IN-01~03: covered by AC-FR-01-01 full RED (tests/boundary/test_validator_shape_ac_fr_01_01.py).
"""

from __future__ import annotations

import pytest

pytestmark = pytest.mark.boundary


class TestUIn04ValueRange:
    """U-IN-04 — value not in {0} union {1..16} returns E004."""

    def test_u_in_04_value_17_returns_e004(self) -> None:
        # Given — 4x4, two blanks; cell value 17 (e.g. G1 with [0][0]=17)
        # from src.boundary.validator import BoundaryValidator
        # matrix = ...
        # When — result = BoundaryValidator().validate(matrix)
        pytest.fail("RED: U-IN-04 — value 17 returns E004 Failure envelope")

    def test_u_in_06_value_minus_one_returns_e004(self) -> None:
        # Given — 4x4, two blanks; cell value -1
        # When — result = BoundaryValidator().validate(matrix)
        pytest.fail("RED: U-IN-06 — value -1 returns E004 Failure envelope")


class TestUIn05DuplicateNonZero:
    """U-IN-05 — duplicate non-zero returns E005."""

    def test_u_in_05_duplicate_non_zero_returns_e005(self) -> None:
        # Given — 4x4, two blanks, non-zero duplicate (e.g. G1 with duplicate 6)
        # When — result = BoundaryValidator().validate(matrix)
        pytest.fail("RED: U-IN-05 — duplicate non-zero returns E005 Failure envelope")


class TestUIn07BlankCountZero:
    """U-IN-07 — blank count 0 returns E002 (AC-FR-01-02)."""

    def test_u_in_07_blank_count_zero_returns_e002(self) -> None:
        # Given — G0-style board with zero blanks (no 0 cells)
        # When — result = BoundaryValidator().validate(matrix)
        pytest.fail("RED: U-IN-07 — zero blanks returns E002 Failure envelope")


class TestUIn08BlankCountThree:
    """U-IN-08 — blank count 3 returns E002 (AC-FR-01-02)."""

    def test_u_in_08_blank_count_three_returns_e002(self) -> None:
        # Given — 4x4 with three 0 cells
        # When — result = BoundaryValidator().validate(matrix)
        pytest.fail("RED: U-IN-08 — three blanks returns E002 Failure envelope")
