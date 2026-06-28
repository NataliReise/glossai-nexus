"""Activation loading for Nexus 0.1 - First Spark.

Public code may define the activation structure.
Real activation data belongs to local files that are ignored by Git.
"""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any


DEFAULT_RECIPIENT_ALIAS = "recipient_name"
DEFAULT_ACTIVATION_PURPOSE = "gift"
DEFAULT_PRIVATE_MESSAGE = (
    "This is a public demo message.\n"
    "Real gift messages belong to the private activation layer."
)

LOCAL_ACTIVATION_PATH = Path(__file__).resolve().parents[1] / "activation.local.json"


@dataclass(frozen=True)
class Activation:
    """Small public activation model for the First Spark prototype."""

    recipient_alias: str
    activation_purpose: str
    private_message: str


def default_activation() -> Activation:
    """Return the public demo activation."""
    return Activation(
        recipient_alias=DEFAULT_RECIPIENT_ALIAS,
        activation_purpose=DEFAULT_ACTIVATION_PURPOSE,
        private_message=DEFAULT_PRIVATE_MESSAGE,
    )


def load_activation(path: Path = LOCAL_ACTIVATION_PATH) -> Activation:
    """Load local activation data, or fall back to the public demo activation."""
    if not path.exists():
        return default_activation()

    data = json.loads(path.read_text(encoding="utf-8"))
    return activation_from_mapping(data)


def activation_from_mapping(data: dict[str, Any]) -> Activation:
    """Create an activation from a mapping, using demo defaults for missing fields."""
    default = default_activation()
    return Activation(
        recipient_alias=str(data.get("recipient_alias", default.recipient_alias)),
        activation_purpose=str(data.get("activation_purpose", default.activation_purpose)),
        private_message=str(data.get("private_message", default.private_message)),
    )
