from __future__ import annotations

from pathlib import Path
from unittest.mock import Mock, patch

from atrium import ChamberRunResult, ClassifiedResonanceController, ResonanceMode
from atrium.classified_resonance import (
    _ArchiveSurfaceLoadError,
    _SurfacePhase,
)
from chambers.resonance.archive_content import ArchiveContentBlock, ArchiveEntry


def _block_with_entries(*entries: ArchiveEntry) -> ArchiveContentBlock:
    return ArchiveContentBlock(
        format="nexus.chamber-block.v1",
        block_type="archive-content",
        block_id="test-archive",
        target_module="nexus-01",
        target_chamber="resonance",
        schema_version=1,
        title="Test Archive",
        entries=entries,
    )


def test_archive_is_lazy_until_explicit_command() -> None:
    commands = iter(("/look", "/help", "/quit"))
    output: list[str] = []
    controller = ClassifiedResonanceController(
        ResonanceMode.COMPOSE,
        output_writer=output.append,
        input_reader=lambda _prompt: next(commands),
    )

    loader = Mock(
        side_effect=AssertionError("Archive loaded without explicit /archive")
    )
    with patch("atrium.classified_resonance._load_builtin_archive", loader):
        result = controller()

    assert not result.completed
    loader.assert_not_called()
    transcript = "\n".join(output)
    assert "  /archive — open the local read-only Resonance Archive" in transcript


def test_archive_is_available_in_every_resonance_surface_phase() -> None:
    cases = (
        (ResonanceMode.COMPOSE, _SurfacePhase.PRE_RUN),
        (ResonanceMode.ANSWER, _SurfacePhase.PRE_RUN),
        (ResonanceMode.COMPOSE, _SurfacePhase.POST_RUN),
        (ResonanceMode.ANSWER, _SurfacePhase.POST_RUN),
        (ResonanceMode.BLOCKED_ANSWER_RECOVERY, _SurfacePhase.BLOCKED),
    )

    for mode, phase in cases:
        controller = ClassifiedResonanceController(mode)
        if phase is _SurfacePhase.POST_RUN:
            controller._last_completed_result = Mock()
        commands = {
            item.command for item in controller._surface_capabilities(phase)
        }
        assert "/archive" in commands


