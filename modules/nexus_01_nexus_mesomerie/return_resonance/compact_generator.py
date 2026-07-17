"""Pure compact text generation from one validated Resonance Return Artifact.

This production boundary performs no file I/O, matching, activation loading,
packaging, or free-word semantic analysis.
"""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import re
import unicodedata
from typing import TypeAlias

from .resonance_render_bridge import ResonanceReturnArtifact


GENERATOR_ID = "nexus-01-compact-resonance"
GENERATOR_VERSION = "1.0.0"

Seed: TypeAlias = int | str | None
JsonScalar: TypeAlias = str | int | bool | None
JsonValue: TypeAlias = JsonScalar | list["JsonValue"] | dict[str, "JsonValue"]


class CompactGenerationError(ValueError):
    """Raised when a compact result cannot be produced safely."""


@dataclass(frozen=True)
class PhraseProfile:
    profile_id: str
    line: str


@dataclass(frozen=True)
class MicroPattern:
    pattern_id: str
    template: str
    wish_line_index: int


@dataclass(frozen=True)
class CompactGenerationResult:
    text: str
    generator_id: str
    generator_version: str
    composition_plan: dict[str, JsonValue]


IMAGE_PROFILES: dict[tuple[str, str], PhraseProfile] = {
    ("waiting-lantern", "appearing-path"): PhraseProfile(
        "image.waiting-lantern.appearing-path.v1",
        "A waiting lantern reveals the beginning of a path.",
    ),
    ("book-bench", "two-voices-one-page"): PhraseProfile(
        "image.book-bench.two-voices-one-page.v1",
        "An open book on the empty bench holds two voices on one page.",
    ),
    ("open-starry-window", "answering-distant-light"): PhraseProfile(
        "image.open-starry-window.answering-distant-light.v1",
        "Through the starry window, a distant light answers.",
    ),
    ("stone-in-water", "colours-carried-outward"): PhraseProfile(
        "image.stone-in-water.colours-carried-outward.v1",
        "Beneath clear water, a painted stone sends its colours outward.",
    ),
    ("bridge-in-mist", "shared-silence"): PhraseProfile(
        "image.bridge-in-mist.shared-silence.v1",
        "On the narrow misted bridge, silence becomes shared.",
    ),
}

SCENT_PROFILES: dict[tuple[str, str], PhraseProfile] = {
    ("summer-rain", "possibility-of-encounter"): PhraseProfile(
        "scent.summer-rain.possibility-of-encounter.v1",
        "Summer rain carries the possibility of encounter.",
    ),
    ("books-and-cedar", "open-books-beside-one-another"): PhraseProfile(
        "scent.books-and-cedar.open-books-beside-one-another.v1",
        "Books and cedar keep two open pages beside one another.",
    ),
    ("evening-salt", "sense-of-return"): PhraseProfile(
        "scent.evening-salt.sense-of-return.v1",
        "Evening salt air carries a sense of return.",
    ),
    ("first-snow", "edge-of-beginning"): PhraseProfile(
        "scent.first-snow.edge-of-beginning.v1",
        "Air before first snow holds the edge of a beginning.",
    ),
    ("warm-bread", "second-place-at-table"): PhraseProfile(
        "scent.warm-bread.second-place-at-table.v1",
        "Warm bread keeps a second place at the quiet table.",
    ),
}

MOVEMENT_PROFILES: dict[tuple[str, str], PhraseProfile] = {
    ("falling-feather", "crossing-feather"): PhraseProfile(
        "movement.falling-feather.crossing-feather.v1",
        "One turning feather meets another across its falling path.",
    ),
    ("loosening-knot", "gathering-without-tightening"): PhraseProfile(
        "movement.loosening-knot.gathering-without-tightening.v1",
        "The loosening knot gathers its threads without tightening.",
    ),
    ("returning-tide", "stream-back-to-sea"): PhraseProfile(
        "movement.returning-tide.stream-back-to-sea.v1",
        "The returning tide draws a stream back toward the sea.",
    ),
    ("opening-circle", "playful-waves"): PhraseProfile(
        "movement.opening-circle.playful-waves.v1",
        "The opening circle lets its edges curl into playful waves.",
    ),
    ("crossing-light", "shadow-alongside"): PhraseProfile(
        "movement.crossing-light.shadow-alongside.v1",
        "Crossing light finds a shadow moving alongside.",
    ),
}

MICRO_PATTERNS: tuple[MicroPattern, ...] = (
    MicroPattern(
        "sensory-wish-movement.v1",
        "{image_line}\n{scent_line}\nMay {wish_word} find room here.\n"
        "{movement_line}\n{return_word}",
        2,
    ),
    MicroPattern(
        "wish-led-passage.v1",
        "For {wish_word}, the way stays open.\n{image_line}\n{movement_line}\n"
        "{scent_line}\n{return_word}",
        0,
    ),
    MicroPattern(
        "image-carried-wish.v1",
        "{image_line}\nLet {wish_word} be carried with care.\n{scent_line}\n"
        "{movement_line}\n{return_word}",
        1,
    ),
)

_UNRESOLVED_PLACEHOLDER = re.compile(r"\{[A-Za-z_][A-Za-z0-9_]*\}")


