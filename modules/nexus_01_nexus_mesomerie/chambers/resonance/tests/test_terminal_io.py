#!/usr/bin/env python3
"""Tests for the human-facing Resonance Chamber terminal adapter."""

from __future__ import annotations

from pathlib import Path
import sys

NEXUS_01_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(NEXUS_01_ROOT))

from chambers.resonance import (
    ChamberInteractionCancelled,
    ResonanceChamberFlow,
    TerminalChamberIO,
    build_v0_1_catalog,
)
from chambers.resonance.terminal_io import ResonanceGuidanceSession


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


def test_word_guidance_precedes_input_and_protects_private_meaning() -> None:
    terminal = FakeTerminal(["presence"])
    io = TerminalChamberIO(build_v0_1_catalog(), terminal.input, terminal.write)

    result = io.enter_word("wish_word")

    assert result == "presence"
    visible = "\n".join(terminal.output)
    assert "Enter one word. No explanation is needed." in visible
    assert "person's name" in visible
    assert "contact information" in visible
    assert "private message" in visible
    assert "identifying information" in visible
    assert "private reason behind your word is not stored" in visible
    assert visible.index("Leave one wish word") < visible.index("Enter exactly one word:")


def test_numbered_information_command_rerenders_the_complete_same_prompt() -> None:
    terminal = FakeTerminal(["  /HeLp  ", "2"])
    handled: list[tuple[str, str, str]] = []

    def handle(command: str, step: str, prompt_kind: str) -> bool:
        handled.append((command, step, prompt_kind))
        terminal.write("  Information shown.")
        return True

    catalog = build_v0_1_catalog()
    io = TerminalChamberIO(
        catalog,
        terminal.input,
        terminal.write,
        information_handler=handle,
    )

    selected = io.choose("image", catalog.option_ids("images"))

    assert selected == "book-bench"
    assert handled == [("/help", "image", "choice")]
    assert terminal.output.count("Begin with one image") == 2
    assert terminal.output.count("--------------------") == 2
    assert terminal.output.count("  2. A book waiting on an empty bench") == 2
    assert terminal.output.count("Enter a number: ") == 2
    assert "2. A book waiting on an empty bench" not in terminal.output


def test_word_information_command_rerenders_and_is_not_selected() -> None:
    terminal = FakeTerminal(["/trace", "presence"])
    handled: list[tuple[str, str, str]] = []

    def handle(command: str, step: str, prompt_kind: str) -> bool:
        handled.append((command, step, prompt_kind))
        terminal.write("  A stable trace.")
        return True

    io = TerminalChamberIO(
        build_v0_1_catalog(),
        terminal.input,
        terminal.write,
        information_handler=handle,
    )

    selected = io.enter_word("return_word")

    assert selected == "presence"
    assert handled == [("/trace", "return_word", "word")]
    assert terminal.output.count("Leave one return word") == 2
    assert terminal.output.count("  Enter one word. No explanation is needed.") == 2
    assert terminal.output.count("Enter exactly one word: ") == 2


def test_unknown_word_command_is_consumed_and_rerenders_same_prompt() -> None:
    terminal = FakeTerminal(["  /UnKnOwN  ", "presence"])
    handled: list[tuple[str, str, str]] = []

    def handle(command: str, step: str, prompt_kind: str) -> bool:
        handled.append((command, step, prompt_kind))
        return False

    io = TerminalChamberIO(
        build_v0_1_catalog(),
        terminal.input,
        terminal.write,
        information_handler=handle,
    )

    selected = io.enter_word("return_word")

    assert selected == "presence"
    assert handled == [("/unknown", "return_word", "word")]
    assert terminal.output.count("  Unknown Chamber command.") == 1
    assert terminal.output.count(
        "  Use /help to see the commands available here."
    ) == 1
    assert terminal.output.count("Leave one return word") == 2
    assert terminal.output.count("  Enter one word. No explanation is needed.") == 2
    assert terminal.output.count("Enter exactly one word: ") == 2
    assert "Please enter exactly one non-empty word." not in terminal.output


