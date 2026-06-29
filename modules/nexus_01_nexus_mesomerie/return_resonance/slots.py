"""Return slot data structures for Nexus 01 Return Resonance."""

from __future__ import annotations

import json
from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path
from typing import Any


class ReturnSlotState(StrEnum):
    """Persistent state for a local return slot."""

    WAITING = "waiting"
    OPENED = "opened"


@dataclass(frozen=True)
class ReturnSlot:
    """A local waiting place for a future return artifact."""

    origin_trace_id: str
    return_slot_id: str
    module_id: str
    package_id: str
    layer_id: str
    status: ReturnSlotState
    result_file: str
    public_safe_label: str = ""
    note: str = ""


class ReturnSlotLoadError(ValueError):
    """Raised when a return slot file cannot be loaded."""


_REQUIRED_SLOT_FIELDS = (
    "origin_trace_id",
    "return_slot_id",
    "module_id",
    "package_id",
    "layer_id",
    "status",
    "result_file",
)


def load_return_slots(path: str | Path) -> list[ReturnSlot]:
    """Load return slots from a JSON file."""

    slot_path = Path(path)
    try:
        raw_data = json.loads(slot_path.read_text(encoding="utf-8"))
    except OSError as error:
        raise ReturnSlotLoadError(f"Could not read return slot file: {slot_path}") from error
    except json.JSONDecodeError as error:
        raise ReturnSlotLoadError(f"Return slot file is not valid JSON: {slot_path}") from error

    raw_slots = raw_data.get("slots") if isinstance(raw_data, dict) else None
    if not isinstance(raw_slots, list):
        raise ReturnSlotLoadError("Return slot file must contain a slots list.")

    return [_slot_from_dict(index, item) for index, item in enumerate(raw_slots)]


def _slot_from_dict(index: int, item: Any) -> ReturnSlot:
    if not isinstance(item, dict):
        raise ReturnSlotLoadError(f"Return slot at index {index} is not an object.")

    missing = [field for field in _REQUIRED_SLOT_FIELDS if not item.get(field)]
    if missing:
        raise ReturnSlotLoadError(
            f"Return slot at index {index} is missing required field(s): "
            + ", ".join(missing)
        )

    try:
        status = ReturnSlotState(item["status"])
    except ValueError as error:
        raise ReturnSlotLoadError(
            f"Return slot at index {index} has unsupported status: {item['status']}"
        ) from error

    return ReturnSlot(
        origin_trace_id=str(item["origin_trace_id"]),
        return_slot_id=str(item["return_slot_id"]),
        module_id=str(item["module_id"]),
        package_id=str(item["package_id"]),
        layer_id=str(item["layer_id"]),
        status=status,
        result_file=str(item["result_file"]),
        public_safe_label=str(item.get("public_safe_label", "")),
        note=str(item.get("note", "")),
    )
