#!/usr/bin/env python3
"""Nexus 0.1 - First Spark.

First running unit: print a small boot sequence.

This file is intentionally tiny. It proves that the first playable slice can
start locally before any command system, file inspection, or puzzle logic is
added.
"""

from __future__ import annotations


MODULE_TITLE = "Nexus 0.1 - First Spark"
RECIPIENT_ALIAS = "recipient_name"


def print_boot_sequence() -> None:
    """Print the first visible boot sequence for First Spark."""
    print()
    print("=" * 48)
    print(MODULE_TITLE)
    print("=" * 48)
    print()
    print("Activation detected.")
    print(f"Recipient: {RECIPIENT_ALIAS}")
    print("Private message: locked.")
    print()
    print("First running unit online.")
    print("Next unit: help command.")
    print()


def main() -> None:
    """Run the first tiny First Spark prototype."""
    print_boot_sequence()


if __name__ == "__main__":
    main()
