#!/usr/bin/env python3
"""Policy layer for the isolated Resonance V0.2 composer.

Ordinary word pairs continue through ``prototype_composer.compose`` unchanged.
Lexically identical pairs use a curated same-word route: a proxy carries the
wish role, while the shared input remains the single visible return word.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
import random
from typing import Any, Sequence

import prototype_composer as base
from same_word_policy import (
    SameWordPolicyError,
    WishRoleProxy,
    choose_wish_role_proxy,
    validate_exact_line_repetition,
    words_are_identical,
)

DEFAULT_PROXIES = (
    WishRoleProxy("first-trace", "the first trace", 3),
    WishRoleProxy("opening-trace", "the opening trace", 2),
)


@dataclass(frozen=True)
class PolicyCompositionPlan:
    base_plan: dict[str, Any]
    same_word_mode: bool
    original_wish_word: str
    original_return_word: str
    wish_role_proxy_id: str | None
    wish_role_proxy_text: str | None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class PolicyComposition:
    plan: PolicyCompositionPlan
    long_form: str
    nexus_echo: str


def compose(
    library: dict[str, Any],
    wish_word: str,
    return_word: str,
    *,
    rng: random.Random | None = None,
    proxies: Sequence[WishRoleProxy] = DEFAULT_PROXIES,
) -> PolicyComposition:
    """Compose normally or activate the narrow same-word route."""
    base.validate_library(library)
    raw_wish = base.validate_free_word(wish_word, "wish_word")
    raw_return = base.validate_free_word(return_word, "return_word")
    active_rng = rng if rng is not None else random.Random()

    if not words_are_identical(raw_wish, raw_return):
        result = base.compose(library, raw_wish, raw_return, rng=active_rng)
        return PolicyComposition(
            plan=PolicyCompositionPlan(
                base_plan=result.plan.to_dict(),
                same_word_mode=False,
                original_wish_word=base.poetic_display_word(raw_wish),
                original_return_word=base.poetic_display_word(raw_return),
                wish_role_proxy_id=None,
                wish_role_proxy_text=None,
            ),
            long_form=result.long_form,
            nexus_echo=result.nexus_echo,
        )

    try:
        proxy = choose_wish_role_proxy(proxies, rng=active_rng)
    except SameWordPolicyError as error:
        raise base.PrototypeCompositionError(str(error)) from error

    shared = base.poetic_display_word(raw_return)
    route = base._weighted_choice(library["routes"], active_rng)
    selected = _select_same_word_blocks(library, route, proxy, shared, active_rng)
    long_form = base._render_long_form(selected)
    try:
        validate_exact_line_repetition(long_form)
    except SameWordPolicyError as error:
        raise base.PrototypeCompositionError(str(error)) from error

    aggregate = base._aggregate(selected)
    _validate_same_word_plan(library, selected, long_form, proxy, shared, aggregate)
    echo_lines, echo_ids = _same_word_echo(
        library, selected, proxy, shared, aggregate, active_rng
    )

    base_plan = {
        "plan_version": "resonance-composition-plan-prototype-v0.2.1",
        "library_version": library["library_version"],
        "world_id": library["world_id"],
        "completion_mode": library["completion_mode"],
        "route_id": route["id"],
        "block_ids": [item.data["id"] for item in selected],
        "block_roles": [item.role for item in selected],
        "operators": sorted(aggregate["operators"]),
        "resonant_gains": sorted(aggregate["gains"]),
        "leaves_states": sorted(aggregate["states"]),
        "motifs_visible": sorted(aggregate["motifs"]),
        "echo_line_ids": list(echo_ids),
        "echo_source_trace": proxy.text,
        "echo_wish_line": 2,
    }
    return PolicyComposition(
        plan=PolicyCompositionPlan(
            base_plan=base_plan,
            same_word_mode=True,
            original_wish_word=base.poetic_display_word(raw_wish),
            original_return_word=shared,
            wish_role_proxy_id=proxy.proxy_id,
            wish_role_proxy_text=proxy.text,
        ),
        long_form=long_form,
        nexus_echo="\n".join(echo_lines),
    )


def _proxy_for_template(template: str, proxy: WishRoleProxy) -> str:
    """Capitalise the proxy only when the slot begins the visible line."""
    stripped = template.lstrip()
    if stripped.startswith("{wish_word}"):
        return proxy.text[:1].upper() + proxy.text[1:]
    return proxy.text


def _select_same_word_blocks(
    library: dict[str, Any],
    route: dict[str, Any],
    proxy: WishRoleProxy,
    shared: str,
    rng: random.Random,
) -> tuple[base._SelectedBlock, ...]:
    active_tags = set(library["active_tags"])
    completion_mode = library["completion_mode"]
    forced_ids = {
        "relation": "relation.interval.01",
        "remainder": "remainder.passage.01",
    }
    selected: list[base._SelectedBlock] = []
    used_ids: set[str] = set()

    for role in route["roles"]:
        candidates = [
            block
            for block in library["blocks"]
            if role in block.get("roles", [])
            and block["id"] not in used_ids
            and set(block.get("requires_all_tags", [])).issubset(active_tags)
            and completion_mode in block.get("completion_modes", [])
            and (role not in forced_ids or block["id"] == forced_ids[role])
        ]
        if not candidates:
            raise base.PrototypeCompositionError(
                f"Same-word route has no compatible block for {role!r}"
            )
        block = base._weighted_choice(candidates, rng)
        visible_wish = (
            _proxy_for_template(block["text"], proxy)
            if role == "wish_entry"
            else shared
        )
        rendered = base._render_template(block["text"], visible_wish, shared)
        selected.append(base._SelectedBlock(role, block, rendered))
        used_ids.add(block["id"])
    return tuple(selected)


def _validate_same_word_plan(
    library: dict[str, Any],
    selected: Sequence[base._SelectedBlock],
    long_form: str,
    proxy: WishRoleProxy,
    shared: str,
    aggregate: dict[str, set[str]],
) -> None:
    if proxy.text.casefold() not in long_form.casefold():
        raise base.PrototypeCompositionError("Same-word proxy is not visible")
    if base._word_occurrences(long_form, shared) != 1:
        raise base.PrototypeCompositionError(
            "Shared word must appear exactly once in the long form"
        )
    if not set(library["required_gain_one_of"]).intersection(aggregate["gains"]):
        raise base.PrototypeCompositionError("Same-word plan has no resonant gain")
    if set(library["forbidden_terminal_states"]).intersection(aggregate["states"]):
        raise base.PrototypeCompositionError(
            "Same-word plan has a forbidden terminal state"
        )
    if not selected[-1].data.get("terminal_allowed", False):
        raise base.PrototypeCompositionError(
            "Same-word ending is not terminal eligible"
        )


def _same_word_echo(
    library: dict[str, Any],
    selected: Sequence[base._SelectedBlock],
    proxy: WishRoleProxy,
    shared: str,
    aggregate: dict[str, set[str]],
    rng: random.Random,
) -> tuple[tuple[str, ...], tuple[str, ...]]:
    selected_ids = {item.data["id"] for item in selected}
    openings = [
        item
        for item in library["echo_line_candidates"].get("line_1", [])
        if base._echo_candidate_available(item, selected_ids, aggregate)
    ]
    if not openings:
        raise base.PrototypeCompositionError(
            "Same-word Echo has no linked opening"
        )
    opening = base._weighted_choice(openings, rng)
    lines = (
        opening["text"],
        f"{proxy.text} crosses",
        "two returns hold one interval open",
        "the passage stays open",
        shared,
    )
    counts = tuple(base._word_count(line) for line in lines)
    if counts != base.EXPECTED_ECHO_COUNTS:
        raise base.PrototypeCompositionError(
            f"Invalid same-word Echo counts: {counts}"
        )
    if base._word_occurrences("\n".join(lines), shared) != 1:
        raise base.PrototypeCompositionError(
            "Shared word must appear once in the Echo"
        )
    try:
        validate_exact_line_repetition(lines)
    except SameWordPolicyError as error:
        raise base.PrototypeCompositionError(str(error)) from error
    return lines, (
        opening["id"],
        f"same-word.{proxy.proxy_id}.l2",
        "echo.trace.interval.l3",
        "echo.trace.passage-open.l4",
        "echo.return-word.l5",
    )
