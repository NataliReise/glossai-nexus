#!/usr/bin/env python3
"""Tests for the player-facing Resonance terminal controller."""

from __future__ import annotations

from pathlib import Path
import sys


MODULE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(MODULE_ROOT))

from atrium.resonance_terminal import ResonanceTerminalController
from return_resonance.artifact_store import ResonanceArtifactStoreError
from return_resonance.resonance_render_bridge import ResonanceReturnArtifact
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


def complete_answers(*tail: str) -> list[str]:
    return [
        "token.json",
        "1",
        "1",
        "1",
        "1",
        "1",
        "1",
        "courage",
        "trust",
        *tail,
    ]


def test_complete_terminal_visit_can_remain_in_memory() -> None:
    terminal = FakeTerminal(complete_answers("no"))
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
    assert controller.last_saved_path is None
    rendered = "\n".join(terminal.output)
    assert "legacy combined path" in rendered
    assert "source and response choices, one at a time" in rendered
    assert "Optional local saving is separate from completion" in rendered
    assert "legacy choice prompts do not support /cancel" in rendered
    assert "remains local in memory" in rendered
    assert "was not saved" in rendered
    assert "Nothing was written" in rendered
    assert "composition remains complete in memory" in rendered
    assert rendered.index("Chamber close") < rendered.rindex("Optional local saving")


def test_confirmed_save_uses_explicit_destination() -> None:
    terminal = FakeTerminal(complete_answers("yes", "~/return-artifact.json"))
    writes: list[tuple[ResonanceReturnArtifact, Path]] = []

    def write(artifact: ResonanceReturnArtifact, path: str | Path) -> Path:
        resolved = Path(path)
        writes.append((artifact, resolved))
        return resolved

    controller = ResonanceTerminalController(
        input_reader=terminal.input,
        output_writer=terminal.write,
        token_loader=lambda _: token(),
        artifact_writer=write,
    )
    result = controller()

    assert result.completed
    assert controller.last_run is not None
    assert len(writes) == 1
    written_artifact, written_path = writes[0]
    assert written_artifact is controller.last_run.composition.artifact
    assert written_path == Path("~/return-artifact.json").expanduser()
    assert controller.last_saved_path == written_path
    rendered = "\n".join(terminal.output)
    assert "saved locally" in rendered
    assert "If you choose to return it" in rendered
    assert "does not send, upload, synchronize, or publish" in rendered


def test_blank_save_destination_keeps_completed_artifact_in_memory() -> None:
    terminal = FakeTerminal(complete_answers("yes", ""))
    controller = ResonanceTerminalController(
        input_reader=terminal.input,
        output_writer=terminal.write,
        token_loader=lambda _: token(),
        artifact_writer=lambda artifact, path: Path(path),
    )

    result = controller()

    assert result.completed
    assert controller.last_run is not None
    assert controller.last_saved_path is None
    rendered = "\n".join(terminal.output)
    assert "No destination selected" in rendered
    assert "Nothing was written" in rendered
    assert "completed artifact remains in memory" in rendered


def test_store_error_keeps_completed_artifact_in_memory() -> None:
    terminal = FakeTerminal(complete_answers("yes", "existing.json"))

    def reject(_: ResonanceReturnArtifact, __: str | Path) -> Path:
        raise ResonanceArtifactStoreError("Refusing to overwrite existing file.")

    controller = ResonanceTerminalController(
        input_reader=terminal.input,
        output_writer=terminal.write,
        token_loader=lambda _: token(),
        artifact_writer=reject,
    )
    result = controller()

    assert result.completed
    assert controller.last_run is not None
    assert controller.last_saved_path is None
    rendered = "\n".join(terminal.output)
    assert "Refusing to overwrite" in rendered
    assert "remains local in memory" in rendered
    assert "Existing material was not replaced" in rendered


def test_save_confirmation_retries_until_yes_or_no() -> None:
    terminal = FakeTerminal(complete_answers("perhaps", "no"))
    controller = ResonanceTerminalController(
        input_reader=terminal.input,
        output_writer=terminal.write,
        token_loader=lambda _: token(),
    )

    result = controller()

    assert result.completed
    assert terminal.output.count("Please answer yes or no.") == 1


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
    assert controller.last_saved_path is None
    rendered = "\n".join(terminal.output)
    assert "No Resonance Token selected" in rendered
    assert "Nothing was written" in rendered
    assert "Returning safely to the Atrium" in rendered


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
    assert controller.last_saved_path is None
    rendered = "\n".join(terminal.output)
    assert "The token is not valid." in rendered
    assert rendered.index("selected carried trace could not safely be opened") < rendered.index(
        "The token is not valid."
    )
    assert "Nothing was written" in rendered
    assert "remains unfinished" in rendered


if __name__ == "__main__":
    test_complete_terminal_visit_can_remain_in_memory()
    test_confirmed_save_uses_explicit_destination()
    test_blank_save_destination_keeps_completed_artifact_in_memory()
    test_store_error_keeps_completed_artifact_in_memory()
    test_save_confirmation_retries_until_yes_or_no()
    test_blank_token_path_returns_unfinished()
    test_invalid_token_returns_unfinished_without_composition()
    print("Nexus Resonance terminal controller tests passed.")
