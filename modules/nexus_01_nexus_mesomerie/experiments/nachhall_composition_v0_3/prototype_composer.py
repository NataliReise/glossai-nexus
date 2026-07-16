#!/usr/bin/env python3
"""Compose one compact 2/4/6/4/1 Nachhall from a curated V0.3 library.

This experiment is intentionally isolated from the active Return Resonance paths.
It performs no semantic analysis and does not persist production results.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import json
from pathlib import Path
import random
import re
from typing import Any, Sequence, TypeVar

EXPECTED_LIBRARY_VERSION = "nachhall-composition-prototype-v0.3"
EXPECTED_PATTERN = (2, 4, 6, 4, 1)
DEFAULT_LIBRARY = Path(__file__).with_name(
    "nachhall_library.mixed_threshold_return.prototype.json"
)
T = TypeVar("T")


class NachhallCompositionError(ValueError):
    """Raised when input, library data, or a rendered poem is invalid."""


@dataclass(frozen=True)
class NachhallPlan:
    library_version: str
    world_id: str
    route_id: str
    wish_line: int
    line_variant_ids: tuple[str, str, str, str]
    seed: int | None


@dataclass(frozen=True)
class NachhallComposition:
    poem: str
    lines: tuple[str, str, str, str, str]
    plan: NachhallPlan


def load_library(path: str | Path = DEFAULT_LIBRARY) -> dict[str, Any]:
    library_path = Path(path)
    try:
        data = json.loads(library_path.read_text(encoding="utf-8"))
    except FileNotFoundError as error:
        raise NachhallCompositionError(f"Library not found: {library_path}") from error
    except json.JSONDecodeError as error:
        raise NachhallCompositionError(f"Library is not valid JSON: {error}") from error

    validate_library(data)
    return data


def validate_free_word(value: str, field: str) -> str:
    if not isinstance(value, str) or not value:
        raise NachhallCompositionError(f"{field} must be one non-empty word")
    if not value.isalpha():
        raise NachhallCompositionError(f"{field} must contain letters only")
    return value


def poetic_display(value: str) -> str:
    return value[:1].upper() + value[1:]


def word_count(line: str) -> int:
    return len(line.split())


def validate_library(data: dict[str, Any]) -> None:
    if not isinstance(data, dict):
        raise NachhallCompositionError("Library root must be an object")
    if data.get("library_version") != EXPECTED_LIBRARY_VERSION:
        raise NachhallCompositionError("Unsupported library_version")

    form = data.get("form")
    if not isinstance(form, dict) or tuple(form.get("word_pattern", ())) != EXPECTED_PATTERN:
        raise NachhallCompositionError("Library must declare the 2/4/6/4/1 form")

    line_1 = data.get("line_1_variants")
    routes = data.get("routes")
    if not isinstance(line_1, list) or not line_1:
        raise NachhallCompositionError("Library requires line_1_variants")
    if not isinstance(routes, list) or not routes:
        raise NachhallCompositionError("Library requires routes")

    seen_ids: set[str] = set()
    _validate_variants(line_1, 1, False, seen_ids)

    allowed_wish_lines = set(form.get("wish_slot_lines", ()))
    for route in routes:
        if not isinstance(route, dict):
            raise NachhallCompositionError("Each route must be an object")
        route_id = _require_id(route, seen_ids)
        wish_line = route.get("wish_line")
        if wish_line not in allowed_wish_lines:
            raise NachhallCompositionError(f"Invalid wish_line in {route_id}")
        _require_positive_weight(route, route_id)

        for line_number in (2, 3, 4):
            key = f"line_{line_number}_variants"
            variants = route.get(key)
            if not isinstance(variants, list) or not variants:
                raise NachhallCompositionError(f"{route_id} requires {key}")
            _validate_variants(
                variants,
                line_number,
                line_number == wish_line,
                seen_ids,
            )


def _validate_variants(
    variants: list[Any],
    line_number: int,
    requires_wish: bool,
    seen_ids: set[str],
) -> None:
    expected_count = EXPECTED_PATTERN[line_number - 1]
    for variant in variants:
        if not isinstance(variant, dict):
            raise NachhallCompositionError("Each variant must be an object")
        variant_id = _require_id(variant, seen_ids)
        _require_positive_weight(variant, variant_id)
        text = variant.get("text")
        if not isinstance(text, str) or not text.strip():
            raise NachhallCompositionError(f"Missing text in {variant_id}")
        placeholder_count = text.count("{wish_word}")
        if placeholder_count != (1 if requires_wish else 0):
            raise NachhallCompositionError(
                f"{variant_id} has an invalid wish_word placeholder count"
            )
        rendered = text.format(wish_word="Wish")
        _validate_visible_line(rendered, expected_count, variant_id)


def _require_id(item: dict[str, Any], seen_ids: set[str]) -> str:
    item_id = item.get("id")
    if not isinstance(item_id, str) or not item_id:
        raise NachhallCompositionError("Every route and variant requires an id")
    if item_id in seen_ids:
        raise NachhallCompositionError(f"Duplicate id: {item_id}")
    seen_ids.add(item_id)
    return item_id


def _require_positive_weight(item: dict[str, Any], item_id: str) -> None:
    weight = item.get("weight")
    if not isinstance(weight, int) or isinstance(weight, bool) or weight <= 0:
        raise NachhallCompositionError(f"{item_id} requires a positive integer weight")


def compose(
    wish_word: str,
    return_word: str,
    *,
    library: dict[str, Any] | None = None,
    seed: int | None = None,
) -> NachhallComposition:
    wish = poetic_display(validate_free_word(wish_word, "wish_word"))
    returned = poetic_display(validate_free_word(return_word, "return_word"))
    data = library if library is not None else load_library()
    validate_library(data)

    rng = random.Random(seed)
    line_1_variant = _weighted_choice(data["line_1_variants"], rng)
    route = _weighted_choice(data["routes"], rng)
    chosen = [
        line_1_variant,
        _weighted_choice(route["line_2_variants"], rng),
        _weighted_choice(route["line_3_variants"], rng),
        _weighted_choice(route["line_4_variants"], rng),
    ]

    lines = tuple(
        variant["text"].format(wish_word=wish) for variant in chosen
    ) + (returned,)
    _validate_poem(lines, wish, returned, int(route["wish_line"]))

    world = data.get("world")
    if not isinstance(world, dict) or not isinstance(world.get("id"), str):
        raise NachhallCompositionError("Library requires world.id")

    plan = NachhallPlan(
        library_version=data["library_version"],
        world_id=world["id"],
        route_id=route["id"],
        wish_line=int(route["wish_line"]),
        line_variant_ids=tuple(variant["id"] for variant in chosen),
        seed=seed,
    )
    return NachhallComposition(poem="\n".join(lines), lines=lines, plan=plan)


def _weighted_choice(items: Sequence[T], rng: random.Random) -> T:
    if not items:
        raise NachhallCompositionError("Cannot choose from an empty collection")
    weights = [int(item["weight"]) for item in items]  # type: ignore[index]
    return rng.choices(list(items), weights=weights, k=1)[0]


def _validate_poem(
    lines: tuple[str, ...],
    wish: str,
    returned: str,
    wish_line: int,
) -> None:
    if len(lines) != 5:
        raise NachhallCompositionError("A Nachhall must contain exactly five lines")
    for index, (line, expected) in enumerate(zip(lines, EXPECTED_PATTERN), start=1):
        _validate_visible_line(line, expected, f"rendered line {index}")

    wish_occurrences = [
        index for index, line in enumerate(lines, start=1) if wish in line.split()
    ]
    if wish_occurrences != [wish_line]:
        raise NachhallCompositionError("Wish word is not confined to its declared line")
    if lines[4] != returned:
        raise NachhallCompositionError("Return word must be the complete fifth line")


def _validate_visible_line(line: str, expected_count: int, context: str) -> None:
    if word_count(line) != expected_count:
        raise NachhallCompositionError(
            f"{context} has {word_count(line)} words; expected {expected_count}"
        )
    if not re.fullmatch(r"[^\W\d_]+(?: [^\W\d_]+)*", line, flags=re.UNICODE):
        raise NachhallCompositionError(
            f"{context} must contain only letter words separated by spaces"
        )


def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Compose one experimental Nachhall")
    parser.add_argument("wish_word")
    parser.add_argument("return_word")
    parser.add_argument("--seed", type=int)
    parser.add_argument("--library", type=Path, default=DEFAULT_LIBRARY)
    parser.add_argument("--show-plan", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)
    try:
        result = compose(
            args.wish_word,
            args.return_word,
            library=load_library(args.library),
            seed=args.seed,
        )
    except NachhallCompositionError as error:
        print(f"Error: {error}")
        return 2

    print(result.poem)
    if args.show_plan:
        print()
        print(json.dumps(result.plan.__dict__, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
