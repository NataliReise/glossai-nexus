#!/usr/bin/env python3
"""Isolated executable composer for the Resonance V0.2 microprototype.

This module is intentionally independent from the V0.1 production opener. It
loads one reviewed building-block library, filters compatible material, creates
an inspectable CompositionPlan, renders a long form, and derives a linked
2/4/6/4/1 Nexus Echo. It performs no semantic analysis of the free words.
"""

from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
import json
from pathlib import Path
import random
import re
from typing import Any, Iterable, Sequence, TypeVar


EXPECTED_LIBRARY_VERSION = "resonance-building-blocks-prototype-v0.2"
EXPECTED_ECHO_COUNTS = (2, 4, 6, 4, 1)
PLAN_VERSION = "resonance-composition-plan-prototype-v0.2"
T = TypeVar("T")


class PrototypeCompositionError(ValueError):
    """Raised when the prototype cannot build a structurally valid composition."""


@dataclass(frozen=True)
class CompositionPlan:
    plan_version: str
    library_version: str
    world_id: str
    completion_mode: str
    route_id: str
    block_ids: tuple[str, ...]
    block_roles: tuple[str, ...]
    operators: tuple[str, ...]
    resonant_gains: tuple[str, ...]
    leaves_states: tuple[str, ...]
    motifs_visible: tuple[str, ...]
    echo_line_ids: tuple[str, ...]
    echo_source_trace: str
    echo_wish_line: int

    def to_dict(self) -> dict[str, Any]:
        value = asdict(self)
        for key, item in tuple(value.items()):
            if isinstance(item, tuple):
                value[key] = list(item)
        return value


@dataclass(frozen=True)
class PrototypeComposition:
    plan: CompositionPlan
    long_form: str
    nexus_echo: str


@dataclass(frozen=True)
class _SelectedBlock:
    role: str
    data: dict[str, Any]
    rendered_text: str


@dataclass(frozen=True)
class _EchoSelection:
    entries: tuple[dict[str, Any], ...]
    rendered_lines: tuple[str, ...]
    source_trace: str
    wish_line: int


def load_library(path: str | Path) -> dict[str, Any]:
    library_path = Path(path)
    try:
        value = json.loads(library_path.read_text(encoding="utf-8"))
    except OSError as error:
        raise PrototypeCompositionError(f"Could not read prototype library: {library_path}") from error
    except json.JSONDecodeError as error:
        raise PrototypeCompositionError(f"Prototype library is not valid JSON: {error.msg}") from error
    validate_library(value)
    return value


def validate_library(library: Any) -> None:
    if not isinstance(library, dict):
        raise PrototypeCompositionError("Prototype library must be a JSON object")
    if library.get("library_version") != EXPECTED_LIBRARY_VERSION:
        raise PrototypeCompositionError(
            f"Unsupported library_version: {library.get('library_version')!r}"
        )
    for field in (
        "world_id",
        "completion_mode",
        "active_tags",
        "required_gain_one_of",
        "forbidden_terminal_states",
        "routes",
        "blocks",
        "echo_line_candidates",
    ):
        if field not in library:
            raise PrototypeCompositionError(f"Prototype library is missing {field!r}")
    if not isinstance(library["routes"], list) or not library["routes"]:
        raise PrototypeCompositionError("Prototype library must contain at least one route")
    if not isinstance(library["blocks"], list) or not library["blocks"]:
        raise PrototypeCompositionError("Prototype library must contain building blocks")

    ids: set[str] = set()
    for block in library["blocks"]:
        if not isinstance(block, dict) or not isinstance(block.get("id"), str):
            raise PrototypeCompositionError("Every building block needs a string id")
        if block["id"] in ids:
            raise PrototypeCompositionError(f"Duplicate building-block id: {block['id']}")
        ids.add(block["id"])
        if not isinstance(block.get("text"), str) or not block["text"].strip():
            raise PrototypeCompositionError(f"Building block {block['id']!r} has no text")
        if not isinstance(block.get("roles"), list) or not block["roles"]:
            raise PrototypeCompositionError(f"Building block {block['id']!r} has no roles")
        if int(block.get("weight", 0)) <= 0:
            raise PrototypeCompositionError(f"Building block {block['id']!r} has invalid weight")


def validate_free_word(value: str, field: str) -> str:
    if not isinstance(value, str) or not value:
        raise PrototypeCompositionError(f"{field} must be one non-empty word")
    if not value.isalpha():
        raise PrototypeCompositionError(f"{field} must contain letters only")
    return value


