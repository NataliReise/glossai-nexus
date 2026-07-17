#!/usr/bin/env python3
"""Independently verify a travelling Nexus 01 Resonance invitation."""

from __future__ import annotations

import argparse
from dataclasses import dataclass, field
from pathlib import Path
import sys


SCRIPT_PATH = Path(__file__).resolve()
NEXUS_ROOT = SCRIPT_PATH.parents[1]
if str(NEXUS_ROOT) not in sys.path:
    sys.path.insert(0, str(NEXUS_ROOT))

from return_resonance.token import (  # noqa: E402
    ResonanceToken,
    ResonanceTokenLoadError,
    load_resonance_token,
)


TOKEN_PATH = Path("resonance_token.local.json")
README_PATH = Path("README.md")
EXPECTED_FILES = frozenset({TOKEN_PATH, README_PATH})
FORBIDDEN_NAMES = frozenset(
    {
        "activation.local.json",
        "return_slots.local.json",
        "return_artifact.local.json",
    }
)
FORBIDDEN_PARTS = frozenset(
    {
        ".git",
        "__pycache__",
        "archive",
        "demos",
        "experiments",
        "packaging",
        "results",
        "tests",
    }
)


@dataclass
class InvitationVerificationResult:
    errors: list[str] = field(default_factory=list)
    token: ResonanceToken | None = None

    @property
    def passed(self) -> bool:
        return not self.errors

    def add_error(self, message: str) -> None:
        self.errors.append(message)


def verify_invitation(
    invitation_dir: Path,
    expected_identity: dict[str, str] | None = None,
) -> InvitationVerificationResult:
    """Verify strict contents and one inert Token V2."""

    result = InvitationVerificationResult()
    if not invitation_dir.is_dir():
        result.add_error(
            f"Resonance invitation does not exist or is not a directory: {invitation_dir}"
        )
        return result

    for path in (invitation_dir, *invitation_dir.rglob("*")):
        if path.is_symlink():
            result.add_error(
                "Symbolic links are not allowed in a Resonance invitation: "
                f"{path.relative_to(invitation_dir)}"
            )

    actual_entries = {
        path.relative_to(invitation_dir)
        for path in invitation_dir.rglob("*")
    }
    for missing in sorted(EXPECTED_FILES - actual_entries, key=str):
        result.add_error(f"Missing invitation file: {missing}")
    for unexpected in sorted(actual_entries - EXPECTED_FILES, key=str):
        result.add_error(f"Unexpected invitation entry: {unexpected}")

    for path in invitation_dir.rglob("*"):
        relative = path.relative_to(invitation_dir)
        folded_parts = {part.casefold() for part in relative.parts}
        if path.name in FORBIDDEN_NAMES:
            result.add_error(f"Forbidden activation, private, or result data: {relative}")
        if FORBIDDEN_PARTS.intersection(folded_parts):
            result.add_error(f"Forbidden development or result path: {relative}")
        if path.suffix.casefold() in {".pyc", ".pyo"}:
            result.add_error(f"Python cache file found: {relative}")

    readme = invitation_dir / README_PATH
    if readme.is_file():
        try:
            readme_text = readme.read_text(encoding="utf-8").casefold()
        except (OSError, UnicodeError) as error:
            result.add_error(f"Invitation README is not readable UTF-8: {error}")
        else:
            for phrase in (
                "optional invitation",
                "does not activate",
                "manual",
                "recipient chooses",
            ):
                if phrase not in readme_text:
                    result.add_error(f"Invitation README is missing guidance: {phrase}")

    token_path = invitation_dir / TOKEN_PATH
    try:
        token = load_resonance_token(token_path)
    except (ResonanceTokenLoadError, OSError, UnicodeError) as error:
        result.add_error(f"Travelling Resonance Token failed validation: {error}")
        return result
    result.token = token
    if token.is_legacy or not token.has_originating_contribution:
        result.add_error("Travelling invitation must contain a Resonance Token V2")
    if expected_identity is not None:
        for field_name, expected in expected_identity.items():
            if getattr(token, field_name, None) != expected:
                result.add_error(f"Travelling Token disagrees with expected {field_name}")
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Verify a travelling Nexus 01 Resonance invitation."
    )
    parser.add_argument("invitation_dir", type=Path)
    args = parser.parse_args(argv)
    result = verify_invitation(args.invitation_dir)
    if result.passed:
        print("Resonance invitation verification passed.")
        print(f"Invitation: {args.invitation_dir}")
        return 0
    print("Resonance invitation verification failed.")
    for error in result.errors:
        print(f"- {error}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
