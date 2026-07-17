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
    EXPECTED_WORD_COUNTS,
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


def independent_paths(
) -> tuple[list[tuple[str, str]], list[tuple[str, str]], list[tuple[str, str]]]:
    catalog = build_v0_1_catalog()
    return (
        list(product(catalog.option_ids("images"), catalog.option_ids("image_responses"))),
        list(product(catalog.option_ids("scents"), catalog.option_ids("scent_responses"))),
        list(
            product(
                catalog.option_ids("movements"),
                catalog.option_ids("movement_responses"),
            )
        ),
    )


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


def word_counts(text: str) -> tuple[int, ...]:
    return tuple(len(line.split()) for line in text.splitlines())


class CompactGeneratorTests(unittest.TestCase):
    def test_every_independent_pair_in_each_domain_is_supported(self) -> None:
        images, scents, movements = independent_paths()
        self.assertEqual((len(images), len(scents), len(movements)), (25, 25, 25))
        defaults = valid_paths()

        for domain, paths in enumerate((images, scents, movements)):
            for path in paths:
                selected = [default[0] for default in defaults]
                selected[domain] = path
                result = generate_compact_resonance(
                    artifact_for(*selected), seed=f"domain-{domain}-{path}"
                )
                self.assertEqual(word_counts(result.text), EXPECTED_WORD_COUNTS)

    def test_all_15625_complete_answer_combinations_are_supported(self) -> None:
        images, scents, movements = independent_paths()
        count = 0
        for image_path, scent_path, movement_path in product(
            images, scents, movements
        ):
            result = generate_compact_resonance(
                artifact_for(image_path, scent_path, movement_path),
                seed="complete-answer-coverage",
            )
            lines = result.text.splitlines()
            self.assertEqual(word_counts(result.text), EXPECTED_WORD_COUNTS)
            count += 1
        self.assertEqual(count, 15_625)

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
                self.assertEqual(word_counts(result.text), EXPECTED_WORD_COUNTS)
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

    def test_unknown_source_and_response_ids_are_rejected_independently(self) -> None:
        cases = (
            replace(artifact_for(), image_id="unknown-image"),
            replace(artifact_for(), image_response_id="unknown-image-response"),
            replace(artifact_for(), scent_id="unknown-scent"),
            replace(artifact_for(), scent_response_id="unknown-scent-response"),
            replace(artifact_for(), movement_id="unknown-movement"),
            replace(artifact_for(), movement_response_id="unknown-movement-response"),
        )
        for artifact in cases:
            with self.subTest(artifact=artifact), self.assertRaises(CompactGenerationError):
                generate_compact_resonance(artifact)

    def test_legacy_pairs_remain_supported_under_compact_contract(self) -> None:
        result = generate_compact_resonance(artifact_for(), seed=None)
        self.assertEqual(
            result.text.splitlines(),
            [
                "Lantern-waiting path-appears.",
                "Summer rain, encounter opens.",
                "May kinship keep this passage open.",
                "Falling feather, feathers cross.",
                "homeward",
            ],
        )
        self.assertEqual(
            result.composition_plan["profile_component_ids"]["image"]["strategy"],
            "legacy-pair-override",
        )

    def test_seed_variation_preserves_content_and_changes_structure(self) -> None:
        artifact = artifact_for(
            ("waiting-lantern", "shared-silence"),
            ("warm-bread", "sense-of-return"),
            ("opening-circle", "shadow-alongside"),
        )
        results = {
            generate_compact_resonance(artifact, seed=f"variation-{index}").text
            for index in range(20)
        }
        self.assertGreaterEqual(len(results), 2)
        for text in results:
            self.assertIn("lantern-waiting", text.casefold())
            self.assertIn("silence-shares", text.casefold())
            self.assertEqual(word_counts(text), EXPECTED_WORD_COUNTS)
            self.assertEqual(text.splitlines()[-1], artifact.return_word)

    def test_route_metadata_is_not_visible(self) -> None:
        artifact = artifact_for(
            ("book-bench", "shared-silence"),
            ("first-snow", "sense-of-return"),
            ("crossing-light", "playful-waves"),
        )
        text = generate_compact_resonance(artifact, seed="no-route-leak").text
        for value in (
            artifact.origin_trace_id,
            artifact.return_slot_id,
            artifact.package_id,
            artifact.module_id,
            artifact.layer_id,
        ):
            self.assertNotIn(value, text)

        for choice_id in (
            artifact.image_id,
            artifact.image_response_id,
            artifact.scent_id,
            artifact.scent_response_id,
            artifact.movement_id,
            artifact.movement_response_id,
        ):
            self.assertNotIn(choice_id, text)

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
                "{image_line}\n{image_line}\nMay {wish_word} keep this passage open.\n"
                "{movement_line}\n{return_word}",
                2,
            ),
        )
        try:
            with self.assertRaisesRegex(CompactGenerationError, "duplicate adjacent"):
                generate_compact_resonance(artifact_for())
        finally:
            generator_module.MICRO_PATTERNS = original

    def test_malformed_word_count_is_rejected(self) -> None:
        original = generator_module.MICRO_PATTERNS
        generator_module.MICRO_PATTERNS = (
            MicroPattern(
                "broken-word-count",
                "{image_line}\n{scent_line}\nMay {wish_word} remain open.\n"
                "{movement_line}\n{return_word}",
                2,
            ),
        )
        try:
            with self.assertRaisesRegex(CompactGenerationError, "2 / 4 / 6 / 4 / 1"):
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
        with self.assertRaisesRegex(CompactGenerationError, "exactly one word"):
            generate_compact_resonance(artifact_for(wish_word="two\nlines"))


if __name__ == "__main__":
    unittest.main()