def test_unknown_numbered_command_is_consumed_and_rerenders_same_prompt() -> None:
    terminal = FakeTerminal(["/unknown", "2"])
    handled: list[tuple[str, str, str]] = []

    def handle(command: str, step: str, prompt_kind: str) -> bool:
        handled.append((command, step, prompt_kind))
        return False

    catalog = build_v0_1_catalog()
    io = TerminalChamberIO(
        catalog,
        terminal.input,
        terminal.write,
        information_handler=handle,
    )

    selected = io.choose("image", catalog.option_ids("images"))

    assert selected == "book-bench"
    assert handled == [("/unknown", "image", "choice")]
    assert terminal.output.count("  Unknown Chamber command.") == 1
    assert terminal.output.count(
        "  Use /help to see the commands available here."
    ) == 1
    assert terminal.output.count("Begin with one image") == 2
    assert terminal.output.count("  2. A book waiting on an empty bench") == 2
    assert terminal.output.count("Enter a number: ") == 2
    assert "Please enter one of the numbers shown above." not in terminal.output


def test_all_known_slash_commands_remain_handler_owned() -> None:
    for command in ("/look", "/help", "/trace"):
        terminal = FakeTerminal([command, "1"])
        handled: list[tuple[str, str, str]] = []

        def handle(value: str, step: str, prompt_kind: str) -> bool:
            handled.append((value, step, prompt_kind))
            return True

        catalog = build_v0_1_catalog()
        io = TerminalChamberIO(
            catalog,
            terminal.input,
            terminal.write,
            information_handler=handle,
        )

        assert io.choose("image", catalog.option_ids("images")) == "waiting-lantern"
        assert handled == [(command, "image", "choice")]
        assert terminal.output.count("Begin with one image") == 2
        assert "  Unknown Chamber command." not in terminal.output


def test_plain_information_words_remain_valid_word_values() -> None:
    for word in ("look", "help", "trace", "walkthrough"):
        terminal = FakeTerminal([word])
        session = ResonanceGuidanceSession("compose", terminal.write, allow_cancel=True)
        io = TerminalChamberIO(
            build_v0_1_catalog(),
            terminal.input,
            terminal.write,
            allow_cancel=True,
            information_handler=session.handle,
        )

        assert io.enter_word("wish_word") == word


def test_help_advertises_cancel_only_when_enabled() -> None:
    disabled_output: list[str] = []
    disabled = ResonanceGuidanceSession(
        "compose", disabled_output.append, allow_cancel=False
    )
    assert disabled.handle("/help", "wish_word", "word")
    assert "/cancel" not in "\n".join(disabled_output)

    enabled_output: list[str] = []
    enabled = ResonanceGuidanceSession(
        "answer", enabled_output.append, allow_cancel=True
    )
    assert enabled.handle("/help", "image_response", "choice")
    visible = "\n".join(enabled_output)
    assert "Enter one of the numbers shown for this step" in visible
    assert "/cancel" in visible
    assert "/walkthrough — ask the Chamber to guide the remaining steps" in visible
    assert "results" not in visible

    enabled.walkthrough_active = True
    active_output: list[str] = []
    enabled.output_fn = active_output.append
    assert enabled.handle("/help", "image_response", "choice")
    assert (
        "/walkthrough — leave guided walkthrough and continue independently"
        in "\n".join(active_output)
    )


def test_walkthrough_decline_rerenders_same_numbered_prompt() -> None:
    terminal = FakeTerminal(["/walkthrough", "no", "2"])
    session = ResonanceGuidanceSession(
        "compose", terminal.write, allow_cancel=True, input_fn=terminal.input
    )
    catalog = build_v0_1_catalog()
    io = TerminalChamberIO(
        catalog,
        terminal.input,
        terminal.write,
        allow_cancel=True,
        information_handler=session.handle,
        before_prompt=session.before_prompt,
    )

    selected = io.choose("image", catalog.option_ids("images"))

    assert selected == "book-bench"
    assert not session.walkthrough_active
    assert "Guided walkthrough" in terminal.output
    assert any("purpose of each remaining step" in line for line in terminal.output)
    assert any("will not choose, fill, or create" in line for line in terminal.output)
    assert terminal.output.count("Begin guided walkthrough? [yes/no]: ") == 1
    assert terminal.output.count("Begin with one image") == 2
    assert not any("Chamber voice" in line for line in terminal.output)


