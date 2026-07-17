"""Tests for the practical local Resonance Return opening command."""

from __future__ import annotations

import json
from itertools import product
from pathlib import Path
import sys
import tempfile

NEXUS_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(NEXUS_ROOT))

from open_resonance_return import LocalResonanceOpenError, open_resonance_return_files
from chambers.resonance.choices import build_v0_1_catalog
from return_resonance.compact_generator import generate_compact_resonance
from return_resonance.resonance_render_bridge import (
    ChamberSelections,
    build_resonance_return_artifact,
)
from return_resonance.token import ResonanceToken

LIBRARY_DIR = NEXUS_ROOT / "resonance_language_library" / "v0_1"


def _token() -> ResonanceToken:
    return ResonanceToken(
        token_version="N01-RT-1",
        token_type="resonance-activation",
        module_id="N01",
        layer_id="return-resonance-1",
        origin_trace_id="n01-test-origin",
        return_slot_id="test-return-slot",
        package_id="test-package",
        enabled_chambers=("resonance",),
    )


def _artifact_dict(
    image_path: tuple[str, str] = ("waiting-lantern", "appearing-path"),
    scent_path: tuple[str, str] = ("summer-rain", "possibility-of-encounter"),
    movement_path: tuple[str, str] = ("falling-feather", "crossing-feather"),
    *,
    wish_word: str = "courage",
    return_word: str = "trust",
) -> dict[str, str]:
    artifact = build_resonance_return_artifact(
        _token(),
        ChamberSelections(
            image_id=image_path[0],
            image_response_id=image_path[1],
            scent_id=scent_path[0],
            scent_response_id=scent_path[1],
            movement_id=movement_path[0],
            movement_response_id=movement_path[1],
            wish_word=wish_word,
            return_word=return_word,
        ),
    )
    return artifact.to_dict()


def _slot_item(
    *,
    slot_status: str = "waiting",
    result_file: str = "test-return.local.md",
    return_slot_id: str = "test-return-slot",
    origin_trace_id: str = "n01-test-origin",
) -> dict[str, str]:
    return {
        "origin_trace_id": origin_trace_id,
        "return_slot_id": return_slot_id,
        "module_id": "N01",
        "package_id": "test-package",
        "layer_id": "return-resonance-1",
        "status": slot_status,
        "result_file": result_file,
        "public_safe_label": "test light",
        "note": "test only",
    }


