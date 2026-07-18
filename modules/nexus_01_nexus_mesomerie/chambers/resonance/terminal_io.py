"""Terminal adapter for the Resonance Chamber interaction boundary."""

from __future__ import annotations

from dataclasses import dataclass
from textwrap import indent
from typing import Callable, Literal, Protocol

from .choices import ChoiceCatalog, ChoiceCatalogError


InputFunction = Callable[[str], str]
OutputFunction = Callable[[str], None]
PromptKind = Literal["choice", "word"]
EntryForm = Literal["compose", "answer"]


class InformationCommandHandler(Protocol):
    def __call__(self, command: str, step: str, prompt_kind: PromptKind) -> bool: ...


class BeforePromptHandler(Protocol):
    def __call__(self, step: str, prompt_kind: PromptKind) -> None: ...


class ChamberInteractionCancelled(RuntimeError):
    """Raised only when an interaction explicitly enables cancellation."""


STEP_TITLES = {
    "image": "Begin with one image",
    "image_response": "Answer the carried image",
    "scent": "Now choose one scent",
    "scent_response": "Answer the carried scent",
    "movement": "Let the trace move",
    "movement_response": "Answer the carried movement",
    "wish_word": "Leave one wish word",
    "return_word": "Leave one return word",
}


WORD_GUIDANCE = (
    "Enter one word. No explanation is needed.",
    "Do not enter a person's name, contact information, a private message, "
    "or other identifying information.",
    "The private reason behind your word is not stored.",
)


def indent_chamber_text(value: str, spaces: int = 2) -> str:
    """Indent non-blank Resonance lines without adding whitespace-only lines."""

    return indent(value, " " * spaces)


_ROOM_TEXT = {
    "compose": {
        "image": "An open field of images waits in the quiet Chamber.",
        "scent": "The chosen image holds while a circle of scents becomes perceptible.",
        "movement": "Image and scent remain present as the Chamber turns toward movement.",
        "wish_word": "The three chosen traces rest together beside a space for one word.",
    },
    "answer": {
        "image_response": "The carried image rests at the threshold of a field of responses.",
        "scent_response": "The carried scent remains present while its responses gather.",
        "movement_response": "The carried movement meets a quiet field of answering motions.",
        "return_word": "The carried resonance and your three responses wait beside one word.",
    },
}


_TRACE_TEXT = {
    "image": "Notice which image you are willing to place at the beginning.",
    "scent": "Attend to the scent that can stand beside the image already chosen.",
    "movement": "Notice how the resonance might move without searching for a correct path.",
    "wish_word": "Let one word hold the wish without explaining its private reason.",
    "image_response": "Attend to the kind of response the carried image makes possible.",
    "scent_response": "Notice what can answer the carried scent without copying it.",
    "movement_response": "Let the carried movement meet a movement of your own choosing.",
    "return_word": "Let one word carry the return without explaining what remains private.",
}


_WALKTHROUGH_TEXT = {
    "image": "Choose the image that will be carried into this originating resonance.",
    "scent": "Choose the scent that will stand beside the image already chosen.",
    "movement": "Choose how the originating trace will move.",
    "wish_word": "Leave one wish word without explaining its private reason.",
    "image_response": "Choose a response that can meet the carried image.",
    "scent_response": "Choose a response that can meet the carried scent.",
    "movement_response": "Choose a movement that can answer the carried movement.",
    "return_word": "Leave one return word without explaining its private meaning.",
}


