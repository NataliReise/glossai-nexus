#!/usr/bin/env python3
"""Isolated compact resonance-text composer experiment V0.4."""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import asdict, dataclass
import hashlib
import json
from pathlib import Path
import random
import re
from typing import Any, Mapping, Sequence, TypeVar


LIBRARY_VERSION = "resonance-composition-profiles-v0.4"
WORD_PATTERN = (2, 4, 6, 4, 1)
SOURCE_FIELDS = (
    "image_id",
    "image_response_id",
    "scent_id",
    "scent_response_id",
    "movement_id",
    "movement_response_id",
)
PROFILE_KINDS = tuple(field.removesuffix("_id") for field in SOURCE_FIELDS)
FREE_WORD_FIELDS = ("wish_word", "return_word")
DEFAULT_LIBRARY = Path(__file__).with_name("profiles.v0_4.json")
PLACEHOLDER_RE = re.compile(r"\{([^{}]+)\}")
VISIBLE_LINE_RE = re.compile(r"[^\W\d_]+(?: [^\W\d_]+)*", re.UNICODE)
T = TypeVar("T")


class CompositionError(ValueError):
    """Raised for unsupported input, malformed data, or invalid output."""


@dataclass(frozen=True)
class ResonanceReturnArtifact:
    image_id: str
    image_response_id: str
    scent_id: str
    scent_response_id: str
    movement_id: str
    movement_response_id: str
    wish_word: str
    return_word: str

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> "ResonanceReturnArtifact":
        if not isinstance(value, Mapping):
            raise CompositionError("Return Artifact must be an object")
        missing = [field for field in (*SOURCE_FIELDS, *FREE_WORD_FIELDS) if field not in value]
        if missing:
            raise CompositionError("Return Artifact is missing: " + ", ".join(missing))
        return cls(**{field: value[field] for field in (*SOURCE_FIELDS, *FREE_WORD_FIELDS)})

    def source_ids(self) -> tuple[tuple[str, str], ...]:
        return tuple((field, getattr(self, field)) for field in SOURCE_FIELDS)


@dataclass(frozen=True)
class CompositionPlan:
    library_version: str
    source_artifact_ids: tuple[tuple[str, str], ...]
    world_id: str
    route_id: str
    selected_profile_ids: tuple[str, ...]
    selected_variant_ids: tuple[str, ...]
    seed: int | None
    rendered_text: str
    trace_id: str

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["source_artifact_ids"] = dict(self.source_artifact_ids)
        data["selected_profile_ids"] = list(self.selected_profile_ids)
        data["selected_variant_ids"] = list(self.selected_variant_ids)
        return data


@dataclass(frozen=True)
class Composition:
    text: str
    lines: tuple[str, ...]
    plan: CompositionPlan


def load_library(path: str | Path = DEFAULT_LIBRARY) -> dict[str, Any]:
    library_path = Path(path)
    try:
        data = json.loads(library_path.read_text(encoding="utf-8"))
    except OSError as error:
        raise CompositionError(f"Could not read profile library: {library_path}") from error
    except json.JSONDecodeError as error:
        raise CompositionError(f"Profile library is not valid JSON: {error.msg}") from error
    validate_library(data)
    return data


