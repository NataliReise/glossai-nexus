from __future__ import annotations

import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch


NEXUS_ROOT = Path(__file__).resolve().parents[1]
FIRST_SPARK_ROOT = NEXUS_ROOT / "first_spark"
for import_root in (NEXUS_ROOT, FIRST_SPARK_ROOT):
    if str(import_root) not in sys.path:
        sys.path.insert(0, str(import_root))

from chambers.resonance import (  # noqa: E402
    OriginatingResonanceContribution,
    build_resonance_token_v2,
)
from first_spark.activation import load_activation  # noqa: E402
import recipient_activation as controller  # noqa: E402
from recipient_activation import (  # noqa: E402
    ActivationChoiceResult,
    RecipientActivationError,
    ResonanceRuntimeInterpretation,
    activate_normally,
    activate_with_resonance_token,
    classify_runtime_interpretation,
    paths_for_nexus,
    run_recipient_activation,
)


ROUTE = {
    "module_id": "N01",
    "layer_id": "return-resonance-1",
    "origin_trace_id": "n01-origin-recipient-test",
    "return_slot_id": "n01-slot-recipient-test",
    "package_id": "n01-package-recipient-test",
}
RECIPIENT = {
    "recipient_alias": "Mélanie",
    "activation_purpose": "Geschenk",
    "private_message": "Für dich — später.",
}


def valid_token_bytes() -> bytes:
    token = build_resonance_token_v2(
        OriginatingResonanceContribution(
            "waiting-lantern", "summer-rain", "falling-feather", "Nähe"
        ),
        **ROUTE,
    )
    return token.to_json().encode("utf-8")


class RecipientActivationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.nexus = self.root / "nexus-copy"
        (self.nexus / "first_spark").mkdir(parents=True)
        self.token = self.root / "invitation" / "resonance_token.local.json"
        self.token.parent.mkdir()
        self.token.write_bytes(valid_token_bytes())

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def normal(self) -> None:
        activate_normally(nexus_root=self.nexus, **RECIPIENT)

    def token_activation(self) -> None:
        activate_with_resonance_token(
            self.token, nexus_root=self.nexus, **RECIPIENT
        )

    def test_normal_activation_with_no_token_nearby(self) -> None:
        self.token.unlink()
        self.normal()
        paths = paths_for_nexus(self.nexus)
        self.assertEqual(load_activation(paths.activation).profile_id, "first-spark")
        self.assertFalse(paths.selected_context.exists())
        self.assertFalse(paths.selected_token.exists())

    def test_normal_activation_is_identical_with_one_token_nearby(self) -> None:
        with patch(
            "recipient_activation._read_selected_token",
            side_effect=AssertionError("normal activation inspected a Token"),
        ):
            self.normal()
        self.assertEqual(
            classify_runtime_interpretation(nexus_root=self.nexus),
            ResonanceRuntimeInterpretation.COMPOSE,
        )

    def test_normal_activation_is_identical_with_many_tokens_nearby(self) -> None:
        for index in range(4):
            (self.token.parent / f"invitation-{index}.json").write_bytes(
                valid_token_bytes()
            )
        with patch(
            "recipient_activation._read_selected_token",
            side_effect=AssertionError("normal activation inspected nearby Tokens"),
        ):
            self.normal()
        activation = load_activation(paths_for_nexus(self.nexus).activation)
        self.assertEqual(activation.profile_id, "first-spark")
        self.assertEqual(activation.recipient_alias, RECIPIENT["recipient_alias"])

    def test_explicit_token_v2_activation_and_context(self) -> None:
        original = self.token.read_bytes()
        self.token_activation()
        paths = paths_for_nexus(self.nexus)
        activation = load_activation(paths.activation)
        self.assertEqual(activation.profile_id, "return-resonance")
        self.assertEqual(paths.selected_token.read_bytes(), original)
        self.assertEqual(self.token.read_bytes(), original)
        context = json.loads(paths.selected_context.read_text(encoding="utf-8"))
        self.assertEqual(context["selected_token_file"], paths.selected_token.name)
        self.assertNotIn("return_word", context)
        self.assertNotIn("private_message", context)
        self.assertFalse(Path(context["selected_token_file"]).is_absolute())
        self.assertEqual(
            classify_runtime_interpretation(nexus_root=self.nexus),
            ResonanceRuntimeInterpretation.ANSWER,
        )

    def test_v1_token_rejection_has_migration_message(self) -> None:
        self.token.write_text(
            json.dumps(
                {
                    "token_version": "N01-RT-1",
                    "token_type": "resonance-activation",
                    **ROUTE,
                    "enabled_chambers": ["resonance"],
                }
            ),
            encoding="utf-8",
        )
        with self.assertRaisesRegex(RecipientActivationError, "Token V2 invitation"):
            self.token_activation()
        self.assertFalse(paths_for_nexus(self.nexus).activation.exists())

    def test_invalid_token_creates_no_partial_or_fallback_state(self) -> None:
        self.token.write_text('{"token_version": "invalid"}', encoding="utf-8")
        with self.assertRaises(RecipientActivationError):
            self.token_activation()
        paths = paths_for_nexus(self.nexus)
        self.assertFalse(paths.activation.exists())
        self.assertFalse(paths.selected_context.exists())
        self.assertFalse(paths.selected_token.exists())

    def test_interactive_cancellation_creates_no_activation(self) -> None:
        output: list[str] = []
        result = run_recipient_activation(
            nexus_root=self.nexus,
            input_reader=lambda _prompt: "q",
            output_writer=output.append,
            **RECIPIENT,
        )
        self.assertEqual(result, ActivationChoiceResult.CANCELLED)
        self.assertFalse(paths_for_nexus(self.nexus).activation.exists())

    def test_blank_token_path_returns_to_explicit_activation_choice(self) -> None:
        answers = iter(("2", "", "q"))
        output: list[str] = []

        result = run_recipient_activation(
            nexus_root=self.nexus,
            input_reader=lambda _prompt: next(answers),
            output_writer=output.append,
            **RECIPIENT,
        )

        self.assertEqual(result, ActivationChoiceResult.CANCELLED)
        transcript = "\n".join(output)
        self.assertIn("selected carried trace could not be opened", transcript)
        self.assertIn("nothing was written", transcript)
        self.assertIn("No nearby Token was discovered or substituted", transcript)
        self.assertIn("Technical detail: no Token path was provided", transcript)
        paths = paths_for_nexus(self.nexus)
        self.assertFalse(paths.activation.exists())
        self.assertFalse(paths.selected_context.exists())
        self.assertFalse(paths.selected_token.exists())

    def test_failed_token_then_explicit_normal_activation(self) -> None:
        invalid = self.root / "invalid-token.json"
        invalid.write_text("not json", encoding="utf-8")
        answers = iter(("2", str(invalid), "1"))
        output: list[str] = []
        result = run_recipient_activation(
            nexus_root=self.nexus,
            input_reader=lambda _prompt: next(answers),
            output_writer=output.append,
            **RECIPIENT,
        )
        self.assertEqual(result, ActivationChoiceResult.FIRST_SPARK)
        transcript = "\n".join(output)
        self.assertLess(
            transcript.index("selected carried trace could not safely be opened"),
            transcript.index("Token activation failed"),
        )
        self.assertIn("Token activation failed", transcript)
        self.assertIn("No nearby Token was discovered or substituted", transcript)
        self.assertIn("Choose again", transcript)
        self.assertEqual(
            load_activation(paths_for_nexus(self.nexus).activation).profile_id,
            "first-spark",
        )

    def test_overwrite_refusal_preserves_existing_activation(self) -> None:
        self.normal()
        path = paths_for_nexus(self.nexus).activation
        original = path.read_bytes()
        with self.assertRaisesRegex(RecipientActivationError, "overwrite"):
            self.token_activation()
        self.assertEqual(path.read_bytes(), original)

    def test_unicode_recipient_data_round_trips(self) -> None:
        self.normal()
        activation = load_activation(paths_for_nexus(self.nexus).activation)
        self.assertEqual(activation.recipient_alias, "Mélanie")
        self.assertEqual(activation.activation_purpose, "Geschenk")
        self.assertEqual(activation.private_message, "Für dich — später.")

    def test_selected_context_survives_moving_nexus_folder(self) -> None:
        self.token_activation()
        moved = self.root / "moved-nexus"
        self.nexus.rename(moved)
        self.assertEqual(
            classify_runtime_interpretation(nexus_root=moved),
            ResonanceRuntimeInterpretation.ANSWER,
        )

    def test_forged_legacy_activation_without_context_is_blocked(self) -> None:
        path = paths_for_nexus(self.nexus).activation
        path.write_text(
            json.dumps(
                {
                    "profile_id": "return-resonance",
                    "recipient_alias": "recipient",
                    "activation_purpose": "legacy",
                    "private_message": "legacy",
                }
            ),
            encoding="utf-8",
        )
        self.assertEqual(
            classify_runtime_interpretation(nexus_root=self.nexus),
            ResonanceRuntimeInterpretation.BLOCKED_ANSWER_RECOVERY,
        )

    def test_tampered_selected_token_is_blocked(self) -> None:
        self.token_activation()
        paths_for_nexus(self.nexus).selected_token.write_bytes(valid_token_bytes() + b" ")
        self.assertEqual(
            classify_runtime_interpretation(nexus_root=self.nexus),
            ResonanceRuntimeInterpretation.BLOCKED_ANSWER_RECOVERY,
        )

    def test_publication_failure_rolls_back_all_new_files(self) -> None:
        real_publish = controller._publish_exclusive
        calls = 0

        def fail_context(staged: Path, final: Path) -> None:
            nonlocal calls
            calls += 1
            if calls == 2:
                raise RecipientActivationError("injected publication failure")
            real_publish(staged, final)

        with patch(
            "recipient_activation._publish_exclusive", side_effect=fail_context
        ):
            with self.assertRaisesRegex(RecipientActivationError, "publication failure"):
                self.token_activation()
        paths = paths_for_nexus(self.nexus)
        self.assertFalse(paths.activation.exists())
        self.assertFalse(paths.selected_context.exists())
        self.assertFalse(paths.selected_token.exists())


if __name__ == "__main__":
    unittest.main()
