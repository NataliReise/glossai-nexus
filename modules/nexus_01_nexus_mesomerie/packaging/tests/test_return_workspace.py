from __future__ import annotations

from dataclasses import asdict
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


NEXUS_ROOT = Path(__file__).resolve().parents[2]
PACKAGING_ROOT = NEXUS_ROOT / "packaging"
for import_root in (NEXUS_ROOT, PACKAGING_ROOT):
    if str(import_root) not in sys.path:
        sys.path.insert(0, str(import_root))

from prepare_nexus_gift import RouteIdentity, prepare_resonance  # noqa: E402
from return_resonance.resonance_render_bridge import (  # noqa: E402
    ChamberSelections,
    build_resonance_return_artifact,
)
from return_resonance.slots import load_return_slots  # noqa: E402
from return_resonance.token import load_resonance_token  # noqa: E402
from verify_return_workspace import verify_workspace  # noqa: E402


ROUTE = RouteIdentity(
    module_id="N01",
    layer_id="return-resonance-1",
    origin_trace_id="n01-origin-workspace01234567",
    return_slot_id="n01-slot-workspace01234567",
    package_id="n01-package-workspace01234567",
)


class ReturnWorkspaceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.result = prepare_resonance(
            gift_label="workspace",
            dist_root=self.root / "dist",
            private_root=self.root / "private",
            recipient_alias="Søren",
            activation_purpose="Geschenk",
            private_message="Nur für dich — локально",
            public_safe_label="leise Rückkehr",
            result_file="return.local.md",
            zip_package=True,
            route=ROUTE,
        )
        assert self.result.private_workspace_path is not None
        assert self.result.private_slot_path is not None
        self.workspace = self.result.private_workspace_path
        self.slot_path = self.result.private_slot_path

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def test_workspace_layout_identity_and_private_separation(self) -> None:
        self.assertEqual(
            {path.name for path in self.workspace.iterdir()},
            {"OPEN_RETURN.sh", "README.md", "incoming", "results", "private", "runtime"},
        )
        self.assertTrue(
            verify_workspace(
                self.workspace,
                asdict(ROUTE),
                gift_dir=self.result.gift_path,
            ).passed
        )
        slot = load_return_slots(self.slot_path)[0]
        token = load_resonance_token(
            self.result.gift_path / "resonance_token.local.json"
        )
        for field_name in asdict(ROUTE):
            self.assertEqual(getattr(slot, field_name), getattr(token, field_name))

        workspace_names = {path.name for path in self.workspace.rglob("*")}
        self.assertNotIn("activation.local.json", workspace_names)
        self.assertNotIn("resonance_token.local.json", workspace_names)
        gift_names = {path.name for path in self.result.gift_path.rglob("*")}
        self.assertNotIn("return_slots.local.json", gift_names)
        self.assertNotIn("OPEN_RETURN.sh", gift_names)

        activation = json.loads(
            (self.result.gift_path / "first_spark/activation.local.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertEqual(activation["recipient_alias"], "Søren")
        self.assertEqual(activation["private_message"], "Nur für dich — локально")
        self.assertEqual(slot.public_safe_label, "leise Rückkehr")

    def test_one_incoming_artifact_opens_then_reuses_exact_manual_edit(self) -> None:
        artifact = self._write_artifact(self.workspace / "incoming/returned.json")

        first = self._run_launcher(cwd=self.root)
        self.assertEqual(first.returncode, 0, first.stdout + first.stderr)
        result_path = self.workspace / "results/return.local.md"
        self.assertTrue(result_path.is_file())
        self.assertIn("Local result created: results/return.local.md", first.stdout)
        first_content = result_path.read_bytes()
        self.assertIn("Nähe".encode(), first_content)
        self.assertIn("帰還".encode(), first_content)

        edited_content = first_content + "\nGiver note: unchanged.\n".encode()
        result_path.write_bytes(edited_content)
        second = self._run_launcher(str(artifact), cwd=self.root / "dist")
        self.assertEqual(second.returncode, 0, second.stdout + second.stderr)
        self.assertIn("Local result reused: results/return.local.md", second.stdout)
        self.assertEqual(result_path.read_bytes(), edited_content)
        self.assertTrue(
            verify_workspace(
                self.workspace,
                asdict(ROUTE),
                gift_dir=self.result.gift_path,
            ).passed
        )

    def test_multiple_incoming_artifacts_refuse_ambiguous_selection(self) -> None:
        self._write_artifact(self.workspace / "incoming/first.json")
        self._write_artifact(self.workspace / "incoming/second.json")

        completed = self._run_launcher(cwd=self.root)

        self.assertNotEqual(completed.returncode, 0)
        self.assertIn("Multiple Return Artifact JSON files", completed.stderr)
        self.assertIn("Refusing ambiguous automatic selection", completed.stderr)
        self.assertFalse((self.workspace / "results/return.local.md").exists())

    def test_explicit_artifact_outside_incoming_works_from_other_cwd(self) -> None:
        artifact = self._write_artifact(self.root / "manually-received.json")

        completed = self._run_launcher(str(artifact), cwd=self.root / "dist")

        self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
        self.assertTrue((self.workspace / "results/return.local.md").is_file())
        self.assertTrue(artifact.is_file())

    def test_waiting_result_recovery_and_opened_missing_rejection(self) -> None:
        artifact = self._write_artifact(self.workspace / "incoming/return.json")
        first = self._run_launcher(str(artifact))
        self.assertEqual(first.returncode, 0, first.stdout + first.stderr)
        result_path = self.workspace / "results/return.local.md"
        original = result_path.read_bytes()

        slot_document = json.loads(self.slot_path.read_text(encoding="utf-8"))
        slot_document["slots"][0]["status"] = "waiting"
        self.slot_path.write_text(
            json.dumps(slot_document, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        repair = self._run_launcher(str(artifact))
        self.assertEqual(repair.returncode, 0, repair.stdout + repair.stderr)
        self.assertEqual(result_path.read_bytes(), original)
        self.assertEqual(load_return_slots(self.slot_path)[0].status.value, "opened")

        result_path.unlink()
        missing = self._run_launcher(str(artifact))
        self.assertEqual(missing.returncode, 2)
        self.assertIn("marked as opened", missing.stdout)
        self.assertIn("will not be regenerated", missing.stdout)

    def test_python_version_failure_is_clear(self) -> None:
        fake_python = self.root / "python-too-old"
        fake_python.write_text(
            "#!/usr/bin/env bash\n"
            "if [[ \"$*\" == *\"sys.version_info[:3]\"* ]]; then\n"
            "  echo 3.10.9\n"
            "  exit 0\n"
            "fi\n"
            "exit 1\n",
            encoding="utf-8",
        )
        fake_python.chmod(0o755)

        completed = self._run_launcher(
            cwd=self.root,
            extra_env={"NEXUS_PYTHON": str(fake_python)},
        )

        self.assertEqual(completed.returncode, 2)
        self.assertIn("Python 3.11 or newer is required", completed.stderr)
        self.assertIn("3.10.9", completed.stderr)

    def test_independent_verifier_accepts_valid_workspace_and_rejects_tampering(self) -> None:
        verifier = PACKAGING_ROOT / "verify_return_workspace.py"
        environment = os.environ.copy()
        environment["PYTHONDONTWRITEBYTECODE"] = "1"
        completed = subprocess.run(
            [
                sys.executable,
                str(verifier),
                str(self.workspace),
                "--gift",
                str(self.result.gift_path),
            ],
            cwd=self.root,
            env=environment,
            capture_output=True,
            text=True,
        )
        self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
        self.assertIn("verification passed", completed.stdout)

        (self.workspace / "activation.local.json").write_text(
            '{"profile_id": "return-resonance"}\n', encoding="utf-8"
        )
        tampered = verify_workspace(self.workspace, asdict(ROUTE))
        self.assertFalse(tampered.passed)
        self.assertTrue(
            any("Unexpected workspace root entry" in error for error in tampered.errors)
        )
        self.assertTrue(
            any("Forbidden travelling" in error for error in tampered.errors)
        )

        launcher = self.workspace / "OPEN_RETURN.sh"
        launcher.write_text(
            launcher.read_text(encoding="utf-8").replace(
                "--output-dir results", "--output-dir /tmp/results"
            ),
            encoding="utf-8",
        )
        slot_document = json.loads(self.slot_path.read_text(encoding="utf-8"))
        slot_document["slots"][0]["result_file"] = "../unsafe.md"
        self.slot_path.write_text(
            json.dumps(slot_document, indent=2) + "\n", encoding="utf-8"
        )
        deeply_tampered = verify_workspace(self.workspace, asdict(ROUTE))
        self.assertTrue(
            any("verified package-relative launcher" in error for error in deeply_tampered.errors)
        )
        self.assertTrue(
            any("plain safe relative filename" in error for error in deeply_tampered.errors)
        )

    def _write_artifact(self, path: Path) -> Path:
        path.parent.mkdir(parents=True, exist_ok=True)
        token = load_resonance_token(
            self.result.gift_path / "resonance_token.local.json"
        )
        artifact = build_resonance_return_artifact(
            token,
            ChamberSelections(
                image_id="waiting-lantern",
                image_response_id="appearing-path",
                scent_id="summer-rain",
                scent_response_id="possibility-of-encounter",
                movement_id="falling-feather",
                movement_response_id="crossing-feather",
                wish_word="Nähe",
                return_word="帰還",
            ),
        )
        path.write_text(artifact.to_json(), encoding="utf-8")
        return path

    def _run_launcher(
        self,
        *arguments: str,
        cwd: Path | None = None,
        extra_env: dict[str, str] | None = None,
    ) -> subprocess.CompletedProcess[str]:
        environment = os.environ.copy()
        environment["PYTHONDONTWRITEBYTECODE"] = "1"
        if extra_env:
            environment.update(extra_env)
        return subprocess.run(
            ["bash", str(self.workspace / "OPEN_RETURN.sh"), *arguments],
            cwd=cwd or self.root,
            env=environment,
            capture_output=True,
            text=True,
        )


if __name__ == "__main__":
    unittest.main()
