"""Player-facing terminal controller for entering the Resonance Chamber.

This layer loads one explicit local token path, creates the existing terminal IO,
retains the rich in-memory Chamber result, and may store the resulting Return
Artifact after explicit confirmation. It does not match, render, or transmit it.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Callable

from chambers.resonance import TerminalChamberIO, build_v0_1_catalog
from return_resonance.artifact_store import (
    ResonanceArtifactStoreError,
    write_resonance_return_artifact,
)
from return_resonance.resonance_render_bridge import ResonanceReturnArtifact
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
ArtifactWriter = Callable[[ResonanceReturnArtifact, str | Path], Path]


@dataclass
class ResonanceTerminalController:
    """Load one local token and run Resonance through existing Chamber layers."""

    input_reader: InputReader = input
    output_writer: OutputWriter = print
    token_loader: TokenLoader = load_resonance_token
    artifact_writer: ArtifactWriter = write_resonance_return_artifact
    last_run: ResonanceChamberRun | None = None
    last_saved_path: Path | None = None

    def __call__(self) -> ChamberRunResult:
        self.output_writer("Resonance Chamber — legacy combined path")
        self.output_writer(
            "This older path asks for source and response choices, one at a time, "
            "then forms one local Return Artifact in memory."
        )
        self.output_writer(
            "Optional local saving is separate from completion. Nothing is sent, "
            "uploaded, synchronized, or published automatically."
        )
        self.output_writer(
            "Leave the Token path blank to return safely before the interaction "
            "begins. The legacy choice prompts do not support /cancel."
        )
        raw_path = self.input_reader("Path to Resonance Token: ").strip()
        if not raw_path:
            self.output_writer(
                "No Resonance Token selected. Nothing was written. Returning safely "
                "to the Atrium."
            )
            return ChamberRunResult(completed=False)

        token_path = Path(raw_path).expanduser()
        try:
            token = self.token_loader(token_path)
        except ResonanceTokenLoadError as error:
            self.output_writer(
                "The selected carried trace could not safely be opened. Nothing was written."
            )
            self.output_writer("The Resonance path remains unfinished.")
            self.output_writer("Returning safely to the Atrium.")
            self.output_writer(f"Technical detail: {error}")
            return ChamberRunResult(completed=False)

        io = TerminalChamberIO(
            build_v0_1_catalog(),
            input_fn=self.input_reader,
            output_fn=self.output_writer,
        )
        runner = ResonanceAtriumRunner(token=token, io=io)
        chamber_result = runner()
        self.last_run = runner.last_run
        self.output_writer("")
        self.output_writer("Chamber close")
        self.output_writer(
            "The Resonance composition is complete and remains local in memory."
        )
        self.output_writer(
            "Nothing has been sent, uploaded, synchronized, or published."
        )
        self._offer_local_save()
        return chamber_result

    def _offer_local_save(self) -> None:
        if self.last_run is None:
            return

        self.output_writer("")
        self.output_writer("Optional local saving")
        self.output_writer(
            "You may leave without saving. The in-memory composition is already complete."
        )
        while True:
            decision = self.input_reader(
                "Save the Return Artifact locally? [yes/no]: "
            ).strip().lower()
            if decision in {"no", "n"}:
                self.output_writer(
                    "The Return Artifact was not saved. Nothing was written."
                )
                self.output_writer("The composition remains complete in memory.")
                return
            if decision in {"yes", "y"}:
                break
            self.output_writer("Please answer yes or no.")

        raw_path = self.input_reader("Path for the Return Artifact: ").strip()
        if not raw_path:
            self.output_writer(
                "No destination selected. Nothing was written; the completed "
                "artifact remains in memory."
            )
            return

        artifact = self.last_run.composition.artifact
        try:
            self.last_saved_path = self.artifact_writer(
                artifact,
                Path(raw_path).expanduser(),
            )
        except ResonanceArtifactStoreError as error:
            self.output_writer("The local Return Artifact was not saved.")
            self.output_writer(
                "Nothing was written. Existing material was not replaced."
            )
            self.output_writer("The completed artifact remains local in memory.")
            self.output_writer(f"Technical detail: {error}")
            return

        self.output_writer("")
        self.output_writer("Local save complete")
        self.output_writer("The Return Artifact was saved and remains local.")
        self.output_writer(f"Return Artifact saved locally: {self.last_saved_path}")
        self.output_writer(
            "If you choose to return it, transfer it manually. Nexus 01 does not "
            "send, upload, synchronize, or publish it."
        )
