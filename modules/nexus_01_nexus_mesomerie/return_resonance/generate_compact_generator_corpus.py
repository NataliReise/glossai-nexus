#!/usr/bin/env python3
"""Generate the review-only corpus for the production compact generator."""

from __future__ import annotations

from itertools import product
import json
from pathlib import Path
import sys


NEXUS_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_ROOT = Path(__file__).resolve().parent
sys.path[:] = [
    entry
    for entry in sys.path
    if Path(entry or ".").resolve() != SCRIPT_ROOT
]
if str(NEXUS_ROOT) not in sys.path:
    sys.path.insert(0, str(NEXUS_ROOT))

from chambers.resonance.choices import build_v0_1_catalog  # noqa: E402
from return_resonance.compact_generator import (  # noqa: E402
    GENERATOR_ID,
    GENERATOR_VERSION,
    generate_compact_resonance,
)
from return_resonance.resonance_render_bridge import (  # noqa: E402
    ARTIFACT_TYPE,
    ARTIFACT_VERSION,
    LANGUAGE_LIBRARY,
    ResonanceReturnArtifact,
)
from return_resonance.token import LAYER_ID, MODULE_ID  # noqa: E402


DEFAULT_OUTPUT = Path(__file__).resolve().with_name("COMPACT_GENERATOR_REVIEW_CORPUS.md")


def build_artifact(
    image_path: tuple[str, str],
    scent_path: tuple[str, str],
    movement_path: tuple[str, str],
    index: int,
) -> ResonanceReturnArtifact:
    return ResonanceReturnArtifact(
        artifact_version=ARTIFACT_VERSION,
        artifact_type=ARTIFACT_TYPE,
        module_id=MODULE_ID,
        layer_id=LAYER_ID,
        origin_trace_id=f"n01-origin-corpus-{index:03d}",
        return_slot_id=f"n01-slot-corpus-{index:03d}",
        package_id=f"n01-package-corpus-{index:03d}",
        language_library=LANGUAGE_LIBRARY,
        image_id=image_path[0],
        image_response_id=image_path[1],
        scent_id=scent_path[0],
        scent_response_id=scent_path[1],
        movement_id=movement_path[0],
        movement_response_id=movement_path[1],
        wish_word="kinship",
        return_word="homeward",
    )


def generate_corpus(output_path: Path = DEFAULT_OUTPUT) -> int:
    catalog = build_v0_1_catalog()
    image_paths = [
        (option.id, catalog.image_compatibility[option.id][0]) for option in catalog.images
    ]
    scent_paths = [
        (option.id, catalog.scent_compatibility[option.id][0]) for option in catalog.scents
    ]
    movement_paths = [
        (option.id, catalog.movement_compatibility[option.id][0])
        for option in catalog.movements
    ]
    combinations = list(product(image_paths, scent_paths, movement_paths))
    if len(combinations) != 125:
        raise RuntimeError(f"Expected 125 Chamber combinations, found {len(combinations)}")

    lines = [
        "# Nexus 01 Compact Generator Review Corpus",
        "",
        f"Generator: `{GENERATOR_ID}`",
        f"Version: `{GENERATOR_VERSION}`",
        "",
        "This review corpus contains one seeded output for every current compatible",
        "image/scent/movement path cross-product. It is generated data, not runtime input.",
        "",
        f"Total outputs: **{len(combinations)}**",
        "",
    ]
    for index, combination in enumerate(combinations, start=1):
        artifact = build_artifact(*combination, index)
        seed = f"review-{index:03d}"
        result = generate_compact_resonance(artifact, seed=seed)
        lines.extend(
            (
                f"## {index:03d} — {artifact.image_id} / {artifact.scent_id} / {artifact.movement_id}",
                "",
                "```text",
                result.text,
                "```",
                "",
                "```json",
                json.dumps(result.composition_plan, indent=2, ensure_ascii=False, sort_keys=True),
                "```",
                "",
            )
        )

    output_path.write_text("\n".join(lines), encoding="utf-8")
    return len(combinations)


def main(argv: list[str] | None = None) -> int:
    arguments = list(sys.argv[1:] if argv is None else argv)
    output = Path(arguments[0]).expanduser().resolve() if arguments else DEFAULT_OUTPUT
    count = generate_corpus(output)
    print(f"Generated {count} compact review outputs: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
