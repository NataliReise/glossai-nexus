"""Regression tests for standalone and Atrium-integrated First Spark entry."""

from __future__ import annotations

from pathlib import Path
import sys
from unittest.mock import patch


FIRST_SPARK_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(FIRST_SPARK_ROOT))

from first_spark.runtime import run_integrated_terminal, run_terminal


def rendered_prints(mock_print) -> str:
    return "\n".join(
        str(call.args[0]) if call.args else "" for call in mock_print.call_args_list
    )


def test_standalone_entry_keeps_banner_activation_and_arrival_step() -> None:
    with patch("builtins.input", side_effect=("/look", "/quit")) as mock_input:
        with patch("builtins.print") as mock_print:
            state = run_terminal()

    transcript = rendered_prints(mock_print)
    assert "Nexus 0.1 - First Spark" in transcript
    assert "Activation detected." in transcript
    assert "Recipient:" in transcript
    assert "First Spark online." in transcript
    assert "Entering the First Spark chamber." in transcript
    assert mock_input.call_count == 2
    assert state.current_module == "spark_chamber"


def test_integrated_entry_begins_directly_in_chamber_interior() -> None:
    with patch("builtins.input", side_effect=("/quit",)) as mock_input:
        with patch("builtins.print") as mock_print:
            state = run_integrated_terminal()

    transcript = rendered_prints(mock_print)
    assert "You are inside the First Spark chamber." in transcript
    assert "Visible traces:" in transcript
    assert "The private message is still locked." in transcript
    assert "Nexus 0.1 - First Spark" not in transcript
    assert "Activation detected." not in transcript
    assert "Recipient:" not in transcript
    assert "First Spark online." not in transcript
    assert "Entering the First Spark chamber." not in transcript
    assert mock_input.call_count == 1
    assert state.current_module == "spark_chamber"


def test_integrated_entry_preserves_message_unlocked_completion_signal() -> None:
    commands = (
        "  /Read Welcome.Log  ",
        "/Read Spark.Note",
        "/LINK SPARK",
        "/UNLOCK",
        "/QUIT",
    )
    with patch("builtins.input", side_effect=commands):
        with patch("builtins.print"):
            state = run_integrated_terminal()

    assert state.message_unlocked is True


def test_terminal_normalizes_case_and_surrounding_whitespace() -> None:
    with patch("builtins.input", side_effect=("  /LOOK  ", "  /QUIT  ")):
        with patch("builtins.print") as mock_print:
            state = run_terminal()

    transcript = rendered_prints(mock_print)
    assert "Entering the First Spark chamber." in transcript
    assert "First Spark closed." in transcript
    assert state.current_module == "spark_chamber"
    assert state.should_quit is True


def test_blank_input_is_ignored() -> None:
    with patch("builtins.input", side_effect=("   ", "/quit")) as mock_input:
        with patch("builtins.print"):
            state = run_terminal()

    assert mock_input.call_count == 2
    assert state.current_module == "arrival"
    assert state.should_quit is True


def test_ctrl_c_returns_without_mutating_completion() -> None:
    with patch("builtins.input", side_effect=KeyboardInterrupt):
        with patch("builtins.print") as mock_print:
            state = run_integrated_terminal()

    transcript = rendered_prints(mock_print)
    assert "First Spark interrupted." in transcript
    assert state.current_module == "spark_chamber"
    assert state.message_unlocked is False
    assert state.should_quit is False


if __name__ == "__main__":
    test_standalone_entry_keeps_banner_activation_and_arrival_step()
    test_integrated_entry_begins_directly_in_chamber_interior()
    test_integrated_entry_preserves_message_unlocked_completion_signal()
    test_terminal_normalizes_case_and_surrounding_whitespace()
    test_blank_input_is_ignored()
    test_ctrl_c_returns_without_mutating_completion()
    print("First Spark runtime entry tests passed.")
