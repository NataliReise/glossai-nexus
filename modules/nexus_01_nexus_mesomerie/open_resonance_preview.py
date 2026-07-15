#!/usr/bin/env python3
"""Preview one Resonance Return locally without changing persistent state."""

from __future__ import annotations

from pathlib import Path
import sys

from return_resonance.local_opening import (
    LocalResonanceOpeningError,
    open_local_resonance_return,
)


def main(argv: list[str] | None = None) -> int:
    arguments = list(argv if argv is not None else sys.argv[1:])
    if len(arguments) not in {2, 3}:
        print(
            "Usage: python3 open_resonance_preview.py "
            "RETURN_ARTIFACT.json RETURN_SLOTS.json [LIBRARY_DIR]",
            file=sys.stderr,
        )
        return 2

    artifact_path = Path(arguments[0]).expanduser()
    slot_path = Path(arguments[1]).expanduser()
    library_dir = Path(arguments[2]).expanduser() if len(arguments) == 3 else None

    try:
        result = open_local_resonance_return(
            artifact_path=artifact_path,
            slot_path=slot_path,
            library_dir=library_dir,
        )
    except LocalResonanceOpeningError as error:
        print(f"Resonance preview could not open: {error}", file=sys.stderr)
        return 1

    print(result.opened.output.text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