def poetic_display_word(value: str) -> str:
    return value[:1].upper() + value[1:]


def compose(
    library: dict[str, Any],
    wish_word: str,
    return_word: str,
    *,
    rng: random.Random | None = None,
    max_attempts: int = 300,
) -> PrototypeComposition:
    """Create one valid long form and linked Echo from a reviewed library."""

    validate_library(library)
    wish = poetic_display_word(validate_free_word(wish_word, "wish_word"))
    returned = poetic_display_word(validate_free_word(return_word, "return_word"))
    active_rng = rng if rng is not None else random.Random()

    last_error: Exception | None = None
    for _ in range(max_attempts):
        try:
            route = _weighted_choice(library["routes"], active_rng)
            selected = _select_blocks(library, route, wish, returned, active_rng)
            long_form = _render_long_form(selected)
            aggregate = _aggregate(selected)
            _validate_selected_plan(library, route, selected, long_form, wish, returned, aggregate)
            echo = _select_echo(library, selected, long_form, wish, returned, aggregate, active_rng)
            plan = CompositionPlan(
                plan_version=PLAN_VERSION,
                library_version=library["library_version"],
                world_id=library["world_id"],
                completion_mode=library["completion_mode"],
                route_id=route["id"],
                block_ids=tuple(item.data["id"] for item in selected),
                block_roles=tuple(item.role for item in selected),
                operators=tuple(sorted(aggregate["operators"])),
                resonant_gains=tuple(sorted(aggregate["gains"])),
                leaves_states=tuple(sorted(aggregate["states"])),
                motifs_visible=tuple(sorted(aggregate["motifs"])),
                echo_line_ids=tuple(entry["id"] for entry in echo.entries),
                echo_source_trace=echo.source_trace,
                echo_wish_line=echo.wish_line,
            )
            return PrototypeComposition(
                plan=plan,
                long_form=long_form,
                nexus_echo="\n".join(echo.rendered_lines),
            )
        except PrototypeCompositionError as error:
            last_error = error

    detail = f": {last_error}" if last_error is not None else ""
    raise PrototypeCompositionError(
        f"No valid composition was found after {max_attempts} reviewed attempts{detail}"
    )


def _select_blocks(
    library: dict[str, Any],
    route: dict[str, Any],
    wish: str,
    returned: str,
    rng: random.Random,
) -> tuple[_SelectedBlock, ...]:
    active_tags = set(library["active_tags"])
    completion_mode = library["completion_mode"]
    selected: list[_SelectedBlock] = []
    used_ids: set[str] = set()

    for role in route["roles"]:
        candidates = [
            block
            for block in library["blocks"]
            if role in block.get("roles", [])
            and block["id"] not in used_ids
            and set(block.get("requires_all_tags", [])).issubset(active_tags)
            and completion_mode in block.get("completion_modes", [])
        ]
        if not candidates:
            raise PrototypeCompositionError(
                f"No compatible building block is available for role {role!r}"
            )
        block = _weighted_choice(candidates, rng)
        rendered = _render_template(block["text"], wish, returned)
        selected.append(_SelectedBlock(role=role, data=block, rendered_text=rendered))
        used_ids.add(block["id"])

    return tuple(selected)


def _aggregate(selected: Sequence[_SelectedBlock]) -> dict[str, set[str]]:
    result = {"operators": set(), "gains": set(), "states": set(), "motifs": set()}
    for item in selected:
        result["operators"].update(item.data.get("operators", []))
        result["gains"].update(item.data.get("adds_gains", []))
        result["states"].update(item.data.get("leaves_states", []))
        result["motifs"].update(item.data.get("motifs_visible", []))
    return result


def _render_long_form(selected: Sequence[_SelectedBlock]) -> str:
    # The route remains the structural source of truth. Blank lines only provide
    # a readable 2/2/2/1 prototype presentation and carry no semantic meaning.
    lines: list[str] = []
    for index, item in enumerate(selected, start=1):
        lines.append(item.rendered_text)
        if index in {2, 4, 6} and index != len(selected):
            lines.append("")
    return "\n".join(lines)


