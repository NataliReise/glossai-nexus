"""Curated V0.1 choices owned by the Resonance Chamber."""

from __future__ import annotations

from dataclasses import dataclass


class ChoiceCatalogError(ValueError):
    """Raised when a Chamber choice or compatibility relation is invalid."""


@dataclass(frozen=True)
class ChoiceOption:
    id: str
    label: str

    def __post_init__(self) -> None:
        if not self.id.strip() or not self.label.strip():
            raise ChoiceCatalogError("Choice option id and label must be non-empty.")


@dataclass(frozen=True)
class ChoiceCatalog:
    images: tuple[ChoiceOption, ...]
    image_responses: tuple[ChoiceOption, ...]
    scents: tuple[ChoiceOption, ...]
    scent_responses: tuple[ChoiceOption, ...]
    movements: tuple[ChoiceOption, ...]
    movement_responses: tuple[ChoiceOption, ...]
    image_compatibility: dict[str, tuple[str, ...]]
    scent_compatibility: dict[str, tuple[str, ...]]
    movement_compatibility: dict[str, tuple[str, ...]]

    def option_ids(self, kind: str) -> tuple[str, ...]:
        options = getattr(self, kind, None)
        if not isinstance(options, tuple):
            raise ChoiceCatalogError(f"Unknown choice kind: {kind}")
        return tuple(option.id for option in options)

    def require_choice(self, kind: str, choice_id: str) -> str:
        if choice_id not in self.option_ids(kind):
            raise ChoiceCatalogError(f"Unknown {kind} choice: {choice_id!r}")
        return choice_id

    def require_response(self, source_kind: str, source_id: str, response_id: str) -> str:
        compatibility = getattr(self, f"{source_kind}_compatibility", None)
        if not isinstance(compatibility, dict):
            raise ChoiceCatalogError(f"Unknown response source kind: {source_kind}")
        allowed = compatibility.get(source_id, ())
        if response_id not in allowed:
            raise ChoiceCatalogError(
                f"Response {response_id!r} is not compatible with {source_kind} {source_id!r}."
            )
        return response_id


def build_v0_1_catalog() -> ChoiceCatalog:
    """Return the first small curated Chamber catalog.

    The seed contains the five complete reference paths already approved by the
    rendering library. Labels are player-facing; IDs remain internal.
    """

    return ChoiceCatalog(
        images=(
            ChoiceOption("waiting-lantern", "A lantern waiting in the dark"),
            ChoiceOption("book-bench", "A book waiting on an empty bench"),
            ChoiceOption("open-starry-window", "A window open to the stars"),
            ChoiceOption("stone-in-water", "A painted stone beneath clear water"),
            ChoiceOption("bridge-in-mist", "A narrow bridge in the mist"),
        ),
        image_responses=(
            ChoiceOption("appearing-path", "A path begins to appear"),
            ChoiceOption("two-voices-one-page", "Two voices meet on one page"),
            ChoiceOption("answering-distant-light", "A distant light answers"),
            ChoiceOption("colours-carried-outward", "Colours travel outward"),
            ChoiceOption("shared-silence", "A silence becomes shared"),
        ),
        scents=(
            ChoiceOption("summer-rain", "Forest after gentle summer rain"),
            ChoiceOption("books-and-cedar", "Old books and cedar wood"),
            ChoiceOption("evening-salt", "Salt air on an evening beach"),
            ChoiceOption("first-snow", "Cold air before the first snow"),
            ChoiceOption("warm-bread", "Warm bread in a quiet kitchen"),
        ),
        scent_responses=(
            ChoiceOption("possibility-of-encounter", "The possibility of encounter"),
            ChoiceOption("open-books-beside-one-another", "Two open books beside one another"),
            ChoiceOption("sense-of-return", "A sense of return"),
            ChoiceOption("edge-of-beginning", "The edge of something beginning"),
            ChoiceOption("second-place-at-table", "A second place waiting at the table"),
        ),
        movements=(
            ChoiceOption("falling-feather", "A feather turning as it falls"),
            ChoiceOption("loosening-knot", "A knot slowly loosening"),
            ChoiceOption("returning-tide", "A tide beginning to return"),
            ChoiceOption("opening-circle", "A circle slowly opening"),
            ChoiceOption("crossing-light", "A line of light crossing the floor"),
        ),
        movement_responses=(
            ChoiceOption("crossing-feather", "Another feather crosses its path"),
            ChoiceOption("gathering-without-tightening", "Threads gathered without tightening"),
            ChoiceOption("stream-back-to-sea", "A stream flowing back to the sea"),
            ChoiceOption("playful-waves", "Edges curling into playful waves"),
            ChoiceOption("shadow-alongside", "A shadow moving alongside"),
        ),
        image_compatibility={
            "waiting-lantern": ("appearing-path",),
            "book-bench": ("two-voices-one-page",),
            "open-starry-window": ("answering-distant-light",),
            "stone-in-water": ("colours-carried-outward",),
            "bridge-in-mist": ("shared-silence",),
        },
        scent_compatibility={
            "summer-rain": ("possibility-of-encounter",),
            "books-and-cedar": ("open-books-beside-one-another",),
            "evening-salt": ("sense-of-return",),
            "first-snow": ("edge-of-beginning",),
            "warm-bread": ("second-place-at-table",),
        },
        movement_compatibility={
            "falling-feather": ("crossing-feather",),
            "loosening-knot": ("gathering-without-tightening",),
            "returning-tide": ("stream-back-to-sea",),
            "opening-circle": ("playful-waves",),
            "crossing-light": ("shadow-alongside",),
        },
    )
