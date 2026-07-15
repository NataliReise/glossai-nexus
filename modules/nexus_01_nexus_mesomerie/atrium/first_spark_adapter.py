"""Adapter from the standalone First Spark terminal to the Nexus Atrium runtime.

First Spark keeps ownership of its terminal interaction and local ``GameState``.
The adapter observes only the public completion signal ``message_unlocked`` and
translates it into the small ``ChamberRunResult`` understood by the Atrium.
"""

from __future__ import annotations

from collections.abc import Callable
from pathlib import Path
import sys
from typing import Protocol

from .runtime import ChamberRunResult


class FirstSparkStateSource(Protocol):
    """Minimal final First Spark state visible at the Nexus boundary."""

    message_unlocked: bool


FirstSparkTerminalRunner = Callable[[], FirstSparkStateSource]


def load_first_spark_terminal_runner() -> FirstSparkTerminalRunner:
    """Load the standalone First Spark runner without coupling package imports.

    The historical First Spark seed keeps its import root inside the
    ``first_spark`` directory.  The adapter adds that root only when the Chamber
    is actually entered, preserving the seed's existing internal imports.
    """

    package_root = Path(__file__).resolve().parents[1] / "first_spark"
    package_root_text = str(package_root)
    if package_root_text not in sys.path:
        sys.path.insert(0, package_root_text)

    from first_spark.runtime import run_terminal

    return run_terminal


def run_first_spark_chamber(
    terminal_runner: FirstSparkTerminalRunner | None = None,
) -> ChamberRunResult:
    """Run First Spark and report whether its own completion signal was reached.

    Interrupting or leaving First Spark before the private message is unlocked
    returns ``completed=False``.  The adapter does not infer completion from the
    current module, the quit flag, or any partial progress marker.
    """

    runner = terminal_runner or load_first_spark_terminal_runner()
    final_state = runner()

    if not hasattr(final_state, "message_unlocked"):
        raise TypeError(
            "First Spark terminal runner must return a state exposing "
            "message_unlocked."
        )

    return ChamberRunResult(completed=bool(final_state.message_unlocked))
