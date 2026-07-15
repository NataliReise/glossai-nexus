#!/usr/bin/env python3
"""Tests for the player-facing Resonance terminal controller."""

from __future__ import annotations

from pathlib import Path
import sys


MODULE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(MODULE_ROOT))

from atrium.resonance_terminal import ResonanceTerminalController
from return_resonance.token import (
    LAYER_ID,
    MODULE_ID,
    TOKEN_TYPE,
    TOKEN_VERSION,
    ResonanceToken,
    ResonanceTokenLoadError,
)


class FakeTerminal:
    def __init__(self, answers: list[str]) -> None:
        self.answers = iter(answers)
        self.output: list[str] = []

    def input(self, prompt: str) -> str:
        self.output.append(prompt)
        return next(self.answers)

    def write(self, value: str) -> None:
        self.output.append(value)


def token() -> ResonanceToken:
    return ResonanceToken(
        token_version=TOKEN_VERSION,
        token_type=TOKEN_TYPE,
        module_id=MODULE_ID,
        layer_id=LAYER_ID,
        origin_trace_id="terminal-origin-001",
        return_slot_id="terminal-slot-001",
        package_id="terminal-package-001",
        enabled_chambers=("resonance",),
    )


def test_complete_terminal_visit_retains_composition_in_memory() -> None:
    terminal = FakeTerminal(
        [
            "token.json",
            "1",
            "1",
            "1",
            "1",
            "1",
            "1",
            "courage",
            "trust",
        ]
    )
    loaded_paths: list[Path] = []

    def load(path: str | Path) -> ResonanceToken:
        loaded_paths.append(Path(path))
        return token()

    controller = ResonanceTerminalController(
        input_reader=terminal.input,
        output_writer=terminal.write,
        token_loader=load,
    )
    result = controller()

    assert result.completed
    assert loaded_paths == [Path("token.json")]
    assert controller.last_run is not None
    assert controller.last_run.composition.artifact.return_word == "trust"
    assert "remains local in memory" in "\n".join(terminal.output)


def test_blank_token_path_returns_unfinished() -> None:
    terminal = FakeTerminal([""])
    controller = ResonanceTerminalController(
        input_reader=terminal.input,
        output_writer=terminal.write,
        token_loader=lambda _: token(),
    )

    result = controller()

    assert not result.completed
    assert controller.last_run is None
    assert "No Resonance Token selected" in "\n".join(terminal.output)


def test_invalid_token_returns_unfinished_without_composition() -> None:
    terminal = FakeTerminal(["broken.json"])

    def reject(_: str | Path) -> ResonanceToken:
        raise ResonanceTokenLoadError("The token is not valid.")

    controller = ResonanceTerminalController(
        input_reader=terminal.input,
        output_writer=terminal.write,
        token_loader=reject,
    )
    result = controller()

    assert not result.completed
    assert controller.last_run is None
    rendered = "\n".join(terminal.output)
    assert "The token is not valid." in rendered
    assert "remains unfinished" in rendered


if __name__ == "__main__":
    test_complete_terminal_visit_retains_composition_in_memory()
    test_blank_token_path_returns_unfinished()
    test_invalid_token_returns_unfinished_without_composition()
    print("Nexus Resonance terminal controller tests passed.")
