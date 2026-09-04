"""Small deterministic terminal-formatting helpers for Nexus 01 surfaces."""

from __future__ import annotations

from collections.abc import Callable
import textwrap


TextWriter = Callable[[str], None]
DEFAULT_TEXT_WIDTH = 76


def wrapped_text_lines(
    text: str,
    *,
    width: int = DEFAULT_TEXT_WIDTH,
    indent: str = "",
) -> tuple[str, ...]:
    """Wrap one semantic text line without breaking words or hyphenated tokens."""

    if width <= len(indent):
        raise ValueError("width must leave room for text after indentation")
    if not text:
        return (indent,)

    wrapper = textwrap.TextWrapper(
        width=width,
        initial_indent=indent,
        subsequent_indent=indent,
        break_long_words=False,
        break_on_hyphens=False,
        replace_whitespace=True,
        drop_whitespace=True,
    )
    lines = wrapper.wrap(text)
    return tuple(lines) if lines else (indent,)


def write_wrapped_text(
    output_writer: TextWriter,
    text: str,
    *,
    width: int = DEFAULT_TEXT_WIDTH,
    indent: str = "",
) -> None:
    """Write one semantic text line as deterministic word-boundary terminal lines."""

    for line in wrapped_text_lines(text, width=width, indent=indent):
        output_writer(line)
