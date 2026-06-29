"""Matching logic for Nexus 01 Return Resonance."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from .artifact import ReturnArtifact
from .slots import ReturnSlot, ReturnSlotState


class MatchStatus(StrEnum):
    """Possible results of matching an artifact to local return slots."""

    MATCH_WAITING = "match_waiting"
    MATCH_OPENED = "match_opened"
    UNKNOWN_SLOT = "unknown_slot"
    PACKAGE_MISMATCH = "package_mismatch"
    LAYER_MISMATCH = "layer_mismatch"


@dataclass(frozen=True)
class MatchResult:
    """Result of matching a return artifact against known local slots."""

    status: MatchStatus
    message: str
    slot: ReturnSlot | None = None

    @property
    def is_match(self) -> bool:
        """Return True if the artifact belongs to a known slot."""

        return self.status in {MatchStatus.MATCH_WAITING, MatchStatus.MATCH_OPENED}


def match_return_artifact(
    artifact: ReturnArtifact,
    slots: list[ReturnSlot],
) -> MatchResult:
    """Match a return artifact against local return slots."""

    slot = _find_slot(artifact, slots)
    if slot is None:
        return MatchResult(
            status=MatchStatus.UNKNOWN_SLOT,
            message="This return does not seem to belong to a waiting slot in this Nexus.",
        )

    if artifact.package_id != slot.package_id:
        return MatchResult(
            status=MatchStatus.PACKAGE_MISMATCH,
            message="This return artifact does not match the package for this slot.",
            slot=slot,
        )

    if artifact.layer_id != slot.layer_id:
        return MatchResult(
            status=MatchStatus.LAYER_MISMATCH,
            message="This return artifact does not match the layer for this slot.",
            slot=slot,
        )

    if slot.status == ReturnSlotState.OPENED:
        return MatchResult(
            status=MatchStatus.MATCH_OPENED,
            message="This return layer has already opened. The Nexus remembers what returned.",
            slot=slot,
        )

    return MatchResult(
        status=MatchStatus.MATCH_WAITING,
        message="The returned artifact fits. A deeper layer of this Nexus becomes readable.",
        slot=slot,
    )


def _find_slot(artifact: ReturnArtifact, slots: list[ReturnSlot]) -> ReturnSlot | None:
    for slot in slots:
        if (
            artifact.origin_trace_id == slot.origin_trace_id
            and artifact.return_slot_id == slot.return_slot_id
        ):
            return slot
    return None
