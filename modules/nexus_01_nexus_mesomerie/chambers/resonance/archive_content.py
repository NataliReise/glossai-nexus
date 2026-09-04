"""Strict data-only Archive Block loader for the Nexus 01 Resonance Chamber."""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
import re
from typing import Any


ARCHIVE_BLOCK_FORMAT = "nexus.chamber-block.v1"
ARCHIVE_BLOCK_TYPE = "archive-content"
ARCHIVE_TARGET_MODULE = "nexus-01"
ARCHIVE_TARGET_CHAMBER = "resonance"
ARCHIVE_SCHEMA_VERSION = 1
ARCHIVE_BUILTIN_ROOT = Path("chambers/resonance/archive_blocks/builtin")
ARCHIVE_COUPLED_ROOT = Path("chambers/resonance/archive_blocks/coupled")

_MANIFEST_FIELDS = frozenset(
    {
        "format",
        "block_type",
        "block_id",
        "target_module",
        "target_chamber",
        "schema_version",
        "title",
    }
)
_OPEN_ENTRY_REQUIRED_FIELDS = frozenset(
    {
        "entry_id",
        "title",
        "access",
        "poetic_indication",
        "clear_orientation",
    }
)
_OPEN_ENTRY_ALLOWED_FIELDS = _OPEN_ENTRY_REQUIRED_FIELDS | {"deeper_trace"}
_SEALED_ENTRY_REQUIRED_FIELDS = frozenset({"entry_id", "title", "access"})
_SEALED_ENTRY_ALLOWED_FIELDS = _SEALED_ENTRY_REQUIRED_FIELDS | {"poetic_indication"}
_IDENTIFIER_PATTERN = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]{0,79}")


class ArchiveBlockLoadError(RuntimeError):
    """Raised when selected Archive data or an explicit constellation is invalid."""


@dataclass(frozen=True)
class ArchiveEntry:
    """One validated immutable Archive entry."""

    entry_id: str
    title: str
    access: str
    poetic_indication: tuple[str, ...] = ()
    clear_orientation: tuple[str, ...] = ()
    deeper_trace: tuple[str, ...] = ()


@dataclass(frozen=True)
class ArchiveContentBlock:
    """One validated immutable data-only Archive content Block."""

    format: str
    block_type: str
    block_id: str
    target_module: str
    target_chamber: str
    schema_version: int
    title: str
    entries: tuple[ArchiveEntry, ...]


@dataclass(frozen=True)
class ArchiveContentConstellation:
    """Validated immutable Archive Blocks carried by one Nexus."""

    builtin_blocks: tuple[ArchiveContentBlock, ...]
    coupled_blocks: tuple[ArchiveContentBlock, ...]

    @property
    def blocks(self) -> tuple[ArchiveContentBlock, ...]:
        return (*self.builtin_blocks, *self.coupled_blocks)

    @property
    def entries(self) -> tuple[ArchiveEntry, ...]:
        return tuple(
            entry
            for block in self.blocks
            for entry in block.entries
        )


def load_archive_block(path: str | Path) -> ArchiveContentBlock:
    """Load and strictly validate one explicitly selected Archive Block directory."""

    block_path = Path(path).expanduser()
    _validate_block_shape(block_path)

    manifest = _read_json_object(block_path / "manifest.json", "manifest")
    _validate_manifest(manifest)

    entries: list[ArchiveEntry] = []
    seen_entry_ids: set[str] = set()
    content_dir = block_path / "content"
    for entry_path in sorted(content_dir.iterdir(), key=lambda candidate: candidate.name):
        entry_data = _read_json_object(entry_path, f"entry {entry_path.name}")
        entry = _parse_entry(entry_data, entry_path.name)
        if entry.entry_id in seen_entry_ids:
            raise ArchiveBlockLoadError(
                f"Archive Block contains duplicate entry_id: {entry.entry_id}"
            )
        seen_entry_ids.add(entry.entry_id)
        entries.append(entry)

    return ArchiveContentBlock(
        format=manifest["format"],
        block_type=manifest["block_type"],
        block_id=manifest["block_id"],
        target_module=manifest["target_module"],
        target_chamber=manifest["target_chamber"],
        schema_version=manifest["schema_version"],
        title=manifest["title"],
        entries=tuple(entries),
    )


