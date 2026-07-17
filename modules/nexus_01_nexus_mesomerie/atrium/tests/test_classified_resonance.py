from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from atrium import (
    ClassifiedResonanceController,
    ResonanceMode,
    run_nexus_terminal,
)


@dataclass(frozen=True)
class ActivationStub:
    profile_id: str = "first-spark"


def run_mode(mode: ResonanceMode) -> tuple[object, str]:
    commands = iter(
        ("resonance", "/cancel", "quit")
        if mode is ResonanceMode.COMPOSE
        else ("resonance", "quit")
    )
    output: list[str] = []

    def forbidden_legacy():
        raise AssertionError("corrected mode reached legacy one-person flow")

    runtime = run_nexus_terminal(
        activation_loader=ActivationStub,
        resonance_runner=forbidden_legacy,
        resonance_mode=mode,
        input_reader=lambda _prompt: next(commands),
        output_writer=output.append,
    )
    return runtime, "\n".join(output)


def test_compose_shows_one_canonical_door_with_compose_wording() -> None:
    runtime, transcript = run_mode(ResonanceMode.COMPOSE)
    assert runtime.state.visible_paths.count("resonance") == 1
    assert "resonance — begin/send a resonance" in transcript
    assert "Compose cancelled" in transcript


def test_answer_shows_same_door_without_reaching_legacy_flow() -> None:
    runtime, transcript = run_mode(ResonanceMode.ANSWER)
    assert runtime.state.visible_paths.count("resonance") == 1
    assert "resonance — answer the carried resonance" in transcript
    assert "no authoritative Nexus activation context was supplied" in transcript


def test_blocked_shows_recovery_door_without_compose_or_legacy_flow() -> None:
    runtime, transcript = run_mode(ResonanceMode.BLOCKED_ANSWER_RECOVERY)
    assert runtime.state.visible_paths.count("resonance") == 1
    assert "resonance — the carried invitation needs attention" in transcript
    assert "blocked — recovery guidance available" in transcript
    assert "Nearby Tokens will not be selected automatically" in transcript
    assert "Compose and legacy Resonance flows remain unavailable" in transcript


def test_corrected_entry_uses_injected_classified_adapter_only() -> None:
    commands = iter(("resonance", "quit"))
    calls: list[str] = []
    classified = ClassifiedResonanceController(
        ResonanceMode.ANSWER, lambda message: calls.append(message)
    )

    def legacy():
        raise AssertionError("legacy controller was reachable")

    run_nexus_terminal(
        activation_loader=ActivationStub,
        resonance_runner=legacy,
        resonance_mode=ResonanceMode.ANSWER,
        classified_resonance_runner=classified,
        input_reader=lambda _prompt: next(commands),
        output_writer=lambda _message: None,
    )
    assert any("no authoritative Nexus activation context" in message for message in calls)


def test_corrected_mode_entries_create_no_return_artifact(tmp_path: Path) -> None:
    before = set(tmp_path.rglob("*"))
    for mode in ResonanceMode:
        result = ClassifiedResonanceController(
            mode,
            lambda _message: None,
            input_reader=lambda _prompt: "/cancel",
        )()
        assert not result.completed
    assert set(tmp_path.rglob("*")) == before
