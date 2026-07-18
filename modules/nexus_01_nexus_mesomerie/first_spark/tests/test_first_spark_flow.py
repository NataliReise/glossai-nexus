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
from first_spark.runtime import INTERRUPT_TEXT, dispatch_command
from first_spark.state import GameState


PUBLIC_REPOSITORY_URL = "https://github.com/NataliReise/glossai-nexus.git"
WHAT_NEXT_GUIDE_URL = (
    "https://github.com/NataliReise/glossai-nexus/blob/main/"
    "modules/nexus_01_nexus_mesomerie/first_spark/WHAT_NEXT.md"
)
SECTION_DIVIDER = "︵‿︵‿୨ ☾𓋹☽ ୧‿︵‿︵"


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
    expected_path = (
        "/look",
        "/read welcome.log",
        "/read spark.note",
        "/link spark",
        "/unlock",
    )
    rendered_steps = tuple(
        line.strip() for line in response.splitlines() if line.startswith("  ")
    )
    assert rendered_steps == expected_path


def assert_unknown_command_recovery(response: str, original_input: str) -> None:
    """Assert that unknown commands receive neutral, non-echoing feedback."""
    assert_contains(response, "Unknown First Spark command.")
    assert_contains(response, "Use /help")
    assert original_input not in response


def assert_after_play_message(response: str) -> None:
    """Assert that the after-play message is shown after unlock."""
    assert_contains(response, "[after-play]")
    assert_contains(response, "The First Spark is complete.")
    assert_contains(response, "You may keep this as a finished gift.")
    assert_contains(response, "Nothing else is required.")
    assert_contains(response, "let the spark travel further")
    assert_contains(response, PUBLIC_REPOSITORY_URL)
    assert_contains(response, "Short guide:")
    assert_contains(response, WHAT_NEXT_GUIDE_URL)
    assert_contains(response, "Never post private activation data")
    assert_contains(response, "public-safe resonance node")
    assert_contains(response, "Use /resonance-node")
    assert_contains(response, "edit only the public alias and public note")


def assert_section_divider(response: str) -> None:
    """Assert that the First Spark section divider separates ending sections."""
    assert_contains(response, SECTION_DIVIDER)
    if response.count(SECTION_DIVIDER) < 2:
        raise AssertionError(
            f"Expected at least two section dividers in response:\n{response}"
        )


def assert_resonance_node(response: str) -> None:
    """Assert that the resonance node draft remains public-safe."""
    assert_contains(response, "[public-safe resonance node draft]")
    assert_contains(response, "This is an optional public-safe note.")
    assert_contains(response, "Resonance Node: N01-RN-draft")
    assert_contains(response, "Module: Nexus 01 - First Spark")
    assert_contains(response, "Status: completed")
    assert_contains(response, "Trace visibility: public-safe summary only")
    assert_contains(response, PUBLIC_REPOSITORY_URL)
    assert_contains(response, "No private activation data")
    assert "[activation message]" not in response


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


def test_interrupt_text() -> None:
    """Test the friendly Ctrl-C interrupt text."""
    assert_contains(INTERRUPT_TEXT, "First Spark interrupted.")
    assert_contains(INTERRUPT_TEXT, "Returning to your terminal.")
    assert "Traceback" not in INTERRUPT_TEXT


def test_first_spark_main_flow() -> None:
    """Test the current First Spark happy path and guidance flow."""
    state = GameState()

    response = run_command(state, "/help")
    assert_contains(response, "/trace")
    assert_contains(response, "/walkthrough")
    assert_contains(response, "/quit")
    assert state.current_module == "arrival"

    response = run_command(state, "git statusquit")
    assert_unknown_command_recovery(response, "git statusquit")
    assert state.current_module == "arrival"

    response = run_command(state, "/walkthrough")
    assert_walkthrough(response)
    assert state.current_module == "arrival"

    response = run_command(state, "/trace")
    assert_contains(response, "Look for the entrance.")
    assert state.current_module == "arrival"

    response = run_command(state, "/look")
    assert_contains(response, "Entering the First Spark chamber.")
    assert state.current_module == "spark_chamber"

    response = run_command(state, "/look")
    assert_contains(response, "Visible traces:")

    response = run_command(state, "/help")
    assert_contains(response, "/walkthrough")
    assert_contains(response, "/quit")

    response = run_command(state, "/walkthrough")
    assert_walkthrough(response)
    assert state.current_module == "spark_chamber"

    response = run_command(state, "/trace")
    assert_contains(response, "Start with what is visible.")

    response = run_command(state, "/unlock")
    assert_contains(response, "The private message does not open yet.")
    assert not state.message_unlocked
    assert state.current_module == "spark_chamber"

    response = run_command(state, "/read welcome.log")
    assert_contains(response, "A spark does not need to become a system before it can glow.")
    assert "welcome.log" in state.read_traces

    response = run_command(state, "/trace")
    assert_contains(response, "The spark has another visible trace.")

    response = run_command(state, "/link spark")
    assert_contains(response, "The spark is not ready to link.")
    assert not state.spark_linked

    response = run_command(state, "/read spark.note")
    assert_contains(response, "Two traces can begin to resonate.")
    assert "spark.note" in state.read_traces

    response = run_command(state, "/trace")
    assert_contains(response, "Two visible traces may form one spark.")

    response = run_command(state, "/link spark")
    assert_contains(response, "Fragment connection detected.")
    assert_contains(response, "The lock no longer feels silent.")
    assert state.spark_linked
    assert state.current_module == "spark_chamber"

    response = run_command(state, "/trace")
    assert_contains(response, "The private message reacts. Try to open it.")

    response = run_command(state, "/unlock")
    assert_contains(response, "The private message opens.")
    assert_contains(response, "[activation message]")
    assert_after_play_message(response)
    assert_section_divider(response)
    assert state.message_unlocked
    assert state.current_module == "ending"

    response = run_command(state, "/look")
    assert_contains(response, "The private message is already open.")
    assert_after_play_message(response)
    assert_section_divider(response)

    response = run_command(state, "/unlock")
    assert_contains(response, "The private message is already open.")
    assert state.message_unlocked

    response = run_command(state, "/help")
    assert_contains(response, "/walkthrough")
    assert_contains(response, "/quit")
    assert_contains(response, "/resonance-node")

    response = run_command(state, "/resonance-node")
    assert_resonance_node(response)
    assert state.current_module == "ending"

    response = run_command(state, "git statusquit")
    assert_unknown_command_recovery(response, "git statusquit")
    assert state.current_module == "ending"

    response = run_command(state, "/walkthrough")
    assert_walkthrough(response)
    assert state.current_module == "ending"

    response = run_command(state, "/trace")
    assert_contains(response, "The First Spark is complete.")

    response = run_command(state, "/quit")
    assert_contains(response, "First Spark closed.")
    assert state.should_quit


