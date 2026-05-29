"""FR-01~05 Control flow RED skeletons — U-FLOW-02 extended (Report/09).

Invalid input must not call SolvePartialMagicSquare.execute (call_count == 0).
Shape/null cases: AC-FR-01-01 full RED in test_resolve_shape_guard_ac_fr_01_01.py.
"""

from __future__ import annotations

import pytest

pytestmark = pytest.mark.control


class TestUFlow02DomainIsolationExtended:
    """U-FLOW-02 — invalid FR-01 inputs never enter execute()."""

    def test_u_flow_02_blank_count_invalid_execute_call_count_zero(self) -> None:
        # Given — matrix with blank count != 2
        # from src.control.use_cases.resolve_magic_square import ResolveMagicSquareUseCase
        # with patch(..., SolvePartialMagicSquare.execute) as execute_spy:
        # When — UIBoundary.solve(matrix) or use_case.execute(matrix)
        # Then (GREEN) — execute_spy.call_count == 0
        pytest.fail("RED: U-FLOW-02 — blank count invalid, execute call_count == 0")

    def test_u_flow_02_value_range_invalid_execute_call_count_zero(self) -> None:
        # Given — matrix with value 17 or -1
        # When — use_case.execute(matrix) with execute spy
        pytest.fail("RED: U-FLOW-02 — value range invalid, execute call_count == 0")

    def test_u_flow_02_duplicate_invalid_execute_call_count_zero(self) -> None:
        # Given — matrix with duplicate non-zero
        # When — use_case.execute(matrix) with execute spy
        pytest.fail("RED: U-FLOW-02 — duplicate non-zero, execute call_count == 0")
