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
    with patch("builtins.input", side_effect=("look", "quit")) as mock_input:
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
    with patch("builtins.input", side_effect=("quit",)) as mock_input:
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
        "read welcome.log",
        "read spark.note",
        "link spark",
        "unlock",
        "quit",
    )
    with patch("builtins.input", side_effect=commands):
        with patch("builtins.print"):
            state = run_integrated_terminal()

    assert state.message_unlocked is True


if __name__ == "__main__":
    test_standalone_entry_keeps_banner_activation_and_arrival_step()
    test_integrated_entry_begins_directly_in_chamber_interior()
    test_integrated_entry_preserves_message_unlocked_completion_signal()
    print("First Spark runtime entry tests passed.")
