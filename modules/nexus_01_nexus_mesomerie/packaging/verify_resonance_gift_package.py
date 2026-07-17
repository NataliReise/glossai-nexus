#!/usr/bin/env python3
"""Verify a staged or published Nexus 01 Resonance gift package."""

from __future__ import annotations

import argparse
from dataclasses import dataclass, field
import stat
import sys
from pathlib import Path


SCRIPT_PATH = Path(__file__).resolve()
NEXUS_ROOT = SCRIPT_PATH.parents[1]
FIRST_SPARK_ROOT = NEXUS_ROOT / "first_spark"
for import_root in (NEXUS_ROOT, FIRST_SPARK_ROOT):
    if str(import_root) not in sys.path:
        sys.path.insert(0, str(import_root))

from first_spark.activation import (  # noqa: E402
    ActivationFileError,
    RETURN_RESONANCE_PROFILE_ID,
    load_activation,
)
from return_resonance.slots import (  # noqa: E402
    ReturnSlotLoadError,
    ReturnSlotState,
    load_return_slots,
)
from return_resonance.token import (  # noqa: E402
    LAYER_ID,
    MODULE_ID,
    ResonanceTokenLoadError,
    load_resonance_token,
)


ACTIVATION_PATH = Path("first_spark/activation.local.json")
TOKEN_PATH = Path("resonance_token.local.json")

PUBLIC_RUNTIME_FILES = frozenset(
    {
        Path("run_nexus.py"),
        *(Path("atrium") / name for name in (
            "__init__.py", "activation_bridge.py", "first_spark_adapter.py",
            "profiles.py", "resonance_adapter.py", "resonance_terminal.py",
            "runtime.py", "state.py", "terminal.py",
        )),
        *(Path("chambers/resonance") / name for name in (
            "__init__.py", "choices.py", "composer.py", "flow.py", "terminal_io.py",
        )),
        Path("first_spark/run_first_spark.py"),
        Path("first_spark/activation.example.json"),
        *(Path("first_spark/first_spark") / name for name in (
            "__init__.py", "activation.py", "command_feedback.py", "config.py",
            "guidance.py", "module_response.py", "runtime.py", "state.py",
        )),
        *(Path("first_spark/first_spark/game_modules") / name for name in (
            "__init__.py", "arrival.py", "ending.py", "spark_chamber.py",
        )),
        *(Path("return_resonance") / name for name in (
            "__init__.py", "artifact.py", "artifact_store.py", "local_opening.py",
            "matching.py", "resonance_render_bridge.py", "result.py", "slots.py",
            "token.py", "writer.py",
        )),
        *(Path("resonance_language_library") / name for name in (
            "render_nexus_echo.py", "render_resonance_artifact.py",
            "render_resonance_output.py",
        )),
        *(Path("resonance_language_library/v0_1") / name for name in (
            "echo_paths.json", "image_responses.json", "images.json",
            "movement_responses.json", "movements.json", "scent_responses.json",
            "scents.json",
        )),
    }
)

GENERATED_GIFT_FILES = frozenset(
    {
        Path("START_HERE.sh"),
        Path("README_FOR_RECIPIENT.md"),
        Path("GIFT_NOTE.md"),
        ACTIVATION_PATH,
        TOKEN_PATH,
    }
)
ALLOWED_FILES = PUBLIC_RUNTIME_FILES | GENERATED_GIFT_FILES
FORBIDDEN_PARTS = frozenset(
    {".git", "__pycache__", ".pytest_cache", "tests", "experiments", "archive", "examples"}
)
FORBIDDEN_NAMES = frozenset(
    {
        "return_slots.local.json",
        "return_slot.local.json",
        "return_artifact.local.txt",
        "resonance_return.local.json",
        "return_result.local.md",
        "local_result.md",
    }
)
SENTINEL_FRAGMENTS = (
    "CHANGE-ME", "CHANGE_ME", "CHANGEME", "REPLACE-ME", "REPLACE_ME", "TODO", "TBD"
)


@dataclass
class VerificationResult:
    errors: list[str] = field(default_factory=list)

    @property
    def passed(self) -> bool:
        return not self.errors

    def add_error(self, message: str) -> None:
        self.errors.append(message)


def contains_template_sentinel(value: str) -> bool:
    upper = value.strip().upper()
    return any(fragment in upper for fragment in SENTINEL_FRAGMENTS)


def is_safe_result_filename(value: str) -> bool:
    path = Path(value)
    if not value or path.is_absolute() or path.name != value or value in {".", ".."}:
        return False
    if any(part in {".", ".."} for part in path.parts):
        return False
    return all(character.isascii() and (character.isalnum() or character in "._-") for character in value)


