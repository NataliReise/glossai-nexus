"""Validate the local Resonance Language Library.

This validator checks only hard structural properties. It does not judge poetic
quality and it never rewrites library data.
"""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
import re
import sys
from typing import Any, Iterable

EXPECTED_LIBRARY_VERSION = "resonance-en-v0.1"
EXPECTED_ECHO_PATTERN = (2, 4, 6, 4, 1)
LIBRARY_FILES = (
    "images.json",
    "image_responses.json",
    "scents.json",
    "scent_responses.json",
    "movements.json",
    "movement_responses.json",
    "echo_paths.json",
)


@dataclass(frozen=True)
class ValidationIssue:
    location: str
    message: str

    def __str__(self) -> str:
        return f"{self.location}: {self.message}"


def _load_json(path: Path) -> tuple[Any | None, list[ValidationIssue]]:
    try:
        return json.loads(path.read_text(encoding="utf-8")), []
    except FileNotFoundError:
        return None, [ValidationIssue(str(path), "file is missing")]
    except json.JSONDecodeError as error:
        return None, [
            ValidationIssue(
                str(path),
                f"invalid JSON at line {error.lineno}, column {error.colno}: {error.msg}",
            )
        ]


def _word_count(text: str) -> int:
    rendered = re.sub(r"\{(?:wish_word|return_word)\}", "word", text)
    return len(re.findall(r"\b[\w'-]+\b", rendered, flags=re.UNICODE))


def _require_mapping(value: Any, location: str, issues: list[ValidationIssue]) -> dict[str, Any]:
    if not isinstance(value, dict):
        issues.append(ValidationIssue(location, "must be a JSON object"))
        return {}
    return value


def _require_list(value: Any, location: str, issues: list[ValidationIssue]) -> list[Any]:
    if not isinstance(value, list):
        issues.append(ValidationIssue(location, "must be a JSON array"))
        return []
    return value


def _collect_entry_ids(document: dict[str, Any], location: str, issues: list[ValidationIssue]) -> set[str]:
    ids: set[str] = set()
    for index, entry_value in enumerate(_require_list(document.get("entries"), f"{location}.entries", issues)):
        entry = _require_mapping(entry_value, f"{location}.entries[{index}]", issues)
        entry_id = entry.get("id")
        if not isinstance(entry_id, str) or not entry_id:
            issues.append(ValidationIssue(f"{location}.entries[{index}].id", "must be a non-empty string"))
            continue
        if entry_id in ids:
            issues.append(ValidationIssue(f"{location}.entries[{index}].id", f"duplicate id {entry_id!r}"))
        ids.add(entry_id)
        _validate_render_lines(entry, f"{location}.entries[{index}]", issues)
    return ids


def _collect_nested_response_ids(
    document: dict[str, Any],
    parent_key: str,
    valid_parent_ids: set[str],
    location: str,
    issues: list[ValidationIssue],
) -> set[str]:
    response_ids: set[str] = set()
    seen_parent_ids: set[str] = set()

    for index, group_value in enumerate(_require_list(document.get("entries"), f"{location}.entries", issues)):
        group = _require_mapping(group_value, f"{location}.entries[{index}]", issues)
        parent_id = group.get(parent_key)
        if not isinstance(parent_id, str) or not parent_id:
            issues.append(ValidationIssue(f"{location}.entries[{index}].{parent_key}", "must be a non-empty string"))
        else:
            if parent_id not in valid_parent_ids:
                issues.append(ValidationIssue(f"{location}.entries[{index}].{parent_key}", f"unknown referenced id {parent_id!r}"))
            if parent_id in seen_parent_ids:
                issues.append(ValidationIssue(f"{location}.entries[{index}].{parent_key}", f"duplicate response group for {parent_id!r}"))
            seen_parent_ids.add(parent_id)

        responses = _require_list(group.get("responses"), f"{location}.entries[{index}].responses", issues)
        local_ids: set[str] = set()
        for response_index, response_value in enumerate(responses):
            response_location = f"{location}.entries[{index}].responses[{response_index}]"
            response = _require_mapping(response_value, response_location, issues)
            response_id = response.get("id")
            if not isinstance(response_id, str) or not response_id:
                issues.append(ValidationIssue(f"{response_location}.id", "must be a non-empty string"))
                continue
            if response_id in local_ids:
                issues.append(ValidationIssue(f"{response_location}.id", f"duplicate id {response_id!r} within group"))
            if response_id in response_ids:
                issues.append(ValidationIssue(f"{response_location}.id", f"duplicate response id {response_id!r} across library"))
            local_ids.add(response_id)
            response_ids.add(response_id)
            _validate_render_lines(response, response_location, issues)

    return response_ids


def _validate_render_lines(entry: dict[str, Any], location: str, issues: list[ValidationIssue]) -> None:
    source_text = entry.get("source_text")
    if not isinstance(source_text, str) or not source_text.strip():
        issues.append(ValidationIssue(f"{location}.source_text", "must be a non-empty string"))

    artifact = entry.get("resonance_artifact")
    if artifact is None:
        return
    artifact_mapping = _require_mapping(artifact, f"{location}.resonance_artifact", issues)
    lines = _require_list(artifact_mapping.get("lines"), f"{location}.resonance_artifact.lines", issues)
    if not lines:
        issues.append(ValidationIssue(f"{location}.resonance_artifact.lines", "must contain at least one line"))
    for line_index, line in enumerate(lines):
        if not isinstance(line, str) or not line.strip():
            issues.append(ValidationIssue(f"{location}.resonance_artifact.lines[{line_index}]", "must be a non-empty string"))