def test_walkthrough_compatibility_declines_remain_local() -> None:
    for answer in ("no", "n", "cancel", "q"):
        terminal = FakeTerminal(["/walkthrough", answer, "1"])
        session = ResonanceGuidanceSession(
            "compose", terminal.write, allow_cancel=True, input_fn=terminal.input
        )
        catalog = build_v0_1_catalog()
        io = TerminalChamberIO(
            catalog,
            terminal.input,
            terminal.write,
            allow_cancel=True,
            information_handler=session.handle,
            before_prompt=session.before_prompt,
        )

        assert io.choose("image", catalog.option_ids("images")) == "waiting-lantern"
        assert not session.walkthrough_active
        assert terminal.output.count("Begin with one image") == 2
        assert any("Guided walkthrough not started" in line for line in terminal.output)


def test_slash_cancel_during_walkthrough_confirmation_cancels_chamber() -> None:
    terminal = FakeTerminal(["/walkthrough", "  /Cancel  "])
    session = ResonanceGuidanceSession(
        "compose", terminal.write, allow_cancel=True, input_fn=terminal.input
    )
    catalog = build_v0_1_catalog()
    io = TerminalChamberIO(
        catalog,
        terminal.input,
        terminal.write,
        allow_cancel=True,
        information_handler=session.handle,
        before_prompt=session.before_prompt,
    )

    try:
        io.choose("image", catalog.option_ids("images"))
    except ChamberInteractionCancelled:
        pass
    else:
        raise AssertionError("walkthrough confirmation /cancel did not cancel")

    assert not session.walkthrough_active
    assert terminal.output.count("Begin with one image") == 1
    assert terminal.output.count("Begin guided walkthrough? [yes/no]: ") == 1
    assert not any("Guided walkthrough not started" in line for line in terminal.output)


def test_disabled_cancel_is_invalid_inside_walkthrough_confirmation() -> None:
    terminal = FakeTerminal(["/walkthrough", "/cancel", "no", "1"])
    session = ResonanceGuidanceSession(
        "compose", terminal.write, allow_cancel=False, input_fn=terminal.input
    )
    catalog = build_v0_1_catalog()
    io = TerminalChamberIO(
        catalog,
        terminal.input,
        terminal.write,
        allow_cancel=False,
        information_handler=session.handle,
        before_prompt=session.before_prompt,
    )

    assert io.choose("image", catalog.option_ids("images")) == "waiting-lantern"
    assert not session.walkthrough_active
    assert terminal.output.count("Please answer yes or no.") == 1
    assert terminal.output.count("Begin guided walkthrough? [yes/no]: ") == 2
    assert terminal.output.count("Begin with one image") == 2
    assert any("Guided walkthrough not started" in line for line in terminal.output)


def test_walkthrough_confirmation_guides_current_step_without_selecting() -> None:
    terminal = FakeTerminal(["/walkthrough", "yes", "2"])
    session = ResonanceGuidanceSession(
        "compose", terminal.write, allow_cancel=True, input_fn=terminal.input
    )
    catalog = build_v0_1_catalog()
    io = TerminalChamberIO(
        catalog,
        terminal.input,
        terminal.write,
        allow_cancel=True,
        information_handler=session.handle,
        before_prompt=session.before_prompt,
    )

    selected = io.choose("image", catalog.option_ids("images"))

    assert selected == "book-bench"
    assert session.walkthrough_active
    assert session.last_guided_step_shown == "image"
    assert terminal.output.count("  Chamber voice") == 1
    assert terminal.output.count(
        "  Choose the image that will be carried into this originating resonance."
    ) == 1
    assert terminal.output.count("Begin with one image") == 2
    assert terminal.output.count("Enter a number: ") == 2


def test_invalid_walkthrough_confirmation_repeats_only_confirmation_prompt() -> None:
    terminal = FakeTerminal(["/walkthrough", "perhaps", "later", "y", "1"])
    session = ResonanceGuidanceSession(
        "compose", terminal.write, allow_cancel=True, input_fn=terminal.input
    )
    catalog = build_v0_1_catalog()
    io = TerminalChamberIO(
        catalog,
        terminal.input,
        terminal.write,
        information_handler=session.handle,
        before_prompt=session.before_prompt,
    )

    assert io.choose("image", catalog.option_ids("images")) == "waiting-lantern"
    assert terminal.output.count("Begin guided walkthrough? [yes/no]: ") == 3
    assert terminal.output.count("Please answer yes or no.") == 2
    assert terminal.output.count("Guided walkthrough") == 1
    assert terminal.output.count("Begin with one image") == 2


