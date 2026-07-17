from __future__ import annotations

from dataclasses import FrozenInstanceError, asdict
import itertools
import unittest

from chambers.resonance import (
    OriginatingResonanceContribution,
    ResonanceComposeError,
    ScriptedChamberIO,
    build_resonance_token_v2,
    build_v0_1_catalog,
    compose_originating_resonance,
    compose_originating_resonance_terminal,
)


ROUTE = {
    "module_id": "N01",
    "layer_id": "return-resonance-1",
    "origin_trace_id": "n01-origin-compose-test",
    "return_slot_id": "n01-slot-compose-test",
    "package_id": "n01-package-compose-test",
}


class RecordingIO(ScriptedChamberIO):
    def __init__(self) -> None:
        super().__init__(
            choices={
                "image": "waiting-lantern",
                "scent": "summer-rain",
                "movement": "falling-feather",
            },
            words={"wish_word": "Nähe"},
        )
        self.steps: list[str] = []

    def choose(self, step: str, option_ids: tuple[str, ...]) -> str:
        self.steps.append(step)
        return super().choose(step, option_ids)

    def enter_word(self, step: str) -> str:
        self.steps.append(step)
        return super().enter_word(step)


class ComposeBoundaryTests(unittest.TestCase):
    def test_all_source_choices_validate(self) -> None:
        catalog = build_v0_1_catalog()
        for image_id in catalog.option_ids("images"):
            self.assertEqual(
                OriginatingResonanceContribution(
                    image_id, "summer-rain", "falling-feather", "hope"
                ).image_id,
                image_id,
            )
        for scent_id in catalog.option_ids("scents"):
            self.assertEqual(
                OriginatingResonanceContribution(
                    "waiting-lantern", scent_id, "falling-feather", "hope"
                ).scent_id,
                scent_id,
            )
        for movement_id in catalog.option_ids("movements"):
            self.assertEqual(
                OriginatingResonanceContribution(
                    "waiting-lantern", "summer-rain", movement_id, "hope"
                ).movement_id,
                movement_id,
            )

    def test_compose_prompts_only_for_originating_fields(self) -> None:
        io = RecordingIO()
        contribution = compose_originating_resonance(io)
        self.assertEqual(io.steps, ["image", "scent", "movement", "wish_word"])
        self.assertEqual(contribution.wish_word, "Nähe")
        self.assertEqual(
            set(asdict(contribution)),
            {"image_id", "scent_id", "movement_id", "wish_word"},
        )

    def test_terminal_compose_uses_existing_numbered_presentation(self) -> None:
        answers = iter(("1", "2", "3", "Verbundenheit"))
        output: list[str] = []
        contribution = compose_originating_resonance_terminal(
            lambda _prompt: next(answers), output.append
        )
        transcript = "\n".join(output)
        self.assertEqual(contribution.image_id, "waiting-lantern")
        self.assertEqual(contribution.scent_id, "books-and-cedar")
        self.assertEqual(contribution.movement_id, "returning-tide")
        self.assertNotIn("answers the image", transcript)
        self.assertNotIn("return word", transcript.casefold())

    def test_unicode_and_invalid_wish_words(self) -> None:
        self.assertEqual(
            OriginatingResonanceContribution(
                "waiting-lantern", "summer-rain", "falling-feather", "  Nähe  "
            ).wish_word,
            "Nähe",
        )
        for value in ("", "two words", "line\nbreak", "CHANGE-ME"):
            with self.subTest(value=value), self.assertRaises(ResonanceComposeError):
                OriginatingResonanceContribution(
                    "waiting-lantern", "summer-rain", "falling-feather", value
                )

    def test_contribution_is_immutable_and_rejects_unknown_sources(self) -> None:
        contribution = OriginatingResonanceContribution(
            "waiting-lantern", "summer-rain", "falling-feather", "hope"
        )
        with self.assertRaises(FrozenInstanceError):
            contribution.wish_word = "changed"  # type: ignore[misc]
        with self.assertRaises(ResonanceComposeError):
            OriginatingResonanceContribution(
                "unknown", "summer-rain", "falling-feather", "hope"
            )

    def test_token_v2_builder_supports_all_source_cross_products(self) -> None:
        catalog = build_v0_1_catalog()
        combinations = itertools.product(
            catalog.option_ids("images"),
            catalog.option_ids("scents"),
            catalog.option_ids("movements"),
        )
        expected_keys = {
            "token_version",
            "token_type",
            "module_id",
            "layer_id",
            "origin_trace_id",
            "return_slot_id",
            "package_id",
            "language_library",
            "enabled_chambers",
            "image_id",
            "scent_id",
            "movement_id",
            "wish_word",
        }
        count = 0
        for image_id, scent_id, movement_id in combinations:
            token = build_resonance_token_v2(
                OriginatingResonanceContribution(
                    image_id, scent_id, movement_id, "Nähe"
                ),
                **ROUTE,
            )
            self.assertEqual(set(token.to_dict()), expected_keys)
            for field_name, expected in ROUTE.items():
                self.assertEqual(getattr(token, field_name), expected)
            count += 1
        self.assertEqual(count, 125)

    def test_token_builder_requires_validated_contribution(self) -> None:
        with self.assertRaises(ResonanceComposeError):
            build_resonance_token_v2(  # type: ignore[arg-type]
                {"image_id": "waiting-lantern"}, **ROUTE
            )


if __name__ == "__main__":
    unittest.main()
