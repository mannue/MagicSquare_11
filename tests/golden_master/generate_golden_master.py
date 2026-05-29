"""Generate or refresh tests/golden_master_expected.txt from current solver output."""

from __future__ import annotations

import argparse
from pathlib import Path

from tests.golden_master.approve import DEFAULT_GOLDEN_MASTER_PATH, write_golden_master
from tests.golden_master.scenarios import build_golden_master_document


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate Golden Master baseline for Magic Square Solver output.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_GOLDEN_MASTER_PATH,
        help="Path to golden master expected file (default: tests/golden_master_expected.txt)",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing baseline without comparison.",
    )
    args = parser.parse_args()

    content = build_golden_master_document()
    if args.output.is_file() and not args.force:
        print(
            f"Baseline already exists: {args.output}\n"
            "Use --force to overwrite, or run pytest -m golden_master -v."
        )
        return 1

    write_golden_master(content, args.output)
    print(f"Golden Master baseline written to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
