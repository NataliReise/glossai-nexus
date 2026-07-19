from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from unittest.mock import Mock, patch

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
        commands = iter(
            ("/first-spark", "/resonance", "/compose", "/cancel", "/quit")
        )
    else:
        activation = ActivationStub("return-resonance")
        commands = iter(("/resonance", "/answer", "/quit"))
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
    commands = iter(("/resonance", "/answer", "/quit"))
    calls: list[str] = []
    classified = ClassifiedResonanceController(
        ResonanceMode.ANSWER,
        lambda message: calls.append(message),
        input_reader=lambda _prompt: next(commands),
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
            input_reader=lambda _prompt: "/quit",
        )()
        assert not result.completed
    assert set(tmp_path.rglob("*")) == before


def test_fresh_and_blocked_controllers_have_no_retained_corrected_result() -> None:
    for mode in ResonanceMode:
        controller = ClassifiedResonanceController(
            mode,
            output_writer=lambda _message: None,
            input_reader=lambda _prompt: "/quit",
        )
        assert controller._last_completed_result is None
        assert not controller().completed
        assert controller._last_completed_result is None


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


def test_compose_pre_run_is_neutral_until_explicit_compose() -> None:
    commands = iter(
        (
            "/look",
            "/help",
            "/answer",
            "/results",
            "/cancel",
            "/unknown",
            "compose",
            "/quit",
        )
    )
    output: list[str] = []
    prompts: list[str] = []
    controller = ClassifiedResonanceController(
        ResonanceMode.COMPOSE,
        output_writer=output.append,
        input_reader=lambda prompt: prompts.append(prompt) or next(commands),
    )
    productive = Mock(return_value=ChamberRunResult(completed=True))
    controller._run_compose = productive

    assert not controller().completed
    assert controller._last_completed_result is None
    productive.assert_not_called()
    transcript = "\n".join(output)
    assert transcript.count("Resonance Chamber — quiet threshold") == 2
    assert "No productive cycle has begun." in transcript
    assert (
        "No productive choice has been made, and nothing has been written "
        "in this Chamber."
    ) in transcript
    assert "  /compose — begin an originating cycle" in transcript
    assert "  /answer —" not in transcript
    assert "  /results —" not in transcript
    assert "  /cancel —" not in transcript
    assert transcript.count("That action is not available at this threshold.") == 5
    assert set(prompts) == {"resonance> "}

    action = Mock(return_value=ChamberRunResult(completed=True))
    explicit = ClassifiedResonanceController(
        ResonanceMode.COMPOSE,
        output_writer=lambda _message: None,
        input_reader=lambda _prompt: "/compose",
    )
    explicit._run_compose = action
    assert explicit().completed
    action.assert_called_once_with()


def test_answer_pre_run_is_neutral_until_explicit_answer() -> None:
    commands = iter(
        (
            "/look",
            "/help",
            "/compose",
            "/results",
            "/cancel",
            "/unknown",
            "answer",
            "/quit",
        )
    )
    output: list[str] = []
    controller = ClassifiedResonanceController(
        ResonanceMode.ANSWER,
        output_writer=output.append,
        input_reader=lambda _prompt: next(commands),
    )
    with patch(
        "atrium.classified_resonance._load_authoritative_selected_token",
        side_effect=AssertionError("pre-run entry revalidated the selected Token"),
    ):
        assert not controller().completed
    assert controller._last_completed_result is None
    transcript = "\n".join(output)
    assert transcript.count("Resonance Chamber — quiet threshold") == 2
    assert (
        "No productive choice has been made, and nothing has been written "
        "in this Chamber."
    ) in transcript
    assert "  /answer — begin the selected answer cycle" in transcript
    assert "  /compose —" not in transcript
    assert "  /results —" not in transcript
    assert "  /cancel —" not in transcript
    assert transcript.count("That action is not available at this threshold.") == 5

    action = Mock(return_value=ChamberRunResult(completed=True))
    explicit = ClassifiedResonanceController(
        ResonanceMode.ANSWER,
        output_writer=lambda _message: None,
        input_reader=lambda _prompt: "/answer",
    )
    explicit._run_answer = action
    assert explicit().completed
    action.assert_called_once_with()


def test_compose_pre_run_eof_returns_calmly_without_productive_action() -> None:
    output: list[str] = []
    controller = ClassifiedResonanceController(
        ResonanceMode.COMPOSE,
        output_writer=output.append,
        input_reader=lambda _prompt: (_ for _ in ()).throw(EOFError),
    )
    productive = Mock(return_value=ChamberRunResult(completed=True))
    controller._run_compose = productive

    result = controller()

    assert not result.completed
    productive.assert_not_called()
    assert controller._last_completed_result is None
    transcript = "\n".join(output)
    assert "Leaving the Resonance Chamber. Returning safely to the Atrium." in transcript
    assert "Unknown Resonance command." not in transcript
    assert "That action is not available at this threshold." not in transcript
    assert "Traceback" not in transcript


def test_answer_pre_run_eof_returns_without_token_revalidation() -> None:
    output: list[str] = []
    controller = ClassifiedResonanceController(
        ResonanceMode.ANSWER,
        output_writer=output.append,
        input_reader=lambda _prompt: (_ for _ in ()).throw(EOFError),
    )
    productive = Mock(return_value=ChamberRunResult(completed=True))
    controller._run_answer = productive
    token_loader = Mock(
        side_effect=AssertionError("EOF revalidated the selected Token")
    )

    with patch(
        "atrium.classified_resonance._load_authoritative_selected_token",
        token_loader,
    ):
        result = controller()

    assert not result.completed
    productive.assert_not_called()
    token_loader.assert_not_called()
    assert controller._last_completed_result is None
    transcript = "\n".join(output)
    assert "Leaving the Resonance Chamber. Returning safely to the Atrium." in transcript
    assert "Unknown Resonance command." not in transcript
    assert "Traceback" not in transcript
