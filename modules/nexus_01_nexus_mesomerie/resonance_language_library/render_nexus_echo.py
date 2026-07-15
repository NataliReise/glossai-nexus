"""Render a Nexus Echo from a slim Return Artifact and approved echo paths.

The renderer performs no free text generation and uses no AI. It selects one
known-valid path, inserts approved one-word slots, and validates the 2-4-6-4-1
Nachhall pattern at runtime.
"""

from __future__ import annotations

from dataclasses import dat