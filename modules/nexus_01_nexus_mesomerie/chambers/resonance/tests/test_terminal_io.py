#!/usr/bin/env python3
"""Tests for the human-facing Resonance Chamber terminal adapter."""

from __future__ import annotations

from pathlib import Path
import sys

NEXUS_01_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(NEXUS_01_ROOT))

from chambers.resonance import (
    ResonanceChamberFlow,
    TerminalChamberIO,
    build_v0_1_catalog,
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


def test_terminal_flow_uses_labels_and_returns_internal_ids() -> None:
    terminal = FakeTerminal(["1", "1", "1", "1", "1", "1", "courage", "trust"])
    catalog = build_v0_1_catalog()
    io = TerminalChamberIO(catalog, terminal.input, terminal.write)

    result = ResonanceChamberFlow(catalog).run(io)

    assert result.image_id == "waiting-lantern"
    assert result.image_response_id == "appearing-path"
    assert result.scent_id == "summer-rain"
    assert result.scent_response_id == "possibility-of-encounter"
    assert result.movement_id == "falling-feather"
    assert result.movement_response_id == "crossing-feather"
    assert result.wish_word == "courage"
    assert result.return_word == "trust"

    visible = "\n".join(terminal.output)
    assert "A lantern waiting in the dark" in visible
    assert "A path begins to appear" in visible
    assert "waiting-lantern" not in visible
    assert "appearing-path" not in visible


def test_invalid_numbers_are_retried() -> None:
    terminal = FakeTerminal(["x", "0", "6", "2"])
    catalog = build_v0_1_catalog()
    io = TerminalChamberIO(catalog, terminal.input, terminal.write)

    selected = io.choose("image", catalog.option_ids("images"))

    assert selected == "book-bench"
    assert terminal.output.count("Please enter one of the numbers shown above.") == 3


def test_multiword_and_blank_words_are_retried() -> None:
    terminal = FakeTerminal(["", "quiet trust", "presence"])
    io = TerminalChamberIO(build_v0_1_catalog(), terminal.input, terminal.write)

    result = io.enter_word("return_word")

    assert result == "presence"
    assert terminal.output.count("Please enter exactly one non-empty word.") == 2


def main() -> int:
    test_terminal_flow_uses_labels_and_returns_internal_ids()
    test_invalid_numbers_are_retried()
    test_multiword_and_blank_words_are_retried()
    print("Resonance Chamber terminal IO tests passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
