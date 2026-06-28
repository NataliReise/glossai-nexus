"""Configuration for Nexus 0.1 - First Spark."""

from __future__ import annotations

from first_spark.activation import load_activation


ACTIVATION = load_activation()

MODULE_TITLE = "Nexus 0.1 - First Spark"
RECIPIENT_ALIAS = ACTIVATION.recipient_alias
PRIVATE_MESSAGE = ACTIVATION.private_message
ACTIVATION_PURPOSE = ACTIVATION.activation_purpose
PROMPT = "nexus> "
START_MODULE = "arrival"
