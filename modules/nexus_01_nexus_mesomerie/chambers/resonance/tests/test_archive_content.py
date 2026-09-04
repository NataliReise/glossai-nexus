#!/usr/bin/env python3
"""Focused tests for the strict Nexus 01 Archive content Block loader."""

from __future__ import annotations

from dataclasses import FrozenInstanceError
import json
from pathlib import Path
import sys

NEXUS_01_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(NEXUS_01_ROOT))

from chambers.resonance.archive_content import (
    ArchiveBlockLoadError,
    load_archive_block,
)


ORIGIN_BLOCK = (
    NEXUS_01_ROOT
    / "chambers/resonance/archive_blocks/builtin/n01-resonance-archive-origin"
)


def _manifest() -> dict[str, object]:
    return {
        "format": "nexus.chamber-block.v1",
        "block_type": "archive-content",
        "block_id": "test-archive-block",
        "target_module": "nexus-01",
        "target_chamber": "resonance",
        "schema_version": 1,
        "title": "Test Archive",
    }


def _open_entry(entry_id: str = "entry-one") -> dict[str, object]:
    return {
        "entry_id": entry_id,
        "title": "Entry One",
        "access": "open",
        "poetic_indication": ["A small trace."],
        "clear_orientation": ["A clear orientation."],
        "deeper_trace": ["A deeper trace."],
    }


def _sealed_entry(entry_id: str = "sealed-entry") -> dict[str, object]:
    return {
        "entry_id": entry_id,
        "title": "Sealed Entry",
        "access": "sealed",
        "poetic_indication": ["Something rests behind this threshold."],
    }


def _write_json(path: Path, data: object) -> None:
    path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def _make_block(
    root: Path,
    *,
    manifest: dict[str, object] | None = None,
    entries: tuple[dict[str, object], ...] | None = None,
) -> Path:
    block = root / "block"
    content = block / "content"
    content.mkdir(parents=True)
    _write_json(block / "manifest.json", _manifest() if manifest is None else manifest)
    selected_entries = (_open_entry(),) if entries is None else entries
    for index, entry in enumerate(selected_entries, start=1):
        _write_json(content / f"{index:03}.json", entry)
    return block


def _expect_load_error(path: Path, expected_text: str) -> None:
    try:
        load_archive_block(path)
    except ArchiveBlockLoadError as error:
        assert expected_text in str(error), str(error)
    else:
        raise AssertionError("Invalid Archive Block was accepted.")


def test_builtin_origin_block_loads_as_immutable_domain_objects() -> None:
    block = load_archive_block(ORIGIN_BLOCK)

    assert block.block_id == "n01-resonance-archive-origin"
    assert block.target_module == "nexus-01"
    assert block.target_chamber == "resonance"
    assert block.schema_version == 1
    assert tuple(entry.entry_id for entry in block.entries) == (
        "what-is-a-nexus",
        "first-spark-chamber",
        "resonance-as-a-gift",
    )
    assert isinstance(block.entries, tuple)
    assert isinstance(block.entries[0].poetic_indication, tuple)

    try:
        block.title = "Changed"  # type: ignore[misc]
    except FrozenInstanceError:
        pass
    else:
        raise AssertionError("ArchiveContentBlock was mutable.")


def test_missing_manifest_is_rejected(tmp_path: Path) -> None:
    block = _make_block(tmp_path)
    (block / "manifest.json").unlink()

    _expect_load_error(block, "exactly manifest.json and content")


def test_malformed_json_and_duplicate_json_keys_are_rejected(tmp_path: Path) -> None:
    malformed = _make_block(tmp_path / "malformed")
    (malformed / "manifest.json").write_text("{", encoding="utf-8")
    _expect_load_error(malformed, "not valid strict JSON")

    duplicate = _make_block(tmp_path / "duplicate")
    (duplicate / "manifest.json").write_text(
        '{"format":"nexus.chamber-block.v1","format":"again"}',
        encoding="utf-8",
    )
    _expect_load_error(duplicate, "duplicate JSON key")


def test_manifest_requires_exact_fields_and_supported_identity(tmp_path: Path) -> None:
    unknown = _manifest()
    unknown["extra"] = "no"
    _expect_load_error(
        _make_block(tmp_path / "unknown", manifest=unknown),
        "unknown extra",
    )

    missing = _manifest()
    del missing["title"]
    _expect_load_error(
        _make_block(tmp_path / "missing", manifest=missing),
        "missing title",
    )

    cases = (
        ("format", "other", "format must equal"),
        ("block_type", "other", "block_type must equal"),
        ("target_module", "nexus-02", "target_module must equal"),
        ("target_chamber", "other", "target_chamber must equal"),
        ("schema_version", 2, "unsupported schema_version"),
    )
    for index, (field, value, message) in enumerate(cases):
        manifest = _manifest()
        manifest[field] = value
        _expect_load_error(
            _make_block(tmp_path / f"case-{index}", manifest=manifest),
            message,
        )


