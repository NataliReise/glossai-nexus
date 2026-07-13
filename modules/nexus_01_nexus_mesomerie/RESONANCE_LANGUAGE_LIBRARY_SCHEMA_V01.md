# Resonance Language Library Schema V0.1

Status date: 2026-07-13

This note defines the first schema direction for the local, versioned language library used by the Resonance Artifact and Nexus Echo renderers.

It builds on:

```text
RESONANCE_OUTPUT_TERMINOLOGY_V01.md
NEXUS_ECHO_STANDARD_TEMPLATE_V01.md
RESONANCE_RESPONSE_SETS_V01.md
```

## Core architecture

The Return Artifact remains small and transportable.

```text
Return Artifact
-> carries selections, free words, and compatibility metadata

Local Nexus language library
-> carries approved render-ready language forms

Local renderers
-> select and arrange approved forms
```

Working principle:

```text
The Return Artifact carries selections, not prose rendering.

The Nexus renders those selections through a local,
versioned library of approved language forms.
```

## Minimal Return Artifact data

A V0.1 Return Artifact may carry a compact structure such as:

```json
{
  "artifact_version": "0.1",
  "language_library": "resonance-en-v0.1",
  "image_id": "waiting-lantern",
  "image_response_id": "appearing-path",
  "scent_id": "summer-rain",
  "scent_response_id": "possibility-of-encounter",
  "movement_id": "falling-feather",
  "movement_response_id": "crossing-feather",
  "wish_word": "courage",
  "return_word": "trust"
}
```

The Return Artifact does not need to carry the full Resonance Artifact or Nexus Echo prose.

## Library responsibilities

The language library should provide:

```text
stable IDs
source-facing text where useful
approved Resonance Artifact lines
approved Nexus Echo forms
compatibility information
motif reuse information
word-count metadata
fallback information
```

The library should not provide a free grammar engine.

## Proposed top-level shape

```json
{
  "library_id": "resonance-en-v0.1",
  "schema_version": "0.1",
  "language": "en",
  "entries": {},
  "echo_paths": {},
  "fallbacks": {}
}
```

## Element entry

A general element entry may use this shape:

```json
{
  "id": "waiting-lantern",
  "category": "image",
  "source_text": "a lantern waiting in the dark",
  "artifact": {
    "lines": [
      "A lantern waits in the dark."
    ]
  },
  "echo": {
    "line_1": [
      {
        "id": "dark-lantern",
        "text": "Dark lantern",
        "word_count": 2,
        "motifs": ["lantern", "light", "darkness"]
      },
      {
        "id": "waiting-lantern-short",
        "text": "Waiting lantern",
        "word_count": 2,
        "motifs": ["lantern", "waiting"]
      }
    ]
  }
}
```

## Resonance Artifact forms

The Resonance Artifact renderer should use complete, approved grammatical forms.

Example:

```json
{
  "id": "falling-feather",
  "category": "movement",
  "source_text": "a feather turning as it falls",
  "artifact": {
    "lines": [
      "A feather turns as it falls."
    ]
  }
}
```

For multi-line rendering:

```json
{
  "id": "playful-waves",
  "category": "movement_response",
  "source_text": "the open edges beginning to curl into two playful waves",
  "artifact": {
    "lines": [
      "Its edges begin to curl",
      "into two playful waves."
    ],
    "requires_carried_id": "opening-circle"
  }
}
```

The renderer selects these lines. It does not derive the grammatical change itself.

## Nexus Echo line forms

### Line 1 form

```json
{
  "id": "open-books",
  "text": "Open books",
  "line": 1,
  "word_count": 2,
  "motifs": ["books", "pages", "opening"]
}
```

### Line 2 form

```json
{
  "id": "wait-beneath-soft-light",
  "text": "wait beneath soft light",
  "line": 2,
  "word_count": 4,
  "requires_line_1": ["open-books"],
  "uses_trace_ids": ["books-and-cedar", "open-books-beside-one-another"],
  "motifs": ["books", "light", "waiting"]
}
```

### Line 3 relation form

```json
{
  "id": "voices-meet-knot-loosens",
  "text": "two voices meet; one knot loosens",
  "line": 3,
  "word_count": 6,
  "uses_trace_ids": ["two-voices-one-page", "loosening-knot"],
  "relation": "meet",
  "motifs": ["voices", "meeting", "knot", "loosening"]
}
```

