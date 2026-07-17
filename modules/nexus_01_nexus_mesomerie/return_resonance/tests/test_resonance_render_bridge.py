"""Integration tests for the Resonance Return Artifact render bridge."""

from __future__ import annotations

from dataclasses import replace
import json
from pathlib import Path
import sys
import tempfile

NEXUS_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(NEXUS_ROOT))

from resonance_language_library.render_resonance_output import default_library_dir
from return_resonance.matching import MatchStatus
from return_resonance.resonance_render_bridge import (
    ChamberSelections,
    ResonanceRenderBridgeError,
    build_resonance_return_artifact,
    load_resonance_return_artifact,
    open_resonance_return,
    parse_resonance_return_artifact,
)
from return_resonance.slots import ReturnSlot, ReturnSlotState
from return_resonance.token import (
    LAYER_ID,
    MODULE_ID,
    RESONANCE_CHAMBER,
    TOKEN_TYPE,
    TOKEN_VERSION,
    ResonanceToken,
)

LIBRARY_DIR = default_library_dir()

EXPECTED_RESONANCE_ARTIFACT = """A lantern waits in the dark.

Around it,
a path begins to appear.

The scent of a forest
after gentle summer rain
carries the possibility of encounter.

A feather turns as it falls.
Another feather crosses its path.

Courage was left here.
Trust answered."""

EXPECTED_ECHO = """Summer rain
opens one hidden path
two feathers cross beneath waiting light
the path carries courage
trust"""


def _token() -> ResonanceToken:
    return ResonanceToken(
        token_version=TOKEN_VERSION,
        token_type=TOKEN_TYPE,
        module_id=MODULE_ID,
        layer_id=LAYER_ID,
        origin_trace_id="trace-demo-001",
        return_slot_id="return-slot-demo-001",
        package_id="nexus-01-demo-package",
        enabled_chambers=(RESONANCE_CHAMBER,),
    )


def _selections() -> ChamberSelections:
    return ChamberSelections(
        image_id="waiting-lantern",
        image_response_id="appearing-path",
        scent_id="summer-rain",
        scent_response_id="possibility-of-encounter",
        movement_id="falling-feather",
        movement_response_id="crossing-feather",
        wish_word="courage",
        return_word="trust",
    )


def _slot(**changes: object) -> ReturnSlot:
    values: dict[str, object] = {
        "origin_trace_id": "trace-demo-001",
        "return_slot_id": "return-slot-demo-001",
        "module_id": MODULE_ID,
        "package_id": "nexus-01-demo-package",
        "layer_id": LAYER_ID,
        "status": ReturnSlotState.WAITING,
        "result_file": "resonance-result.txt",
    }
    values.update(changes)
    return ReturnSlot(**values)


def _assert_bridge_error(action: object, expected: str) -> None:
    try:
        action()
    except ResonanceRenderBridgeError as error:
        if expected not in str(error):
            raise AssertionError(f"Expected {expected!r} in error, got: {error}") from error
    else:
        raise AssertionError("Expected ResonanceRenderBridgeError")


def test_complete_bridge_roundtrip_and_opening() -> None:
    artifact = build_resonance_return_artifact(_token(), _selections())

    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / "resonance-return.json"
        path.write_text(artifact.to_json(), encoding="utf-8")
        loaded = load_resonance_return_artifact(path)

    assert loaded == artifact
    opened = open_resonance_return(loaded, [_slot()], LIBRARY_DIR)
    assert opened.match.status == MatchStatus.MATCH_WAITING
    assert opened.output.resonance_artifact.text == EXPECTED_RESONANCE_ARTIFACT
    assert opened.output.nexus_echo.text == EXPECTED_ECHO
    assert opened.output.nexus_echo.word_counts == (2, 4, 6, 4, 1)


def test_serialized_contract_is_lossless() -> None:
    artifact = build_resonance_return_artifact(_token(), _selections())
    decoded = json.loads(artifact.to_json())
    assert parse_resonance_return_artifact(decoded) == artifact
    assert decoded == artifact.to_dict()


def test_package_mismatch_is_rejected_before_rendering() -> None:
    artifact = build_resonance_return_artifact(_token(), _selections())
    _assert_bridge_error(
        lambda: open_resonance_return(
            replace(artifact, package_id="wrong-package"), [_slot()], LIBRARY_DIR
        ),
        "package_mismatch",
    )


