"""Minimal flow tests for Nexus 0.1 - First Spark."""

from __future__ import annotations

import importlib.util
from pathlib import Path
import sys
import tempfile


FIRST_SPARK_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(FIRST_SPARK_ROOT))

CREATE_LOCAL_ACTIVATION_PATH = FIRST_SPARK_ROOT / "create_local_activation.py"
CREATE_LOCAL_ACTIVATION_SPEC = importlib.util.spec_from_file_location(
    "create_local_activation", CREATE_LOCAL_ACTIVATION_PATH
)
if CREATE_LOCAL_ACTIVATION_SPEC is None or CREATE_LOCAL_ACTIVATION_SPEC.loader is None:
    raise ImportError(f"Could not load {CREATE_LOCAL_ACTIVATION_PATH}")
CREATE_LOCAL_ACTIVATION_MODULE = importlib.util.module_from_spec(
    CREATE_LOCAL_ACTIVATION_SPEC
)
CREATE_LOCAL_ACTIVATION_SPEC.loader.exec_module(CREATE_LOCAL_ACTIVATION_MODULE)
create_local_activation = CREATE_LOCAL_ACTIVATION_MODULE.create_local_activation

from first_spark.activation import ActivationFileError, load_activation
from first_spark.runtime import dispatch_command
from first_spark.state import GameState


PUBLIC_REPOSITORY_URL = "https://github.com/NataliReise/glossai-nexus.git"
SECTION_DIVIDER = "︵‿︵‿୨🜂 ☾𓋹☽ 🜄୧‿︵‿︵"


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


def assert_after_play_message(response: str) -> None:
    """Assert that the after-play message is shown after unlock."""
    assert_contains(response, "[after-play]")
    assert_contains(response, "The First Spark is complete.")
    assert_contains(response, "You may keep this as a finished gift.")
    assert_contains(response, "Nothing else is required.")
    assert_contains(response, "let the spark travel further")
    assert_contains(response, PUBLIC_REPOSITORY_URL)
    assert_contains(response, "Never post private activation data")
    assert_contains(response, "public-safe resonance node")


def assert_section_divider(response: str) -> None:
    """Assert that the First Spark section divider separates ending sections."""
    assert_contains(response, SECTION_DIVIDER)
    if response.count(SECTION_DIVIDER) < 2:
        raise AssertionError(
            f"Expected at least two section dividers in response:\n{response}"
        )


def test_local_activation_creation_helper() -> None:
    """Test safe creation of activation.local.json from an example file."""
    with tempfile.TemporaryDirectory() as directory:
        example_path = Path(directory) / "activation.example.json"
        local_path = Path(directory) / "activation.local.json"
        example_content = '{"recipient_alias": "recipient_name"}\n'
        existing_content = '{"recipient_alias": "already_exists"}\n'
        example_path.write_text(example_content, encoding="utf-8")

        message = create_local_activation(example_path, local_path)
        assert_contains(message, "Local activation file created.")
        assert_contains(message, "ignored by Git")
        assert local_path.read_text(encoding="utf-8") == example_content

        local_path.write_text(existing_content, encoding="utf-8")
        message = create_local_activation(example_path, local_path)
        assert_contains(message, "already exists")
        assert_contains(message, "Nothing was changed")
        assert local_path.read_text(encoding="utf-8") == existing_content


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
    assert_after_play_message(response)
    assert_section_divider(response)
    assert state.message_unlocked
    assert state.current_module == "ending"

    response = run_command(state, "look")
    assert_contains(response, "The private message is already open.")
    assert_after_play_message(response)
    assert_section_divider(response)

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
    test_local_activation_creation_helper()
    test_activation_file_validation_errors()
    test_first_spark_main_flow()
    print("First Spark flow tests passed.")
