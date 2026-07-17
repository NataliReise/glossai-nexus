from __future__ import annotations

from dataclasses import FrozenInstanceError, asdict
import unittest

from chambers.resonance import (
    AnsweringResonanceContribution,
    OriginatingResonanceContribution,
    ResonanceAnswerError,
    ScriptedChamberIO,
    build_answer_resonance_return_artifact,
    build_resonance_token_v2,
    build_v0_1_catalog,
    collect_answering_resonance,
)
from return_resonance.compact_generator import generate_compact_resonance
from return_resonance.matching import MatchStatus, match_return_artifact
from return_resonance.slots import ReturnSlot, ReturnSlotState


ROUTE = {
    "module_id": "N01",
    "layer_id": "return-resonance-1",
    "origin_trace_id": "answer-origin-001",
    "return_slot_id": "answer-slot-001",
    "package_id": "answer-package-001",
}


def token(image="waiting-lantern", scent="summer-rain", movement="falling-feather"):
    return build_resonance_token_v2(
        OriginatingResonanceContribution(image, scent, movement, "Nähe"),
        **ROUTE,
    )


class AnswerCoreTests(unittest.TestCase):
    def test_contribution_is_immutable_and_contains_only_answer_fields(self) -> None:
        contribution = AnsweringResonanceContribution(
            "shared-silence", "sense-of-return", "shadow-alongside", "Rückkehr"
        )
        self.assertEqual(
            set(asdict(contribution)),
            {"image_response_id", "scent_response_id", "movement_response_id", "return_word"},
        )
        with self.assertRaises(FrozenInstanceError):
            contribution.return_word = "changed"  # type: ignore[misc]

    def test_all_response_choices_are_supported(self) -> None:
        catalog = build_v0_1_catalog()
        defaults = {
            "image_response_id": catalog.image_responses[0].id,
            "scent_response_id": catalog.scent_responses[0].id,
            "movement_response_id": catalog.movement_responses[0].id,
            "return_word": "trust",
        }
        for field, options in (
            ("image_response_id", catalog.image_responses),
            ("scent_response_id", catalog.scent_responses),
            ("movement_response_id", catalog.movement_responses),
        ):
            for option in options:
                values = {**defaults, field: option.id}
                self.assertEqual(getattr(AnsweringResonanceContribution(**values), field), option.id)

    def test_every_source_permits_every_corresponding_response(self) -> None:
        catalog = build_v0_1_catalog()
        defaults = AnsweringResonanceContribution(
            catalog.image_responses[0].id,
            catalog.scent_responses[0].id,
            catalog.movement_responses[0].id,
            "trust",
        )
        for sources, responses, source_field, response_field in (
            (catalog.images, catalog.image_responses, "image", "image_response_id"),
            (catalog.scents, catalog.scent_responses, "scent", "scent_response_id"),
            (catalog.movements, catalog.movement_responses, "movement", "movement_response_id"),
        ):
            for source in sources:
                for response in responses:
                    origins = {"image": "waiting-lantern", "scent": "summer-rain", "movement": "falling-feather"}
                    origins[source_field] = source.id
                    values = asdict(defaults)
                    values[response_field] = response.id
                    artifact = build_answer_resonance_return_artifact(
                        token(origins["image"], origins["scent"], origins["movement"]),
                        AnsweringResonanceContribution(**values),
                    )
                    self.assertEqual(getattr(artifact, response_field), response.id)

    def test_unicode_and_invalid_return_words(self) -> None:
        self.assertEqual(
            AnsweringResonanceContribution(
                "appearing-path", "sense-of-return", "crossing-feather", "信頼"
            ).return_word,
            "信頼",
        )
        for invalid in ("", "two words", "line\nbreak", "CHANGE-ME", "x\x00y", "x" * 81):
            with self.subTest(invalid=repr(invalid)), self.assertRaises(ResonanceAnswerError):
                AnsweringResonanceContribution(
                    "appearing-path", "sense-of-return", "crossing-feather", invalid
                )

    def test_collection_prompts_only_for_complete_response_sets(self) -> None:
        catalog = build_v0_1_catalog()
        io = ScriptedChamberIO(
            choices={
                "image_response": "shared-silence",
                "scent_response": "second-place-at-table",
                "movement_response": "playful-waves",
            },
            words={"return_word": "home"},
        )
        contribution = collect_answering_resonance(io, catalog)
        self.assertEqual(contribution.return_word, "home")
        self.assertNotIn("wish_word", io.words)

    def test_artifact_copies_origin_and_route_and_uses_answer(self) -> None:
        selected = token("bridge-in-mist", "warm-bread", "opening-circle")
        answer = AnsweringResonanceContribution(
            "appearing-path", "open-books-beside-one-another", "stream-back-to-sea", "ankommen"
        )
        artifact = build_answer_resonance_return_artifact(selected, answer)
        for field in (*ROUTE, "language_library", "image_id", "scent_id", "movement_id", "wish_word"):
            self.assertEqual(getattr(artifact, field), getattr(selected, field))
        for field, value in asdict(answer).items():
            self.assertEqual(getattr(artifact, field), value)

    def test_artifact_matches_slot_and_existing_supported_path_generates(self) -> None:
        artifact = build_answer_resonance_return_artifact(
            token(),
            AnsweringResonanceContribution(
                "appearing-path",
                "possibility-of-encounter",
                "crossing-feather",
                "trust",
            ),
        )
        slot = ReturnSlot(
            origin_trace_id=ROUTE["origin_trace_id"],
            return_slot_id=ROUTE["return_slot_id"],
            module_id=ROUTE["module_id"],
            package_id=ROUTE["package_id"],
            layer_id=ROUTE["layer_id"],
            status=ReturnSlotState.WAITING,
            result_file="answer-result.md",
        )
        self.assertEqual(
            match_return_artifact(artifact.to_matching_artifact(), [slot]).status,
            MatchStatus.MATCH_WAITING,
        )
        self.assertIn("trust", generate_compact_resonance(artifact, seed=7).text)


if __name__ == "__main__":
    unittest.main()
