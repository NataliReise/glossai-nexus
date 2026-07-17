#!/usr/bin/env python3
"""Prepare either a First Spark gift or a matched Resonance gift boundary."""

from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
import json
import os
from pathlib import Path
import secrets
import shutil
import stat
import sys
import tempfile
import zipfile


SCRIPT_PATH = Path(__file__).resolve()
NEXUS_ROOT = SCRIPT_PATH.parents[1]
REPO_ROOT = SCRIPT_PATH.parents[3]
FIRST_SPARK_ROOT = NEXUS_ROOT / "first_spark"
DEFAULT_DIST_ROOT = REPO_ROOT / "dist"
DEFAULT_PRIVATE_ROOT = DEFAULT_DIST_ROOT / "nexus-01-return-workspaces"
for import_root in (SCRIPT_PATH.parent, NEXUS_ROOT, FIRST_SPARK_ROOT):
    if str(import_root) not in sys.path:
        sys.path.insert(0, str(import_root))

from build_first_spark_gift_package import (  # noqa: E402
    GiftPackageError,
    build_gift_package,
    package_name_from_label,
)
from first_spark.activation import (  # noqa: E402
    ActivationFileError,
    FIRST_SPARK_PROFILE_ID,
    RETURN_RESONANCE_PROFILE_ID,
    activation_from_mapping,
    load_activation,
)
from make_return_slot import build_slot_document  # noqa: E402
from return_workspace import (  # noqa: E402
    SLOT_PATH as WORKSPACE_SLOT_PATH,
    build_return_workspace,
    workspace_name,
)
from return_resonance.slots import load_return_slots  # noqa: E402
from return_resonance.token import (  # noqa: E402
    LAYER_ID,
    MODULE_ID,
    TOKEN_TYPE,
    TOKEN_VERSION,
    parse_resonance_token,
)
from verify_first_spark_gift_package import verify_package as verify_first_spark_package  # noqa: E402
from verify_resonance_gift_package import (  # noqa: E402
    ACTIVATION_PATH,
    PUBLIC_RUNTIME_FILES,
    TOKEN_PATH,
    contains_template_sentinel,
    is_safe_result_filename,
    verify_preparation,
)
from verify_return_workspace import verify_workspace  # noqa: E402


RESONANCE_PACKAGE_PREFIX = "nexus-01-resonance-gift"
TOKEN_NOTE = "This token identifies a resonance arc, not a person."
SLOT_NOTE = "origin_trace_id identifies a local resonance arc, not a person"

RESONANCE_START_SCRIPT = """#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"
PYTHONDONTWRITEBYTECODE=1 python3 run_nexus.py --legacy-preactivated
"""

RESONANCE_README = """# Nexus 01 - Resonance Gift

This is an explicitly legacy pre-activated Nexus 01 Resonance gift. It preserves
the earlier one-person compatibility flow and is not the corrected recipient-
choice invitation model.

## Start

Open a terminal in this folder and run:

```bash
./START_HERE.sh
```

You need Python 3 and a Linux terminal. No external Python packages are required.

The legacy Atrium offers `first-spark` and `resonance`. When the Resonance Chamber asks
for a token path, enter:

```text
resonance_token.local.json
```

If you save the Return Artifact, choose a local destination you can find again.
The giver's private matching Return Slot is not contained in this gift.

`START_HERE.sh` deliberately uses `--legacy-preactivated`. Do not remove that
flag or reinterpret the bundled Token V1 as a corrected Token V2 invitation.
"""

RESONANCE_GIFT_NOTE = """# Resonance Gift Boundary

The activation and Resonance Token travel with this package.
The matching private Return Slot remains with the giver.

This package does not upload, send, sync, or track anything automatically.
"""


class PreparationError(RuntimeError):
    """Raised when a gift cannot be prepared without publishing partial output."""


@dataclass(frozen=True)
class RouteIdentity:
    module_id: str
    layer_id: str
    origin_trace_id: str
    return_slot_id: str
    package_id: str


@dataclass(frozen=True)
class PreparationResult:
    mode: str
    gift_path: Path
    zip_path: Path | None = None
    private_slot_path: Path | None = None
    route: RouteIdentity | None = None
    private_workspace_path: Path | None = None


def generate_route_identity() -> RouteIdentity:
    """Generate opaque structural identifiers without using activation content."""
    route_key = secrets.token_hex(12)
    return RouteIdentity(
        module_id=MODULE_ID,
        layer_id=LAYER_ID,
        origin_trace_id=f"n01-origin-{route_key}",
        return_slot_id=f"n01-slot-{route_key}",
        package_id=f"n01-package-{route_key}",
    )


