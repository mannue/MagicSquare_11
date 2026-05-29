"""FR-01~05 Boundary output RED skeletons — U-OUT-01~03 (Report/09)."""

from __future__ import annotations

import pytest

pytestmark = pytest.mark.boundary


class TestUOutSuccessContract:
    """U-OUT — success int[6] output contract (G1 baseline)."""

    def test_u_out_01_success_result_length_six(self) -> None:
        # Given — valid matrix G1
        # from src.boundary.ui_boundary import UIBoundary
        # When — result = UIBoundary.solve(matrix)  # or ResultFormatter after solve
        pytest.fail("RED: U-OUT-01 — success result length is 6")

    def test_u_out_02_success_coordinates_one_indexed(self) -> None:
        # Given — valid matrix G1; expected [2,2,7,3,3,10]
        # When — result = UIBoundary.solve(matrix)
        pytest.fail("RED: U-OUT-02 — success coordinates are 1-index in [1,4]")

    def test_u_out_03_success_tuple_field_order(self) -> None:
        # Given — valid matrix G1
        # When — result = UIBoundary.solve(matrix)
        # Then (GREEN) — [r1,c1,n1,r2,c2,n2] field order and n1,n2 from missing set
        pytest.fail("RED: U-OUT-03 — success payload [r1,c1,n1,r2,c2,n2] field order")
