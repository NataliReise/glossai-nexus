"""Compatibility exports for the packageable Return Workspace builder."""

from __future__ import annotations

from resonance_invitation_runtime import (
    InvitationPublicationError,
    OPEN_RETURN_SCRIPT,
    WORKSPACE_README,
    WORKSPACE_RUNTIME_FILES,
    WORKSPACE_RUNTIME_SOURCE_FILES,
    WORKSPACE_SLOT_PATH,
    _build_return_workspace,
    workspace_name,
)


ReturnWorkspaceBuildError = InvitationPublicationError
RUNTIME_SOURCE_FILES = WORKSPACE_RUNTIME_SOURCE_FILES
RUNTIME_FILES = WORKSPACE_RUNTIME_FILES
SLOT_PATH = WORKSPACE_SLOT_PATH
build_return_workspace = _build_return_workspace

__all__ = [
    "OPEN_RETURN_SCRIPT",
    "RUNTIME_FILES",
    "RUNTIME_SOURCE_FILES",
    "ReturnWorkspaceBuildError",
    "SLOT_PATH",
    "WORKSPACE_README",
    "build_return_workspace",
    "workspace_name",
]
