"""Minimal descriptive state model for the Nexus 01 Atrium.

This module does not render terminal text and does not dispatch Chambers.
It only records which paths belong to the current activation and which of
those paths have already been completed.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from enum import Enum


FIRST_SPARK_CHAMBER = "first-spark"
RESONANCE_CHAMBER = "resonance"
KNOWN_CHAMBERS = frozenset({FIRST_SPARK_CHAMBER, RESONANCE_CHAMBER})


class AtriumStateError(ValueError):
    """Raised when an Atrium state would contradict the Nexus structure."""


class AtriumPhase(str, Enum):
    """Player-facing phase of the one Nexus Atrium."""

    SEALED = "sealed"
    ARRIVAL = "arrival"
    RETURN = "return"


@dataclass(frozen=True)
class AtriumState:
    """Describe visible Nexus paths without owning Chamber mechanics.

    ``enabled_chambers`` comes from a validated activation profile.
    ``completed_chambers`` records only local progress in this Nexus run.
    A completed path may remain visible even when it is no longer offered as
    the next unfinished path.
    """

    phase: AtriumPhase
    enabled_chambers: frozenset[str] = frozenset()
    completed_chambers: frozenset[str] = frozenset()

    def __post_init__(self) -> None:
        unknown_enabled = self.enabled_chambers - KNOWN_CHAMBERS
        if unknown_enabled:
            raise AtriumStateError(
                "Atrium state contains unknown enabled Chamber(s): "
                + ", ".join(sorted(unknown_enabled))
            )

        unknown_completed = self.completed_chambers - KNOWN_CHAMBERS
        if unknown_completed:
            raise AtriumStateError(
                "Atrium state contains unknown completed Chamber(s): "
                + ", ".join(sorted(unknown_completed))
            )

        not_enabled = self.completed_chambers - self.enabled_chambers
        if not_enabled:
            raise AtriumStateError(
                "A Chamber cannot be completed unless it is enabled: "
                + ", ".join(sorted(not_enabled))
            )

        if self.phase is AtriumPhase.SEALED:
            if self.enabled_chambers or self.completed_chambers:
                raise AtriumStateError(
                    "A sealed Atrium cannot expose enabled or completed Chambers."
                )
        elif not self.enabled_chambers:
            raise AtriumStateError(
                "An activated Atrium must contain at least one enabled Chamber."
            )

        if self.phase is AtriumPhase.ARRIVAL and self.completed_chambers:
            raise AtriumStateError(
                "The arrival phase cannot already contain completed Chambers."
            )

        if self.phase is AtriumPhase.RETURN and not self.completed_chambers:
            raise AtriumStateError(
                "The return phase requires at least one completed Chamber."
            )

    @classmethod
    def sealed(cls) -> "AtriumState":
        """Return a Nexus present without a valid activation."""

        return cls(phase=AtriumPhase.SEALED)

    @classmethod
    def activated(cls, enabled_chambers: frozenset[str]) -> "AtriumState":
        """Return the first Atrium state for one validated activation."""

        return cls(
            phase=AtriumPhase.ARRIVAL,
            enabled_chambers=frozenset(enabled_chambers),
        )

    @property
    def visible_paths(self) -> tuple[str, ...]:
        """Return every path made visible by the current activation."""

        return tuple(sorted(self.enabled_chambers))

    @property
    def unfinished_paths(self) -> tuple[str, ...]:
        """Return enabled paths not yet completed in this local run."""

        return tuple(sorted(self.enabled_chambers - self.completed_chambers))

    def is_enabled(self, chamber_id: str) -> bool:
        return chamber_id in self.enabled_chambers

    def is_completed(self, chamber_id: str) -> bool:
        return chamber_id in self.completed_chambers

    def after_completion(self, chamber_id: str) -> "AtriumState":
        """Return the changed Atrium state after one Chamber completes."""

        if chamber_id not in KNOWN_CHAMBERS:
            raise AtriumStateError(f"Unknown Chamber: {chamber_id!r}")
        if chamber_id not in self.enabled_chambers:
            raise AtriumStateError(
                f"Chamber {chamber_id!r} cannot complete because it is not enabled."
            )

        return replace(
            self,
            phase=AtriumPhase.RETURN,
            completed_chambers=self.completed_chambers | {chamber_id},
        )
