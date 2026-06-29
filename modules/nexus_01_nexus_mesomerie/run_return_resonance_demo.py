#!/usr/bin/env python3
"""Run the safe public Return Resonance demo for Nexus 01.

This script uses only public demo data from the examples directory.
It creates a local .local.md result file next to the demo runner.
That local result file is ignored by Git.
"""

from __future__ import annotations

from pathlib import Path
import sys

NEXUS_01_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(NEXUS_01_ROOT))

from return_resonance import (
    MatchStatus,
    load_return_slots,
    match_return_artifact,
    open_return_result,
    parse_return_artifact,
)

EXAMPLES_DIR = NEXUS_01_ROOT / "examples"
DEMO_ARTIFACT_PATH = EXAMPLES_DIR / "return_artifact.demo.txt"
DEMO_SLOT_PATH = EXAMPLES_DIR / "return_slot.demo.json"
OUTPUT_DIR = NEXUS_01_ROOT


def main() -> int:
    print("Nexus 01 - Return Resonance Demo")
    print("=================================")
    print()
    print("This demo uses only safe public example data.")
    print("It does not read First Spark internals and does not publish anything online.")
    print()

    artifact = parse_return_artifact(DEMO_ARTIFACT_PATH.read_text(encoding="utf-8"))
    slots = load_return_slots(DEMO_SLOT_PATH)
    match = match_return_artifact(artifact, slots)

    print("Artifact:", DEMO_ARTIFACT_PATH.relative_to(NEXUS_01_ROOT))
    print("Slot file:", DEMO_SLOT_PATH.relative_to(NEXUS_01_ROOT))
    print("Match status:", match.status.value)
    print("Message:", match.message)
    print()

    if match.status not in {MatchStatus.MATCH_WAITING, MatchStatus.MATCH_OPENED}:
        print("No local result was opened because the artifact did not match a slot.")
        return 1

    result = open_return_result(artifact, match, OUTPUT_DIR)
    result_display_path = _display_path(result.path)

    if result.created:
        print("Local result created:", result_display_path)
    else:
        print("Local result reused:", result_display_path)

    print()
    print("--- Local result preview ---")
    print()
    print(_preview(result.content))
    print()
    print("Run this script again to see the same result reused instead of regenerated.")
    print()
    print("Privacy reminder:")
    print("Do not publish real return artifacts or local return results unless reviewed carefully.")

    return 0


def _display_path(path: Path) -> Path:
    try:
        return path.relative_to(NEXUS_01_ROOT)
    except ValueError:
        return path


def _preview(content: str, max_lines: int = 24) -> str:
    lines = content.splitlines()
    preview_lines = lines[:max_lines]
    if len(lines) > max_lines:
        preview_lines.append("...")
    return "\n".join(preview_lines)


if __name__ == "__main__":
    raise SystemExit(main())
