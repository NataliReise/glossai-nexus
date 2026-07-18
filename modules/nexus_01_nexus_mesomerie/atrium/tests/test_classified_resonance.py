from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from atrium import (
    ChamberRunResult,
    ClassifiedResonanceController,
    ResonanceMode,
    run_nexus_terminal,
)


@dataclass(frozen=True)
class ActivationStub:
    profile_id: str = "first-spark"
    activation_purpose: str = "gift"


def run_mode(mode: ResonanceMode) -> tuple[object, str]:
    if mode is ResonanceMode.COMPOSE:
        activation = ActivationStub("first-spark")
        commands = iter(("/first-spark", "/resonance", "/cancel", "/quit"))
    else:
        activation = ActivationStub("return-resonance")
        commands = iter(("/resonance", "/quit"))
    output: list[str] = []

    def forbidden_legacy():
        raise AssertionError("corrected mode reached legacy one-person flow")

    runtime = run_nexus_terminal(
        activation_loader=lambda: activation,
        first_spark_runner=lambda: ChamberRunResult(completed=True),
        resonance_runner=forbidden_legacy,
        resonance_mode=mode,
        input_reader=lambda _prompt: next(commands),
        output_writer=output.append,
    )
    return runtime, "\n".join(output)


def test_compose_shows_one_canonical_door_with_compose_wording() -> None:
    runtime, transcript = run_mode(ResonanceMode.COMPOSE)
    assert runtime.state.visible_paths.count("resonance") == 1
    assert "resonance — shape a resonance invitation" in transcript
    assert "begin/send" not in transcript
    assert "Nothing is sent, uploaded, synchronized, or published automatically" in transcript
    assert "one choice at a time" in transcript
    assert "Use /cancel" in transcript
    assert "No invitation or workspace was created" in transcript


def test_answer_shows_same_door_without_reaching_legacy_flow() -> None:
    runtime, transcript = run_mode(ResonanceMode.ANSWER)
    assert runtime.state.visible_paths.count("resonance") == 1
    assert "resonance — answer the carried resonance" in transcript
    plain = transcript.index("selected carried trace could not safely be opened")
    diagnostic = transcript.index("no authoritative Nexus activation context was supplied")
    assert plain < diagnostic
    assert "Nothing was written" in transcript
    assert "No nearby Token was discovered or substituted" in transcript


def test_blocked_shows_recovery_door_without_compose_or_legacy_flow() -> None:
    runtime, transcript = run_mode(ResonanceMode.BLOCKED_ANSWER_RECOVERY)
    assert runtime.state.visible_paths.count("resonance") == 1
    assert "resonance — the carried invitation needs attention" in transcript
    assert "blocked — recovery guidance available" in transcript
    plain = transcript.index("selected carried trace could not safely be opened")
    diagnostic = transcript.index("original selected Token V2 context")
    assert plain < diagnostic
    assert "No Chamber interaction began. Nothing was written." in transcript
    assert "Nearby Tokens will not be selected automatically" in transcript
    assert "Compose and legacy Resonance flows remain unavailable" in transcript


def test_corrected_entry_uses_injected_classified_adapter_only() -> None:
    commands = iter(("/resonance", "/quit"))
    calls: list[str] = []
    classified = ClassifiedResonanceController(
        ResonanceMode.ANSWER, lambda message: calls.append(message)
    )

    def legacy():
        raise AssertionError("legacy controller was reachable")

    run_nexus_terminal(
        activation_loader=lambda: ActivationStub("return-resonance"),
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


def test_blocked_recovery_remains_one_shot_on_repeated_visits() -> None:
    output: list[str] = []
    prompts: list[str] = []
    controller = ClassifiedResonanceController(
        ResonanceMode.BLOCKED_ANSWER_RECOVERY,
        output_writer=output.append,
        input_reader=lambda prompt: prompts.append(prompt) or "/quit",
    )

    assert not controller().completed
    assert not controller().completed
    transcript = "\n".join(output)
    assert transcript.count("Resonance Chamber — carried resonance unavailable") == 2
    assert transcript.count("No Chamber interaction began. Nothing was written.") == 2
    assert "completed cycle" not in transcript
    assert prompts == []
