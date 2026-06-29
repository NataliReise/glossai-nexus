"""Parsing for Nexus 01 return artifacts."""

from __future__ import annotations

from dataclasses import dataclass


class ReturnArtifactParseError(ValueError):
    """Raised when a return artifact text is incomplete or malformed."""


@dataclass(frozen=True)
class ReturnArtifact:
    """Structured public-safe representation of a return artifact.

    The object may contain situated meaning, but it should not be treated as
    public-safe unless it was created from explicit demo data or reviewed by a
    human.
    """

    version: str
    module: str
    origin_trace_id: str
    return_slot_id: str
    package_id: str
    layer_id: str
    carrier_image: str = ""
    carrier_movement: str = ""
    return_word: str = ""
    return_image: str = ""
    return_tone: str = ""


_HEADER_FIELDS = {
    "Version": "version",
    "Module": "module",
    "Origin Trace": "origin_trace_id",
    "Return Slot": "return_slot_id",
    "Package": "package_id",
    "Layer": "layer_id",
}

_BLOCK_FIELDS = {
    "Carrier image": "carrier_image",
    "Carrier movement": "carrier_movement",
    "Return word": "return_word",
    "Return image": "return_image",
    "Return tone": "return_tone",
}

_REQUIRED_FIELDS = (
    "version",
    "module",
    "origin_trace_id",
    "return_slot_id",
    "package_id",
    "layer_id",
)


def parse_return_artifact(text: str) -> ReturnArtifact:
    """Parse a structured text return artifact.

    The first MVP format is intentionally human-readable. Header fields use
    ``Name: value`` lines. Small block fields use a label line ending in ``:``
    followed by one or more text lines.
    """

    if not text or not text.strip():
        raise ReturnArtifactParseError("Return artifact is empty.")

    lines = text.splitlines()
    if not any(line.strip() == "NEXUS RETURN ARTIFACT" for line in lines):
        raise ReturnArtifactParseError("Return artifact header is missing.")

    values: dict[str, str] = {}
    current_block: str | None = None
    block_lines: list[str] = []

    def flush_block() -> None:
        nonlocal current_block, block_lines
        if current_block is not None:
            values[current_block] = "\n".join(line.rstrip() for line in block_lines).strip()
        current_block = None
        block_lines = []

    for raw_line in lines:
        line = raw_line.strip()

        if line == "NEXUS RETURN ARTIFACT":
            continue

        if not line:
            if current_block is not None:
                block_lines.append("")
            continue

        if line.endswith(":"):
            label = line[:-1]
            if label in _BLOCK_FIELDS:
                flush_block()
                current_block = _BLOCK_FIELDS[label]
                continue
            flush_block()
            continue

        matched_header = False
        for label, field_name in _HEADER_FIELDS.items():
            prefix = f"{label}:"
            if line.startswith(prefix):
                flush_block()
                values[field_name] = line[len(prefix) :].strip()
                matched_header = True
                break

        if matched_header:
            continue

        if current_block is not None:
            block_lines.append(raw_line)

    flush_block()

    missing = [field for field in _REQUIRED_FIELDS if not values.get(field)]
    if missing:
        raise ReturnArtifactParseError(
            "Return artifact is missing required field(s): " + ", ".join(missing)
        )

    return ReturnArtifact(
        version=values["version"],
        module=values["module"],
        origin_trace_id=values["origin_trace_id"],
        return_slot_id=values["return_slot_id"],
        package_id=values["package_id"],
        layer_id=values["layer_id"],
        carrier_image=values.get("carrier_image", ""),
        carrier_movement=values.get("carrier_movement", ""),
        return_word=values.get("return_word", ""),
        return_image=values.get("return_image", ""),
        return_tone=values.get("return_tone", ""),
    )
