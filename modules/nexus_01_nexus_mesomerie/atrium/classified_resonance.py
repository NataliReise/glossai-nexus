"""State-specific entry adapters for the corrected Resonance Chamber."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
import secrets
from typing import TYPE_CHECKING

from chambers.resonance import (
    AnsweringResonanceContribution,
    ChamberInteractionCancelled,
    ResonanceAnswerError,
    ResonanceComposeError,
    TerminalChamberIO,
    build_answer_resonance_return_artifact,
    build_resonance_token_v2,
    build_v0_1_catalog,
    collect_answering_resonance,
    compose_originating_resonance,
)
from chambers.resonance.terminal_io import ResonanceGuidanceSession
from return_resonance.artifact_store import (
    ResonanceArtifactStoreError,
    write_resonance_return_artifact,
)
from return_resonance.resonance_render_bridge import ResonanceReturnArtifact
from return_resonance.token import (
    ResonanceToken,
    ResonanceTokenLoadError,
    load_resonance_token,
)

from .resonance_mode import ResonanceMode
from .runtime import ChamberRunResult


if TYPE_CHECKING:
    from resonance_invitation_runtime import (
        InvitationPreparationResult,
        RouteIdentity,
    )


OutputWriter = Callable[[str], None]
InputReader = Callable[[str], str]
ArtifactWriter = Callable[[ResonanceReturnArtifact, str | Path], Path]
InvitationPreparer = Callable[..., "InvitationPreparationResult"]
RouteFactory = Callable[[], "RouteIdentity"]


@dataclass(frozen=True)
class CompletedComposeResult:
    """Latest successfully published corrected COMPOSE result."""

    token: ResonanceToken
    invitation_path: Path
    private_workspace_path: Path


@dataclass(frozen=True)
class CompletedAnswerResult:
    """Latest successfully written corrected ANSWER result."""

    artifact: ResonanceReturnArtifact
    artifact_path: Path
    carried_public_safe_label: str


CompletedCorrectedResult = CompletedComposeResult | CompletedAnswerResult


class _SurfacePhase(Enum):
    PRE_RUN = "pre-run"
    POST_RUN = "post-run"
    BLOCKED = "blocked"


@dataclass(frozen=True)
class _SurfaceCapability:
    command: str
    help_text: str


DOOR_LABELS = {
    ResonanceMode.COMPOSE: "shape a resonance invitation",
    ResonanceMode.ANSWER: "answer the carried resonance",
    ResonanceMode.BLOCKED_ANSWER_RECOVERY: "the carried invitation needs attention",
}


COMPOSE_THRESHOLD = (
    "Shape a Resonance invitation one choice at a time: an image, a scent, "
    "a movement, and one wish word.\n"
    "No private explanation is requested, and private reasons are not stored.\n"
    "This Chamber creates local material only. Nothing is sent, uploaded, "
    "synchronized, or published automatically. "
    "Local outputs are created only after your explicit confirmation.\n"
    "Use /cancel at any interactive prompt to end the current Resonance cycle "
    "safely without creating a new output. At yes/no prompts, you may also "
    "answer no. At a destination prompt, blank input also cancels creation. "
    "Full-cycle cancellation returns safely to the Atrium. You may leave "
    "without creating anything."
)


ANSWER_THRESHOLD = (
    "A carried Resonance contribution is present. You may answer it in your "
    "own way, one response at a time: three responses and one return word.\n"
    "No private explanation is requested, and private reasons are not stored.\n"
    "This Chamber creates local material only. Nothing is returned, sent, "
    "uploaded, synchronized, or published automatically. A Return Artifact is "
    "written only after your explicit "
    "confirmation and a valid local destination.\n"
    "Use /cancel at any interactive prompt to end the current Resonance cycle "
    "safely without creating a new output. At yes/no prompts, you may also "
    "answer no. At a destination prompt, blank input also cancels creation. "
    "Full-cycle cancellation returns safely to the Atrium. You may leave "
    "without creating anything."
)


def resonance_door_label(mode: ResonanceMode) -> str:
    """Return mode-specific wording without changing Chamber identity."""

    return DOOR_LABELS[mode]


@dataclass
class ClassifiedResonanceController:
    """Keep corrected modes away from the legacy one-person controller."""

    mode: ResonanceMode
    output_writer: OutputWriter = print
    input_reader: InputReader = input
    nexus_root: Path | None = None
    artifact_writer: ArtifactWriter = write_resonance_return_artifact
    invitation_preparer: InvitationPreparer | None = None
    route_factory: RouteFactory | None = None
    _last_completed_result: CompletedCorrectedResult | None = field(
        default=None,
        init=False,
        repr=False,
    )

    def __call__(self) -> ChamberRunResult:
        if self._last_completed_result is not None and self.mode in {
            ResonanceMode.COMPOSE,
            ResonanceMode.ANSWER,
        }:
            return self._run_post_run()

        if self.mode in {ResonanceMode.COMPOSE, ResonanceMode.ANSWER}:
            return self._run_pre_run()

        return self._run_surface(_SurfacePhase.BLOCKED)

    def _run_pre_run(self) -> ChamberRunResult:
        return self._run_surface(_SurfacePhase.PRE_RUN)

    def _run_post_run(self) -> ChamberRunResult:
        return self._run_surface(_SurfacePhase.POST_RUN)

    def _run_surface(self, phase: _SurfacePhase) -> ChamberRunResult:
        self._display_surface(phase)
        capabilities = self._surface_capabilities(phase)
        visible_commands = frozenset(
            capability.command for capability in capabilities
        )
        while True:
            try:
                command = self.input_reader("resonance> ").strip().casefold()
            except (KeyboardInterrupt, EOFError):
                self.output_writer("")
                return self._leave_surface()

            if not command:
                continue
            if command == "help" and phase is _SurfacePhase.POST_RUN:
                command = "/help"
            if command not in visible_commands:
                self._display_unknown_surface_command(phase)
                continue
            if command == "/look":
                self._display_surface(phase)
                continue
            if command == "/help":
                self._display_surface_help(capabilities)
                continue
            if command == "/trace":
                self._display_post_run_trace()
                continue
            if command == "/results":
                self._display_results()
                continue
            if command == "/quit":
                return self._leave_surface()
            if command == "/compose":
                return self._run_compose()
            if command == "/answer":
                return self._run_answer()

            raise AssertionError(f"Unhandled Resonance Surface command: {command}")

    def _surface_capabilities(
        self,
        phase: _SurfacePhase,
    ) -> tuple[_SurfaceCapability, ...]:
        state_label = {
            _SurfacePhase.PRE_RUN: "quiet",
            _SurfacePhase.POST_RUN: "completed",
            _SurfacePhase.BLOCKED: "blocked",
        }[phase]
        capabilities = [
            _SurfaceCapability(
                "/look", f"perceive the {state_label} Chamber state"
            ),
            _SurfaceCapability("/help", "show the commands available here"),
        ]
        if phase is _SurfacePhase.POST_RUN:
            capabilities.append(
                _SurfaceCapability("/trace", "receive a gentle next trace")
            )
            if self._last_completed_result is not None:
                result_label = (
                    "cycle" if self.mode is ResonanceMode.COMPOSE else "answer"
                )
                capabilities.append(
                    _SurfaceCapability(
                        "/results",
                        f"view this session's most recent completed {result_label}",
                    )
                )
        if phase is not _SurfacePhase.BLOCKED and self.mode is ResonanceMode.COMPOSE:
            action_text = (
                "begin an originating cycle"
                if phase is _SurfacePhase.PRE_RUN
                else "begin another independent originating cycle"
            )
            capabilities.append(_SurfaceCapability("/compose", action_text))
        elif self.mode is ResonanceMode.ANSWER and phase is _SurfacePhase.PRE_RUN:
            capabilities.append(
                _SurfaceCapability("/answer", "begin the selected answer cycle")
            )
        capabilities.append(_SurfaceCapability("/quit", "return to the Atrium"))
        return tuple(capabilities)

    def _display_surface(self, phase: _SurfacePhase) -> None:
        if phase is _SurfacePhase.PRE_RUN:
            self._display_pre_run()
            return
        if phase is _SurfacePhase.BLOCKED:
            self._display_blocked()
            return
        self._display_post_run()

    def _display_pre_run(self) -> None:
        self.output_writer("Resonance Chamber — quiet threshold")
        self.output_writer("")
        self.output_writer("The Chamber is open. No productive cycle has begun.")
        self.output_writer(
            "No productive choice has been made, and nothing has been written "
            "in this Chamber."
        )

    def _display_blocked(self) -> None:
        self.output_writer("Resonance Chamber — carried resonance unavailable")
        self.output_writer("")
        self.output_writer(
            "The selected carried trace could not safely be opened."
        )
        self.output_writer(
            "Its original selected Token V2 context is missing, invalid, "
            "altered, or mismatched."
        )
        self.output_writer(
            "Nothing was written, and no nearby Token will be selected "
            "automatically."
        )
        self.output_writer(
            "Restore the selected activation context and Token copy from a "
            "trusted backup, or prepare a fresh Nexus activation."
        )
        self.output_writer(
            "Compose and legacy Resonance flows remain unavailable."
        )

    def _display_surface_help(
        self,
        capabilities: tuple[_SurfaceCapability, ...],
    ) -> None:
        self.output_writer("Resonance Chamber commands")
        for capability in capabilities:
            self.output_writer(
                f"  {capability.command} — {capability.help_text}"
            )

    def _leave_surface(self) -> ChamberRunResult:
        self.output_writer(
            "Leaving the Resonance Chamber. Returning safely to the Atrium."
        )
        return ChamberRunResult(completed=False)

    def _display_unknown_surface_command(self, phase: _SurfacePhase) -> None:
        if phase is _SurfacePhase.PRE_RUN:
            self.output_writer("That action is not available at this threshold.")
        else:
            self.output_writer("Unknown Resonance command.")
        self.output_writer("Use /help to see the commands available here.")

    def _display_post_run(self) -> None:
        if self.mode is ResonanceMode.COMPOSE:
            self.output_writer("Resonance Chamber — completed cycle")
            self.output_writer("")
            self.output_writer("One originating cycle is complete.")
            self.output_writer(
                "The Chamber remains available, but no new cycle has begun."
            )
            self.output_writer(
                "A completed originating trace rests quietly in the Chamber."
            )
            return

        self.output_writer("Resonance Chamber — completed answer")
        self.output_writer("")
        self.output_writer("This answer cycle is complete.")
        self.output_writer("No second answer has begun from the selected Token.")
        self.output_writer(
            "A completed answering trace rests quietly in the Chamber."
        )

    def _display_post_run_trace(self) -> None:
        if self.mode is ResonanceMode.COMPOSE:
            self.output_writer(
                "  The completed invitation rests where you placed it. Another "
                "originating trace begins only if you choose /compose."
            )
            return
        self.output_writer(
            "  This answer remains with its selected Token. Another answer begins "
            "only from another deliberately selected Token context."
        )

    def _display_results(self) -> None:
        result = self._last_completed_result
        if result is None:
            return

        catalog = build_v0_1_catalog()
        if isinstance(result, CompletedComposeResult):
            self._display_compose_results(result, catalog)
            return
        self._display_answer_results(result, catalog)

    def _display_compose_results(self, result, catalog) -> None:
        token = result.token
        self.output_writer(
            "Resonance results — most recent originating cycle in this session"
        )
        self.output_writer(
            "  Earlier local outputs remain separate and unchanged."
        )
        self.output_writer("")
        self.output_writer("[private local]")
        self.output_writer(
            f"    Image: {_choice_label(catalog, 'images', token.image_id)}"
        )
        self.output_writer(
            f"    Scent: {_choice_label(catalog, 'scents', token.scent_id)}"
        )
        self.output_writer(
            "    Movement: "
            + _choice_label(catalog, "movements", token.movement_id)
        )
        self.output_writer(f"    Wish word: {token.wish_word}")
        self.output_writer("")
        self.output_writer("[public-safe]")
        self.output_writer(
            "    No public-safe summary was created for this cycle."
        )
        self.output_writer("")
        self.output_writer("[local path]")
        invitation_available = result.invitation_path.is_dir()
        workspace_available = result.private_workspace_path.is_dir()
        self.output_writer(
            "    Travelling invitation: "
            f"{result.invitation_path} — {_path_status(invitation_available)}"
        )
        self.output_writer(
            "    Private Return Workspace: "
            f"{result.private_workspace_path} — {_path_status(workspace_available)}"
        )
        if not invitation_available or not workspace_available:
            self.output_writer("  No filesystem search was performed.")

    def _display_answer_results(self, result, catalog) -> None:
        artifact = result.artifact
        self.output_writer(
            "Resonance results — most recent answer cycle in this session"
        )
        self.output_writer(
            "  Earlier local outputs remain separate and unchanged."
        )
        self.output_writer("")
        self.output_writer("[private local]")
        self.output_writer(
            "    Carried image: "
            + _choice_label(catalog, "images", artifact.image_id)
        )
        self.output_writer(
            "    Carried scent: "
            + _choice_label(catalog, "scents", artifact.scent_id)
        )
        self.output_writer(
            "    Carried movement: "
            + _choice_label(catalog, "movements", artifact.movement_id)
        )
        self.output_writer(f"    Wish word: {artifact.wish_word}")
        self.output_writer(
            "    Image response: "
            + _choice_label(
                catalog, "image_responses", artifact.image_response_id
            )
        )
        self.output_writer(
            "    Scent response: "
            + _choice_label(
                catalog, "scent_responses", artifact.scent_response_id
            )
        )
        self.output_writer(
            "    Movement response: "
            + _choice_label(
                catalog, "movement_responses", artifact.movement_response_id
            )
        )
        self.output_writer(f"    Return word: {artifact.return_word}")
        self.output_writer("")
        self.output_writer("[public-safe]")
        if result.carried_public_safe_label:
            self.output_writer(
                f"    Carried label: {result.carried_public_safe_label}"
            )
        else:
            self.output_writer(
                "    No public-safe summary was attached to the carried resonance."
            )
        self.output_writer("")
        self.output_writer("[local path]")
        artifact_available = result.artifact_path.is_file()
        self.output_writer(
            f"    Return Artifact: {result.artifact_path} — "
            f"{_path_status(artifact_available)}"
        )
        if not artifact_available:
            self.output_writer("  No filesystem search was performed.")

    def _run_compose(self) -> ChamberRunResult:
        from resonance_invitation_runtime import (
            InvitationPublicationError,
            generate_route_identity,
            prepare_resonance_invitation,
        )

        self.output_writer("Resonance Chamber — shape a resonance invitation")
        self.output_writer(COMPOSE_THRESHOLD)
        catalog = build_v0_1_catalog()
        guidance = ResonanceGuidanceSession(
            "compose",
            self.output_writer,
            allow_cancel=True,
            input_fn=self.input_reader,
        )
        io = TerminalChamberIO(
            catalog,
            input_fn=self.input_reader,
            output_fn=self.output_writer,
            allow_cancel=True,
            information_handler=guidance.handle,
            before_prompt=guidance.before_prompt,
        )
        try:
            contribution = compose_originating_resonance(io, catalog)
        except ChamberInteractionCancelled:
            _display_compose_cancelled(self.output_writer)
            return ChamberRunResult(completed=False)
        except ResonanceComposeError as error:
            _display_compose_failure(
                self.output_writer,
                f"The originating contribution is not valid: {error}",
            )
            return ChamberRunResult(completed=False)

        self.output_writer("")
        self.output_writer("Resonance invitation shaped")
        self.output_writer(
            "The Chamber has gathered your originating contribution. "
            "No local output exists yet."
        )
        self.output_writer(
            "Creation still requires your explicit confirmation. The travelling "
            "invitation and private Return Workspace will remain separate."
        )
        _display_compose_summary(contribution, catalog, self.output_writer)
        if not _confirm_compose_publication(self.input_reader, self.output_writer):
            _display_compose_cancelled(self.output_writer)
            return ChamberRunResult(completed=False)

        invitation_root_text = self.input_reader(
            "Parent directory for the travelling invitation (blank to cancel): "
        ).strip()
        if not invitation_root_text or invitation_root_text.casefold() == "/cancel":
            _display_compose_cancelled(self.output_writer)
            return ChamberRunResult(completed=False)
        private_root_text = self.input_reader(
            "Parent directory for the private Return Workspace (blank to cancel): "
        ).strip()
        if not private_root_text or private_root_text.casefold() == "/cancel":
            _display_compose_cancelled(self.output_writer)
            return ChamberRunResult(completed=False)

        invitation_root = Path(invitation_root_text).expanduser()
        private_root = Path(private_root_text).expanduser()
        nexus_root = (
            self.nexus_root or Path(__file__).resolve().parents[1]
        ).expanduser().resolve()
        if any(
            destination.resolve().is_relative_to(nexus_root)
            for destination in (invitation_root, private_root)
        ):
            _display_compose_failure(
                self.output_writer,
                "Publication destinations must remain outside the travelling "
                "Nexus carrier.",
            )
            return ChamberRunResult(completed=False)

        route_factory = self.route_factory or generate_route_identity
        invitation_preparer = (
            self.invitation_preparer or prepare_resonance_invitation
        )
        route = route_factory()
        try:
            token = build_resonance_token_v2(
                contribution,
                module_id=route.module_id,
                layer_id=route.layer_id,
                origin_trace_id=route.origin_trace_id,
                return_slot_id=route.return_slot_id,
                package_id=route.package_id,
            )
            publication = invitation_preparer(
                token,
                invitation_root=invitation_root,
                private_root=private_root,
                forbidden_root=nexus_root,
            )
        except (InvitationPublicationError, ResonanceComposeError, OSError) as error:
            _display_compose_failure(
                self.output_writer,
                f"Resonance invitation publication failed: {error}",
            )
            return ChamberRunResult(completed=False)

        self._last_completed_result = CompletedComposeResult(
            token=publication.token,
            invitation_path=publication.invitation_path,
            private_workspace_path=publication.private_workspace_path,
        )

        self.output_writer("")
        self.output_writer("Local creation complete")
        self.output_writer(
            "The travelling invitation and private Return Workspace were created "
            "as two separate local outputs."
        )
        self.output_writer("They remain local.")
        self.output_writer("")
        self.output_writer("Local paths")
        self.output_writer(
            f"Travelling Resonance invitation: {publication.invitation_path}"
        )
        self.output_writer(
            f"Private Return Workspace: {publication.private_workspace_path}"
        )
        self.output_writer("")
        self.output_writer("Public / private boundary")
        self.output_writer(
            "The travelling invitation may be carried. Keep the private Return "
            "Workspace with the originating person."
        )
        self.output_writer("")
        self.output_writer("Optional manual carrying")
        self.output_writer(
            "If you choose to carry this invitation, transfer it manually. "
            "Nothing requires you to carry, forward, publish, or share it."
        )
        self.output_writer(
            "Nexus 01 does not send, upload, synchronize, or publish files. The "
            "invitation does not choose the recipient's activation mode."
        )
        self.output_writer("")
        self.output_writer("Resonance cycle complete")
        self.output_writer(
            "The travelling invitation and private Return Workspace were created "
            "and remain separate local outputs."
        )
        self.output_writer("This cycle will not begin again automatically.")
        self.output_writer(
            "Return through /resonance whenever you wish to revisit the Chamber."
        )
        self.output_writer(
            "There, /compose can begin another independent invitation."
        )
        return ChamberRunResult(completed=True)

    def _run_answer(self) -> ChamberRunResult:
        self.output_writer("Resonance Chamber — answer the carried resonance")
        if self.nexus_root is None:
            _display_answer_open_failure(
                self.output_writer,
                "ANSWER cannot begin because no authoritative Nexus activation "
                "context was supplied.",
            )
            return ChamberRunResult(completed=False)

        try:
            token = _load_authoritative_selected_token(self.nexus_root)
        except (ResonanceAnswerError, ResonanceTokenLoadError) as error:
            _display_answer_open_failure(
                self.output_writer,
                f"ANSWER cannot begin: {error}",
            )
            return ChamberRunResult(completed=False)

        self.output_writer(ANSWER_THRESHOLD)
        catalog = build_v0_1_catalog()
        _display_originating_contribution(token, catalog, self.output_writer)
        guidance = ResonanceGuidanceSession(
            "answer",
            self.output_writer,
            allow_cancel=True,
            input_fn=self.input_reader,
        )
        io = TerminalChamberIO(
            catalog,
            input_fn=self.input_reader,
            output_fn=self.output_writer,
            allow_cancel=True,
            information_handler=guidance.handle,
            before_prompt=guidance.before_prompt,
        )
        try:
            contribution = collect_answering_resonance(io, catalog)
        except ChamberInteractionCancelled:
            _display_answer_cancelled(self.output_writer)
            return ChamberRunResult(completed=False)
        except ResonanceAnswerError as error:
            _display_answer_creation_failure(
                self.output_writer,
                f"The answer is not valid: {error}",
            )
            return ChamberRunResult(completed=False)

        self.output_writer("")
        self.output_writer("Answer shaped")
        self.output_writer(
            "The Chamber has gathered your answer. No Return Artifact exists yet."
        )
        self.output_writer(
            "Creation requires your explicit confirmation and a valid local destination."
        )
        _display_answer_confirmation(contribution, catalog, self.output_writer)
        if not _confirm_publication(self.input_reader, self.output_writer):
            _display_answer_cancelled(self.output_writer)
            return ChamberRunResult(completed=False)

        parent_text = self.input_reader(
            "Parent directory for the Return Artifact (blank to cancel): "
        ).strip()
        if not parent_text or parent_text.casefold() == "/cancel":
            _display_answer_cancelled(self.output_writer)
            return ChamberRunResult(completed=False)

        parent = Path(parent_text).expanduser()
        nexus_root = self.nexus_root.expanduser().resolve()
        if not parent.is_dir():
            _display_answer_creation_failure(
                self.output_writer,
                "The Return Artifact destination must be an existing directory.",
            )
            return ChamberRunResult(completed=False)
        parent = parent.resolve()
        if parent.is_relative_to(nexus_root):
            _display_answer_creation_failure(
                self.output_writer,
                "The Return Artifact destination must remain outside the "
                "travelling Nexus carrier.",
            )
            return ChamberRunResult(completed=False)

        artifact = build_answer_resonance_return_artifact(token, contribution)
        try:
            destination = _unused_return_artifact_path(parent)
            published = self.artifact_writer(artifact, destination)
        except ResonanceArtifactStoreError as error:
            _display_answer_creation_failure(self.output_writer, str(error))
            return ChamberRunResult(completed=False)

        self._last_completed_result = CompletedAnswerResult(
            artifact=artifact,
            artifact_path=published,
            carried_public_safe_label=token.public_safe_label,
        )

        self.output_writer("")
        self.output_writer("Local creation complete")
        self.output_writer("The Return Artifact was created and remains local.")
        self.output_writer("")
        self.output_writer("Local path")
        self.output_writer(f"Return Artifact: {published}")
        self.output_writer("")
        self.output_writer("Optional manual return")
        self.output_writer(
            "If you choose to return this Artifact, transfer the JSON file manually. "
            "Nothing requires you to return, publish, or share it."
        )
        self.output_writer(
            "Nexus 01 does not send, upload, synchronize, or publish it."
        )
        self.output_writer("")
        self.output_writer("Resonance cycle complete")
        self.output_writer("The Return Artifact was created and remains local.")
        self.output_writer("This answer cycle will not begin again automatically.")
        self.output_writer(
            "Another answer requires another deliberately selected Token context."
        )
        return ChamberRunResult(completed=True)


def _display_compose_cancelled(output_writer: OutputWriter) -> None:
    output_writer("")
    output_writer("Local creation cancelled")
    output_writer("Nothing was written. No invitation or workspace was created.")
    output_writer("The Resonance invitation remains unfinished.")
    output_writer("Returning safely to the Atrium.")


def _display_compose_failure(output_writer: OutputWriter, detail: str) -> None:
    output_writer("")
    output_writer("The local invitation and private workspace were not created.")
    output_writer(
        "Nothing from this attempt was kept. Existing material was not replaced."
    )
    output_writer("The Resonance invitation remains unfinished.")
    output_writer("Returning safely to the Atrium.")
    output_writer("")
    output_writer(f"Technical detail: {detail}")
    output_writer("No partial invitation or private workspace was kept.")


def _display_answer_open_failure(output_writer: OutputWriter, detail: str) -> None:
    output_writer("The selected carried trace could not safely be opened.")
    output_writer("No Chamber interaction began. Nothing was written.")
    output_writer(
        "Return safely to the Atrium, then restore the deliberately selected "
        "Token V2 context or choose another explicit activation path."
    )
    output_writer("No nearby Token was discovered or substituted.")
    output_writer("")
    output_writer(f"Technical detail: {detail}")


def _display_answer_cancelled(output_writer: OutputWriter) -> None:
    output_writer("")
    output_writer("Local creation cancelled")
    output_writer("Nothing was written. No Return Artifact was created.")
    output_writer("The answer route remains unfinished.")
    output_writer("Returning safely to the Atrium.")


def _display_answer_creation_failure(
    output_writer: OutputWriter,
    detail: str,
) -> None:
    output_writer("")
    output_writer("The local Return Artifact was not created.")
    output_writer("Nothing was written. Existing material was not replaced.")
    output_writer("The answer route remains unfinished.")
    output_writer("Returning safely to the Atrium.")
    output_writer("")
    output_writer(f"Technical detail: {detail}")


def _load_authoritative_selected_token(nexus_root: Path) -> ResonanceToken:
    """Revalidate activation, then load only its canonical selected Token copy."""

    # Local imports avoid coupling activation startup to Chamber implementation.
    from recipient_activation import (
        RecipientActivationError,
        classify_runtime_interpretation,
        paths_for_nexus,
    )

    try:
        mode = classify_runtime_interpretation(nexus_root=nexus_root)
    except RecipientActivationError as error:
        raise ResonanceAnswerError(str(error)) from error
    if mode is not ResonanceMode.ANSWER:
        raise ResonanceAnswerError(
            "the completed activation no longer has a valid selected Token V2 context."
        )
    token = load_resonance_token(paths_for_nexus(nexus_root).selected_token)
    if token.is_legacy or not token.has_originating_contribution:
        raise ResonanceAnswerError(
            "the selected invitation is not a Resonance Token V2."
        )
    return token


def _display_originating_contribution(token, catalog, output_writer) -> None:
    output_writer("")
    output_writer("Carried Resonance contribution")
    if token.public_safe_label:
        output_writer(f"From: {token.public_safe_label}")
    output_writer(f"Image: {_choice_label(catalog, 'images', token.image_id)}")
    output_writer(f"Scent: {_choice_label(catalog, 'scents', token.scent_id)}")
    output_writer(
        f"Movement: {_choice_label(catalog, 'movements', token.movement_id)}"
    )
    output_writer(f"Wish word: {token.wish_word}")


def _display_answer_confirmation(contribution, catalog, output_writer) -> None:
    lookup = {
        option.id: option.label
        for kind in ("image_responses", "scent_responses", "movement_responses")
        for option in getattr(catalog, kind)
    }
    output_writer("")
    output_writer("Review your answer")
    output_writer(f"Image response: {lookup[contribution.image_response_id]}")
    output_writer(f"Scent response: {lookup[contribution.scent_response_id]}")
    output_writer(f"Movement response: {lookup[contribution.movement_response_id]}")
    output_writer(f"Return word: {contribution.return_word}")


def _display_compose_summary(contribution, catalog, output_writer) -> None:
    output_writer("")
    output_writer("Your originating resonance — review")
    output_writer(
        f"Image: {_choice_label(catalog, 'images', contribution.image_id)}"
    )
    output_writer(
        f"Scent: {_choice_label(catalog, 'scents', contribution.scent_id)}"
    )
    output_writer(
        "Movement: "
        + _choice_label(catalog, "movements", contribution.movement_id)
    )
    output_writer(f"Wish word: {contribution.wish_word}")


def _choice_label(catalog, kind: str, choice_id: str) -> str:
    return next(
        option.label for option in getattr(catalog, kind) if option.id == choice_id
    )


def _path_status(available: bool) -> str:
    if available:
        return "available"
    return "no longer available at the known location"


_RETURN_ARTIFACT_NAME_ATTEMPTS = 8


def _unused_return_artifact_path(parent: Path) -> Path:
    for _attempt in range(_RETURN_ARTIFACT_NAME_ATTEMPTS):
        opaque_id = secrets.token_hex(12)
        candidate = parent / f"n01-return-artifact-{opaque_id}.json"
        if not candidate.exists() and not candidate.is_symlink():
            return candidate
    raise ResonanceArtifactStoreError(
        "Could not choose an unused Return Artifact filename. Nothing was written."
    )


def _confirm_compose_publication(
    input_reader: InputReader,
    output_writer: OutputWriter,
) -> bool:
    while True:
        answer = input_reader(
            "Create the travelling invitation and private workspace? [yes/no]: "
        ).strip().casefold()
        if answer in {"yes", "y"}:
            return True
        if answer in {"no", "n", "cancel", "q", "/cancel"}:
            return False
        output_writer("Please answer yes or no.")


def _confirm_publication(input_reader: InputReader, output_writer: OutputWriter) -> bool:
    while True:
        answer = (
            input_reader("Create this Return Artifact? [yes/no]: ")
            .strip()
            .casefold()
        )
        if answer in {"yes", "y"}:
            return True
        if answer in {"no", "n", "cancel", "q", "/cancel"}:
            return False
        output_writer("Please answer yes or no.")
