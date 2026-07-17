#!/usr/bin/env python3
"""CLI compatibility wrapper for inert Resonance invitation publication."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys


SCRIPT_PATH = Path(__file__).resolve()
NEXUS_ROOT = SCRIPT_PATH.parents[1]
if str(NEXUS_ROOT) not in sys.path:
    sys.path.insert(0, str(NEXUS_ROOT))

from resonance_invitation_runtime import (  # noqa: E402
    InvitationPreparationResult,
    InvitationPublicationError,
    _build_return_workspace,
    _publish,
    invitation_name,
    prepare_resonance_invitation as _prepare_resonance_invitation,
)
from prepare_nexus_gift import PreparationError  # noqa: E402
from return_resonance.token import (  # noqa: E402
    ResonanceTokenLoadError,
    load_resonance_token,
)


# Compatibility names retained for existing callers and focused fault injection.
build_return_workspace = _build_return_workspace


def prepare_resonance_invitation(
    token,
    *,
    invitation_root: Path,
    private_root: Path,
    result_file: str | None = None,
) -> InvitationPreparationResult:
    """Retain the established packaging exception and fault-injection surface."""

    try:
        return _prepare_resonance_invitation(
            token,
            invitation_root=invitation_root,
            private_root=private_root,
            result_file=result_file,
            _workspace_builder=build_return_workspace,
            _publisher=_publish,
        )
    except InvitationPublicationError as error:
        raise PreparationError(str(error)) from error


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Prepare an inert Resonance Token V2 invitation and private workspace."
    )
    parser.add_argument("--token", type=Path, required=True)
    parser.add_argument("--invitation-root", type=Path, required=True)
    parser.add_argument("--private-root", type=Path, required=True)
    parser.add_argument("--result-file")
    args = parser.parse_args(argv)
    try:
        token = load_resonance_token(args.token)
        result = prepare_resonance_invitation(
            token,
            invitation_root=args.invitation_root,
            private_root=args.private_root,
            result_file=args.result_file,
        )
    except (
        OSError,
        ResonanceTokenLoadError,
        InvitationPublicationError,
        PreparationError,
    ) as error:
        print(f"Resonance invitation preparation failed: {error}", file=sys.stderr)
        return 1
    print(f"Travelling Resonance invitation: {result.invitation_path}")
    print(f"Private Return Workspace: {result.private_workspace_path}")
    return 0


__all__ = [
    "InvitationPreparationResult",
    "PreparationError",
    "build_return_workspace",
    "invitation_name",
    "prepare_resonance_invitation",
]


if __name__ == "__main__":
    raise SystemExit(main())
