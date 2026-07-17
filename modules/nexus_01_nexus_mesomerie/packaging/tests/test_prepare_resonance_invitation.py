from __future__ import annotations

import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch


NEXUS_ROOT = Path(__file__).resolve().parents[2]
PACKAGING_ROOT = NEXUS_ROOT / "packaging"
for import_root in (NEXUS_ROOT, PACKAGING_ROOT):
    if str(import_root) not in sys.path:
        sys.path.insert(0, str(import_root))

from chambers.resonance.compose import (  # noqa: E402
    OriginatingResonanceContribution,
    build_resonance_token_v2,
)
import prepare_resonance_invitation as invitation_module  # noqa: E402
from prepare_nexus_gift import PreparationError  # noqa: E402
from prepare_resonance_invitation import (  # noqa: E402
    invitation_name,
    prepare_resonance_invitation,
)
from return_resonance.slots import load_return_slots  # noqa: E402
from return_resonance.token import parse_resonance_token  # noqa: E402
from return_workspace import SLOT_PATH, workspace_name  # noqa: E402
from verify_resonance_invitation import verify_invitation  # noqa: E402
from verify_return_workspace import verify_workspace  # noqa: E402


ROUTE = {
    "module_id": "N01",
    "layer_id": "return-resonance-1",
    "origin_trace_id": "n01-origin-invitation-test",
    "return_slot_id": "n01-slot-invitation-test",
    "package_id": "n01-package-invitation-test",
}


def token_v2():
    return build_resonance_token_v2(
        OriginatingResonanceContribution(
            "bridge-in-mist", "first-snow", "opening-circle", "Nähe"
        ),
        public_safe_label="Für später",
        **ROUTE,
    )


class InvitationPreparationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.invitation_root = self.root / "travelling"
        self.private_root = self.root / "private-retained"

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def prepare(self):
        return prepare_resonance_invitation(
            token_v2(),
            invitation_root=self.invitation_root,
            private_root=self.private_root,
        )

    def test_creation_preserves_route_and_strict_separation(self) -> None:
        result = self.prepare()
        self.assertEqual(
            {path.name for path in result.invitation_path.iterdir()},
            {"README.md", "resonance_token.local.json"},
        )
        invitation_names = {path.name for path in result.invitation_path.rglob("*")}
        workspace_names = {path.name for path in result.private_workspace_path.rglob("*")}
        self.assertNotIn("activation.local.json", invitation_names)
        self.assertNotIn("return_slots.local.json", invitation_names)
        self.assertNotIn("resonance_token.local.json", workspace_names)
        self.assertNotIn("activation.local.json", workspace_names)

        slot = load_return_slots(result.private_slot_path)[0]
        for field_name, expected in ROUTE.items():
            self.assertEqual(getattr(result.token, field_name), expected)
            self.assertEqual(getattr(slot, field_name), expected)
        self.assertTrue(verify_invitation(result.invitation_path, ROUTE).passed)
        self.assertTrue(verify_workspace(result.private_workspace_path, ROUTE).passed)

    def test_no_overwrite(self) -> None:
        first = self.prepare()
        marker = first.invitation_path / "marker.local"
        marker.write_text("preserve", encoding="utf-8")
        with self.assertRaises(PreparationError):
            self.prepare()
        self.assertEqual(marker.read_text(encoding="utf-8"), "preserve")

    def test_staging_failure_publishes_neither_output(self) -> None:
        with patch(
            "prepare_resonance_invitation.build_return_workspace",
            side_effect=RuntimeError("injected staging failure"),
        ):
            with self.assertRaisesRegex(RuntimeError, "injected staging failure"):
                self.prepare()
        self.assertFalse(
            (self.invitation_root / invitation_name(ROUTE["return_slot_id"])).exists()
        )
        self.assertFalse(
            (self.private_root / workspace_name(ROUTE["return_slot_id"])).exists()
        )

    def test_second_publication_failure_rolls_back_first_output(self) -> None:
        real_publish = invitation_module._publish
        calls = 0

        def fail_second_publication(staged: Path, final: Path) -> None:
            nonlocal calls
            calls += 1
            if calls == 2:
                raise RuntimeError("injected publication failure")
            real_publish(staged, final)

        with patch(
            "prepare_resonance_invitation._publish",
            side_effect=fail_second_publication,
        ):
            with self.assertRaisesRegex(RuntimeError, "publication failure"):
                self.prepare()
        self.assertFalse(
            (self.invitation_root / invitation_name(ROUTE["return_slot_id"])).exists()
        )
        self.assertFalse(
            (self.private_root / workspace_name(ROUTE["return_slot_id"])).exists()
        )

    def test_legacy_v1_token_is_explicitly_rejected(self) -> None:
        legacy = parse_resonance_token(
            {
                "token_version": "N01-RT-1",
                "token_type": "resonance-activation",
                **ROUTE,
                "enabled_chambers": ["resonance"],
            }
        )
        with self.assertRaisesRegex(PreparationError, "Token V2"):
            prepare_resonance_invitation(
                legacy,
                invitation_root=self.invitation_root,
                private_root=self.private_root,
            )

    def test_verifiers_reject_tampering(self) -> None:
        result = self.prepare()
        (result.invitation_path / "activation.local.json").write_text(
            json.dumps({"profile_id": "return-resonance"}), encoding="utf-8"
        )
        self.assertFalse(verify_invitation(result.invitation_path).passed)


if __name__ == "__main__":
    unittest.main()
