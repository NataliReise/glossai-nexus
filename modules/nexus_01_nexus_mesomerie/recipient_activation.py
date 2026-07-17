#!/usr/bin/env python3
"""Recipient-controlled activation boundary for Nexus 01.

Token files are inert unless one explicit token path is passed to
``activate_with_resonance_token``.  This module does not discover tokens or
enter either Resonance Chamber mode.
"""

from __future__ import annotations

import argparse
from collections.abc import Callable
from dataclasses import asdict, dataclass
from enum import StrEnum
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import sys
import tempfile


SCRIPT_PATH = Path(__file__).resolve()
NEXUS_ROOT = SCRIPT_PATH.parent
FIRST_SPARK_ROOT = NEXUS_ROOT / "first_spark"
if str(FIRST_SPARK_ROOT) not in sys.path:
    sys.path.insert(0, str(FIRST_SPARK_ROOT))

from first_spark.activation import (  # noqa: E402
    FIRST_SPARK_PROFILE_ID,
    RETURN_RESONANCE_PROFILE_ID,
    Activation,
    ActivationFileError,
    activation_from_mapping,
    load_activation,
)
from return_resonance.token import (  # noqa: E402
    ResonanceToken,
    ResonanceTokenLoadError,
    parse_resonance_token,
)
from atrium.resonance_mode import ResonanceMode  # noqa: E402


# Compatibility name retained for callers of the first controller boundary.
ResonanceRuntimeInterpretation = ResonanceMode


ACTIVATION_FILENAME = "activation.local.json"
SELECTED_TOKEN_FILENAME = "resonance_token.local.json"
SELECTED_CONTEXT_FILENAME = "activation.local.resonance-context.json"
CONTEXT_VERSION = "N01-RAC-1"
ROUTE_FIELDS = (
    "module_id",
    "layer_id",
    "origin_trace_id",
    "return_slot_id",
    "package_id",
)
CONTEXT_FIELDS = frozenset(
    {
        "context_version",
        "selected_token_file",
        "selected_token_sha256",
        *ROUTE_FIELDS,
    }
)
SHA256_PATTERN = re.compile(r"[0-9a-f]{64}")


class RecipientActivationError(RuntimeError):
    """Raised when a completed activation cannot be published safely."""


class ActivationChoiceResult(StrEnum):
    FIRST_SPARK = "first-spark"
    RETURN_RESONANCE = "return-resonance"
    CANCELLED = "cancelled"


@dataclass(frozen=True)
class ActivationPaths:
    activation: Path
    selected_context: Path
    selected_token: Path


InputReader = Callable[[str], str]
OutputWriter = Callable[[str], None]


def paths_for_nexus(nexus_root: Path) -> ActivationPaths:
    """Return package-relative activation paths without inspecting their files."""

    activation_root = nexus_root.expanduser().resolve() / "first_spark"
    return ActivationPaths(
        activation=activation_root / ACTIVATION_FILENAME,
        selected_context=activation_root / SELECTED_CONTEXT_FILENAME,
        selected_token=activation_root / SELECTED_TOKEN_FILENAME,
    )


def activate_normally(
    *,
    nexus_root: Path,
    recipient_alias: str,
    activation_purpose: str,
    private_message: str,
) -> Activation:
    """Publish first-spark activation without discovering or reading any Token."""

    paths = paths_for_nexus(nexus_root)
    _require_activation_root(paths.activation.parent)
    _require_no_activation(paths.activation)
    activation = _validated_activation(
        FIRST_SPARK_PROFILE_ID,
        recipient_alias,
        activation_purpose,
        private_message,
    )
    _publish_activation_only(paths.activation, activation)
    return activation


def activate_with_resonance_token(
    token_path: Path,
    *,
    nexus_root: Path,
    recipient_alias: str,
    activation_purpose: str,
    private_message: str,
) -> Activation:
    """Validate one deliberately selected V2 Token, then publish answer state."""

    paths = paths_for_nexus(nexus_root)
    _require_activation_root(paths.activation.parent)
    _require_no_activation(paths.activation)
    if paths.selected_context.exists() or paths.selected_token.exists():
        raise RecipientActivationError(
            "A selected Resonance Token context already exists; refusing to replace it."
        )

    token_bytes, token = _read_selected_token(token_path)
    activation = _validated_activation(
        RETURN_RESONANCE_PROFILE_ID,
        recipient_alias,
        activation_purpose,
        private_message,
    )
    context = _context_for_token(token, token_bytes)
    _publish_resonance_activation(paths, activation, token_bytes, context)
    return activation


