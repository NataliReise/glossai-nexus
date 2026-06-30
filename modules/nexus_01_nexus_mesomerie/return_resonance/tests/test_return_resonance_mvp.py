"""MVP tests for the Nexus 01 Return Resonance extension layer."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys
import tempfile

NEXUS_01_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(NEXUS_01_ROOT))

BEFORE_RETURN_RESONANCE_IMPORTS = set(sys.modules)

from return_resonance import (
    MatchStatus,
    ReturnResultError,
    load_return_slots,
    match_return_artifact,
    open_return_result,
    parse_return_artifact,
)
from return_resonance.artifact import ReturnArtifactParseError
from return_resonance.slots import ReturnSlotLoadError, ReturnSlotState

AFTER_RETURN_RESONANCE_IMPORTS = set(sys.modules)


EXAMPLES_DIR = NEXUS_01_ROOT / "examples"
DEMO_ARTIFACT_PATH = EXAMPLES_DIR / "return_artifact.demo.txt"
UNKNOWN_SLOT_ARTIFACT_PATH = EXAMPLES_DIR / "return_artifact.unknown_slot.demo.txt"
QUIET_GARDEN_ARTIFACT_PATH = EXAMPLES_DIR / "return_artifact.quiet_garden.demo.txt"
DEMO_SLOT_PATH = EXAMPLES_DIR / "return_slot.demo.json"
DEMO_RUNNER_PATH = NEXUS_01_ROOT / "run_return_resonance_demo.py"
CLI_RUNNER_PATH = NEXUS_01_ROOT / "run_return_resonance.py"
SLOT_GENERATOR_PATH = NEXUS_01_ROOT / "make_return_slot.py"


def assert_contains(text: str, expected: str) -> None:
    if expected not in text:
        raise AssertionError(f"Expected to find {expected!r} in text:\n{text}")


def load_demo_match():
    artifact = parse_return_artifact(DEMO_ARTIFACT_PATH.read_text(encoding="utf-8"))
    slots = load_return_slots(DEMO_SLOT_PATH)
    return artifact, match_return_artifact(artifact, slots)


def load_module(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_demo_runner_module():
    return load_module(DEMO_RUNNER_PATH, "run_return_resonance_demo")


def load_cli_runner_module():
    return load_module(CLI_RUNNER_PATH, "run_return_resonance")


def load_slot_generator_module():
    return load_module(SLOT_GENERATOR_PATH, "make_return_slot")


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


def test_parse_unknown_slot_return_artifact() -> None:
    artifact = parse_return_artifact(UNKNOWN_SLOT_ARTIFACT_PATH.read_text(encoding="utf-8"))

    assert artifact.version == "N01-RA-GEN-1"
    assert artifact.origin_trace_id == "n01-demo-origin-7kq2"
    assert artifact.return_slot_id == "unknown-slot"
    assert artifact.package_id == "demo-package"
    assert artifact.layer_id == "return-resonance-1"
    assert artifact.return_word == "trust"


def test_parse_quiet_garden_return_artifact() -> None:
    artifact = parse_return_artifact(QUIET_GARDEN_ARTIFACT_PATH.read_text(encoding="utf-8"))

    assert artifact.version == "N01-RA-GEN-1"
    assert artifact.origin_trace_id == "n01-local-origin-a4m9"
    assert artifact.return_slot_id == "quiet-garden-01"
    assert artifact.package_id == "local-package-garden-01"
    assert artifact.layer_id == "return-resonance-1"
    assert artifact.return_word == "patience"


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


def test_parse_return_artifact_allows_missing_optional_return_word() -> None:
    text = """NEXUS RETURN ARTIFACT
