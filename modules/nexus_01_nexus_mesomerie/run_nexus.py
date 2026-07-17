#!/usr/bin/env python3
"""Start corrected Nexus 01 activation and its shared Atrium."""

from __future__ import annotations

import argparse
from collections.abc import Callable
from pathlib import Path

from atrium.runtime import NexusAtriumRuntime
from atrium.classified_resonance import ClassifiedResonanceController
from atrium.terminal import run_nexus_terminal
from recipient_activation import (
    ActivationChoiceResult,
    RecipientActivationError,
    ResonanceMode,
    classify_runtime_interpretation,
    paths_for_nexus,
    run_recipient_activation,
)
from first_spark.activation import load_activation


NEXUS_ROOT = Path(__file__).resolve().parent
InputReader = Callable[[str], str]
OutputWriter = Callable[[str], None]


def run_corrected_nexus(
    *,
    nexus_root: Path = NEXUS_ROOT,
    recipient_alias: str = "recipient_name",
    activation_purpose: str = "gift",
    private_message: str = "A Nexus 01 gift is waiting for you.",
    input_reader: InputReader = input,
    output_writer: OutputWriter = print,
    activation_controller: Callable[..., ActivationChoiceResult] = run_recipient_activation,
    classifier: Callable[..., ResonanceMode] = classify_runtime_interpretation,
    atrium_runner: Callable[..., NexusAtriumRuntime] = run_nexus_terminal,
) -> NexusAtriumRuntime | None:
    """Activate when needed, classify, and enter the corrected Atrium."""

    paths = paths_for_nexus(nexus_root)
    if not paths.activation.is_file():
        outcome = activation_controller(
            nexus_root=nexus_root,
            recipient_alias=recipient_alias,
            activation_purpose=activation_purpose,
            private_message=private_message,
            input_reader=input_reader,
            output_writer=output_writer,
        )
        if outcome is ActivationChoiceResult.CANCELLED:
            output_writer("Nexus 01 remains unactivated. The Atrium was not opened.")
            return None

    try:
        mode = classifier(nexus_root=nexus_root)
        activation = load_activation(paths.activation)
    except (RecipientActivationError, ValueError) as error:
        output_writer(f"Nexus 01 could not open its activation state: {error}")
        return None

    return atrium_runner(
        activation_loader=lambda: activation,
        input_reader=input_reader,
        output_writer=output_writer,
        resonance_mode=mode,
        classified_resonance_runner=ClassifiedResonanceController(
            mode=mode,
            output_writer=output_writer,
            input_reader=input_reader,
            nexus_root=nexus_root,
        ),
    )


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Start Nexus 01.")
    parser.add_argument(
        "--legacy-preactivated",
        action="store_true",
        help="Run the explicitly legacy pre-activated one-person Resonance path.",
    )
    parser.add_argument("--nexus-root", type=Path, default=NEXUS_ROOT)
    parser.add_argument("--recipient-alias", default="recipient_name")
    parser.add_argument("--activation-purpose", default="gift")
    parser.add_argument(
        "--private-message", default="A Nexus 01 gift is waiting for you."
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    if args.legacy_preactivated:
        run_nexus_terminal()
        return 0
    try:
        run_corrected_nexus(
            nexus_root=args.nexus_root,
            recipient_alias=args.recipient_alias,
            activation_purpose=args.activation_purpose,
            private_message=args.private_message,
        )
    except (EOFError, KeyboardInterrupt):
        print("\nNexus 01 start cancelled. No automatic fallback was used.")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
