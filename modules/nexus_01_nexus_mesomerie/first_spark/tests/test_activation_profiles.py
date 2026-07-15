"""Tests for backward-compatible Nexus 01 activation profile loading."""

from __future__ import annotations

import json
from pathlib import Path
import sys
import tempfile


FIRST_SPARK_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(FIRST_SPARK_ROOT))

from first_spark.activation import (
    ActivationFileError,
    FIRST_SPARK_PROFILE_ID,
    RETURN_RESONANCE_PROFILE_ID,
    activation_from_mapping,
    default_activation,
    load_activation,
)


def assert_contains(text: str, expected: str) -> None:
    if expected not in text:
        raise AssertionError(f"Expected to find {expected!r} in:\n{text}")


def test_default_activation_uses_first_spark_profile() -> None:
    activation = default_activation()
    assert activation.profile_id == FIRST_SPARK_PROFILE_ID


def test_legacy_activation_normalizes_to_first_spark() -> None:
    activation = activation_from_mapping(
        {
            "recipient_alias": "legacy-recipient",
            "activation_purpose": "gift",
            "private_message": "Legacy message",
        }
    )

    assert activation.profile_id == FIRST_SPARK_PROFILE_ID
    assert activation.recipient_alias == "legacy-recipient"
    assert activation.private_message == "Legacy message"


def test_explicit_first_spark_profile_is_preserved() -> None:
    activation = activation_from_mapping(
        {
            "profile_id": FIRST_SPARK_PROFILE_ID,
            "recipient_alias": "spark-recipient",
        }
    )

    assert activation.profile_id == FIRST_SPARK_PROFILE_ID
    assert activation.recipient_alias == "spark-recipient"


def test_return_resonance_profile_is_preserved() -> None:
    activation = activation_from_mapping(
        {
            "profile_id": RETURN_RESONANCE_PROFILE_ID,
            "recipient_alias": "resonance-recipient",
        }
    )

    assert activation.profile_id == RETURN_RESONANCE_PROFILE_ID
    assert activation.recipient_alias == "resonance-recipient"


def test_unknown_profile_is_rejected() -> None:
    try:
        activation_from_mapping({"profile_id": "neutral-demo"})
    except ActivationFileError as error:
        message = str(error)
        assert_contains(message, "Unknown activation profile")
        assert_contains(message, FIRST_SPARK_PROFILE_ID)
        assert_contains(message, RETURN_RESONANCE_PROFILE_ID)
    else:
        raise AssertionError("Expected ActivationFileError for unknown profile.")


def test_file_loader_preserves_legacy_and_explicit_profiles() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)

        legacy_path = root / "legacy.json"
        legacy_path.write_text(
            json.dumps({"recipient_alias": "legacy-file"}), encoding="utf-8"
        )
        assert load_activation(legacy_path).profile_id == FIRST_SPARK_PROFILE_ID

        resonance_path = root / "resonance.json"
        resonance_path.write_text(
            json.dumps(
                {
                    "profile_id": RETURN_RESONANCE_PROFILE_ID,
                    "recipient_alias": "resonance-file",
                }
            ),
            encoding="utf-8",
        )
        assert (
            load_activation(resonance_path).profile_id
            == RETURN_RESONANCE_PROFILE_ID
        )


def test_file_loader_wraps_unknown_profile_with_path_context() -> None:
    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / "activation.local.json"
        path.write_text(json.dumps({"profile_id": "unknown"}), encoding="utf-8")

        try:
            load_activation(path)
        except ActivationFileError as error:
            message = str(error)
            assert_contains(message, "Activation file could not be loaded.")
            assert_contains(message, str(path))
            assert_contains(message, "Unknown activation profile")
        else:
            raise AssertionError("Expected ActivationFileError for unknown profile file.")


if __name__ == "__main__":
    test_default_activation_uses_first_spark_profile()
    test_legacy_activation_normalizes_to_first_spark()
    test_explicit_first_spark_profile_is_preserved()
    test_return_resonance_profile_is_preserved()
    test_unknown_profile_is_rejected()
    test_file_loader_preserves_legacy_and_explicit_profiles()
    test_file_loader_wraps_unknown_profile_with_path_context()
    print("First Spark activation profile tests passed.")
