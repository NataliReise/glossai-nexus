#!/usr/bin/env python3
"""Run Return Resonance with explicit local file paths.

This command is the small local-first CLI after the fixed public demo.
It accepts a return artifact, a slot file, and an output directory.
It does not publish anything online.
"""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

NEXUS_01_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(NEXUS_01_ROOT))

from return_resonance import (
    MatchStatus,
    ReturnResultError,
    load_return_slots,
    match_return_artifact,
    open_return_result,
    parse_return_artifact,
)
from return_resonance.artifact import ReturnArtifactParseError
from return_resonance.slots import ReturnSlotLoadError


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)

    artifact_path = args.artifact.expanduser().resolve()
    slots_path = args.slots.expanduser().resolve()
    output_dir = args.output_dir.expanduser().resolve()

    print("Nexus 01 - Return Resonance")
    print("===========================")
    print()
    print("This command opens a local return resonance layer.")
    print("It does not read First Spark internals and does not publish anything online.")
    print()

    try:
        artifact = parse_return_artifact(artifact_path.read_text(encoding="utf-8"))
        slots = load_return_slots(slots_path)
        match = match_return_artifact(artifact, slots)
    except FileNotFoundError as error:
        print("Error: file not found:", error.filename)
        return 2
    except (ReturnArtifactParseError, ReturnSlotLoadError) as error:
        print("Error:", error)
        return 2

    print("Artifact:", _display_path(artifact_path))
    print("Slot file:", _display_path(slots_path))
    print("Output dir:", _display_path(output_dir))
    print("Match status:", match.status.value)
    print("Message:", match.message)
    print()

    if match.status not in {MatchStatus.MATCH_WAITING, MatchStatus.MATCH_OPENED}:
        print("No local result was opened because the artifact did not match a slot.")
        return 1

    try:
        result = open_return_result(artifact, match, output_dir)
    except ReturnResultError as error:
        print("Error:", error)
        return 2

    if result.created:
        print("Local result created:", _display_path(result.path))
    else:
        print("Local result reused:", _display_path(result.path))

    print()
    print("Privacy reminder:")
    print("Do not publish real return artifacts or local return results unless reviewed carefully.")

    return 0


def _parse_args(argv: list[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Open a local Nexus 01 Return Resonance layer.",
    )
    parser.add_argument(
        "--artifact",
        required=True,
        type=Path,
        help="Path to a structured return artifact text file.",
    )
    parser.add_argument(
        "--slots",
        required=True,
        type=Path,
        help="Path to a return slot JSON file.",
    )
    parser.add_argument(
        "--output-dir",
        required=True,
        type=Path,
        help="Directory for local return result files.",
    )
    return parser.parse_args(argv)


def _display_path(path: Path) -> Path:
    try:
        return path.relative_to(Path.cwd())
    except ValueError:
        return path


if __name__ == "__main__":
    raise SystemExit(main())
