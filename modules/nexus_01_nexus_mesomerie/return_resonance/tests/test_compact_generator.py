"""Exhaustive tests for the pure production compact generator boundary."""

from __future__ import annotations

from dataclasses import replace
from itertools import product
import json
from pathlib import Path
import sys
import tempfile
import unittest


NEXUS_ROOT = Path(__file__).resolve().parents[2]
if str(NEXUS_ROOT) not in sys.path:
    sys.path.insert(0, str(NEXUS_ROOT))

from chambers.resonance.choices import build_v0_1_catalog  # noqa: E402
import return_resonance.compact_generator as generator_module  # noqa: E402
from return_resonance.compact_generator import (  # noqa: E402
    GENERATOR_ID,
    GENERATOR_VERSION,
    CompactGenerationError,
    MicroPattern,
    generate_compact_resonance,
)
from return_resonance.generate_compact_generator_corpus import generate_corpus  # noqa: E402
from return_resonance.resonance_render_bridge import (  # noqa: E402
    ARTIFACT_TYPE,
    ARTIFACT_VERSION,
    LANGUAGE_LIBRARY,
    ResonanceReturnArtifact,
)
from return_resonance.token import LAYER_ID, MODULE_ID  # noqa: E402


def valid_paths() -> tuple[list[tuple[str, str]], list[tuple[str, str]], list[tuple[str, str]]]:
    catalog = build_v0_1_catalog()
    images = [
        (option.id, catalog.image_compatibility[option.id][0]) for option in catalog.images
    ]
    scents = [
        (option.id, catalog.scent_compatibility[option.id][0]) for option in catalog.scents
    ]
    movements = [
        (option.id, catalog.movement_compatibility[option.id][0])
        for option in catalog.movements
    ]
    return images, scents, movements


def artifact_for(
    image_path: tuple[str, str] | None = None,
    scent_path: tuple[str, str] | None = None,
    movement_path: tuple[str, str] | None = None,
    *,
    wish_word: str = "kinship",
    return_word: str = "homeward",
) -> ResonanceReturnArtifact:
    images, scents, movements = valid_paths()
    image_id, image_response_id = image_path or images[0]
    scent_id, scent_response_id = scent_path or scents[0]
    movement_id, movement_response_id = movement_path or movements[0]
    return ResonanceReturnArtifact(
        artifact_version=ARTIFACT_VERSION,
        artifact_type=ARTIFACT_TYPE,
        module_id=MODULE_ID,
        layer_id=LAYER_ID,
        origin_trace_id="n01-origin-generator-test",
        return_slot_id="n01-slot-generator-test",
        package_id="n01-package-generator-test",
        language_library=LANGUAGE_LIBRARY,
        image_id=image_id,
        image_response_id=image_response_id,
        scent_id=scent_id,
        scent_response_id=scent_response_id,
        movement_id=movement_id,
        movement_response_id=movement_response_id,
        wish_word=wish_word,
        return_word=return_word,
    )


