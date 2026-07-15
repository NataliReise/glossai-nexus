"""Tests for the local Nexus Echo renderer."""

from __future__ import annotations

import json
from pathlib import Path
import shutil
import sys
import tempfile

LIBRARY_ROOT = Path(__file__).resolve().parents[1]
NEXUS_ROOT = LIBRARY_ROOT.parent
sys.path.insert(0, str(NEXUS_ROOT))

from resonance_language_library.render_nexus_echo import (
    NexusEchoRenderError,
    render_nexus_echo,
)

LIBRARY_DIR = LIBRARY_ROOT / "v0_1"
FIXTURES = Path(__file__).resolve().parent / "fixtures" / "resonance_artifact_cases.json"


def _cases() -> list[dict[str, object]]:
    document = json.loads(FIXTURES.read_text(encoding="utf-8"))
    return document["cases"]


def _echo_document() -> dict[str, object]:
    return json.loads((LIBRARY_DIR / "echo_paths.json").read_text(encoding="utf-8"))


def _base_artifact() -> dict[str, object]:
    artifact = dict(_cases()[0]["artifact"])
    artifact["wish_word"] = "hope"
    artifact["return_word"] = "spirit"
    return artifact


def _assert_error_contains(
    artifact: dict[str, object],
    expected: str,
    library_dir: Path = LIBRARY_DIR,
) -> None:
    try:
        render_nexus_echo(artifact, library_dir)
    except NexusEchoRenderError as error:
        if expected not in str(error):
            raise AssertionError(f"Expected {expected!r} in error, got: {error}") from error
    else:
        raise AssertionError("Expected NexusEchoRenderError")


def test_all_reference_echoes_match_exactly() -> None:
    for case in _cases():
        artifact = case["artifact"]
        expected = case["expected_echo"]
        result = render_nexus_echo(artifact, LIBRARY_DIR)
        assert result.text == expected, case["id"]
        assert result.path_id == case["id"]
        assert result.word_counts == (2, 4, 6, 4, 1)


def test_tina_mixed_composition_uses_approved_components() -> None:
    artifact = _base_artifact()
    artifact.update(
        {
            "image_id": "open-starry-window",
            "image_response_id": "answering-distant-light",
            "scent_id": "summer-rain",
            "scent_response_id": "possibility-of-encounter",
            "movement_id": "returning-tide",
            "movement_response_id": "stream-back-to-sea",
        }
    )

    result = render_nexus_echo(artifact, LIBRARY_DIR)

    assert result.text == "\n".join(
        [
            "Evening window",
            "summer rain opens pathways",
            "tide and stream meet beneath stars",
            "the window gathers hope",
            "spirit",
        ]
    )
    assert result.path_id == (
        "mixed:image-starry-window+scent-summer-rain+movement-returning-tide"
    )
    assert result.word_counts == (2, 4, 6, 4, 1)


def test_all_125_chamber_family_combinations_render() -> None:
    document = _echo_document()
    components = document["components"]
    image_components = components["image"]
    scent_components = components["scent"]
    movement_components = components["movement"]

    rendered_ids: set[str] = set()
    for image in image_components:
        for scent in scent_components:
            for movement in movement_components:
                artifact = _base_artifact()
                artifact.update(image["requires"])
                artifact.update(scent["requires"])
                artifact.update(movement["requires"])
                result = render_nexus_echo(artifact, LIBRARY_DIR)
                assert result.word_counts == (2, 4, 6, 4, 1)
                rendered_ids.add(result.path_id)

    assert len(rendered_ids) == 125


def test_unknown_component_uses_no_improvisation_fallback() -> None:
    artifact = _base_artifact()
    artifact["movement_response_id"] = "waiting-hand"
    _assert_error_contains(artifact, "No approved Nexus Echo path or component composition")


def test_wrong_library_version_is_rejected() -> None:
    artifact = dict(_cases()[0]["artifact"])
    artifact["language_library"] = "resonance-en-v9"
    _assert_error_contains(artifact, "Unsupported language_library")


def test_multiword_slot_values_are_rejected() -> None:
    artifact = dict(_cases()[0]["artifact"])
    artifact["wish_word"] = "quiet courage"
    _assert_error_contains(artifact, "wish_word must be exactly one")


def test_unknown_placeholders_are_rejected() -> None:
    with tempfile.TemporaryDirectory() as directory:
        copy_dir = Path(directory) / "library"
        shutil.copytree(LIBRARY_DIR, copy_dir)
        path = copy_dir / "echo_paths.json"
        document = json.loads(path.read_text(encoding="utf-8"))
        document["paths"][0]["lines"][1] = "opens {unknown_slot} hidden path"
        path.write_text(json.dumps(document, indent=2), encoding="utf-8")
        _assert_error_contains(dict(_cases()[0]["artifact"]), "Unknown placeholder", copy_dir)


def test_runtime_word_count_is_enforced_for_exact_paths() -> None:
    with tempfile.TemporaryDirectory() as directory:
        copy_dir = Path(directory) / "library"
        shutil.copytree(LIBRARY_DIR, copy_dir)
        path = copy_dir / "echo_paths.json"
        document = json.loads(path.read_text(encoding="utf-8"))
        document["paths"][0]["lines"][1] = "opens one very hidden path"
        path.write_text(json.dumps(document, indent=2), encoding="utf-8")
        _assert_error_contains(dict(_cases()[0]["artifact"]), "expected 4 words", copy_dir)


def test_runtime_word_count_is_enforced_for_components() -> None:
    with tempfile.TemporaryDirectory() as directory:
        copy_dir = Path(directory) / "library"
        shutil.copytree(LIBRARY_DIR, copy_dir)
        path = copy_dir / "echo_paths.json"
        document = json.loads(path.read_text(encoding="utf-8"))
        document["components"]["scent"][0]["line_2"] = "summer rain opens many pathways"
        path.write_text(json.dumps(document, indent=2), encoding="utf-8")

        artifact = _base_artifact()
        artifact.update(
            {
                "image_id": "open-starry-window",
                "image_response_id": "answering-distant-light",
                "scent_id": "summer-rain",
                "scent_response_id": "possibility-of-encounter",
                "movement_id": "returning-tide",
                "movement_response_id": "stream-back-to-sea",
            }
        )
        _assert_error_contains(artifact, "expected 4 words", copy_dir)


def test_missing_echo_path_file_is_reported() -> None:
    with tempfile.TemporaryDirectory() as directory:
        empty_dir = Path(directory)
        _assert_error_contains(dict(_cases()[0]["artifact"]), "Missing library file", empty_dir)


if __name__ == "__main__":
    test_all_reference_echoes_match_exactly()
    test_tina_mixed_composition_uses_approved_components()
    test_all_125_chamber_family_combinations_render()
    test_unknown_component_uses_no_improvisation_fallback()
    test_wrong_library_version_is_rejected()
    test_multiword_slot_values_are_rejected()
    test_unknown_placeholders_are_rejected()
    test_runtime_word_count_is_enforced_for_exact_paths()
    test_runtime_word_count_is_enforced_for_components()
    test_missing_echo_path_file_is_reported()
    print("Nexus Echo renderer tests passed.")
