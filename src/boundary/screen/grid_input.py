"""Parse 4x4 grid values from screen entry widgets."""

from __future__ import annotations

import tkinter as tk
from typing import Any

GRID_SIZE = 4


def read_grid_from_entries(cells: list[list[tk.Entry]]) -> list[list[int]] | None:
    """Return parsed grid, or None when every cell is empty (AC-FR-01-01 None analogue)."""
    values: list[list[int | None]] = []
    for row in cells:
        row_values: list[int | None] = []
        for entry in row:
            text = entry.get().strip()
            if text == "":
                row_values.append(None)
                continue
            row_values.append(int(text))
        values.append(row_values)

    if all(cell is None for row in values for cell in row):
        return None

    parsed: list[list[int]] = []
    for row in values:
        parsed.append([0 if cell is None else cell for cell in row])
    return parsed


def set_grid_on_entries(cells: list[list[tk.Entry]], grid: list[list[int]]) -> None:
    """Fill entry widgets from a 4x4 integer grid."""
    for row_index in range(GRID_SIZE):
        for col_index in range(GRID_SIZE):
            value = grid[row_index][col_index]
            cells[row_index][col_index].delete(0, tk.END)
            if value != 0:
                cells[row_index][col_index].insert(0, str(value))


def clear_entries(cells: list[list[tk.Entry]]) -> None:
    """Clear all grid entry widgets."""
    for row in cells:
        for entry in row:
            entry.delete(0, tk.END)
