from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import unittest

from composer import (
    CompositionError,
    LIBRARY_VERSION,
    PROFILE_KINDS,
    SOURCE_FIELDS,
    WORD_PATTERN,
    artifact_for_world,
    compose,
    load_library,
    validate_library,
)


LIBRARY_PATH = Path(__file__).with_name("profiles.v0_4.json")


class ComposerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.library = load_library(LIBRARY_PATH)

    def artifact(self, world: str = "clear-meeting", wish: str = "hope", returned: str = "trust"):
        return artifact_for_world(self.library, world, wish, returned)

    def test_seed_reproducibility_includes_plan_and_trace(self) -> None:
        first = compose(self.artifact(), library=self.library, seed=1701)
        second = compose(self.artifact(), library=self.library, seed=1701)
        self.assertEqual(first, second)
        self.assertEqual(first.plan.seed, 1701)
        self.assertEqual(first.plan.rendered_text, first.text)
        self.assertTrue(first.plan.trace_id.startswith("v04-"))

    def test_structural_invariants_across_all_worlds_and_many_seeds(self) -> None:
        for world in self.library["supported_worlds"]:
            for seed in range(40):
                result = compose(self.artifact(world["id"]), library=self.library, seed=seed)
                self.assertEqual(tuple(len(line.split()) for line in result.lines), WORD_PATTERN)
                self.assertEqual(len(result.lines), 5)
                self.assertLessEqual(sum(len(line.split()) for line in result.lines), 25)
                self.assertEqual(result.lines[-1], "Trust")
                self.assertNotIn("{", result.text)
                self.assertNotIn("}", result.text)
                wish_line = int(result.plan.route_id.rsplit(".", 1)[-1])
                expected_line = {1: 3, 2: 2, 3: 4}[wish_line]
                self.assertEqual(
                    [index for index, line in enumerate(result.lines[:4], 1) if "Hope" in line.split()],
                    [expected_line],
                )

    def test_plan_records_every_source_profile_and_variant(self) -> None:
        result = compose(self.artifact("quiet-interior"), library=self.library, seed=4)
        self.assertEqual(result.plan.library_version, LIBRARY_VERSION)
        self.assertEqual(tuple(dict(result.plan.source_artifact_ids)), SOURCE_FIELDS)
        self.assertEqual(len(result.plan.selected_profile_ids), len(PROFILE_KINDS))
        self.assertEqual(len(result.plan.selected_variant_ids), len(PROFILE_KINDS))
        self.assertEqual(result.plan.world_id, "quiet-interior")

    def test_unicode_free_words_are_preserved_without_semantic_analysis(self) -> None:
        result = compose(
            self.artifact("distance-return", "nähe", "rückkehr"),
            library=self.library,
            seed=7,
        )
        self.assertEqual(result.lines[-1], "Rückkehr")
        self.assertEqual(sum(line.split().count("Nähe") for line in result.lines[:4]), 1)

    def test_identical_wish_and_return_words_keep_both_slots(self) -> None:
        result = compose(
            self.artifact("playful-transformation", "nähe", "nähe"),
            library=self.library,
            seed=12,
        )
        self.assertEqual(result.lines[-1], "Nähe")
        self.assertEqual(sum(line.split().count("Nähe") for line in result.lines[:4]), 1)
        self.assertEqual(sum(line.split().count("Nähe") for line in result.lines), 2)

    def test_unsupported_id_and_mixed_known_ids_fail_clearly(self) -> None:
        unknown = self.artifact().__dict__ | {"image_id": "unknown-image"}
        mixed = self.artifact().__dict__ | {"movement_id": "returning-tide", "movement_response_id": "stream-back-to-sea"}
        for artifact in (unknown, mixed):
            with self.subTest(artifact=artifact):
                with self.assertRaisesRegex(CompositionError, "Unsupported Return Artifact ID combination"):
                    compose(artifact, library=self.library, seed=1)

    def test_missing_artifact_field_fails_clearly(self) -> None:
        artifact = dict(self.artifact().__dict__)
        del artifact["wish_word"]
        with self.assertRaisesRegex(CompositionError, "Return Artifact is missing: wish_word"):
            compose(artifact, library=self.library, seed=1)

    def test_invalid_free_words_fail_calmly(self) -> None:
        for word in ("two words", "half-light", "word2", "", "quiet!"):
            with self.subTest(word=word):
                with self.assertRaises(CompositionError):
                    compose(self.artifact(wish=word), library=self.library, seed=1)

    def test_malformed_profiles_are_rejected(self) -> None:
        malformed_cases = []
        duplicate = deepcopy(self.library)
        duplicate["profiles"]["image"][0]["roles"]["seed"][1]["id"] = duplicate["profiles"]["image"][0]["roles"]["seed"][0]["id"]
        malformed_cases.append((duplicate, "Duplicate id"))
        placeholder = deepcopy(self.library)
        placeholder["profiles"]["image"][0]["roles"]["seed"][0]["text"] = "Waiting {thing}"
        malformed_cases.append((placeholder, "text must contain letter words"))
        missing_role = deepcopy(self.library)
        del missing_role["profiles"]["movement_response"][0]["roles"]["bridge"]
        malformed_cases.append((missing_role, "lacks role"))
        bad_noun = deepcopy(self.library)
        bad_noun["profiles"]["image"][0]["roles"]["seed"][0]["visible_nouns"] = ["ocean"]
        malformed_cases.append((bad_noun, "not visible"))

        for library, message in malformed_cases:
            with self.subTest(message=message):
                with self.assertRaisesRegex(CompositionError, message):
                    validate_library(library)

    def test_adjacent_content_verb_repetition_is_rejected(self) -> None:
        library = deepcopy(self.library)
        for kind in ("image_response", "movement", "movement_response"):
            for profile in library["profiles"][kind]:
                for variants in profile["roles"].values():
                    for variant in variants:
                        variant["content_verb"] = "repeat"
        validate_library(library)
        with self.assertRaisesRegex(CompositionError, "Adjacent lines repeat content verb"):
            compose(self.artifact(), library=library, seed=2, max_attempts=30)

    def test_excessive_visible_noun_repetition_is_rejected(self) -> None:
        library = deepcopy(self.library)
        for kind in ("image", "image_response", "scent"):
            for profile in library["profiles"][kind]:
                for variants in profile["roles"].values():
                    for variant in variants:
                        words = variant["text"].split()
                        words[0] = "Echo"
                        variant["text"] = " ".join(words)
                        variant["visible_nouns"] = ["echo"]
        validate_library(library)
        with self.assertRaisesRegex(CompositionError, "Visible noun repeats excessively"):
            compose(self.artifact(), library=library, seed=3, max_attempts=30)

    def test_all_routes_are_reached_and_have_visible_variation(self) -> None:
        results = [compose(self.artifact(), library=self.library, seed=seed) for seed in range(160)]
        self.assertEqual(
            {result.plan.route_id for result in results},
            {route["id"] for route in self.library["routes"]},
        )
        self.assertGreater(len({result.text for result in results}), 30)
        wish_lines = {
            next(index for index, line in enumerate(result.lines[:4], 1) if "Hope" in line.split())
            for result in results
        }
        self.assertEqual(wish_lines, {2, 3, 4})

    def test_trace_is_stable_and_changes_with_rendered_plan(self) -> None:
        results = [compose(self.artifact(), library=self.library, seed=seed) for seed in range(12)]
        by_text = {result.text: result.plan.trace_id for result in results}
        self.assertEqual(len(by_text), len(set(by_text.values())))

    def test_library_file_remains_json_serializable(self) -> None:
        self.assertIsInstance(json.dumps(self.library, ensure_ascii=False), str)


if __name__ == "__main__":
    unittest.main()

