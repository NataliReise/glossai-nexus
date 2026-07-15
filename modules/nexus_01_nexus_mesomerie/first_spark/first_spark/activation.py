"""Activation loading for Nexus 0.1 - First Spark.

Public code may define the activation structure.
Real activation data belongs to local files that are ignored by Git.

The First Spark package remains independently runnable.  It therefore stores
only the validated public profile ID here; translation into the shared Atrium
profile model happens later at the Nexus boundary.
"""

from __future__ import annotations

from dataclasses import dataclass
import json
from json import JSONDecodeError
from pathlib import Path
from typing import Any


FIRST_SPARK_PROFILE_ID = "first-spark"
RETURN_RESONANCE_PROFILE_ID = "return-resonance"
KNOWN_PROFILE_IDS = frozenset(
    {FIRST_SPARK_PROFILE_ID, RETURN_RESONANCE_PROFILE_ID}
)

DEFAULT_PROFILE_ID = FIRST_SPARK_PROFILE_ID
DEFAULT_RECIPIENT_ALIAS = "recipient_name"
DEFAULT_ACTIVATION_PURPOSE = "gift"
DEFAULT_PRIVATE_MESSAGE = (
    "This is a public demo message.\n"
    "Real gift messages belong to the private activation layer."
)

LOCAL_ACTIVATION_PATH = Path(__file__).resolve().parents[1] / "activation.local.json"
EXAMPLE_ACTIVATION_PATH = Path(__file__).resolve().parents[1] / "activation.example.json"


class ActivationFileError(ValueError):
    """Raised when a local activation file cannot be loaded safely."""


@dataclass(frozen=True)
class Activation:
    """Small activation model retained by the standalone First Spark seed."""

    profile_id: str
    recipient_alias: str
    activation_purpose: str
    private_message: str


def default_activation() -> Activation:
    """Return the current public development fallback activation."""

    return Activation(
        profile_id=DEFAULT_PROFILE_ID,
        recipient_alias=DEFAULT_RECIPIENT_ALIAS,
        activation_purpose=DEFAULT_ACTIVATION_PURPOSE,
        private_message=DEFAULT_PRIVATE_MESSAGE,
    )


def activation_error_text(path: Path, detail: str) -> str:
    """Return a friendly activation-file error message."""

    return (
        "Activation file could not be loaded.\n\n"
        f"Please check:\n{path}\n\n"
        f"Problem:\n{detail}\n\n"
        "The file must be valid JSON with an object at the top level.\n"
        f"You can compare it with:\n{EXAMPLE_ACTIVATION_PATH}"
    )


def load_activation(path: Path = LOCAL_ACTIVATION_PATH) -> Activation:
    """Load local activation data, or use the current development fallback."""

    if not path.exists():
        return default_activation()

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except JSONDecodeError as error:
        detail = f"Invalid JSON near line {error.lineno}, column {error.colno}: {error.msg}."
        raise ActivationFileError(activation_error_text(path, detail)) from error
    except OSError as error:
        detail = str(error)
        raise ActivationFileError(activation_error_text(path, detail)) from error

    if not isinstance(data, dict):
        detail = "The top-level JSON value must be an object like activation.example.json."
        raise ActivationFileError(activation_error_text(path, detail))

    try:
        return activation_from_mapping(data)
    except ActivationFileError as error:
        raise ActivationFileError(activation_error_text(path, str(error))) from error


def activation_from_mapping(data: dict[str, Any]) -> Activation:
    """Create one normalized activation from a JSON-compatible mapping.

    Legacy activation files do not contain ``profile_id``.  They are preserved
    by normalizing that missing field to ``first-spark``.
    """

    default = default_activation()
    profile_id = str(data.get("profile_id", DEFAULT_PROFILE_ID)).strip()

    if profile_id not in KNOWN_PROFILE_IDS:
        allowed = ", ".join(sorted(KNOWN_PROFILE_IDS))
        raise ActivationFileError(
            f"Unknown activation profile {profile_id!r}. Allowed profiles: {allowed}."
        )

    return Activation(
        profile_id=profile_id,
        recipient_alias=str(data.get("recipient_alias", default.recipient_alias)),
        activation_purpose=str(data.get("activation_purpose", default.activation_purpose)),
        private_message=str(data.get("private_message", default.private_message)),
    )