def activation_mapping(
    profile_id: str,
    recipient_alias: str,
    activation_purpose: str,
    private_message: str,
) -> dict[str, str]:
    mapping = {
        "profile_id": profile_id,
        "recipient_alias": recipient_alias,
        "activation_purpose": activation_purpose,
        "private_message": private_message,
    }
    activation_from_mapping(mapping)
    return mapping


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def validate_first_spark_activation(path: Path) -> None:
    activation = load_activation(path)
    if activation.profile_id != FIRST_SPARK_PROFILE_ID:
        raise PreparationError(
            "First Spark preparation requires activation.profile_id == 'first-spark'."
        )


def validate_public_label(value: str) -> str:
    cleaned = value.strip()
    if not cleaned:
        raise PreparationError("public_safe_label must not be empty")
    if contains_template_sentinel(cleaned):
        raise PreparationError("public_safe_label contains a template sentinel")
    if len(cleaned) > 80:
        raise PreparationError("public_safe_label must be 80 characters or fewer")
    return cleaned


def validate_result_filename(value: str) -> str:
    if not is_safe_result_filename(value):
        raise PreparationError(
            "result_file must be one plain ASCII filename without directories or traversal"
        )
    if contains_template_sentinel(value):
        raise PreparationError("result_file contains a template sentinel")
    return value


def resonance_package_name(gift_label: str) -> str:
    # Reuse the existing normalizer without changing the First Spark builder.
    normalized_name = package_name_from_label(gift_label)
    normal_prefix = "nexus-01-first-spark-gift-"
    return RESONANCE_PACKAGE_PREFIX + "-" + normalized_name.removeprefix(normal_prefix)


def copy_resonance_runtime(package_dir: Path) -> None:
    """Copy only the files in the verifier-owned full-runtime allowlist."""
    for relative_path in sorted(PUBLIC_RUNTIME_FILES, key=str):
        source = NEXUS_ROOT / relative_path
        if not source.is_file():
            raise PreparationError(f"Required Resonance runtime file is missing: {source}")
        target = package_dir / relative_path
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)


def build_staged_resonance_package(
    package_dir: Path,
    activation: dict[str, str],
    token: dict[str, object],
) -> None:
    package_dir.mkdir(parents=True)
    copy_resonance_runtime(package_dir)
    write_json(package_dir / ACTIVATION_PATH, activation)
    write_json(package_dir / TOKEN_PATH, token)
    _write_text(package_dir / "README_FOR_RECIPIENT.md", RESONANCE_README)
    _write_text(package_dir / "GIFT_NOTE.md", RESONANCE_GIFT_NOTE)
    _write_text(package_dir / "START_HERE.sh", RESONANCE_START_SCRIPT)
    _make_executable(package_dir / "START_HERE.sh")


def prepare_first_spark(
    *,
    gift_label: str,
    dist_root: Path,
    activation_path: Path | None,
    recipient_alias: str,
    activation_purpose: str,
    private_message: str,
    zip_package: bool,
) -> PreparationResult:
    dist_root = dist_root.expanduser().resolve()
    package_name = package_name_from_label(gift_label)
    final_package = dist_root / package_name
    final_zip = (dist_root / package_name).with_suffix(".zip") if zip_package else None
    _require_absent(final_package, final_zip)

    dist_root.parent.mkdir(parents=True, exist_ok=True)
    stage_root = Path(tempfile.mkdtemp(prefix=".nexus-first-spark-stage-", dir=dist_root.parent))
    published: list[Path] = []
    try:
        stage_dist = stage_root / "dist"
        if activation_path is None:
            staged_activation = stage_root / "activation.local.json"
            mapping = activation_mapping(
                FIRST_SPARK_PROFILE_ID, recipient_alias, activation_purpose, private_message
            )
            write_json(staged_activation, mapping)
        else:
            staged_activation = activation_path.expanduser().resolve()

        validate_first_spark_activation(staged_activation)
        staged_package = build_gift_package(
            package_name=package_name,
            dist_root=stage_dist,
            local_activation_path=staged_activation,
            overwrite=False,
            zip_package=zip_package,
        )
        verification = verify_first_spark_package(staged_package)
        if not verification.passed:
            raise PreparationError(
                "Staged First Spark package failed verification: " + "; ".join(verification.errors)
            )
        staged_zip = (stage_dist / package_name).with_suffix(".zip") if zip_package else None
        if staged_zip is not None:
            _verify_zip(staged_zip, staged_package, package_name)

        _publish(staged_package, final_package)
        published.append(final_package)
        if staged_zip is not None and final_zip is not None:
            _publish(staged_zip, final_zip)
            published.append(final_zip)
        return PreparationResult("first-spark", final_package, final_zip)
    except Exception:
        _rollback_publication(*published)
        raise
    finally:
        shutil.rmtree(stage_root, ignore_errors=True)


