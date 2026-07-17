from __future__ import annotations

from pathlib import Path
import tempfile
import unittest

from atrium.classified_resonance import ClassifiedResonanceController
from atrium.resonance_mode import ResonanceMode
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
        values = iter(answers)
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
        self.assertTrue(any("travelling invitation" in prompt for prompt in prompts))

    def test_cancellation_at_each_boundary_publishes_nothing(self) -> None:
        cases = (
            ("during-collection", ("/cancel",)),
            ("before-confirmation", ("1", "1", "1", "trust", "no")),
            ("before-first-destination", ("1", "1", "1", "trust", "yes", "")),
            (
                "before-second-destination",
                ("1", "1", "1", "trust", "yes", str(self.travelling_root), ""),
            ),
        )
        for name, answers in cases:
            with self.subTest(name=name):
                result, _, transcript = self.run_compose(answers)
                self.assertFalse(result.completed)
                self.assertIn("No invitation or workspace was created", transcript)
                self.assertFalse(self.travelling_root.exists())
                self.assertFalse(self.private_root.exists())

    def test_no_overwrite_preserves_existing_invitation(self) -> None:
        first, _, _ = self.run_compose(self.successful_answers())
        self.assertTrue(first.completed)
        invitation = self.travelling_root / invitation_name(ROUTE.return_slot_id)
        marker = invitation / "local-marker"
        marker.write_text("preserve", encoding="utf-8")

        second, _, transcript = self.run_compose(self.successful_answers())
        self.assertFalse(second.completed)
        self.assertIn("Refusing to overwrite", transcript)
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
        self.assertFalse(
            (self.travelling_root / invitation_name(ROUTE.return_slot_id)).exists()
        )
        self.assertFalse(
            (self.private_root / workspace_name(ROUTE.return_slot_id)).exists()
        )

    def test_private_outputs_cannot_be_published_inside_carrier(self) -> None:
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
        self.assertEqual(list(carrier.iterdir()), [])
        self.assertFalse(self.private_root.exists())

    def test_corrected_compose_route_never_reaches_legacy_controller(self) -> None:
        values = iter(("resonance", "/cancel", "quit"))

        def forbidden_legacy():
            raise AssertionError("legacy one-person controller was reached")

        runtime = run_nexus_terminal(
            activation_loader=lambda: object(),
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


if __name__ == "__main__":
    unittest.main()