def classify_runtime_interpretation(
    *, nexus_root: Path
) -> ResonanceMode:
    """Classify completed activation state without changing any local file."""

    paths = paths_for_nexus(nexus_root)
    if not paths.activation.is_file():
        raise RecipientActivationError("No completed local activation exists.")
    try:
        activation = load_activation(paths.activation)
    except ActivationFileError as error:
        raise RecipientActivationError(str(error)) from error

    if activation.profile_id == FIRST_SPARK_PROFILE_ID:
        return ResonanceMode.COMPOSE
    if activation.profile_id != RETURN_RESONANCE_PROFILE_ID:
        raise RecipientActivationError(
            f"Unsupported completed activation profile: {activation.profile_id!r}."
        )

    try:
        _load_and_validate_selected_context(paths)
    except (OSError, UnicodeError, ValueError, ResonanceTokenLoadError):
        return ResonanceMode.BLOCKED_ANSWER_RECOVERY
    return ResonanceMode.ANSWER


def run_recipient_activation(
    *,
    nexus_root: Path,
    recipient_alias: str,
    activation_purpose: str,
    private_message: str,
    input_reader: InputReader = input,
    output_writer: OutputWriter = print,
) -> ActivationChoiceResult:
    """Run the explicit recipient choice loop with injectable terminal I/O."""

    while True:
        output_writer("")
        output_writer("Choose how to activate this Nexus 01")
        output_writer("1. Activate normally")
        output_writer("2. Activate with a Resonance Token")
        output_writer("q. Cancel without activating")
        choice = input_reader("Activation choice: ").strip().casefold()

        if choice in {"q", "quit", "cancel"}:
            output_writer("Activation cancelled. No activation state was created.")
            return ActivationChoiceResult.CANCELLED
        if choice == "1":
            try:
                activate_normally(
                    nexus_root=nexus_root,
                    recipient_alias=recipient_alias,
                    activation_purpose=activation_purpose,
                    private_message=private_message,
                )
            except RecipientActivationError as error:
                output_writer(f"Normal activation failed: {error}")
                continue
            output_writer("Nexus 01 activated normally with First Spark.")
            return ActivationChoiceResult.FIRST_SPARK
        if choice == "2":
            token_value = input_reader("Path to the Resonance Token V2: ").strip()
            if not token_value:
                output_writer("Token activation failed: no Token path was provided.")
                output_writer("No activation state was created. Choose again or cancel.")
                continue
            try:
                activate_with_resonance_token(
                    Path(token_value),
                    nexus_root=nexus_root,
                    recipient_alias=recipient_alias,
                    activation_purpose=activation_purpose,
                    private_message=private_message,
                )
            except (RecipientActivationError, ResonanceTokenLoadError) as error:
                output_writer(f"Token activation failed: {error}")
                output_writer("No activation state was created. Choose again or cancel.")
                continue
            output_writer(
                "Nexus 01 activated with the deliberately selected Resonance Token."
            )
            return ActivationChoiceResult.RETURN_RESONANCE

        output_writer("Please choose 1, 2, or q.")


def _read_selected_token(path: Path) -> tuple[bytes, ResonanceToken]:
    try:
        token_bytes = path.expanduser().read_bytes()
    except OSError as error:
        raise RecipientActivationError(
            f"Could not read the selected Resonance Token: {path}"
        ) from error
    try:
        decoded = token_bytes.decode("utf-8")
    except UnicodeError as error:
        raise RecipientActivationError(
            "The selected Resonance Token is not valid UTF-8."
        ) from error
    try:
        raw = json.loads(decoded)
    except json.JSONDecodeError as error:
        raise RecipientActivationError(
            f"The selected Resonance Token is not valid JSON: {error.msg}."
        ) from error
    try:
        token = parse_resonance_token(raw)
    except ResonanceTokenLoadError as error:
        raise RecipientActivationError(str(error)) from error
    if token.is_legacy or not token.has_originating_contribution:
        raise RecipientActivationError(
            "Resonance Token V1 cannot activate the corrected recipient-choice flow. "
            "Ask the originating person to create a Resonance Token V2 invitation."
        )
    return token_bytes, token


def _context_for_token(
    token: ResonanceToken, token_bytes: bytes
) -> dict[str, str]:
    return {
        "context_version": CONTEXT_VERSION,
        "selected_token_file": SELECTED_TOKEN_FILENAME,
        "selected_token_sha256": hashlib.sha256(token_bytes).hexdigest(),
        **{field_name: getattr(token, field_name) for field_name in ROUTE_FIELDS},
    }