def prepare_resonance(
    *,
    gift_label: str,
    dist_root: Path,
    private_root: Path,
    recipient_alias: str,
    activation_purpose: str,
    private_message: str,
    public_safe_label: str,
    result_file: str | None,
    zip_package: bool,
    route: RouteIdentity | None = None,
) -> PreparationResult:
    dist_root = dist_root.expanduser().resolve()
    private_root = private_root.expanduser().resolve()
    package_name = resonance_package_name(gift_label)
    route = route or generate_route_identity()
    _validate_route(route)
    public_safe_label = validate_public_label(public_safe_label)
    result_file = validate_result_filename(
        result_file or f"return_resonance_{route.return_slot_id}.local.md"
    )

    final_package = dist_root / package_name
    final_zip = (dist_root / package_name).with_suffix(".zip") if zip_package else None
    final_workspace = private_root / workspace_name(route.return_slot_id)
    final_slot = final_workspace / WORKSPACE_SLOT_PATH
    if final_workspace.is_relative_to(final_package) or final_package.is_relative_to(
        final_workspace
    ):
        raise PreparationError(
            "The private Return Workspace and travelling gift must be separate paths."
        )
    _require_absent(final_package, final_zip, final_workspace)

    activation = activation_mapping(
        RETURN_RESONANCE_PROFILE_ID, recipient_alias, activation_purpose, private_message
    )
    token: dict[str, object] = {
        "token_version": TOKEN_VERSION,
        "token_type": TOKEN_TYPE,
        **asdict(route),
        "enabled_chambers": ["resonance"],
        "public_safe_label": public_safe_label,
        "note": TOKEN_NOTE,
    }
    parsed_token = parse_resonance_token(token)
    if not parsed_token.enables_resonance:
        raise PreparationError("Generated Resonance Token does not enable resonance")

    slot_document = build_slot_document(
        origin_trace_id=route.origin_trace_id,
        return_slot_id=route.return_slot_id,
        package_id=route.package_id,
        result_file=result_file,
        public_safe_label=public_safe_label,
        note=SLOT_NOTE,
        module_id=route.module_id,
        layer_id=route.layer_id,
    )

    dist_root.parent.mkdir(parents=True, exist_ok=True)
    private_root.parent.mkdir(parents=True, exist_ok=True)
    gift_stage_root = Path(tempfile.mkdtemp(prefix=".nexus-resonance-stage-", dir=dist_root.parent))
    workspace_stage_root = Path(
        tempfile.mkdtemp(prefix=".nexus-return-workspace-stage-", dir=private_root.parent)
    )
    published: list[Path] = []
    try:
        staged_package = gift_stage_root / package_name
        staged_workspace = workspace_stage_root / workspace_name(route.return_slot_id)
        staged_slot = staged_workspace / WORKSPACE_SLOT_PATH
        build_staged_resonance_package(staged_package, activation, token)
        build_return_workspace(staged_workspace, slot_document)

        verification = verify_preparation(staged_package, staged_slot)
        if not verification.passed:
            raise PreparationError(
                "Staged Resonance preparation failed verification: "
                + "; ".join(verification.errors)
            )
        workspace_verification = verify_workspace(
            staged_workspace,
            asdict(route),
            gift_dir=staged_package,
        )
        if not workspace_verification.passed:
            raise PreparationError(
                "Staged private Return Workspace failed verification: "
                + "; ".join(workspace_verification.errors)
            )
        loaded_slot = load_return_slots(staged_slot)[0]
        for field_name in (
            "module_id", "layer_id", "origin_trace_id", "return_slot_id", "package_id"
        ):
            if getattr(parsed_token, field_name) != getattr(loaded_slot, field_name):
                raise PreparationError(f"Generated route identity mismatch: {field_name}")

        staged_zip = None
        if zip_package:
            staged_zip = Path(
                shutil.make_archive(
                    str(gift_stage_root / package_name),
                    "zip",
                    root_dir=gift_stage_root,
                    base_dir=package_name,
                )
            )
            _verify_zip(staged_zip, staged_package, package_name)

        _publish(staged_package, final_package)
        published.append(final_package)
        _publish(staged_workspace, final_workspace)
        published.append(final_workspace)
        if staged_zip is not None and final_zip is not None:
            _publish(staged_zip, final_zip)
            published.append(final_zip)
        return PreparationResult(
            mode="resonance",
            gift_path=final_package,
            zip_path=final_zip,
            private_slot_path=final_slot,
            route=route,
            private_workspace_path=final_workspace,
        )
    except Exception:
        _rollback_publication(*published)
        raise
    finally:
        shutil.rmtree(gift_stage_root, ignore_errors=True)
        shutil.rmtree(workspace_stage_root, ignore_errors=True)


