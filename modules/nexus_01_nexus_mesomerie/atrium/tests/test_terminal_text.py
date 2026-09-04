from __future__ import annotations

from atrium.terminal_text import (
    DEFAULT_TEXT_WIDTH,
    wrapped_text_lines,
    write_wrapped_text,
)


def test_wrapped_text_uses_word_boundaries_and_shared_indentation() -> None:
    text = (
        "It may contain signs, rules, traces, and a path that becomes visible "
        "through exploration. The visitor may look closely, test possibilities, "
        "ask for orientation, pause, or leave."
    )

    lines = wrapped_text_lines(text, width=50, indent="  ")

    assert len(lines) > 1
    assert all(line.startswith("  ") for line in lines)
    assert all(len(line) <= 50 for line in lines)
    assert " ".join(line.strip() for line in lines) == text


def test_wrapped_text_never_breaks_long_words_or_hyphenated_identifiers() -> None:
    long_token = "resonance-as-a-gift-with-an-intentionally-long-identifier"
    text = f"Use {long_token} exactly."

    lines = wrapped_text_lines(text, width=24)

    assert long_token in lines
    assert any(len(line) > 24 for line in lines)
    assert "".join(lines).count(long_token) == 1


def test_write_wrapped_text_is_deterministic_at_default_width() -> None:
    output: list[str] = []
    text = (
        "A Nexus offers structure without claiming the encounter. It may "
        "remember only what it is asked to keep."
    )

    write_wrapped_text(output.append, text, indent="  ")

    assert output
    assert all(len(line) <= DEFAULT_TEXT_WIDTH for line in output)
    assert " ".join(line.strip() for line in output) == text
