"""Row-major blank cell discovery for partial magic square boards."""

from __future__ import annotations


def find_blank_coords(grid: list[list[int]]) -> list[tuple[int, int]]:
    """Return 0-index coordinates of blank cells in row-major order."""
    coords: list[tuple[int, int]] = []
    for row_index, row in enumerate(grid):
        for col_index, cell in enumerate(row):
            if cell == 0:
                coords.append((row_index, col_index))
    return coords
