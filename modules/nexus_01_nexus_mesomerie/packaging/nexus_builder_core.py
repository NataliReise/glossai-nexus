"""Safe reusable core operations for the local Nexus 01 Builder."""

from __future__ import annotations

from dataclasses import dataclass
import os
from pathlib import Path
import shutil
import sys
import tempfile


SCRIPT_PATH = Path(__file__).resolve()
NEXUS_ROOT = SCRIPT_PATH.parents[1]
if str(NEXUS_ROOT) not in sys.path:
    sys.path.insert(0, str(NEXUS_ROOT))

from chambers.resonance.archive_content import (  # noqa: E402
    ARCHIVE_BUILTIN_ROOT,
    ARCHIVE_COUPLED_ROOT,
    ArchiveBlockLoadError,
    ArchiveContentBlock,
    build_archive_constellation,
    load_archive_block,
    load_archive_constellation,
)


BUILTIN_ARCHIVE_ROOT = ARCHIVE_BUILTIN_ROOT
COUPLED_ARCHIVE_ROOT = ARCHIVE_COUPLED_ROOT
_REQUIRED_NEXUS_FILES = (
    Path("run_nexus.py"),
    Path("chambers/resonance/archive_content.py"),
)
_COUPLING_REQUIRED_NEXUS_FILES = (
    Path("atrium/classified_resonance.py"),
)
_COUPLING_DIRECTORY_BOUNDARY = (
    Path("chambers"),
    Path("chambers/resonance"),
    Path("chambers/resonance/archive_blocks"),
    BUILTIN_ARCHIVE_ROOT,
)
_REFERENCE_ARCHIVE_BLOCK_ID = "n01-resonance-archive-origin"
_STAGE_PREFIX = ".nexus-builder-stage-"


class NexusBuilderError(RuntimeError):
    """Raised when a Builder operation cannot complete safely."""


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


@dataclass(frozen=True)
class CouplingResult:
    """One successfully coupled public-safe Archive Block."""

    block: ArchiveContentBlock
    destination: Path
    constellation: NexusConstellation


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


def couple_archive_block(
    block_path: str | Path,
    *,
    nexus_root: str | Path = NEXUS_ROOT,
) -> CouplingResult:
    """Deliberately couple one validated Archive Block into one explicit Nexus."""

    source_path = Path(block_path).expanduser()
    source_block = inspect_archive_block(source_path)
    root, current = _inspect_coupling_target(nexus_root)
    _prospective_archive_constellation(current, source_block)

    archive_parent = root / COUPLED_ARCHIVE_ROOT.parent
    coupled_root = root / COUPLED_ARCHIVE_ROOT
    final_block = coupled_root / source_block.block_id
    if final_block.exists() or final_block.is_symlink():
        raise NexusBuilderError(
            f"Refusing to overwrite existing coupled Block path: {final_block}"
        )

    try:
        stage_root = Path(
            tempfile.mkdtemp(
                prefix=_STAGE_PREFIX,
                dir=archive_parent,
            )
        )
    except OSError as error:
        raise NexusBuilderError(
            f"Could not create a local Builder staging directory: {error}"
        ) from error

    staged_block_path = stage_root / source_block.block_id
    created_coupled_root = False
    reserved_final = False
    published = False

    try:
        shutil.copytree(
            source_path,
            staged_block_path,
            symlinks=True,
            copy_function=shutil.copy2,
        )
        staged_block = inspect_archive_block(staged_block_path)
        if staged_block != source_block:
            raise NexusBuilderError(
                "Staged Archive Block does not match the validated source Block."
            )

        current_before_publish = inspect_nexus(root)
        _prospective_archive_constellation(
            current_before_publish,
            staged_block,
        )

        if not coupled_root.exists():
            try:
                coupled_root.mkdir()
                created_coupled_root = True
            except FileExistsError:
                pass

        if coupled_root.is_symlink() or not coupled_root.is_dir():
            raise NexusBuilderError(
                f"Coupled Archive root is not a safe regular directory: {coupled_root}"
            )

        try:
            final_block.mkdir()
            reserved_final = True
        except FileExistsError as error:
            raise NexusBuilderError(
                f"Refusing to overwrite existing coupled Block path: {final_block}"
            ) from error

        try:
            os.rename(staged_block_path, final_block)
        except OSError as error:
            raise NexusBuilderError(
                f"Could not publish the staged Archive Block safely: {error}"
            ) from error
        reserved_final = False
        published = True

        constellation = _verify_published_block(
            root,
            staged_block.block_id,
        )
        return CouplingResult(
            block=staged_block,
            destination=final_block,
            constellation=constellation,
        )
    except Exception as error:
        rollback_error = _rollback_coupling(
            final_block=final_block,
            coupled_root=coupled_root,
            created_coupled_root=created_coupled_root,
            reserved_final=reserved_final,
            published=published,
        )
        if rollback_error is not None:
            raise NexusBuilderError(
                "Archive Block coupling failed and rollback also failed: "
                f"{rollback_error}"
            ) from error
        if isinstance(error, NexusBuilderError):
            raise
        raise NexusBuilderError(
            f"Archive Block coupling failed safely: {error}"
        ) from error
    finally:
        shutil.rmtree(stage_root, ignore_errors=True)


