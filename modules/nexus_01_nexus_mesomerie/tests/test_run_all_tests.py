from __future__ import annotations

from pathlib import Path
import sys
import tempfile
import unittest


NEXUS_ROOT = Path(__file__).resolve().parents[1]
if str(NEXUS_ROOT) not in sys.path:
    sys.path.insert(0, str(NEXUS_ROOT))

import run_all_tests


class CanonicalTestRunnerTests(unittest.TestCase):
    def test_discovery_includes_required_safety_groups_and_excludes_experiments(self) -> None:
        relative = {
            path.relative_to(NEXUS_ROOT).as_posix()
            for path in run_all_tests.discover_test_files()
        }
        self.assertTrue(run_all_tests.REQUIRED_TEST_FILES <= relative)
        self.assertFalse(any("experiments/" in path for path in relative))

    def test_tmp_path_function_is_run_with_temporary_directory(self) -> None:
        observed: list[Path] = []

        def test_example(tmp_path: Path) -> None:
            self.assertTrue(tmp_path.is_dir())
            observed.append(tmp_path)

        run_all_tests._run_function(test_example)
        self.assertEqual(len(observed), 1)
        self.assertFalse(observed[0].exists())

    def test_unknown_fixture_is_rejected(self) -> None:
        def test_example(monkeypatch: object) -> None:
            del monkeypatch

        with self.assertRaisesRegex(
            run_all_tests.TestCollectionError, "Unsupported test parameters"
        ):
            run_all_tests._run_function(test_example)

    def test_missing_required_group_fails_collection(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            with self.assertRaisesRegex(
                run_all_tests.TestCollectionError, "Required test group is missing"
            ):
                run_all_tests.discover_test_files(Path(temporary))


if __name__ == "__main__":
    unittest.main()