def generate_compact_resonance(
    artifact: ResonanceReturnArtifact,
    seed: Seed = None,
) -> CompactGenerationResult:
    """Render one compact result from an already validated transport artifact."""

    if not isinstance(artifact, ResonanceReturnArtifact):
        raise CompactGenerationError(
            "Compact generator requires a validated ResonanceReturnArtifact instance."
        )
    if isinstance(seed, bool) or not isinstance(seed, (int, str, type(None))):
        raise CompactGenerationError("seed must be an integer, text, or None")

    image_profile = _resolve_profile(
        "image", artifact.image_id, artifact.image_response_id, IMAGE_PROFILES
    )
    scent_profile = _resolve_profile(
        "scent", artifact.scent_id, artifact.scent_response_id, SCENT_PROFILES
    )
    movement_profile = _resolve_profile(
        "movement", artifact.movement_id, artifact.movement_response_id, MOVEMENT_PROFILES
    )
    wish_word = _require_single_line_word(artifact.wish_word, "wish_word")
    return_word = _require_single_line_word(artifact.return_word, "return_word")

    pattern = MICRO_PATTERNS[_pattern_index(seed, len(MICRO_PATTERNS))]
    values = {
        "image_line": image_profile.line,
        "scent_line": scent_profile.line,
        "movement_line": movement_profile.line,
        "wish_word": wish_word,
        "return_word": return_word,
    }
    try:
        text = pattern.template.format_map(values)
    except KeyError as error:
        raise CompactGenerationError(
            f"Generator micro-pattern {pattern.pattern_id!r} has unresolved placeholder {error}."
        ) from error

    lines = _validate_rendered_text(
        text,
        wish_word=wish_word,
        return_word=return_word,
        wish_line_index=pattern.wish_line_index,
    )
    same_word = _normalized_word(wish_word) == _normalized_word(return_word)
    plan: dict[str, JsonValue] = {
        "generator_id": GENERATOR_ID,
        "generator_version": GENERATOR_VERSION,
        "seed": seed,
        "pattern_id": pattern.pattern_id,
        "profile_ids": {
            "image": image_profile.profile_id,
            "scent": scent_profile.profile_id,
            "movement": movement_profile.profile_id,
        },
        "source_artifact_ids": {
            "image_id": artifact.image_id,
            "image_response_id": artifact.image_response_id,
            "scent_id": artifact.scent_id,
            "scent_response_id": artifact.scent_response_id,
            "movement_id": artifact.movement_id,
            "movement_response_id": artifact.movement_response_id,
        },
        "free_word_roles": {
            "wish_word": "grammatical wish clause",
            "return_word": "final standalone line",
        },
        "same_word_strategy": (
            "separated-wish-role-and-final-return" if same_word else "not-required"
        ),
        "line_count": len(lines),
        "rendered_text": text,
    }
    return CompactGenerationResult(
        text=text,
        generator_id=GENERATOR_ID,
        generator_version=GENERATOR_VERSION,
        composition_plan=plan,
    )


def _resolve_profile(
    kind: str,
    source_id: str,
    response_id: str,
    profiles: dict[tuple[str, str], PhraseProfile],
) -> PhraseProfile:
    try:
        return profiles[(source_id, response_id)]
    except KeyError as error:
        raise CompactGenerationError(
            f"Unsupported {kind} path: {source_id!r} with response {response_id!r}."
        ) from error


def _require_single_line_word(value: str, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise CompactGenerationError(f"{field_name} must be non-empty text")
    cleaned = value.strip()
    if any(character in cleaned for character in ("\n", "\r")):
        raise CompactGenerationError(f"{field_name} must remain on one visible line")
    if any(unicodedata.category(character) == "Cc" for character in cleaned):
        raise CompactGenerationError(f"{field_name} must not contain control characters")
    return cleaned


def _pattern_index(seed: Seed, pattern_count: int) -> int:
    if pattern_count < 1:
        raise CompactGenerationError("Compact generator has no micro-patterns")
    if seed is None:
        return 0
    seed_bytes = f"{type(seed).__name__}:{seed}".encode("utf-8")
    digest = hashlib.sha256(seed_bytes).digest()
    return int.from_bytes(digest[:8], "big") % pattern_count


def _validate_rendered_text(
    text: str,
    *,
    wish_word: str,
    return_word: str,
    wish_line_index: int,
) -> tuple[str, ...]:
    if _UNRESOLVED_PLACEHOLDER.search(text):
        raise CompactGenerationError("Rendered text contains an unresolved placeholder")
    lines = tuple(text.splitlines())
    if len(lines) != 5 or any(not line.strip() for line in lines):
        raise CompactGenerationError("Compact generator must render exactly five non-empty lines")
    if lines[-1] != return_word:
        raise CompactGenerationError("return_word must remain the final standalone line")
    if not 0 <= wish_line_index < len(lines) - 1 or wish_word not in lines[wish_line_index]:
        raise CompactGenerationError("wish_word was not preserved in its grammatical role")
    normalized_lines = [_normalized_phrase(line) for line in lines]
    for previous, current in zip(normalized_lines, normalized_lines[1:]):
        if previous == current:
            raise CompactGenerationError("Rendered text contains duplicate adjacent phrases")
    return lines


def _normalized_phrase(value: str) -> str:
    normalized = unicodedata.normalize("NFC", value).strip().casefold()
    return normalized.rstrip(".!?").strip()


def _normalized_word(value: str) -> str:
    return unicodedata.normalize("NFC", value).strip().casefold()
