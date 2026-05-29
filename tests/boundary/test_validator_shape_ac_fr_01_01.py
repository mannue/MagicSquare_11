"""AC-FR-01-01 shape validation RED tests — BoundaryValidator (Track A).

AC-FR-01-01, PRD §8.1 INVALID_SIZE — 4×4 외 입력 즉시 실패, Domain 미호출.
"""

from __future__ import annotations

import importlib
import inspect
from pathlib import Path
from typing import Any

import pytest

from tests.conftest import (
    AC_FR_01_01,
    FORBIDDEN_ERROR_CODES_AC_FR_01_01,
    INVALID_SIZE_CODE,
    INVALID_SIZE_MESSAGE,
    make_grid,
)

pytestmark = pytest.mark.boundary


def _validate(grid: Any) -> Any:
    """Invoke BoundaryValidator.validate (RED: implementation pending)."""
    from src.boundary.validator import BoundaryValidator

    return BoundaryValidator().validate(grid)


def _assert_invalid_size_contract(result: Any) -> None:
    assert result.success is False, "shape failure must not report success"
    assert result.error.code == INVALID_SIZE_CODE
    assert result.error.message == INVALID_SIZE_MESSAGE


class TestAcFr0101NormalFailureReturn:
    """AC-FR-01-01, PRD §8.1 INVALID_SIZE — 정상 실패 반환 (grid=None)."""

    def test_none_grid_returns_failure_not_success(self, boundary_validator: Any) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE."""
        # Given
        grid = None
        # When
        result = boundary_validator.validate(grid)
        # Then — AC-FR-01-01
        assert result.success is False

    def test_none_grid_returns_code_invalid_size(self, boundary_validator: Any) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE."""
        # Given
        grid = None
        # When
        result = boundary_validator.validate(grid)
        # Then — AC-FR-01-01
        assert result.error.code == INVALID_SIZE_CODE

    def test_none_grid_returns_message_grid_must_be_4x4(self, boundary_validator: Any) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE."""
        # Given
        grid = None
        # When
        result = boundary_validator.validate(grid)
        # Then — AC-FR-01-01
        assert result.error.message == INVALID_SIZE_MESSAGE

    def test_none_grid_returns_validation_failure_type(self) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE."""
        # Given
        grid = None
        # When
        result = _validate(grid)
        # Then — AC-FR-01-01
        from src.boundary.errors import ValidationFailure

        assert isinstance(result, ValidationFailure)

    def test_none_grid_does_not_raise_type_error_on_validate(self, boundary_validator: Any) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE."""
        # Given
        grid = None
        # When / Then — AC-FR-01-01
        try:
            result = boundary_validator.validate(grid)
        except TypeError as exc:
            pytest.fail(f"None must yield contract failure, not TypeError: {exc}")
        assert result.success is False


class TestAcFr0101BoundaryValues:
    """AC-FR-01-01, PRD §8.1 INVALID_SIZE — 경계값 형상 실패."""

    def test_empty_list_grid_returns_invalid_size_failure(self, boundary_validator: Any) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE."""
        # Given
        grid: list[list[int]] = []
        # When
        result = boundary_validator.validate(grid)
        # Then — AC-FR-01-01
        _assert_invalid_size_contract(result)

    def test_four_empty_rows_grid_returns_invalid_size_failure(
        self, boundary_validator: Any
    ) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE."""
        # Given
        grid = [[]] * 4
        # When
        result = boundary_validator.validate(grid)
        # Then — AC-FR-01-01
        _assert_invalid_size_contract(result)

    def test_3x4_grid_returns_invalid_size_failure(self, boundary_validator: Any) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE."""
        # Given
        grid = make_grid(3, 4)
        # When
        result = boundary_validator.validate(grid)
        # Then — AC-FR-01-01
        _assert_invalid_size_contract(result)

    def test_4x3_grid_returns_invalid_size_failure(self, boundary_validator: Any) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE."""
        # Given
        grid = make_grid(4, 3)
        # When
        result = boundary_validator.validate(grid)
        # Then — AC-FR-01-01
        _assert_invalid_size_contract(result)

    def test_5x5_grid_returns_invalid_size_failure(self, boundary_validator: Any) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE."""
        # Given
        grid = make_grid(5, 5)
        # When
        result = boundary_validator.validate(grid)
        # Then — AC-FR-01-01
        _assert_invalid_size_contract(result)


