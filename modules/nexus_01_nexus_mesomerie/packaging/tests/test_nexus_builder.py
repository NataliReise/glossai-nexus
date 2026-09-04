from __future__ import annotations

from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
import json
from pathlib import Path
import sys
from unittest.mock import patch


NEXUS_ROOT = Path(__file__).resolve().parents[2]
PACKAGING_ROOT = NEXUS_ROOT / "packaging"
for import_root in (PACKAGING_ROOT, NEXUS_ROOT):
    if str(import_root) not in sys.path:
        sys.path.insert(0, str(import_root))

from nexus_builder import main as builder_main  # noqa: E402
from nexus_builder_core import (  # noqa: E402
    COUPLED_ARCHIVE_ROOT,
    NexusBuilderError,
    couple_archive_block,
    inspect_archive_block,
    inspect_nexus,
)


def _write_block(
    path: Path,
    *,
    block_id: str,
    title: str | None = None,
    entry_id: str | None = None,
) -> Path:
    path.mkdir(parents=True)
    manifest = {
        "format": "nexus.chamber-block.v1",
        "block_type": "archive-content",
        "block_id": block_id,
        "target_module": "nexus-01",
        "target_chamber": "resonance",
        "schema_version": 1,
        "title": title or block_id,
    }
    entry = {
        "entry_id": entry_id or f"{block_id}-entry",
        "title": "Builder Test Entry",
        "access": "open",
        "poetic_indication": ["A small trace waits here."],
        "clear_orientation": ["This is public-safe test Archive content."],
    }
    (path / "content").mkdir()
    (path / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    (path / "content/001.json").write_text(
        json.dumps(entry, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return path


def _make_nexus(tmp_path: Path) -> Path:
    nexus = tmp_path / "nexus"
    (nexus / "chambers/resonance").mkdir(parents=True)
    (nexus / "run_nexus.py").write_text("# test marker\n", encoding="utf-8")
    (nexus / "chambers/resonance/archive_content.py").write_text(
        "# test marker\n",
        encoding="utf-8",
    )
    (nexus / "atrium").mkdir()
    (nexus / "atrium/classified_resonance.py").write_text(
        "# test marker\n",
        encoding="utf-8",
    )
    _write_block(
        nexus
        / "chambers/resonance/archive_blocks/builtin"
        / "n01-resonance-archive-origin",
        block_id="n01-resonance-archive-origin",
        title="Origin",
    )
    return nexus


def test_builder_inspects_real_reference_block() -> None:
    block = inspect_archive_block(
        NEXUS_ROOT
        / "chambers/resonance/archive_blocks/builtin"
        / "n01-resonance-archive-origin"
    )

    assert block.block_id == "n01-resonance-archive-origin"
    assert block.target_module == "nexus-01"
    assert block.target_chamber == "resonance"
    assert len(block.entries) == 3


def test_missing_coupled_root_is_valid_and_read_only(tmp_path: Path) -> None:
    nexus = _make_nexus(tmp_path)
    coupled_root = nexus / COUPLED_ARCHIVE_ROOT
    assert not coupled_root.exists()

    constellation = inspect_nexus(nexus)

    assert [block.block_id for block in constellation.builtin_blocks] == [
        "n01-resonance-archive-origin"
    ]
    assert constellation.coupled_blocks == ()
    assert not coupled_root.exists()


def test_builder_reads_only_explicit_archive_roots(tmp_path: Path) -> None:
    nexus = _make_nexus(tmp_path)
    unrelated = _write_block(
        nexus / "downloads-looking-nearby-block",
        block_id="must-not-be-discovered",
    )

    constellation = inspect_nexus(nexus)

    assert constellation.block_ids == ("n01-resonance-archive-origin",)
    assert unrelated.is_dir()


def test_builder_shows_builtin_and_coupled_blocks_deterministically(
    tmp_path: Path,
) -> None:
    nexus = _make_nexus(tmp_path)
    coupled_root = nexus / COUPLED_ARCHIVE_ROOT
    _write_block(coupled_root / "z-source-name", block_id="z-block")
    _write_block(coupled_root / "a-source-name", block_id="a-block")

    constellation = inspect_nexus(nexus)

    assert [block.block_id for block in constellation.coupled_blocks] == [
        "a-block",
        "z-block",
    ]
    assert constellation.block_ids == (
        "n01-resonance-archive-origin",
        "a-block",
        "z-block",
    )


def test_duplicate_block_identity_is_rejected(tmp_path: Path) -> None:
    nexus = _make_nexus(tmp_path)
    _write_block(
        nexus / COUPLED_ARCHIVE_ROOT / "duplicate-copy",
        block_id="n01-resonance-archive-origin",
    )

    try:
        inspect_nexus(nexus)
    except NexusBuilderError as error:
        assert "duplicate block_id: n01-resonance-archive-origin" in str(error)
    else:
        raise AssertionError("duplicate block_id should be rejected")


def test_invalid_child_in_explicit_block_root_is_rejected(tmp_path: Path) -> None:
    nexus = _make_nexus(tmp_path)
    coupled_root = nexus / COUPLED_ARCHIVE_ROOT
    coupled_root.mkdir(parents=True)
    (coupled_root / "README.txt").write_text("not a Block\n", encoding="utf-8")

    try:
        inspect_nexus(nexus)
    except NexusBuilderError as error:
        assert "may contain only Block directories" in str(error)
    else:
        raise AssertionError("non-Block child should be rejected")


def test_builder_cli_is_thin_and_reports_same_constellation(tmp_path: Path) -> None:
    nexus = _make_nexus(tmp_path)
    stdout = StringIO()
    stderr = StringIO()

    with redirect_stdout(stdout), redirect_stderr(stderr):
        exit_code = builder_main(
            ["show-constellation", "--nexus-root", str(nexus)]
        )

    assert exit_code == 0
    assert stderr.getvalue() == ""
    output = stdout.getvalue()
    assert "Archive constellation" in output
    assert "n01-resonance-archive-origin — Origin" in output
    assert "Coupled Blocks:\n  (none)" in output


def _archive_stage_dirs(nexus: Path) -> tuple[Path, ...]:
    archive_parent = nexus / COUPLED_ARCHIVE_ROOT.parent
    return tuple(
        path
        for path in archive_parent.iterdir()
        if path.name.startswith(".nexus-builder-stage-")
    )


def test_builder_couples_valid_block_to_normalized_destination(
    tmp_path: Path,
) -> None:
    nexus = _make_nexus(tmp_path / "target")
    source = _write_block(
        tmp_path / "external" / "friendly-source-folder",
        block_id="carried.archive-1",
        title="Carried Archive",
        entry_id="carried-entry",
    )
    activation = nexus / "first_spark/activation.local.json"
    activation.parent.mkdir()
    activation.write_text('{"private":"keep"}\n', encoding="utf-8")
    private_result = nexus / "results/private.local.md"
    private_result.parent.mkdir()
    private_result.write_text("keep private\n", encoding="utf-8")
    source_bytes = {
        path.relative_to(source): path.read_bytes()
        for path in source.rglob("*")
        if path.is_file()
    }

    result = couple_archive_block(source, nexus_root=nexus)

    destination = nexus / COUPLED_ARCHIVE_ROOT / "carried.archive-1"
    assert result.destination == destination
    assert result.block.block_id == "carried.archive-1"
    assert destination.is_dir()
    assert {
        path.relative_to(destination): path.read_bytes()
        for path in destination.rglob("*")
        if path.is_file()
    } == source_bytes
    assert source.is_dir()
    assert activation.read_text(encoding="utf-8") == '{"private":"keep"}\n'
    assert private_result.read_text(encoding="utf-8") == "keep private\n"
    assert result.constellation.block_ids == (
        "n01-resonance-archive-origin",
        "carried.archive-1",
    )
    assert _archive_stage_dirs(nexus) == ()


def test_coupling_refuses_duplicate_block_and_entry_identity(
    tmp_path: Path,
) -> None:
    nexus = _make_nexus(tmp_path / "target")

    duplicate_block = _write_block(
        tmp_path / "duplicate-block-source",
        block_id="n01-resonance-archive-origin",
        entry_id="different-entry",
    )
    try:
        couple_archive_block(duplicate_block, nexus_root=nexus)
    except NexusBuilderError as error:
        assert "duplicate block_id: n01-resonance-archive-origin" in str(error)
    else:
        raise AssertionError("Duplicate block_id was coupled.")

    duplicate_entry = _write_block(
        tmp_path / "duplicate-entry-source",
        block_id="different-block",
        entry_id="n01-resonance-archive-origin-entry",
    )
    try:
        couple_archive_block(duplicate_entry, nexus_root=nexus)
    except NexusBuilderError as error:
        assert "duplicate entry_id: n01-resonance-archive-origin-entry" in str(error)
    else:
        raise AssertionError("Duplicate entry_id was coupled.")

    assert not (nexus / COUPLED_ARCHIVE_ROOT).exists()
    assert _archive_stage_dirs(nexus) == ()


def test_coupling_never_overwrites_existing_destination(tmp_path: Path) -> None:
    nexus = _make_nexus(tmp_path / "target")
    coupled_root = nexus / COUPLED_ARCHIVE_ROOT
    existing = _write_block(
        coupled_root / "candidate-block",
        block_id="other-logical-block",
        entry_id="other-entry",
    )
    source = _write_block(
        tmp_path / "candidate-source",
        block_id="candidate-block",
        entry_id="candidate-entry",
    )
    before = {
        path.relative_to(existing): path.read_bytes()
        for path in existing.rglob("*")
        if path.is_file()
    }

    try:
        couple_archive_block(source, nexus_root=nexus)
    except NexusBuilderError as error:
        assert "Refusing to overwrite existing coupled Block path" in str(error)
    else:
        raise AssertionError("Existing destination was overwritten.")

    after = {
        path.relative_to(existing): path.read_bytes()
        for path in existing.rglob("*")
        if path.is_file()
    }
    assert after == before
    assert _archive_stage_dirs(nexus) == ()


def test_staged_block_validation_failure_leaves_nexus_unchanged(
    tmp_path: Path,
) -> None:
    nexus = _make_nexus(tmp_path / "target")
    source = _write_block(
        tmp_path / "source",
        block_id="staged-failure",
        entry_id="staged-entry",
    )
    validated_source = inspect_archive_block(source)

    with patch(
        "nexus_builder_core.inspect_archive_block",
        side_effect=(
            validated_source,
            NexusBuilderError("injected staged validation failure"),
        ),
    ):
        try:
            couple_archive_block(source, nexus_root=nexus)
        except NexusBuilderError as error:
            assert "injected staged validation failure" in str(error)
        else:
            raise AssertionError("Injected staged validation failure was ignored.")

    assert not (nexus / COUPLED_ARCHIVE_ROOT).exists()
    assert _archive_stage_dirs(nexus) == ()


def test_post_publish_verification_failure_rolls_back_only_new_block(
    tmp_path: Path,
) -> None:
    nexus = _make_nexus(tmp_path / "target")
    source = _write_block(
        tmp_path / "source",
        block_id="rollback-block",
        entry_id="rollback-entry",
    )

    with patch(
        "nexus_builder_core._verify_published_block",
        side_effect=NexusBuilderError("injected final verification failure"),
    ):
        try:
            couple_archive_block(source, nexus_root=nexus)
        except NexusBuilderError as error:
            assert "injected final verification failure" in str(error)
        else:
            raise AssertionError("Injected final verification failure was ignored.")

    assert not (nexus / COUPLED_ARCHIVE_ROOT / "rollback-block").exists()
    assert not (nexus / COUPLED_ARCHIVE_ROOT).exists()
    assert _archive_stage_dirs(nexus) == ()


def test_coupling_refuses_symlink_target_boundaries(tmp_path: Path) -> None:
    real_nexus = _make_nexus(tmp_path / "real-target")
    source = _write_block(
        tmp_path / "source",
        block_id="symlink-test",
        entry_id="symlink-entry",
    )
    root_link = tmp_path / "nexus-link"
    root_link.symlink_to(real_nexus, target_is_directory=True)

    try:
        couple_archive_block(source, nexus_root=root_link)
    except NexusBuilderError as error:
        assert "root must not be a symbolic link" in str(error)
    else:
        raise AssertionError("Symlink Nexus root was accepted.")

    archive_blocks = real_nexus / "chambers/resonance/archive_blocks"
    moved_archive_blocks = tmp_path / "moved-archive-blocks"
    archive_blocks.rename(moved_archive_blocks)
    archive_blocks.symlink_to(moved_archive_blocks, target_is_directory=True)

    try:
        couple_archive_block(source, nexus_root=real_nexus)
    except NexusBuilderError as error:
        assert "unsafe Archive directory boundary" in str(error)
    else:
        raise AssertionError("Symlink Archive boundary was accepted.")

    assert not (moved_archive_blocks / "coupled").exists()


def test_builder_cli_couples_one_explicit_block(tmp_path: Path) -> None:
    nexus = _make_nexus(tmp_path / "target")
    source = _write_block(
        tmp_path / "source",
        block_id="cli-carried-block",
        title="CLI Carried Block",
        entry_id="cli-carried-entry",
    )
    stdout = StringIO()
    stderr = StringIO()

    with redirect_stdout(stdout), redirect_stderr(stderr):
        exit_code = builder_main(
            [
                "couple",
                str(source),
                "--nexus-root",
                str(nexus),
            ]
        )

    assert exit_code == 0
    assert stderr.getvalue() == ""
    output = stdout.getvalue()
    assert "Archive Block coupled." in output
    assert "Block ID: cli-carried-block" in output
    assert "Title: CLI Carried Block" in output
    assert (nexus / COUPLED_ARCHIVE_ROOT / "cli-carried-block").is_dir()


def test_coupling_rejects_non_archive_capable_target(tmp_path: Path) -> None:
    nexus = _make_nexus(tmp_path / "target")
    (nexus / "atrium/classified_resonance.py").unlink()
    source = _write_block(
        tmp_path / "source",
        block_id="missing-runtime",
        entry_id="missing-runtime-entry",
    )

    try:
        couple_archive_block(source, nexus_root=nexus)
    except NexusBuilderError as error:
        assert "Archive-capable runtime file" in str(error)
    else:
        raise AssertionError("Non-Archive-capable target was accepted.")

    assert not (nexus / COUPLED_ARCHIVE_ROOT).exists()


def test_publication_race_refuses_newly_occupied_destination(
    tmp_path: Path,
) -> None:
    nexus = _make_nexus(tmp_path / "target")
    source = _write_block(
        tmp_path / "source",
        block_id="race-block",
        entry_id="race-entry",
    )
    coupled_root = nexus / COUPLED_ARCHIVE_ROOT
    final_block = coupled_root / "race-block"

    import nexus_builder_core as builder_core

    original_prospective = builder_core._prospective_archive_constellation
    call_count = 0

    def occupy_destination(current, candidate) -> None:
        nonlocal call_count
        call_count += 1
        original_prospective(current, candidate)
        if call_count == 2:
            coupled_root.mkdir(parents=True, exist_ok=True)
            final_block.mkdir()
            (final_block / "race-marker.txt").write_text(
                "another actor arrived first\n",
                encoding="utf-8",
            )

    with patch(
        "nexus_builder_core._prospective_archive_constellation",
        side_effect=occupy_destination,
    ):
        try:
            couple_archive_block(source, nexus_root=nexus)
        except NexusBuilderError as error:
            assert "Refusing to overwrite existing coupled Block path" in str(error)
        else:
            raise AssertionError("A newly occupied destination was overwritten.")

    assert (final_block / "race-marker.txt").read_text(
        encoding="utf-8"
    ) == "another actor arrived first\n"
    assert _archive_stage_dirs(nexus) == ()


def test_post_publish_rollback_preserves_preexisting_coupled_blocks(
    tmp_path: Path,
) -> None:
    nexus = _make_nexus(tmp_path / "target")
    coupled_root = nexus / COUPLED_ARCHIVE_ROOT
    existing = _write_block(
        coupled_root / "existing-folder",
        block_id="existing-block",
        entry_id="existing-entry",
    )
    existing_bytes = {
        path.relative_to(existing): path.read_bytes()
        for path in existing.rglob("*")
        if path.is_file()
    }
    source = _write_block(
        tmp_path / "source",
        block_id="new-block",
        entry_id="new-entry",
    )

    with patch(
        "nexus_builder_core._verify_published_block",
        side_effect=NexusBuilderError("injected final verification failure"),
    ):
        try:
            couple_archive_block(source, nexus_root=nexus)
        except NexusBuilderError as error:
            assert "injected final verification failure" in str(error)
        else:
            raise AssertionError("Injected final verification failure was ignored.")

    assert coupled_root.is_dir()
    assert existing.is_dir()
    assert {
        path.relative_to(existing): path.read_bytes()
        for path in existing.rglob("*")
        if path.is_file()
    } == existing_bytes
    assert not (coupled_root / "new-block").exists()
    assert _archive_stage_dirs(nexus) == ()
