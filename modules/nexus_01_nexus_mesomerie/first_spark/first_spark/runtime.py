"""Runtime for Nexus 0.1 - First Spark."""

from __future__ import annotations

from collections.abc import Callable

from first_spark.config import PROMPT
from first_spark.game_modules import arrival, ending, spark_chamber
from first_spark.module_response import ModuleResponse
from first_spark.state import GameState


ModuleHandler = Callable[[str, GameState], ModuleResponse]


INTERRUPT_TEXT = """First Spark interrupted.
Returning to your terminal."""


MODULES: dict[str, ModuleHandler] = {
    "arrival": arrival.handle_command,
    "spark_chamber": spark_chamber.handle_command,
    "ending": ending.handle_command,
}


def print_response(response: ModuleResponse) -> None:
    """Print a module response with consistent spacing."""
    if response.text:
        print()
        print(response.text)
        print()


def dispatch_command(command: str, state: GameState) -> ModuleResponse:
    """Send a command to the currently active game module."""
    module_handler = MODULES[state.current_module]
    response = module_handler(command, state)

    if response.next_module is not None:
        state.current_module = response.next_module

    if response.should_quit:
        state.should_quit = True

    return response


def read_command() -> str | None:
    """Read one command from the terminal.

    Return None when the player interrupts First Spark with Ctrl-C.
    """
    try:
        return input(PROMPT).strip().lower()
    except KeyboardInterrupt:
        print()
        print(INTERRUPT_TEXT)
        return None


def run_terminal() -> GameState:
    """Run the modular First Spark terminal and return its final local state.

    Returning the state does not change the standalone terminal experience.  It
    only allows an outer Nexus runtime to observe whether First Spark reached
    its own completion condition.
    """
    state = GameState()
    print()
    print(arrival.boot_text())
    print()

    while not state.should_quit:
        command = read_command()
        if command is None:
            break
        if command == "":
            continue

        response = dispatch_command(command, state)
        print_response(response)

    return state
