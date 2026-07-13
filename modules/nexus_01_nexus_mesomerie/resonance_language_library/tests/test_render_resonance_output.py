"""End-to-end tests for the complete local Resonance output."""

from __future__ import annotations

import json
from pathlib import Path
import sys

LIBRARY_ROOT = Path(__file__).resolve().parents[1]
NEXUS_ROOT = LIBRARY_ROOT.parent
sys.path.insert(0, str(NEXUS_ROOT))

from resonance_language_library.render_resonance_output import (
    ResonanceOutputRenderError,
    render_resonance_output,
)

LIBRARY_DIR = LIBRARY_ROOT / "v0_1"
FIXTURES = Path(__file__).resolve().parent / "fixtures" / "resonance_artifact_cases.json"


def _cases() -> list[dict[str, object]]:
    document = json.loads(FIXTURES.read_text(encoding="utf-8"))
    return document["cases"]


def test_all_reference_cases_render_both_outputs() -> None:
    for case in _cases():
        artifact = case["artifact"]
        result = render_resonance_output(artifact, LIBRARY_DIR)

        assert result.resonance_artifact.text == case["expected"], case["id"]
        assert result.nexus_echo.text == case["expected_echo"], case["id"]
        assert result.nexus_echo.path_id == case["id"]
        assert result.nexus_echo.word_counts == (2, 4, 6, 4, 1)
        assert result.text == (
            "Resonance Artifact\n"
            "==================\n\n"
            f"{case['expected']}\n\n"
            "Nexus Echo\n"
            "==========\n\n"
            f"{case['expected_echo']}"
        )


def test_one_invalid_input_stops_the_complete_output() -> None:
    artifact = dict(_cases()[0]["artifact"])
    artifact["movement_response_id"] = "waiting-hand"

    try:
        render_resonance_output(artifact, LIBRARY_DIR)
    except ResonanceOutputRenderError as error:
        assert "No approved Nexus Echo path" in str(error)
    else:
        raise AssertionError("Expected ResonanceOutputRenderError")


if __name__ == "__main__":
    test_all_reference_cases_render_both_outputs()
    test_one_invalid_input_stops_the_complete_output()
    print("Resonance end-to-end output tests passed.")
