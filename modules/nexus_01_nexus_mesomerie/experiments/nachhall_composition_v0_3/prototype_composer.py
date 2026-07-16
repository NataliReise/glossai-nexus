#!/usr/bin/env python3
"""Compose one compact 2/4/6/4/1 Nachhall from a curated V0.3 library.

This experiment is intentionally isolated from the active Return Resonance paths.
It performs no semantic analysis and does not persist production results.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import json
from pathlib import Path
import random
import re
from typing import Any, Sequence, TypeVar

EXPECTED_LIBRARY_VERSION = "