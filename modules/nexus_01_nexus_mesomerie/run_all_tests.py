#!/usr/bin/env python3
"""Run the complete Nexus 01 production and integration test suite."""

from __future__ import annotations

import hashlib
import importlib.util
import inspect
from pathlib import Path
import sys
import tempfile
import types
import unittest


sys.dont_write_bytecode = True


NEXUS_ROOT = Path(__file__).resolve().parent
TEST_ROOTS = (
    "atrium/tests",
    "chambers/resonance/tests",
    "first_spark/tests",
    "packaging/tests",
    "resonance_language_library/tests",
    "return_resonance/tests",
    "tests",
)
SCRIPT_CHECKS = {"return_resonance/tests/test_resonance_return_demo.py"}
REQUIRED_TEST_FILES = {
    "atrium/tests/test_classified_resonance.py",
    "return_resonance/tests/test_resonance_token_v2.py",
    "return_resonance/tests/test_artifact_store.py",
}


class TestCollectionError(RuntimeError):
    """Raised when the required production suite cannot be collected safely."""


def discover_test_files(root: Path = NEXUS_ROOT) -> tuple[Path, ...]:
    """Return every production test file from the explicit Nexus 01 roots."""
    files: list[Path] = []
    for relative_root in TEST_ROOTS:
        test_root = root / relative_root
        if not test_root.is_dir():
            raise TestCollectionError(f"Required test group is missing: {relative_root}")
        group_files = sorted(test_root.glob("test_*.py"))
        if not group_files:
            raise TestCollectionError(f"Required test group is empty: {relative_root}")
        files.extend(group_files)

    relative_files = {path.relative_to(root).as_posix() for path in files}
    missing = sorted(REQUIRED_TEST_FILES - relative_files)
    if missing:
        raise TestCollectionError(
            "Required safety test files were not collected: " + ", ".join(missing)
        )
    return tuple(files)


def _load_test_module(path: Path) -> types.ModuleType:
    digest = hashlib.sha256(str(path).encode("utf-8")).hexdigest()[:12]
    module_name = f"nexus_01_test_{path.stem}_{digest}"
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise TestCollectionError(f"Could not load test file: {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def _run_function(function: object) -> None:
    signature = inspect.signature(function)
    parameters = tuple(signature.parameters)
    if not parameters:
        function()  # type: ignore[operator]
        return
    if parameters == ("tmp_path",):
        with tempfile.TemporaryDirectory(prefix="nexus-01-test-") as temporary:
            function(Path(temporary))  # type: ignore[operator]
        return
    raise TestCollectionError(
        f"Unsupported test parameters for {function.__module__}.{function.__name__}: "
        + ", ".join(parameters)
    )


def _function_test_case(function: object) -> unittest.FunctionTestCase:
    return unittest.FunctionTestCase(
        lambda: _run_function(function),
        description=f"{function.__module__}.{function.__name__}",
    )


def _collect_file(path: Path, root: Path) -> unittest.TestSuite:
    module = _load_test_module(path)
    relative = path.relative_to(root).as_posix()
    if relative in SCRIPT_CHECKS:
        main = getattr(module, "main", None)
        if not callable(main):
            raise TestCollectionError(f"Required scripted check has no main(): {relative}")
        return unittest.TestSuite((_function_test_case(main),))

    suite = unittest.defaultTestLoader.loadTestsFromModule(module)
    for name, function in inspect.getmembers(module, inspect.isfunction):
        if name.startswith("test_") and function.__module__ == module.__name__:
            suite.addTest(_function_test_case(function))
    if suite.countTestCases() == 0:
        raise TestCollectionError(f"No tests were collected from: {relative}")
    return suite


def build_suite(root: Path = NEXUS_ROOT) -> tuple[unittest.TestSuite, int]:
    suite = unittest.TestSuite()
    files = discover_test_files(root)
    for path in files:
        relative = path.relative_to(root).as_posix()
        print(f"Collecting {relative}", flush=True)
        suite.addTest(_collect_file(path, root))
    return suite, len(files)


def main() -> int:
    try:
        suite, file_count = build_suite()
    except (TestCollectionError, OSError, ImportError) as error:
        print(f"Nexus 01 test collection failed: {error}", file=sys.stderr)
        return 2

    planned_count = suite.countTestCases()
    print(
        f"Running {planned_count} tests from {file_count} production test files.",
        flush=True,
    )
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    print(
        "Nexus 01 test summary: "
        f"files={file_count}, run={result.testsRun}, "
        f"failures={len(result.failures)}, errors={len(result.errors)}, "
        f"skipped={len(result.skipped)}",
        flush=True,
    )
    if result.testsRun != planned_count:
        print("Not every collected test was executed.", file=sys.stderr)
        return 1
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
