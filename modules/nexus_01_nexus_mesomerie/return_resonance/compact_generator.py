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
GENERATOR_VERSION = "1.1.0"

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
class FragmentProfile:
    profile_id: str
    fragment: str


@dataclass(frozen=True)
class DomainProfiles:
    domain_id: str
    source_profiles: dict[str, FragmentProfile]
    response_profiles: dict[str, FragmentProfile]
    line_template: str
    legacy_pairs: dict[tuple[str, str], PhraseProfile]


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


LEGACY_IMAGE_PAIRS: dict[tuple[str, str], PhraseProfile] = {
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

LEGACY_SCENT_PAIRS: dict[tuple[str, str], PhraseProfile] = {
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

LEGACY_MOVEMENT_PAIRS: dict[tuple[str, str], PhraseProfile] = {
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

IMAGE_DOMAIN = DomainProfiles(
    domain_id="image",
    source_profiles={
        "waiting-lantern": FragmentProfile(
            "image.source.waiting-lantern.v1",
            "A waiting lantern holds its place in the dark",
        ),
        "book-bench": FragmentProfile(
            "image.source.book-bench.v1",
            "An open book waits on an empty bench",
        ),
        "open-starry-window": FragmentProfile(
            "image.source.open-starry-window.v1",
            "A window stands open to the stars",
        ),
        "stone-in-water": FragmentProfile(
            "image.source.stone-in-water.v1",
            "A painted stone rests beneath clear water",
        ),
        "bridge-in-mist": FragmentProfile(
            "image.source.bridge-in-mist.v1",
            "A narrow bridge crosses the mist",
        ),
    },
    response_profiles={
        "appearing-path": FragmentProfile(
            "image.response.appearing-path.v1", "a path begins to appear"
        ),
        "two-voices-one-page": FragmentProfile(
            "image.response.two-voices-one-page.v1",
            "two voices meet on one page",
        ),
        "answering-distant-light": FragmentProfile(
            "image.response.answering-distant-light.v1",
            "a distant light shines back",
        ),
        "colours-carried-outward": FragmentProfile(
            "image.response.colours-carried-outward.v1",
            "colours travel outward",
        ),
        "shared-silence": FragmentProfile(
            "image.response.shared-silence.v1", "silence becomes shared"
        ),
    },
    line_template="{source}; in answer, {response}.",
    legacy_pairs=LEGACY_IMAGE_PAIRS,
)

SCENT_DOMAIN = DomainProfiles(
    domain_id="scent",
    source_profiles={
        "summer-rain": FragmentProfile(
            "scent.source.summer-rain.v1",
            "The scent of summer rain settles through the forest",
        ),
        "books-and-cedar": FragmentProfile(
            "scent.source.books-and-cedar.v1",
            "The scent of books and cedar lingers among open pages",
        ),
        "evening-salt": FragmentProfile(
            "scent.source.evening-salt.v1",
            "The scent of evening salt gathers along the shore",
        ),
        "first-snow": FragmentProfile(
            "scent.source.first-snow.v1",
            "The air before first snow carries a clear scent",
        ),
        "warm-bread": FragmentProfile(
            "scent.source.warm-bread.v1",
            "The scent of warm bread fills the quiet kitchen",
        ),
    },
    response_profiles={
        "possibility-of-encounter": FragmentProfile(
            "scent.response.possibility-of-encounter.v1",
            "the possibility of encounter opens",
        ),
        "open-books-beside-one-another": FragmentProfile(
            "scent.response.open-books-beside-one-another.v1",
            "two open books rest beside one another",
        ),
        "sense-of-return": FragmentProfile(
            "scent.response.sense-of-return.v1", "a sense of return gathers"
        ),
        "edge-of-beginning": FragmentProfile(
            "scent.response.edge-of-beginning.v1",
            "the edge of a beginning draws near",
        ),
        "second-place-at-table": FragmentProfile(
            "scent.response.second-place-at-table.v1",
            "a second place waits at the table",
        ),
    },
    line_template="{source}; from it, {response}.",
    legacy_pairs=LEGACY_SCENT_PAIRS,
)

MOVEMENT_DOMAIN = DomainProfiles(
    domain_id="movement",
    source_profiles={
        "falling-feather": FragmentProfile(
            "movement.source.falling-feather.v1", "A feather turns as it falls"
        ),
        "loosening-knot": FragmentProfile(
            "movement.source.loosening-knot.v1", "A knot slowly loosens"
        ),
        "returning-tide": FragmentProfile(
            "movement.source.returning-tide.v1", "The tide begins to return"
        ),
        "opening-circle": FragmentProfile(
            "movement.source.opening-circle.v1", "A circle slowly opens"
        ),
        "crossing-light": FragmentProfile(
            "movement.source.crossing-light.v1",
            "A line of light travels across the floor",
        ),
    },
    response_profiles={
        "crossing-feather": FragmentProfile(
            "movement.response.crossing-feather.v1",
            "another feather crosses the air",
        ),
        "gathering-without-tightening": FragmentProfile(
            "movement.response.gathering-without-tightening.v1",
            "threads gather without tightening",
        ),
        "stream-back-to-sea": FragmentProfile(
            "movement.response.stream-back-to-sea.v1",
            "a stream flows back to the sea",
        ),
        "playful-waves": FragmentProfile(
            "movement.response.playful-waves.v1",
            "edges curl into playful waves",
        ),
        "shadow-alongside": FragmentProfile(
            "movement.response.shadow-alongside.v1",
            "a shadow moves alongside",
        ),
    },
    line_template="{source}; in reply, {response}.",
    legacy_pairs=LEGACY_MOVEMENT_PAIRS,
)

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

    image_profile, image_components = _compose_domain_profile(
        artifact.image_id, artifact.image_response_id, IMAGE_DOMAIN
    )
    scent_profile, scent_components = _compose_domain_profile(
        artifact.scent_id, artifact.scent_response_id, SCENT_DOMAIN
    )
    movement_profile, movement_components = _compose_domain_profile(
        artifact.movement_id, artifact.movement_response_id, MOVEMENT_DOMAIN
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
        "profile_component_ids": {
            "image": image_components,
            "scent": scent_components,
            "movement": movement_components,
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


def _compose_domain_profile(
    source_id: str,
    response_id: str,
    domain: DomainProfiles,
) -> tuple[PhraseProfile, dict[str, JsonValue]]:
    try:
        source = domain.source_profiles[source_id]
    except KeyError as error:
        raise CompactGenerationError(
            f"Unsupported {domain.domain_id} source ID: {source_id!r}."
        ) from error
    try:
        response = domain.response_profiles[response_id]
    except KeyError as error:
        raise CompactGenerationError(
            f"Unsupported {domain.domain_id} response ID: {response_id!r}."
        ) from error

    legacy = domain.legacy_pairs.get((source_id, response_id))
    if legacy is not None:
        profile = legacy
        strategy = "legacy-pair-override"
    else:
        profile = PhraseProfile(
            profile_id=(
                f"{domain.domain_id}.composed.{source_id}.{response_id}.v1"
            ),
            line=domain.line_template.format(
                source=source.fragment,
                response=response.fragment,
            ),
        )
        strategy = "composed-source-response"

    components: dict[str, JsonValue] = {
        "source": source.profile_id,
        "response": response.profile_id,
        "strategy": strategy,
    }
    return profile, components


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
