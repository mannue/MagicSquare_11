"""AC-FR-01-01 domain isolation RED tests — ResolveMagicSquareUseCase (Track B).

AC-FR-01-01, PRD §8.1 INVALID_SIZE — shape failure must not call resolve().
"""

from __future__ import annotations

from typing import Any
from unittest.mock import MagicMock, patch

import pytest

from tests.conftest import (
    AC_FR_01_01,
    INVALID_SIZE_CODE,
    INVALID_SIZE_MESSAGE,
    make_grid,
)

pytestmark = pytest.mark.control


class TestAcFr0101DomainIsolation:
    """AC-FR-01-01, PRD §8.1 INVALID_SIZE — resolve() / Domain 진입 0회."""

    def test_none_grid_resolve_call_count_is_zero(self, resolve_use_case: Any) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE."""
        # Given
        use_case, domain_spy = resolve_use_case
        grid = None
        # When
        use_case.execute(grid=grid)
        # Then — AC-FR-01-01
        assert domain_spy.resolve.call_count == 0

    def test_empty_list_resolve_never_called(self, resolve_use_case: Any) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE."""
        # Given
        use_case, domain_spy = resolve_use_case
        grid: list[list[int]] = []
        # When
        use_case.execute(grid=grid)
        # Then — AC-FR-01-01
        domain_spy.resolve.assert_not_called()

    def test_3x4_grid_resolve_never_called(self, resolve_use_case: Any) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE."""
        # Given
        use_case, domain_spy = resolve_use_case
        grid = make_grid(3, 4)
        # When
        use_case.execute(grid=grid)
        # Then — AC-FR-01-01
        assert domain_spy.resolve.call_count == 0

    def test_none_grid_use_case_returns_invalid_size_without_resolve(
        self, resolve_use_case: Any
    ) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE."""
        # Given
        use_case, domain_spy = resolve_use_case
        grid = None
        # When
        result = use_case.execute(grid=grid)
        # Then — AC-FR-01-01
        assert result.success is False
        assert result.error.code == INVALID_SIZE_CODE
        assert result.error.message == INVALID_SIZE_MESSAGE
        domain_spy.resolve.assert_not_called()

    @patch(
        "src.control.use_cases.resolve_magic_square.ResolveMagicSquareUseCase._run_domain"
    )
    def test_none_grid_run_domain_patch_assert_not_called(
        self, mock_run_domain: MagicMock, resolve_use_case: Any
    ) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE."""
        # Given
        use_case, _domain_spy = resolve_use_case
        grid = None
        # When
        use_case.execute(grid=grid)
        # Then — AC-FR-01-01
        mock_run_domain.assert_not_called()


class TestAcFr0101ResolveContractIsolation:
    """AC-FR-01-01, PRD §8.1 INVALID_SIZE — resolve()가 None grid를 직접 처리하지 않음."""

    def test_4x3_grid_resolve_call_count_is_zero(self, resolve_use_case: Any) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE."""
        # Given
        use_case, domain_spy = resolve_use_case
        grid = make_grid(4, 3)
        # When
        use_case.execute(grid=grid)
        # Then — AC-FR-01-01
        assert domain_spy.resolve.call_count == 0

    def test_boundary_handles_none_before_resolve_invoked(
        self, resolve_use_case: Any
    ) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE."""
        # Given
        use_case, domain_spy = resolve_use_case
        grid = None
        # When
        result = use_case.execute(grid=grid)
        # Then — AC-FR-01-01
        assert result.error.code == INVALID_SIZE_CODE
        domain_spy.resolve.assert_not_called()

    def test_5x5_grid_resolve_never_called(self, resolve_use_case: Any) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE."""
        # Given
        use_case, domain_spy = resolve_use_case
        grid = make_grid(5, 5)
        # When
        use_case.execute(grid=grid)
        # Then — AC-FR-01-01
        domain_spy.resolve.assert_not_called()

    def test_four_empty_rows_resolve_call_count_is_zero(
        self, resolve_use_case: Any
    ) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE."""
        # Given
        use_case, domain_spy = resolve_use_case
        grid = [[]] * 4
        # When
        use_case.execute(grid=grid)
        # Then — AC-FR-01-01
        assert domain_spy.resolve.call_count == 0

    def test_scope_ac_fr_01_02_to_05_cases_not_in_control_shape_module(self) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE."""
        # Given
        from pathlib import Path

        source = Path(__file__).read_text(encoding="utf-8")
        import_lines = [
            line
            for line in source.splitlines()
            if line.strip().startswith(("from ", "import "))
        ]
        joined = "\n".join(import_lines)
        # When / Then — AC-FR-01-01
        assert "AC-FR-01-01" in source
        assert "blank_count" not in joined
        assert "duplicate" not in joined
        assert "missing_number" not in joined
