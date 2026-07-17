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

from prepare_nexus_gift import RouteIdentity, prepare_resonance  # noqa: E402
from verify_resonance_gift_package import verify_package, verify_preparation  # noqa: E402


ROUTE = RouteIdentity(
    module_id="N01",
    layer_id="return-resonance-1",
    origin_trace_id="n01-origin-fedcba9876543210",
    return_slot_id="n01-slot-fedcba9876543210",
    package_id="n01-package-fedcba9876543210",
)


class VerifyResonanceGiftPackageTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        root = Path(self.temp_dir.name)
        self.result = prepare_resonance(
            gift_label="verify",
            dist_root=root / "dist",
            private_root=root / "private",
            recipient_alias="recipient",
            activation_purpose="gift",
            private_message="private",
            public_safe_label="verification route",
            result_file="return.local.md",
            zip_package=False,
            route=ROUTE,
        )

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_clean_package_and_private_slot_pass(self) -> None:
        result = verify_preparation(self.result.gift_path, self.result.private_slot_path)
        self.assertEqual(result.errors, [])

    def test_unexpected_development_file_fails_allowlist(self) -> None:
        extra = self.result.gift_path / "experiments" / "draft.py"
        extra.parent.mkdir()
        extra.write_text("draft", encoding="utf-8")

        result = verify_package(self.result.gift_path)
        self.assertFalse(result.passed)
        self.assertTrue(any("outside Resonance allowlist" in error for error in result.errors))

    def test_private_slot_inside_gift_fails(self) -> None:
        leaked_slot = self.result.gift_path / "return_slots.local.json"
        leaked_slot.write_text(
            self.result.private_slot_path.read_text(encoding="utf-8"), encoding="utf-8"
        )

        result = verify_package(self.result.gift_path)
        self.assertFalse(result.passed)
        self.assertTrue(any("return_slots.local.json" in error for error in result.errors))

    def test_mismatched_private_slot_fails_shared_identity(self) -> None:
        document = json.loads(self.result.private_slot_path.read_text(encoding="utf-8"))
        document["slots"][0]["package_id"] = "n01-package-other"
        self.result.private_slot_path.write_text(
            json.dumps(document, indent=2), encoding="utf-8"
        )

        result = verify_preparation(self.result.gift_path, self.result.private_slot_path)
        self.assertFalse(result.passed)
        self.assertTrue(any("disagree on package_id" in error for error in result.errors))

    def test_unsafe_result_filename_fails(self) -> None:
        document = json.loads(self.result.private_slot_path.read_text(encoding="utf-8"))
        document["slots"][0]["result_file"] = "../escape.local.md"
        self.result.private_slot_path.write_text(
            json.dumps(document, indent=2), encoding="utf-8"
        )

        result = verify_preparation(self.result.gift_path, self.result.private_slot_path)
        self.assertFalse(result.passed)
        self.assertTrue(any("plain safe relative filename" in error for error in result.errors))


if __name__ == "__main__":
    unittest.main()
