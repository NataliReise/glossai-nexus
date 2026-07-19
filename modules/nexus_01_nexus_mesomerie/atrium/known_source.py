"""Safe raw-byte boundary for an explicitly known local source path."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
import errno
import os
from pathlib import Path
import stat


class KnownSourceReadStatus(Enum):
    AVAILABLE = "available"
    MISSING = "missing"
    SYMLINK = "symlink"
    NOT_REGULAR = "not-regular"
    UNAVAILABLE = "unavailable"
    TOO_LARGE = "too-large"


@dataclass(frozen=True, slots=True)
class KnownSourceReadResult:
    status: KnownSourceReadStatus
    content: bytes | None = None

    def __post_init__(self) -> None:
        if self.status is KnownSourceReadStatus.AVAILABLE:
            if not isinstance(self.content, bytes):
                raise ValueError("available known-source result requires bytes")
            return
        if self.content is not None:
            raise ValueError("unavailable known-source result cannot contain bytes")


def read_known_source_bytes(
    path: Path,
    *,
    max_bytes: int,
) -> KnownSourceReadResult:
    """Read bounded bytes from one exact absolute path without following links."""

    if not path.is_absolute():
        raise ValueError("known-source path must be absolute")
    if max_bytes <= 0:
        raise ValueError("known-source byte limit must be positive")

    flags = os.O_RDONLY | os.O_CLOEXEC | os.O_NOFOLLOW | os.O_NONBLOCK
    try:
        descriptor = os.open(path, flags)
    except OSError as error:
        return _open_error_result(error)

    result = KnownSourceReadResult(KnownSourceReadStatus.UNAVAILABLE)
    try:
        metadata = os.fstat(descriptor)
        if not stat.S_ISREG(metadata.st_mode):
            result = KnownSourceReadResult(KnownSourceReadStatus.NOT_REGULAR)
        else:
            result = _read_bounded(descriptor, max_bytes=max_bytes)
    except OSError:
        result = KnownSourceReadResult(KnownSourceReadStatus.UNAVAILABLE)
    finally:
        try:
            os.close(descriptor)
        except OSError:
            result = KnownSourceReadResult(KnownSourceReadStatus.UNAVAILABLE)
    return result


def _open_error_result(error: OSError) -> KnownSourceReadResult:
    if error.errno == errno.ENOENT:
        status = KnownSourceReadStatus.MISSING
    elif error.errno == errno.ELOOP:
        status = KnownSourceReadStatus.SYMLINK
    else:
        status = KnownSourceReadStatus.UNAVAILABLE
    return KnownSourceReadResult(status)


def _read_bounded(descriptor: int, *, max_bytes: int) -> KnownSourceReadResult:
    chunks: list[bytes] = []
    bytes_read = 0
    boundary = max_bytes + 1
    while bytes_read < boundary:
        chunk = os.read(descriptor, min(64 * 1024, boundary - bytes_read))
        if not chunk:
            break
        chunks.append(chunk)
        bytes_read += len(chunk)
    if bytes_read > max_bytes:
        return KnownSourceReadResult(KnownSourceReadStatus.TOO_LARGE)
    return KnownSourceReadResult(
        KnownSourceReadStatus.AVAILABLE,
        b"".join(chunks),
    )
