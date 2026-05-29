"""Missing number discovery for partial magic square boards."""

from __future__ import annotations

_MIN_VALUE = 1
_MAX_VALUE = 16


def find_not_exist_nums(grid: list[list[int]]) -> list[int]:
    """Return absent values from 1..16 in ascending order."""
    present = {cell for row in grid for cell in row if cell != 0}
    return [value for value in range(_MIN_VALUE, _MAX_VALUE + 1) if value not in present]
