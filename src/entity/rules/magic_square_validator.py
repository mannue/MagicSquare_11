"""Magic square validity checks for complete 4x4 boards."""

from __future__ import annotations

MAGIC_CONSTANT = 34
_MIN_VALUE = 1
_MAX_VALUE = 16
_GRID_SIZE = 4


def _sum_row(grid: list[list[int]], row_index: int) -> int:
    return sum(grid[row_index])


def _sum_col(grid: list[list[int]], col_index: int) -> int:
    return sum(grid[row_index][col_index] for row_index in range(_GRID_SIZE))


def _sum_diagonal(grid: list[list[int]], *, anti: bool = False) -> int:
    if anti:
        return sum(
            grid[index][_GRID_SIZE - 1 - index] for index in range(_GRID_SIZE)
        )
    return sum(grid[index][index] for index in range(_GRID_SIZE))


def is_magic_square(grid: list[list[int]]) -> bool:
    """Return True when the board satisfies magic square invariants."""
    values = [cell for row in grid for cell in row]
    if any(cell == 0 for cell in values):
        return False
    if any(cell < _MIN_VALUE or cell > _MAX_VALUE for cell in values):
        return False
    if len(values) != len(set(values)):
        return False
    if any(_sum_row(grid, row_index) != MAGIC_CONSTANT for row_index in range(_GRID_SIZE)):
        return False
    if any(_sum_col(grid, col_index) != MAGIC_CONSTANT for col_index in range(_GRID_SIZE)):
        return False
    if _sum_diagonal(grid) != MAGIC_CONSTANT:
        return False
    if _sum_diagonal(grid, anti=True) != MAGIC_CONSTANT:
        return False
    return True