def _validate_selected_plan(
    library: dict[str, Any],
    route: dict[str, Any],
    selected: Sequence[_SelectedBlock],
    long_form: str,
    wish: str,
    returned: str,
    aggregate: dict[str, set[str]],
) -> None:
    if tuple(route["roles"]) != tuple(item.role for item in selected):
        raise PrototypeCompositionError("Selected block roles do not match the route")
    expected_occurrences = 2 if wish == returned else 1
    if _word_occurrences(long_form, wish) != expected_occurrences:
        raise PrototypeCompositionError(
            "The long form contains an unexpected wish-word occurrence"
        )
    if _word_occurrences(long_form, returned) != expected_occurrences:
        raise PrototypeCompositionError(
            "The long form contains an unexpected return-word occurrence"
        )
    required = set(library["required_gain_one_of"])
    if not required.intersection(aggregate["gains"]):
        raise PrototypeCompositionError("The selected plan contains no required resonant gain")
    forbidden = set(library["forbidden_terminal_states"])
    if forbidden.intersection(aggregate["states"]):
        raise PrototypeCompositionError("The selected plan contains a forbidden terminal state")
    if not selected[-1].data.get("terminal_allowed", False):
        raise PrototypeCompositionError("The final block is not terminal-eligible")
    if "{wish_word}" in long_form or "{return_word}" in long_form:
        raise PrototypeCompositionError("The long form contains unresolved placeholders")


def _select_echo(
    library: dict[str, Any],
    selected: Sequence[_SelectedBlock],
    long_form: str,
    wish: str,
    returned: str,
    aggregate: dict[str, set[str]],
    rng: random.Random,
) -> _EchoSelection:
    document = library["echo_line_candidates"]
    selected_ids = {item.data["id"] for item in selected}

    first_candidates = [
        item
        for item in document.get("line_1", [])
        if _echo_candidate_available(item, selected_ids, aggregate)
    ]
    if not first_candidates:
        raise PrototypeCompositionError("No linked Echo opening is available")

    middle_by_line: dict[int, list[dict[str, Any]]] = {2: [], 3: [], 4: []}
    for item in document.get("line_2_to_4", []):
        line = item.get("line")
        if line in middle_by_line and _echo_candidate_available(
            item, selected_ids, aggregate
        ):
            middle_by_line[line].append(item)
    if any(not middle_by_line[line] for line in (2, 3, 4)):
        raise PrototypeCompositionError(
            "The selected long form has no complete linked Echo route"
        )

    final_candidates = document.get("line_5", [])
    if not final_candidates:
        raise PrototypeCompositionError("No final return-word Echo line is available")

    combinations: list[tuple[list[dict[str, Any]], str, int, int]] = []
    for line2 in middle_by_line[2]:
        for line3 in middle_by_line[3]:
            for line4 in middle_by_line[4]:
                middle = [line2, line3, line4]
                wish_entries = [entry for entry in middle if entry.get("wish_slot") is True]
                if len(wish_entries) != 1:
                    continue
                rendered_middle = [
                    _render_template(entry["text"], wish, returned) for entry in middle
                ]
                trace = _longest_shared_phrase(
                    long_form, rendered_middle, minimum_words=2
                )
                if not trace:
                    continue
                weight = 1
                for entry in middle:
                    weight *= int(entry.get("weight", 1))
                combinations.append(
                    (middle, trace, int(wish_entries[0]["line"]), weight)
                )

    if not combinations:
        raise PrototypeCompositionError(
            "No Echo combination inherits a concrete lexical trace"
        )

    first = _weighted_choice(first_candidates, rng)
    middle, trace, wish_line, _ = _weighted_choice(
        combinations, rng, weight_getter=lambda item: item[3]
    )
    final = _weighted_choice(final_candidates, rng)
    entries = (first, *middle, final)
    lines = tuple(_render_template(entry["text"], wish, returned) for entry in entries)
    _validate_echo(lines, wish, returned, trace)
    return _EchoSelection(
        entries=entries,
        rendered_lines=lines,
        source_trace=trace,
        wish_line=wish_line,
    )


def _echo_candidate_available(
    candidate: dict[str, Any],
    selected_ids: set[str],
    aggregate: dict[str, set[str]],
) -> bool:
    required_all = set(candidate.get("source_block_ids_all", []))
    if required_all and not required_all.issubset(selected_ids):
        return False
    required_any = set(candidate.get("source_block_ids_any", []))
    if required_any and not required_any.intersection(selected_ids):
        return False
    motifs_any = set(candidate.get("requires_visible_motifs_any", []))
    if motifs_any and not motifs_any.intersection(aggregate["motifs"]):
        return False
    operators_any = set(candidate.get("inherits_operators_any", []))
    if operators_any and not operators_any.intersection(aggregate["operators"]):
        return False
    return True


