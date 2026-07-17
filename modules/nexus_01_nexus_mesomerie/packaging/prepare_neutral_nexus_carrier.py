#!/usr/bin/env python3
"""Build one corrected activation-ready Neutral Nexus Carrier."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import json
import os
from pathlib import Path
import re
import shutil
import stat
import sys
import tempfile


SCRIPT_PATH = Path(__file__).resolve()
NEXUS_ROOT = SCRIPT_PATH.parents[1]
REPO_ROOT = SCRIPT_PATH.parents[3]
DEFAULT_OUTPUT_DIR = REPO_ROOT / "dist"
if str(NEXUS_ROOT) not in sys.path:
    sys.path.insert(0, str(NEXUS_ROOT))

from return_resonance.token import (  # noqa: E402
    ResonanceTokenLoadError,
    parse_resonance_token,
)
from verify_neutral_nexus_carrier import (  # noqa: E402
    NEUTRAL_RUNTIME_FILES,
    README_PATH,
    SIDECAR_PATH,
    START_PATH,
    START_SCRIPT,
    verify_carrier,
    verify_carrier_zip,
)


PACKAGE_PREFIX = "nexus-01-neutral-carrier"

RECIPIENT_README = """# Nexus 01 — Neutral Nexus Carrier

This is an **activation-ready** Nexus 01, not a pre-activated gift. The
recipient chooses how to activate it on first start:

1. normal activation;
2. activation with a deliberately selected Resonance Token V2; or
3. cancellation without creating activation state.

Start it with:

```bash
./START_HERE.sh
```

Python 3.11 or newer and a Bash-compatible terminal are required.

## Optional Resonance invitation

If `invitation/resonance_token.v2.json` is present, it is **only an invitation**.
Its presence does not activate this Nexus and it is never selected
automatically. Normal activation leaves the invitation unused and unchanged.

To accept it, choose Token activation and deliberately select this relative
path when prompted:

```text
invitation/resonance_token.v2.json
```

The Token may instead travel separately and any valid Nexus 01 Token V2 may be
selected deliberately. It is not tied to this particular carrier copy.

