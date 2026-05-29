"""Magic square validity checks for complete 4x4 boards."""

from __future__ import annotations

MAGIC_CONSTANT = 34
_MIN_VALUE = 1
_MAX_VALUE = 16
_GRID_SIZE = 4


def is_magic_square(grid: list[list[int]]) -> bool:
    """Return True when the board satisfies magic square invariants."""
    values = [cell for row in grid for cell in row]
    if any(cell == 0 for cell in values):
        return False
    if any(cell < _MIN_VALUE or cell > _MAX_VALUE for cell in values):
        return False
    if len(values) != len(set(values)):
        return False
    if any(sum(row) != MAGIC_CONSTANT for row in grid):
        return False
    for col_index in range(_GRID_SIZE):
        if sum(grid[row_index][col_index] for row_index in range(_GRID_SIZE)) != MAGIC_CONSTANT:
            return False
    if sum(grid[index][index] for index in range(_GRID_SIZE)) != MAGIC_CONSTANT:
        return False
    if sum(grid[index][_GRID_SIZE - 1 - index] for index in range(_GRID_SIZE)) != MAGIC_CONSTANT:
        return False
    return True