def load_archive_constellation(
    builtin_root: str | Path,
    coupled_root: str | Path,
) -> ArchiveContentConstellation:
    """Load only the two explicit Archive Block roots for one Nexus."""

    builtin_blocks = _load_block_root(
        Path(builtin_root).expanduser(),
        required=True,
    )
    coupled_blocks = _load_block_root(
        Path(coupled_root).expanduser(),
        required=False,
    )

    return build_archive_constellation(
        builtin_blocks=builtin_blocks,
        coupled_blocks=coupled_blocks,
    )


def build_archive_constellation(
    *,
    builtin_blocks: tuple[ArchiveContentBlock, ...],
    coupled_blocks: tuple[ArchiveContentBlock, ...],
) -> ArchiveContentConstellation:
    """Validate compatibility and build one deterministic Archive constellation."""

    ordered_builtin = tuple(
        sorted(builtin_blocks, key=lambda block: block.block_id)
    )
    ordered_coupled = tuple(
        sorted(coupled_blocks, key=lambda block: block.block_id)
    )

    seen_block_ids: set[str] = set()
    seen_entry_ids: dict[str, str] = {}
    for block in (*ordered_builtin, *ordered_coupled):
        if block.block_id in seen_block_ids:
            raise ArchiveBlockLoadError(
                "Archive constellation contains duplicate block_id: "
                f"{block.block_id}"
            )
        seen_block_ids.add(block.block_id)

        for entry in block.entries:
            previous_block_id = seen_entry_ids.get(entry.entry_id)
            if previous_block_id is not None:
                raise ArchiveBlockLoadError(
                    "Archive constellation contains duplicate entry_id: "
                    f"{entry.entry_id} "
                    f"(Blocks {previous_block_id} and {block.block_id})"
                )
            seen_entry_ids[entry.entry_id] = block.block_id

    return ArchiveContentConstellation(
        builtin_blocks=ordered_builtin,
        coupled_blocks=ordered_coupled,
    )


def _load_block_root(
    block_root: Path,
    *,
    required: bool,
) -> tuple[ArchiveContentBlock, ...]:
    try:
        if block_root.is_symlink():
            raise ArchiveBlockLoadError(
                f"Archive Block root must not be a symbolic link: {block_root}"
            )
        if not block_root.exists():
            if required:
                raise ArchiveBlockLoadError(
                    f"Required Archive Block root is missing: {block_root}"
                )
            return ()
        if not block_root.is_dir():
            raise ArchiveBlockLoadError(
                f"Archive Block root is not a directory: {block_root}"
            )

        children = tuple(sorted(block_root.iterdir(), key=lambda path: path.name))
        if required and not children:
            raise ArchiveBlockLoadError(
                f"Required Archive Block root contains no Blocks: {block_root}"
            )

        blocks: list[ArchiveContentBlock] = []
        for child in children:
            if child.is_symlink():
                raise ArchiveBlockLoadError(
                    f"Archive Block root contains a symbolic link: {child}"
                )
            if not child.is_dir():
                raise ArchiveBlockLoadError(
                    "Archive Block root may contain only Block directories: "
                    f"{child}"
                )
            blocks.append(load_archive_block(child))

        return tuple(sorted(blocks, key=lambda block: block.block_id))
    except ArchiveBlockLoadError:
        raise
    except OSError as error:
        raise ArchiveBlockLoadError(
            f"Archive Block root could not be inspected: {block_root}: {error}"
        ) from error