def _load_and_validate_selected_context(paths: ActivationPaths) -> ResonanceToken:
    raw_context = json.loads(paths.selected_context.read_text(encoding="utf-8"))
    if not isinstance(raw_context, dict) or set(raw_context) != CONTEXT_FIELDS:
        raise ValueError("Selected Resonance context has an invalid shape.")
    if raw_context["context_version"] != CONTEXT_VERSION:
        raise ValueError("Selected Resonance context version is unsupported.")
    if raw_context["selected_token_file"] != SELECTED_TOKEN_FILENAME:
        raise ValueError("Selected Resonance Token reference is not package-relative.")
    digest = raw_context["selected_token_sha256"]
    if not isinstance(digest, str) or SHA256_PATTERN.fullmatch(digest) is None:
        raise ValueError("Selected Resonance Token digest is invalid.")
    token_bytes = paths.selected_token.read_bytes()
    if not hashlib.sha256(token_bytes).hexdigest() == digest:
        raise ValueError("Selected Resonance Token no longer matches its activation.")
    raw_token = json.loads(token_bytes.decode("utf-8"))
    token = parse_resonance_token(raw_token)
    if token.is_legacy or not token.has_originating_contribution:
        raise ValueError("Selected Resonance Token is not Token V2.")
    for field_name in ROUTE_FIELDS:
        value = raw_context[field_name]
        if not isinstance(value, str) or value != getattr(token, field_name):
            raise ValueError(
                f"Selected Resonance context disagrees on {field_name}."
            )
    return token


def _validated_activation(
    profile_id: str,
    recipient_alias: str,
    activation_purpose: str,
    private_message: str,
) -> Activation:
    try:
        return activation_from_mapping(
            {
                "profile_id": profile_id,
                "recipient_alias": recipient_alias,
                "activation_purpose": activation_purpose,
                "private_message": private_message,
            }
        )
    except ActivationFileError as error:
        raise RecipientActivationError(str(error)) from error


def _require_activation_root(path: Path) -> None:
    if not path.is_dir():
        raise RecipientActivationError(
            f"Nexus First Spark runtime directory was not found: {path}"
        )


def _require_no_activation(path: Path) -> None:
    if path.exists():
        raise RecipientActivationError(
            f"Refusing to overwrite existing local activation: {path}"
        )


def _activation_bytes(activation: Activation) -> bytes:
    return (
        json.dumps(asdict(activation), indent=2, ensure_ascii=False) + "\n"
    ).encode("utf-8")


def _publish_activation_only(path: Path, activation: Activation) -> None:
    stage_root = Path(
        tempfile.mkdtemp(prefix=".nexus-activation-stage-", dir=path.parent.parent)
    )
    try:
        staged = stage_root / ACTIVATION_FILENAME
        staged.write_bytes(_activation_bytes(activation))
        _publish_exclusive(staged, path)
    finally:
        shutil.rmtree(stage_root, ignore_errors=True)


def _publish_resonance_activation(
    paths: ActivationPaths,
    activation: Activation,
    token_bytes: bytes,
    context: dict[str, str],
) -> None:
    stage_root = Path(
        tempfile.mkdtemp(
            prefix=".nexus-token-activation-stage-",
            dir=paths.activation.parent.parent,
        )
    )
    published: list[Path] = []
    try:
        staged_token = stage_root / SELECTED_TOKEN_FILENAME
        staged_context = stage_root / SELECTED_CONTEXT_FILENAME
        staged_activation = stage_root / ACTIVATION_FILENAME
        staged_token.write_bytes(token_bytes)
        staged_context.write_text(
            json.dumps(context, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        staged_activation.write_bytes(_activation_bytes(activation))

        # activation.local.json is the completion marker and is published last.
        for staged, final in (
            (staged_token, paths.selected_token),
            (staged_context, paths.selected_context),
            (staged_activation, paths.activation),
        ):
            _publish_exclusive(staged, final)
            published.append(final)
    except Exception:
        for path in reversed(published):
            try:
                path.unlink()
            except FileNotFoundError:
                pass
        raise
    finally:
        shutil.rmtree(stage_root, ignore_errors=True)


def _publish_exclusive(staged: Path, final: Path) -> None:
    try:
        os.link(staged, final)
    except FileExistsError as error:
        raise RecipientActivationError(
            f"Refusing to overwrite existing local activation state: {final}"
        ) from error
    except OSError as error:
        raise RecipientActivationError(
            f"Could not publish local activation state: {final}"
        ) from error


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Choose normal or voluntary Resonance Token activation for Nexus 01."
    )
    parser.add_argument("--nexus-root", type=Path, default=NEXUS_ROOT)
    parser.add_argument("--recipient-alias", default="recipient_name")
    parser.add_argument("--activation-purpose", default="gift")
    parser.add_argument(
        "--private-message", default="A Nexus 01 gift is waiting for you."
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        run_recipient_activation(
            nexus_root=args.nexus_root,
            recipient_alias=args.recipient_alias,
            activation_purpose=args.activation_purpose,
            private_message=args.private_message,
        )
    except (EOFError, KeyboardInterrupt):
        print("\nActivation cancelled. No automatic fallback was used.")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
