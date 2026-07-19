from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from atrium.classified_resonance import (
    ClassifiedResonanceController,
    CompletedAnswerResult,
)
from atrium.resonance_mode import ResonanceMode
from atrium.terminal import run_nexus_terminal
from chambers.resonance import OriginatingResonanceContribution, build_resonance_token_v2
from recipient_activation import activate_with_resonance_token, paths_for_nexus
from return_resonance.artifact_store import (
    ResonanceArtifactStoreError,
    write_resonance_return_artifact,
)


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
        values = iter(("/answer", *answers))
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
        destination_parent = self.root / "answers"
        destination_parent.mkdir()
        with patch(
            "atrium.classified_resonance.secrets.token_hex",
            return_value="0123456789abcdef01234567",
        ):
            result, prompts, transcript = self.run_answer(
                ("5", "1", "4", "Rückkehr", "yes", str(destination_parent))
            )
        self.assertTrue(result.completed)
        artifacts = list(destination_parent.iterdir())
        self.assertEqual(len(artifacts), 1)
        destination = artifacts[0]
        self.assertRegex(
            destination.name,
            r"^n01-return-artifact-[0-9a-f]{24}\.json$",
        )
        self.assertNotIn("Nähe".casefold(), destination.name.casefold())
        self.assertNotIn("Rückkehr".casefold(), destination.name.casefold())
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
        self.assertIn(
            "Parent directory for the Return Artifact (blank to cancel): ",
            prompts,
        )
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
        destination_parent = self.root / "cancelled"
        destination_parent.mkdir()

        def capture_writer(_artifact, destination):
            path = Path(destination)
            written.append(path)
            return path

        with patch(
            "atrium.classified_resonance.secrets.token_hex",
            return_value="111111111111111111111111",
        ):
            result, _, _ = self.run_answer(
                ("1", "1", "1", "trust", "yes", str(destination_parent)),
                artifact_writer=capture_writer,
            )

        self.assertTrue(result.completed)
        self.assertEqual(
            written,
            [destination_parent / "n01-return-artifact-111111111111111111111111.json"],
        )
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
        self.assertEqual(prompts[0], "resonance> ")
        self.assertTrue(all(prompt == "Enter a number: " for prompt in prompts[1:]))
        self.assertFalse(any(self.root.glob("*.return.json")))
        self.assert_context_unchanged()

    def test_answer_help_preserves_prior_selection_and_completion(self) -> None:
        destination_parent = self.root / "guided-results"
        destination_parent.mkdir()
        result, _, transcript = self.run_answer(
            ("5", "/help", "1", "4", "Rückkehr", "yes", str(destination_parent))
        )

        self.assertTrue(result.completed)
        destination = next(destination_parent.iterdir())
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
        self.assertEqual(prompts[0], "resonance> ")
        self.assertTrue(
            all("number" in prompt for prompt in prompts[1:] if "guided" not in prompt)
        )
        self.assertFalse(any(self.root.glob("*.return.json")))
        self.assert_context_unchanged()

    def test_answer_walkthrough_guides_each_step_once_and_preserves_completion(self) -> None:
        destination_parent = self.root / "walkthrough-results"
        destination_parent.mkdir()
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
                str(destination_parent),
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
        destination = next(destination_parent.iterdir())
        artifact = json.loads(destination.read_text(encoding="utf-8"))
        self.assertEqual(artifact["image_response_id"], "shared-silence")
        self.assertEqual(artifact["scent_response_id"], "possibility-of-encounter")
        self.assertEqual(artifact["movement_response_id"], "playful-waves")
        self.assertEqual(artifact["return_word"], "Rückkehr")
        self.assert_context_unchanged()

    def test_generated_name_collision_retries_without_changing_existing_bytes(self) -> None:
        destination_parent = self.root / "collision-results"
        destination_parent.mkdir()
        collision = (
            destination_parent
            / "n01-return-artifact-aaaaaaaaaaaaaaaaaaaaaaaa.json"
        )
        collision.write_bytes(b"keep me")
        with patch(
            "atrium.classified_resonance.secrets.token_hex",
            side_effect=(
                "aaaaaaaaaaaaaaaaaaaaaaaa",
                "bbbbbbbbbbbbbbbbbbbbbbbb",
            ),
        ):
            result, _, _ = self.run_answer(
                ("1", "1", "1", "trust", "yes", str(destination_parent))
            )
        self.assertTrue(result.completed)
        self.assertEqual(collision.read_bytes(), b"keep me")
        generated = (
            destination_parent
            / "n01-return-artifact-bbbbbbbbbbbbbbbbbbbbbbbb.json"
        )
        self.assertTrue(generated.is_file())
        self.assert_context_unchanged()

    def test_two_independent_answers_create_distinct_artifacts_in_one_directory(self) -> None:
        destination_parent = self.root / "multiple-results"
        destination_parent.mkdir()
        ids = (
            "111111111111111111111111",
            "222222222222222222222222",
        )
        with patch(
            "atrium.classified_resonance.secrets.token_hex", side_effect=ids
        ):
            first, _, _ = self.run_answer(
                ("1", "1", "1", "trust", "yes", str(destination_parent))
            )
            first_path = destination_parent / f"n01-return-artifact-{ids[0]}.json"
            first_bytes = first_path.read_bytes()
            second, _, _ = self.run_answer(
                ("5", "1", "4", "return", "yes", str(destination_parent))
            )

        second_path = destination_parent / f"n01-return-artifact-{ids[1]}.json"
        self.assertTrue(first.completed)
        self.assertTrue(second.completed)
        self.assertTrue(second_path.is_file())
        self.assertNotEqual(first_path, second_path)
        self.assertEqual(first_path.read_bytes(), first_bytes)
        self.assertEqual(len(list(destination_parent.iterdir())), 2)
        self.assert_context_unchanged()

    def test_exhausted_name_collisions_fail_without_writing(self) -> None:
        destination_parent = self.root / "exhausted-results"
        destination_parent.mkdir()
        ids = tuple(f"{index:024x}" for index in range(8))
        original = {}
        for opaque_id in ids:
            path = destination_parent / f"n01-return-artifact-{opaque_id}.json"
            path.write_bytes(f"keep-{opaque_id}".encode("ascii"))
            original[path] = path.read_bytes()

        def forbidden_writer(*_args, **_kwargs):
            raise AssertionError("collision exhaustion invoked the artifact writer")

        with patch(
            "atrium.classified_resonance.secrets.token_hex", side_effect=ids
        ):
            result, _, transcript = self.run_answer(
                ("1", "1", "1", "trust", "yes", str(destination_parent)),
                artifact_writer=forbidden_writer,
            )

        self.assertFalse(result.completed)
        self.assertIn("Could not choose an unused Return Artifact filename", transcript)
        self.assertIn("Nothing was written", transcript)
        self.assertEqual(
            {path: path.read_bytes() for path in destination_parent.iterdir()},
            original,
        )
        self.assert_context_unchanged()

    def test_invalid_answer_parent_destinations_fail_without_writing(self) -> None:
        regular_file = self.root / "not-a-directory"
        regular_file.write_bytes(b"keep me")
        missing = self.root / "missing-parent"
        inside_carrier = self.nexus / "private-answer-output"
        inside_carrier.mkdir()

        def forbidden_writer(*_args, **_kwargs):
            raise AssertionError("invalid parent invoked the artifact writer")

        for name, destination, expected in (
            ("regular-file", regular_file, "must be an existing directory"),
            ("missing", missing, "must be an existing directory"),
            ("carrier", inside_carrier, "outside the travelling Nexus carrier"),
        ):
            with self.subTest(name=name):
                values = iter(
                    ("/answer", "1", "1", "1", "trust", "yes", str(destination))
                )
                output: list[str] = []
                controller = ClassifiedResonanceController(
                    ResonanceMode.ANSWER,
                    output_writer=output.append,
                    input_reader=lambda _prompt: next(values),
                    nexus_root=self.nexus,
                    artifact_writer=forbidden_writer,
                )
                result = controller()
                transcript = "\n".join(output)
                self.assertFalse(result.completed)
                self.assertIsNone(controller._last_completed_result)
                self.assertIn(expected, transcript)
                self.assertIn("Nothing was written", transcript)

        self.assertEqual(regular_file.read_bytes(), b"keep me")
        self.assertFalse(missing.exists())
        self.assertEqual(list(inside_carrier.iterdir()), [])
        self.assert_context_unchanged()

    def test_failed_later_answer_write_preserves_retained_success(self) -> None:
        destination_parent = self.root / "retained-answer"
        destination_parent.mkdir()
        values = iter(
            (
                "/answer",
                "1",
                "1",
                "1",
                "first",
                "yes",
                str(destination_parent),
                "5",
                "1",
                "4",
                "second",
                "yes",
                str(destination_parent),
            )
        )
        writes = 0

        def writer(artifact, destination):
            nonlocal writes
            writes += 1
            if writes == 2:
                raise ResonanceArtifactStoreError("simulated writer failure")
            return write_resonance_return_artifact(artifact, destination)

        controller = ClassifiedResonanceController(
            ResonanceMode.ANSWER,
            output_writer=lambda _message: None,
            input_reader=lambda _prompt: next(values),
            nexus_root=self.nexus,
            artifact_writer=writer,
        )
        with patch(
            "atrium.classified_resonance.secrets.token_hex",
            side_effect=(
                "333333333333333333333333",
                "444444444444444444444444",
            ),
        ):
            self.assertTrue(controller().completed)
            retained = controller._last_completed_result
            self.assertIsInstance(retained, CompletedAnswerResult)
            self.assertFalse(controller._run_answer().completed)

        self.assertIs(controller._last_completed_result, retained)
        self.assertTrue(retained.artifact_path.is_file())
        self.assertEqual(len(list(destination_parent.iterdir())), 1)
        self.assert_context_unchanged()

    def test_invalidated_selected_context_prevents_answer_before_prompting(self) -> None:
        paths_for_nexus(self.nexus).selected_token.write_bytes(b"{}\n")
        result, prompts, transcript = self.run_answer(())
        self.assertFalse(result.completed)
        self.assertEqual(prompts, ["resonance> "])
        self.assertIn("ANSWER cannot begin", transcript)
        self.assertLess(
            transcript.index("selected carried trace could not safely be opened"),
            transcript.index("ANSWER cannot begin"),
        )
        self.assertIn("Nothing was written", transcript)
        self.assertIn("No nearby Token was discovered or substituted", transcript)
        self.assertFalse(any(self.root.glob("*.return.json")))

    def test_corrected_answer_route_cannot_reach_legacy_controller(self) -> None:
        values = iter(
            ("/resonance", "/answer", "1", "1", "1", "trust", "no", "/quit")
        )

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
        destination_parent = self.root / "post-run-answers"
        destination_parent.mkdir()
        values = iter(
            (
                "/answer",
                "5",
                "1",
                "4",
                "Rückkehr",
                "yes",
                str(destination_parent),
                " /LOOK ",
                "/trace",
                "help",
                "/answer",
                "/new-answer",
                "/select-token",
                "/results",
                "results",
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
        retained = controller._last_completed_result
        self.assertIsInstance(retained, CompletedAnswerResult)
        destination = retained.artifact_path
        with patch(
            "atrium.classified_resonance.collect_answering_resonance",
            side_effect=AssertionError("post-run collected another response"),
        ), patch(
            "return_resonance.local_opening.open_local_resonance_return"
        ) as opening, patch(
            "return_resonance.matching.match_return_artifact"
        ) as matching, patch(
            "return_resonance.compact_generator.generate_compact_resonance"
        ) as generator:
            self.assertFalse(controller().completed)
        opening.assert_not_called()
        matching.assert_not_called()
        generator.assert_not_called()

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
        self.assertIn(
            "/results — view this session's most recent completed answer", post_run
        )
        self.assertIn(
            "Resonance results — most recent answer cycle in this session", post_run
        )
        self.assertIn("Earlier local outputs remain separate and unchanged.", post_run)
        for text in (
            "[private local]",
            "    Carried image: A narrow bridge in the mist",
            "    Carried scent: Warm bread in a quiet kitchen",
            "    Carried movement: A circle slowly opening",
            "    Wish word: Nähe",
            "    Image response: A silence becomes shared",
            "    Scent response: The possibility of encounter",
            "    Movement response: Edges curling into playful waves",
            "    Return word: Rückkehr",
            "[public-safe]",
            "    Carried label: Von B",
            "[local path]",
            f"    Return Artifact: {destination} — available",
        ):
            self.assertIn(text, post_run)
        for hidden in (
            "artifact_version",
            "origin_trace_id",
            ROUTE["origin_trace_id"],
            ROUTE["return_slot_id"],
            ROUTE["package_id"],
            "CompletedAnswerResult",
            "ResonanceReturnArtifact(",
        ):
            self.assertNotIn(hidden, post_run)
        self.assertEqual(post_run.count("Unknown Resonance command."), 5)
        self.assertTrue(all(prompt == "resonance> " for prompt in prompts[-10:]))
        self.assertIs(controller._last_completed_result, retained)
        self.assert_context_unchanged()

    def test_answer_results_keep_values_when_known_artifact_is_missing(self) -> None:
        destination_parent = self.root / "removed-results"
        destination_parent.mkdir()
        values = iter(
            (
                "/answer",
                "5",
                "1",
                "4",
                "Rückkehr",
                "yes",
                str(destination_parent),
                "/results",
                "/quit",
            )
        )
        output: list[str] = []
        controller = ClassifiedResonanceController(
            ResonanceMode.ANSWER,
            output_writer=output.append,
            input_reader=lambda _prompt: next(values),
            nexus_root=self.nexus,
        )

        self.assertIsNone(controller._last_completed_result)
        self.assertTrue(controller().completed)
        retained = controller._last_completed_result
        self.assertIsInstance(retained, CompletedAnswerResult)
        destination = retained.artifact_path
        destination.unlink()
        self.assertFalse(controller().completed)
        self.assertIs(controller._last_completed_result, retained)

        results = "\n".join(output)
        self.assertIn("Return word: Rückkehr", results)
        self.assertIn(
            f"Return Artifact: {destination} — no longer available at the known location",
            results,
        )
        self.assertEqual(results.count("No filesystem search was performed."), 1)
        self.assert_context_unchanged()

    def test_answer_results_explain_absent_public_safe_label(self) -> None:
        destination_parent = self.root / "unlabelled-results"
        destination_parent.mkdir()
        token_without_label = build_resonance_token_v2(
            OriginatingResonanceContribution(
                "bridge-in-mist", "warm-bread", "opening-circle", "Nähe"
            ),
            **ROUTE,
        )
        values = iter(
            (
                "/answer",
                "5",
                "1",
                "4",
                "Rückkehr",
                "yes",
                str(destination_parent),
                "/results",
                "/quit",
            )
        )
        output: list[str] = []
        controller = ClassifiedResonanceController(
            ResonanceMode.ANSWER,
            output_writer=output.append,
            input_reader=lambda _prompt: next(values),
            nexus_root=self.nexus,
        )

        with patch(
            "atrium.classified_resonance._load_authoritative_selected_token",
            return_value=token_without_label,
        ):
            self.assertTrue(controller().completed)
        self.assertFalse(controller().completed)

        results = "\n".join(output)
        self.assertIn(
            "No public-safe summary was attached to the carried resonance.",
            results,
        )

    def test_only_success_activates_answer_post_run_gate(self) -> None:
        destination_parent = self.root / "answer-after-cancel"
        destination_parent.mkdir()
        values = iter(
            (
                "/answer",
                "/cancel",
                "/answer",
                "1",
                "1",
                "1",
                "return",
                "yes",
                str(destination_parent),
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
        destination_parent = self.root / "answer-before-interrupt"
        destination_parent.mkdir()
        values = iter(
            ("/answer", "1", "1", "1", "return", "yes", str(destination_parent))
        )
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
