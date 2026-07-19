from __future__ import annotations

from dataclasses import FrozenInstanceError
import json
from pathlib import Path
import unittest
from unittest.mock import patch

from atrium.known_source import KnownSourceReadResult, KnownSourceReadStatus
from atrium.stable_result import (
    STABLE_RESULT_MAX_BYTES,
    StableResonanceView,
    StableResultReadResult,
    StableResultReadStatus,
    read_stable_resonance_result,
)


VISIBLE_LINES = (
    "Lantern-waiting path-appears.",
    "Summer rain, encounter opens.",
    "May kinship keep this passage open.",
    "Falling feather, feathers cross.",
    "homeward",
)
TRACE_SENTINEL = "TRACE-SENTINEL-MUST-STAY-HIDDEN"


def _canonical_document() -> str:
    trace = {
        "trace_format": "nexus-01-compact-result-trace-v1",
        "deterministic_seed": TRACE_SENTINEL,
    }
    return "\n".join(
        [
            "# Resonance Return",
            "",
            "## Compact Resonance",
            "",
            "```text",
            *VISIBLE_LINES,
            "```",
            "",
            "<!-- nexus-01-result-trace-start -->",
            "<details>",
            "<summary>Technical trace</summary>",
            "",
            "```json",
            json.dumps(trace, indent=2, ensure_ascii=False, sort_keys=True),
            "```",
            "",
            "</details>",
            "<!-- nexus-01-result-trace-end -->",
            "",
            "---",
            "",
            "This result remains local unless you deliberately transfer it.",
            "",
        ]
    )


class StableResultReaderTests(unittest.TestCase):
    def test_available_uses_boundary_limit_and_exposes_only_five_lines(self) -> None:
        source = Path("/tmp/nexus-stable-result.md")
        boundary = KnownSourceReadResult(
            KnownSourceReadStatus.AVAILABLE,
            _canonical_document().encode("utf-8"),
        )
        with patch(
            "atrium.stable_result.read_known_source_bytes",
            return_value=boundary,
        ) as reader:
            result = read_stable_resonance_result(source)

        reader.assert_called_once_with(source, max_bytes=STABLE_RESULT_MAX_BYTES)
        self.assertEqual(result.status, StableResultReadStatus.AVAILABLE)
        self.assertEqual(result.view, StableResonanceView(VISIBLE_LINES))
        self.assertNotIn(TRACE_SENTINEL, "\n".join(result.view.lines))

    def test_boundary_statuses_map_without_second_filesystem_check(self) -> None:
        expected = {
            KnownSourceReadStatus.MISSING: StableResultReadStatus.MISSING,
            KnownSourceReadStatus.SYMLINK: StableResultReadStatus.SYMLINK,
            KnownSourceReadStatus.NOT_REGULAR: StableResultReadStatus.NOT_REGULAR,
            KnownSourceReadStatus.UNAVAILABLE: StableResultReadStatus.UNAVAILABLE,
            KnownSourceReadStatus.TOO_LARGE: StableResultReadStatus.TOO_LARGE,
        }
        source = Path("/tmp/nexus-stable-result.md")
        for boundary_status, stable_status in expected.items():
            with self.subTest(status=boundary_status), patch(
                "atrium.stable_result.read_known_source_bytes",
                return_value=KnownSourceReadResult(boundary_status),
            ) as reader:
                result = read_stable_resonance_result(source)
            reader.assert_called_once_with(source, max_bytes=STABLE_RESULT_MAX_BYTES)
            self.assertEqual(result, StableResultReadResult(stable_status))

    def test_invalid_utf8_never_returns_a_partial_view(self) -> None:
        with patch(
            "atrium.stable_result.read_known_source_bytes",
            return_value=KnownSourceReadResult(
                KnownSourceReadStatus.AVAILABLE,
                b"\xff\xfe",
            ),
        ):
            result = read_stable_resonance_result(Path("/tmp/invalid.md"))
        self.assertEqual(result.status, StableResultReadStatus.INVALID_UTF8)
        self.assertIsNone(result.view)

    def test_noncanonical_documents_are_invalid_without_partial_view(self) -> None:
        canonical = _canonical_document()
        variants = {
            "missing visible line": canonical.replace(
                f"{VISIBLE_LINES[-1]}\n```", "```", 1
            ),
            "extra visible line": canonical.replace(
                f"{VISIBLE_LINES[-1]}\n```", f"{VISIBLE_LINES[-1]}\nextra\n```", 1
            ),
            "missing technical section": canonical.replace(
                "<!-- nexus-01-result-trace-start -->", "", 1
            ),
            "duplicate technical section": canonical.replace(
                "<!-- nexus-01-result-trace-start -->",
                "<!-- nexus-01-result-trace-start -->\n"
                "<!-- nexus-01-result-trace-start -->",
                1,
            ),
            "truncated JSON block": canonical.replace("```\n\n</details>", "</details>", 1),
            "unexpected suffix": canonical + "unexpected\n",
        }
        for label, document in variants.items():
            with self.subTest(label=label), patch(
                "atrium.stable_result.read_known_source_bytes",
                return_value=KnownSourceReadResult(
                    KnownSourceReadStatus.AVAILABLE,
                    document.encode("utf-8"),
                ),
            ):
                result = read_stable_resonance_result(Path("/tmp/invalid.md"))
            self.assertEqual(result.status, StableResultReadStatus.INVALID_FORMAT)
            self.assertIsNone(result.view)

    def test_invalid_json_trace_is_invalid_and_never_exposed(self) -> None:
        document = _canonical_document().replace(
            json.dumps(
                {
                    "trace_format": "nexus-01-compact-result-trace-v1",
                    "deterministic_seed": TRACE_SENTINEL,
                },
                indent=2,
                ensure_ascii=False,
                sort_keys=True,
            ),
            '{"deterministic_seed": "TRACE-SENTINEL-MUST-STAY-HIDDEN"',
        )
        with patch(
            "atrium.stable_result.read_known_source_bytes",
            return_value=KnownSourceReadResult(
                KnownSourceReadStatus.AVAILABLE,
                document.encode("utf-8"),
            ),
        ):
            result = read_stable_resonance_result(Path("/tmp/invalid.md"))
        self.assertEqual(result.status, StableResultReadStatus.INVALID_FORMAT)
        self.assertIsNone(result.view)

    def test_result_invariants_and_immutability(self) -> None:
        with self.assertRaises(ValueError):
            StableResultReadResult(StableResultReadStatus.AVAILABLE)
        with self.assertRaises(ValueError):
            StableResultReadResult(
                StableResultReadStatus.MISSING,
                StableResonanceView(VISIBLE_LINES),
            )
        with self.assertRaises(ValueError):
            StableResonanceView(("one", "two", "three", "four"))  # type: ignore[arg-type]
        result = StableResultReadResult(
            StableResultReadStatus.AVAILABLE,
            StableResonanceView(VISIBLE_LINES),
        )
        with self.assertRaises(FrozenInstanceError):
            result.view = None  # type: ignore[misc]


if __name__ == "__main__":
    unittest.main()
