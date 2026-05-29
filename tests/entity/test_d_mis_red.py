"""FR-01~05 Domain Full RED — D-MIS-01 (Report/09). Domain Mock forbidden."""

from __future__ import annotations

import pytest

pytestmark = pytest.mark.entity


class TestDMis01MissingNumbers:
    """D-MIS-01 — find_not_exist_nums on G1, ascending."""

    def test_d_mis_01_g1_missing_numbers_7_10_ascending(
        self, grid_g1: list[list[int]]
    ) -> None:
        # Given — matrix = G1
        from src.entity.rules.missing_number_finder import find_not_exist_nums

        grid = grid_g1
        # When
        missing = find_not_exist_nums(grid)
        # Then — I7, I11
        assert missing == [7, 10]
