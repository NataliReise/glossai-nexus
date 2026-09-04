from __future__ import annotations

from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
import json
from pathlib import Path
import sys


NEXUS_ROOT = Path(__file__).resolve().parents[2]
PACKAGING_ROOT = NEXUS_ROOT / "packaging"
for import_root in (PACKAGING_ROOT, NEXUS_ROOT):
    if str(import_root) not in sys.path:
        sys.path.insert(0, str(import_root))

from nexus_builder import main as builder_main  # noqa: E402
from nexus_builder_core import (  # noqa: E402
    COUPLED_ARCHIVE_ROOT,
    NexusBuilderError,
    inspect_archive_block,
    inspect_nexus,
)


def _write_block(
    path: Path,
    *,
    block_id: str,
    title: str | None = None,
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
        "entry_id": f"{block_id}-entry",
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
