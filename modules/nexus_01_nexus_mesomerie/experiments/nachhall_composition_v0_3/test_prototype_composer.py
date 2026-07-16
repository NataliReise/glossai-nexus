from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import tempfile

from prototype_composer import (
    EXPECTED_PATTERN,
    NachhallCompositionError,
    compose,
    load_library,
    validate_free_word,
    validate_library,
)


LIBRARY_PATH = Path(__file__).resolve().with_name(
    "nachhall_library.mixed_threshold_return.prototype.json"
)


def _library() -> dict[str, object]:
    return load_library(LIBRARY_PATH)


def _assert_raises(expected_fragment: str, callback) -> None:
    try:
        callback()
    except NachhallCompositionError as error:
        if expected_fragment not in str(error):
            raise AssertionError(
                f"Expected {expected_fragment!r} in error message, got {str(error)!r}"
            ) from error
    else:
        raise AssertionError("Expected NachhallCompositionError")


def test_library_loads_and_declares_compact_form() -> None:
    library = _library()
    assert library["library_version"] == "nachhall-composition-prototype-v0.3"
    assert tuple(library["form"]["word_pattern"]) == EXPECTED_PATTERN
    assert len(library["routes"]) == 3


def test_seeded_composition_is_reproducible() -> None:
    first = compose("hope", "spirit", library=_library(), seed=17)
    second = compose("hope", "spirit", library=_library(), seed=17)
    assert first == second


def test_many_seeds_preserve_all_structural_invariants() -> None:
    library = _library()
    for seed in range(100):
        result = compose("hope", "spirit", library=library, seed=seed)
        assert tuple(len(line.split()) for line in result.lines) == EXPECTED_PATTERN
        assert result.lines[-1] == "Spirit"
        assert result.plan.wish_line in {2, 3, 4}
        assert result.lines[result.plan.wish_line - 1].split().count("Hope") == 1
        assert sum(line.split().count("Hope") for line in result.lines[:4]) == 1
        assert len(result.plan.line_variant_ids) == 4


def test_seed_range_reaches_all_three_micro_routes() -> None:
    route_ids = {
        compose("hope", "spirit", library=_library(), seed=seed).plan.route_id
        for seed in range(200)
    }
    assert route_ids == {
        "route.moving-wish.01",
        "route.early-wish.02",
        "route.late-wish.03",
    }


def test_multiple_seeds_create_surface_variation() -> None:
    poems = {
        compose("hope", "spirit", library=_library(), seed=seed).poem
        for seed in range(80)
    }
    assert len(poems) > 20


def test_unicode_letter_words_are_supported() -> None:
    result = compose("nähe", "rückkehr", library=_library(), seed=3)
    assert "Nähe" in result.lines[result.plan.wish_line - 1].split()
    assert result.lines[-1] == "Rückkehr"


def test_invalid_free_words_are_rejected() -> None:
    for value in ("two words", "half-light", "word2", "quiet!", "", "_trace"):
        _assert_raises(
            "letters only" if value else "non-empty word",
            lambda value=value: validate_free_word(value, "wish_word"),
        )


def test_same_word_uses_two_slots_without_failing_validation() -> None:
    result = compose("return", "return", library=_library(), seed=11)
    assert result.lines[-1] == "Return"
    assert sum(line.split().count("Return") for line in result.lines[:4]) == 1
    assert sum(line.split().count("Return") for line in result.lines) == 2


def test_missing_library_fails_calmly() -> None:
    with tempfile.TemporaryDirectory() as directory:
        missing = Path(directory) / "missing.json"
        _assert_raises("Library not found", lambda: load_library(missing))


def test_invalid_json_fails_calmly() -> None:
    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / "broken.json"
        path.write_text("{not-json", encoding="utf-8")
        _assert_raises("not valid JSON", lambda: load_library(path))


def test_duplicate_variant_id_is_rejected() -> None:
    library = deepcopy(_library())
    library["line_1_variants"][1]["id"] = library["line_1_variants"][0]["id"]
    _assert_raises("Duplicate id", lambda: validate_library(library))


def test_zero_weight_is_rejected() -> None:
    library = deepcopy(_library())
    library["routes"][0]["weight"] = 0
    _assert_raises("positive integer weight", lambda: validate_library(library))


def test_wrong_word_count_is_rejected_before_composition() -> None:
    library = deepcopy(_library())
    library["routes"][0]["line_2_variants"][0]["text"] = "summer rain enters"
    _assert_raises("expected 4", lambda: validate_library(library))


def test_wrong_placeholder_location_is_rejected() -> None:
    library = deepcopy(_library())
    library["routes"][0]["line_2_variants"][0]["text"] = "{wish_word} rain enters softly"
    _assert_raises("placeholder count", lambda: validate_library(library))


def test_visible_punctuation_is_rejected() -> None:
    library = deepcopy(_library())
    library["line_1_variants"][0]["text"] = "Rain, window"
    _assert_raises("letter words", lambda: validate_library(library))


if __name__ == "__main__":
    test_library_loads_and_declares_compact_form()
    test_seeded_composition_is_reproducible()
    test_many_seeds_preserve_all_structural_invariants()
    test_seed_range_reaches_all_three_micro_routes()
    test_multiple_seeds_create_surface_variation()
    test_unicode_letter_words_are_supported()
    test_invalid_free_words_are_rejected()
    test_same_word_uses_two_slots_without_failing_validation()
    test_missing_library_fails_calmly()
    test_invalid_json_fails_calmly()
    test_duplicate_variant_id_is_rejected()
    test_zero_weight_is_rejected()
    test_wrong_word_count_is_rejected_before_composition()
    test_wrong_placeholder_location_is_rejected()
    test_visible_punctuation_is_rejected()
    print("Nachhall V0.3 composer tests passed.")
