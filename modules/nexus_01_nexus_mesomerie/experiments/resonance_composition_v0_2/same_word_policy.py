#!/usr/bin/env python3
"""Lexical identity and repetition policy for the Resonance V0.2 prototype."""

from __future__ import annotations

from dataclasses import dataclass
import random
from typing import Iterable, Sequence


class SameWordPolicyError(ValueError):
    """Raised when a same-word or repetition policy cannot be satisfied."""


@dataclass(frozen=True)
class WishRoleProxy:
    proxy_id: str
    text: str
    weight: int = 1


def words_are_identical(wish_word: str, return_word: str) -> bool:
    """Detect lexical identity without semantic interpretation."""
    if not isinstance(wish_word, str) or not isinstance(return_word, str):
        return False
    return wish_word.casefold() == return_word.casefold()


def choose_wish_role_proxy(
    proxies: Sequence[WishRoleProxy],
    *,
    rng: random.Random | None = None,
) -> WishRoleProxy:
    """Choose one curated proxy by positive integer weight."""
    if not proxies:
        raise SameWordPolicyError("Same-word mode requires at least one proxy")
    weights = [proxy.weight for proxy in proxies]
    if any(weight <= 0 for weight in weights):
        raise SameWordPolicyError("Proxy weights must be positive integers")
    active_rng = rng if rng is not None else random.Random()
    return active_rng.choices(list(proxies), weights=weights, k=1)[0]


def validate_exact_line_repetition(
    lines: str | Iterable[str],
    *,
    explicit_reprises: Iterable[str] = (),
) -> None:
    """Reject accidental exact line duplication while preserving parallelism.

    Similar or related lines are intentionally not compared. An exact duplicate
    is accepted only when its normalised text is explicitly curated as a reprise.
    """
    source = lines.splitlines() if isinstance(lines, str) else list(lines)
    allowed = {
        line.strip().casefold()
        for line in explicit_reprises
        if isinstance(line, str) and line.strip()
    }
    seen: set[str] = set()
    for raw_line in source:
        line = raw_line.strip()
        if not line:
            continue
        normalised = line.casefold()
        if normalised in seen and normalised not in allowed:
            raise SameWordPolicyError(
                f"Accidental duplicate rendered line: {line!r}"
            )
        seen.add(normalised)
