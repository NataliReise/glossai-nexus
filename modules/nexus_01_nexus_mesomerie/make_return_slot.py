#!/usr/bin/env python3
"""Create a local Return Resonance slot file from explicit safe values.

This is the first small generator step after the copy-before-use template.
It does not read private activation packages.
It does not read First Spark internals.
It does not publish anything online.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

DEFAULT_MODULE_ID = "N01"
DEFAULT_LAYER_ID = "return-resonance-1"
DEFAULT_STATUS = "waiting"
DEFAULT_DOCUMENT_STATUS = "private local return slots"
DEFAULT_NOTE = "origin_trace_id identifies a local resonance arc, not a person"


class ReturnSlotGeneratorError(Exception):
    """Raised when a local return slot file cannot be generated safely."""


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)

    output_path = args.output.expanduser().resolve()

    print("Nexus 01 - Make Return Slot")
    print("===========================")
    print()
    print("This command creates a local Return Resonance slot file from explicit values.")
    print("It does not read private activation packages and does not publish anything online.")
    print()

    try:
        slot_document = build_slot_document(
            origin_trace_id=args.origin_trace_id,
            return_slot_id=args.return_slot_id,
            package_id=args.package_id,
            result_file=args.result_file,
            public_safe_label=args.public_safe_label,
            note=args.note,
            module_id=args.module_id,
            layer_id=args.layer_id,
        )
        write_slot_document(slot_document, output_path, overwrite=args.overwrite)
    except ReturnSlotGeneratorError as error:
        print("Error:", error)
        return 1
    except OSError as error:
        print("Error:", error)
        return 2

    print("Slot file created:", _display_path(output_path))
    print("Origin trace:", args.origin_trace_id)
    print("Return slot:", args.return_slot_id)
    print("Package:", args.package_id)
    print("Layer:", args.layer_id)
    print()
    print("Privacy reminder:")
    print("Do not put private gift meaning, real names, contact details, key material,")
    print("or private relationship context into a public-safe slot.")

    return 0


def build_slot_document(
    *,
    origin_trace_id: str,
    return_slot_id: str,
    package_id: str,
    result_file: str,
    public_safe_label: str,
    note: str,
    module_id: str = DEFAULT_MODULE_ID,
    layer_id: str = DEFAULT_LAYER_ID,
) -> dict[str, object]:
    """Build a single-slot Return Resonance document from explicit safe values."""

    for field_name, value in {
        "origin_trace_id": origin_trace_id,
        "return_slot_id": return_slot_id,
        "package_id": package_id,
        "result_file": result_file,
        "public_safe_label": public_safe_label,
        "module_id": module_id,
        "layer_id": layer_id,
    }.items():
        _require_non_empty(field_name, value)

    return {
        "document_status": DEFAULT_DOCUMENT_STATUS,
        "slots": [
            {
                "origin_trace_id": origin_trace_id,
                "return_slot_id": return_slot_id,
                "module_id": module_id,
                "package_id": package_id,
                "layer_id": layer_id,
                "status": DEFAULT_STATUS,
                "result_file": result_file,
                "public_safe_label": public_safe_label,
                "note": note,
            }
        ],
    }


def write_slot_document(
    slot_document: dict[str, object],
    output_path: Path,
    *,
    overwrite: bool = False,
) -> None:
    """Write the generated slot document to a local JSON file."""

    if output_path.exists() and not overwrite:
        raise ReturnSlotGeneratorError(
            f"output file already exists: {output_path}. Use --overwrite to replace it."
        )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(slot_document, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def _require_non_empty(field_name: str, value: str) -> None:
    if not value.strip():
        raise ReturnSlotGeneratorError(f"{field_name} must not be empty")


def _parse_args(argv: list[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create a local Nexus 01 Return Resonance slot file.",
    )
    parser.add_argument(
        "--origin-trace-id",
        required=True,
        help="Safe local origin trace ID, not a person identifier.",
    )
    parser.add_argument(
        "--return-slot-id",
        required=True,
        help="Safe symbolic return slot ID.",
    )
    parser.add_argument(
        "--package-id",
        required=True,
        help="Safe local package ID.",
    )
    parser.add_argument(
        "--result-file",
        required=True,
        help="Local result filename, usually ending in .local.md.",
    )
    parser.add_argument(
        "--public-safe-label",
        required=True,
        help="Short public-safe label for the slot.",
    )
    parser.add_argument(
        "--output",
        required=True,
        type=Path,
        help="Path where the local slot JSON file should be written.",
    )
    parser.add_argument(
        "--module-id",
        default=DEFAULT_MODULE_ID,
        help="Module ID. Defaults to N01.",
    )
    parser.add_argument(
        "--layer-id",
        default=DEFAULT_LAYER_ID,
        help="Layer ID. Defaults to return-resonance-1.",
    )
    parser.add_argument(
        "--note",
        default=DEFAULT_NOTE,
        help="Local-safe note for the slot.",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Replace the output file if it already exists.",
    )
    return parser.parse_args(argv)


def _display_path(path: Path) -> Path:
    try:
        return path.relative_to(Path.cwd())
    except ValueError:
        return path


if __name__ == "__main__":
    raise SystemExit(main())
