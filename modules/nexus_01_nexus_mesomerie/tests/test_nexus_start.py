from __future__ import annotations

from pathlib import Path
import tempfile
import unittest
from unittest.mock import Mock, patch

from atrium import NexusAtriumRuntime, ResonanceMode
from chambers.resonance import (
    OriginatingResonanceContribution,
    build_resonance_token_v2,
)
from recipient_activation import (
    ActivationChoiceResult,
    activate_normally,
    activate_with_resonance_token,
    paths_for_nexus,
)
import run_nexus as start_module
from run_nexus import run_corrected_nexus


RECIPIENT = {
    "recipient_alias": "Mélanie",
    "activation_purpose": "gift",
    "private_message": "Für dich",
}
ROUTE = {
    "module_id": "N01",
    "layer_id": "return-resonance-1",
    "origin_trace_id": "n01-origin-start-test",
    "return_slot_id": "n01-slot-start-test",
    "package_id": "n01-package-start-test",
}


class NexusStartTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.nexus = self.root / "nexus"
        (self.nexus / "first_spark").mkdir(parents=True)
        self.token = self.root / "resonance-token-v2.json"
        token = build_resonance_token_v2(
            OriginatingResonanceContribution(
                "waiting-lantern", "summer-rain", "falling-feather", "Nähe"
            ),
            **ROUTE,
        )
        self.token.write_text(token.to_json(), encoding="utf-8")

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def start_with_answers(self, *answers: str):
        values = iter(answers)
        captured: dict[str, object] = {}

        def atrium_runner(**kwargs):
            captured.update(kwargs)
            return NexusAtriumRuntime.from_activation(
                kwargs["activation_loader"](), kwargs["resonance_mode"]
            )

        result = run_corrected_nexus(
            nexus_root=self.nexus,
            input_reader=lambda _prompt: next(values),
            output_writer=lambda _message: None,
            atrium_runner=atrium_runner,
            **RECIPIENT,
        )
        return result, captured

    def test_first_launch_normal_activates_then_opens_compose_atrium(self) -> None:
        runtime, captured = self.start_with_answers("1")
        self.assertIsNotNone(runtime)
        self.assertEqual(captured["resonance_mode"], ResonanceMode.COMPOSE)
        self.assertEqual(runtime.resonance_mode, ResonanceMode.COMPOSE)
        self.assertIsNone(
            captured["classified_resonance_runner"]._known_resonance_source
        )

    def test_first_launch_token_v2_activates_then_opens_answer_atrium(self) -> None:
        runtime, captured = self.start_with_answers("2", str(self.token))
        self.assertIsNotNone(runtime)
        self.assertEqual(captured["resonance_mode"], ResonanceMode.ANSWER)
        self.assertEqual(runtime.resonance_mode, ResonanceMode.ANSWER)
        classified = captured["classified_resonance_runner"]
        self.assertEqual(classified.nexus_root, self.nexus)

    def test_first_launch_cancellation_writes_nothing_and_skips_atrium(self) -> None:
        atrium_runner = Mock(side_effect=AssertionError("Atrium must not open"))
        result = run_corrected_nexus(
            nexus_root=self.nexus,
            input_reader=lambda _prompt: "q",
            output_writer=lambda _message: None,
            atrium_runner=atrium_runner,
            **RECIPIENT,
        )
        self.assertIsNone(result)
        self.assertFalse(paths_for_nexus(self.nexus).activation.exists())
        atrium_runner.assert_not_called()

    def test_restart_first_spark_does_not_prompt_or_invoke_controller(self) -> None:
        activate_normally(nexus_root=self.nexus, **RECIPIENT)
        controller = Mock(side_effect=AssertionError("must not prompt again"))
        captured: dict[str, object] = {}

        def atrium_runner(**kwargs):
            captured.update(kwargs)
            return NexusAtriumRuntime.from_activation(
                kwargs["activation_loader"](), kwargs["resonance_mode"]
            )

        run_corrected_nexus(
            nexus_root=self.nexus,
            activation_controller=controller,
            atrium_runner=atrium_runner,
            input_reader=lambda _prompt: (_ for _ in ()).throw(
                AssertionError("must not prompt")
            ),
            output_writer=lambda _message: None,
            **RECIPIENT,
        )
        controller.assert_not_called()
        self.assertEqual(captured["resonance_mode"], ResonanceMode.COMPOSE)

    def test_restart_valid_resonance_does_not_prompt_and_opens_answer(self) -> None:
        activate_with_resonance_token(
            self.token, nexus_root=self.nexus, **RECIPIENT
        )
        controller = Mock(side_effect=AssertionError("must not prompt again"))
        captured: dict[str, object] = {}

        def atrium_runner(**kwargs):
            captured.update(kwargs)
            return NexusAtriumRuntime.from_activation(
                kwargs["activation_loader"](), kwargs["resonance_mode"]
            )

        run_corrected_nexus(
            nexus_root=self.nexus,
            activation_controller=controller,
            atrium_runner=atrium_runner,
            input_reader=lambda _prompt: (_ for _ in ()).throw(
                AssertionError("must not prompt")
            ),
            output_writer=lambda _message: None,
            **RECIPIENT,
        )
        controller.assert_not_called()
        self.assertEqual(captured["resonance_mode"], ResonanceMode.ANSWER)

    def test_missing_or_altered_selected_token_opens_blocked_atrium(self) -> None:
        for mutation in ("missing", "altered"):
            with self.subTest(mutation=mutation):
                nexus = self.root / f"nexus-{mutation}"
                (nexus / "first_spark").mkdir(parents=True)
                activate_with_resonance_token(self.token, nexus_root=nexus, **RECIPIENT)
                selected = paths_for_nexus(nexus).selected_token
                if mutation == "missing":
                    selected.unlink()
                else:
                    selected.write_bytes(selected.read_bytes() + b" ")
                captured: dict[str, object] = {}

                def atrium_runner(**kwargs):
                    captured.update(kwargs)
                    return NexusAtriumRuntime.from_activation(
                        kwargs["activation_loader"](), kwargs["resonance_mode"]
                    )

                run_corrected_nexus(
                    nexus_root=nexus,
                    atrium_runner=atrium_runner,
                    input_reader=lambda _prompt: (_ for _ in ()).throw(
                        AssertionError("blocked restart must not prompt")
                    ),
                    output_writer=lambda _message: None,
                    **RECIPIENT,
                )
                self.assertEqual(
                    captured["resonance_mode"],
                    ResonanceMode.BLOCKED_ANSWER_RECOVERY,
                )

    def test_forged_return_resonance_activation_opens_blocked_atrium(self) -> None:
        paths_for_nexus(self.nexus).activation.write_text(
            '{"profile_id":"return-resonance"}\n', encoding="utf-8"
        )
        _, captured = self.start_with_answers()
        self.assertEqual(
            captured["resonance_mode"],
            ResonanceMode.BLOCKED_ANSWER_RECOVERY,
        )

    def test_incidental_tokens_do_not_affect_existing_normal_activation(self) -> None:
        activate_normally(nexus_root=self.nexus, **RECIPIENT)
        for index in range(3):
            (self.nexus / f"unused-token-{index}.json").write_bytes(
                self.token.read_bytes()
            )
        _, captured = self.start_with_answers()
        self.assertEqual(captured["resonance_mode"], ResonanceMode.COMPOSE)

    def test_legacy_flag_uses_only_explicit_compatibility_path(self) -> None:
        with patch("run_nexus.run_nexus_terminal") as legacy_runner:
            self.assertEqual(start_module.main(["--legacy-preactivated"]), 0)
        legacy_runner.assert_called_once_with()

    def test_known_resonance_source_cli_is_optional_and_forwarded_exactly(self) -> None:
        self.assertIsNone(start_module.parse_args([]).known_resonance_source)
        lexical_source = Path("/tmp/nexus-a/../nexus-known-source.md")

        with patch("run_nexus.run_corrected_nexus") as runner:
            self.assertEqual(
                start_module.main(
                    ["--known-resonance-source", str(lexical_source)]
                ),
                0,
            )

        runner.assert_called_once()
        self.assertEqual(
            runner.call_args.kwargs["known_resonance_source"], lexical_source
        )
        self.assertEqual(
            str(runner.call_args.kwargs["known_resonance_source"]),
            "/tmp/nexus-a/../nexus-known-source.md",
        )

    def test_relative_known_resonance_source_stops_before_runtime(self) -> None:
        with patch("run_nexus.run_corrected_nexus") as runner:
            with self.assertRaises(SystemExit):
                start_module.main(
                    ["--known-resonance-source", "relative/result.md"]
                )

        runner.assert_not_called()

    def test_missing_absolute_source_reaches_controller_without_file_io(self) -> None:
        class NoFileSystemPath(type(Path())):
            def _forbid(self, *_args, **_kwargs):
                raise AssertionError("known source touched the filesystem")

            exists = _forbid
            is_file = _forbid
            stat = _forbid
            open = _forbid
            read_text = _forbid
            resolve = _forbid
            glob = _forbid
            rglob = _forbid

        activate_normally(nexus_root=self.nexus, **RECIPIENT)
        source = NoFileSystemPath(
            "/tmp/nexus-a/../nexus-known-source-not-present.md"
        )
        captured: dict[str, object] = {}

        def atrium_runner(**kwargs):
            captured.update(kwargs)
            return NexusAtriumRuntime.from_activation(
                kwargs["activation_loader"](), kwargs["resonance_mode"]
            )

        runtime = run_corrected_nexus(
            nexus_root=self.nexus,
            known_resonance_source=source,
            atrium_runner=atrium_runner,
            **RECIPIENT,
        )

        self.assertIsNotNone(runtime)
        controller = captured["classified_resonance_runner"]
        self.assertIs(controller._known_resonance_source, source)
        self.assertEqual(
            str(controller._known_resonance_source),
            "/tmp/nexus-a/../nexus-known-source-not-present.md",
        )


if __name__ == "__main__":
    unittest.main()