def _validate_route(route: RouteIdentity) -> None:
    if route.module_id != MODULE_ID or route.layer_id != LAYER_ID:
        raise PreparationError("Route identity uses an unsupported module_id or layer_id")
    for field_name, value in asdict(route).items():
        if not value or contains_template_sentinel(value):
            raise PreparationError(f"Route field {field_name!r} is empty or contains a sentinel")
        if not all(character.isascii() and (character.isalnum() or character in "._-") for character in value):
            raise PreparationError(f"Route field {field_name!r} is not public-safe ASCII")


def _require_absent(*paths: Path | None) -> None:
    for path in paths:
        if path is not None and path.exists():
            raise PreparationError(f"Refusing to overwrite existing output: {path}")


def _publish(staged: Path, final: Path) -> None:
    final.parent.mkdir(parents=True, exist_ok=True)
    if final.exists():
        raise PreparationError(f"Refusing to overwrite existing output: {final}")
    if staged.is_file():
        # Hard-link creation is exclusive: it cannot replace a file introduced
        # between the preflight check and publication.
        os.link(staged, final)
        staged.unlink()
    else:
        os.rename(staged, final)


def _rollback_publication(*paths: Path | None) -> None:
    for path in paths:
        if path is None or not path.exists():
            continue
        if path.is_dir():
            shutil.rmtree(path)
        else:
            path.unlink()


def _verify_zip(zip_path: Path, package_dir: Path, package_name: str) -> None:
    expected = {
        f"{package_name}/{path.relative_to(package_dir).as_posix()}"
        for path in package_dir.rglob("*")
        if path.is_file()
    }
    with zipfile.ZipFile(zip_path) as archive:
        actual = {name for name in archive.namelist() if not name.endswith("/")}
        bad_entry = any(Path(name).is_absolute() or ".." in Path(name).parts for name in actual)
    if bad_entry or actual != expected:
        raise PreparationError("Generated ZIP contents do not exactly match the verified package")


def _write_text(path: Path, value: str) -> None:
    path.write_text(value.rstrip() + "\n", encoding="utf-8")


def _make_executable(path: Path) -> None:
    path.chmod(path.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Prepare a local Nexus 01 gift boundary.")
    subparsers = parser.add_subparsers(dest="mode", required=True)

    def add_common(subparser: argparse.ArgumentParser) -> None:
        subparser.add_argument("--gift-label", required=True)
        subparser.add_argument("--dist-root", type=Path, default=DEFAULT_DIST_ROOT)
        subparser.add_argument("--recipient-alias", default="recipient_name")
        subparser.add_argument("--activation-purpose", default="gift")
        subparser.add_argument("--private-message", default="A Nexus 01 gift is waiting for you.")
        subparser.add_argument("--zip", action="store_true")

    first_spark_parser = subparsers.add_parser("first-spark")
    add_common(first_spark_parser)
    first_spark_parser.add_argument(
        "--activation", type=Path, help="Accept an existing first-spark activation file."
    )

    resonance_parser = subparsers.add_parser("resonance")
    add_common(resonance_parser)
    resonance_parser.add_argument("--private-root", type=Path, default=DEFAULT_PRIVATE_ROOT)
    resonance_parser.add_argument("--public-safe-label", default="resonance path")
    resonance_parser.add_argument("--result-file")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        if args.mode == "first-spark":
            result = prepare_first_spark(
                gift_label=args.gift_label,
                dist_root=args.dist_root,
                activation_path=args.activation,
                recipient_alias=args.recipient_alias,
                activation_purpose=args.activation_purpose,
                private_message=args.private_message,
                zip_package=args.zip,
            )
        else:
            result = prepare_resonance(
                gift_label=args.gift_label,
                dist_root=args.dist_root,
                private_root=args.private_root,
                recipient_alias=args.recipient_alias,
                activation_purpose=args.activation_purpose,
                private_message=args.private_message,
                public_safe_label=args.public_safe_label,
                result_file=args.result_file,
                zip_package=args.zip,
            )
    except (ActivationFileError, GiftPackageError, OSError, PreparationError, ValueError) as error:
        print("Nexus 01 gift preparation failed.")
        print(error)
        return 1

    print("Nexus 01 gift preparation passed all validation.")
    print(f"Travelling gift: {result.gift_path}")
    if result.zip_path:
        print(f"Travelling ZIP: {result.zip_path}")
    if result.private_workspace_path:
        print(f"Private Return Workspace: {result.private_workspace_path}")
    if result.route:
        print("Structural route:")
        for field_name, value in asdict(result.route).items():
            print(f"  {field_name}: {value}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
