"""Minimal flow tests for Nexus 0.1 - First Spark."""

from __future__ import annotations

from pathlib import Path
import sys
import tempfile


FIRST_SPARK_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(FIRST_SPARK_ROOT))

from first_spark.activation import ActivationFileError, load_activation
from first_spark.runtime import dispatch_command
from first_spark.state import GameState


def assert_contains(text: str, expected: str) -> None:
    """Assert that a response contains the expected text."""
    if expected not in text:
        raise AssertionError(f"Expected to find {expected!r} in response:\n{text}")


def run_command(state: GameState, command: str) -> str:
    """Dispatch one command and return its response text."""
    response = dispatch_command(command, state)
    return response.text


def assert_walkthrough(response: str) -> None:
    """Assert that a response contains the full spoiler walkthrough."""
    assert_contains(response, "Spoiler warning:")
    assert_contains(response, "Complete path:")
    assert_contains(response, "look")
    assert_contains(response, "read welcome.log")
    assert_contains(response, "read spark.note")
    assert_contains(response, "link spark")
    assert_contains(response, "unlock")


def assert_unknown_command_recovery(response: str) -> None:
    """Assert that unknown commands explain possible pasted input."""
    assert_contains(response, "Unknown command:")
    assert_contains(response, "pasted input")
    assert_contains(response, "fresh prompt")


def test_activation_file_validation_errors() -> None:
    """Test friendly errors for invalid local activation files."""
    with tempfile.TemporaryDirectory() as directory:
        invalid_json_path = Path(directory) / "activation.local.json"
        invalid_json_path.write_text("{not valid json", encoding="utf-8")

        try:
            load_activation(invalid_json_path)
        except ActivationFileError as error:
            message = str(error)
            assert_contains(message, "Activation file could not be loaded.")
            assert_contains(message, "Invalid JSON")
            assert_contains(message, "activation.example.json")
        else:
            raise AssertionError("Expected ActivationFileError for invalid JSON.")

        wrong_shape_path = Path(directory) / "activation.local.json"
        wrong_shape_path.write_text("[]", encoding="utf-8")

        try:
            load_activation(wrong_shape_path)
        except ActivationFileError as error:
            message = str(error)
            assert_contains(message, "Activation file could not be loaded.")
            assert_contains(message, "top-level JSON value must be an object")
            assert_contains(message, "activation.example.json")
        else:
            raise AssertionError("Expected ActivationFileError for non-object JSON.")


def test_first_spark_main_flow() -> None:
    """Test the current First Spark happy path and guidance flow."""
    state = GameState()

    response = run_command(state, "help")
    assert_contains(response, "trace")
    assert_contains(response, "walkthrough")
    assert_contains(response, "return to your terminal")
    assert state.current_module == "arrival"

    response = run_command(state, "git statusquit")
    assert_unknown_command_recovery(response)
    assert state.current_module == "arrival"

    response = run_command(state, "walkthrough")
    assert_walkthrough(response)
    assert state.current_module == "arrival"

    response = run_command(state, "trace")
    assert_contains(response, "Look for the entrance.")
    assert state.current_module == "arrival"

    response = run_command(state, "look")
    assert_contains(response, "Entering the First Spark chamber.")
    assert state.current_module == "spark_chamber"

    response = run_command(state, "help")
    assert_contains(response, "walkthrough")
    assert_contains(response, "return to your terminal")

    response = run_command(state, "walkthrough")
    assert_walkthrough(response)
    assert state.current_module == "spark_chamber"

    response = run_command(state, "trace")
    assert_contains(response, "Start with what is visible.")

    response = run_command(state, "unlock")
    assert_contains(response, "The private message does not open yet.")
    assert not state.message_unlocked
    assert state.current_module == "spark_chamber"

    response = run_command(state, "read welcome.log")
    assert_contains(response, "A spark does not need to become a system before it can glow.")
    assert "welcome.log" in state.read_traces

    response = run_command(state, "trace")
    assert_contains(response, "The spark has another visible trace.")

    response = run_command(state, "link spark")
    assert_contains(response, "The spark is not ready to link.")
    assert not state.spark_linked

    response = run_command(state, "read spark.note")
    assert_contains(response, "Two traces can begin to resonate.")
    assert "spark.note" in state.read_traces

    response = run_command(state, "trace")
    assert_contains(response, "Two visible traces may form one spark.")

    response = run_command(state, "link spark")
    assert_contains(response, "Fragment connection detected.")
    assert_contains(response, "The lock no longer feels silent.")
    assert state.spark_linked
    assert state.current_module == "spark_chamber"

    response = run_command(state, "trace")
    assert_contains(response, "The private message reacts. Try to open it.")

    response = run_command(state, "unlock")
    assert_contains(response, "The private message opens.")
    assert_contains(response, "[activation message]")
    assert state.message_unlocked
    assert state.current_module == "ending"

    response = run_command(state, "help")
    assert_contains(response, "walkthrough")
    assert_contains(response, "return to your terminal")

    response = run_command(state, "git statusquit")
    assert_unknown_command_recovery(response)
    assert state.current_module == "ending"

    response = run_command(state, "walkthrough")
    assert_walkthrough(response)
    assert state.current_module == "ending"

    response = run_command(state, "trace")
    assert_contains(response, "The First Spark is complete.")

    response = run_command(state, "quit")
    assert_contains(response, "First Spark closed.")
    assert state.should_quit


if __name__ == "__main__":
    test_activation_file_validation_errors()
    test_first_spark_main_flow()
    print("First Spark flow tests passed.")
