"""Tests for composing Nexus 01 return artifacts from resonance tokens."""

from __future__ import annotations

import json
from pathlib import Path
import sys

NEXUS_01_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(NEXUS_01_ROOT))

from return_resonance import (
    MatchStatus,
    ResonanceExpression,
    ReturnArtifactWriteError,
    compose_return_artifact,
    load_resonance_token,
    load_return_slots,
    match_return_artifact,
    parse_return_artifact,
)

TEMPLATE_PATH = NEXUS_01_ROOT / "templates" / "resonance_token.template.json"
DEMO_SLOT_PATH = NEXUS_01_ROOT / "examples" / "return_slot.demo.json"


def make_demo_token(tmp_path: Path):
    data = json.loads(TEMPLATE_PATH.read_text(encoding="utf-8"))
    data.update(
        {
            "origin_trace_id": "n01-demo-origin-7kq2",
            "return_slot_id": "lantern-river-01",
            "package_id": "demo-package",
            "public_safe_label": "lantern river",
        }
    )
    token_path = tmp_path / "resonance_token.local.json"
    token_path.write_text(json.dumps(data), encoding="utf-8")
    return load_resonance_token(token_path)


def test_compose_return_artifact_round_trips_through_parser(tmp_path: Path) -> None:
    token = make_demo_token(tmp_path)
    expression = ResonanceExpression(
        carrier_image="lantern",
        carrier_movement="across the river",
        return_word="trust",
        return_image="window",
        return_tone="luminous",
    )

    text = compose_return_artifact(token, expression)
    artifact = parse_return_artifact(text)

    assert artifact.version == "N01-RA-GEN-1"
    assert artifact.module == "Nexus 01 - First Spark"
    assert artifact.origin_trace_id == token.origin_trace_id
    assert artifact.return_slot_id == token.return_slot_id
    assert artifact.package_id == token.package_id
    assert artifact.layer_id == token.layer_id
    assert artifact.carrier_image == "lantern"
    assert artifact.carrier_movement == "across the river"
    assert artifact.return_word == "trust"
    assert artifact.return_image == "window"
    assert artifact.return_tone == "luminous"
    assert "Do not post this return artifact publicly." in text


def test_composed_artifact_matches_existing_slot(tmp_path: Path) -> None:
    token = make_demo_token(tmp_path)
    expression = ResonanceExpression(
        carrier_image="lantern",
        carrier_movement="across the river",
        return_word="trust",
        return_image="window",
        return_tone="luminous",
    )

    artifact = parse_return_artifact(compose_return_artifact(token, expression))
    match = match_return_artifact(artifact, load_return_slots(DEMO_SLOT_PATH))

    assert match.status == MatchStatus.MATCH_WAITING
    assert match.is_match


def test_resonance_expression_requires_all_five_values() -> None:
    try:
        ResonanceExpression(
            carrier_image="lantern",
            carrier_movement="across the river",
            return_word="",
            return_image="window",
            return_tone="luminous",
        )
    except ReturnArtifactWriteError as error:
        assert "return_word" in str(error)
    else:
        raise AssertionError("Expected an error for an empty expression value.")


if __name__ == "__main__":
    import tempfile

    with tempfile.TemporaryDirectory() as directory:
        temp_path = Path(directory)
        test_compose_return_artifact_round_trips_through_parser(temp_path)
        test_composed_artifact_matches_existing_slot(temp_path)
    test_resonance_expression_requires_all_five_values()
    print("Return Artifact writer tests passed.")
