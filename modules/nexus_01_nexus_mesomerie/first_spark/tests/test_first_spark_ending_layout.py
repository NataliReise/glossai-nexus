"""Focused layout checks for the First Spark ending."""

from __future__ import annotations

from pathlib import Path
import sys


FIRST_SPARK_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(FIRST_SPARK_ROOT))

from first_spark.game_modules.ending import (  # noqa: E402
    ACTIVATION_MESSAGE,
    AFTER_PLAY_MESSAGE,
    ALREADY_OPEN_TEXT,
    ENDING_TEXT,
    PERSONAL_DIVIDER,
    TECHNICAL_SECTION_DIVIDER,
)


def assert_ending_layout(response: str) -> None:
    """Keep orientation first and the personal activation message last."""
    after_play_start = response.index(AFTER_PLAY_MESSAGE.strip())
    personal_message_start = response.index(ACTIVATION_MESSAGE.strip())

    assert after_play_start < personal_message_start
    assert response.count(PERSONAL_DIVIDER) == 2
    assert response.count(TECHNICAL_SECTION_DIVIDER) == 3
    assert response.rstrip().endswith(PERSONAL_DIVIDER)

    opening_personal_divider = response.index(PERSONAL_DIVIDER)
    closing_personal_divider = response.rindex(PERSONAL_DIVIDER)
    assert opening_personal_divider < personal_message_start < closing_personal_divider


def test_first_open_ends_with_personal_message() -> None:
    """The first opening should leave the gift message in the final viewport."""
    assert_ending_layout(ENDING_TEXT)


def test_repeated_open_ends_with_personal_message() -> None:
    """Repeated viewing should preserve the same calm ending hierarchy."""
    assert_ending_layout(ALREADY_OPEN_TEXT)


if __name__ == "__main__":
    test_first_open_ends_with_personal_message()
    test_repeated_open_ends_with_personal_message()
    print("First Spark ending layout tests passed.")
