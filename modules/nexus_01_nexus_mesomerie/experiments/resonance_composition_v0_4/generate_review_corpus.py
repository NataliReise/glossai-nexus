#!/usr/bin/env python3
"""Generate a deterministic 60-result human-review corpus with plans."""

from __future__ import annotations

import json
from pathlib import Path

from composer import artifact_for_world, compose, load_library


OUTPUT = Path(__file__).with_name("REVIEW_CORPUS.md")
WORD_PAIRS = (
    ("courage", "trust"),
    ("nähe", "rückkehr"),
    ("perhaps", "welcome"),
    ("lumen", "lumen"),
)


def render_corpus() -> str:
    library = load_library()
    lines = [
        "# Resonance Composition V0.4 Human-Review Corpus",
        "",
        "Generated deterministically by `generate_review_corpus.py`.",
        "Sixty outputs: five supported worlds × twelve seeds.",
        "Each result is followed by its complete composition plan.",
        "",
    ]
    number = 0
    for world_index, world in enumerate(library["supported_worlds"]):
        lines.extend((f"## {world['id']}", ""))
        for local_seed in range(12):
            number += 1
            seed = world_index * 1000 + local_seed
            wish, returned = WORD_PAIRS[local_seed % len(WORD_PAIRS)]
            artifact = artifact_for_world(library, world["id"], wish, returned)
            result = compose(artifact, library=library, seed=seed)
            lines.extend(
                (
                    f"### {number:02d} · seed {seed} · `{result.plan.trace_id}`",
                    "",
                    "```text",
                    result.text,
                    "```",
                    "",
                    "<details><summary>Composition plan</summary>",
                    "",
                    "```json",
                    json.dumps(result.plan.to_dict(), ensure_ascii=False, indent=2),
                    "```",
                    "",
                    "</details>",
                    "",
                )
            )
    return "\n".join(lines)


def main() -> int:
    OUTPUT.write_text(render_corpus(), encoding="utf-8")
    print(f"Wrote 60 seeded outputs to {OUTPUT.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
