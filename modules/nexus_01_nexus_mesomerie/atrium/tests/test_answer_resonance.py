from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

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

    def run_answer(self, answers: tuple[str, ...], **overrides):
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
            **overrides,
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
        self.assertIn("one response at a time", transcript)
        self.assertIn("private reasons are not stored", transcript)
        self.assertIn("Nothing is returned, sent, uploaded, synchronized, or published", transcript)
        self.assertIn("Use /cancel at any interactive prompt", transcript)
        self.assertIn("end the current Resonance cycle safely", transcript)
        self.assertIn("At yes/no prompts, you may also answer no", transcript)
        self.assertIn("blank input also cancels creation", transcript)
        self.assertIn("Full-cycle cancellation returns safely to the Atrium", transcript)
        self.assertNotIn("Previous confirmation forms", transcript)
        self.assertIn("No Return Artifact exists yet", transcript)
        self.assertIn("If you choose to return this Artifact", transcript)
        self.assertIn("Nothing requires you to return, publish, or share", transcript)
        self.assertLess(
            transcript.index("Answer shaped"),
            transcript.index("Return Artifact: "),
        )
        self.assertLess(
            transcript.index("Local creation complete"),
            transcript.index("Local path"),
        )
        self.assertLess(
            transcript.index("Local path"),
            transcript.index("Optional manual return"),
        )
        self.assertFalse(any("wish" in prompt.casefold() for prompt in prompts))
        self.assert_context_unchanged()

    def test_cancellation_during_choices_and_at_confirmation_writes_nothing(self) -> None:
        def forbidden_writer(*_args, **_kwargs):
            raise AssertionError("artifact writer was called after cancellation")

        for suffix, answers in (
            ("image-response", ("/cancel",)),
            ("scent-response", ("1", "/cancel")),
            ("movement-response", ("1", "1", "/cancel")),
            ("return-word", ("1", "1", "1", "/cancel")),
            ("confirmation", ("1", "1", "1", "trust", "no")),
            ("destination", ("1", "1", "1", "trust", "yes", "")),
        ):
            with self.subTest(suffix=suffix):
                result, _, transcript = self.run_answer(
                    answers,
                    artifact_writer=forbidden_writer,
                )
                self.assertFalse(result.completed)
                self.assertIn("No Return Artifact was created", transcript)
                self.assertIn("Nothing was written", transcript)
                self.assertIn("answer route remains unfinished", transcript)
                self.assertIn("Returning safely to the Atrium", transcript)
                self.assertEqual(list(self.root.glob("*.return.json")), [])
                self.assert_context_unchanged()

    def test_slash_cancel_at_new_answer_boundaries_writes_nothing(self) -> None:
        cases = (
            ("walkthrough-confirmation", ("/walkthrough", " /Cancel ")),
            ("creation-confirmation", ("1", "1", "1", "trust", "/cancel")),
            (
                "artifact-destination",
                ("1", "1", "1", "trust", "yes", " /CANCEL "),
            ),
        )

        def forbidden_writer(*_args, **_kwargs):
            raise AssertionError("artifact writer was called after /cancel")

        for name, answers in cases:
            with self.subTest(name=name):
                result, _, transcript = self.run_answer(
                    answers,
                    artifact_writer=forbidden_writer,
                )
                self.assertFalse(result.completed)
                self.assertIn("Nothing was written", transcript)
                self.assertIn("answer route remains unfinished", transcript)
                self.assert_context_unchanged()

    def test_answer_confirmation_compatibility_declines_remain_supported(self) -> None:
        def forbidden_writer(*_args, **_kwargs):
            raise AssertionError("declined creation invoked the artifact writer")

        for answer in ("no", "cancel", "q"):
            with self.subTest(answer=answer):
                result, _, transcript = self.run_answer(
                    ("1", "1", "1", "trust", answer),
                    artifact_writer=forbidden_writer,
                )
                self.assertFalse(result.completed)
                self.assertIn("Nothing was written", transcript)
                self.assert_context_unchanged()

    def test_answer_path_with_cancel_prefix_is_not_a_command(self) -> None:
        written: list[Path] = []

        def capture_writer(_artifact, destination):
            path = Path(destination)
            written.append(path)
            return path

        result, _, _ = self.run_answer(
            (
                "1",
                "1",
                "1",
                "trust",
                "yes",
                "/cancelled/example.json",
            ),
            artifact_writer=capture_writer,
        )

        self.assertTrue(result.completed)
        self.assertEqual(written, [Path("/cancelled/example.json")])
        self.assert_context_unchanged()

    def test_answer_exploration_is_nonwriting_and_reveals_only_current_step(self) -> None:
        def forbidden_writer(*_args, **_kwargs):
            raise AssertionError("information command invoked the artifact writer")

        result, prompts, transcript = self.run_answer(
            ("/look", "/help", "/trace", "/cancel"),
            artifact_writer=forbidden_writer,
        )

        self.assertFalse(result.completed)
        self.assertIn("carried image rests at the threshold", transcript)
        self.assertIn("Enter one of the numbers shown for this step", transcript)
        self.assertIn("Attend to the kind of response", transcript)
        self.assertGreaterEqual(transcript.count("Answer the carried image"), 4)
        self.assertNotIn("Answer the carried scent", transcript)
        self.assertNotIn("Answer the carried movement", transcript)
        self.assertTrue(all(prompt == "Enter a number: " for prompt in prompts))
        self.assertFalse(any(self.root.glob("*.return.json")))
        self.assert_context_unchanged()

    def test_answer_help_preserves_prior_selection_and_completion(self) -> None:
        destination = self.root / "guided-resonance-return.json"
        result, _, transcript = self.run_answer(
            ("5", "/help", "1", "4", "Rückkehr", "yes", str(destination))
        )

        self.assertTrue(result.completed)
        artifact = json.loads(destination.read_text(encoding="utf-8"))
        self.assertEqual(artifact["image_response_id"], "shared-silence")
        self.assertEqual(artifact["scent_response_id"], "possibility-of-encounter")
        self.assertIn("Current Chamber grammar", transcript)
        self.assertLess(
            transcript.index("Current Chamber grammar"),
            transcript.index("Answer the carried movement"),
        )
        self.assert_context_unchanged()

    def test_answer_walkthrough_can_stop_without_selecting_or_writing(self) -> None:
        def forbidden_writer(*_args, **_kwargs):
            raise AssertionError("walkthrough invoked the artifact writer")

        result, prompts, transcript = self.run_answer(
            ("/walkthrough", "yes", "/walkthrough", "/cancel"),
            artifact_writer=forbidden_writer,
        )

        self.assertFalse(result.completed)
        self.assertEqual(transcript.count("Chamber voice"), 1)
        self.assertIn("response that can meet the carried image", transcript)
        self.assertIn("Guided walkthrough ended", transcript)
        self.assertEqual(transcript.count("Answer the carried image"), 3)
        self.assertTrue(all("number" in prompt for prompt in prompts if "guided" not in prompt))
        self.assertFalse(any(self.root.glob("*.return.json")))
        self.assert_context_unchanged()

    def test_answer_walkthrough_guides_each_step_once_and_preserves_completion(self) -> None:
        destination = self.root / "walkthrough-resonance-return.json"
        result, _, transcript = self.run_answer(
            (
                "/walkthrough",
                "yes",
                "5",
                "/trace",
                "1",
                "4",
                "Rückkehr",
                "yes",
                str(destination),
            )
        )

        self.assertTrue(result.completed)
        self.assertEqual(transcript.count("Chamber voice"), 4)
        for guidance in (
            "response that can meet the carried image",
            "response that can meet the carried scent",
            "movement that can answer the carried movement",
            "return word without explaining",
        ):
            self.assertEqual(transcript.count(guidance), 1)
        artifact = json.loads(destination.read_text(encoding="utf-8"))
        self.assertEqual(artifact["image_response_id"], "shared-silence")
        self.assertEqual(artifact["scent_response_id"], "possibility-of-encounter")
        self.assertEqual(artifact["movement_response_id"], "playful-waves")
        self.assertEqual(artifact["return_word"], "Rückkehr")
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
        self.assertIn("Nothing was written. Existing material was not replaced", transcript)
        self.assertIn("answer route remains unfinished", transcript)
        self.assert_context_unchanged()

    def test_invalidated_selected_context_prevents_answer_before_prompting(self) -> None:
        paths_for_nexus(self.nexus).selected_token.write_bytes(b"{}\n")
        result, prompts, transcript = self.run_answer(())
        self.assertFalse(result.completed)
        self.assertEqual(prompts, [])
        self.assertIn("ANSWER cannot begin", transcript)
        self.assertLess(
            transcript.index("selected carried trace could not safely be opened"),
            transcript.index("ANSWER cannot begin"),
        )
        self.assertIn("Nothing was written", transcript)
        self.assertIn("No nearby Token was discovered or substituted", transcript)
        self.assertFalse(any(self.root.glob("*.return.json")))

    def test_corrected_answer_route_cannot_reach_legacy_controller(self) -> None:
        values = iter(("/resonance", "1", "1", "1", "trust", "no", "/quit"))

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

    def test_successful_answer_reentry_is_nonproductive_post_run(self) -> None:
        destination = self.root / "post-run-answer.json"
        values = iter(
            (
                "5",
                "1",
                "4",
                "Rückkehr",
                "yes",
                str(destination),
                " /LOOK ",
                "/trace",
                "help",
                "/answer",
                "/new-answer",
                "/select-token",
                "/results",
                "/leave",
                "/quit",
            )
        )
        prompts: list[str] = []
        output: list[str] = []
        writes = 0

        def read(prompt: str) -> str:
            prompts.append(prompt)
            return next(values)

        def counted_writer(artifact, path):
            nonlocal writes
            writes += 1
            from return_resonance.artifact_store import write_resonance_return_artifact

            return write_resonance_return_artifact(artifact, path)

        controller = ClassifiedResonanceController(
            ResonanceMode.ANSWER,
            output_writer=output.append,
            input_reader=read,
            nexus_root=self.nexus,
            artifact_writer=counted_writer,
        )

        self.assertTrue(controller().completed)
        with patch(
            "atrium.classified_resonance.collect_answering_resonance",
            side_effect=AssertionError("post-run collected another response"),
        ):
            self.assertFalse(controller().completed)

        transcript = "\n".join(output)
        post_run = transcript[transcript.index("Resonance Chamber — completed answer") :]
        self.assertEqual(writes, 1)
        self.assertIn("This answer cycle will not begin again automatically", transcript)
        self.assertGreaterEqual(post_run.count("Resonance Chamber — completed answer"), 2)
        self.assertIn("another deliberately selected Token context", post_run)
        self.assertIn("leave Nexus 01", post_run)
        self.assertNotIn("/answer —", post_run)
        self.assertNotIn("/new-answer —", post_run)
        self.assertNotIn("/select-token —", post_run)
        self.assertNotIn("/results —", post_run)
        self.assertEqual(post_run.count("Unknown Resonance command."), 5)
        self.assertTrue(all(prompt == "resonance> " for prompt in prompts[-9:]))
        self.assert_context_unchanged()

    def test_only_success_activates_answer_post_run_gate(self) -> None:
        destination = self.root / "answer-after-cancel.json"
        values = iter(
            (
                "/cancel",
                "1",
                "1",
                "1",
                "return",
                "yes",
                str(destination),
            )
        )
        output: list[str] = []
        controller = ClassifiedResonanceController(
            ResonanceMode.ANSWER,
            output_writer=output.append,
            input_reader=lambda _prompt: next(values),
            nexus_root=self.nexus,
        )

        self.assertFalse(controller().completed)
        self.assertTrue(controller().completed)
        transcript = "\n".join(output)
        self.assertEqual(transcript.count("Resonance Chamber — answer the carried resonance"), 2)
        self.assertNotIn("Resonance Chamber — completed answer", transcript)
        self.assert_context_unchanged()

    def test_answer_post_run_ctrl_c_returns_without_writing_again(self) -> None:
        destination = self.root / "answer-before-interrupt.json"
        values = iter(("1", "1", "1", "return", "yes", str(destination)))
        output: list[str] = []
        writes = 0

        def read(_prompt: str) -> str:
            try:
                return next(values)
            except StopIteration:
                raise KeyboardInterrupt

        def counted_writer(artifact, path):
            nonlocal writes
            writes += 1
            from return_resonance.artifact_store import write_resonance_return_artifact

            return write_resonance_return_artifact(artifact, path)

        controller = ClassifiedResonanceController(
            ResonanceMode.ANSWER,
            output_writer=output.append,
            input_reader=read,
            nexus_root=self.nexus,
            artifact_writer=counted_writer,
        )

        self.assertTrue(controller().completed)
        self.assertFalse(controller().completed)
        self.assertEqual(writes, 1)
        self.assertIn("Returning safely to the Atrium", "\n".join(output))
        self.assert_context_unchanged()


if __name__ == "__main__":
    unittest.main()