def _write_inputs(
    root: Path,
    *,
    slot_status: str = "waiting",
    result_file: str = "test-return.local.md",
    artifact_data: dict[str, str] | None = None,
    slots: list[dict[str, str]] | None = None,
) -> tuple[Path, Path, Path]:
    artifact_path = root / "return-artifact.json"
    slots_path = root / "return-slots.json"
    output_dir = root / "results"

    artifact_path.write_text(
        json.dumps(artifact_data or _artifact_dict(), indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    slots_path.write_text(
        json.dumps(
            {
                "document_status": "local test fixture",
                "slots": slots or [_slot_item(slot_status=slot_status, result_file=result_file)],
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    return artifact_path, slots_path, output_dir


def _slot_status(path: Path) -> str:
    document = json.loads(path.read_text(encoding="utf-8"))
    return document["slots"][0]["status"]


def _fail_generator(*args: object, **kwargs: object) -> object:
    raise AssertionError("generator must not be called")


def test_first_open_creates_result_and_marks_slot_opened() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        artifact_path, slots_path, output_dir = _write_inputs(root)
        calls = 0

        def counted_generator(artifact: object, *, seed: object) -> object:
            nonlocal calls
            calls += 1
            return generate_compact_resonance(artifact, seed=seed)

        result = open_resonance_return_files(
            artifact_path,
            slots_path,
            output_dir,
            LIBRARY_DIR,
            generator=counted_generator,
        )

        assert result.created is True
        assert result.slot_state_changed is True
        assert result.path == output_dir / "test-return.local.md"
        assert result.path.exists()
        assert result.content == result.path.read_text(encoding="utf-8")
        assert "# Resonance Return" in result.content
        assert "## Compact Resonance" in result.content
        assert "Summer rain carries the possibility of encounter." in result.content
        assert "courage" in result.content
        assert "\ntrust\n```" in result.content
        assert "Resonance Artifact" not in result.content
        assert "Nexus Echo" not in result.content
        assert result.generation is not None
        assert result.generation.generator_id == "nexus-01-compact-resonance"
        assert calls == 1
        assert '"composition_plan"' in result.content
        assert '"artifact_identity"' in result.content
        assert _slot_status(slots_path) == "opened"


def test_second_open_reuses_result_without_overwriting() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        artifact_path, slots_path, output_dir = _write_inputs(root)

        first = open_resonance_return_files(
            artifact_path,
            slots_path,
            output_dir,
            LIBRARY_DIR,
        )
        original = first.path.read_bytes()
        edited = original + "\nLOCAL NOTE — behalten\n".encode("utf-8")
        first.path.write_bytes(edited)

        second = open_resonance_return_files(
            artifact_path,
            slots_path,
            output_dir,
            LIBRARY_DIR,
            generator=_fail_generator,
        )

        assert second.created is False
        assert second.slot_state_changed is False
        assert second.generation is None
        assert second.content.encode("utf-8") == edited
        assert second.path.read_bytes() == edited
        assert _slot_status(slots_path) == "opened"


def test_opened_slot_without_result_is_rejected() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        artifact_path, slots_path, output_dir = _write_inputs(root, slot_status="opened")

        try:
            open_resonance_return_files(
                artifact_path,
                slots_path,
                output_dir,
                LIBRARY_DIR,
            )
        except LocalResonanceOpenError as error:
            assert "marked as opened" in str(error)
            assert "result file is missing" in str(error)
        else:
            raise AssertionError("Expected LocalResonanceOpenError")


def test_mismatched_package_creates_nothing_and_changes_no_state() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        artifact_path, slots_path, output_dir = _write_inputs(root)
        artifact = json.loads(artifact_path.read_text(encoding="utf-8"))
        artifact["package_id"] = "wrong-package"
        artifact_path.write_text(json.dumps(artifact, indent=2) + "\n", encoding="utf-8")

        try:
            open_resonance_return_files(
                artifact_path,
                slots_path,
                output_dir,
                LIBRARY_DIR,
            )
        except Exception as error:
            assert "package_mismatch" in str(error)
        else:
            raise AssertionError("Expected mismatch error")

        assert not output_dir.exists()
        assert _slot_status(slots_path) == "waiting"


def test_waiting_result_repairs_state_without_regeneration_after_update_failure() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        artifact_path, slots_path, output_dir = _write_inputs(root)

        def fail_update(*args: object) -> bool:
            raise OSError("simulated slot update failure")

        try:
            open_resonance_return_files(
                artifact_path,
                slots_path,
                output_dir,
                slot_state_updater=fail_update,
            )
        except LocalResonanceOpenError as error:
            assert "result was preserved successfully" in str(error)
            assert "retry" in str(error)
        else:
            raise AssertionError("Expected slot update recovery error")

        result_path = output_dir / "test-return.local.md"
        preserved = result_path.read_bytes()
        assert preserved
        assert _slot_status(slots_path) == "waiting"

        recovered = open_resonance_return_files(
            artifact_path,
            slots_path,
            output_dir,
            generator=_fail_generator,
        )
        assert recovered.created is False
        assert recovered.slot_state_changed is True
        assert recovered.content.encode("utf-8") == preserved
        assert result_path.read_bytes() == preserved
        assert _slot_status(slots_path) == "opened"


def test_all_125_chamber_combinations_cross_opening_boundary() -> None:
    catalog = build_v0_1_catalog()
    image_paths = [
        (option.id, catalog.image_compatibility[option.id][0]) for option in catalog.images
    ]
    scent_paths = [
        (option.id, catalog.scent_compatibility[option.id][0]) for option in catalog.scents
    ]
    movement_paths = [
        (option.id, catalog.movement_compatibility[option.id][0])
        for option in catalog.movements
    ]
    combinations = list(product(image_paths, scent_paths, movement_paths))
    assert len(combinations) == 125

    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        for index, (image_path, scent_path, movement_path) in enumerate(combinations):
            case_root = root / f"case-{index:03d}"
            case_root.mkdir()
            artifact = _artifact_dict(image_path, scent_path, movement_path)
            artifact_path, slots_path, output_dir = _write_inputs(
                case_root,
                artifact_data=artifact,
                result_file=f"result-{index:03d}.local.md",
            )
            result = open_resonance_return_files(
                artifact_path,
                slots_path,
                output_dir,
                library_dir=case_root / "missing-legacy-library",
            )
            assert result.created is True
            assert result.generation is not None
            assert result.content.count("```text") == 1
            assert result.generation.text in result.content


def test_opening_is_deterministic_for_same_structural_identity() -> None:
    contents: list[bytes] = []
    seeds: list[object] = []
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        for name in ("first", "second"):
            case_root = root / name
            case_root.mkdir()
            artifact_path, slots_path, output_dir = _write_inputs(case_root)
            result = open_resonance_return_files(artifact_path, slots_path, output_dir)
            contents.append(result.path.read_bytes())
            assert result.generation is not None
            seeds.append(result.generation.composition_plan["seed"])
    assert contents[0] == contents[1]
    assert seeds[0] == seeds[1]


def test_unicode_and_identical_words_remain_visible_and_separated() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        artifact = _artifact_dict(wish_word="Nähe", return_word="Nähe")
        artifact_path, slots_path, output_dir = _write_inputs(root, artifact_data=artifact)
        result = open_resonance_return_files(artifact_path, slots_path, output_dir)

        assert result.generation is not None
        lines = result.generation.text.splitlines()
        assert lines[-1] == "Nähe"
        assert "Nähe" not in lines[-2]
        assert (
            result.generation.composition_plan["same_word_strategy"]
            == "separated-wish-role-and-final-return"
        )
        assert result.path.read_text(encoding="utf-8") == result.content


def test_unsafe_and_ambiguous_result_filenames_are_rejected() -> None:
    unsafe_names = (
        "",
        "/tmp/escape.md",
        "../escape.md",
        "nested/result.md",
        "nested\\result.md",
        ".hidden.md",
        "result..md",
        "CON.md",
        "trailing.",
        "space name.md",
    )
    for index, result_file in enumerate(unsafe_names):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            artifact_path, slots_path, output_dir = _write_inputs(
                root,
                result_file=result_file,
            )
            try:
                open_resonance_return_files(artifact_path, slots_path, output_dir)
            except Exception as error:
                assert "result_file" in str(error) or "required field" in str(error)
            else:
                raise AssertionError(f"Unsafe result filename was accepted: {index}: {result_file!r}")
            assert not output_dir.exists()


def test_two_slots_cannot_share_case_insensitive_result_target() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        slots = [
            _slot_item(result_file="shared.local.md"),
            _slot_item(
                result_file="SHARED.local.md",
                return_slot_id="other-slot",
                origin_trace_id="other-origin",
            ),
        ]
        artifact_path, slots_path, output_dir = _write_inputs(root, slots=slots)
        try:
            open_resonance_return_files(artifact_path, slots_path, output_dir)
        except LocalResonanceOpenError as error:
            assert "Multiple Return Slots" in str(error)
        else:
            raise AssertionError("Expected duplicate result target rejection")
        assert not output_dir.exists()
        assert _slot_status(slots_path) == "waiting"


def test_atomic_publication_never_overwrites_racing_result() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        artifact_path, slots_path, output_dir = _write_inputs(root)
        result_path = output_dir / "test-return.local.md"
        foreign_content = b"another return already arrived\n"

        def racing_generator(artifact: object, *, seed: object) -> object:
            generated = generate_compact_resonance(artifact, seed=seed)
            output_dir.mkdir(parents=True)
            result_path.write_bytes(foreign_content)
            return generated

        try:
            open_resonance_return_files(
                artifact_path,
                slots_path,
                output_dir,
                generator=racing_generator,
            )
        except LocalResonanceOpenError as error:
            assert "Refusing to overwrite" in str(error)
        else:
            raise AssertionError("Expected exclusive publication failure")

        assert result_path.read_bytes() == foreign_content
        assert _slot_status(slots_path) == "waiting"


def test_legacy_renderer_is_not_invoked() -> None:
    import resonance_language_library.render_resonance_output as legacy_output
    import return_resonance.resonance_render_bridge as legacy_bridge

    original_bridge = legacy_bridge.open_resonance_return
    original_renderer = legacy_output.render_resonance_output

    def fail_legacy(*args: object, **kwargs: object) -> object:
        raise AssertionError("legacy renderer must not be called")

    legacy_bridge.open_resonance_return = fail_legacy
    legacy_output.render_resonance_output = fail_legacy
    try:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            artifact_path, slots_path, output_dir = _write_inputs(root)
            result = open_resonance_return_files(
                artifact_path,
                slots_path,
                output_dir,
                library_dir=root / "does-not-exist",
            )
            assert result.created is True
            assert "## Compact Resonance" in result.content
    finally:
        legacy_bridge.open_resonance_return = original_bridge
        legacy_output.render_resonance_output = original_renderer


if __name__ == "__main__":
    test_first_open_creates_result_and_marks_slot_opened()
    test_second_open_reuses_result_without_overwriting()
    test_opened_slot_without_result_is_rejected()
    test_mismatched_package_creates_nothing_and_changes_no_state()
    test_waiting_result_repairs_state_without_regeneration_after_update_failure()
    test_all_125_chamber_combinations_cross_opening_boundary()
    test_opening_is_deterministic_for_same_structural_identity()
    test_unicode_and_identical_words_remain_visible_and_separated()
    test_unsafe_and_ambiguous_result_filenames_are_rejected()
    test_two_slots_cannot_share_case_insensitive_result_target()
    test_atomic_publication_never_overwrites_racing_result()
    test_legacy_renderer_is_not_invoked()
    print("Local Resonance Return opening tests passed.")