def test_bare_help_is_the_only_non_slash_command() -> None:
    """Keep bare help as an unadvertised rescue alias in every module."""
    for module_name in ("arrival", "spark_chamber", "ending"):
        state = GameState(current_module=module_name)
        response = run_command(state, "help")
        assert_contains(response, "/help")
        advertised_commands = {
            line.strip().split()[0]
            for line in response.splitlines()
            if line.startswith("  ")
        }
        assert "help" not in advertised_commands


def test_former_bare_commands_are_unknown_and_non_mutating() -> None:
    """Reject every former bare action before it reaches a module handler."""
    former_commands = (
        "look",
        "trace",
        "walkthrough",
        "quit",
        "read",
        "read welcome.log",
        "read spark.note",
        "link",
        "link spark",
        "unlock",
        "resonance-node",
    )

    for command in former_commands:
        state = GameState(current_module="spark_chamber")
        response = run_command(state, command)
        assert_unknown_command_recovery(response, command)
        assert state == GameState(current_module="spark_chamber")

    unknown_slash = "/unknown-secret"
    state = GameState(current_module="spark_chamber")
    response = run_command(state, unknown_slash)
    assert_unknown_command_recovery(response, unknown_slash)
    assert state == GameState(current_module="spark_chamber")


def test_arrival_slash_quit_preserves_leaving_semantics() -> None:
    """Allow the canonical leaving command before entering the Chamber."""
    state = GameState()
    response = run_command(state, "/quit")
    assert_contains(response, "First Spark closed.")
    assert state.current_module == "arrival"
    assert state.should_quit is True


def test_recognized_slash_families_keep_module_validation() -> None:
    """Keep read/link usage and target validation inside the Chamber module."""
    state = GameState(current_module="spark_chamber")

    assert_contains(run_command(state, "/read"), "Usage: /read <trace-name>")
    assert_contains(run_command(state, "/read missing.log"), "Trace not found")
    assert_contains(run_command(state, "/link"), "Usage: /link spark")
    assert_contains(run_command(state, "/link moon"), "Unknown link target")
    assert state == GameState(current_module="spark_chamber")


def test_resonance_node_remains_ending_only_and_view_only() -> None:
    """Expose the static node only after completion without changing state."""
    arrival_state = GameState()
    response = run_command(arrival_state, "/resonance-node")
    assert_unknown_command_recovery(response, "/resonance-node")
    assert arrival_state == GameState()

    ending_state = GameState(
        current_module="ending",
        read_traces={"welcome.log", "spark.note"},
        spark_linked=True,
        message_unlocked=True,
    )
    before = GameState(
        current_module="ending",
        read_traces=set(ending_state.read_traces),
        spark_linked=True,
        message_unlocked=True,
    )
    assert_resonance_node(run_command(ending_state, "/resonance-node"))
    assert ending_state == before


def test_current_player_docs_show_canonical_slash_commands() -> None:
    """Keep current First Spark player documentation on the public grammar."""
    readme = (FIRST_SPARK_ROOT / "README.md").read_text(encoding="utf-8")
    for command in (
        "/help",
        "/look",
        "/read <trace-name>",
        "/link spark",
        "/unlock",
        "/trace",
        "/walkthrough",
        "/resonance-node",
        "/quit",
    ):
        assert f"- `{command}`" in readme

    activation_guide = (FIRST_SPARK_ROOT / "LOCAL_ACTIVATION_GUIDE.md").read_text(
        encoding="utf-8"
    )
    assert "\n/help\n" in activation_guide
    assert "\n/quit\n" in activation_guide

    what_next = (FIRST_SPARK_ROOT / "WHAT_NEXT.md").read_text(encoding="utf-8")
    assert "\n/resonance-node\n" in what_next
    assert "Use `/resonance-node`" in what_next


if __name__ == "__main__":
    test_local_activation_creation_helper()
    test_activation_file_validation_errors()
    test_interrupt_text()
    test_first_spark_main_flow()
    test_bare_help_is_the_only_non_slash_command()
    test_former_bare_commands_are_unknown_and_non_mutating()
    test_arrival_slash_quit_preserves_leaving_semantics()
    test_recognized_slash_families_keep_module_validation()
    test_resonance_node_remains_ending_only_and_view_only()
    test_current_player_docs_show_canonical_slash_commands()
    print("First Spark flow tests passed.")
