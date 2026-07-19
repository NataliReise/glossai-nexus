from __future__ import annotations

from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest

from atrium.classified_resonance import (
    ClassifiedResonanceController,
    CompletedComposeResult,
)
from atrium.resonance_mode import ResonanceMode
from atrium.runtime import ChamberRunResult, NexusAtriumRuntime
from atrium.state import AtriumState, RESONANCE_CHAMBER
from atrium.terminal import run_nexus_terminal
import resonance_invitation_runtime as publication_module
from resonance_invitation_runtime import (
    InvitationPublicationError,
    RouteIdentity,
    invitation_name,
    prepare_resonance_invitation,
    workspace_name,
)
from return_resonance.slots import load_return_slots
from return_resonance.token import TOKEN_VERSION_V2, load_resonance_token


ROUTE = RouteIdentity(
    module_id="N01",
    layer_id="return-resonance-1",
    origin_trace_id="n01-origin-compose-atrium",
    return_slot_id="n01-slot-compose-atrium",
    package_id="n01-package-compose-atrium",
)


class ComposeAtriumTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.travelling_root = self.root / "travelling"
        self.private_root = self.root / "retained-private"

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def run_compose(self, answers: tuple[str, ...], **overrides):
        values = iter(("/compose", *answers))
        prompts: list[str] = []
        output: list[str] = []

        def read(prompt: str) -> str:
            prompts.append(prompt)
            return next(values)

        controller = ClassifiedResonanceController(
            ResonanceMode.COMPOSE,
            output_writer=output.append,
            input_reader=read,
            route_factory=lambda: ROUTE,
            **overrides,
        )
        return controller(), prompts, "\n".join(output)

    def successful_answers(self) -> tuple[str, ...]:
        return (
            "5",
            "4",
            "3",
            "Nähe",
            "yes",
            str(self.travelling_root),
            str(self.private_root),
        )

    def test_real_compose_publishes_one_strictly_separated_pair(self) -> None:
        result, prompts, transcript = self.run_compose(self.successful_answers())
        self.assertTrue(result.completed)
        invitation = self.travelling_root / invitation_name(ROUTE.return_slot_id)
        workspace = self.private_root / workspace_name(ROUTE.return_slot_id)
        self.assertEqual(
            {path.name for path in invitation.iterdir()},
            {"README.md", "resonance_token.local.json"},
        )
        token = load_resonance_token(invitation / "resonance_token.local.json")
        self.assertEqual(
            (invitation / "resonance_token.local.json").read_bytes(),
            token.to_json().encode("utf-8"),
        )
        self.assertEqual(token.token_version, TOKEN_VERSION_V2)
        self.assertEqual(token.image_id, "bridge-in-mist")
        self.assertEqual(token.scent_id, "first-snow")
        self.assertEqual(token.movement_id, "returning-tide")
        self.assertEqual(token.wish_word, "Nähe")
        slot = load_return_slots(workspace / "private/return_slots.local.json")[0]
        for field_name in (
            "module_id",
            "layer_id",
            "origin_trace_id",
            "return_slot_id",
            "package_id",
        ):
            self.assertEqual(getattr(token, field_name), getattr(slot, field_name))

        invitation_names = {path.name for path in invitation.rglob("*")}
        workspace_names = {path.name for path in workspace.rglob("*")}
        self.assertNotIn("return_slots.local.json", invitation_names)
        self.assertNotIn("resonance_token.local.json", workspace_names)
        for forbidden in (
            "activation.local.json",
            "activation.local.resonance-context.json",
            "return_artifact.local.json",
            "return_result.local.md",
        ):
            self.assertNotIn(forbidden, invitation_names | workspace_names)
        self.assertEqual(
            {path.relative_to(invitation) for path in invitation.rglob("*.json")},
            {Path("resonance_token.local.json")},
        )
        self.assertEqual(
            {path.relative_to(workspace) for path in workspace.rglob("*.json")},
            {Path("private/return_slots.local.json")},
        )
        self.assertEqual(list((workspace / "incoming").iterdir()), [])
        self.assertEqual(list((workspace / "results").iterdir()), [])
        self.assertFalse(
            any(
                path.name.startswith("nexus-01-neutral-carrier")
                for path in self.root.rglob("*")
            )
        )
        self.assertFalse(any("response" in line.casefold() for line in transcript.splitlines()))
        self.assertFalse(any("return word" in line.casefold() for line in transcript.splitlines()))
        self.assertIn("Your originating resonance", transcript)
        self.assertIn("Travelling Resonance invitation", transcript)
        self.assertIn("Private Return Workspace", transcript)
        self.assertIn("manually", transcript)
        self.assertIn("does not choose the recipient's activation mode", transcript)
        self.assertIn("one choice at a time", transcript)
        self.assertIn("private reasons are not stored", transcript)
        self.assertIn("Nothing is sent, uploaded, synchronized, or published", transcript)
        self.assertIn("Use /cancel at any interactive prompt", transcript)
        self.assertIn("end the current Resonance cycle safely", transcript)
        self.assertIn("At yes/no prompts, you may also answer no", transcript)
        self.assertIn("blank input also cancels creation", transcript)
        self.assertIn("Full-cycle cancellation returns safely to the Atrium", transcript)
        self.assertNotIn("Previous confirmation forms", transcript)
        self.assertIn("If you choose to carry this invitation", transcript)
        self.assertIn("Nothing requires you to carry, forward, publish, or share", transcript)
        self.assertLess(
            transcript.index("Resonance invitation shaped"),
            transcript.index("Travelling Resonance invitation:"),
        )
        self.assertLess(
            transcript.index("Local creation complete"),
            transcript.index("Local paths"),
        )
        self.assertLess(
            transcript.index("Local paths"),
            transcript.index("Optional manual carrying"),
        )
        self.assertTrue(any("travelling invitation" in prompt for prompt in prompts))

    def test_cancellation_at_each_boundary_publishes_nothing(self) -> None:
        cases = (
            ("at-image", ("/cancel",)),
            ("at-scent", ("1", "/cancel")),
            ("at-movement", ("1", "1", "/cancel")),
            ("at-wish-word", ("1", "1", "1", "/cancel")),
            ("before-confirmation", ("1", "1", "1", "trust", "no")),
            ("before-first-destination", ("1", "1", "1", "trust", "yes", "")),
            (
                "before-second-destination",
                ("1", "1", "1", "trust", "yes", str(self.travelling_root), ""),
            ),
        )

        def forbidden_preparer(*_args, **_kwargs):
            raise AssertionError("invitation preparer was called after cancellation")

        for name, answers in cases:
            with self.subTest(name=name):
                result, _, transcript = self.run_compose(
                    answers,
                    invitation_preparer=forbidden_preparer,
                )
                self.assertFalse(result.completed)
                self.assertIn("No invitation or workspace was created", transcript)
                self.assertIn("Nothing was written", transcript)
                self.assertIn("remains unfinished", transcript)
                self.assertIn("Returning safely to the Atrium", transcript)
                self.assertFalse(self.travelling_root.exists())
                self.assertFalse(self.private_root.exists())

    def test_slash_cancel_at_new_compose_boundaries_publishes_nothing(self) -> None:
        cases = (
            ("walkthrough-confirmation", ("/walkthrough", " /Cancel ")),
            ("creation-confirmation", ("1", "1", "1", "trust", "/cancel")),
            (
                "invitation-destination",
                ("1", "1", "1", "trust", "yes", " /Cancel "),
            ),
            (
                "workspace-destination",
                (
                    "1",
                    "1",
                    "1",
                    "trust",
                    "yes",
                    str(self.travelling_root),
                    "/CANCEL",
                ),
            ),
        )

        def forbidden_preparer(*_args, **_kwargs):
            raise AssertionError("invitation preparer was called after /cancel")

        for name, answers in cases:
            with self.subTest(name=name):
                result, _, transcript = self.run_compose(
                    answers,
                    invitation_preparer=forbidden_preparer,
                )
                self.assertFalse(result.completed)
                self.assertIn("Nothing was written", transcript)
                self.assertIn("remains unfinished", transcript)
                self.assertFalse(self.travelling_root.exists())
                self.assertFalse(self.private_root.exists())

    def test_compose_confirmation_compatibility_declines_remain_supported(self) -> None:
        def forbidden_preparer(*_args, **_kwargs):
            raise AssertionError("declined creation invoked invitation preparation")

        for answer in ("no", "cancel", "q"):
            with self.subTest(answer=answer):
                result, _, transcript = self.run_compose(
                    ("1", "1", "1", "trust", answer),
                    invitation_preparer=forbidden_preparer,
                )
                self.assertFalse(result.completed)
                self.assertIn("Nothing was written", transcript)

    def test_compose_path_with_cancel_prefix_is_not_a_command(self) -> None:
        calls: list[dict[str, Path]] = []

        def capture_preparer(_token, **kwargs):
            calls.append(kwargs)
            return SimpleNamespace(
                token=_token,
                invitation_path=kwargs["invitation_root"] / "invitation",
                private_workspace_path=kwargs["private_root"] / "workspace",
            )

        result, _, _ = self.run_compose(
            (
                "1",
                "1",
                "1",
                "trust",
                "yes",
                "/cancelled/example",
                str(self.private_root),
            ),
            invitation_preparer=capture_preparer,
        )

        self.assertTrue(result.completed)
        self.assertEqual(calls[0]["invitation_root"], Path("/cancelled/example"))

    def test_compose_exploration_is_nonwriting_and_reveals_only_current_step(self) -> None:
        def forbidden_preparer(*_args, **_kwargs):
            raise AssertionError("information command invoked invitation preparation")

        result, prompts, transcript = self.run_compose(
            ("/look", "/help", "/trace", "/cancel"),
            invitation_preparer=forbidden_preparer,
        )

        self.assertFalse(result.completed)
        self.assertIn("An open field of images", transcript)
        self.assertIn("Enter one of the numbers shown for this step", transcript)
        self.assertIn("Notice which image", transcript)
        self.assertGreaterEqual(transcript.count("Begin with one image"), 4)
        self.assertNotIn("Now choose one scent", transcript)
        self.assertNotIn("Let the trace move", transcript)
        self.assertEqual(prompts[0], "resonance> ")
        self.assertTrue(all(prompt == "Enter a number: " for prompt in prompts[1:]))
        self.assertFalse(self.travelling_root.exists())
        self.assertFalse(self.private_root.exists())

    def test_compose_trace_preserves_prior_selection_and_completion(self) -> None:
        preparations = 0

        def counted_preparer(token, **kwargs):
            nonlocal preparations
            preparations += 1
            return prepare_resonance_invitation(token, **kwargs)

        answers = (
            "5",
            "/trace",
            "4",
            "3",
            "Nähe",
            "yes",
            str(self.travelling_root),
            str(self.private_root),
        )
        result, _, transcript = self.run_compose(
            answers,
            invitation_preparer=counted_preparer,
        )

        self.assertTrue(result.completed)
        self.assertEqual(preparations, 1)
        invitation = self.travelling_root / invitation_name(ROUTE.return_slot_id)
        token = load_resonance_token(invitation / "resonance_token.local.json")
        self.assertEqual(token.image_id, "bridge-in-mist")
        self.assertEqual(token.scent_id, "first-snow")
        self.assertIn("Attend to the scent", transcript)
        self.assertLess(
            transcript.index("Attend to the scent"),
            transcript.index("Let the trace move"),
        )

    def test_compose_walkthrough_can_stop_without_selecting_or_publishing(self) -> None:
        def forbidden_preparer(*_args, **_kwargs):
            raise AssertionError("walkthrough invoked invitation preparation")

        result, prompts, transcript = self.run_compose(
            ("/walkthrough", "yes", "/walkthrough", "/cancel"),
            invitation_preparer=forbidden_preparer,
        )

        self.assertFalse(result.completed)
        self.assertEqual(transcript.count("Chamber voice"), 1)
        self.assertIn("image that will be carried", transcript)
        self.assertIn("Guided walkthrough ended", transcript)
        self.assertEqual(transcript.count("Begin with one image"), 3)
        self.assertEqual(prompts[0], "resonance> ")
        self.assertTrue(
            all("number" in prompt for prompt in prompts[1:] if "guided" not in prompt)
        )
        self.assertFalse(self.travelling_root.exists())
        self.assertFalse(self.private_root.exists())

    def test_compose_walkthrough_guides_each_step_once_and_preserves_completion(self) -> None:
        preparations = 0

        def counted_preparer(token, **kwargs):
            nonlocal preparations
            preparations += 1
            return prepare_resonance_invitation(token, **kwargs)

        result, _, transcript = self.run_compose(
            (
                "/walkthrough",
                "yes",
                "5",
                "/look",
                "4",
                "3",
                "Nähe",
                "yes",
                str(self.travelling_root),
                str(self.private_root),
            ),
            invitation_preparer=counted_preparer,
        )

        self.assertTrue(result.completed)
        self.assertEqual(preparations, 1)
        self.assertEqual(transcript.count("Chamber voice"), 4)
        for guidance in (
            "image that will be carried",
            "scent that will stand beside",
            "originating trace will move",
            "wish word without explaining",
        ):
            self.assertEqual(transcript.count(guidance), 1)
        invitation = self.travelling_root / invitation_name(ROUTE.return_slot_id)
        token = load_resonance_token(invitation / "resonance_token.local.json")
        self.assertEqual(token.image_id, "bridge-in-mist")
        self.assertEqual(token.scent_id, "first-snow")
        self.assertEqual(token.movement_id, "returning-tide")
        self.assertEqual(token.wish_word, "Nähe")

    def test_no_overwrite_preserves_existing_invitation(self) -> None:
        first, _, _ = self.run_compose(self.successful_answers())
        self.assertTrue(first.completed)
        invitation = self.travelling_root / invitation_name(ROUTE.return_slot_id)
        marker = invitation / "local-marker"
        marker.write_text("preserve", encoding="utf-8")

        second, _, transcript = self.run_compose(self.successful_answers())
        self.assertFalse(second.completed)
        self.assertIn("Refusing to overwrite", transcript)
        self.assertIn("were not created", transcript)
        self.assertIn("Existing material was not replaced", transcript)
        self.assertEqual(marker.read_text(encoding="utf-8"), "preserve")

    def test_second_publication_failure_rolls_back_invitation(self) -> None:
        calls = 0

        def fail_second(staged: Path, final: Path) -> None:
            nonlocal calls
            calls += 1
            if calls == 2:
                raise InvitationPublicationError("injected second publication failure")
            publication_module._publish(staged, final)

        def failing_preparer(token, **kwargs):
            return prepare_resonance_invitation(
                token,
                **kwargs,
                _publisher=fail_second,
            )

        result, _, transcript = self.run_compose(
            self.successful_answers(), invitation_preparer=failing_preparer
        )
        self.assertFalse(result.completed)
        self.assertIn("No partial invitation", transcript)
        self.assertIn("Nothing from this attempt was kept", transcript)
        self.assertFalse(
            (self.travelling_root / invitation_name(ROUTE.return_slot_id)).exists()
        )
        self.assertFalse(
            (self.private_root / workspace_name(ROUTE.return_slot_id)).exists()
        )

    def test_invitation_output_cannot_be_published_inside_carrier(self) -> None:
        carrier = self.root / "carrier"
        carrier.mkdir()
        answers = (
            "1",
            "1",
            "1",
            "trust",
            "yes",
            str(carrier / "travelling"),
            str(self.private_root),
        )
        result, _, transcript = self.run_compose(answers, nexus_root=carrier)
        self.assertFalse(result.completed)
        self.assertIn("outside the travelling Nexus carrier", transcript)
        self.assertIn("Nothing from this attempt was kept", transcript)
        self.assertEqual(list(carrier.iterdir()), [])
        self.assertFalse(self.private_root.exists())

    def test_private_output_cannot_be_published_inside_carrier(self) -> None:
        carrier = self.root / "carrier"
        carrier.mkdir()
        answers = (
            "1",
            "1",
            "1",
            "trust",
            "yes",
            str(self.travelling_root),
            str(carrier / "private"),
        )
        result, _, transcript = self.run_compose(answers, nexus_root=carrier)
        self.assertFalse(result.completed)
        self.assertIn("outside the travelling Nexus carrier", transcript)
        self.assertIn("Nothing from this attempt was kept", transcript)
        self.assertEqual(list(carrier.iterdir()), [])
        self.assertFalse(self.travelling_root.exists())

    def test_corrected_compose_route_never_reaches_legacy_controller(self) -> None:
        values = iter(
            ("/first-spark", "/resonance", "/compose", "/cancel", "/quit")
        )

        class GiftActivation:
            profile_id = "first-spark"
            activation_purpose = "gift"

        def forbidden_legacy():
            raise AssertionError("legacy one-person controller was reached")

        runtime = run_nexus_terminal(
            activation_loader=GiftActivation,
            first_spark_runner=lambda: ChamberRunResult(completed=True),
            resonance_runner=forbidden_legacy,
            resonance_mode=ResonanceMode.COMPOSE,
            classified_resonance_runner=ClassifiedResonanceController(
                ResonanceMode.COMPOSE,
                output_writer=lambda _message: None,
                input_reader=lambda _prompt: next(values),
                route_factory=lambda: ROUTE,
            ),
            input_reader=lambda _prompt: next(values),
            output_writer=lambda _message: None,
        )
        self.assertEqual(runtime.resonance_mode, ResonanceMode.COMPOSE)

    def test_successful_compose_reentry_waits_in_post_run_until_quit(self) -> None:
        values = iter(
            (
                "/compose",
                *self.successful_answers(),
                " /LOOK ",
                "help",
                "/trace",
                "/quit",
            )
        )
        output: list[str] = []
        preparations = 0

        def counted_preparer(token, **kwargs):
            nonlocal preparations
            preparations += 1
            return prepare_resonance_invitation(token, **kwargs)

        controller = ClassifiedResonanceController(
            ResonanceMode.COMPOSE,
            output_writer=output.append,
            input_reader=lambda _prompt: next(values),
            route_factory=lambda: ROUTE,
            invitation_preparer=counted_preparer,
        )

        self.assertTrue(controller().completed)
        self.assertFalse(controller().completed)

        transcript = "\n".join(output)
        self.assertEqual(preparations, 1)
        self.assertIn("Resonance cycle complete", transcript)
        self.assertIn("This cycle will not begin again automatically", transcript)
        self.assertGreaterEqual(transcript.count("Resonance Chamber — completed cycle"), 2)
        self.assertIn("Another originating trace begins only if you choose /compose", transcript)
        self.assertIn("/compose — begin another independent originating cycle", transcript)
        self.assertIn("Returning safely to the Atrium", transcript)

    def test_only_success_activates_compose_post_run_gate(self) -> None:
        values = iter(
            ("/compose", "/cancel", "/compose", *self.successful_answers())
        )
        output: list[str] = []
        controller = ClassifiedResonanceController(
            ResonanceMode.COMPOSE,
            output_writer=output.append,
            input_reader=lambda _prompt: next(values),
            route_factory=lambda: ROUTE,
        )

        self.assertFalse(controller().completed)
        self.assertTrue(controller().completed)

        transcript = "\n".join(output)
        self.assertEqual(transcript.count("Resonance Chamber — shape a resonance invitation"), 2)
        self.assertNotIn("Resonance Chamber — completed cycle", transcript)

    def test_compose_post_run_exposes_results_and_rejects_bare_results(self) -> None:
        values = iter(
            (
                "/compose",
                *self.successful_answers(),
                "",
                "/leave",
                "compose",
                "/results",
                "results",
                "/answer",
                "/new-answer",
                "/unknown",
                " /HELP ",
                "/quit",
            )
        )
        prompts: list[str] = []
        output: list[str] = []

        def read(prompt: str) -> str:
            prompts.append(prompt)
            return next(values)

        controller = ClassifiedResonanceController(
            ResonanceMode.COMPOSE,
            output_writer=output.append,
            input_reader=read,
            route_factory=lambda: ROUTE,
        )
        self.assertTrue(controller().completed)
        self.assertFalse(controller().completed)

        transcript = "\n".join(output)
        post_run = transcript[transcript.index("Resonance Chamber — completed cycle") :]
        self.assertEqual(post_run.count("Unknown Resonance command."), 6)
        self.assertIn(
            "/results — view this session's most recent completed cycle", post_run
        )
        self.assertIn(
            "Resonance results — most recent originating cycle in this session",
            post_run,
        )
        self.assertIn("Earlier local outputs remain separate and unchanged.", post_run)
        self.assertNotIn("/answer —", post_run)
        self.assertNotIn("/new-answer —", post_run)
        self.assertTrue(all(prompt == "resonance> " for prompt in prompts[-10:]))

    def test_compose_results_are_allowlisted_view_only_and_return_to_prompt(self) -> None:
        values = iter(
            ("/compose", *self.successful_answers(), "/results", "/quit")
        )
        output: list[str] = []
        prompts: list[str] = []
        preparations = 0

        def read(prompt: str) -> str:
            prompts.append(prompt)
            return next(values)

        def counted_preparer(token, **kwargs):
            nonlocal preparations
            preparations += 1
            return prepare_resonance_invitation(token, **kwargs)

        controller = ClassifiedResonanceController(
            ResonanceMode.COMPOSE,
            output_writer=output.append,
            input_reader=read,
            route_factory=lambda: ROUTE,
            invitation_preparer=counted_preparer,
        )

        self.assertIsNone(controller._last_completed_result)
        self.assertTrue(controller().completed)
        retained = controller._last_completed_result
        self.assertIsInstance(retained, CompletedComposeResult)
        self.assertFalse(controller().completed)
        self.assertIs(controller._last_completed_result, retained)
        self.assertEqual(preparations, 1)

        transcript = "\n".join(output)
        results = transcript[transcript.index("Resonance results —") :]
        for text in (
            "[private local]",
            "    Image: A narrow bridge in the mist",
            "    Scent: Cold air before the first snow",
            "    Movement: A tide beginning to return",
            "    Wish word: Nähe",
            "[public-safe]",
            "No public-safe summary was created for this cycle",
            "[local path]",
            "Travelling invitation:",
            "Private Return Workspace:",
            "— available",
        ):
            self.assertIn(text, results)
        for hidden in (
            "token_version",
            "origin_trace_id",
            ROUTE.origin_trace_id,
            ROUTE.package_id,
            "CompletedComposeResult",
            "ResonanceToken(",
        ):
            self.assertNotIn(hidden, results)
        self.assertEqual(prompts[-2:], ["resonance> ", "resonance> "])

    def test_compose_results_report_only_missing_known_paths(self) -> None:
        invitation = self.root / "known-invitation"
        workspace = self.root / "known-workspace"
        invitation.mkdir()
        workspace.mkdir()
        values = iter(
            ("/compose", *self.successful_answers(), "/results", "/quit")
        )
        output: list[str] = []

        def prepare(token, **_kwargs):
            return SimpleNamespace(
                token=token,
                invitation_path=invitation,
                private_workspace_path=workspace,
            )

        controller = ClassifiedResonanceController(
            ResonanceMode.COMPOSE,
            output_writer=output.append,
            input_reader=lambda _prompt: next(values),
            route_factory=lambda: ROUTE,
            invitation_preparer=prepare,
        )

        self.assertTrue(controller().completed)
        invitation.rmdir()
        workspace.rmdir()
        self.assertFalse(controller().completed)

        results = "\n".join(output)
        self.assertIn("Wish word: Nähe", results)
        self.assertIn(
            f"Travelling invitation: {invitation} — no longer available at the known location",
            results,
        )
        self.assertIn(
            f"Private Return Workspace: {workspace} — no longer available at the known location",
            results,
        )
        self.assertEqual(results.count("No filesystem search was performed."), 1)

    def test_explicit_compose_starts_fresh_independent_second_cycle(self) -> None:
        second_travelling = self.root / "travelling-two"
        second_private = self.root / "retained-private-two"
        routes = iter(
            (
                ROUTE,
                RouteIdentity(
                    module_id="N01",
                    layer_id="return-resonance-1",
                    origin_trace_id="n01-origin-compose-second",
                    return_slot_id="n01-slot-compose-second",
                    package_id="n01-package-compose-second",
                ),
            )
        )
        values = iter(
            (
                "/compose",
                *self.successful_answers(),
                "/compose",
                "1",
                "2",
                "4",
                "Weite",
                "yes",
                str(second_travelling),
                str(second_private),
                "/results",
                "/quit",
            )
        )
        published_tokens = []
        output: list[str] = []

        def capture_preparer(token, **kwargs):
            published_tokens.append(token)
            return prepare_resonance_invitation(token, **kwargs)

        controller = ClassifiedResonanceController(
            ResonanceMode.COMPOSE,
            output_writer=output.append,
            input_reader=lambda _prompt: next(values),
            route_factory=lambda: next(routes),
            invitation_preparer=capture_preparer,
        )

        self.assertTrue(controller().completed)
        self.assertTrue(controller().completed)
        self.assertFalse(controller().completed)
        self.assertEqual(len(published_tokens), 2)
        self.assertEqual(
            [token.wish_word for token in published_tokens],
            ["Nähe", "Weite"],
        )
        self.assertNotEqual(
            published_tokens[0].return_slot_id,
            published_tokens[1].return_slot_id,
        )
        self.assertTrue(
            (second_travelling / invitation_name("n01-slot-compose-second")).is_dir()
        )
        self.assertTrue(
            (second_private / workspace_name("n01-slot-compose-second")).is_dir()
        )
        self.assertTrue(
            (self.travelling_root / invitation_name(ROUTE.return_slot_id)).is_dir()
        )
        self.assertTrue(
            (self.private_root / workspace_name(ROUTE.return_slot_id)).is_dir()
        )
        results = "\n".join(output)
        results = results[results.index("Resonance results —") :]
        self.assertIn("most recent originating cycle in this session", results)
        self.assertIn("Earlier local outputs remain separate and unchanged.", results)
        self.assertIn("Wish word: Weite", results)
        self.assertNotIn("Wish word: Nähe", results)

    def test_cancelled_second_compose_preserves_prior_atrium_milestone(self) -> None:
        values = iter(
            (
                "/compose",
                *self.successful_answers(),
                "/compose",
                "/cancel",
                "/results",
                "/quit",
            )
        )
        controller = ClassifiedResonanceController(
            ResonanceMode.COMPOSE,
            output_writer=lambda _message: None,
            input_reader=lambda _prompt: next(values),
            route_factory=lambda: ROUTE,
        )
        runtime = NexusAtriumRuntime(
            state=AtriumState.activated(frozenset({RESONANCE_CHAMBER})),
            resonance_mode=ResonanceMode.COMPOSE,
        )

        self.assertTrue(runtime.enter_chamber(RESONANCE_CHAMBER, controller).completed)
        retained = controller._last_completed_result
        self.assertIsNotNone(retained)
        self.assertTrue(runtime.state.is_completed(RESONANCE_CHAMBER))
        completed_state = runtime.state
        self.assertFalse(runtime.enter_chamber(RESONANCE_CHAMBER, controller).completed)
        self.assertIs(controller._last_completed_result, retained)
        self.assertTrue(runtime.state.is_completed(RESONANCE_CHAMBER))
        self.assertFalse(runtime.enter_chamber(RESONANCE_CHAMBER, controller).completed)
        self.assertEqual(runtime.state, completed_state)
        self.assertIs(controller._last_completed_result, retained)
        self.assertTrue(runtime.state.is_completed(RESONANCE_CHAMBER))

    def test_failed_second_compose_preserves_gate_and_prior_atrium_milestone(self) -> None:
        second_travelling = self.root / "failed-travelling"
        second_private = self.root / "failed-private"
        values = iter(
            (
                "/compose",
                *self.successful_answers(),
                "/compose",
                "1",
                "1",
                "1",
                "again",
                "yes",
                str(second_travelling),
                str(second_private),
                "/quit",
            )
        )
        preparations = 0

        def fail_second_preparation(token, **kwargs):
            nonlocal preparations
            preparations += 1
            if preparations == 2:
                raise InvitationPublicationError("injected second-cycle failure")
            return prepare_resonance_invitation(token, **kwargs)

        controller = ClassifiedResonanceController(
            ResonanceMode.COMPOSE,
            output_writer=lambda _message: None,
            input_reader=lambda _prompt: next(values),
            route_factory=lambda: ROUTE,
            invitation_preparer=fail_second_preparation,
        )
        runtime = NexusAtriumRuntime(
            state=AtriumState.activated(frozenset({RESONANCE_CHAMBER})),
            resonance_mode=ResonanceMode.COMPOSE,
        )

        self.assertTrue(runtime.enter_chamber(RESONANCE_CHAMBER, controller).completed)
        retained = controller._last_completed_result
        self.assertIsNotNone(retained)
        self.assertFalse(runtime.enter_chamber(RESONANCE_CHAMBER, controller).completed)
        self.assertIs(controller._last_completed_result, retained)
        self.assertTrue(runtime.state.is_completed(RESONANCE_CHAMBER))
        self.assertFalse(runtime.enter_chamber(RESONANCE_CHAMBER, controller).completed)
        self.assertTrue(runtime.state.is_completed(RESONANCE_CHAMBER))
        self.assertEqual(preparations, 2)


if __name__ == "__main__":
    unittest.main()
