from __future__ import annotations

from dataclasses import FrozenInstanceError
import errno
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from atrium.known_source import (
    KnownSourceReadResult,
    KnownSourceReadStatus,
    read_known_source_bytes,
)


class KnownSourceBoundaryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def test_regular_file_returns_exact_raw_bytes_without_mutation(self) -> None:
        source = self.root / "source.bin"
        original = b"\x00resonance\xff\n"
        source.write_bytes(original)

        with patch.object(Path, "write_text") as write_text, patch.object(
            Path, "write_bytes"
        ) as write_bytes, patch.object(Path, "unlink") as unlink, patch.object(
            Path, "rename"
        ) as rename, patch.object(Path, "replace") as replace:
            result = read_known_source_bytes(source, max_bytes=len(original))

        self.assertEqual(result.status, KnownSourceReadStatus.AVAILABLE)
        self.assertEqual(result.content, original)
        self.assertEqual(source.read_bytes(), original)
        write_text.assert_not_called()
        write_bytes.assert_not_called()
        unlink.assert_not_called()
        rename.assert_not_called()
        replace.assert_not_called()

    def test_missing_path_is_calm_and_creates_nothing(self) -> None:
        source = self.root / "missing.bin"
        before = set(self.root.iterdir())

        with patch.object(Path, "glob") as glob, patch.object(Path, "rglob") as rglob:
            result = read_known_source_bytes(source, max_bytes=8)

        self.assertEqual(result, KnownSourceReadResult(KnownSourceReadStatus.MISSING))
        self.assertIsNone(result.content)
        self.assertEqual(set(self.root.iterdir()), before)
        glob.assert_not_called()
        rglob.assert_not_called()

    def test_symlink_is_rejected_without_reading_target(self) -> None:
        target = self.root / "target.bin"
        target.write_bytes(b"private target")
        source = self.root / "source-link"
        try:
            source.symlink_to(target)
        except (NotImplementedError, OSError) as error:
            self.skipTest(f"symlinks unavailable: {type(error).__name__}")

        with patch("atrium.known_source.os.read", wraps=os.read) as reader:
            result = read_known_source_bytes(source, max_bytes=64)

        self.assertEqual(result.status, KnownSourceReadStatus.SYMLINK)
        self.assertIsNone(result.content)
        reader.assert_not_called()

    def test_directory_is_not_regular_and_does_not_hang(self) -> None:
        result = read_known_source_bytes(self.root, max_bytes=8)

        self.assertEqual(result.status, KnownSourceReadStatus.NOT_REGULAR)
        self.assertIsNone(result.content)

    def test_open_failure_is_unavailable_without_error_or_path_leak(self) -> None:
        source = self.root / "private.bin"
        failure = PermissionError(errno.EACCES, "private path", str(source))

        with patch("atrium.known_source.os.open", side_effect=failure):
            result = read_known_source_bytes(source, max_bytes=8)

        self.assertEqual(result.status, KnownSourceReadStatus.UNAVAILABLE)
        self.assertIsNone(result.content)
        self.assertNotIn(str(source), repr(result))

    def test_byte_limit_accepts_exact_size_and_rejects_one_more(self) -> None:
        exact = self.root / "exact.bin"
        oversized = self.root / "oversized.bin"
        exact.write_bytes(b"1234")
        oversized.write_bytes(b"12345")

        exact_result = read_known_source_bytes(exact, max_bytes=4)
        with patch("atrium.known_source.os.read", wraps=os.read) as reader:
            oversized_result = read_known_source_bytes(oversized, max_bytes=4)

        self.assertEqual(exact_result.content, b"1234")
        self.assertEqual(exact_result.status, KnownSourceReadStatus.AVAILABLE)
        self.assertEqual(oversized_result.status, KnownSourceReadStatus.TOO_LARGE)
        self.assertIsNone(oversized_result.content)
        self.assertGreater(reader.call_count, 0)
        for call in reader.call_args_list:
            requested_bytes = call.args[1]
            self.assertGreater(requested_bytes, 0)
            self.assertLessEqual(requested_bytes, 5)

    def test_invalid_preconditions_do_not_open_any_path(self) -> None:
        with patch("atrium.known_source.os.open") as opener:
            with self.assertRaises(ValueError):
                read_known_source_bytes(Path("relative.bin"), max_bytes=1)
            with self.assertRaises(ValueError):
                read_known_source_bytes(self.root / "source.bin", max_bytes=0)
            with self.assertRaises(ValueError):
                read_known_source_bytes(self.root / "source.bin", max_bytes=-1)

        opener.assert_not_called()

    def test_lexical_path_is_passed_to_open_without_normalization(self) -> None:
        (self.root / "middle").mkdir()
        target = self.root / "source.bin"
        target.write_bytes(b"bytes")
        lexical = self.root / "middle" / ".." / "source.bin"

        with patch.object(Path, "resolve", side_effect=AssertionError), patch(
            "atrium.known_source.os.open", wraps=os.open
        ) as opener:
            result = read_known_source_bytes(lexical, max_bytes=5)

        self.assertEqual(result.content, b"bytes")
        self.assertEqual(opener.call_args.args[0], lexical)
        self.assertIn("..", str(opener.call_args.args[0]))

    def test_open_uses_only_safe_read_flags(self) -> None:
        source = self.root / "source.bin"
        source.write_bytes(b"safe")

        with patch("atrium.known_source.os.open", wraps=os.open) as opener:
            result = read_known_source_bytes(source, max_bytes=4)

        self.assertEqual(result.status, KnownSourceReadStatus.AVAILABLE)
        flags = opener.call_args.args[1]
        self.assertTrue(flags & os.O_CLOEXEC)
        self.assertTrue(flags & os.O_NOFOLLOW)
        self.assertTrue(flags & os.O_NONBLOCK)
        self.assertFalse(flags & (os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_TRUNC))

    def test_descriptor_closes_for_all_post_open_outcomes(self) -> None:
        regular = self.root / "regular.bin"
        oversized = self.root / "oversized.bin"
        regular.write_bytes(b"ok")
        oversized.write_bytes(b"toolarge")

        for source, limit, expected in (
            (regular, 2, KnownSourceReadStatus.AVAILABLE),
            (oversized, 2, KnownSourceReadStatus.TOO_LARGE),
            (self.root, 2, KnownSourceReadStatus.NOT_REGULAR),
        ):
            with self.subTest(status=expected):
                opened: list[int] = []
                real_open = os.open

                def tracked_open(*args):
                    descriptor = real_open(*args)
                    opened.append(descriptor)
                    return descriptor

                with patch("atrium.known_source.os.open", side_effect=tracked_open), patch(
                    "atrium.known_source.os.close", wraps=os.close
                ) as closer:
                    result = read_known_source_bytes(source, max_bytes=limit)
                self.assertEqual(result.status, expected)
                closer.assert_called_once_with(opened[0])

        opened = []
        real_open = os.open

        def tracked_open(*args):
            descriptor = real_open(*args)
            opened.append(descriptor)
            return descriptor

        with patch("atrium.known_source.os.open", side_effect=tracked_open), patch(
            "atrium.known_source.os.read", side_effect=OSError(errno.EIO, "read failed")
        ), patch("atrium.known_source.os.close", wraps=os.close) as closer:
            result = read_known_source_bytes(regular, max_bytes=2)
        self.assertEqual(result.status, KnownSourceReadStatus.UNAVAILABLE)
        closer.assert_called_once_with(opened[0])

    def test_result_invariants_and_immutability(self) -> None:
        with self.assertRaises(ValueError):
            KnownSourceReadResult(KnownSourceReadStatus.AVAILABLE)
        with self.assertRaises(ValueError):
            KnownSourceReadResult(KnownSourceReadStatus.MISSING, b"unexpected")

        result = KnownSourceReadResult(KnownSourceReadStatus.AVAILABLE, b"safe")
        with self.assertRaises(FrozenInstanceError):
            result.content = b"changed"


if __name__ == "__main__":
    unittest.main()
