"""Tests for the Nexus 01 resonance token boundary."""

from __future__ import annotations

import json
from pathlib import Path
import sys
import tempfile

NEXUS_01_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(NEXUS_01_ROOT))

from return_resonance import (
    MatchStatus,
    ReturnArtifact,
    ResonanceTokenLoadError,
    load_resonance_token,
    load_return_slots,
    match_return_artifact,
    parse_resonance_token,
)


def valid_token_data() -> dict[str, object]:
    return {
        "token_version": "N01-RT-1",
        "token_type": "resonance-activation",
        "module_id": "N01",
        "layer_id": "return-resonance-1",
        "origin_trace_id": "n01-local-origin-a4m9",
        "return_slot_id": "quiet-garden-01",
        "package_id": "local-package-garden-01",
        "enabled_chambers": ["resonance"],
        "public_safe_label": "quiet garden",
        "note": "This token identifies a resonance arc, not a person.",
    }


def assert_error_contains(data: object, expected: str) -> None:
    try:
        parse_resonance_token(data)
    except ResonanceTokenLoadError as error:
        if expected not in str(error):
            raise AssertionError(
                f"Expected {expected!r} in token error, got: {error}"
            ) from error
    else:
        raise AssertionError("Expected ResonanceTokenLoadError.")


def test_parse_valid_resonance_token() -> None:
    token = parse_resonance_token(valid_token_data())

    assert token.token_version == "N01-RT-1"
    assert token.token_type == "resonance-activation"
    assert token.module_id == "N01"
    assert token.layer_id == "return-resonance-1"
    assert token.origin_trace_id == "n01-local-origin-a4m9"
    assert token.return_slot_id == "quiet-garden-01"
    assert token.package_id == "local-package-garden-01"
    assert token.enabled_chambers == ("resonance",)
    assert token.enables_resonance
    assert token.public_safe_label == "quiet garden"


def test_load_resonance_token_from_file() -> None:
    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / "resonance_token.local.json"
        path.write_text(json.dumps(valid_token_data()), encoding="utf-8")

        token = load_resonance_token(path)

    assert token.return_slot_id == "quiet-garden-01"
    assert token.enables_resonance


def test_resonance_token_requires_json_object() -> None:
    assert_error_contains([], "JSON object")


def test_resonance_token_requires_core_fields() -> None:
    data = valid_token_data()
    del data["origin_trace_id"]
    del data["enabled_chambers"]

    assert_error_contains(data, "origin_trace_id")
    assert_error_contains(data, "enabled_chambers")


def test_resonance_token_rejects_wrong_version() -> None:
    data = valid_token_data()
    data["token_version"] = "N01-RT-99"

    assert_error_contains(data, "token_version")


def test_resonance_token_rejects_wrong_type() -> None:
    data = valid_token_data()
    data["token_type"] = "gift-activation"

    assert_error_contains(data, "token_type")


def test_resonance_token_rejects_wrong_module() -> None:
    data = valid_token_data()
    data["module_id"] = "N02"

    assert_error_contains(data, "module_id")


def test_resonance_token_rejects_wrong_layer() -> None:
    data = valid_token_data()
    data["layer_id"] = "other-layer"

    assert_error_contains(data, "layer_id")


def test_resonance_token_must_enable_resonance_chamber() -> None:
    data = valid_token_data()
    data["enabled_chambers"] = ["spark"]

    assert_error_contains(data, "'resonance' Chamber")


def test_resonance_token_rejects_duplicate_chambers() -> None:
    data = valid_token_data()
    data["enabled_chambers"] = ["resonance", "resonance"]

    assert_error_contains(data, "duplicates")


def test_resonance_token_fields_match_existing_slot_mechanism() -> None:
    token = parse_resonance_token(valid_token_data())

    artifact = ReturnArtifact(
        version="N01-RA-GEN-1",
        module="Nexus 01 - First Spark",
        origin_trace_id=token.origin_trace_id,
        return_slot_id=token.return_slot_id,
        package_id=token.package_id,
        layer_id=token.layer_id,
        carrier_image="garden",
        carrier_movement="through the quiet gate",
        return_word="patience",
        return_image="soft moss",
        return_tone="gentle",
    )

    slot_document = {
        "slots": [
            {
                "origin_trace_id": token.origin_trace_id,
                "return_slot_id": token.return_slot_id,
                "module_id": token.module_id,
                "package_id": token.package_id,
                "layer_id": token.layer_id,
                "status": "waiting",
                "result_file": "return_resonance_quiet_garden.local.md",
                "public_safe_label": token.public_safe_label,
            }
        ]
    }

    with tempfile.TemporaryDirectory() as directory:
        slot_path = Path(directory) / "return_slots.local.json"
        slot_path.write_text(json.dumps(slot_document), encoding="utf-8")
        slots = load_return_slots(slot_path)

    result = match_return_artifact(artifact, slots)

    assert result.status == MatchStatus.MATCH_WAITING
    assert result.is_match
    assert result.slot is not None
    assert result.slot.return_slot_id == token.return_slot_id


if __name__ == "__main__":
    test_parse_valid_resonance_token()
    test_load_resonance_token_from_file()
    test_resonance_token_requires_json_object()
    test_resonance_token_requires_core_fields()
    test_resonance_token_rejects_wrong_version()
    test_resonance_token_rejects_wrong_type()
    test_resonance_token_rejects_wrong_module()
    test_resonance_token_rejects_wrong_layer()
    test_resonance_token_must_enable_resonance_chamber()
    test_resonance_token_rejects_duplicate_chambers()
    test_resonance_token_fields_match_existing_slot_mechanism()
    print("Resonance token tests passed.")