def _validate_block_shape(block_path: Path) -> None:
    try:
        if block_path.is_symlink():
            raise ArchiveBlockLoadError(
                f"Archive Block path must not be a symbolic link: {block_path}"
            )
        if not block_path.exists():
            raise ArchiveBlockLoadError(f"Archive Block does not exist: {block_path}")
        if not block_path.is_dir():
            raise ArchiveBlockLoadError(
                f"Archive Block must be a directory: {block_path}"
            )

        children = tuple(block_path.iterdir())
        for child in children:
            if child.is_symlink():
                raise ArchiveBlockLoadError(
                    f"Symbolic links are not allowed inside an Archive Block: {child.name}"
                )

        child_names = {child.name for child in children}
        required_names = {"manifest.json", "content"}
        if child_names != required_names:
            missing = sorted(required_names - child_names)
            unexpected = sorted(child_names - required_names)
            details: list[str] = []
            if missing:
                details.append("missing " + ", ".join(missing))
            if unexpected:
                details.append("unexpected " + ", ".join(unexpected))
            raise ArchiveBlockLoadError(
                "Archive Block must contain exactly manifest.json and content/"
                + (": " + "; ".join(details) if details else "")
            )

        manifest_path = block_path / "manifest.json"
        if not manifest_path.is_file():
            raise ArchiveBlockLoadError(
                "Archive Block manifest.json must be a regular file."
            )

        content_dir = block_path / "content"
        if not content_dir.is_dir():
            raise ArchiveBlockLoadError(
                "Archive Block content must be a regular directory."
            )

        content_children = tuple(content_dir.iterdir())
        if not content_children:
            raise ArchiveBlockLoadError(
                "Archive Block content must contain at least one JSON entry."
            )
        for child in content_children:
            if child.is_symlink():
                raise ArchiveBlockLoadError(
                    "Symbolic links are not allowed inside Archive Block content: "
                    f"{child.name}"
                )
            if child.is_dir():
                raise ArchiveBlockLoadError(
                    "Nested directories are not allowed inside Archive Block content: "
                    f"{child.name}"
                )
            if not child.is_file():
                raise ArchiveBlockLoadError(
                    f"Archive Block content entry must be a regular file: {child.name}"
                )
            if child.suffix != ".json":
                raise ArchiveBlockLoadError(
                    f"Archive Block content accepts only .json files: {child.name}"
                )
    except ArchiveBlockLoadError:
        raise
    except OSError as error:
        raise ArchiveBlockLoadError(
            f"Archive Block structure could not be inspected: {block_path}: {error}"
        ) from error


def _read_json_object(path: Path, label: str) -> dict[str, Any]:
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as error:
        raise ArchiveBlockLoadError(
            f"Archive Block {label} could not be read as UTF-8 JSON: {path}: {error}"
        ) from error
    try:
        data = json.loads(text, object_pairs_hook=_unique_json_object)
    except (json.JSONDecodeError, ValueError) as error:
        raise ArchiveBlockLoadError(
            f"Archive Block {label} is not valid strict JSON: {path}: {error}"
        ) from error
    if not isinstance(data, dict):
        raise ArchiveBlockLoadError(
            f"Archive Block {label} must contain a top-level JSON object: {path}"
        )
    return data


def _unique_json_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def _validate_manifest(manifest: dict[str, Any]) -> None:
    fields = frozenset(manifest)
    if fields != _MANIFEST_FIELDS:
        _raise_field_error("manifest", fields, _MANIFEST_FIELDS, _MANIFEST_FIELDS)

    expected_strings = {
        "format": ARCHIVE_BLOCK_FORMAT,
        "block_type": ARCHIVE_BLOCK_TYPE,
        "target_module": ARCHIVE_TARGET_MODULE,
        "target_chamber": ARCHIVE_TARGET_CHAMBER,
    }
    for field, expected in expected_strings.items():
        if manifest[field] != expected:
            raise ArchiveBlockLoadError(
                f"Archive Block manifest {field} must equal {expected!r}."
            )

    if type(manifest["schema_version"]) is not int:
        raise ArchiveBlockLoadError(
            "Archive Block manifest schema_version must be the integer 1."
        )
    if manifest["schema_version"] != ARCHIVE_SCHEMA_VERSION:
        raise ArchiveBlockLoadError(
            "Archive Block manifest uses an unsupported schema_version: "
            f"{manifest['schema_version']!r}"
        )

    _validate_identifier(manifest["block_id"], "manifest block_id")
    _validate_display_text(manifest["title"], "manifest title")


