"""Player-facing terminal controller for entering the Resonance Chamber.

This layer loads one explicit local token path, creates the existing terminal IO,
and retains the rich in-memory Chamber result. It does not save, match, render,
or transmit the resulting Return Artifact.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Callable

from chambers.resonance import TerminalChamberIO, build_v0_1_catalog
from return_resonance.token import (
    ResonanceToken,
    ResonanceTokenLoadError,
    load_resonance_token,
)

from .resonance_adapter import ResonanceAtriumRunner, ResonanceChamberRun
from .runtime import ChamberRunResult


InputReader = Callable[[str], str]
OutputWriter = Callable[[str], None]
TokenLoader = Callable[[str | Path], ResonanceToken]


@dataclass
class ResonanceTerminalController:
    """Load one local token and run Resonance through existing Chamber layers."""

    input_reader: InputReader = input
    output_writer: OutputWriter = print
    token_loader: TokenLoader = load_resonance_token
    last_run: ResonanceChamberRun | None = None

    def __call__(self) -> ChamberRunResult:
        raw_path = self.input_reader("Path to Resonance Token: ").strip()
        if not raw_path:
            self.output_writer("No Resonance Token selected. Returning to the Atrium.")
            return ChamberRunResult(completed=False)

        token_path = Path(raw_path).expanduser()
        try:
            token = self.token_loader(token_path)
        except ResonanceTokenLoadError as error:
            self.output_writer(str(error))
            self.output_writer("The Resonance path remains unfinished.")
            return ChamberRunResult(completed=False)

        io = TerminalChamberIO(
            build_v0_1_catalog(),
            input_fn=self.input_reader,
            output_fn=self.output_writer,
        )
        runner = ResonanceAtriumRunner(token=token, io=io)
        chamber_result = runner()
        self.last_run = runner.last_run
        self.output_writer("The Resonance composition is complete and remains local in memory.")
        return chamber_result