The originating person's private Return Workspace must remain private and must
not travel with this carrier. Nexus modules, invitations, and later Return
Artifacts are transferred manually by people. No upload, sending, cloud
transport, synchronization, tracking, or automatic communication occurs.
"""


class NeutralCarrierError(RuntimeError):
    """Raised when a carrier cannot be built and published safely."""


@dataclass(frozen=True)
class NeutralCarrierResult:
    carrier_path: Path
    zip_path: Path | None
    sidecar_path: Path | None


def carrier_name(label: str) -> str:
    """Return one public-safe deterministic package name."""

    cleaned = label.strip().lower()
    slug = re.sub(r"[^a-z0-9._-]+", "-", cleaned).strip("-._")
    if not slug:
        raise NeutralCarrierError(
            "carrier_label must contain an ASCII letter or number."
        )
    if len(slug) > 60:
        raise NeutralCarrierError("carrier_label is too long.")
    return f"{PACKAGE_PREFIX}-{slug}"


def prepare_neutral_nexus_carrier(
    *,
    output_dir: Path,
    carrier_label: str,
    token_path: Path | None = None,
    zip_package: bool = False,
) -> NeutralCarrierResult:
    """Stage, verify, and publish one neutral carrier without activation data."""

    output_dir = output_dir.expanduser().resolve()
    package_name = carrier_name(carrier_label)
    final_carrier = output_dir / package_name
    final_zip = final_carrier.with_suffix(".zip") if zip_package else None
    _require_absent(final_carrier, final_zip)

    token_bytes = _validated_token_bytes(token_path) if token_path else None
    output_dir.parent.mkdir(parents=True, exist_ok=True)
    stage_root = Path(
        tempfile.mkdtemp(prefix=".neutral-nexus-carrier-stage-", dir=output_dir.parent)
    )
    published: list[Path] = []
    try:
        staged_carrier = stage_root / package_name
        staged_carrier.mkdir()
        _copy_runtime(staged_carrier)
        _write_text(staged_carrier / START_PATH, START_SCRIPT)
        _make_executable(staged_carrier / START_PATH)
        _write_text(staged_carrier / README_PATH, RECIPIENT_README)
        if token_bytes is not None:
            sidecar = staged_carrier / SIDECAR_PATH
            sidecar.parent.mkdir()
            sidecar.write_bytes(token_bytes)

        verification = verify_carrier(staged_carrier, token_path)
        if not verification.passed:
            raise NeutralCarrierError(
                "Staged Neutral Nexus Carrier failed verification: "
                + "; ".join(verification.errors)
            )

        staged_zip = None
        if zip_package:
            staged_zip = Path(
                shutil.make_archive(
                    str(stage_root / package_name),
                    "zip",
                    root_dir=stage_root,
                    base_dir=package_name,
                )
            )
            zip_verification = verify_carrier_zip(staged_zip, token_path)
            if not zip_verification.passed:
                raise NeutralCarrierError(
                    "Staged Neutral Nexus Carrier ZIP failed verification: "
                    + "; ".join(zip_verification.errors)
                )

        _publish(staged_carrier, final_carrier)
        published.append(final_carrier)
        if staged_zip is not None and final_zip is not None:
            _publish(staged_zip, final_zip)
            published.append(final_zip)
        return NeutralCarrierResult(
            carrier_path=final_carrier,
            zip_path=final_zip,
            sidecar_path=(final_carrier / SIDECAR_PATH if token_bytes else None),
        )
    except Exception:
        _rollback(*published)
        raise
    finally:
        shutil.rmtree(stage_root, ignore_errors=True)


def _validated_token_bytes(path: Path) -> bytes:
    try:
        token_bytes = path.expanduser().read_bytes()
        data = json.loads(token_bytes.decode("utf-8"))
        token = parse_resonance_token(data)
    except OSError as error:
        raise NeutralCarrierError(f"Could not read optional Token: {path}") from error
    except UnicodeError as error:
        raise NeutralCarrierError("Optional Token must be UTF-8 JSON.") from error
    except (json.JSONDecodeError, ResonanceTokenLoadError) as error:
        raise NeutralCarrierError(f"Optional Token failed validation: {error}") from error
    if token.is_legacy or not token.has_originating_contribution:
        raise NeutralCarrierError(
            "Neutral Nexus Carrier accepts only Resonance Token V2 invitations."
        )
    return token_bytes


def _copy_runtime(carrier_dir: Path) -> None:
    for relative in sorted(NEUTRAL_RUNTIME_FILES, key=str):
        source = NEXUS_ROOT / relative
        if not source.is_file():
            raise NeutralCarrierError(f"Required carrier runtime file is missing: {source}")
        target = carrier_dir / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)


def _require_absent(*paths: Path | None) -> None:
    for path in paths:
        if path is not None and path.exists():
            raise NeutralCarrierError(f"Refusing to overwrite existing output: {path}")


def _publish(staged: Path, final: Path) -> None:
    final.parent.mkdir(parents=True, exist_ok=True)
    if final.exists():
        raise NeutralCarrierError(f"Refusing to overwrite existing output: {final}")
    try:
        if staged.is_file():
            os.link(staged, final)
        else:
            os.rename(staged, final)
    except OSError as error:
        raise NeutralCarrierError(f"Could not publish carrier output: {final}") from error


def _rollback(*paths: Path) -> None:
    for path in reversed(paths):
        if path.is_dir():
            shutil.rmtree(path)
        elif path.exists():
            path.unlink()


def _write_text(path: Path, content: str) -> None:
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def _make_executable(path: Path) -> None:
    path.chmod(path.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Prepare a Neutral Nexus Carrier.")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--carrier-label", required=True)
    parser.add_argument("--token", type=Path)
    parser.add_argument("--zip", action="store_true")
    args = parser.parse_args(argv)
    try:
        result = prepare_neutral_nexus_carrier(
            output_dir=args.output_dir,
            carrier_label=args.carrier_label,
            token_path=args.token,
            zip_package=args.zip,
        )
    except NeutralCarrierError as error:
        print(f"Neutral Nexus Carrier preparation failed: {error}", file=sys.stderr)
        return 1
    print(f"Neutral Nexus Carrier directory: {result.carrier_path}")
    if result.zip_path:
        print(f"Neutral Nexus Carrier ZIP: {result.zip_path}")
    if result.sidecar_path:
        print(f"Optional inert Token V2 sidecar: {result.sidecar_path}")
    else:
        print("Optional inert Token V2 sidecar: not included")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