def _validate_echo(lines: Sequence[str], wish: str, returned: str, trace: str) -> None:
    if len(lines) != 5:
        raise PrototypeCompositionError("The Nexus Echo must contain exactly five lines")
    counts = tuple(_word_count(line) for line in lines)
    if counts != EXPECTED_ECHO_COUNTS:
        raise PrototypeCompositionError(
            f"Invalid Nexus Echo word counts: {counts}; expected {EXPECTED_ECHO_COUNTS}"
        )
    expected_occurrences = 2 if wish == returned else 1
    echo_text = "\n".join(lines)
    if _word_occurrences(echo_text, wish) != expected_occurrences:
        raise PrototypeCompositionError(
            "The Nexus Echo contains an unexpected wish-word occurrence"
        )
    if lines[-1] != returned:
        raise PrototypeCompositionError(
            "The return word must be the complete final Echo line"
        )
    if _word_occurrences(echo_text, returned) != expected_occurrences:
        raise PrototypeCompositionError(
            "The Nexus Echo contains an unexpected return-word occurrence"
        )
    if any(
        not all(character.isalpha() or character.isspace() for character in line)
        for line in lines
    ):
        raise PrototypeCompositionError("The Nexus Echo must remain punctuation-free")
    if trace.lower() not in " ".join(lines).lower():
        raise PrototypeCompositionError("The recorded Echo trace is not visible in the Echo")


def _render_template(template: str, wish: str, returned: str) -> str:
    rendered = template.replace("{wish_word}", wish).replace(
        "{return_word}", returned
    )
    if "{" in rendered or "}" in rendered:
        raise PrototypeCompositionError(
            f"Unresolved placeholder in template: {template!r}"
        )
    return rendered


def _weighted_choice(
    items: Sequence[T],
    rng: random.Random,
    *,
    weight_getter: Any = lambda item: int(item.get("weight", 1)),
) -> T:
    if not items:
        raise PrototypeCompositionError("Cannot choose from an empty candidate pool")
    weights = [max(0, int(weight_getter(item))) for item in items]
    if not any(weights):
        raise PrototypeCompositionError("Candidate pool contains no positive weight")
    return rng.choices(list(items), weights=weights, k=1)[0]


def _word_count(text: str) -> int:
    return len(re.findall(r"[^\W_]+", text, flags=re.UNICODE))


def _word_occurrences(text: str, word: str) -> int:
    return sum(
        token == word
        for token in re.findall(r"[^\W_]+", text, flags=re.UNICODE)
    )


def _tokenise(text: str) -> list[str]:
    return [
        token.lower()
        for token in re.findall(r"[^\W_]+", text, flags=re.UNICODE)
    ]


def _longest_shared_phrase(
    long_form: str, echo_lines: Iterable[str], minimum_words: int
) -> str:
    long_lines = [_tokenise(line) for line in long_form.splitlines() if line.strip()]
    best: list[str] = []
    for echo_line in echo_lines:
        echo_tokens = _tokenise(echo_line)
        for size in range(len(echo_tokens), minimum_words - 1, -1):
            for start in range(0, len(echo_tokens) - size + 1):
                phrase = echo_tokens[start : start + size]
                if len(phrase) <= len(best):
                    continue
                if any(
                    _contains_subsequence(line_tokens, phrase)
                    for line_tokens in long_lines
                ):
                    best = phrase
    return " ".join(best)


def _contains_subsequence(tokens: Sequence[str], phrase: Sequence[str]) -> bool:
    size = len(phrase)
    return any(
        list(tokens[index : index + size]) == list(phrase)
        for index in range(len(tokens) - size + 1)
    )


def _default_library_path() -> Path:
    return Path(__file__).resolve().with_name(
        "building_blocks.mixed_threshold_return.prototype.json"
    )


def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run the isolated Resonance V0.2 poetry composer prototype"
    )
    parser.add_argument("--library", type=Path, default=_default_library_path())
    parser.add_argument("--wish", required=True)
    parser.add_argument("--return-word", required=True)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--count", type=int, default=1)
    parser.add_argument("--show-plan", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)
    if args.count < 1:
        print("Error: --count must be at least 1")
        return 2
    try:
        library = load_library(args.library)
        rng = random.Random(args.seed)
        for index in range(args.count):
            result = compose(library, args.wish, args.return_word, rng=rng)
            if index:
                print("\n" + "=" * 72 + "\n")
            print("Resonance Artifact")
            print("==================\n")
            print(result.long_form)
            print("\nNexus Echo")
            print("==========\n")
            print(result.nexus_echo)
            if args.show_plan:
                print("\nComposition Plan")
                print("================\n")
                print(json.dumps(result.plan.to_dict(), indent=2, ensure_ascii=False))
    except PrototypeCompositionError as error:
        print(f"Error: {error}")
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
