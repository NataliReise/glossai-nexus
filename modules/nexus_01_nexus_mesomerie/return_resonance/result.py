"""Local result generation for Nexus 01 Return Resonance."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .artifact import ReturnArtifact
from .matching import MatchResult, MatchStatus


class ReturnResultError(ValueError):
    """Raised when a return result cannot be created or read."""


@dataclass(frozen=True)
class ReturnResult:
    """A local return resonance result."""

    path: Path
    content: str
    created: bool


def open_return_result(
    artifact: ReturnArtifact,
    match: MatchResult,
    output_dir: str | Path,
) -> ReturnResult:
    """Create or read the local result for a matched return artifact.

    This function implements the first MVP rule:

    Generate once. Revisit often.
    """

    if match.status not in {MatchStatus.MATCH_WAITING, MatchStatus.MATCH_OPENED}:
        raise ReturnResultError("Cannot open a return result without a matching slot.")

    if match.slot is None:
        raise ReturnResultError("Cannot open a return result without slot data.")

    output_path = Path(output_dir) / match.slot.result_file

    if output_path.exists():
        return ReturnResult(
            path=output_path,
            content=output_path.read_text(encoding="utf-8"),
            created=False,
        )

    if match.status == MatchStatus.MATCH_OPENED:
        raise ReturnResultError(
            "This return layer is marked as opened, but the local result file was not found."
        )

    content = compose_return_result(artifact, match)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(content, encoding="utf-8")

    return ReturnResult(path=output_path, content=content, created=True)


def compose_return_result(artifact: ReturnArtifact, match: MatchResult) -> str:
    """Compose a stable local Markdown result for a matched artifact."""

    if match.slot is None:
        raise ReturnResultError("Cannot compose a return result without slot data.")

    origin_image = match.slot.public_safe_label or match.slot.return_slot_id
    returned_image = artifact.return_image or "returned trace"
    return_word = artifact.return_word or "return"
    return_tone = artifact.return_tone or "quiet"
    carrier_image = artifact.carrier_image or "carrier"
    carrier_movement = artifact.carrier_movement or "returns"

    resonance_lines = [
        _title_word(carrier_image),
        f"{return_tone} {returned_image}",
        f"{return_word} {carrier_movement}",
        "a spark remembers home",
        "Resonance",
    ]

    return "\n".join(
        [
            f"# Return Resonance: {match.slot.return_slot_id}",
            "",
            "Status: opened",
            f"Module: {match.slot.module_id}",
            f"Layer: {match.slot.layer_id}",
            f"Origin trace: {match.slot.origin_trace_id}",
            "",
            "---",
            "",
            "## Return status",
            "",
            "The returned artifact fits.",
            "",
            "A deeper layer of this Nexus becomes readable.",
            "",
            "No public trace has been created by this local result.",
            "",
            "---",
            "",
            "## Origin and return",
            "",
            "Origin image:",
            "",
            "```text",
            origin_image,
            "```",
            "",
            "Returned image:",
            "",
            "```text",
            returned_image,
            "```",
            "",
            "Return word:",
            "",
            "```text",
            return_word,
            "```",
            "",
            "---",
            "",
            "## Generated resonance",
            "",
            "```text",
            *resonance_lines,
            "```",
            "",
            "---",
            "",
            "## Public-safe witness phrase",
            "",
            "```text",
            f"The {carrier_image} answered through the {origin_image}.",
            "```",
            "",
            "---",
            "",
            "## Privacy reminder",
            "",
            "This is a local return resonance result.",
            "",
            "Do not publish it unless you have reviewed it carefully and intentionally made it public-safe.",
            "",
        ]
    )


def _title_word(value: str) -> str:
    value = value.strip()
    if not value:
        return "Return"
    return value[0].upper() + value[1:]
