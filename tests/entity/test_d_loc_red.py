"""FR-01~05 Domain Full RED — D-LOC-01 (Report/09). Domain Mock forbidden."""

from __future__ import annotations

import pytest

pytestmark = pytest.mark.entity


class TestDLoc01BlankCoordinates:
    """D-LOC-01 — find_blank_coords on G1, row-major."""

    def test_d_loc_01_g1_row_major_blank_coords(
        self, grid_g1: list[list[int]]
    ) -> None:
        # Given — matrix = G1
        from src.entity.rules.blank_finder import find_blank_coords

        grid = grid_g1
        # When
        coords = find_blank_coords(grid)
        # Then — I6, row-major 0-index
        assert coords == [(1, 1), (2, 2)]