def test_layer_mismatch_is_rejected_before_rendering() -> None:
    artifact = build_resonance_return_artifact(_token(), _selections())
    _assert_bridge_error(
        lambda: open_resonance_return(
            replace(artifact, layer_id="wrong-layer"), [_slot()], LIBRARY_DIR
        ),
        "layer_mismatch",
    )


def test_module_mismatch_is_rejected_before_rendering() -> None:
    artifact = build_resonance_return_artifact(_token(), _selections())
    _assert_bridge_error(
        lambda: open_resonance_return(artifact, [_slot(module_id="N99")], LIBRARY_DIR),
        "module_mismatch",
    )


def test_unsupported_contract_versions_are_rejected() -> None:
    artifact = build_resonance_return_artifact(_token(), _selections()).to_dict()

    wrong_artifact = dict(artifact)
    wrong_artifact["artifact_version"] = "9.0"
    _assert_bridge_error(
        lambda: parse_resonance_return_artifact(wrong_artifact),
        "Unsupported artifact_version",
    )

    wrong_library = dict(artifact)
    wrong_library["language_library"] = "resonance-en-v9"
    _assert_bridge_error(
        lambda: parse_resonance_return_artifact(wrong_library),
        "Unsupported language_library",
    )


def test_unknown_and_incompatible_selection_ids_are_rejected_after_matching() -> None:
    artifact = build_resonance_return_artifact(_token(), _selections())

    _assert_bridge_error(
        lambda: open_resonance_return(
            replace(artifact, image_id="unknown-image"), [_slot()], LIBRARY_DIR
        ),
        "Unknown image_id",
    )

    _assert_bridge_error(
        lambda: open_resonance_return(
            replace(artifact, image_response_id="shared-silence"), [_slot()], LIBRARY_DIR
        ),
        "not compatible",
    )


def test_artifact_without_approved_echo_path_is_rejected() -> None:
    artifact = build_resonance_return_artifact(_token(), _selections())
    _assert_bridge_error(
        lambda: open_resonance_return(
            replace(artifact, movement_response_id="waiting-hand"),
            [_slot()],
            LIBRARY_DIR,
        ),
        "No approved Nexus Echo path",
    )


def test_missing_and_unknown_fields_are_rejected() -> None:
    artifact = build_resonance_return_artifact(_token(), _selections()).to_dict()

    missing = dict(artifact)
    del missing["wish_word"]
    _assert_bridge_error(
        lambda: parse_resonance_return_artifact(missing),
        "missing required field",
    )

    unknown = dict(artifact)
    unknown["private_reason"] = "must not travel"
    _assert_bridge_error(
        lambda: parse_resonance_return_artifact(unknown),
        "unknown field",
    )


def test_untrusted_artifact_free_words_are_strictly_validated() -> None:
    valid = build_resonance_return_artifact(_token(), _selections()).to_dict()
    for field_name in ("wish_word", "return_word"):
        for invalid in ("two words", "x" * 81, "x\x00y", "x\x80y", "CHANGE-ME"):
            candidate = dict(valid)
            candidate[field_name] = invalid
            _assert_bridge_error(
                lambda candidate=candidate: parse_resonance_return_artifact(candidate),
                field_name,
            )

    unicode_words = dict(valid)
    unicode_words["wish_word"] = "Nähe"
    unicode_words["return_word"] = "帰還"
    parsed = parse_resonance_return_artifact(unicode_words)
    assert parsed.wish_word == "Nähe"
    assert parsed.return_word == "帰還"


if __name__ == "__main__":
    test_complete_bridge_roundtrip_and_opening()
    test_serialized_contract_is_lossless()
    test_package_mismatch_is_rejected_before_rendering()
    test_layer_mismatch_is_rejected_before_rendering()
    test_module_mismatch_is_rejected_before_rendering()
    test_unsupported_contract_versions_are_rejected()
    test_unknown_and_incompatible_selection_ids_are_rejected_after_matching()
    test_artifact_without_approved_echo_path_is_rejected()
    test_missing_and_unknown_fields_are_rejected()
    test_untrusted_artifact_free_words_are_strictly_validated()
    print("Resonance render bridge integration tests passed.")
