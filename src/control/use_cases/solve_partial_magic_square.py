"""Solve a partial 4x4 magic square via two combination attempts."""

from __future__ import annotations

from src.entity.errors import UnsolvableDomainError
from src.entity.rules.blank_finder import find_blank_coords
from src.entity.rules.magic_square_validator import is_magic_square
from src.entity.rules.missing_number_finder import find_not_exist_nums


def _filled_grid(
    grid: list[list[int]],
    first_coord: tuple[int, int],
    second_coord: tuple[int, int],
    first_value: int,
    second_value: int,
) -> list[list[int]]:
    filled = [row[:] for row in grid]
    filled[first_coord[0]][first_coord[1]] = first_value
    filled[second_coord[0]][second_coord[1]] = second_value
    return filled


def solution(grid: list[list[int]]) -> list[int]:
    """Return success payload [r1, c1, n1, r2, c2, n2] with 1-index coordinates."""
    blank_coords = find_blank_coords(grid)
    missing_numbers = find_not_exist_nums(grid)
    small, large = missing_numbers[0], missing_numbers[1]
    first_row, first_col = blank_coords[0]
    second_row, second_col = blank_coords[1]

    attempt_one = _filled_grid(
        grid,
        blank_coords[0],
        blank_coords[1],
        small,
        large,
    )
    if is_magic_square(attempt_one):
        return [
            first_row + 1,
            first_col + 1,
            small,
            second_row + 1,
            second_col + 1,
            large,
        ]

    attempt_two = _filled_grid(
        grid,
        blank_coords[0],
        blank_coords[1],
        large,
        small,
    )
    if is_magic_square(attempt_two):
        return [
            first_row + 1,
            first_col + 1,
            large,
            second_row + 1,
            second_col + 1,
            small,
        ]

    raise UnsolvableDomainError("No valid combination produces a magic square.")
