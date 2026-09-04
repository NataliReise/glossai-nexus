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
    ARCHIVE_BUILTIN_ROOT,
    ARCHIVE_COUPLED_ROOT,
    ArchiveBlockLoadError,
    ArchiveContentBlock,
    load_archive_block,
    load_archive_constellation,
)


BUILTIN_ARCHIVE_ROOT = ARCHIVE_BUILTIN_ROOT
COUPLED_ARCHIVE_ROOT = ARCHIVE_COUPLED_ROOT
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

    try:
        archive = load_archive_constellation(
            root / BUILTIN_ARCHIVE_ROOT,
            root / COUPLED_ARCHIVE_ROOT,
        )
    except ArchiveBlockLoadError as error:
        raise NexusBuilderError(
            f"Nexus Archive constellation inspection failed: {error}"
        ) from error

    return NexusConstellation(
        nexus_root=root,
        builtin_blocks=archive.builtin_blocks,
        coupled_blocks=archive.coupled_blocks,
    )


def verify_nexus_constellation(
    nexus_root: str | Path = NEXUS_ROOT,
) -> NexusConstellation:
    """Validate the current local constellation without changing the Nexus."""

    return inspect_nexus(nexus_root)
