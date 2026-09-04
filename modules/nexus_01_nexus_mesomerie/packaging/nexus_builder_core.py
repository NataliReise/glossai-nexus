"""Safe reusable core operations for the local Nexus 01 Builder."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import sys


SCRIPT_PATH = Path(__file__).resolve()
NEXUS_ROOT = SCRIPT_PATH.parents[1]
if str(NEXUS_ROOT) not in sys.path:
    sys.path.insert(0, str(NEXUS_ROOT))

from chambers.resonance.archive_content import (  # noqa: E402
    ArchiveBlockLoadError,
    ArchiveContentBlock,
    load_archive_block,
)


BUILTIN_ARCHIVE_ROOT = Path("chambers/resonance/archive_blocks/builtin")
COUPLED_ARCHIVE_ROOT = Path("chambers/resonance/archive_blocks/coupled")
_REQUIRED_NEXUS_FILES = (
    Path("run_nexus.py"),
    Path("chambers/resonance/archive_content.py"),
)


class NexusBuilderError(RuntimeError):
    """Raised when Builder inspection cannot establish a safe valid state."""


@dataclass(frozen=True)
class NexusConstellation:
    """Validated read-only view of Archive Blocks currently carried by a Nexus."""

    nexus_root: Path
    builtin_blocks: tuple[ArchiveContentBlock, ...]
    coupled_blocks: tuple[ArchiveContentBlock, ...]

    @property
    def block_ids(self) -> tuple[str, ...]:
        return tuple(
            block.block_id
            for block in (*self.builtin_blocks, *self.coupled_blocks)
        )


def inspect_archive_block(path: str | Path) -> ArchiveContentBlock:
    """Validate and return one explicitly selected data-only Archive Block."""

    selected = Path(path).expanduser()
    try:
        return load_archive_block(selected)
    except ArchiveBlockLoadError as error:
        raise NexusBuilderError(
            f"Archive Block inspection failed: {error}"
        ) from error


def inspect_nexus(nexus_root: str | Path = NEXUS_ROOT) -> NexusConstellation:
    """Inspect only explicit Nexus 01 Archive roots and validate the constellation."""

    root = Path(nexus_root).expanduser().resolve()
    if not root.is_dir():
        raise NexusBuilderError(f"Nexus root is not a directory: {root}")

    for relative in _REQUIRED_NEXUS_FILES:
        required = root / relative
        if required.is_symlink() or not required.is_file():
            raise NexusBuilderError(
                f"Nexus root is missing required regular file: {relative}"
            )

    builtin = _load_block_root(root / BUILTIN_ARCHIVE_ROOT, required=True)
    coupled = _load_block_root(root / COUPLED_ARCHIVE_ROOT, required=False)

    seen: set[str] = set()
    for block in (*builtin, *coupled):
        if block.block_id in seen:
            raise NexusBuilderError(
                "Nexus Archive constellation contains duplicate block_id: "
                f"{block.block_id}"
            )
        seen.add(block.block_id)

    return NexusConstellation(
        nexus_root=root,
        builtin_blocks=builtin,
        coupled_blocks=coupled,
    )


def verify_nexus_constellation(
    nexus_root: str | Path = NEXUS_ROOT,
) -> NexusConstellation:
    """Validate the current local constellation without changing the Nexus."""

    return inspect_nexus(nexus_root)


def _load_block_root(
    block_root: Path,
    *,
    required: bool,
) -> tuple[ArchiveContentBlock, ...]:
    if block_root.is_symlink():
        raise NexusBuilderError(
            f"Archive Block root must not be a symbolic link: {block_root}"
        )
    if not block_root.exists():
        if required:
            raise NexusBuilderError(
                f"Required Archive Block root is missing: {block_root}"
            )
        return ()
    if not block_root.is_dir():
        raise NexusBuilderError(
            f"Archive Block root is not a directory: {block_root}"
        )

    try:
        children = tuple(sorted(block_root.iterdir(), key=lambda path: path.name))
    except OSError as error:
        raise NexusBuilderError(
            f"Archive Block root could not be inspected: {block_root}: {error}"
        ) from error

    if required and not children:
        raise NexusBuilderError(
            f"Required Archive Block root contains no Blocks: {block_root}"
        )

    blocks: list[ArchiveContentBlock] = []
    for child in children:
        if child.is_symlink():
            raise NexusBuilderError(
                f"Archive Block root contains a symbolic link: {child}"
            )
        if not child.is_dir():
            raise NexusBuilderError(
                f"Archive Block root may contain only Block directories: {child}"
            )
        blocks.append(inspect_archive_block(child))

    return tuple(sorted(blocks, key=lambda block: block.block_id))