def test_active_walkthrough_guides_new_steps_once_despite_invalid_input() -> None:
    terminal = FakeTerminal(["/walkthrough", "yes", "x", "1", "0", "1"])
    session = ResonanceGuidanceSession(
        "compose", terminal.write, allow_cancel=True, input_fn=terminal.input
    )
    catalog = build_v0_1_catalog()
    io = TerminalChamberIO(
        catalog,
        terminal.input,
        terminal.write,
        information_handler=session.handle,
        before_prompt=session.before_prompt,
    )

    assert io.choose("image", catalog.option_ids("images")) == "waiting-lantern"
    assert io.choose("scent", catalog.option_ids("scents")) == "summer-rain"
    assert terminal.output.count("  Chamber voice") == 2
    assert terminal.output.count(
        "  Choose the image that will be carried into this originating resonance."
    ) == 1
    assert terminal.output.count(
        "  Choose the scent that will stand beside the image already chosen."
    ) == 1


def test_information_commands_do_not_repeat_active_walkthrough_guidance() -> None:
    terminal = FakeTerminal(
        ["/walkthrough", "yes", "/look", "/help", "/trace", "/unknown", "1"]
    )
    session = ResonanceGuidanceSession(
        "compose", terminal.write, allow_cancel=True, input_fn=terminal.input
    )
    catalog = build_v0_1_catalog()
    io = TerminalChamberIO(
        catalog,
        terminal.input,
        terminal.write,
        allow_cancel=True,
        information_handler=session.handle,
        before_prompt=session.before_prompt,
    )

    assert io.choose("image", catalog.option_ids("images")) == "waiting-lantern"
    assert terminal.output.count("  Chamber voice") == 1
    assert terminal.output.count(
        "  Choose the image that will be carried into this originating resonance."
    ) == 1
    assert terminal.output.count("  Unknown Chamber command.") == 1


def test_walkthrough_stop_suppresses_current_replay_and_later_steps() -> None:
    terminal = FakeTerminal(["/walkthrough", "yes", "1", "/walkthrough", "1", "1"])
    session = ResonanceGuidanceSession(
        "compose", terminal.write, allow_cancel=True, input_fn=terminal.input
    )
    catalog = build_v0_1_catalog()
    io = TerminalChamberIO(
        catalog,
        terminal.input,
        terminal.write,
        information_handler=session.handle,
        before_prompt=session.before_prompt,
    )

    assert io.choose("image", catalog.option_ids("images")) == "waiting-lantern"
    assert io.choose("scent", catalog.option_ids("scents")) == "summer-rain"
    assert io.choose("movement", catalog.option_ids("movements")) == "falling-feather"
    assert not session.walkthrough_active
    assert terminal.output.count("  Chamber voice") == 2
    assert terminal.output.count("Now choose one scent") == 2
    assert any("Guided walkthrough ended" in line for line in terminal.output)
    assert not any("originating trace will move" in line for line in terminal.output)


def test_walkthrough_can_restart_and_guide_the_current_step_again() -> None:
    terminal = FakeTerminal(
        ["/walkthrough", "yes", "1", "/walkthrough", "1", "/walkthrough", "yes", "1"]
    )
    session = ResonanceGuidanceSession(
        "compose", terminal.write, allow_cancel=True, input_fn=terminal.input
    )
    catalog = build_v0_1_catalog()
    io = TerminalChamberIO(
        catalog,
        terminal.input,
        terminal.write,
        information_handler=session.handle,
        before_prompt=session.before_prompt,
    )

    assert io.choose("image", catalog.option_ids("images")) == "waiting-lantern"
    assert io.choose("scent", catalog.option_ids("scents")) == "summer-rain"
    assert io.choose("movement", catalog.option_ids("movements")) == "falling-feather"
    assert session.walkthrough_active
    assert session.last_guided_step_shown == "movement"
    assert terminal.output.count(
        "  Choose how the originating trace will move."
    ) == 1


def test_invalid_word_does_not_repeat_active_walkthrough_guidance() -> None:
    terminal = FakeTerminal(["two words", "/look", "presence"])
    session = ResonanceGuidanceSession(
        "answer", terminal.write, allow_cancel=True, input_fn=terminal.input
    )
    session.walkthrough_active = True
    io = TerminalChamberIO(
        build_v0_1_catalog(),
        terminal.input,
        terminal.write,
        information_handler=session.handle,
        before_prompt=session.before_prompt,
    )

    assert io.enter_word("return_word") == "presence"
    assert terminal.output.count("  Chamber voice") == 1
    assert terminal.output.count(
        "  Leave one return word without explaining its private meaning."
    ) == 1


