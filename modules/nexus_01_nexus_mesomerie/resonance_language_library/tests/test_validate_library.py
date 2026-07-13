"""Tests for the local Resonance Language Library validator."""

from __future__ import annotations

import json
from pathlib import Path
import shutil
import sys
import tempfile

LIBRARY_ROOT = Path(__file__).resolve().parents[1]
NEXUS_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(LIBRARY_ROOT))

from validate_library import EXPECTED_ECHO_PATTERN, _word_count, validate_library

SOURCE_LIBRARY = LIBRARY_ROOT / "v0_1"


def _copy_library() -> tuple[tempfile.TemporaryDirectory[str], Path]:
    temporary = tempfile.TemporaryDirectory()
    target = Path(temporary.name) / "v0_1"
    shutil.copytree(SOURCE_LIBRARY, target)
    return temporary, target


def _read_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, document: dict[str, object]) -> None:
    path.write_text(json.dumps(document, indent=2) + "\n", encoding="utf-8")


def _messages(issues: list[object]) -> str:
    return "\n".join(str(issue) for issue in issues)


def test_current_library_is_valid() -> None:
    issues = validate_library(SOURCE_LIBRARY)
    assert not issues, _messages(issues)


def test_word_count_treats_slots_as_one_word() -> None:
    lines = [
        "Summer rain",
        "opens one hidden path",
        "two feathers cross beneath waiting light",
        "the path carries {wish_word}",
        "{return_word}",
    ]
    assert tuple(_word_count(line) for line in lines) == EXPECTED_ECHO_PATTERN


def test_validator_reports_unknown_echo_reference() -> None:
    temporary, library = _copy_library()
    try:
        path = library / "echo_paths.json"
        document = _read_json(path)
        document["paths"][0]["requires"]["image_id"] = "missing-image"
        _write_json(path, document)

        issues = validate_library(library)
        assert "unknown referenced id 'missing-image'" in _messages(issues)
    finally:
        temporary.cleanup()


def test_validator_reports_wrong_echo_word_count() -> None:
    temporary, library = _copy_library()
    try:
        path = library / "echo_paths.json"
        document = _read_json(path)
        document["paths"][0]["lines"][1] = "opens a hidden path today"
        _write_json(path, document)

        issues = validate_library(library)
        messages = _messages(issues)
        assert "expected 4 words, found 5" in messages
    finally:
        temporary.cleanup()


def test_validator_reports_broken_echo_motif() -> None:
    temporary, library = _copy_library()
    try:
        path = library / "echo_paths.json"
        document = _read_json(path)
        document["paths"][0]["echo_motif"] = "lantern"
        _write_json(path, document)

        issues = validate_library(library)
        messages = _messages(issues)
        assert "does not appear in line 1 or 2" in messages
        assert "does not reappear in line 4" in messages
    finally:
        temporary.cleanup()


def test_validator_reports_invalid_scene_compatibility() -> None:
    temporary, library = _copy_library()
    try:
        path = library / "scent_responses.json"
        document = _read_json(path)
        document["scene_compatible"][0]["compatible_scent_ids"].append("missing-scent")
        _write_json(path, document)

        issues = validate_library(library)
        assert "unknown scent id 'missing-scent'" in _messages(issues)
    finally:
        temporary.cleanup()


def test_validator_reports_library_version_mismatch() -> None:
    temporary, library = _copy_library()
    try:
        path = library / "images.json"
        document = _read_json(path)
        document["library_version"] = "resonance-en-v9.9"
        _write_json(path, document)

        issues = validate_library(library)
        assert "library_version must be 'resonance-en-v0.1'" in _messages(issues)
    finally:
        temporary.cleanup()


if __name__ == "__main__":
    test_current_library_is_valid()
    test_word_count_treats_slots_as_one_word()
    test_validator_reports_unknown_echo_reference()
    test_validator_reports_wrong_echo_word_count()
    test_validator_reports_broken_echo_motif()
    test_validator_reports_invalid_scene_compatibility()
    test_validator_reports_library_version_mismatch()
    print("Resonance language library validator tests passed.")
