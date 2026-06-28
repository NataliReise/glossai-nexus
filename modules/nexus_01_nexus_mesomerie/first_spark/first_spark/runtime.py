"""Runtime for Nexus 0.1 - First Spark."""

from __future__ import annotations

from collections.abc import Callable

from first_spark.config import PROMPT
from first_spark.game_modules import arrival, spark_chamber
from first_spark.module_response import ModuleResponse
from first_spark.state import GameState


ModuleHandler = Callable[[str, GameState], ModuleResponse]


MODULES: dict[str, ModuleHandler] = {
    "arrival": arrival.handle_command,
    "spark_chamber": spark_chamber.handle_command,
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


def run_terminal() -> None:
    """Run the modular First Spark terminal."""
    state = GameState()
    print()
    print(arrival.boot_text())
    print()

    while not state.should_quit:
        command = input(PROMPT).strip().lower()
        if command == "":
            continue

        response = dispatch_command(command, state)
        print_response(response)
