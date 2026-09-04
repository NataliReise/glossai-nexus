#!/usr/bin/env python3
"""Thin local terminal interface for Nexus Builder V0.1."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys


SCRIPT_PATH = Path(__file__).resolve()
NEXUS_ROOT = SCRIPT_PATH.parents[1]
PACKAGING_ROOT = SCRIPT_PATH.parent
for import_root in (PACKAGING_ROOT, NEXUS_ROOT):
    if str(import_root) not in sys.path:
        sys.path.insert(0, str(import_root))

from nexus_builder_core import (  # noqa: E402
    NexusBuilderError,
    NexusConstellation,
    inspect_archive_block,
    inspect_nexus,
    verify_nexus_constellation,
)


def _add_nexus_root_argument(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--nexus-root",
        type=Path,
        default=NEXUS_ROOT,
        help="explicit Nexus 01 root to inspect",
    )


def _print_constellation(constellation: NexusConstellation) -> None:
    print("Archive constellation")
    print("")
    print("Built-in Blocks:")
    if constellation.builtin_blocks:
        for block in constellation.builtin_blocks:
            print(f"  {block.block_id} — {block.title}")
    else:
        print("  (none)")
    print("")
    print("Coupled Blocks:")
    if constellation.coupled_blocks:
        for block in constellation.coupled_blocks:
            print(f"  {block.block_id} — {block.title}")
    else:
        print("  (none)")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Inspect and verify a local Nexus 01 Archive constellation."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    inspect_nexus_parser = subparsers.add_parser(
        "inspect-nexus",
        help="inspect one explicit Nexus 01 root",
    )
    _add_nexus_root_argument(inspect_nexus_parser)

    inspect_block_parser = subparsers.add_parser(
        "inspect-block",
        help="inspect one explicit Archive Block directory",
    )
    inspect_block_parser.add_argument("block", type=Path)

    constellation_parser = subparsers.add_parser(
        "show-constellation",
        help="show built-in and deliberately coupled Archive Blocks",
    )
    _add_nexus_root_argument(constellation_parser)

    verify_parser = subparsers.add_parser(
        "verify",
        help="verify the current Archive constellation without changing it",
    )
    _add_nexus_root_argument(verify_parser)

    args = parser.parse_args(argv)

    try:
        if args.command == "inspect-block":
            block = inspect_archive_block(args.block)
            print("Archive Block inspection passed.")
            print(f"Block ID: {block.block_id}")
            print(f"Title: {block.title}")
            print(f"Target: {block.target_module}/{block.target_chamber}")
            print(f"Schema: {block.schema_version}")
            print(f"Entries: {len(block.entries)}")
            return 0

        if args.command == "inspect-nexus":
            constellation = inspect_nexus(args.nexus_root)
            print("Nexus inspection passed.")
            print(f"Nexus root: {constellation.nexus_root}")
            print(f"Built-in Archive Blocks: {len(constellation.builtin_blocks)}")
            print(f"Coupled Archive Blocks: {len(constellation.coupled_blocks)}")
            return 0

        if args.command == "show-constellation":
            _print_constellation(inspect_nexus(args.nexus_root))
            return 0

        if args.command == "verify":
            constellation = verify_nexus_constellation(args.nexus_root)
            print("Nexus constellation verification passed.")
            print(f"Archive Blocks: {len(constellation.block_ids)}")
            return 0

    except NexusBuilderError as error:
        print(f"Nexus Builder refused the request: {error}", file=sys.stderr)
        return 1

    parser.error(f"unsupported Builder command: {args.command}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
