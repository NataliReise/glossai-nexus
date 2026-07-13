"""Tests for the local Resonance Artifact renderer."""

from __future__ import annotations

import json
from pathlib import Path
import sys
import tempfile

LIBRARY_ROOT = Path(__file__).resolve().parents[1]
NEXUS_01_ROOT = LIBRARY_ROOT.parent
sys.path.insert(0, str(LIBRARY_ROOT))

from render_resonance_artifact import (  # noqa: E402
    ResonanceArtifactRenderError,
    default_library_dir,
    render_resonance_artifact,
)

FIXTURE_PATH = Path(__file__).resolve().parent / "fixtures" / "resonance_artifact_cases.json"


def _fixture_cases() -> list[dict[str, object]]:
    document = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    return document["cases"]


def _assert_error_contains(artifact: dict[str, object], expected: str) -> None:
    try:
        render_resonance_artifact(artifact, default_library_dir())
    except ResonanceArtifactRenderError as error:
        if expected not in str(error):
            raise AssertionError(
                f"Expected {expected!r} in render error, got: {error}"
            ) from error
    else:
        raise AssertionError("Expected ResonanceArtifactRenderError")


def test_all_reference_cases_render_exactly() -> None:
    cases = _fixture_cases()
    assert len(cases) == 5
    for case in cases:
        rendered = render_resonance_artifact(case["artifact"], default_library_dir())
        assert rendered.text == case["expected"], case["id"]
        assert rendered.library_version == "resonance-en-v0.1"


def test_unknown_id_is_rejected() -> None:
    artifact = dict(_fixture_cases()[0]["artifact"])
    artifact["image_id"] = "unknown-image"
    _assert_error_contains(artifact, "Unknown image_id")


def test_incompatible_image_response_is_rejected() -> None:
    artifact = dict(_fixture_cases()[0]["artifact"])
    artifact["image_response_id"] = "shared-silence"
    _assert_error_contains(artifact, "not compatible")


def test_incompatible_scent_response_is_rejected() -> None:
    artifact = dict(_fixture_cases()[0]["artifact"])
    artifact["scent_response_id"] = "second-place-at-table"
    _assert_error_contains(artifact, "not compatible")


def test_wrong_library_version_is_rejected() -> None:
    artifact = dict(_fixture_cases()[0]["artifact"])
    artifact["language_library"] = "resonance-en-v9.9"
    _assert_error_contains(artifact, "Unsupported language_library")


def test_words_must_remain_single_tokens() -> None:
    artifact = dict(_fixture_cases()[0]["artifact"])
    artifact["return_word"] = "quiet trust"
    _assert_error_contains(artifact, "exactly one non-empty word")


def test_missing_library_file_fails_calmly() -> None:
    artifact = dict(_fixture_cases()[0]["artifact"])
    with tempfile.TemporaryDirectory() as directory:
        try:
            render_resonance_artifact(artifact, Path(directory))
        except ResonanceArtifactRenderError as error:
            assert "Missing library file" in str(error)
        else:
            raise AssertionError("Expected ResonanceArtifactRenderError")


if __name__ == "__main__":
    test_all_reference_cases_render_exactly()
    test_unknown_id_is_rejected()
    test_incompatible_image_response_is_rejected()
    test_incompatible_scent_response_is_rejected()
    test_wrong_library_version_is_rejected()
    test_words_must_remain_single_tokens()
    test_missing_library_file_fails_calmly()
    print("Resonance Artifact renderer tests passed.")