def verify_package(package_dir: Path) -> VerificationResult:
    result = VerificationResult()
    if not package_dir.is_dir():
        result.add_error(f"Package directory does not exist or is not a directory: {package_dir}")
        return result

    actual_files = {path.relative_to(package_dir) for path in package_dir.rglob("*") if path.is_file()}
    for missing in sorted(ALLOWED_FILES - actual_files, key=str):
        result.add_error(f"Missing required file: {missing}")
    for unexpected in sorted(actual_files - ALLOWED_FILES, key=str):
        result.add_error(f"Unexpected file outside Resonance allowlist: {unexpected}")

    for relative_path in actual_files:
        if FORBIDDEN_PARTS.intersection(relative_path.parts):
            result.add_error(f"Forbidden development path found: {relative_path}")
        if relative_path.name in FORBIDDEN_NAMES:
            result.add_error(f"Forbidden private or generated file found: {relative_path}")
        if relative_path.suffix in {".pyc", ".pyo"}:
            result.add_error(f"Forbidden Python cache file found: {relative_path}")

    start_script = package_dir / "START_HERE.sh"
    if start_script.is_file() and not start_script.stat().st_mode & (
        stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH
    ):
        result.add_error("START_HERE.sh is not executable")

    activation = None
    try:
        activation = load_activation(package_dir / ACTIVATION_PATH)
    except ActivationFileError as error:
        result.add_error(f"Resonance activation failed runtime validation: {error}")
    if activation is not None and activation.profile_id != RETURN_RESONANCE_PROFILE_ID:
        result.add_error("Resonance activation must use profile_id 'return-resonance'")

    token = None
    try:
        token = load_resonance_token(package_dir / TOKEN_PATH)
    except ResonanceTokenLoadError as error:
        result.add_error(f"Bundled Resonance Token failed validation: {error}")
    if token is not None:
        for field_name in ("origin_trace_id", "return_slot_id", "package_id"):
            if contains_template_sentinel(getattr(token, field_name)):
                result.add_error(f"Token field {field_name!r} contains a template sentinel")
        if not token.enables_resonance:
            result.add_error("Bundled Resonance Token must enable the Resonance Chamber")

    return result


def verify_preparation(package_dir: Path, private_slot_path: Path) -> VerificationResult:
    result = verify_package(package_dir)
    try:
        token = load_resonance_token(package_dir / TOKEN_PATH)
    except ResonanceTokenLoadError:
        return result

    try:
        slots = load_return_slots(private_slot_path)
    except ReturnSlotLoadError as error:
        result.add_error(f"Private Return Slot failed validation: {error}")
        return result

    if len(slots) != 1:
        result.add_error("Private Return Slot document must contain exactly one slot")
        return result

    slot = slots[0]
    if slot.status is not ReturnSlotState.WAITING:
        result.add_error("Generated private Return Slot must have status 'waiting'")
    if not is_safe_result_filename(slot.result_file):
        result.add_error("Return Slot result_file must be a plain safe relative filename")
    if contains_template_sentinel(slot.result_file):
        result.add_error("Return Slot result_file contains a template sentinel")

    for field_name in (
        "module_id", "layer_id", "origin_trace_id", "return_slot_id", "package_id"
    ):
        token_value = getattr(token, field_name)
        slot_value = getattr(slot, field_name)
        if token_value != slot_value:
            result.add_error(
                f"Token and Return Slot disagree on {field_name}: {token_value!r} != {slot_value!r}"
            )
        if contains_template_sentinel(slot_value):
            result.add_error(f"Return Slot field {field_name!r} contains a template sentinel")

    if token.module_id != MODULE_ID or slot.module_id != MODULE_ID:
        result.add_error(f"Resonance route must use module_id {MODULE_ID!r}")
    if token.layer_id != LAYER_ID or slot.layer_id != LAYER_ID:
        result.add_error(f"Resonance route must use layer_id {LAYER_ID!r}")
    return result


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Verify a Nexus 01 Resonance gift package.")
    parser.add_argument("package_dir", type=Path)
    parser.add_argument(
        "--private-slot",
        type=Path,
        help="Also validate the matching giver-retained Return Slot.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    result = (
        verify_preparation(args.package_dir, args.private_slot)
        if args.private_slot
        else verify_package(args.package_dir)
    )
    if result.passed:
        print("Resonance gift package verification passed.")
        print(f"Travelling gift: {args.package_dir}")
        if args.private_slot:
            print(f"Retained private slot: {args.private_slot}")
        return 0

    print("Resonance gift package verification failed.")
    for error in result.errors:
        print(f"- {error}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
