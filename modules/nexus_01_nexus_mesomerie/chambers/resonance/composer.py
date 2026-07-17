"""Thin integration boundary from Chamber flow to transport artifact."""

from __future__ import annotations

from dataclasses import asdict, dataclass

from return_resonance.resonance_render_bridge import (
    ChamberSelections,
    ResonanceReturnArtifact,
    build_resonance_return_artifact,
)
from return_resonance.token import (
    ResonanceToken,
    ResonanceTokenLoadError,
    validate_originating_wish_word,
)

from .choices import ChoiceCatalog, ChoiceCatalogError, build_v0_1_catalog
from .flow import ChamberIO, ResonanceChamberFlow


@dataclass(frozen=True)
class ComposedResonanceReturn:
    """Explicitly preserve both sides of the Chamber boundary."""

    selections: ChamberSelections
    artifact: ResonanceReturnArtifact


class ResonanceAnswerError(ValueError):
    """Raised when a corrected answer contribution cannot be validated."""


@dataclass(frozen=True)
class AnsweringResonanceContribution:
    """The answering person's response, without Token or route data."""

    image_response_id: str
    scent_response_id: str
    movement_response_id: str
    return_word: str

    def __post_init__(self) -> None:
        catalog = build_v0_1_catalog()
        try:
            image_response_id = catalog.require_choice(
                "image_responses", self.image_response_id
            )
            scent_response_id = catalog.require_choice(
                "scent_responses", self.scent_response_id
            )
            movement_response_id = catalog.require_choice(
                "movement_responses", self.movement_response_id
            )
            return_word = validate_originating_wish_word(self.return_word)
        except (ChoiceCatalogError, ResonanceTokenLoadError) as error:
            raise ResonanceAnswerError(
                str(error).replace("wish_word", "return_word")
            ) from error

        object.__setattr__(self, "image_response_id", image_response_id)
        object.__setattr__(self, "scent_response_id", scent_response_id)
        object.__setattr__(self, "movement_response_id", movement_response_id)
        object.__setattr__(self, "return_word", return_word)


def collect_answering_resonance(
    io: ChamberIO,
    catalog: ChoiceCatalog | None = None,
) -> AnsweringResonanceContribution:
    """Collect only independent response-side choices, without file I/O."""

    active_catalog = catalog if catalog is not None else build_v0_1_catalog()
    try:
        contribution = AnsweringResonanceContribution(
            image_response_id=io.choose(
                "image_response", active_catalog.option_ids("image_responses")
            ),
            scent_response_id=io.choose(
                "scent_response", active_catalog.option_ids("scent_responses")
            ),
            movement_response_id=io.choose(
                "movement_response", active_catalog.option_ids("movement_responses")
            ),
            return_word=io.enter_word("return_word"),
        )
    except ChoiceCatalogError as error:
        raise ResonanceAnswerError(str(error)) from error
    return contribution


def build_answer_resonance_return_artifact(
    token: ResonanceToken,
    contribution: AnsweringResonanceContribution,
) -> ResonanceReturnArtifact:
    """Purely join one validated Token V2 to one validated answer."""

    if token.is_legacy or not token.has_originating_contribution:
        raise ResonanceAnswerError(
            "Corrected ANSWER requires the deliberately selected Resonance Token V2."
        )
    if not isinstance(contribution, AnsweringResonanceContribution):
        raise ResonanceAnswerError(
            "Corrected ANSWER requires a validated answering contribution."
        )

    selections = ChamberSelections(
        image_id=token.image_id,
        scent_id=token.scent_id,
        movement_id=token.movement_id,
        wish_word=token.wish_word,
        **asdict(contribution),
    )
    return build_resonance_return_artifact(token, selections)


def compose_resonance_return(
    token: ResonanceToken,
    io: ChamberIO,
    catalog: ChoiceCatalog | None = None,
) -> ComposedResonanceReturn:
    """Run the Chamber grammar, then join its result to validated route identity.

    This function deliberately does not read or write files, render poetry, match a
    Return Slot, or manage Atrium state. It is only the narrow integration seam
    between the Chamber-owned flow and the shared transport contract.
    """

    active_catalog = catalog if catalog is not None else build_v0_1_catalog()
    selections = ResonanceChamberFlow(active_catalog).run(io)
    artifact = build_resonance_return_artifact(token, selections)
    return ComposedResonanceReturn(selections=selections, artifact=artifact)