def test_archive_reads_multiple_entries_before_explicit_back() -> None:
    commands = iter(
        (
            "/archive",
            "/read what-is-a-nexus",
            "/read first-spark-chamber",
            "/back",
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

    result = controller()

    assert not result.completed
    transcript = "\n".join(output)
    assert "Resonance Archive — Origin" in transcript
    assert (
        "Archive entries open only when you choose /read <entry-id>."
        in transcript
    )
    assert "what-is-a-nexus — What is a Nexus?" in transcript
    assert "first-spark-chamber — First Spark Chamber" in transcript
    assert "resonance-as-a-gift — Resonance as a Gift" in transcript
    assert "Archive entry — What is a Nexus?" in transcript
    assert "Archive entry — First Spark Chamber" in transcript
    assert "A Nexus is not a net that holds people together." in transcript
    assert "First Spark is a small puzzle chamber." in transcript
    archive_prose_lines = [
        line
        for line in output
        if line.startswith("  ")
        and " — " not in line
        and not line.lstrip().startswith("/")
    ]
    assert archive_prose_lines
    assert max(map(len, archive_prose_lines)) <= 76
    assert prompts == [
        "resonance> ",
        "resonance|archive> ",
        "resonance|archive> ",
        "resonance|archive> ",
        "resonance> ",
    ]


def test_archive_uses_slash_commands_and_hierarchical_prompt() -> None:
    commands = iter(
        (
            "/archive",
            "what-is-a-nexus",
            "/help",
            "/back",
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

    result = controller()

    assert not result.completed
    transcript = "\n".join(output)
    assert "Unknown Archive command." in transcript
    assert "Archive entry — What is a Nexus?" not in transcript
    assert "Resonance Archive commands" in transcript
    assert "  /look — show the Archive index" in transcript
    assert "  /help — show the commands available here" in transcript
    assert "  /read <entry-id> — read one Archive entry" in transcript
    assert "  /back — return to the Resonance Chamber" in transcript
    assert prompts.count("resonance|archive> ") == 3


def test_archive_help_and_dispatch_share_local_capability_source() -> None:
    commands = iter(("/archive", "/look", "/help", "/back", "/quit"))
    output: list[str] = []
    controller = ClassifiedResonanceController(
        ResonanceMode.COMPOSE,
        output_writer=output.append,
        input_reader=lambda _prompt: next(commands),
    )
    reduced_capabilities = tuple(
        capability
        for capability in controller._archive_capabilities()
        if capability.command != "/look"
    )

    with (
        patch.object(
            controller,
            "_archive_capabilities",
            return_value=reduced_capabilities,
        ),
        patch(
            "atrium.classified_resonance._load_builtin_archive",
            return_value=_block_with_entries(),
        ),
    ):
        result = controller()

    assert not result.completed
    transcript = "\n".join(output)
    assert "Unknown Archive command." in transcript
    assert "  /look — show the Archive index" not in transcript
    assert "  /help — show the commands available here" in transcript
    assert "  /read <entry-id> — read one Archive entry" in transcript
    assert "  /back — return to the Resonance Chamber" in transcript


def test_unknown_archive_entry_stays_inside_archive() -> None:
    commands = iter(
        (
            "/archive",
            "/read missing-entry",
            "/look",
            "/back",
            "/quit",
        )
    )
    output: list[str] = []
    prompts: list[str] = []
    controller = ClassifiedResonanceController(
        ResonanceMode.ANSWER,
        output_writer=output.append,
        input_reader=lambda prompt: prompts.append(prompt) or next(commands),
    )

    result = controller()

    assert not result.completed
    transcript = "\n".join(output)
    assert "That Archive entry is not available." in transcript
    assert transcript.count("Resonance Archive — Origin") == 2
    assert prompts.count("resonance|archive> ") == 3
    assert "Traceback" not in transcript


def test_sealed_archive_entry_never_renders_deeper_material() -> None:
    sealed = ArchiveEntry(
        entry_id="sealed-entry",
        title="Sealed Entry",
        access="sealed",
        poetic_indication=("A public teaser remains.",),
        clear_orientation=("MUST NOT RENDER CLEAR",),
        deeper_trace=("MUST NOT RENDER DEEP",),
    )
    block = _block_with_entries(sealed)
    commands = iter(("/archive", "/read sealed-entry", "/back", "/quit"))
    output: list[str] = []
    controller = ClassifiedResonanceController(
        ResonanceMode.BLOCKED_ANSWER_RECOVERY,
        output_writer=output.append,
        input_reader=lambda _prompt: next(commands),
    )

    with patch(
        "atrium.classified_resonance._load_builtin_archive",
        return_value=block,
    ):
        result = controller()

    assert not result.completed
    transcript = "\n".join(output)
    assert "sealed-entry — Sealed Entry [sealed]" in transcript
    assert "A public teaser remains." in transcript
    assert "This entry remains sealed. No deeper trace is shown." in transcript
    assert "MUST NOT RENDER CLEAR" not in transcript
    assert "MUST NOT RENDER DEEP" not in transcript


def test_invalid_archive_is_calm_and_does_not_block_productive_action() -> None:
    cases = (
        (ResonanceMode.COMPOSE, "/compose", "_run_compose"),
        (ResonanceMode.ANSWER, "/answer", "_run_answer"),
    )

    for mode, action_command, method_name in cases:
        commands = iter(("/archive", action_command))
        output: list[str] = []
        controller = ClassifiedResonanceController(
            mode,
            output_writer=output.append,
            input_reader=lambda _prompt: next(commands),
            nexus_root=Path("/tmp/nexus-invalid-archive"),
        )
        productive = Mock(return_value=ChamberRunResult(completed=True))
        setattr(controller, method_name, productive)

        with patch(
            "atrium.classified_resonance._load_builtin_archive",
            side_effect=_ArchiveSurfaceLoadError("invalid test Block"),
        ):
            result = controller()

        assert result.completed
        productive.assert_called_once_with()
        transcript = "\n".join(output)
        assert "Resonance Archive — unavailable" in transcript
        assert "The local Archive could not be opened safely." in transcript
        assert "Nothing was changed." in transcript
        assert "Traceback" not in transcript
