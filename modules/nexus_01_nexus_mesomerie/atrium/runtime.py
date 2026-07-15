"""Minimal runtime wrapper for the Nexus 01 Atrium.

The runtime owns Nexus-level path availability and local completion state.  It
does not implement Chamber mechanics, terminal interaction, activation loading,
or persistence.  A Chamber crosses this boundary through one small runner
callable and reports whether its current visit completed successfully.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

from .activation_bridge import ActivationProfileSource, atrium_state_from_activation
from .state import AtriumState, AtriumStateError, KNOWN_CHAMBERS


class AtriumRuntimeError(ValueError):
    """Raised when a requested Nexus path cannot be entered safely."""


@dataclass(frozen=True)
class ChamberRunResult:
    """Small result returned by a Chamber adapter after one visit."""

    completed: bool


ChamberRunner = Callable[[], ChamberRunResult]


@dataclass
class NexusAtriumRuntime:
    """Own the current Atrium state while delegating all Chamber mechanics."""

    state: AtriumState

    @classmethod
    def from_activation(
        cls,
        activation: ActivationProfileSource | None,
    ) -> "NexusAtriumRuntime":
        """Create one runtime from the validated activation boundary value."""

        return cls(state=atrium_state_from_activation(activation))

    def enter_chamber(
        self,
        chamber_id: str,
        runner: ChamberRunner,
    ) -> ChamberRunResult:
        """Enter one enabled Chamber and update the Atrium after completion.

        The runner owns the entire Chamber visit.  An interrupted or unfinished
        visit returns ``completed=False`` and leaves the Atrium state unchanged.
        """

        if chamber_id not in KNOWN_CHAMBERS:
            raise AtriumRuntimeError(f"Unknown Nexus 01 Chamber: {chamber_id!r}")

        if not self.state.is_enabled(chamber_id):
            raise AtriumRuntimeError(
                f"Chamber {chamber_id!r} is not enabled by this activation."
            )

        result = runner()
        if not isinstance(result, ChamberRunResult):
            raise AtriumRuntimeError(
                "A Chamber runner must return ChamberRunResult."
            )

        if result.completed:
            try:
                self.state = self.state.after_completion(chamber_id)
            except AtriumStateError as error:
                raise AtriumRuntimeError(
                    f"Chamber {chamber_id!r} could not return to the Atrium."
                ) from error

        return result
