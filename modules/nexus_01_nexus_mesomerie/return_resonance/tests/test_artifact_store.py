#!/usr/bin/env python3
"""Tests for safe local Resonance Return Artifact persistence."""

from __future__ import annotations

import json
from pathlib import Path
import sys
import tempfile

NEXUS_01_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(NEXUS_01_ROOT))

from return_resonance.artifact_store import (
    ResonanceArtifactStoreError,
    write_resonance_return_artifact,
)
from return_resonance.resonance_render_bridge import ResonanceReturnArtifact


def artifact() -> ResonanceReturnArtifact:
    return ResonanceReturnArtifact(
        artifact_version="0.1",
        artifact_type="resonance-return",
        module_id="N01",
        layer_id="return-resonance-1",
        origin_trace_id="store-origin-001",
        return_slot_id="store-slot-001",
        package_id="store-package-001",
        language_library="resonance-en-v0.1",
        image_id="waiting-lantern",
        image_response_id="appearing-path",
        scent_id="summer-rain",
        scent_response_id="possibility-of-encounter",
        movement_id="falling-feather",
        movement_response_id="crossing-feather",
        wish_word="courage",
        return_word="trust",
    )


def test_store_writes_exact_artifact_json(tmp_path: Path) -> None:
    destination = tmp_path / "return-artifact.json"

    written_path = write_resonance_return_artifact(artifact(), destination)

    assert written_path == destination
    assert json.loads(destination.read_text(encoding="utf-8")) == artifact().to_dict()
    assert destination.read_text(encoding="utf-8").endswith("\n")


def test_store_refuses_to_overwrite_existing_file(tmp_path: Path) -> None:
    destination = tmp_path / "existing.json"
    destination.write_text("keep me", encoding="utf-8")

    try:
        write_resonance_return_artifact(artifact(), destination)
    except ResonanceArtifactStoreError as error:
        assert "Refusing to overwrite" in str(error)
    else:
        raise AssertionError("Artifact store overwrote an existing file.")

    assert destination.read_text(encoding="utf-8") == "keep me"


def test_store_does_not_create_parent_directories(tmp_path: Path) -> None:
    destination = tmp_path / "missing" / "return-artifact.json"

    try:
        write_resonance_return_artifact(artifact(), destination)
    except ResonanceArtifactStoreError as error:
        assert "Could not write" in str(error)
    else:
        raise AssertionError("Artifact store created an undeclared parent directory.")

    assert not destination.exists()


if __name__ == "__main__":
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        test_store_writes_exact_artifact_json(root)
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        test_store_refuses_to_overwrite_existing_file(root)
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        test_store_does_not_create_parent_directories(root)
    print("Resonance Artifact store tests passed.")