@dataclass
class ResonanceGuidanceSession:
    """Hold only transient exploration state for one corrected Chamber visit."""

    entry_form: EntryForm
    output_fn: OutputFunction
    allow_cancel: bool
    input_fn: InputFunction = input
    room_looked_at: bool = False
    most_recent_help_step: str | None = None
    most_recent_trace_step: str | None = None
    walkthrough_active: bool = False
    last_guided_step_shown: str | None = None

    def handle(self, command: str, step: str, prompt_kind: PromptKind) -> bool:
        if command == "/look":
            self._look(step)
        elif command == "/help":
            self._help(step, prompt_kind)
        elif command == "/trace":
            self._trace(step)
        elif command == "/walkthrough":
            self._walkthrough()
        else:
            return False
        return True

    def before_prompt(self, step: str, prompt_kind: PromptKind) -> None:
        _ = prompt_kind
        if not self.walkthrough_active or self.last_guided_step_shown == step:
            return
        self.last_guided_step_shown = step
        self.output_fn("")
        self.output_fn(indent_chamber_text("Chamber voice"))
        self.output_fn(indent_chamber_text(_WALKTHROUGH_TEXT[step]))

    def _look(self, step: str) -> None:
        room_text = _ROOM_TEXT[self.entry_form][step]
        if self.room_looked_at:
            room_text = "The Chamber remains attentive. " + room_text
        self.room_looked_at = True
        self._display("Chamber view", room_text)

    def _help(self, step: str, prompt_kind: PromptKind) -> None:
        self.most_recent_help_step = step
        if prompt_kind == "choice":
            lines = ["Enter one of the numbers shown for this step."]
        else:
            lines = [
                "Enter exactly one non-empty word.",
                "Slash-prefixed information commands are not used as the chosen word.",
                "Plain words such as look, help, or trace remain valid words.",
            ]
        lines.extend(
            (
                "/look — perceive the Chamber at its current step.",
                "/help — show the current input grammar.",
                "/trace — receive one gentle hint for the current step.",
            )
        )
        if self.walkthrough_active:
            lines.append(
                "/walkthrough — leave guided walkthrough and continue independently."
            )
        else:
            lines.append(
                "/walkthrough — ask the Chamber to guide the remaining steps."
            )
        if self.allow_cancel:
            lines.append("/cancel — leave safely without creating a new output.")
        self._display("Current Chamber grammar", *lines)

    def _trace(self, step: str) -> None:
        self.most_recent_trace_step = step
        self._display("A trace answers", _TRACE_TEXT[step])

    def _walkthrough(self) -> None:
        if self.walkthrough_active:
            self.walkthrough_active = False
            self.output_fn("")
            self.output_fn(
                indent_chamber_text(
                    "Guided walkthrough ended. Continue in your own way."
                )
            )
            return

        self.output_fn("")
        self.output_fn("Guided walkthrough")
        self.output_fn(
            indent_chamber_text(
                "The Chamber can reveal the purpose of each remaining step, "
                "one step at a time."
            )
        )
        self.output_fn(
            indent_chamber_text(
                "It will not choose, fill, or create anything for you."
            )
        )
        while True:
            answer = (
                self.input_fn("Begin guided walkthrough? [yes/no]: ")
                .strip()
                .casefold()
            )
            if self.allow_cancel and answer == "/cancel":
                raise ChamberInteractionCancelled
            if answer in {"yes", "y"}:
                self.walkthrough_active = True
                self.last_guided_step_shown = None
                return
            if answer in {"no", "n", "cancel", "q"}:
                self.output_fn(indent_chamber_text("Guided walkthrough not started."))
                return
            self.output_fn("Please answer yes or no.")

    def _display(self, heading: str, *lines: str) -> None:
        self.output_fn("")
        self.output_fn(heading)
        for line in lines:
            self.output_fn(indent_chamber_text(line))


@dataclass
class TerminalChamberIO:
    """Human-facing terminal adapter that keeps internal IDs out of sight."""

    catalog: ChoiceCatalog
    input_fn: InputFunction = input
    output_fn: OutputFunction = print
    allow_cancel: bool = False
    information_handler: InformationCommandHandler | None = None
    before_prompt: BeforePromptHandler | None = None

    def choose(self, step: str, option_ids: tuple[str, ...]) -> str:
        if not option_ids:
            raise ChoiceCatalogError(f"No options are available at step {step!r}.")

        labels = tuple(self._label_for(option_id) for option_id in option_ids)
        self._render_choice_prompt(step, labels)

        while True:
            raw_value = self.input_fn("Enter a number: ").strip()
            if self.allow_cancel and raw_value.casefold() == "/cancel":
                raise ChamberInteractionCancelled("Chamber interaction cancelled.")
            if self._handle_information_command(raw_value, step, "choice"):
                self._render_choice_prompt(step, labels)
                continue
            try:
                index = int(raw_value)
            except ValueError:
                self.output_fn("Please enter one of the numbers shown above.")
                continue

            if 1 <= index <= len(option_ids):
                return option_ids[index - 1]

            self.output_fn("Please enter one of the numbers shown above.")

    def enter_word(self, step: str) -> str:
        self._render_word_prompt(step)

        while True:
            value = self.input_fn("Enter exactly one word: ").strip()
            if self.allow_cancel and value.casefold() == "/cancel":
                raise ChamberInteractionCancelled("Chamber interaction cancelled.")
            if self._handle_information_command(value, step, "word"):
                self._render_word_prompt(step)
                continue
            if value and len(value.split()) == 1:
                return value
            self.output_fn("Please enter exactly one non-empty word.")

    def _render_choice_prompt(self, step: str, labels: tuple[str, ...]) -> None:
        if self.before_prompt is not None:
            self.before_prompt(step, "choice")
        title = STEP_TITLES.get(step, "Choose one path")
        self.output_fn("")
        self.output_fn(title)
        self.output_fn("-" * len(title))
        for index, label in enumerate(labels, start=1):
            self.output_fn(indent_chamber_text(f"{index}. {label}"))

    def _render_word_prompt(self, step: str) -> None:
        if self.before_prompt is not None:
            self.before_prompt(step, "word")
        title = STEP_TITLES.get(step, "Leave one word")
        self.output_fn("")
        self.output_fn(title)
        self.output_fn("-" * len(title))
        for line in WORD_GUIDANCE:
            self.output_fn(indent_chamber_text(line))

    def _handle_information_command(
        self,
        raw_value: str,
        step: str,
        prompt_kind: PromptKind,
    ) -> bool:
        if self.information_handler is None:
            return False
        command = raw_value.casefold()
        if not command.startswith("/"):
            return False
        if not self.information_handler(command, step, prompt_kind):
            self.output_fn(indent_chamber_text("Unknown Chamber command."))
            self.output_fn(
                indent_chamber_text("Use /help to see the commands available here.")
            )
        return True

    def _label_for(self, option_id: str) -> str:
        for kind in (
            "images",
            "image_responses",
            "scents",
            "scent_responses",
            "movements",
            "movement_responses",
        ):
            for option in getattr(self.catalog, kind):
                if option.id == option_id:
                    return option.label
        raise ChoiceCatalogError(f"No player-facing label exists for option {option_id!r}.")