def test_walkthrough_guidance_covers_all_corrected_steps() -> None:
    output: list[str] = []
    session = ResonanceGuidanceSession("compose", output.append, allow_cancel=True)
    session.walkthrough_active = True
    for step, prompt_kind in (
        ("image", "choice"),
        ("scent", "choice"),
        ("movement", "choice"),
        ("wish_word", "word"),
        ("image_response", "choice"),
        ("scent_response", "choice"),
        ("movement_response", "choice"),
        ("return_word", "word"),
    ):
        session.before_prompt(step, prompt_kind)

    assert output.count("  Chamber voice") == 8
    assert any("wish word" in line for line in output)
    assert any("meet the carried image" in line for line in output)
    assert any("meet the carried scent" in line for line in output)
    assert any("answer the carried movement" in line for line in output)
    assert any("return word" in line for line in output)


def test_cancel_behavior_is_unchanged_and_only_enabled_explicitly() -> None:
    disabled = TerminalChamberIO(
        build_v0_1_catalog(), FakeTerminal(["/cancel"]).input, lambda _value: None
    )
    assert disabled.enter_word("wish_word") == "/cancel"

    enabled_terminal = FakeTerminal(["/cancel"])
    enabled = TerminalChamberIO(
        build_v0_1_catalog(),
        enabled_terminal.input,
        enabled_terminal.write,
        allow_cancel=True,
    )
    try:
        enabled.enter_word("wish_word")
    except ChamberInteractionCancelled:
        pass
    else:
        raise AssertionError("enabled /cancel did not cancel the interaction")


def test_unknown_slash_input_keeps_no_handler_behavior() -> None:
    word_terminal = FakeTerminal(["/unknown"])
    word_io = TerminalChamberIO(
        build_v0_1_catalog(), word_terminal.input, word_terminal.write
    )
    assert word_io.enter_word("wish_word") == "/unknown"
    assert "  Unknown Chamber command." not in word_terminal.output

    choice_terminal = FakeTerminal(["/unknown", "1"])
    catalog = build_v0_1_catalog()
    choice_io = TerminalChamberIO(
        catalog, choice_terminal.input, choice_terminal.write
    )
    assert choice_io.choose("image", catalog.option_ids("images")) == "waiting-lantern"
    assert choice_terminal.output.count(
        "Please enter one of the numbers shown above."
    ) == 1


def main() -> int:
    test_terminal_flow_uses_labels_and_returns_internal_ids()
    test_invalid_numbers_are_retried()
    test_multiword_and_blank_words_are_retried()
    test_word_guidance_precedes_input_and_protects_private_meaning()
    test_numbered_information_command_rerenders_the_complete_same_prompt()
    test_word_information_command_rerenders_and_is_not_selected()
    test_unknown_word_command_is_consumed_and_rerenders_same_prompt()
    test_unknown_numbered_command_is_consumed_and_rerenders_same_prompt()
    test_all_known_slash_commands_remain_handler_owned()
    test_plain_information_words_remain_valid_word_values()
    test_help_advertises_cancel_only_when_enabled()
    test_walkthrough_decline_rerenders_same_numbered_prompt()
    test_walkthrough_compatibility_declines_remain_local()
    test_slash_cancel_during_walkthrough_confirmation_cancels_chamber()
    test_disabled_cancel_is_invalid_inside_walkthrough_confirmation()
    test_walkthrough_confirmation_guides_current_step_without_selecting()
    test_invalid_walkthrough_confirmation_repeats_only_confirmation_prompt()
    test_active_walkthrough_guides_new_steps_once_despite_invalid_input()
    test_information_commands_do_not_repeat_active_walkthrough_guidance()
    test_walkthrough_stop_suppresses_current_replay_and_later_steps()
    test_walkthrough_can_restart_and_guide_the_current_step_again()
    test_invalid_word_does_not_repeat_active_walkthrough_guidance()
    test_walkthrough_guidance_covers_all_corrected_steps()
    test_cancel_behavior_is_unchanged_and_only_enabled_explicitly()
    test_unknown_slash_input_keeps_no_handler_behavior()
    print("Resonance Chamber terminal IO tests passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
