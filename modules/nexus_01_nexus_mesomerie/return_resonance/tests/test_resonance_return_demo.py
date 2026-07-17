#!/usr/bin/env python3
"""Verify the complete public-safe Resonance Return demo."""

from __future__ import annotations

import json
from pathlib import Path
import sys
import tempfile

NEXUS_01_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(NEXUS_01_ROOT))

from examples.resonance_return_demo.run_demo import (
    ARTIFACT_FILE,
    SLOT_TEMPLATE,
    run_demo,
)

def main() -> None:
    artifact_before = ARTIFACT_FILE.read_text(encoding="utf-8")
    slots_before = SLOT_TEMPLATE.read_text(encoding="utf-8")

    with tempfile.TemporaryDirectory() as temporary_directory:
        workspace = Path(temporary_directory) / "demo-workspace"

        first = run_demo(workspace, reset=True)
        assert first.created is True
        assert first.slot_state_changed is True
        assert first.path.exists()
        assert "## Compact Resonance" in first.content
        assert "Summer rain carries the possibility of encounter." in first.content
        assert "\ntrust\n```" in first.content
        assert '"generator_id": "nexus-01-compact-resonance"' in first.content
        assert "Resonance Artifact" not in first.content
        assert "Nexus Echo" not in first.content

        mutable_slots = json.loads(
            (workspace / "return_slots.json").read_text(encoding="utf-8")
        )
        assert mutable_slots["slots"][0]["status"] == "opened"

        result_before = first.path.read_text(encoding="utf-8")
        first.path.write_text(result_before + "\nLocal demo note.\n", encoding="utf-8")

        second = run_demo(workspace)
        assert second.created is False
        assert second.slot_state_changed is False
        assert second.content.endswith("Local demo note.\n")

        reset = run_demo(workspace, reset=True)
        assert reset.created is True
        assert reset.slot_state_changed is True
        assert "Local demo note." not in reset.content
        assert reset.content == result_before

    assert ARTIFACT_FILE.read_text(encoding="utf-8") == artifact_before
    assert SLOT_TEMPLATE.read_text(encoding="utf-8") == slots_before

    print("Public Resonance Return demo tests passed.")


if __name__ == "__main__":
    main()
