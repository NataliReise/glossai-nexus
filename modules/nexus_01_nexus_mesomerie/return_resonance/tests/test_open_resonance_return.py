"""Tests for the practical local Resonance Return opening command."""

from __future__ import annotations

import json
from pathlib import Path
import sys
import tempfile

NEXUS_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(NEXUS_ROOT))

from open_resonance_return import LocalResonanceOpenError, open_resonance_return_files
from return_resonance.resonance_render_bridge import (
    ChamberSelections,
    build_resonance_return_artifact,
)
from return_resonance.token import ResonanceToken

LIBRARY_DIR = NEXUS_ROOT / "resonance_language_library" / "v0_1"


def _token() -> ResonanceToken:
    return ResonanceToken(
        token_version="N01-RT-1",
        token_type="resonance-activation",
        module_id="N01",
        layer_id="return-resonance-1",
        origin_trace_id="n01-test-origin",
        return_slot_id="test-return-slot",
        package_id="test-package",
        enabled_chambers=("resonance",),
    )


def _artifact_dict() -> dict[str, str]:
    artifact = build_resonance_return_artifact(
        _token(),
        ChamberSelections(
            image_id="waiting-lantern",
            image_response_id="appearing-path",
            scent_id="summer-rain",
            scent_response_id="possibility-of-encounter",
            movement_id="falling-feather",
            movement_response_id="crossing-feather",
            wish_word="courage",
            return_word="trust",
        ),
    )
    return artifact.to_dict()


def _write_inputs(root: Path, *, slot_status: str = "waiting") -> tuple[Path, Path, Path]:
    artifact_path = root / "return-artifact.json"
    slots_path = root / "return-slots.json"
    output_dir = root / "results"

    artifact_path.write_text(
        json.dumps(_artifact_dict(), indent=2) + "\n",
        encoding="utf-8",
    )
    slots_path.write_text(
        json.dumps(
            {
                "document_status": "local test fixture",
                "slots": [
                    {
                        "origin_trace_id": "n01-test-origin",
                        "return_slot_id": "test-return-slot",
                        "module_id": "N01",
                        "package_id": "test-package",
                        "layer_id": "return-resonance-1",
                        "status": slot_status,
                        "result_file": "test-return.local.md",
                        "public_safe_label": "test light",
                        "note": "test only",
                    }
                ],
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    return artifact_path, slots_path, output_dir


def _slot_status(path: Path) -> str:
    document = json.loads(path.read_text(encoding="utf-8"))
    return document["slots"][0]["status"]


def test_first_open_creates_result_and_marks_slot_opened() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        artifact_path, slots_path, output_dir = _write_inputs(root)

        result = open_resonance_return_files(
            artifact_path,
            slots_path,
            output_dir,
            LIBRARY_DIR,
        )

        assert result.created is True
        assert result.slot_state_changed is True
        assert result.path == output_dir / "test-return.local.md"
        assert result.path.exists()
        assert result.content == result.path.read_text(encoding="utf-8")
        assert "# Resonance Return: test-return-slot" in result.content
        assert "Resonance Artifact" in result.content
        assert "Nexus Echo" in result.content
        assert "Summer rain" in result.content
        assert result.opened.output.nexus_echo.word_counts == (2, 4, 6, 4, 1)
        assert _slot_status(slots_path) == "opened"


def test_second_open_reuses_result_without_overwriting() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        artifact_path, slots_path, output_dir = _write_inputs(root)

        first = open_resonance_return_files(
            artifact_path,
            slots_path,
            output_dir,
            LIBRARY_DIR,
        )
        original = first.path.read_text(encoding="utf-8")
        first.path.write_text(original + "\nLOCAL NOTE\n", encoding="utf-8")

        second = open_resonance_return_files(
            artifact_path,
            slots_path,
            output_dir,
            LIBRARY_DIR,
        )

        assert second.created is False
        assert second.slot_state_changed is False
        assert second.content.endswith("LOCAL NOTE\n")
        assert second.path.read_text(encoding="utf-8").endswith("LOCAL NOTE\n")
        assert _slot_status(slots_path) == "opened"


def test_opened_slot_without_result_is_rejected() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        artifact_path, slots_path, output_dir = _write_inputs(root, slot_status="opened")

        try:
            open_resonance_return_files(
                artifact_path,
                slots_path,
                output_dir,
                LIBRARY_DIR,
            )
        except LocalResonanceOpenError as error:
            assert "marked as opened" in str(error)
            assert "result file is missing" in str(error)
        else:
            raise AssertionError("Expected LocalResonanceOpenError")


def test_mismatched_package_creates_nothing_and_changes_no_state() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        artifact_path, slots_path, output_dir = _write_inputs(root)
        artifact = json.loads(artifact_path.read_text(encoding="utf-8"))
        artifact["package_id"] = "wrong-package"
        artifact_path.write_text(json.dumps(artifact, indent=2) + "\n", encoding="utf-8")

        try:
            open_resonance_return_files(
                artifact_path,
                slots_path,
                output_dir,
                LIBRARY_DIR,
            )
        except Exception as error:
            assert "package_mismatch" in str(error)
        else:
            raise AssertionError("Expected mismatch error")

        assert not output_dir.exists()
        assert _slot_status(slots_path) == "waiting"


if __name__ == "__main__":
    test_first_open_creates_result_and_marks_slot_opened()
    test_second_open_reuses_result_without_overwriting()
    test_opened_slot_without_result_is_rejected()
    test_mismatched_package_creates_nothing_and_changes_no_state()
    print("Local Resonance Return opening tests passed.")
