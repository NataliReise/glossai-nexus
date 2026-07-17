from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest

from atrium.classified_resonance import ClassifiedResonanceController
from atrium.resonance_mode import ResonanceMode
from atrium.terminal import run_nexus_terminal
from chambers.resonance import OriginatingResonanceContribution, build_resonance_token_v2
from recipient_activation import activate_with_resonance_token, paths_for_nexus


RECIPIENT = {
    "recipient_alias": "Cécile",
    "activation_purpose": "gift",
    "private_message": "Für dich",
}
ROUTE = {
    "module_id": "N01",
    "layer_id": "return-resonance-1",
    "origin_trace_id": "answer-terminal-origin",
    "return_slot_id": "answer-terminal-slot",
    "package_id": "answer-terminal-package",
}


class AnswerTerminalTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.nexus = self.root / "nexus"
        (self.nexus / "first_spark").mkdir(parents=True)
        self.invitation = self.root / "invitation.json"
        token = build_resonance_token_v2(
            OriginatingResonanceContribution(
                "bridge-in-mist", "warm-bread", "opening-circle", "Nähe"
            ),
            public_safe_label="Von B",
            **ROUTE,
        )
        self.invitation.write_text(token.to_json(), encoding="utf-8")
        activate_with_resonance_token(self.invitation, nexus_root=self.nexus, **RECIPIENT)
        paths = paths_for_nexus(self.nexus)
        self.before = {
            "activation": paths.activation.read_bytes(),
            "context": paths.selected_context.read_bytes(),
            "token": paths.selected_token.read_bytes(),
        }

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def run_answer(self, answers: tuple[str, ...]):
        values = iter(answers)
        prompts: list[str] = []
        output: list[str] = []

        def read(prompt: str) -> str:
            prompts.append(prompt)
            return next(values)

        result = ClassifiedResonanceController(
            ResonanceMode.ANSWER,
            output_writer=output.append,
            input_reader=read,
            nexus_root=self.nexus,
        )()
        return result, prompts, "\n".join(output)

    def assert_context_unchanged(self) -> None:
        paths = paths_for_nexus(self.nexus)
        self.assertEqual(paths.activation.read_bytes(), self.before["activation"])
        self.assertEqual(paths.selected_context.read_bytes(), self.before["context"])
        self.assertEqual(paths.selected_token.read_bytes(), self.before["token"])

    def test_confirmed_answer_displays_origin_and_publishes_exactly_one_artifact(self) -> None:
        destination = self.root / "resonance-return.json"
        result, prompts, transcript = self.run_answer(
            ("5", "1", "4", "Rückkehr", "yes", str(destination))
        )
        self.assertTrue(result.completed)
        self.assertTrue(destination.is_file())
        artifact = json.loads(destination.read_text(encoding="utf-8"))
        self.assertEqual(artifact["image_id"], "bridge-in-mist")
        self.assertEqual(artifact["wish_word"], "Nähe")
        self.assertEqual(artifact["image_response_id"], "shared-silence")
        self.assertEqual(artifact["scent_response_id"], "possibility-of-encounter")
        self.assertEqual(artifact["movement_response_id"], "playful-waves")
        self.assertEqual(artifact["return_word"], "Rückkehr")
        self.assertIn("From: Von B", transcript)
        self.assertIn("A narrow bridge in the mist", transcript)
        self.assertIn("Warm bread in a quiet kitchen", transcript)
        self.assertIn("A circle slowly opening", transcript)
        self.assertIn("Wish word: Nähe", transcript)
        self.assertIn("manually", transcript)
        self.assertFalse(any("wish" in prompt.casefold() for prompt in prompts))
        self.assert_context_unchanged()

    def test_cancellation_during_choices_and_at_confirmation_writes_nothing(self) -> None:
        for suffix, answers in (
            ("choice", ("/cancel",)),
            ("confirmation", ("1", "1", "1", "trust", "no")),
        ):
            with self.subTest(suffix=suffix):
                result, _, transcript = self.run_answer(answers)
                self.assertFalse(result.completed)
                self.assertIn("No Return Artifact was created", transcript)
                self.assertEqual(list(self.root.glob("*.return.json")), [])
                self.assert_context_unchanged()

    def test_overwrite_is_refused_without_changing_existing_bytes(self) -> None:
        destination = self.root / "existing.json"
        destination.write_bytes(b"keep me")
        result, _, transcript = self.run_answer(
            ("1", "1", "1", "trust", "yes", str(destination))
        )
        self.assertFalse(result.completed)
        self.assertEqual(destination.read_bytes(), b"keep me")
        self.assertIn("Refusing to overwrite", transcript)
        self.assert_context_unchanged()

    def test_invalidated_selected_context_prevents_answer_before_prompting(self) -> None:
        paths_for_nexus(self.nexus).selected_token.write_bytes(b"{}\n")
        result, prompts, transcript = self.run_answer(())
        self.assertFalse(result.completed)
        self.assertEqual(prompts, [])
        self.assertIn("ANSWER cannot begin", transcript)
        self.assertFalse(any(self.root.glob("*.return.json")))

    def test_corrected_answer_route_cannot_reach_legacy_controller(self) -> None:
        values = iter(("resonance", "1", "1", "1", "trust", "no", "quit"))

        class ReturnActivation:
            profile_id = "return-resonance"
            activation_purpose = "gift"

        def forbidden_legacy():
            raise AssertionError("legacy one-person controller was reached")

        runtime = run_nexus_terminal(
            activation_loader=ReturnActivation,
            resonance_runner=forbidden_legacy,
            resonance_mode=ResonanceMode.ANSWER,
            classified_resonance_runner=ClassifiedResonanceController(
                ResonanceMode.ANSWER,
                output_writer=lambda _message: None,
                input_reader=lambda _prompt: next(values),
                nexus_root=self.nexus,
            ),
            input_reader=lambda _prompt: next(values),
            output_writer=lambda _message: None,
        )
        self.assertEqual(runtime.resonance_mode, ResonanceMode.ANSWER)


if __name__ == "__main__":
    unittest.main()