class TestAcFr0101MessageExactMatch:
    """AC-FR-01-01, PRD §8.1 INVALID_SIZE — 메시지 문자 단위 동일성."""

    def test_none_grid_message_exact_match_prd_8_1(self, boundary_validator: Any) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE."""
        # Given
        grid = None
        expected = "Grid must be 4x4."
        # When
        result = boundary_validator.validate(grid)
        # Then — AC-FR-01-01
        assert result.error.message == expected
        assert result.error.message == INVALID_SIZE_MESSAGE

    def test_empty_list_message_exact_match_prd_8_1(self, boundary_validator: Any) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE."""
        # Given
        grid: list[list[int]] = []
        # When
        result = boundary_validator.validate(grid)
        # Then — AC-FR-01-01
        assert result.error.message == INVALID_SIZE_MESSAGE

    def test_3x4_message_exact_match_prd_8_1(self, boundary_validator: Any) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE."""
        # Given
        grid = make_grid(3, 4)
        # When
        result = boundary_validator.validate(grid)
        # Then — AC-FR-01-01
        assert result.error.message == INVALID_SIZE_MESSAGE

    def test_four_empty_rows_message_exact_match_prd_8_1(
        self, boundary_validator: Any
    ) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE."""
        # Given
        grid = [[]] * 4
        # When
        result = boundary_validator.validate(grid)
        # Then — AC-FR-01-01
        assert result.error.message == INVALID_SIZE_MESSAGE

    def test_invalid_size_message_byte_for_byte_equals_constant(self) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE."""
        # Given
        grid = None
        # When
        result = _validate(grid)
        # Then — AC-FR-01-01
        assert repr(result.error.message) == repr(INVALID_SIZE_MESSAGE)
        assert len(result.error.message) == len(INVALID_SIZE_MESSAGE)


class TestAcFr0101ScopeLimit:
    """AC-FR-01-01, PRD §8.1 INVALID_SIZE — AC-FR-01-02~05 / FR-02~05 범위 제한."""

    def test_scope_module_docstring_declares_ac_fr_01_01_only(self) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE."""
        # Given
        module = importlib.import_module(
            "tests.boundary.test_validator_shape_ac_fr_01_01"
        )
        # When / Then — AC-FR-01-01
        assert AC_FR_01_01 in module.__doc__
        assert "INVALID_SIZE" in module.__doc__

    def test_scope_shape_suite_does_not_import_blank_finder(self) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE."""
        # Given
        source = Path(__file__).read_text(encoding="utf-8")
        import_lines = [
            line
            for line in source.splitlines()
            if line.strip().startswith(("from ", "import "))
        ]
        # When / Then — AC-FR-01-01 (FR-02 coordinate discovery out of scope)
        joined = "\n".join(import_lines)
        assert "blank_finder" not in joined
        assert "BlankFinder" not in joined

    def test_scope_shape_suite_does_not_import_solver(self) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE."""
        # Given
        source = Path(__file__).read_text(encoding="utf-8")
        import_lines = [
            line
            for line in source.splitlines()
            if line.strip().startswith(("from ", "import "))
        ]
        # When / Then — AC-FR-01-01 (FR-05 combination solver out of scope)
        joined = "\n".join(import_lines)
        assert "solver" not in joined
        assert "magic_square_validator" not in joined

    def test_scope_forbidden_error_codes_not_used_as_expected_pass(
        self, boundary_validator: Any
    ) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE."""
        # Given — shape failures only; not blank/range/duplicate (AC-FR-01-02~04)
        grid = None
        # When
        result = boundary_validator.validate(grid)
        # Then — AC-FR-01-01
        assert result.error.code not in FORBIDDEN_ERROR_CODES_AC_FR_01_01

    def test_scope_no_valid_4x4_shape_failure_test_in_module(self) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE."""
        # Given
        module = importlib.import_module(
            "tests.boundary.test_validator_shape_ac_fr_01_01"
        )
        # When
        test_names = [
            name
            for name, obj in inspect.getmembers(module, inspect.isfunction)
            if name.startswith("test_")
        ]
        # Then — AC-FR-01-01 (valid 4×4 happy path excluded)
        assert not any("valid_4x4" in name or "happy_path_success" in name for name in test_names)
