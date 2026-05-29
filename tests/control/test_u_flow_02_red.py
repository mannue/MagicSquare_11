"""FR-01~05 Control flow Full RED — U-FLOW-02 extended (Report/09).

Invalid FR-01 inputs must not call domain resolve (call_count == 0).
Shape/null cases: AC-FR-01-01 in test_resolve_shape_guard_ac_fr_01_01.py.
"""

from __future__ import annotations

from typing import Any

import pytest

from tests.conftest import (
    DUPLICATE_NON_ZERO_CODE,
    INVALID_BLANK_COUNT_CODE,
    INVALID_VALUE_RANGE_CODE,
    grid_g1_with_cell,
    grid_with_three_blanks,
)

pytestmark = pytest.mark.control


class TestUFlow02DomainIsolationExtended:
    """U-FLOW-02 — invalid FR-01 inputs never enter domain resolve()."""

    def test_u_flow_02_blank_count_invalid_execute_call_count_zero(
        self, resolve_use_case: Any
    ) -> None:
        # Given — matrix with blank count != 2 (three blanks)
        use_case, domain_spy = resolve_use_case
        grid = grid_with_three_blanks()
        # When
        result = use_case.execute(grid=grid)
        # Then — AC-FR-01-05, PRD §13
        assert result.success is False
        assert result.error.code == INVALID_BLANK_COUNT_CODE
        domain_spy.resolve.assert_not_called()

    def test_u_flow_02_value_range_invalid_execute_call_count_zero(
        self, resolve_use_case: Any
    ) -> None:
        # Given — matrix with value 17
        use_case, domain_spy = resolve_use_case
        grid = grid_g1_with_cell(0, 0, 17)
        # When
        result = use_case.execute(grid=grid)
        # Then
        assert result.success is False
        assert result.error.code == INVALID_VALUE_RANGE_CODE
        domain_spy.resolve.assert_not_called()

    def test_u_flow_02_duplicate_invalid_execute_call_count_zero(
        self, resolve_use_case: Any
    ) -> None:
        # Given — matrix with duplicate non-zero
        use_case, domain_spy = resolve_use_case
        grid = grid_g1_with_cell(0, 0, 6)
        # When
        result = use_case.execute(grid=grid)
        # Then
        assert result.success is False
        assert result.error.code == DUPLICATE_NON_ZERO_CODE
        domain_spy.resolve.assert_not_called()