Line 3 forms should be complete approved six-word phrases. They should not be assembled freely from isolated nouns and verbs in V0.1.

### Line 4 echo form

A fixed form:

```json
{
  "id": "light-turns-homeward",
  "text": "the light turns homeward",
  "line": 4,
  "word_count": 4,
  "reuses_motif": "light",
  "uses_trace_ids": ["answering-distant-light", "sense-of-return"],
  "motifs": ["light", "return"]
}
```

A controlled one-word slot form:

```json
{
  "id": "path-carries-wish-word",
  "template": "the path carries {wish_word}",
  "line": 4,
  "fixed_word_count": 3,
  "slot": {
    "name": "wish_word",
    "required_word_count": 1
  },
  "result_word_count": 4,
  "reuses_motif": "path"
}
```

Only explicitly declared slots are allowed. Slot insertion is not free sentence generation.

### Line 5 form

Line 5 is not stored as prose.

```text
L5 = return_word
```

The renderer validates that it is one accepted word.

## Echo path entries

Because compatibility is relational, the library may define complete approved paths rather than expecting the renderer to discover poetic combinations.

Example:

```json
{
  "id": "clear-meeting-01",
  "requires": {
    "image_id": "waiting-lantern",
    "image_response_id": "appearing-path",
    "movement_id": "falling-feather",
    "movement_response_id": "crossing-feather"
  },
  "lines": {
    "line_1_id": "summer-rain",
    "line_2_id": "opens-one-hidden-path",
    "line_3_id": "feathers-cross-waiting-light",
    "line_4_id": "path-carries-wish-word",
    "line_5_source": "return_word"
  }
}
```

A path may depend on all selected IDs or on a compatible subset. The exact matching strategy should remain explicit and testable.

## Why complete approved paths may be useful

The poetic quality of the Nexus Echo depends mainly on Lines 3 and 4.

Blindly combining individually valid forms could produce formally correct but weak or contradictory poems.

For V0.1, a practical balance is:

```text
approved reusable line forms
+
approved compatibility paths
+
strict validation
```

## Compatibility fields

Useful fields may include:

```text
requires_trace_ids
compatible_with
incompatible_with
requires_line_1
reuses_motif
uses_trace_ids
relation
fallback_group
```

Not every entry needs every field.

## Motif metadata

Motifs support validation and traceability. They do not authorize free synonym generation.

```json
{
  "motifs": ["bridge", "crossing", "silence", "room"]
}
```

A motif may be used to verify that Line 4 repeats something recognizable from Line 1 or Line 2.

The renderer should still select complete approved forms.

## Word-count metadata

Every stored Echo form should include its expected word count.

```json
{
  "text": "light and shadow share one silence",
  "word_count": 6
}
```

The runtime validator must count the rendered result independently rather than trusting metadata alone.

## Versioning

The Return Artifact should declare the required language library:

```json
{
  "artifact_version": "0.1",
  "language_library": "resonance-en-v0.1"
}
```

The local Nexus should check:

```text
artifact schema supported
library version available
all selected IDs known
all required render forms available
```

A later library must not silently reinterpret an older artifact without a declared compatibility rule.

## Missing library or ID behavior

The Nexus must not improvise missing prose.

Preferred order:

```text
1. use the declared compatible local library
2. use an explicitly compatible fallback library
3. show a calm technical fallback based on IDs and free words
4. never invent substitute poetic language
```

A technical fallback may preserve the artifact safely without pretending to render the intended poem.

## Separation of concerns

```text
Return Artifact
-> selection and transport

Language library
-> approved language and compatibility

Resonance Artifact renderer
-> complete readable long form

Nexus Echo renderer
-> approved Nachhall path

Validators
-> schema, IDs, compatibility, and word pattern
```

## V0.1 implementation boundary

For the first implementation, the library may remain deliberately small:

```text
five tested compositions
five canonical Resonance Artifacts
five canonical standard Echo paths
one or more explicit fallbacks
```

The schema should support later expansion, but the renderer should not become more general than the tested language material requires.

## Design formula

```text
The artifact says what was chosen.
The library knows how it may be shown.
The renderer selects; it does not improvise.
```
