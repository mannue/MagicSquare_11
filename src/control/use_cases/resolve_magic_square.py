"""Resolve magic square use case — Boundary validation before Domain."""

from __future__ import annotations

from typing import Any

from src.boundary.errors import ValidationFailure
from src.boundary.validator import BoundaryValidator


class ResolveMagicSquareUseCase:
    """Orchestrates shape validation and domain resolution."""

    def __init__(
        self,
        domain_resolver: Any,
        validator: BoundaryValidator | None = None,
    ) -> None:
        self._domain_resolver = domain_resolver
        self._validator = validator or BoundaryValidator()

    def execute(self, grid: Any) -> ValidationFailure | Any:
        validation = self._validator.validate(grid)
        if not validation.success:
            return validation
        return self._run_domain(grid)

    def _run_domain(self, grid: Any) -> Any:
        return self._domain_resolver.resolve(grid)
