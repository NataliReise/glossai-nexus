#!/usr/bin/env python3
"""Tests for local Resonance Return opening orchestration."""

from __future__ import annotations

import json
from pathlib import Path
import sys
import tempfile

NEXUS_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(NEXUS_ROOT))

from return_resonance.local_opening import (
    LocalResonanceOpeningError,
    open_local_resonance_return,
)


ARTIFACT = {
    "artifact_version": "0.1",
    "artifact_type": "resonance-return",
    "module_id": "N01",
    "layer_id": "return-resonance-1",
    "origin_trace_id": "trace-demo-001",
    "return_slot_id": "return-slot-demo-001",
    "package_id": "nexus-01-demo-package",
    "language_library": "resonance-en-v0.1",
    "image_id": "waiting-lantern",
    "image_response_id": "appearing-path",
    "scent_id": "summer-rain",
    "scent_response_id": "possibility-of-encounter",
    "movement_id": "falling-feather",
    "movement_response_id": "crossing-feather",
    "wish_word": "courage",
    "return_word": "trust",
}


def slot_data(*, package_id: str = "nexus-01-demo-package") -> dict[str, object]:
    return {
        "slots": [
            {
                "origin_trace_id": "trace-demo-001",
                "return_slot_id": "return-slot-demo-001",
                "module_id": "N01",
                "package_id": package_id,
                "layer_id": "return-resonance-1",
                "status": "waiting",
                "result_file": "resonance-result.txt",
                "public_safe_label": "demo path",
                "note": "Local test slot.",
            }
        ]
    }


def write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def test_matching_return_opens_both_local_outputs() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        artifact_path = root / "return.json"
        slot_path = root / "slots.json"
        write_json(artifact_path, ARTIFACT)
        write_json(slot_path, slot_data())

        result = open_local_resonance_return(artifact_path, slot_path)

    assert result.opened.match.status.value == "match_waiting"
    assert "A lantern waits in the dark." in result.opened.output.resonance_artifact.text
    assert result.opened.output.nexus_echo.text.endswith("trust")
    assert result.opened.output.nexus_echo.word_counts == (2, 4, 6, 4, 1)


def test_mismatch_fails_before_any_output_is_returned() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        artifact_path = root / "return.json"
        slot_path = root / "slots.json"
        write_json(artifact_path, ARTIFACT)
        write_json(slot_path, slot_data(package_id="wrong-package"))

        try:
            open_local_resonance_return(artifact_path, slot_path)
        except LocalResonanceOpeningError as error:
            assert "package_mismatch" in str(error)
        else:
            raise AssertionError("Expected a package mismatch to stop local opening.")


def test_invalid_artifact_and_slot_files_are_wrapped_locally() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        artifact_path = root / "return.json"
        slot_path = root / "slots.json"
        artifact_path.write_text("not json", encoding="utf-8")
        write_json(slot_path, slot_data())

        try:
            open_local_resonance_return(artifact_path, slot_path)
        except LocalResonanceOpeningError as error:
            assert "not valid JSON" in str(error)
        else:
            raise AssertionError("Expected invalid artifact JSON to fail.")

        write_json(artifact_path, ARTIFACT)
        slot_path.write_text("{}\n", encoding="utf-8")

        try:
            open_local_resonance_return(artifact_path, slot_path)
        except LocalResonanceOpeningError as error:
            assert "slots list" in str(error)
        else:
            raise AssertionError("Expected an invalid slot contract to fail.")


def test_successful_opening_does_not_mutate_slot_file() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        artifact_path = root / "return.json"
        slot_path = root / "slots.json"
        write_json(artifact_path, ARTIFACT)
        write_json(slot_path, slot_data())
        before = slot_path.read_bytes()

        open_local_resonance_return(artifact_path, slot_path)

        after = slot_path.read_bytes()

    assert after == before


if __name__ == "__main__":
    test_matching_return_opens_both_local_outputs()
    test_mismatch_fails_before_any_output_is_returned()
    test_invalid_artifact_and_slot_files_are_wrapped_locally()
    test_successful_opening_does_not_mutate_slot_file()
    print("Local Resonance opening tests passed.")
