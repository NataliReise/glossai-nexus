"""Render a Nexus Echo from a slim Return Artifact and approved echo paths.

The renderer performs no free text generation and uses no AI. It first selects an
exact known-valid path. If no exact path exists, it combines one approved image,
scent, and movement component, then validates the 2-4-6-4-1 Nachhall pattern.
"""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
import re
from typing import Any

EXPECTED_ARTIFACT_VERSION = "0.1"
EXPECTED_LIBRARY_VERSION = "resonance-en-v0.1"
EXPECTED_WORD_COUNTS = (2, 4, 6, 4, 1)
ALLOWED_PLACEHOLDERS