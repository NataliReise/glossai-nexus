"""Focused tests for the strict, inert Resonance Token V2 boundary."""

from __future__ import annotations

from dataclasses import FrozenInstanceError
import json
from pathlib import Path
import sys
import tempfile


NEXUS_ROOT = Path(__file__).resolve().parents[2]
if str(NEXUS_ROOT) not in sys.path:
    sys.path.insert(0, str(NEXUS_ROOT))

from return_resonance.token import (  # noqa: E402
    TOKEN_VERSION_V1,
    TOKEN_VERSION_V2,
    ResonanceTokenLoadError,
    load_resonance_token,
    parse_resonance_token,
)


def valid_v2_data() -> dict[str, object]:
    return {
        "token_version": TOKEN_VERSION_V2,
        "token_type": "resonance-activation",
        "module_id": "N01",
        "layer_id": "return-resonance-1",
        "origin_trace_id": "n01-origin-0123456789abcdef",
        "return_slot_id": "n01-slot-0123456789abcdef",
        "package_id": "n01-package-0123456789abcdef",
        "language_library": "resonance-en-v0.1",
        "enabled_chambers": ["resonance"],
        "image_id": "waiting-lantern",
        "scent_id": "summer-rain",
        "movement_id": "falling-feather",
        "wish_word": "Nähe",
        "public_safe_label": "quiet invitation",
    }


def legacy_v1_data() -> dict[str, object]:
    value = valid_v2_data()
    value["token_version"] = TOKEN_VERSION_V1
    for field_name in (
        "language_library", "image_id", "scent_id", "movement_id", "wish_word"
    ):
        del value[field_name]
    return value


def assert_rejected(data: object, expected: str) -> None:
    try:
        parse_resonance_token(data)
    except ResonanceTokenLoadError as error:
        assert expected in str(error), str(error)
    else:
        raise AssertionError("Expected ResonanceTokenLoadError")


def test_valid_v2_contains_originating_contribution_only() -> None:
    token = parse_resonance_token(valid_v2_data())

    assert token.token_version == TOKEN_VERSION_V2
    assert not token.is_legacy
    assert token.has_originating_contribution
    assert token.language_library == "resonance-en-v0.1"
    assert token.image_id == "waiting-lantern"
    assert token.scent_id == "summer-rain"
    assert token.movement_id == "falling-feather"
    assert token.wish_word == "Nähe"
    assert set(token.to_dict()).isdisjoint(
        {"image_response_id", "scent_response_id", "movement_response_id", "return_word"}
    )


def test_every_v2_required_field_is_enforced() -> None:
    optional = {"public_safe_label"}
    for field_name in valid_v2_data().keys() - optional:
        value = valid_v2_data()
        del value[field_name]
        assert_rejected(value, field_name)


def test_v2_rejects_answer_side_and_other_unknown_fields() -> None:
    for field_name in (
        "image_response_id", "scent_response_id", "movement_response_id", "return_word"
    ):
        value = valid_v2_data()
        value[field_name] = "must-not-travel"
        assert_rejected(value, "answer-side")

    value = valid_v2_data()
    value["recipient_alias"] = "must-not-travel"
    assert_rejected(value, "unknown field")

    value = valid_v2_data()
    value["note"] = "V1 metadata does not belong in the minimal V2 shape."
    assert_rejected(value, "unknown field")

    value = valid_v2_data()
    value["enabled_chambers"] = ["resonance", "future-chamber"]
    assert_rejected(value, "only 'resonance'")


def test_v2_rejects_invalid_source_ids() -> None:
    for field_name in ("image_id", "scent_id", "movement_id"):
        value = valid_v2_data()
        value[field_name] = "unsupported-source"
        assert_rejected(value, field_name)


def test_v2_preserves_unicode_wish_word_and_rejects_non_words() -> None:
    for word in ("Nähe", "帰還", "écho"):
        value = valid_v2_data()
        value["wish_word"] = word
        assert parse_resonance_token(value).wish_word == word

    for word in ("", "two words", "line\nbreak", "line\tbreak"):
        value = valid_v2_data()
        value["wish_word"] = word
        assert_rejected(value, "wish_word")


def test_v2_validates_route_identity_and_template_sentinels() -> None:
    invalid_routes = {
        "origin_trace_id": "person name",
        "return_slot_id": "../slot",
        "package_id": "unsafe/package",
    }
    for field_name, invalid in invalid_routes.items():
        value = valid_v2_data()
        value[field_name] = invalid
        assert_rejected(value, field_name)

    for field_name in (
        "origin_trace_id", "return_slot_id", "package_id", "wish_word",
        "public_safe_label",
    ):
        value = valid_v2_data()
        value[field_name] = "CHANGE-ME"
        assert_rejected(value, "template sentinel")


def test_v2_json_round_trip_and_immutability() -> None:
    token = parse_resonance_token(valid_v2_data())
    encoded = token.to_json()
    decoded = json.loads(encoded)
    assert parse_resonance_token(decoded) == token
    assert "Nähe" in encoded

    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / "resonance-token.json"
        path.write_text(encoded, encoding="utf-8")
        before = path.read_bytes()
        loaded = load_resonance_token(path)
        after = path.read_bytes()
    assert loaded == token
    assert after == before

    try:
        token.wish_word = "changed"  # type: ignore[misc]
    except FrozenInstanceError:
        pass
    else:
        raise AssertionError("ResonanceToken must remain immutable")


def test_v1_remains_readable_as_legacy_without_originating_fields() -> None:
    token = parse_resonance_token(legacy_v1_data())

    assert token.is_legacy
    assert not token.has_originating_contribution
    assert token.language_library == ""
    assert token.image_id == ""
    assert token.scent_id == ""
    assert token.movement_id == ""
    assert token.wish_word == ""
    assert parse_resonance_token(json.loads(token.to_json())) == token
