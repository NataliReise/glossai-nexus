"""Read one explicitly known canonical stable Resonance result."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
import json
from pathlib import Path
import re

from .known_source import KnownSourceReadStatus, read_known_source_bytes


STABLE_RESULT_MAX_BYTES = 1024 * 1024


class StableResultReadStatus(Enum):
    AVAILABLE = "available"
    MISSING = "missing"
    SYMLINK = "symlink"
    NOT_REGULAR = "not-regular"
    UNAVAILABLE = "unavailable"
    TOO_LARGE = "too-large"
    INVALID_UTF8 = "invalid-utf8"
    INVALID_FORMAT = "invalid-format"


@dataclass(frozen=True, slots=True)
class StableResonanceView:
    lines: tuple[str, str, str, str, str]

    def __post_init__(self) -> None:
        if len(self.lines) != 5 or any(
            not isinstance(line, str)
            or not line
            or "\n" in line
            or "\r" in line
            for line in self.lines
        ):
            raise ValueError("stable Resonance view requires five non-empty lines")


@dataclass(frozen=True, slots=True)
class StableResultReadResult:
    status: StableResultReadStatus
    view: StableResonanceView | None = None

    def __post_init__(self) -> None:
        if self.status is StableResultReadStatus.AVAILABLE:
            if not isinstance(self.view, StableResonanceView):
                raise ValueError("available stable result requires a view")
            return
        if self.view is not None:
            raise ValueError("unavailable stable result cannot contain a view")


_TRACE_START = "<!-- nexus-01-result-trace-start -->"
_TRACE_END = "<!-- nexus-01-result-trace-end -->"
_DOCUMENT_PATTERN = re.compile(
    r"\A# Resonance Return\n\n"
    r"## Compact Resonance\n\n"
    r"```text\n"
    r"(?P<line_1>[^\r\n]+)\n"
    r"(?P<line_2>[^\r\n]+)\n"
    r"(?P<line_3>[^\r\n]+)\n"
    r"(?P<line_4>[^\r\n]+)\n"
    r"(?P<line_5>[^\r\n]+)\n"
    r"```\n\n"
    r"<!-- nexus-01-result-trace-start -->\n"
    r"<details>\n"
    r"<summary>Technical trace</summary>\n\n"
    r"```json\n"
    r"(?P<trace>\{.*\})\n"
    r"```\n\n"
    r"</details>\n"
    r"<!-- nexus-01-result-trace-end -->\n\n"
    r"---\n\n"
    r"This result remains local unless you deliberately transfer it\.\n\Z",
    re.DOTALL,
)

_BOUNDARY_STATUS_MAP = {
    KnownSourceReadStatus.MISSING: StableResultReadStatus.MISSING,
    KnownSourceReadStatus.SYMLINK: StableResultReadStatus.SYMLINK,
    KnownSourceReadStatus.NOT_REGULAR: StableResultReadStatus.NOT_REGULAR,
    KnownSourceReadStatus.UNAVAILABLE: StableResultReadStatus.UNAVAILABLE,
    KnownSourceReadStatus.TOO_LARGE: StableResultReadStatus.TOO_LARGE,
}


def read_stable_resonance_result(path: Path) -> StableResultReadResult:
    """Read and strictly parse one canonical stable-result Markdown file."""

    source = read_known_source_bytes(path, max_bytes=STABLE_RESULT_MAX_BYTES)
    if source.status is not KnownSourceReadStatus.AVAILABLE:
        return StableResultReadResult(_BOUNDARY_STATUS_MAP[source.status])

    assert source.content is not None
    try:
        document = source.content.decode("utf-8", errors="strict")
    except UnicodeDecodeError:
        return StableResultReadResult(StableResultReadStatus.INVALID_UTF8)
    return _parse_stable_result(document)


def _parse_stable_result(document: str) -> StableResultReadResult:
    if document.count(_TRACE_START) != 1 or document.count(_TRACE_END) != 1:
        return StableResultReadResult(StableResultReadStatus.INVALID_FORMAT)
    match = _DOCUMENT_PATTERN.fullmatch(document)
    if match is None:
        return StableResultReadResult(StableResultReadStatus.INVALID_FORMAT)
    try:
        trace = json.loads(match.group("trace"))
    except json.JSONDecodeError:
        return StableResultReadResult(StableResultReadStatus.INVALID_FORMAT)
    if not isinstance(trace, dict):
        return StableResultReadResult(StableResultReadStatus.INVALID_FORMAT)

    return StableResultReadResult(
        StableResultReadStatus.AVAILABLE,
        StableResonanceView(
            (
                match.group("line_1"),
                match.group("line_2"),
                match.group("line_3"),
                match.group("line_4"),
                match.group("line_5"),
            )
        ),
    )
