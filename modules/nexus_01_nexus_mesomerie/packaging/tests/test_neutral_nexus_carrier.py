from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch


NEXUS_ROOT = Path(__file__).resolve().parents[2]
PACKAGING_ROOT = NEXUS_ROOT / "packaging"
for import_root in (NEXUS_ROOT, PACKAGING_ROOT):
    if str(import_root) not in sys.path:
        sys.path.insert(0, str(import_root))

from chambers.resonance import (  # noqa: E402
    OriginatingResonanceContribution,
    build_resonance_token_v2,
)
from return_resonance.slots import load_return_slots  # noqa: E402
from return_resonance.token import load_resonance_token  # noqa: E402
from prepare_neutral_nexus_carrier import (  # noqa: E402
    NeutralCarrierError,
    carrier_name,
    prepare_neutral_nexus_carrier,
)
from verify_neutral_nexus_carrier import (  # noqa: E402
    NEUTRAL_RUNTIME_FILES,
    SIDECAR_PATH,
    verify_carrier,
    verify_carrier_zip,
)


ROUTE = {
    "module_id": "N01",
    "layer_id": "return-resonance-1",
    "origin_trace_id": "n01-origin-carrier-test",
    "return_slot_id": "n01-slot-carrier-test",
    "package_id": "n01-package-carrier-test",
}

FIRST_SPARK_COMPLETION_COMMANDS = (
    "/first-spark",
    "/read welcome.log",
    "/read spark.note",
    "/link spark",
    "/unlock",
    "/quit",
)


class NeutralNexusCarrierTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.output = self.root / "dist"
        self.token = self.root / "invitation-source.json"
        token = build_resonance_token_v2(
            OriginatingResonanceContribution(
                "waiting-lantern", "summer-rain", "falling-feather", "Nähe"
            ),
            **ROUTE,
        )
        self.token.write_text(token.to_json(), encoding="utf-8")

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def build(self, *, with_token: bool = False, zip_package: bool = False):
        return prepare_neutral_nexus_carrier(
            output_dir=self.output,
            carrier_label="Sunday Carrier",
            token_path=self.token if with_token else None,
            zip_package=zip_package,
        )

    def start(self, carrier: Path, answers: str) -> subprocess.CompletedProcess[str]:
        environment = os.environ.copy()
        environment["PYTHONDONTWRITEBYTECODE"] = "1"
        return subprocess.run(
            [str(carrier / "START_HERE.sh")],
            cwd=self.root,
            env=environment,
            input=answers,
            capture_output=True,
            text=True,
        )

    def test_carrier_without_token_has_exact_neutral_boundary(self) -> None:
        result = self.build()
        self.assertTrue(verify_carrier(result.carrier_path).passed)
        self.assertIsNone(result.sidecar_path)
        self.assertFalse((result.carrier_path / SIDECAR_PATH).exists())
        for forbidden in (
            "first_spark/activation.local.json",
            "first_spark/activation.local.resonance-context.json",
            "first_spark/resonance_token.local.json",
            "return_slots.local.json",
            "return_artifact.local.json",
            "return_result.local.md",
        ):
            self.assertFalse((result.carrier_path / forbidden).exists())
        self.assertTrue(
            all((result.carrier_path / path).is_file() for path in NEUTRAL_RUNTIME_FILES)
        )
        launcher = (result.carrier_path / "START_HERE.sh").read_text(encoding="utf-8")
        self.assertNotIn("--legacy-preactivated", launcher)

    def test_known_source_runtime_is_byte_identical_and_imports_in_isolation(self) -> None:
        relative = Path("atrium/known_source.py")
        self.assertIn(relative, NEUTRAL_RUNTIME_FILES)
        self.assertEqual(sum(path == relative for path in NEUTRAL_RUNTIME_FILES), 1)

        result = self.build()
        source = NEXUS_ROOT / relative
        carried = result.carrier_path / relative
        self.assertTrue(carried.is_file())
        self.assertEqual(carried.read_bytes(), source.read_bytes())

        environment = os.environ.copy()
        environment.pop("PYTHONPATH", None)
        environment["PYTHONDONTWRITEBYTECODE"] = "1"
        imported = subprocess.run(
            [
                sys.executable,
                "-I",
                "-B",
                "-c",
                (
                    "import pathlib, sys; "
                    "sys.path.insert(0, '.'); "
                    "import atrium.known_source as module; "
                    "from atrium.known_source import ("
                    "KnownSourceReadResult, KnownSourceReadStatus, "
                    "read_known_source_bytes); "
                    "expected = (pathlib.Path.cwd() / 'atrium/known_source.py').resolve(); "
                    "actual = pathlib.Path(module.__file__).resolve(); "
                    "raise SystemExit(0 if actual == expected else 3)"
                ),
            ],
            cwd=result.carrier_path,
            env=environment,
            capture_output=True,
            text=True,
        )
        self.assertEqual(imported.returncode, 0, imported.stderr or imported.stdout)

    def test_carrier_with_token_preserves_bytes_without_activation(self) -> None:
        source_bytes = self.token.read_bytes()
        result = self.build(with_token=True)
        self.assertEqual(result.sidecar_path.read_bytes(), source_bytes)
        self.assertEqual(self.token.read_bytes(), source_bytes)
        self.assertTrue(
            verify_carrier(result.carrier_path, expected_token_source=self.token).passed
        )
        self.assertFalse(
            (result.carrier_path / "first_spark/activation.local.json").exists()
        )
        self.assertFalse(
            (
                result.carrier_path
                / "first_spark/activation.local.resonance-context.json"
            ).exists()
        )

    def test_invalid_and_v1_tokens_are_rejected(self) -> None:
        invalid = self.root / "invalid.json"
        invalid.write_text("not json", encoding="utf-8")
        legacy = self.root / "legacy.json"
        legacy.write_text(
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
        for token_path in (invalid, legacy):
            with self.subTest(token_path=token_path), self.assertRaises(
                NeutralCarrierError
            ):
                prepare_neutral_nexus_carrier(
                    output_dir=self.output,
                    carrier_label="invalid",
                    token_path=token_path,
                )
        self.assertFalse((self.output / carrier_name("invalid")).exists())

    def test_normal_first_start_is_compose_with_or_without_sidecar(self) -> None:
        for with_token in (False, True):
            with self.subTest(with_token=with_token):
                output = self.root / ("with-token" if with_token else "without-token")
                result = prepare_neutral_nexus_carrier(
                    output_dir=output,
                    carrier_label="normal",
                    token_path=self.token if with_token else None,
                )
                sidecar_before = (
                    (result.carrier_path / SIDECAR_PATH).read_bytes()
                    if with_token
                    else None
                )
                answers = "\n".join(("1", *FIRST_SPARK_COMPLETION_COMMANDS, "/quit", ""))
                run = self.start(result.carrier_path, answers)
                self.assertEqual(run.returncode, 0, run.stderr)
                self.assertIn("shape a resonance invitation", run.stdout)
                self.assertNotIn("answer the carried resonance", run.stdout)
                self.assertNotIn("Activation detected.", run.stdout)
                self.assertNotIn("First Spark online.", run.stdout)
                self.assertTrue(
                    (result.carrier_path / "first_spark/activation.local.json").is_file()
                )
                self.assertFalse(
                    (
                        result.carrier_path
                        / "first_spark/activation.local.resonance-context.json"
                    ).exists()
                )
                if with_token:
                    self.assertEqual(
                        (result.carrier_path / SIDECAR_PATH).read_bytes(), sidecar_before
                    )
                    self.assertFalse(
                        (
                            result.carrier_path
                            / "first_spark/resonance_token.local.json"
                        ).exists()
                    )

    def test_standalone_carrier_compose_publishes_invitation_and_workspace(self) -> None:
        result = self.build()
        travelling = self.root / "composed-travelling"
        retained = self.root / "composed-private"
        answers = "\n".join(
            (
                "1",
                *FIRST_SPARK_COMPLETION_COMMANDS,
                "/resonance",
                "/compose",
                "5",
                "4",
                "3",
                "Nähe",
                "yes",
                str(travelling),
                str(retained),
                "/quit",
                "",
            )
        )
        run = self.start(result.carrier_path, answers)
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertIn("Travelling Resonance invitation", run.stdout)
        self.assertIn("Private Return Workspace", run.stdout)
        invitations = [path for path in travelling.iterdir() if path.is_dir()]
        workspaces = [path for path in retained.iterdir() if path.is_dir()]
        self.assertEqual(len(invitations), 1)
        self.assertEqual(len(workspaces), 1)
        token = load_resonance_token(
            invitations[0] / "resonance_token.local.json"
        )
        slot = load_return_slots(
            workspaces[0] / "private/return_slots.local.json"
        )[0]
        for field_name in (
            "module_id",
            "layer_id",
            "origin_trace_id",
            "return_slot_id",
            "package_id",
        ):
            self.assertEqual(getattr(token, field_name), getattr(slot, field_name))
        self.assertTrue((workspaces[0] / "runtime/open_resonance_return.py").is_file())
        self.assertTrue(
            (workspaces[0] / "runtime/return_resonance/compact_generator.py").is_file()
        )
        self.assertFalse(
            any(
                path.name == "return_slots.local.json"
                for path in result.carrier_path.rglob("*")
            )
        )
        self.assertFalse(
            any(
                path.name == "return_artifact.local.json"
                for path in result.carrier_path.rglob("*")
            )
        )

    def test_explicit_sidecar_selection_is_answer_and_restarts_without_prompt(self) -> None:
        result = self.build(with_token=True)
        first = self.start(
            result.carrier_path,
            "2\ninvitation/resonance_token.v2.json\n/quit\n",
        )
        self.assertEqual(first.returncode, 0, first.stderr)
        self.assertIn("answer the carried resonance", first.stdout)
        self.assertTrue(
            (
                result.carrier_path
                / "first_spark/activation.local.resonance-context.json"
            ).is_file()
        )
        restart = self.start(result.carrier_path, "/quit\n")
        self.assertEqual(restart.returncode, 0, restart.stderr)
        self.assertNotIn("Choose how to activate", restart.stdout)
        self.assertIn("answer the carried resonance", restart.stdout)

    def test_cancellation_creates_no_local_activation(self) -> None:
        result = self.build(with_token=True)
        run = self.start(result.carrier_path, "q\n")
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertIn("Atrium was not opened", run.stdout)
        self.assertFalse(
            (result.carrier_path / "first_spark/activation.local.json").exists()
        )
        self.assertFalse(
            (
                result.carrier_path
                / "first_spark/activation.local.resonance-context.json"
            ).exists()
        )

    def test_unused_sidecar_can_be_removed_after_normal_activation(self) -> None:
        result = self.build(with_token=True)
        self.assertEqual(self.start(result.carrier_path, "1\n/quit\n").returncode, 0)
        (result.carrier_path / SIDECAR_PATH).unlink()
        restart = self.start(result.carrier_path, "/quit\n")
        self.assertEqual(restart.returncode, 0, restart.stderr)
        self.assertIn("first-spark: open", restart.stdout)
        self.assertNotIn("resonance", restart.stdout.lower())
        self.assertNotIn("Choose how to activate", restart.stdout)

    def test_carrier_remains_movable_before_and_after_activation(self) -> None:
        before = self.build(with_token=True)
        moved_before = self.root / "moved-before"
        before.carrier_path.rename(moved_before)
        self.assertEqual(self.start(moved_before, "1\n/quit\n").returncode, 0)

        second_output = self.root / "second-dist"
        after = prepare_neutral_nexus_carrier(
            output_dir=second_output,
            carrier_label="after",
            token_path=self.token,
        )
        self.assertEqual(
            self.start(
                after.carrier_path,
                "2\ninvitation/resonance_token.v2.json\n/quit\n",
            ).returncode,
            0,
        )
        moved_after = self.root / "moved-after"
        after.carrier_path.rename(moved_after)
        restart = self.start(moved_after, "/quit\n")
        self.assertEqual(restart.returncode, 0, restart.stderr)
        self.assertIn("answer the carried resonance", restart.stdout)

    def test_no_overwrite_and_staging_failure_publish_nothing(self) -> None:
        result = self.build()
        marker = result.carrier_path / "keep.txt"
        marker.write_text("keep", encoding="utf-8")
        with self.assertRaises(NeutralCarrierError):
            self.build()
        self.assertEqual(marker.read_text(encoding="utf-8"), "keep")

        failure_output = self.root / "failed-dist"
        with patch(
            "prepare_neutral_nexus_carrier._copy_runtime",
            side_effect=RuntimeError("injected staging failure"),
        ):
            with self.assertRaisesRegex(RuntimeError, "staging failure"):
                prepare_neutral_nexus_carrier(
                    output_dir=failure_output,
                    carrier_label="failed",
                    zip_package=True,
                )
        self.assertFalse((failure_output / carrier_name("failed")).exists())
        self.assertFalse((failure_output / carrier_name("failed")).with_suffix(".zip").exists())

    def test_directory_zip_and_tamper_verification(self) -> None:
        result = self.build(with_token=True, zip_package=True)
        self.assertTrue(verify_carrier(result.carrier_path, self.token).passed)
        self.assertTrue(result.zip_path and result.zip_path.is_file())
        self.assertTrue(verify_carrier_zip(result.zip_path, self.token).passed)
        (result.carrier_path / "first_spark/activation.local.json").write_text(
            '{"profile_id":"first-spark"}\n', encoding="utf-8"
        )
        verification = verify_carrier(result.carrier_path, self.token)
        self.assertFalse(verification.passed)
        self.assertTrue(any("activation.local.json" in error for error in verification.errors))


if __name__ == "__main__":
    unittest.main()
