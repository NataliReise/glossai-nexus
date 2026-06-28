"""Configuration for Nexus 0.1 - First Spark."""

from __future__ import annotations

import sys

from first_spark.activation import ActivationFileError, load_activation


try:
    ACTIVATION = load_activation()
except ActivationFileError as error:
    print(error, file=sys.stderr)
    raise SystemExit(1) from error

MODULE_TITLE = "Nexus 0.1 - First Spark"
RECIPIENT_ALIAS = ACTIVATION.recipient_alias
PRIVATE_MESSAGE = ACTIVATION.private_message
ACTIVATION_PURPOSE = ACTIVATION.activation_purpose
PROMPT = "nexus> "
START_MODULE = "arrival"
