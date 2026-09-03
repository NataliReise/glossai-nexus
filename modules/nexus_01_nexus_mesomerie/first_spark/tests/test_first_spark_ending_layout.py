"""Focused layout checks for the First Spark ending."""

from __future__ import annotations

from pathlib import Path
import sys


FIRST_SPARK_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(FIRST_SPARK_ROOT))

from first_spark.game_modules.ending import (  # noqa: E402
    ACTIVATION_MESSAGE,
    AFTER_PLAY_MESSAGE,
    PERSONAL_DIVIDER,
    TECHNICAL_SECTION_DIVIDER,
    build_ending_text,
)


def assert_private_ending_layout(response: str) -> None:
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


def assert_neutral_ending_layout(response: str) -> None:
    """Keep the public First Spark ending free of private-message content."""
    assert AFTER_PLAY_MESSAGE.strip() in response
    assert ACTIVATION_MESSAGE.strip() not in response
    assert "[activation message]" not in response
    assert PERSONAL_DIVIDER not in response
    assert response.count(TECHNICAL_SECTION_DIVIDER) == 3


def test_first_open_ends_with_personal_message() -> None:
    """The first opening should leave the gift message in the final viewport."""
    response = build_ending_text("The private message opens.", True)
    assert_private_ending_layout(response)


def test_repeated_open_ends_with_personal_message() -> None:
    """Repeated viewing should preserve the same calm ending hierarchy."""
    response = build_ending_text("The private message is already open.", True)
    assert_private_ending_layout(response)


def test_neutral_first_open_hides_activation_message() -> None:
    """A public fallback run should not reveal an activation-message block."""
    response = build_ending_text("The private message opens.", False)
    assert_neutral_ending_layout(response)


def test_neutral_repeated_open_hides_activation_message() -> None:
    """Repeated viewing should remain neutral without private activation."""
    response = build_ending_text("The private message is already open.", False)
    assert_neutral_ending_layout(response)


if __name__ == "__main__":
    test_first_open_ends_with_personal_message()
    test_repeated_open_ends_with_personal_message()
    test_neutral_first_open_hides_activation_message()
    test_neutral_repeated_open_hides_activation_message()
    print("First Spark ending layout tests passed.")
