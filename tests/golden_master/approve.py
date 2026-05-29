"""Approve-pattern helpers for Golden Master regression tests."""

from __future__ import annotations

import difflib
from pathlib import Path

from tests.golden_master.scenarios import (
    GoldenScenario,
    build_golden_master_document,
    normalize_block,
    parse_golden_master_sections,
    serialize_scenario_block,
)

DEFAULT_GOLDEN_MASTER_PATH = (
    Path(__file__).resolve().parent.parent / "golden_master_expected.txt"
)


def read_golden_master(path: Path = DEFAULT_GOLDEN_MASTER_PATH) -> str | None:
    """Return baseline text when the file exists."""
    if not path.is_file():
        return None
    return Path(path).read_text(encoding="utf-8")


def write_golden_master(
    content: str,
    path: Path = DEFAULT_GOLDEN_MASTER_PATH,
) -> None:
    """Persist Golden Master baseline text."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")


def unified_diff(expected: str, actual: str) -> str:
    """Return unified diff with ``--- expected`` / ``+++ actual`` headers."""
    return "".join(
        difflib.unified_diff(
            expected.splitlines(keepends=True),
            actual.splitlines(keepends=True),
            fromfile="expected",
            tofile="actual",
        )
    )


def approve_golden_master(
    path: Path = DEFAULT_GOLDEN_MASTER_PATH,
    *,
    auto_create: bool = True,
) -> tuple[str, str | None]:
    """Compare or create the full Golden Master baseline using the approve pattern."""
    actual = build_golden_master_document()
    expected = read_golden_master(path)

    if expected is None:
        if not auto_create:
            raise FileNotFoundError(f"Golden Master baseline not found: {path}")
        write_golden_master(actual, path)
        return "created", None

    if expected == actual:
        return "matched", None

    return "mismatch", unified_diff(expected, actual)


def approve_scenario(
    scenario: GoldenScenario,
    path: Path = DEFAULT_GOLDEN_MASTER_PATH,
    *,
    auto_create: bool = True,
) -> tuple[str, str | None]:
    """Compare or create one scenario section against the baseline file."""
    actual_block = normalize_block(serialize_scenario_block(scenario))
    expected_text = read_golden_master(path)

    if expected_text is None:
        if not auto_create:
            raise FileNotFoundError(f"Golden Master baseline not found: {path}")
        write_golden_master(build_golden_master_document(), path)
        return "created", None

    expected_sections = parse_golden_master_sections(expected_text)
    expected_block = expected_sections.get(scenario.name)

    if expected_block is None:
        if not auto_create:
            raise KeyError(
                f"Scenario [{scenario.name}] missing from baseline: {path}"
            )
        write_golden_master(build_golden_master_document(), path)
        return "created", None

    if normalize_block(expected_block) == actual_block:
        return "matched", None

    return "mismatch", unified_diff(normalize_block(expected_block), actual_block)


def assert_approved_scenario(
    scenario: GoldenScenario,
    path: Path = DEFAULT_GOLDEN_MASTER_PATH,
    *,
    auto_create: bool = True,
) -> None:
    """Assert scenario output matches baseline; fail with unified diff on mismatch."""
    status, diff_text = approve_scenario(scenario, path, auto_create=auto_create)

    if status == "created":
        raise AssertionError(
            f"Golden Master baseline created for [{scenario.name}]; re-run to verify."
        )

    assert status == "matched", (
        f"Golden Master mismatch for {scenario.tc_id} [{scenario.name}].\n"
        f"{diff_text}\n"
        "________________________________________\n"
        "Re-run `python -m tests.golden_master.generate_golden_master --force` "
        "after reviewing intentional output changes."
    )