class CompactGeneratorTests(unittest.TestCase):
    def test_all_125_current_chamber_combinations(self) -> None:
        images, scents, movements = valid_paths()
        combinations = list(product(images, scents, movements))
        self.assertEqual(len(combinations), 125)

        for index, (image_path, scent_path, movement_path) in enumerate(combinations):
            with self.subTest(index=index):
                artifact = artifact_for(image_path, scent_path, movement_path)
                result = generate_compact_resonance(artifact, seed=f"combination-{index:03d}")
                lines = result.text.splitlines()
                self.assertEqual(len(lines), 5)
                self.assertEqual(lines[-1], artifact.return_word)
                self.assertIn(artifact.wish_word, result.text)
                self.assertEqual(
                    result.composition_plan["source_artifact_ids"]["image_id"],
                    artifact.image_id,
                )
                self.assertEqual(
                    result.composition_plan["source_artifact_ids"]["scent_id"],
                    artifact.scent_id,
                )
                self.assertEqual(
                    result.composition_plan["source_artifact_ids"]["movement_id"],
                    artifact.movement_id,
                )

    def test_seed_is_deterministic(self) -> None:
        artifact = artifact_for()
        first = generate_compact_resonance(artifact, seed="stable-seed")
        second = generate_compact_resonance(artifact, seed="stable-seed")
        self.assertEqual(first, second)

    def test_unicode_free_words_are_preserved(self) -> None:
        result = generate_compact_resonance(
            artifact_for(wish_word="Nähe", return_word="帰還"), seed=17
        )
        self.assertIn("Nähe", result.text)
        self.assertEqual(result.text.splitlines()[-1], "帰還")
        json.dumps(result.composition_plan, ensure_ascii=False)

    def test_identical_words_use_deliberate_separation(self) -> None:
        result = generate_compact_resonance(
            artifact_for(wish_word="echo", return_word="echo"), seed="same-word"
        )
        lines = result.text.splitlines()
        self.assertEqual(lines[-1], "echo")
        self.assertNotIn("echo", lines[-2].casefold())
        self.assertEqual(
            result.composition_plan["same_word_strategy"],
            "separated-wish-role-and-final-return",
        )

    def test_unsupported_and_incompatible_ids_are_rejected(self) -> None:
        cases = (
            replace(artifact_for(), image_id="unknown-image"),
            replace(artifact_for(), image_response_id="shared-silence"),
            replace(artifact_for(), scent_id="unknown-scent"),
            replace(artifact_for(), scent_response_id="sense-of-return"),
            replace(artifact_for(), movement_id="unknown-movement"),
            replace(artifact_for(), movement_response_id="playful-waves"),
        )
        for artifact in cases:
            with self.subTest(artifact=artifact), self.assertRaises(CompactGenerationError):
                generate_compact_resonance(artifact)

    def test_unresolved_placeholder_is_rejected(self) -> None:
        original = generator_module.MICRO_PATTERNS
        generator_module.MICRO_PATTERNS = (
            MicroPattern(
                "broken-placeholder",
                "{image_line}\n{scent_line}\nMay {wish_word} remain.\n"
                "{movement_line}\n{missing}",
                2,
            ),
        )
        try:
            with self.assertRaisesRegex(CompactGenerationError, "unresolved placeholder"):
                generate_compact_resonance(artifact_for())
        finally:
            generator_module.MICRO_PATTERNS = original

    def test_duplicate_adjacent_phrase_is_rejected(self) -> None:
        original = generator_module.MICRO_PATTERNS
        generator_module.MICRO_PATTERNS = (
            MicroPattern(
                "broken-duplicate",
                "{image_line}\n{image_line}\nMay {wish_word} remain.\n"
                "{movement_line}\n{return_word}",
                2,
            ),
        )
        try:
            with self.assertRaisesRegex(CompactGenerationError, "duplicate adjacent"):
                generate_compact_resonance(artifact_for())
        finally:
            generator_module.MICRO_PATTERNS = original

    def test_composition_plan_is_json_serializable(self) -> None:
        result = generate_compact_resonance(artifact_for(), seed=42)
        encoded = json.dumps(result.composition_plan, ensure_ascii=False, sort_keys=True)
        decoded = json.loads(encoded)
        self.assertEqual(decoded["generator_id"], GENERATOR_ID)
        self.assertEqual(decoded["generator_version"], GENERATOR_VERSION)
        self.assertEqual(decoded["rendered_text"], result.text)

    def test_review_corpus_contains_all_125_combinations(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "corpus.md"
            self.assertEqual(generate_corpus(output), 125)
            corpus = output.read_text(encoding="utf-8")
        self.assertEqual(corpus.count("\n## "), 125)
        self.assertEqual(corpus.count('"rendered_text":'), 125)

    def test_multiline_free_word_is_rejected(self) -> None:
        with self.assertRaisesRegex(CompactGenerationError, "one visible line"):
            generate_compact_resonance(artifact_for(wish_word="two\nlines"))


if __name__ == "__main__":
    unittest.main()