def test_manifest_rejects_invalid_identifier_title_and_boolean_schema(tmp_path: Path) -> None:
    bad_id = _manifest()
    bad_id["block_id"] = "not safe"
    _expect_load_error(
        _make_block(tmp_path / "bad-id", manifest=bad_id),
        "public-safe ASCII identifier",
    )

    bad_title = _manifest()
    bad_title["title"] = "   "
    _expect_load_error(
        _make_block(tmp_path / "bad-title", manifest=bad_title),
        "non-empty UTF-8 string",
    )

    boolean_schema = _manifest()
    boolean_schema["schema_version"] = True
    _expect_load_error(
        _make_block(tmp_path / "bool-schema", manifest=boolean_schema),
        "must be the integer 1",
    )


def test_open_entry_requires_exact_fields_and_nonempty_text_arrays(tmp_path: Path) -> None:
    missing = _open_entry()
    del missing["clear_orientation"]
    _expect_load_error(
        _make_block(tmp_path / "missing", entries=(missing,)),
        "missing clear_orientation",
    )

    unknown = _open_entry()
    unknown["extra"] = "no"
    _expect_load_error(
        _make_block(tmp_path / "unknown", entries=(unknown,)),
        "unknown extra",
    )

    empty = _open_entry()
    empty["poetic_indication"] = []
    _expect_load_error(
        _make_block(tmp_path / "empty", entries=(empty,)),
        "poetic_indication must be a non-empty array",
    )

    blank = _open_entry()
    blank["clear_orientation"] = ["   "]
    _expect_load_error(
        _make_block(tmp_path / "blank", entries=(blank,)),
        "must contain only non-empty text strings",
    )


def test_entry_identifier_and_access_are_strict(tmp_path: Path) -> None:
    bad_id = _open_entry("not safe")
    _expect_load_error(
        _make_block(tmp_path / "bad-id", entries=(bad_id,)),
        "public-safe ASCII identifier",
    )

    bad_access = _open_entry()
    bad_access["access"] = "hidden"
    _expect_load_error(
        _make_block(tmp_path / "bad-access", entries=(bad_access,)),
        "access must be 'open' or 'sealed'",
    )

    non_string_access = _open_entry()
    non_string_access["access"] = []
    _expect_load_error(
        _make_block(tmp_path / "non-string-access", entries=(non_string_access,)),
        "access must be 'open' or 'sealed'",
    )


def test_sealed_entry_allows_only_optional_public_teaser(tmp_path: Path) -> None:
    block = load_archive_block(
        _make_block(tmp_path / "valid", entries=(_sealed_entry(),))
    )
    entry = block.entries[0]
    assert entry.access == "sealed"
    assert entry.poetic_indication == ("Something rests behind this threshold.",)
    assert entry.clear_orientation == ()
    assert entry.deeper_trace == ()

    invalid = _sealed_entry()
    invalid["clear_orientation"] = ["This must remain absent."]
    _expect_load_error(
        _make_block(tmp_path / "invalid", entries=(invalid,)),
        "unknown clear_orientation",
    )


def test_duplicate_entry_ids_are_rejected(tmp_path: Path) -> None:
    _expect_load_error(
        _make_block(
            tmp_path,
            entries=(_open_entry("same-entry"), _open_entry("same-entry")),
        ),
        "duplicate entry_id",
    )


def test_content_files_are_loaded_in_deterministic_filename_order(tmp_path: Path) -> None:
    block = _make_block(tmp_path)
    content = block / "content"
    for path in content.iterdir():
        path.unlink()
    _write_json(content / "020.json", _open_entry("second"))
    _write_json(content / "010.json", _open_entry("first"))

    loaded = load_archive_block(block)

    assert tuple(entry.entry_id for entry in loaded.entries) == ("first", "second")


def test_block_rejects_extra_root_files_nested_directories_and_empty_content(
    tmp_path: Path,
) -> None:
    extra = _make_block(tmp_path / "extra")
    (extra / "README.md").write_text("not allowed\n", encoding="utf-8")
    _expect_load_error(extra, "unexpected README.md")

    nested = _make_block(tmp_path / "nested")
    (nested / "content" / "nested").mkdir()
    _expect_load_error(nested, "Nested directories are not allowed")

    empty = _make_block(tmp_path / "empty")
    for path in (empty / "content").iterdir():
        path.unlink()
    _expect_load_error(empty, "at least one JSON entry")


def test_content_rejects_non_json_files_and_symbolic_links(tmp_path: Path) -> None:
    non_json = _make_block(tmp_path / "non-json")
    (non_json / "content" / "note.txt").write_text("no\n", encoding="utf-8")
    _expect_load_error(non_json, "accepts only .json files")

    symlink = _make_block(tmp_path / "symlink")
    (symlink / "content" / "linked.json").symlink_to("001.json")
    _expect_load_error(symlink, "Symbolic links are not allowed")

    target = _make_block(tmp_path / "root-target")
    root_link = tmp_path / "root-link"
    root_link.symlink_to(target, target_is_directory=True)
    _expect_load_error(root_link, "must not be a symbolic link")


def test_selected_block_does_not_discover_or_validate_siblings(tmp_path: Path) -> None:
    selected = _make_block(tmp_path / "selected")
    sibling = _make_block(tmp_path / "sibling")
    (sibling / "manifest.json").write_text("{", encoding="utf-8")

    loaded = load_archive_block(selected)

    assert loaded.block_id == "test-archive-block"
