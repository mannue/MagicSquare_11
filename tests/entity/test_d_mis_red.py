"""FR-01~05 Domain RED skeleton — D-MIS-01 (Report/09). Domain Mock forbidden."""

from __future__ import annotations

import pytest

pytestmark = pytest.mark.entity


class TestDMis01MissingNumbers:
    """D-MIS-01 — find_not_exist_nums on G1, ascending."""

    def test_d_mis_01_g1_missing_numbers_7_10_ascending(self) -> None:
        # Given — matrix = G1
        # from src.entity.rules.missing_number_finder import find_not_exist_nums
        # When — missing = find_not_exist_nums(matrix)
        # Then (GREEN) — [7, 10]
        pytest.fail("RED: D-MIS-01 — G1 missing numbers {7,10} ascending")