Version: N01-RA-GEN-1
Module: Nexus 01 - First Spark
Origin Trace: n01-demo-origin-7kq2
Return Slot: lantern-river-01
Package: demo-package
Layer: return-resonance-1
"""

    artifact = parse_return_artifact(text)

    assert artifact.return_word == ""
    assert artifact.return_image == ""
    assert artifact.return_tone == ""


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


def test_load_return_slot_requires_slots_list() -> None:
    with tempfile.TemporaryDirectory() as directory:
        slot_path = Path(directory) / "return_slots.local.json"
        slot_path.write_text('{"document_status": "missing slots"}\n', encoding="utf-8")

        try:
            load_return_slots(slot_path)
        except ReturnSlotLoadError as error:
            assert_contains(str(error), "slots list")
        else:
            raise AssertionError("Expected ReturnSlotLoadError for missing slots list.")


def test_load_return_slot_requires_core_fields() -> None:
    with tempfile.TemporaryDirectory() as directory:
        slot_path = Path(directory) / "return_slots.local.json"
        slot_path.write_text(
            json.dumps(
                {
                    "slots": [
                        {
                            "origin_trace_id": "n01-demo-origin-7kq2",
                            "return_slot_id": "lantern-river-01",
                            "module_id": "N01",
                            "package_id": "demo-package",
                            "status": "waiting",
                            "result_file": "return_resonance_lantern_river.local.md",
                        }
                    ]
                }
            ),
            encoding="utf-8",
        )

        try:
            load_return_slots(slot_path)
        except ReturnSlotLoadError as error:
            assert_contains(str(error), "layer_id")
        else:
            raise AssertionError("Expected ReturnSlotLoadError for incomplete slot.")


def test_load_return_slot_rejects_unknown_status() -> None:
    with tempfile.TemporaryDirectory() as directory:
        slot_path = Path(directory) / "return_slots.local.json"
        slot_data = json.loads(DEMO_SLOT_PATH.read_text(encoding="utf-8"))
        slot_data["slots"][0]["status"] = "half-open"
        slot_path.write_text(json.dumps(slot_data), encoding="utf-8")

        try:
            load_return_slots(slot_path)
        except ReturnSlotLoadError as error:
            assert_contains(str(error), "unsupported status")
            assert_contains(str(error), "half-open")
        else:
            raise AssertionError("Expected ReturnSlotLoadError for unsupported slot status.")


def test_match_demo_artifact_to_waiting_slot() -> None:
    artifact, result = load_demo_match()

    assert artifact.return_slot_id == "lantern-river-01"
    assert result.status == MatchStatus.MATCH_WAITING
    assert result.is_match
    assert result.slot is not None
    assert result.slot.return_slot_id == "lantern-river-01"
    assert_contains(result.message, "returned artifact fits")


def test_match_unknown_slot() -> None:
    artifact = parse_return_artifact(UNKNOWN_SLOT_ARTIFACT_PATH.read_text(encoding="utf-8"))
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


def test_open_return_result_generates_once_then_reuses() -> None:
    artifact, match = load_demo_match()

    with tempfile.TemporaryDirectory() as directory:
        first_result = open_return_result(artifact, match, directory)

        assert first_result.created
        assert first_result.path.name == "return_resonance_lantern_river.local.md"
        assert first_result.path.exists()
        assert first_result.path.read_text(encoding="utf-8") == first_result.content
        assert_contains(first_result.content, "# Return Resonance: lantern-river-01")
        assert_contains(first_result.content, "Status: opened")
        assert_contains(first_result.content, "trust")
        assert_contains(first_result.content, "Do not publish it unless")

        first_result.path.write_text("already remembered\n", encoding="utf-8")
        second_result = open_return_result(artifact, match, directory)

        assert not second_result.created
        assert second_result.content == "already remembered\n"


def test_open_return_result_rejects_non_matching_result() -> None:
    artifact = parse_return_artifact(UNKNOWN_SLOT_ARTIFACT_PATH.read_text(encoding="utf-8"))
    slots = load_return_slots(DEMO_SLOT_PATH)
    match = match_return_artifact(artifact, slots)

    with tempfile.TemporaryDirectory() as directory:
        try:
            open_return_result(artifact, match, directory)
        except ReturnResultError as error:
            assert_contains(str(error), "without a matching slot")
        else:
            raise AssertionError("Expected ReturnResultError for non-matching result.")


def test_open_return_result_requires_existing_file_for_opened_slot() -> None:
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
        match = match_return_artifact(artifact, slots)

        try:
            open_return_result(artifact, match, directory)
        except ReturnResultError as error:
            assert_contains(str(error), "marked as opened")
        else:
            raise AssertionError("Expected ReturnResultError for missing opened result file.")


def test_return_resonance_demo_runner_uses_local_result() -> None:
    demo_runner = load_demo_runner_module()

    with tempfile.TemporaryDirectory() as directory:
        demo_runner.OUTPUT_DIR = Path(directory)
        first_exit_code = demo_runner.main()
        second_exit_code = demo_runner.main()

        result_path = Path(directory) / "return_resonance_lantern_river.local.md"
        assert first_exit_code == 0
        assert second_exit_code == 0
        assert result_path.exists()
        assert_contains(result_path.read_text(encoding="utf-8"), "# Return Resonance: lantern-river-01")


def test_return_resonance_cli_uses_explicit_paths() -> None:
    cli_runner = load_cli_runner_module()

    with tempfile.TemporaryDirectory() as directory:
        exit_code = cli_runner.main(
            [
                "--artifact",
                str(DEMO_ARTIFACT_PATH),
                "--slots",
                str(DEMO_SLOT_PATH),
                "--output-dir",
                directory,
            ]
        )

        result_path = Path(directory) / "return_resonance_lantern_river.local.md"
        assert exit_code == 0
        assert result_path.exists()
        assert_contains(result_path.read_text(encoding="utf-8"), "# Return Resonance: lantern-river-01")


def test_return_resonance_cli_returns_one_for_non_match() -> None:
    cli_runner = load_cli_runner_module()

    with tempfile.TemporaryDirectory() as directory:
        exit_code = cli_runner.main(
            [
                "--artifact",
                str(UNKNOWN_SLOT_ARTIFACT_PATH),
                "--slots",
                str(DEMO_SLOT_PATH),
                "--output-dir",
                directory,
            ]
        )

        assert exit_code == 1
        assert not (Path(directory) / "return_resonance_lantern_river.local.md").exists()


def test_make_return_slot_creates_loadable_slot_file() -> None:
    slot_generator = load_slot_generator_module()

    with tempfile.TemporaryDirectory() as directory:
        output_path = Path(directory) / "slots" / "return_slots.local.json"
        exit_code = slot_generator.main(
            [
                "--origin-trace-id",
                "n01-local-origin-test1",
                "--return-slot-id",
                "quiet-garden-01",
                "--package-id",
                "local-package-test1",
                "--result-file",
                "return_resonance_quiet_garden.local.md",
                "--public-safe-label",
                "quiet garden",
                "--output",
                str(output_path),
            ]
        )

        assert exit_code == 0
        assert output_path.exists()

        raw_data = json.loads(output_path.read_text(encoding="utf-8"))
        assert raw_data["document_status"] == "private local return slots"

        slots = load_return_slots(output_path)
        assert len(slots) == 1
        slot = slots[0]
        assert slot.origin_trace_id == "n01-local-origin-test1"
        assert slot.return_slot_id == "quiet-garden-01"
        assert slot.module_id == "N01"
        assert slot.package_id == "local-package-test1"
        assert slot.layer_id == "return-resonance-1"
        assert slot.status == ReturnSlotState.WAITING
        assert slot.result_file == "return_resonance_quiet_garden.local.md"


def test_generated_slot_can_open_matching_return_artifact() -> None:
    slot_generator = load_slot_generator_module()
    artifact = parse_return_artifact(QUIET_GARDEN_ARTIFACT_PATH.read_text(encoding="utf-8"))

    with tempfile.TemporaryDirectory() as directory:
        base_dir = Path(directory)
        slot_path = base_dir / "slots" / "return_slots.local.json"
        result_dir = base_dir / "results"

        exit_code = slot_generator.main(
            [
                "--origin-trace-id",
                "n01-local-origin-a4m9",
                "--return-slot-id",
                "quiet-garden-01",
                "--package-id",
                "local-package-garden-01",
                "--result-file",
                "return_resonance_quiet_garden.local.md",
                "--public-safe-label",
                "quiet garden",
                "--output",
                str(slot_path),
            ]
        )

        assert exit_code == 0
        slots = load_return_slots(slot_path)
        match = match_return_artifact(artifact, slots)
        result = open_return_result(artifact, match, result_dir)

        assert match.status == MatchStatus.MATCH_WAITING
        assert match.is_match
        assert result.created
        assert result.path.name == "return_resonance_quiet_garden.local.md"
        assert result.path.exists()
        assert_contains(result.content, "# Return Resonance: quiet-garden-01")
        assert_contains(result.content, "patience")


def test_generated_slot_result_reuses_existing_local_file() -> None:
    slot_generator = load_slot_generator_module()
    artifact = parse_return_artifact(QUIET_GARDEN_ARTIFACT_PATH.read_text(encoding="utf-8"))

    with tempfile.TemporaryDirectory() as directory:
        base_dir = Path(directory)
        slot_path = base_dir / "slots" / "return_slots.local.json"
        result_dir = base_dir / "results"

        exit_code = slot_generator.main(
            [
                "--origin-trace-id",
                "n01-local-origin-a4m9",
                "--return-slot-id",
                "quiet-garden-01",
                "--package-id",
                "local-package-garden-01",
                "--result-file",
                "return_resonance_quiet_garden.local.md",
                "--public-safe-label",
                "quiet garden",
                "--output",
                str(slot_path),
            ]
        )

        assert exit_code == 0
        slots = load_return_slots(slot_path)
        match = match_return_artifact(artifact, slots)
        first_result = open_return_result(artifact, match, result_dir)

        assert first_result.created
        first_result.path.write_text("quiet garden already remembered\n", encoding="utf-8")

        second_result = open_return_result(artifact, match, result_dir)

        assert not second_result.created
        assert second_result.content == "quiet garden already remembered\n"
        assert first_result.path.read_text(encoding="utf-8") == "quiet garden already remembered\n"


def test_make_return_slot_does_not_overwrite_without_flag() -> None:
    slot_generator = load_slot_generator_module()

    with tempfile.TemporaryDirectory() as directory:
        output_path = Path(directory) / "return_slots.local.json"
        output_path.write_text("already here\n", encoding="utf-8")

        exit_code = slot_generator.main(
            [
                "--origin-trace-id",
                "n01-local-origin-test1",
                "--return-slot-id",
                "quiet-garden-01",
                "--package-id",
                "local-package-test1",
                "--result-file",
                "return_resonance_quiet_garden.local.md",
                "--public-safe-label",
                "quiet garden",
                "--output",
                str(output_path),
            ]
        )

        assert exit_code == 1
        assert output_path.read_text(encoding="utf-8") == "already here\n"


def test_return_resonance_import_does_not_load_first_spark() -> None:
    newly_imported = AFTER_RETURN_RESONANCE_IMPORTS - BEFORE_RETURN_RESONANCE_IMPORTS
    forbidden_imports = {
        name for name in newly_imported if name == "first_spark" or name.startswith("first_spark.")
    }

    if forbidden_imports:
        raise AssertionError(
            "Return Resonance imported First Spark unexpectedly: "
            + ", ".join(sorted(forbidden_imports))
        )


if __name__ == "__main__":
    test_parse_demo_return_artifact()
    test_parse_unknown_slot_return_artifact()
    test_parse_quiet_garden_return_artifact()
    test_parse_return_artifact_requires_core_fields()
    test_parse_return_artifact_allows_missing_optional_return_word()
    test_load_demo_return_slot()
    test_load_return_slot_requires_slots_list()
    test_load_return_slot_requires_core_fields()
    test_load_return_slot_rejects_unknown_status()
    test_match_demo_artifact_to_waiting_slot()
    test_match_unknown_slot()
    test_match_package_mismatch()
    test_match_layer_mismatch()
    test_match_already_opened_slot()
    test_open_return_result_generates_once_then_reuses()
    test_open_return_result_rejects_non_matching_result()
    test_open_return_result_requires_existing_file_for_opened_slot()
    test_return_resonance_demo_runner_uses_local_result()
    test_return_resonance_cli_uses_explicit_paths()
    test_return_resonance_cli_returns_one_for_non_match()
    test_make_return_slot_creates_loadable_slot_file()
    test_generated_slot_can_open_matching_return_artifact()
    test_generated_slot_result_reuses_existing_local_file()
    test_make_return_slot_does_not_overwrite_without_flag()
    test_return_resonance_import_does_not_load_first_spark()
    print("Return Resonance MVP tests passed.")