def _validate_versions(documents: dict[str, dict[str, Any]], issues: list[ValidationIssue]) -> None:
    for filename, document in documents.items():
        version = document.get("library_version")
        if version != EXPECTED_LIBRARY_VERSION:
            issues.append(
                ValidationIssue(
                    filename,
                    f"library_version must be {EXPECTED_LIBRARY_VERSION!r}, got {version!r}",
                )
            )


def _validate_echo_paths(
    document: dict[str, Any],
    known_ids: dict[str, set[str]],
    issues: list[ValidationIssue],
) -> None:
    form = _require_mapping(document.get("form"), "echo_paths.json.form", issues)
    pattern = tuple(_require_list(form.get("word_pattern"), "echo_paths.json.form.word_pattern", issues))
    if pattern != EXPECTED_ECHO_PATTERN:
        issues.append(
            ValidationIssue(
                "echo_paths.json.form.word_pattern",
                f"must be {list(EXPECTED_ECHO_PATTERN)!r}, got {list(pattern)!r}",
            )
        )

    path_ids: set[str] = set()
    required_keys = {
        "image_id": "images",
        "image_response_id": "image_responses",
        "scent_id": "scents",
        "scent_response_id": "scent_responses",
        "movement_id": "movements",
        "movement_response_id": "movement_responses",
    }

    for index, path_value in enumerate(_require_list(document.get("paths"), "echo_paths.json.paths", issues)):
        location = f"echo_paths.json.paths[{index}]"
        path = _require_mapping(path_value, location, issues)
        path_id = path.get("id")
        if not isinstance(path_id, str) or not path_id:
            issues.append(ValidationIssue(f"{location}.id", "must be a non-empty string"))
        elif path_id in path_ids:
            issues.append(ValidationIssue(f"{location}.id", f"duplicate path id {path_id!r}"))
        else:
            path_ids.add(path_id)

        requires = _require_mapping(path.get("requires"), f"{location}.requires", issues)
        for field, category in required_keys.items():
            value = requires.get(field)
            if not isinstance(value, str) or not value:
                issues.append(ValidationIssue(f"{location}.requires.{field}", "must be a non-empty string"))
            elif value not in known_ids[category]:
                issues.append(ValidationIssue(f"{location}.requires.{field}", f"unknown referenced id {value!r}"))

        lines = _require_list(path.get("lines"), f"{location}.lines", issues)
        if len(lines) != len(EXPECTED_ECHO_PATTERN):
            issues.append(ValidationIssue(f"{location}.lines", "must contain exactly five lines"))
            continue
        for line_index, (line, expected_count) in enumerate(zip(lines, EXPECTED_ECHO_PATTERN, strict=True)):
            if not isinstance(line, str) or not line.strip():
                issues.append(ValidationIssue(f"{location}.lines[{line_index}]", "must be a non-empty string"))
                continue
            actual_count = _word_count(line)
            if actual_count != expected_count:
                issues.append(
                    ValidationIssue(
                        f"{location}.lines[{line_index}]",
                        f"expected {expected_count} words, found {actual_count}: {line!r}",
                    )
                )

        if isinstance(path.get("echo_motif"), str) and len(lines) >= 4:
            motif = path["echo_motif"].casefold()
            earlier = f"{lines[0]} {lines[1]}".casefold()
            echoed = lines[3].casefold()
            if motif not in earlier:
                issues.append(ValidationIssue(f"{location}.echo_motif", f"motif {motif!r} does not appear in line 1 or 2"))
            if motif not in echoed:
                issues.append(ValidationIssue(f"{location}.echo_motif", f"motif {motif!r} does not reappear in line 4"))

        if len(lines) >= 5 and lines[4] != "{return_word}":
            issues.append(ValidationIssue(f"{location}.lines[4]", "must be exactly '{return_word}' in V0.1"))


def validate_library(library_dir: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    documents: dict[str, dict[str, Any]] = {}

    for filename in LIBRARY_FILES:
        document, load_issues = _load_json(library_dir / filename)
        issues.extend(load_issues)
        if document is not None:
            documents[filename] = _require_mapping(document, filename, issues)

    if len(documents) != len(LIBRARY_FILES):
        return issues

    _validate_versions(documents, issues)

    image_ids = _collect_entry_ids(documents["images.json"], "images.json", issues)
    scent_ids = _collect_entry_ids(documents["scents.json"], "scents.json", issues)
    movement_ids = _collect_entry_ids(documents["movements.json"], "movements.json", issues)

    image_response_ids = _collect_nested_response_ids(
        documents["image_responses.json"], "image_id", image_ids, "image_responses.json", issues
    )
    scent_response_ids = _collect_nested_response_ids(
        documents["scent_responses.json"], "scent_id", scent_ids, "scent_responses.json", issues
    )
    movement_response_ids = _collect_nested_response_ids(
        documents["movement_responses.json"], "movement_id", movement_ids, "movement_responses.json", issues
    )

    _validate_echo_paths(
        documents["echo_paths.json"],
        {
            "images": image_ids,
            "image_responses": image_response_ids,
            "scents": scent_ids,
            "scent_responses": scent_response_ids,
            "movements": movement_ids,
            "movement_responses": movement_response_ids,
        },
        issues,
    )

    return issues


def default_library_dir() -> Path:
    return Path(__file__).resolve().parent / "v0_1"


def main(argv: Iterable[str] | None = None) -> int:
    arguments = list(argv if argv is not None else sys.argv[1:])
    library_dir = Path(arguments[0]).resolve() if arguments else default_library_dir()
    issues = validate_library(library_dir)

    if issues:
        print(f"Resonance language library validation failed with {len(issues)} issue(s):")
        for issue in issues:
            print(f"- {issue}")
        return 1

    print(f"Resonance language library valid: {library_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
