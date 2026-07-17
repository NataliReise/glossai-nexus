from __future__ import annotations

import json
from pathlib import Path
import sys
import tempfile
import unittest


NEXUS_ROOT = Path(__file__).resolve().parents[2]
PACKAGING_ROOT = NEXUS_ROOT / "packaging"
FIRST_SPARK_ROOT = NEXUS_ROOT / "first_spark"
for import_root in (NEXUS_ROOT, PACKAGING_ROOT, FIRST_SPARK_ROOT):
    if str(import_root) not in sys.path:
        sys.path.insert(0, str(import_root))

from first_spark.activation import load_activation  # noqa: E402
from prepare_nexus_gift import (  # noqa: E402
    PreparationError,
    RouteIdentity,
    prepare_first_spark,
    prepare_resonance,
)
from return_resonance.resonance_render_bridge import (  # noqa: E402
    ChamberSelections,
    build_resonance_return_artifact,
)
from return_resonance.slots import load_return_slots  # noqa: E402
from return_resonance.token import load_resonance_token  # noqa: E402
from verify_first_spark_gift_package import verify_package as verify_first_spark  # noqa: E402
from verify_resonance_gift_package import verify_preparation  # noqa: E402


FIXED_ROUTE = RouteIdentity(
    module_id="N01",
    layer_id="return-resonance-1",
    origin_trace_id="n01-origin-0123456789abcdef",
    return_slot_id="n01-slot-0123456789abcdef",
    package_id="n01-package-0123456789abcdef",
)


class PrepareNexusGiftTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        self.dist = self.root / "dist"
        self.private = self.root / "private"

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_generated_first_spark_delegates_to_existing_builder(self) -> None:
        result = prepare_first_spark(
            gift_label="normal",
            dist_root=self.dist,
            activation_path=None,
            recipient_alias="Áda",
            activation_purpose="gift",
            private_message="Für dich",
            zip_package=True,
        )

        self.assertTrue((result.gift_path / "run_first_spark.py").is_file())
        self.assertFalse((result.gift_path / "run_nexus.py").exists())
        activation = load_activation(result.gift_path / "activation.local.json")
        self.assertEqual(activation.profile_id, "first-spark")
        self.assertEqual(activation.recipient_alias, "Áda")
        self.assertTrue(verify_first_spark(result.gift_path).passed)
        self.assertTrue(result.zip_path and result.zip_path.is_file())

    def test_existing_wrong_profile_is_rejected_before_publication(self) -> None:
        activation_path = self.root / "wrong.json"
        activation_path.write_text(
            json.dumps({"profile_id": "return-resonance"}), encoding="utf-8"
        )

        with self.assertRaises(PreparationError):
            prepare_first_spark(
                gift_label="wrong",
                dist_root=self.dist,
                activation_path=activation_path,
                recipient_alias="unused",
                activation_purpose="unused",
                private_message="unused",
                zip_package=False,
            )
        self.assertFalse(self.dist.exists())

    def test_first_spark_verifier_rejects_resonance_activation(self) -> None:
        result = prepare_first_spark(
            gift_label="verify-profile",
            dist_root=self.dist,
            activation_path=None,
            recipient_alias="recipient",
            activation_purpose="gift",
            private_message="private",
            zip_package=False,
        )
        activation_path = result.gift_path / "activation.local.json"
        activation_path.write_text(
            json.dumps({"profile_id": "return-resonance"}), encoding="utf-8"
        )

        verification = verify_first_spark(result.gift_path)
        self.assertFalse(verification.passed)
        self.assertTrue(any("must use the 'first-spark' profile" in error for error in verification.errors))

    def test_resonance_outputs_are_matched_and_separated(self) -> None:
        result = self._prepare_resonance(zip_package=True)

        token_path = result.gift_path / "resonance_token.local.json"
        token = load_resonance_token(token_path)
        slot = load_return_slots(result.private_slot_path)[0]
        for field_name in (
            "module_id", "layer_id", "origin_trace_id", "return_slot_id", "package_id"
        ):
            self.assertEqual(getattr(token, field_name), getattr(slot, field_name))

        self.assertEqual(
            load_activation(result.gift_path / "first_spark/activation.local.json").profile_id,
            "return-resonance",
        )
        self.assertTrue(token.enables_resonance)
        self.assertFalse((result.gift_path / "return_slots.local.json").exists())
        self.assertFalse((result.gift_path / "return_slot.local.json").exists())
        self.assertFalse(any("tests" in path.parts for path in result.gift_path.rglob("*")))
        self.assertTrue(verify_preparation(result.gift_path, result.private_slot_path).passed)
        self.assertTrue(result.zip_path and result.zip_path.is_file())

    def test_generated_token_supplies_later_artifact_route(self) -> None:
        result = self._prepare_resonance()
        token = load_resonance_token(result.gift_path / "resonance_token.local.json")
        artifact = build_resonance_return_artifact(
            token,
            ChamberSelections(
                image_id="threshold",
                image_response_id="step_closer",
                scent_id="rain",
                scent_response_id="memory",
                movement_id="turning",
                movement_response_id="slowly",
                wish_word="Nähe",
                return_word="Heimkehr",
            ),
        )
        for field_name in (
            "module_id", "layer_id", "origin_trace_id", "return_slot_id", "package_id"
        ):
            self.assertEqual(getattr(artifact, field_name), getattr(token, field_name))

    def test_result_file_rejects_absolute_and_parent_paths(self) -> None:
        for unsafe in ("../result.local.md", "/tmp/result.local.md", "folder/result.local.md"):
            with self.subTest(unsafe=unsafe), self.assertRaises(PreparationError):
                self._prepare_resonance(result_file=unsafe)

    def test_template_sentinel_is_rejected(self) -> None:
        with self.assertRaises(PreparationError):
            self._prepare_resonance(public_safe_label="CHANGE-ME")

    def test_existing_output_is_never_overwritten(self) -> None:
        first = self._prepare_resonance()
        marker = first.gift_path / "marker.txt"
        marker.write_text("keep", encoding="utf-8")

        with self.assertRaises(PreparationError):
            self._prepare_resonance()
        self.assertEqual(marker.read_text(encoding="utf-8"), "keep")

    def _prepare_resonance(
        self,
        *,
        zip_package: bool = False,
        result_file: str | None = None,
        public_safe_label: str = "quiet route",
    ):
        return prepare_resonance(
            gift_label="resonant",
            dist_root=self.dist,
            private_root=self.private,
            recipient_alias="Zoë",
            activation_purpose="gift",
            private_message="Bleibt lokal",
            public_safe_label=public_safe_label,
            result_file=result_file,
            zip_package=zip_package,
            route=FIXED_ROUTE,
        )


if __name__ == "__main__":
    unittest.main()
