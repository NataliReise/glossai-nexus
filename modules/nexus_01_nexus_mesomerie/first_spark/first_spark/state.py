"""Game state for Nexus 0.1 - First Spark."""

from __future__ import annotations

from dataclasses import dataclass, field

from first_spark.config import START_MODULE


@dataclass
class GameState:
    """Small shared state passed through game modules."""

    current_module: str = START_MODULE
    read_traces: set[str] = field(default_factory=set)
    spark_linked: bool = False
    should_quit: bool = False
