"""Magic Square 4x4 boundary screen — validation and solve entry point."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk
from typing import Any

from src.boundary.errors import ValidationFailure, ValidationSuccess
from src.boundary.screen.grid_input import (
    GRID_SIZE,
    clear_entries,
    read_grid_from_entries,
    set_grid_on_entries,
)
from src.boundary.validator import BoundaryValidator

_G1_SAMPLE: list[list[int]] = [
    [1, 14, 15, 4],
    [12, 0, 6, 9],
    [8, 11, 0, 5],
    [13, 2, 3, 16],
]


class MagicSquareScreenApp:
    """Tkinter UI delegating validation to BoundaryValidator."""

    def __init__(self, root: tk.Tk) -> None:
        self._root = root
        self._validator = BoundaryValidator()
        self._cells: list[list[tk.Entry]] = []
        self._result_var = tk.StringVar(value="Enter a 4x4 grid and click Validate.")
        self._build_layout()

    def _build_layout(self) -> None:
        self._root.title("Magic Square 4x4 — Boundary")
        self._root.resizable(False, False)

        frame = ttk.Frame(self._root, padding=12)
        frame.grid(row=0, column=0, sticky="nsew")

        grid_frame = ttk.LabelFrame(frame, text="Grid (blank = 0)", padding=8)
        grid_frame.grid(row=0, column=0, columnspan=2, sticky="ew")

        for row_index in range(GRID_SIZE):
            row_entries: list[tk.Entry] = []
            for col_index in range(GRID_SIZE):
                entry = ttk.Entry(grid_frame, width=4, justify="center")
                entry.grid(row=row_index, column=col_index, padx=2, pady=2)
                row_entries.append(entry)
            self._cells.append(row_entries)

        button_frame = ttk.Frame(frame, padding=(0, 8, 0, 0))
        button_frame.grid(row=1, column=0, columnspan=2, sticky="ew")

        ttk.Button(button_frame, text="Validate", command=self._on_validate).grid(
            row=0, column=0, padx=4
        )
        ttk.Button(button_frame, text="Solve", command=self._on_solve).grid(
            row=0, column=1, padx=4
        )
        ttk.Button(button_frame, text="Load G1", command=self._on_load_g1).grid(
            row=0, column=2, padx=4
        )
        ttk.Button(button_frame, text="Clear", command=self._on_clear).grid(
            row=0, column=3, padx=4
        )
        ttk.Button(
            button_frame,
            text="None Grid (AC-FR-01-01)",
            command=self._on_validate_none,
        ).grid(row=0, column=4, padx=4)

        result_frame = ttk.LabelFrame(frame, text="Result", padding=8)
        result_frame.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(8, 0))
        ttk.Label(
            result_frame,
            textvariable=self._result_var,
            wraplength=420,
            justify="left",
        ).grid(row=0, column=0, sticky="w")

    def _show_validation_result(self, result: ValidationFailure | ValidationSuccess) -> None:
        if isinstance(result, ValidationFailure):
            self._result_var.set(
                f"code={result.error.code}\nmessage={result.error.message}"
            )
            return
        self._result_var.set("Validation passed.")

    def _parse_grid_or_show_error(self) -> list[list[int]] | None | bool:
        try:
            return read_grid_from_entries(self._cells)
        except ValueError:
            self._result_var.set("message=Each cell must be empty, 0, or an integer.")
            return False

    def _on_validate(self) -> None:
        grid = self._parse_grid_or_show_error()
        if grid is False:
            return
        self._show_validation_result(self._validator.validate(grid))

    def _on_validate_none(self) -> None:
        self._show_validation_result(self._validator.validate(None))

    def _on_load_g1(self) -> None:
        set_grid_on_entries(self._cells, _G1_SAMPLE)

    def _on_clear(self) -> None:
        clear_entries(self._cells)
        self._result_var.set("Grid cleared.")

    def _on_solve(self) -> None:
        grid = self._parse_grid_or_show_error()
        if grid is False:
            return
        validation = self._validator.validate(grid)
        if isinstance(validation, ValidationFailure):
            self._show_validation_result(validation)
            return
        try:
            from src.control.use_cases.solve_partial_magic_square import solution

            solve_result = solution(grid)
        except Exception as exc:
            self._result_var.set(f"code=SOLVE_ERROR\nmessage={exc}")
            return
        self._result_var.set(f"success\nsolution={solve_result}")


def main() -> None:
    root = tk.Tk()
    MagicSquareScreenApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
