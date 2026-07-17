#!/usr/bin/env python3
"""Prepare an inert Token V2 invitation and matching private workspace."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import hashlib
from pathlib import Path
import shutil
import sys
import tempfile


SCRIPT_PATH = Path(__file__).resolve()
NEXUS_ROOT = SCRIPT_PATH.parents[1]
for import_root in (SCRIPT_PATH.parent, NEXUS_ROOT):
    if str(import_root) not in sys.path:
        sys.path.insert(0, str(import_root))

from make_return_slot import build_slot_document  # noqa: E402
from prepare_nexus_gift import (  # noqa: E402
    PreparationError,
    SLOT_NOTE,
    _publish,
    _require_absent,
    _rollback_publication,
    validate_result_filename,
)
from return_workspace import (  # noqa: E402
    SLOT_PATH as WORKSPACE_SLOT_PATH,
    build_return_workspace,
    workspace_name,
)
from return_resonance.slots import load_return_slots  # noqa: E402
from return_resonance.token import (  # noqa: E402
    ResonanceToken,
    ResonanceTokenLoadError,
    load_resonance_token,
    parse_resonance_token,
)
from verify_resonance_invitation import (  # noqa: E402
    README_PATH,
    TOKEN_PATH,
    verify_invitation,
)
from verify_return_workspace import verify_workspace  # noqa: E402


INVITATION_README = """# Nexus 01 Resonance Invitation

This folder carries an **optional invitation** created in the shared Resonance
Chamber. It does not activate a Nexus merely by being present.

Pass this folder manually alongside a Nexus 01 module. The recipient chooses
whether to activate normally or deliberately accept this Token later. Nothing
is uploaded, sent, synchronized, consumed, or changed automatically.
"""


@dataclass(frozen=True)
class InvitationPreparationResult:
    invitation_path: Path
    private_workspace_path: Path
    private_slot_path: Path
    token: ResonanceToken


def invitation_name(return_slot_id: str) -> str:
    """Derive one public-safe folder name from the opaque route ID."""

    workspace = workspace_name(return_slot_id)
    return workspace.replace("n01-return-workspace-", "n01-resonance-invitation-", 1)


def prepare_resonance_invitation(
    token: ResonanceToken,
    *,
    invitation_root: Path,
    private_root: Path,
    result_file: str | None = None,
) -> InvitationPreparationResult:
    """Atomically publish one invitation and its separate private workspace."""

    try:
        validated_token = parse_resonance_token(token.to_dict())
    except (AttributeError, ResonanceTokenLoadError) as error:
        raise PreparationError(
            "Invitation preparation requires a validated Resonance Token V2."
        ) from error
    if validated_token.is_legacy or not validated_token.has_originating_contribution:
        raise PreparationError(
            "Invitation preparation requires a Resonance Token V2 with originating data."
        )

    invitation_root = invitation_root.expanduser().resolve()
    private_root = private_root.expanduser().resolve()
    final_invitation = invitation_root / invitation_name(validated_token.return_slot_id)
    final_workspace = private_root / workspace_name(validated_token.return_slot_id)
    final_slot = final_workspace / WORKSPACE_SLOT_PATH
    if final_workspace.is_relative_to(final_invitation) or final_invitation.is_relative_to(
        final_workspace
    ):
        raise PreparationError(
            "The private Return Workspace and travelling invitation must be separate paths."
        )
    _require_absent(final_invitation, final_workspace)

    result_target_key = hashlib.sha256(
        validated_token.return_slot_id.encode("ascii")
    ).hexdigest()[:24]
    result_file = validate_result_filename(
        result_file or f"return_resonance_{result_target_key}.local.md"
    )
    public_safe_label = validated_token.public_safe_label or "resonance invitation"
    slot_document = build_slot_document(
        origin_trace_id=validated_token.origin_trace_id,
        return_slot_id=validated_token.return_slot_id,
        package_id=validated_token.package_id,
        result_file=result_file,
        public_safe_label=public_safe_label,
        note=SLOT_NOTE,
        module_id=validated_token.module_id,
        layer_id=validated_token.layer_id,
    )
    identity = {
        name: getattr(validated_token, name)
        for name in (
            "module_id",
            "layer_id",
            "origin_trace_id",
            "return_slot_id",
            "package_id",
        )
    }

    invitation_root.parent.mkdir(parents=True, exist_ok=True)
    private_root.parent.mkdir(parents=True, exist_ok=True)
    invitation_stage_root = Path(
        tempfile.mkdtemp(
            prefix=".nexus-invitation-stage-", dir=invitation_root.parent
        )
    )
    workspace_stage_root = Path(
        tempfile.mkdtemp(
            prefix=".nexus-return-workspace-stage-", dir=private_root.parent
        )
    )
    published: list[Path] = []
    try:
        staged_invitation = invitation_stage_root / final_invitation.name
        staged_workspace = workspace_stage_root / final_workspace.name
        staged_invitation.mkdir()
        (staged_invitation / README_PATH).write_text(
            INVITATION_README.rstrip() + "\n", encoding="utf-8"
        )
        (staged_invitation / TOKEN_PATH).write_text(
            validated_token.to_json(), encoding="utf-8"
        )
        build_return_workspace(staged_workspace, slot_document)

        invitation_check = verify_invitation(staged_invitation, identity)
        if not invitation_check.passed:
            raise PreparationError(
                "Staged Resonance invitation failed verification: "
                + "; ".join(invitation_check.errors)
            )
        workspace_check = verify_workspace(staged_workspace, identity)
        if not workspace_check.passed:
            raise PreparationError(
                "Staged private Return Workspace failed verification: "
                + "; ".join(workspace_check.errors)
            )
        loaded_slot = load_return_slots(staged_workspace / WORKSPACE_SLOT_PATH)[0]
        for field_name, expected in identity.items():
            if getattr(loaded_slot, field_name) != expected:
                raise PreparationError(
                    f"Invitation and Return Slot disagree on {field_name}."
                )

        _publish(staged_invitation, final_invitation)
        published.append(final_invitation)
        _publish(staged_workspace, final_workspace)
        published.append(final_workspace)
        return InvitationPreparationResult(
            invitation_path=final_invitation,
            private_workspace_path=final_workspace,
            private_slot_path=final_slot,
            token=validated_token,
        )
    except Exception:
        _rollback_publication(*published)
        raise
    finally:
        shutil.rmtree(invitation_stage_root, ignore_errors=True)
        shutil.rmtree(workspace_stage_root, ignore_errors=True)


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
    except (OSError, ResonanceTokenLoadError, PreparationError) as error:
        print(f"Resonance invitation preparation failed: {error}", file=sys.stderr)
        return 1
    print(f"Travelling Resonance invitation: {result.invitation_path}")
    print(f"Private Return Workspace: {result.private_workspace_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
