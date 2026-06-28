"""Standard response object for First Spark game modules."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ModuleResponse:
    """Standard output from a game module to the runtime."""

    text: str
    next_module: str | None = None
    should_quit: bool = False