def _inspect_coupling_target(
    nexus_root: str | Path,
) -> tuple[Path, NexusConstellation]:
    raw_root = Path(nexus_root).expanduser()
    if raw_root.is_symlink():
        raise NexusBuilderError(
            f"Coupling target Nexus root must not be a symbolic link: {raw_root}"
        )

    root = raw_root.resolve()
    constellation = inspect_nexus(root)

    for relative in _COUPLING_REQUIRED_NEXUS_FILES:
        required = root / relative
        if required.is_symlink() or not required.is_file():
            raise NexusBuilderError(
                "Coupling target is missing required Archive-capable runtime file: "
                f"{relative}"
            )

    for relative in _COUPLING_DIRECTORY_BOUNDARY:
        directory = root / relative
        if directory.is_symlink() or not directory.is_dir():
            raise NexusBuilderError(
                "Coupling target contains an unsafe Archive directory boundary: "
                f"{relative}"
            )

    builtin_ids = {block.block_id for block in constellation.builtin_blocks}
    if _REFERENCE_ARCHIVE_BLOCK_ID not in builtin_ids:
        raise NexusBuilderError(
            "Coupling target does not contain the required Nexus 01 "
            f"reference Archive Block: {_REFERENCE_ARCHIVE_BLOCK_ID}"
        )

    return root, constellation


def _prospective_archive_constellation(
    current: NexusConstellation,
    candidate: ArchiveContentBlock,
) -> None:
    try:
        build_archive_constellation(
            builtin_blocks=current.builtin_blocks,
            coupled_blocks=(*current.coupled_blocks, candidate),
        )
    except ArchiveBlockLoadError as error:
        raise NexusBuilderError(
            "Archive Block is incompatible with the current constellation: "
            f"{error}"
        ) from error


def _verify_published_block(
    nexus_root: Path,
    block_id: str,
) -> NexusConstellation:
    constellation = inspect_nexus(nexus_root)
    if block_id not in {
        block.block_id for block in constellation.coupled_blocks
    }:
        raise NexusBuilderError(
            f"Published Archive Block is missing from the verified constellation: {block_id}"
        )
    return constellation


def _rollback_coupling(
    *,
    final_block: Path,
    coupled_root: Path,
    created_coupled_root: bool,
    reserved_final: bool,
    published: bool,
) -> OSError | None:
    try:
        if published and final_block.exists():
            shutil.rmtree(final_block)
        elif reserved_final and final_block.exists():
            final_block.rmdir()

        if created_coupled_root and coupled_root.exists():
            try:
                coupled_root.rmdir()
            except OSError:
                # Another valid entry may now exist; never remove a non-empty root.
                pass
    except OSError as error:
        return error
    return None