def _parse_entry(data: dict[str, Any], filename: str) -> ArchiveEntry:
    for required in ("entry_id", "title", "access"):
        if required not in data:
            raise ArchiveBlockLoadError(
                f"Archive entry {filename} is missing required field: {required}"
            )

    access = data["access"]
    if not isinstance(access, str) or access not in {"open", "sealed"}:
        raise ArchiveBlockLoadError(
            f"Archive entry {filename} access must be 'open' or 'sealed'."
        )

    fields = frozenset(data)
    if access == "open":
        _raise_field_error(
            f"entry {filename}",
            fields,
            _OPEN_ENTRY_REQUIRED_FIELDS,
            _OPEN_ENTRY_ALLOWED_FIELDS,
        )
    else:
        _raise_field_error(
            f"entry {filename}",
            fields,
            _SEALED_ENTRY_REQUIRED_FIELDS,
            _SEALED_ENTRY_ALLOWED_FIELDS,
        )

    _validate_identifier(data["entry_id"], f"entry {filename} entry_id")
    _validate_display_text(data["title"], f"entry {filename} title")

    poetic = _optional_text_tuple(data, "poetic_indication", filename)
    clear = _optional_text_tuple(data, "clear_orientation", filename)
    deeper = _optional_text_tuple(data, "deeper_trace", filename)

    if access == "open":
        if not poetic:
            raise ArchiveBlockLoadError(
                f"Open Archive entry {filename} requires poetic_indication."
            )
        if not clear:
            raise ArchiveBlockLoadError(
                f"Open Archive entry {filename} requires clear_orientation."
            )

    return ArchiveEntry(
        entry_id=data["entry_id"],
        title=data["title"],
        access=access,
        poetic_indication=poetic,
        clear_orientation=clear,
        deeper_trace=deeper,
    )


def _raise_field_error(
    label: str,
    fields: frozenset[str],
    required: frozenset[str],
    allowed: frozenset[str],
) -> None:
    missing = sorted(required - fields)
    unknown = sorted(fields - allowed)
    if not missing and not unknown:
        return
    details: list[str] = []
    if missing:
        details.append("missing " + ", ".join(missing))
    if unknown:
        details.append("unknown " + ", ".join(unknown))
    raise ArchiveBlockLoadError(
        f"Archive Block {label} has invalid fields: " + "; ".join(details)
    )


def _validate_identifier(value: Any, label: str) -> None:
    if not isinstance(value, str) or _IDENTIFIER_PATTERN.fullmatch(value) is None:
        raise ArchiveBlockLoadError(
            f"Archive Block {label} must be a 1-80 character public-safe ASCII "
            "identifier beginning with a letter or digit."
        )


def _validate_display_text(value: Any, label: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ArchiveBlockLoadError(
            f"Archive Block {label} must be a non-empty UTF-8 string."
        )


def _optional_text_tuple(
    data: dict[str, Any],
    field: str,
    filename: str,
) -> tuple[str, ...]:
    if field not in data:
        return ()
    value = data[field]
    if not isinstance(value, list) or not value:
        raise ArchiveBlockLoadError(
            f"Archive entry {filename} {field} must be a non-empty array of text strings."
        )
    for item in value:
        if not isinstance(item, str) or not item.strip():
            raise ArchiveBlockLoadError(
                f"Archive entry {filename} {field} must contain only non-empty text strings."
            )
    return tuple(value)
