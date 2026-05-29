"""Golden Master scenario definitions for Magic Square Solver output."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Callable

from src.boundary.errors import ValidationFailure
from src.boundary.validator import BoundaryValidator
from src.control.use_cases.solve_partial_magic_square import solution
from src.entity.errors import UnsolvableDomainError
from src.entity.rules.blank_finder import find_blank_coords
from src.entity.rules.missing_number_finder import find_not_exist_nums
from tests.conftest import (
    DUPLICATE_NON_ZERO_CODE,
    G0_COMPLETE,
    G1_STEP_A,
    G2_REVERSE,
    G3_UNSOLVABLE,
    INVALID_BLANK_COUNT_CODE,
    copy_grid,
    grid_g1_with_cell,
)

Grid = list[list[int]]
SECTION_HEADER_PATTERN = re.compile(r"^\[(?P<name>[a-z][a-z0-9_]*)\]\s*$", re.MULTILINE)

NORMAL_SUCCESS_GRID: Grid = copy_grid(G1_STEP_A)


@dataclass(frozen=True)
class GoldenScenario:
    """One Golden Master input scenario."""

    tc_id: str
    name: str
    grid: Grid
    expect_success: bool = True
    expect_error: str | None = None


SCENARIOS: tuple[GoldenScenario, ...] = (
    GoldenScenario("GM-TC-01", "normal_success", copy_grid(NORMAL_SUCCESS_GRID)),
    GoldenScenario("GM-TC-02", "reverse_success", copy_grid(G2_REVERSE)),
    GoldenScenario(
        "GM-TC-03",
        "invalid_blank_count",
        copy_grid(G0_COMPLETE),
        expect_success=False,
        expect_error=INVALID_BLANK_COUNT_CODE,
    ),
    GoldenScenario(
        "GM-TC-04",
        "duplicate_number",
        grid_g1_with_cell(0, 0, 6),
        expect_success=False,
        expect_error=DUPLICATE_NON_ZERO_CODE,
    ),
    GoldenScenario(
        "GM-TC-05",
        "no_valid_solution",
        copy_grid(G3_UNSOLVABLE),
        expect_success=False,
        expect_error="UnsolvableDomainError",
    ),
)

SCENARIO_BY_NAME: dict[str, GoldenScenario] = {
    scenario.name: scenario for scenario in SCENARIOS
}


def format_grid(grid: Grid) -> str:
    """Serialize a 4x4 grid as space-separated rows."""
    return "\n".join(" ".join(str(cell) for cell in row) for row in grid)


def format_solution(values: list[int]) -> str:
    """Serialize solver success payload as int[6]."""
    return "[" + ",".join(str(value) for value in values) + "]"


def parse_solution_payload(output_line: str) -> list[int]:
    """Parse ``[r1,c1,n1,r2,c2,n2]`` from a serialized Output line."""
    inner = output_line.strip().removeprefix("[").removesuffix("]")
    return [int(part) for part in inner.split(",")]


def run_scenario(scenario: GoldenScenario) -> str:
    """Run validate/solve flow and return the Golden Master body for one scenario."""
    validator = BoundaryValidator()
    validation = validator.validate(scenario.grid)

    lines = ["Input:", format_grid(scenario.grid)]

    if isinstance(validation, ValidationFailure):
        lines.extend(["Error:", validation.error.code])
        return "\n".join(lines)

    try:
        solve_result = solution(scenario.grid)
    except UnsolvableDomainError:
        lines.extend(["Error:", "UnsolvableDomainError"])
        return "\n".join(lines)

    lines.extend(["Output:", format_solution(solve_result)])
    return "\n".join(lines)


def serialize_scenario_block(scenario: GoldenScenario) -> str:
    """Serialize one scenario section including header."""
    return f"[{scenario.name}]\n{run_scenario(scenario)}"


def build_golden_master_document(
    scenarios: tuple[GoldenScenario, ...] = SCENARIOS,
    runner: Callable[[GoldenScenario], str] = run_scenario,
) -> str:
    """Build the full Golden Master expected file contents."""
    blocks: list[str] = []
    for index, scenario in enumerate(scenarios):
        block = f"[{scenario.name}]\n{runner(scenario)}"
        blocks.append(block)
        if index < len(scenarios) - 1:
            blocks.append("")
            blocks.append("________________________________________")
            blocks.append("")
    return "\n".join(blocks) + "\n"


def parse_golden_master_sections(text: str) -> dict[str, str]:
    """Parse baseline text into ``section_name -> full block`` mapping."""
    matches = list(SECTION_HEADER_PATTERN.finditer(text))
    if not matches:
        return {}

    sections: dict[str, str] = {}
    for index, match in enumerate(matches):
        name = match.group("name")
        start = match.start()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        block = text[start:end]
        block = re.sub(
            r"\n+________________________________________\s*$",
            "",
            block,
            flags=re.MULTILINE,
        )
        sections[name] = block.rstrip() + "\n"
    return sections


def normalize_block(block: str) -> str:
    """Normalize section text for stable file comparison."""
    return block.rstrip() + "\n"


def assert_success_contract(scenario: GoldenScenario, payload: list[int]) -> None:
    """Verify int[6], row-major blank order, and 1-index coordinates."""
    assert len(payload) == 6, "success payload must be int[6]"

    r1, c1, n1, r2, c2, n2 = payload
    for coordinate in (r1, c1, r2, c2):
        assert 1 <= coordinate <= 4, "coordinates must be 1-index in 1..4"

    blank_coords = find_blank_coords(scenario.grid)
    assert (r1, c1) == (blank_coords[0][0] + 1, blank_coords[0][1] + 1)
    assert (r2, c2) == (blank_coords[1][0] + 1, blank_coords[1][1] + 1)

    missing_small, missing_large = find_not_exist_nums(scenario.grid)
    assert {n1, n2} == {missing_small, missing_large}


def assert_small_first_combination(scenario: GoldenScenario, payload: list[int]) -> None:
    """Verify attempt-1 (small on first blank) succeeded."""
    _n1, _c1, n1, _r2, _c2, n2 = payload
    missing_small, missing_large = find_not_exist_nums(scenario.grid)
    assert n1 == missing_small and n2 == missing_large


def assert_reverse_fallback_combination(scenario: GoldenScenario, payload: list[int]) -> None:
    """Verify attempt-2 (large on first blank) succeeded."""
    _r1, _c1, n1, _r2, _c2, n2 = payload
    missing_small, missing_large = find_not_exist_nums(scenario.grid)
    assert n1 == missing_large and n2 == missing_small
