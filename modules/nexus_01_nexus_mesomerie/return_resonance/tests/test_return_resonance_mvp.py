"""MVP tests for the Nexus 01 Return Resonance extension layer."""

from __future__ import annotations

from pathlib import Path
import sys
import tempfile

NEXUS_01_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(NEXUS_01_ROOT))

from return_resonance import MatchStatus, load_return_slots, match_return_artifact, parse_return_artifact
from return_resonance.artifact import ReturnArtifactParseError
from return_resonance.slots import ReturnSlotState


EXAMPLES_DIR = NEXUS_01_ROOT / "examples"
DEMO_ARTIFACT_PATH = EXAMPLES_DIR / "return_artifact.demo.txt"
DEMO_SLOT_PATH = EXAMPLES_DIR / "return_slot.demo.json"


def assert_contains(text: str, expected: str) -> None:
    if expected not in text:
        raise AssertionError(f"Expected to find {expected!r} in text:\n{text}")


def test_parse_demo_return_artifact() -> None:
    artifact = parse_return_artifact(DEMO_ARTIFACT_PATH.read_text(encoding="utf-8"))

    assert artifact.version == "N01-RA-GEN-1"
    assert artifact.module == "Nexus 01 - First Spark"
    assert artifact.origin_trace_id == "n01-demo-origin-7kq2"
    assert artifact.return_slot_id == "lantern-river-01"
    assert artifact.package_id == "demo-package"
    assert artifact.layer_id == "return-resonance-1"
    assert artifact.carrier_image == "lantern"
    assert artifact.carrier_movement == "across the river"
    assert artifact.return_word == "trust"
    assert artifact.return_image == "window"
    assert artifact.return_tone == "luminous"


def test_parse_return_artifact_requires_core_fields() -> None:
    text = """NEXUS RETURN ARTIFACT
Version: N01-RA-GEN-1
Module: Nexus 01 - First Spark
"""

    try:
        parse_return_artifact(text)
    except ReturnArtifactParseError as error:
        message = str(error)
        assert_contains(message, "origin_trace_id")
        assert_contains(message, "return_slot_id")
        assert_contains(message, "package_id")
        assert_contains(message, "layer_id")
    else:
        raise AssertionError("Expected ReturnArtifactParseError for incomplete artifact.")


def test_load_demo_return_slot() -> None:
    slots = load_return_slots(DEMO_SLOT_PATH)

    assert len(slots) == 1
    slot = slots[0]
    assert slot.origin_trace_id == "n01-demo-origin-7kq2"
    assert slot.return_slot_id == "lantern-river-01"
    assert slot.module_id == "N01"
    assert slot.package_id == "demo-package"
    assert slot.layer_id == "return-resonance-1"
    assert slot.status == ReturnSlotState.WAITING
    assert slot.result_file == "return_resonance_lantern_river.local.md"


def test_match_demo_artifact_to_waiting_slot() -> None:
    artifact = parse_return_artifact(DEMO_ARTIFACT_PATH.read_text(encoding="utf-8"))
    slots = load_return_slots(DEMO_SLOT_PATH)

    result = match_return_artifact(artifact, slots)

    assert result.status == MatchStatus.MATCH_WAITING
    assert result.is_match
    assert result.slot is not None
    assert result.slot.return_slot_id == "lantern-river-01"
    assert_contains(result.message, "returned artifact fits")


def test_match_unknown_slot() -> None:
    artifact_text = DEMO_ARTIFACT_PATH.read_text(encoding="utf-8").replace(
        "Return Slot: lantern-river-01", "Return Slot: unknown-slot"
    )
    artifact = parse_return_artifact(artifact_text)
    slots = load_return_slots(DEMO_SLOT_PATH)

    result = match_return_artifact(artifact, slots)

    assert result.status == MatchStatus.UNKNOWN_SLOT
    assert not result.is_match
    assert result.slot is None
    assert_contains(result.message, "does not seem to belong")


def test_match_package_mismatch() -> None:
    artifact_text = DEMO_ARTIFACT_PATH.read_text(encoding="utf-8").replace(
        "Package: demo-package", "Package: other-package"
    )
    artifact = parse_return_artifact(artifact_text)
    slots = load_return_slots(DEMO_SLOT_PATH)

    result = match_return_artifact(artifact, slots)

    assert result.status == MatchStatus.PACKAGE_MISMATCH
    assert not result.is_match
    assert result.slot is not None
    assert_contains(result.message, "package")


def test_match_layer_mismatch() -> None:
    artifact_text = DEMO_ARTIFACT_PATH.read_text(encoding="utf-8").replace(
        "Layer: return-resonance-1", "Layer: other-layer"
    )
    artifact = parse_return_artifact(artifact_text)
    slots = load_return_slots(DEMO_SLOT_PATH)

    result = match_return_artifact(artifact, slots)

    assert result.status == MatchStatus.LAYER_MISMATCH
    assert not result.is_match
    assert result.slot is not None
    assert_contains(result.message, "layer")


def test_match_already_opened_slot() -> None:
    with tempfile.TemporaryDirectory() as directory:
        opened_slot_path = Path(directory) / "return_slot.demo.json"
        opened_slot_path.write_text(
            DEMO_SLOT_PATH.read_text(encoding="utf-8").replace(
                '"status": "waiting"', '"status": "opened"'
            ),
            encoding="utf-8",
        )

        artifact = parse_return_artifact(DEMO_ARTIFACT_PATH.read_text(encoding="utf-8"))
        slots = load_return_slots(opened_slot_path)

    result = match_return_artifact(artifact, slots)

    assert result.status == MatchStatus.MATCH_OPENED
    assert result.is_match
    assert result.slot is not None
    assert_contains(result.message, "already opened")


def test_first_spark_is_not_imported_by_return_resonance() -> None:
    imported_names = set(sys.modules)
    forbidden_imports = {
        name for name in imported_names if name == "first_spark" or name.startswith("first_spark.")
    }

    if forbidden_imports:
        raise AssertionError(
            "Return Resonance tests imported First Spark unexpectedly: "
            + ", ".join(sorted(forbidden_imports))
        )


if __name__ == "__main__":
    test_parse_demo_return_artifact()
    test_parse_return_artifact_requires_core_fields()
    test_load_demo_return_slot()
    test_match_demo_artifact_to_waiting_slot()
    test_match_unknown_slot()
    test_match_package_mismatch()
    test_match_layer_mismatch()
    test_match_already_opened_slot()
    test_first_spark_is_not_imported_by_return_resonance()
    print("Return Resonance MVP tests passed.")
