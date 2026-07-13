#!/usr/bin/env python3
"""Run the public-safe Nexus 01 Resonance Return demo in a separate workspace."""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path
import sys

DEMO_DIR = Path(__file__).resolve().parent
NEXUS_01_ROOT = DEMO_DIR.parents[1]
sys.path.insert(0, str(NEXUS_01_ROOT))

from open_resonance_return import LocalResonanceResult, open_resonance_return_files

ARTIFACT_FILE = DEMO_DIR / "resonance_return.demo.json"
SLOT_TEMPLATE = DEMO_DIR / "return_slots.template.json"


def run_demo(workspace: str | Path, reset: bool = False) -> LocalResonanceResult:
    """Copy mutable demo state into a workspace and open the safe demo artifact."""

    workspace_path = Path(workspace).expanduser().resolve()
    if reset and workspace_path.exists():
        shutil.rmtree(workspace_path)

    workspace_path.mkdir(parents=True, exist_ok=True)
    slots_path = workspace_path / "return_slots.json"
    output_dir = workspace_path / "results"

    if not slots_path.exists():
        shutil.copyfile(SLOT_TEMPLATE, slots_path)

    return open_resonance_return_files(
        artifact_path=ARTIFACT_FILE,
        slots_path=slots_path,
        output_dir=output_dir,
    )


def _parse_args(argv: list[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run the public-safe Nexus 01 Resonance Return demo.",
    )
    parser.add_argument(
        "--workspace",
        type=Path,
        default=Path("/tmp/nexus-01-resonance-return-demo"),
        help="Mutable demo workspace (default: /tmp/nexus-01-resonance-return-demo).",
    )
    parser.add_argument(
        "--reset",
        action="store_true",
        help="Delete and recreate the demo workspace before opening.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)

    print("Nexus 01 - Public Resonance Return Demo")
    print("=======================================")
    print()
    print("All identifiers and meanings in this demo are invented and public-safe.")
    print()

    try:
        result = run_demo(args.workspace, reset=args.reset)
    except (OSError, ValueError) as error:
        print("Error:", error)
        return 1

    action = "created" if result.created else "reused"
    print(f"Local result {action}:", result.path)
    print("Slot state:", "opened now" if result.slot_state_changed else "already opened")
    print()
    print("Open the Markdown file above to inspect the Resonance Artifact and Nexus Echo.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
