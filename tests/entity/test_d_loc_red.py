"""FR-01~05 Domain RED skeleton — D-LOC-01 (Report/09). Domain Mock forbidden."""

from __future__ import annotations

import pytest

pytestmark = pytest.mark.entity


class TestDLoc01BlankCoordinates:
    """D-LOC-01 — find_blank_coords on G1, row-major."""

    def test_d_loc_01_g1_row_major_blank_coords(self) -> None:
        # Given — matrix = G1
        # from src.entity.rules.blank_finder import find_blank_coords
        # When — coords = find_blank_coords(matrix)
        # Then (GREEN) — 0-index [(1,1), (2,2)]; 1-index (2,2), (3,3)
        pytest.fail("RED: D-LOC-01 — G1 row-major blanks (2,2) and (3,3) 1-index")