def validate_free_word(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value:
        raise CompositionError(f"{field} must be one non-empty word")
    if not value.isalpha():
        raise CompositionError(f"{field} must contain letters only")
    return value


def poetic_display(value: str) -> str:
    return value[:1].upper() + value[1:]


def validate_library(data: Any) -> None:
    if not isinstance(data, dict):
        raise CompositionError("Profile library root must be an object")
    if data.get("library_version") != LIBRARY_VERSION:
        raise CompositionError("Unsupported library_version")
    form = data.get("form")
    if not isinstance(form, dict) or tuple(form.get("word_pattern", ())) != WORD_PATTERN:
        raise CompositionError("Profile library must declare the 2/4/6/4/1 form")
    if form.get("max_visible_words") != 25:
        raise CompositionError("Profile library must declare max_visible_words 25")

    routes = data.get("routes")
    worlds = data.get("supported_worlds")
    profiles = data.get("profiles")
    if not isinstance(routes, list) or not routes:
        raise CompositionError("Profile library requires routes")
    if not isinstance(worlds, list) or not worlds:
        raise CompositionError("Profile library requires supported_worlds")
    if not isinstance(profiles, dict) or set(profiles) != set(PROFILE_KINDS):
        raise CompositionError("Profile library must define exactly the six profile kinds")

    seen_ids: set[str] = set()
    role_word_counts: dict[tuple[str, str], set[int]] = {}
    profile_index: dict[tuple[str, str], dict[str, Any]] = {}
    for kind in PROFILE_KINDS:
        entries = profiles[kind]
        if not isinstance(entries, list) or not entries:
            raise CompositionError(f"Profile kind {kind!r} must be a non-empty list")
        for profile in entries:
            if not isinstance(profile, dict):
                raise CompositionError(f"Each {kind} profile must be an object")
            profile_id = _require_unique_id(profile, seen_ids, f"{kind} profile")
            source_id = profile.get("source_id")
            roles = profile.get("roles")
            if not isinstance(source_id, str) or not source_id:
                raise CompositionError(f"{profile_id} requires source_id")
            if (kind, source_id) in profile_index:
                raise CompositionError(f"Duplicate {kind} source_id: {source_id}")
            if not isinstance(roles, dict) or not roles:
                raise CompositionError(f"{profile_id} requires roles")
            profile_index[(kind, source_id)] = profile
            for role, variants in roles.items():
                if not isinstance(role, str) or not isinstance(variants, list) or not variants:
                    raise CompositionError(f"{profile_id} has malformed role {role!r}")
                counts = role_word_counts.setdefault((kind, role), set())
                for variant in variants:
                    _validate_variant(variant, seen_ids, profile_id)
                    counts.add(_word_count(variant["text"]))
                if len(counts) != 1:
                    raise CompositionError(f"{kind}.{role} variants must have one word count")

    route_ids: set[str] = set()
    for route in routes:
        if not isinstance(route, dict):
            raise CompositionError("Each route must be an object")
        route_id = _require_unique_id(route, seen_ids, "route")
        route_ids.add(route_id)
        _require_weight(route, route_id)
        wish_line = route.get("wish_line")
        lines = route.get("lines")
        if wish_line not in {2, 3, 4}:
            raise CompositionError(f"{route_id} has invalid wish_line")
        if not isinstance(lines, list) or len(lines) != 4:
            raise CompositionError(f"{route_id} requires four pre-return lines")
        used_kinds: list[str] = []
        wish_slots: list[int] = []
        for line_number, template in enumerate(lines, start=1):
            if not isinstance(template, str) or not template:
                raise CompositionError(f"{route_id} line {line_number} is invalid")
            placeholders = PLACEHOLDER_RE.findall(template)
            if PLACEHOLDER_RE.sub("", template).strip():
                raise CompositionError(f"{route_id} line {line_number} contains uncurated literal text")
            expected = 0
            for placeholder in placeholders:
                if placeholder == "wish_word":
                    expected += 1
                    wish_slots.append(line_number)
                    continue
                parts = placeholder.split(".")
                if len(parts) != 2 or tuple(parts) not in role_word_counts:
                    raise CompositionError(f"{route_id} has unknown placeholder {placeholder!r}")
                used_kinds.append(parts[0])
                expected += next(iter(role_word_counts[tuple(parts)]))
            if expected != WORD_PATTERN[line_number - 1]:
                raise CompositionError(
                    f"{route_id} line {line_number} renders {expected} words; expected {WORD_PATTERN[line_number - 1]}"
                )
        if wish_slots != [wish_line]:
            raise CompositionError(f"{route_id} does not preserve its declared wish slot")
        if Counter(used_kinds) != Counter(PROFILE_KINDS):
            raise CompositionError(f"{route_id} must use every source profile exactly once")

    seen_worlds: set[str] = set()
    seen_tuples: set[tuple[str, ...]] = set()
    for world in worlds:
        if not isinstance(world, dict):
            raise CompositionError("Each supported world must be an object")
        world_id = world.get("id")
        if not isinstance(world_id, str) or not world_id or world_id in seen_worlds:
            raise CompositionError("Supported world IDs must be unique non-empty strings")
        seen_worlds.add(world_id)
        source_tuple: list[str] = []
        for field, kind in zip(SOURCE_FIELDS, PROFILE_KINDS):
            source_id = world.get(field)
            if not isinstance(source_id, str) or (kind, source_id) not in profile_index:
                raise CompositionError(f"{world_id} has unknown {field}")
            source_tuple.append(source_id)
        identity = tuple(source_tuple)
        if identity in seen_tuples:
            raise CompositionError(f"Duplicate supported source tuple: {world_id}")
        seen_tuples.add(identity)
        for route in routes:
            for template in route["lines"]:
                for placeholder in PLACEHOLDER_RE.findall(template):
                    if placeholder == "wish_word":
                        continue
                    kind, role = placeholder.split(".")
                    profile = profile_index[(kind, world[f"{kind}_id"])]
                    if role not in profile["roles"]:
                        raise CompositionError(
                            f"{profile['id']} lacks role {role!r} required by {route['id']}"
                        )


def _validate_variant(variant: Any, seen_ids: set[str], profile_id: str) -> None:
    if not isinstance(variant, dict):
        raise CompositionError(f"{profile_id} contains a non-object variant")
    variant_id = _require_unique_id(variant, seen_ids, "variant")
    _require_weight(variant, variant_id)
    text = variant.get("text")
    verb = variant.get("content_verb")
    nouns = variant.get("visible_nouns")
    if not isinstance(text, str) or not VISIBLE_LINE_RE.fullmatch(text):
        raise CompositionError(f"{variant_id} text must contain letter words and spaces only")
    if "{" in text or "}" in text:
        raise CompositionError(f"{variant_id} contains a placeholder")
    if verb is not None and (not isinstance(verb, str) or not verb.isalpha()):
        raise CompositionError(f"{variant_id} has invalid content_verb")
    if not isinstance(nouns, list) or any(not isinstance(noun, str) or not noun.isalpha() for noun in nouns):
        raise CompositionError(f"{variant_id} has invalid visible_nouns")
    visible_tokens = {token.casefold() for token in text.split()}
    if any(noun.casefold() not in visible_tokens for noun in nouns):
        raise CompositionError(f"{variant_id} annotates a noun not visible in its text")


def _require_unique_id(item: dict[str, Any], seen: set[str], context: str) -> str:
    item_id = item.get("id")
    if not isinstance(item_id, str) or not item_id:
        raise CompositionError(f"Every {context} requires an id")
    if item_id in seen:
        raise CompositionError(f"Duplicate id: {item_id}")
    seen.add(item_id)
    return item_id


def _require_weight(item: dict[str, Any], context: str) -> None:
    weight = item.get("weight")
    if not isinstance(weight, int) or isinstance(weight, bool) or weight <= 0:
        raise CompositionError(f"{context} requires a positive integer weight")


def compose(
    artifact: ResonanceReturnArtifact | Mapping[str, Any],
    *,
    library: dict[str, Any] | None = None,
    seed: int | None = None,
    max_attempts: int = 200,
) -> Composition:
    data = library if library is not None else load_library()
    validate_library(data)
    source = artifact if isinstance(artifact, ResonanceReturnArtifact) else ResonanceReturnArtifact.from_mapping(artifact)
    if not isinstance(seed, (int, type(None))) or isinstance(seed, bool):
        raise CompositionError("seed must be an integer or null")
    if not isinstance(max_attempts, int) or isinstance(max_attempts, bool) or max_attempts < 1:
        raise CompositionError("max_attempts must be a positive integer")
    wish_raw = validate_free_word(source.wish_word, "wish_word")
    return_raw = validate_free_word(source.return_word, "return_word")
    wish = poetic_display(wish_raw)
    returned = poetic_display(return_raw)

    world = _resolve_world(data, source)
    profile_index = {
        (kind, profile["source_id"]): profile
        for kind, profiles in data["profiles"].items()
        for profile in profiles
    }
    selected_profiles = {
        kind: profile_index[(kind, getattr(source, field))]
        for field, kind in zip(SOURCE_FIELDS, PROFILE_KINDS)
    }
    rng = random.Random(seed)
    collision_words = {wish.casefold(), returned.casefold()}
    last_reason = "no candidate was attempted"

    for _ in range(max_attempts):
        route = _weighted_choice(data["routes"], rng)
        variants: dict[str, dict[str, Any]] = {}
        try:
            for template in route["lines"]:
                for placeholder in PLACEHOLDER_RE.findall(template):
                    if placeholder == "wish_word" or placeholder in variants:
                        continue
                    kind, role = placeholder.split(".")
                    candidates = [
                        variant
                        for variant in selected_profiles[kind]["roles"][role]
                        if collision_words.isdisjoint(
                            token.casefold() for token in variant["text"].split()
                        )
                    ]
                    variants[placeholder] = _weighted_choice(candidates, rng)
            lines, line_verbs, visible_nouns = _render_route(route, variants, wish, returned)
            _validate_rendered(lines, route, wish, returned, line_verbs, visible_nouns)
        except CompositionError as error:
            last_reason = str(error)
            continue

        text = "\n".join(lines)
        variant_ids = tuple(variants[key]["id"] for key in sorted(variants))
        profile_ids = tuple(selected_profiles[kind]["id"] for kind in PROFILE_KINDS)
        trace_payload = {
            "library_version": data["library_version"],
            "source_ids": dict(source.source_ids()),
            "route_id": route["id"],
            "variant_ids": variant_ids,
            "seed": seed,
            "text": text,
        }
        digest = hashlib.sha256(
            json.dumps(trace_payload, ensure_ascii=False, sort_keys=True).encode("utf-8")
        ).hexdigest()[:12]
        plan = CompositionPlan(
            library_version=data["library_version"],
            source_artifact_ids=source.source_ids(),
            world_id=world["id"],
            route_id=route["id"],
            selected_profile_ids=profile_ids,
            selected_variant_ids=variant_ids,
            seed=seed,
            rendered_text=text,
            trace_id=f"v04-{digest}",
        )
        return Composition(text=text, lines=lines, plan=plan)

    raise CompositionError(
        f"No structurally valid composition found after {max_attempts} local attempts: {last_reason}"
    )


def _resolve_world(data: dict[str, Any], artifact: ResonanceReturnArtifact) -> dict[str, Any]:
    expected = tuple(getattr(artifact, field) for field in SOURCE_FIELDS)
    for world in data["supported_worlds"]:
        if tuple(world[field] for field in SOURCE_FIELDS) == expected:
            return world
    joined = ", ".join(f"{field}={value!r}" for field, value in artifact.source_ids())
    raise CompositionError(f"Unsupported Return Artifact ID combination: {joined}")


def _render_route(
    route: dict[str, Any],
    variants: dict[str, dict[str, Any]],
    wish: str,
    returned: str,
) -> tuple[tuple[str, ...], tuple[frozenset[str], ...], tuple[str, ...]]:
    lines: list[str] = []
    line_verbs: list[frozenset[str]] = []
    visible_nouns: list[str] = []
    for template in route["lines"]:
        verbs: set[str] = set()

        def replace(match: re.Match[str]) -> str:
            key = match.group(1)
            if key == "wish_word":
                return wish
            if key not in variants:
                raise CompositionError(f"Unresolved placeholder: {key}")
            variant = variants[key]
            if variant["content_verb"]:
                verbs.add(variant["content_verb"].casefold())
            visible_nouns.extend(noun.casefold() for noun in variant["visible_nouns"])
            return variant["text"]

        rendered = PLACEHOLDER_RE.sub(replace, template)
        if "{" in rendered or "}" in rendered:
            raise CompositionError("Rendered text contains an unresolved placeholder")
        lines.append(rendered)
        line_verbs.append(frozenset(verbs))
    lines.append(returned)
    line_verbs.append(frozenset())
    return tuple(lines), tuple(line_verbs), tuple(visible_nouns)


def _validate_rendered(
    lines: tuple[str, ...],
    route: dict[str, Any],
    wish: str,
    returned: str,
    line_verbs: tuple[frozenset[str], ...],
    visible_nouns: tuple[str, ...],
) -> None:
    if len(lines) != 5:
        raise CompositionError("Compact result must contain exactly five lines")
    if sum(_word_count(line) for line in lines) > 25:
        raise CompositionError("Compact result exceeds 25 visible words")
    for number, (line, expected) in enumerate(zip(lines, WORD_PATTERN), start=1):
        if _word_count(line) != expected:
            raise CompositionError(f"Rendered line {number} has invalid word count")
        if not VISIBLE_LINE_RE.fullmatch(line):
            raise CompositionError(f"Rendered line {number} contains invalid visible characters")
    wish_positions = [
        number
        for number, line in enumerate(lines[:4], start=1)
        if wish.casefold() in (token.casefold() for token in line.split())
    ]
    if wish_positions != [route["wish_line"]]:
        raise CompositionError("Wish word is not confined to its intended slot")
    if lines[-1] != returned:
        raise CompositionError("Return word must be the deliberate final line")
    if wish.casefold() != returned.casefold() and any(
        returned.casefold() == token.casefold()
        for line in lines[:4]
        for token in line.split()
    ):
        raise CompositionError("Return word appears before its ending")
    for first, second in zip(line_verbs, line_verbs[1:]):
        repeated = first.intersection(second)
        if repeated:
            raise CompositionError(
                "Adjacent lines repeat content verb: " + ", ".join(sorted(repeated))
            )
    excessive = sorted(noun for noun, count in Counter(visible_nouns).items() if count > 2)
    if excessive:
        raise CompositionError("Visible noun repeats excessively: " + ", ".join(excessive))


def _weighted_choice(items: Sequence[T], rng: random.Random) -> T:
    if not items:
        raise CompositionError("No collision-free curated variant is available")
    weights = [int(item["weight"]) for item in items]  # type: ignore[index]
    return rng.choices(list(items), weights=weights, k=1)[0]


def _word_count(text: str) -> int:
    return len(text.split())


def artifact_for_world(data: dict[str, Any], world_id: str, wish: str, returned: str) -> ResonanceReturnArtifact:
    for world in data["supported_worlds"]:
        if world["id"] == world_id:
            return ResonanceReturnArtifact(
                **{field: world[field] for field in SOURCE_FIELDS},
                wish_word=wish,
                return_word=returned,
            )
    raise CompositionError(f"Unknown supported world: {world_id!r}")


def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Compose one isolated V0.4 resonance text")
    parser.add_argument("--world", required=True)
    parser.add_argument("--wish", required=True)
    parser.add_argument("--return-word", required=True)
    parser.add_argument("--seed", type=int)
    parser.add_argument("--library", type=Path, default=DEFAULT_LIBRARY)
    parser.add_argument("--show-plan", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)
    try:
        library = load_library(args.library)
        artifact = artifact_for_world(library, args.world, args.wish, args.return_word)
        result = compose(artifact, library=library, seed=args.seed)
    except CompositionError as error:
        print(f"Error: {error}")
        return 2
    print(result.text)
    if args.show_plan:
        print()
        print(json.dumps(result.plan.to_dict(), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
