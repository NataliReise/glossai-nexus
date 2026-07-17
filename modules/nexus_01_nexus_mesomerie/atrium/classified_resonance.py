"""State-specific entry adapters for the corrected Resonance Chamber."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
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


DOOR_LABELS = {
    ResonanceMode.COMPOSE: "begin/send a resonance",
    ResonanceMode.ANSWER: "answer the carried resonance",
    ResonanceMode.BLOCKED_ANSWER_RECOVERY: "the carried invitation needs attention",
}


def resonance_door_label(mode: ResonanceMode) -> str:
    """Return mode-specific wording without changing Chamber identity."""

    return DOOR_LABELS[mode]


@dataclass(frozen=True)
class ClassifiedResonanceController:
    """Keep corrected modes away from the legacy one-person controller."""

    mode: ResonanceMode
    output_writer: OutputWriter = print
    input_reader: InputReader = input
    nexus_root: Path | None = None
    artifact_writer: ArtifactWriter = write_resonance_return_artifact
    invitation_preparer: InvitationPreparer | None = None
    route_factory: RouteFactory | None = None

    def __call__(self) -> ChamberRunResult:
        if self.mode is ResonanceMode.COMPOSE:
            return self._run_compose()
        elif self.mode is ResonanceMode.ANSWER:
            return self._run_answer()
        else:
            self.output_writer(
                "Resonance Chamber — the carried invitation needs attention"
            )
            self.output_writer(
                "This activation expects its original selected Token V2 context, "
                "but that package-relative context is missing, invalid, altered, "
                "or mismatched."
            )
            self.output_writer(
                "Restore the selected activation context and Token copy from a "
                "trusted backup, or prepare a fresh Nexus activation. Nearby Tokens "
                "will not be selected automatically."
            )
            self.output_writer("Compose and legacy Resonance flows remain unavailable.")
        return ChamberRunResult(completed=False)

    def _run_compose(self) -> ChamberRunResult:
        from resonance_invitation_runtime import (
            InvitationPublicationError,
            generate_route_identity,
            prepare_resonance_invitation,
        )

        self.output_writer("Resonance Chamber — begin/send a resonance")
        catalog = build_v0_1_catalog()
        io = TerminalChamberIO(
            catalog,
            input_fn=self.input_reader,
            output_fn=self.output_writer,
            allow_cancel=True,
        )
        try:
            contribution = compose_originating_resonance(io, catalog)
        except ChamberInteractionCancelled:
            self.output_writer("Compose cancelled. No invitation or workspace was created.")
            return ChamberRunResult(completed=False)
        except ResonanceComposeError as error:
            self.output_writer(f"The originating contribution is not valid: {error}")
            self.output_writer("No invitation or workspace was created.")
            return ChamberRunResult(completed=False)

        _display_compose_summary(contribution, catalog, self.output_writer)
        if not _confirm_compose_publication(self.input_reader, self.output_writer):
            self.output_writer("Compose cancelled. No invitation or workspace was created.")
            return ChamberRunResult(completed=False)

        invitation_root_text = self.input_reader(
            "Parent directory for the travelling invitation (blank to cancel): "
        ).strip()
        if not invitation_root_text:
            self.output_writer("Compose cancelled. No invitation or workspace was created.")
            return ChamberRunResult(completed=False)
        private_root_text = self.input_reader(
            "Parent directory for the private Return Workspace (blank to cancel): "
        ).strip()
        if not private_root_text:
            self.output_writer("Compose cancelled. No invitation or workspace was created.")
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
            self.output_writer(
                "Publication destinations must remain outside the travelling "
                "Nexus carrier. No output was created."
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
            self.output_writer(f"Resonance invitation publication failed: {error}")
            self.output_writer(
                "No partial invitation or private workspace was kept."
            )
            return ChamberRunResult(completed=False)

        self.output_writer(
            f"Travelling Resonance invitation: {publication.invitation_path}"
        )
        self.output_writer(
            f"Private Return Workspace: {publication.private_workspace_path}"
        )
        self.output_writer(
            "Transfer the invitation manually if you choose. Keep the private "
            "Return Workspace with the originating person."
        )
        self.output_writer(
            "Nexus 01 does not send or synchronize files automatically. The "
            "invitation does not choose the recipient's activation mode."
        )
        return ChamberRunResult(completed=True)

    def _run_answer(self) -> ChamberRunResult:
        self.output_writer("Resonance Chamber — answer the carried resonance")
        if self.nexus_root is None:
            self.output_writer(
                "ANSWER cannot begin because no authoritative Nexus activation "
                "context was supplied."
            )
            return ChamberRunResult(completed=False)

        try:
            token = _load_authoritative_selected_token(self.nexus_root)
        except (ResonanceAnswerError, ResonanceTokenLoadError) as error:
            self.output_writer(f"ANSWER cannot begin: {error}")
            self.output_writer(
                "Restore the deliberately selected Token V2 context; no nearby "
                "Token will be substituted."
            )
            return ChamberRunResult(completed=False)

        catalog = build_v0_1_catalog()
        _display_originating_contribution(token, catalog, self.output_writer)
        io = TerminalChamberIO(
            catalog,
            input_fn=self.input_reader,
            output_fn=self.output_writer,
            allow_cancel=True,
        )
        try:
            contribution = collect_answering_resonance(io, catalog)
        except ChamberInteractionCancelled:
            self.output_writer("Answer cancelled. No Return Artifact was created.")
            return ChamberRunResult(completed=False)
        except ResonanceAnswerError as error:
            self.output_writer(f"The answer is not valid: {error}")
            self.output_writer("No Return Artifact was created.")
            return ChamberRunResult(completed=False)

        _display_answer_confirmation(contribution, catalog, self.output_writer)
        if not _confirm_publication(self.input_reader, self.output_writer):
            self.output_writer("Answer cancelled. No Return Artifact was created.")
            return ChamberRunResult(completed=False)

        destination_text = self.input_reader(
            "Local path for the Return Artifact (blank to cancel): "
        ).strip()
        if not destination_text:
            self.output_writer("Answer cancelled. No Return Artifact was created.")
            return ChamberRunResult(completed=False)

        artifact = build_answer_resonance_return_artifact(token, contribution)
        try:
            published = self.artifact_writer(
                artifact, Path(destination_text).expanduser()
            )
        except ResonanceArtifactStoreError as error:
            self.output_writer(str(error))
            self.output_writer("No existing Artifact was changed or replaced.")
            return ChamberRunResult(completed=False)

        self.output_writer(f"Return Artifact created locally: {published}")
        self.output_writer(
            "Return this JSON file manually to the originating person. "
            "Nexus 01 does not send or synchronize it."
        )
        return ChamberRunResult(completed=True)


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
    output_writer("Carried originating contribution")
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
    output_writer("Your answer")
    output_writer(f"Image response: {lookup[contribution.image_response_id]}")
    output_writer(f"Scent response: {lookup[contribution.scent_response_id]}")
    output_writer(f"Movement response: {lookup[contribution.movement_response_id]}")
    output_writer(f"Return word: {contribution.return_word}")


def _display_compose_summary(contribution, catalog, output_writer) -> None:
    output_writer("")
    output_writer("Your originating resonance")
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
        if answer in {"no", "n", "cancel", "q"}:
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
        if answer in {"no", "n", "cancel", "q"}:
            return False
        output_writer("Please answer yes or no.")
