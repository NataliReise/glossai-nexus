from __future__ import annotations

from pathlib import Path
import random
import tempfile

from prototype_composer import (
    EXPECTED_ECHO_COUNTS,
    PrototypeCompositionError,
    compose,
    load_library,
    validate_free_word,
)


LIBRARY_PATH = Path(__file__).resolve().with_name(
    "building_blocks.mixed_threshold_return.prototype.json"
)


def _library() -> dict[str, object]:
    return load_library(LIBRARY_PATH)


def test_seeded_composition_is_reproducible() -> None:
    first = compose(_library(), "hope", "spirit", rng=random.Random(17))
    second = compose(_library(), "hope", "spirit", rng=random.Random(17))
    assert first == second


def test_multiple_seeds_create_variation() -> None:
    long_forms = set()
    echoes = set()
    for seed in range(40):
        result = compose(_library(), "hope", "spirit", rng=random.Random(seed))
        long_forms.add(result.long_form)
        echoes.add(result.nexus_echo)
    assert len(long_forms) > 10
    assert len(echoes) > 5


def test_echo_invariants_hold_across_many_runs() -> None:
    for seed in range(100):
        result = compose(_library(), "blue", "perhaps", rng=random.Random(seed))
        lines = result.nexus_echo.splitlines()
        counts = tuple(len(line.split()) for line in lines)
        assert counts == EXPECTED_ECHO_COUNTS
        assert sum(line.count("Blue") for line in lines) == 1
        assert lines[-1] == "Perhaps"
        assert result.plan.echo_wish_line in {2, 3, 4}
        assert result.plan.echo_source_trace
        assert result.plan.echo_source_trace.lower() in result.nexus_echo.lower()


def test_long_form_contains_each_free_word_once() -> None:
    for seed in range(40):
        result = compose(_library(), "hush", "return", rng=random.Random(seed))
        assert result.long_form.count("Hush") == 1
        assert result.long_form.count("Return") == 1


def test_required_resonance_gain_is_present() -> None:
    library = _library()
    required = set(library["required_gain_one_of"])
    for seed in range(40):
        result = compose(library, "hope", "spirit", rng=random.Random(seed))
        assert required.intersection(result.plan.resonant_gains)


def test_invalid_free_words_are_rejected() -> None:
    for value in ("two words", "half-light", "word2", "quiet!", ""):
        try:
            validate_free_word(value, "wish_word")
        except PrototypeCompositionError:
            pass
        else:
            raise AssertionError(f"Expected invalid free word to fail: {value!r}")


def test_existing_library_is_required() -> None:
    with tempfile.TemporaryDirectory() as directory:
        missing = Path(directory) / "missing.json"
        try:
            load_library(missing)
        except PrototypeCompositionError as error:
            assert "Could not read prototype library" in str(error)
        else:
            raise AssertionError("Expected PrototypeCompositionError")


if __name__ == "__main__":
    test_seeded_composition_is_reproducible()
    test_multiple_seeds_create_variation()
    test_echo_invariants_hold_across_many_runs()
    test_long_form_contains_each_free_word_once()
    test_required_resonance_gain_is_present()
    test_invalid_free_words_are_rejected()
    test_existing_library_is_required()
    print("Prototype composer tests passed.")
