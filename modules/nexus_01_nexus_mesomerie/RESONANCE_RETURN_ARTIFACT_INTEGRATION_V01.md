# Resonance Return Artifact Integration V0.1

Status date: 2026-07-14

## Purpose

This note defines the first shared data contract between the existing Return Resonance transport path and the local Resonance rendering pipeline.

The aim is not to replace either working implementation prematurely. The aim is to identify their common structural core, preserve the tested boundaries of both systems, and define one integration target for the next implementation slice.

## Current structures

### Existing Return Resonance artifact

The current human-readable Return Artifact is created from a `ResonanceToken` and a `ResonanceExpression`.

Its structural fields are:

```text
version
module
origin_trace_id
return_slot_id
package_id
layer_id
```

Its current expression fields are:

```text
carrier_image
carrier_movement
return_word
return_image
return_tone
```

This format already supports:

- transport through a private human channel
- parsing back into a typed `ReturnArtifact`
- slot matching
- local result creation
- protection against mismatched package and layer identifiers

### Resonance rendering input

The local rendering pipeline currently consumes a slim JSON object with:

```text
artifact_version
language_library
image_id
image_response_id
scent_id
scent_response_id
movement_id
movement_response_id
wish_word
return_word
```

This input already supports:

- deterministic Resonance Artifact rendering
- deterministic Nexus Echo rendering
- exact path matching against approved IDs
- local, versioned language-library lookup
- no-improvisation fallback behavior

## Field comparison

### Direct structural overlap

The following fields already describe the same transport identity and should remain authoritative:

```text
origin_trace_id
return_slot_id
package_id
layer_id
```

The existing token already provides the stable module identifier `N01`. The current text artifact stores a human-readable module name instead. For integration, the stable machine field should be `module_id`.

### Version fields

The two current version fields serve different purposes and should not be merged:

```text
artifact_version
language_library
```

`artifact_version` identifies the data contract.

`language_library` identifies the approved local phrase library used for rendering.

The earlier text-artifact value `N01-RA-GEN-1` remains an implementation/version marker for the legacy writer during migration. It should not be reused as the version of the new JSON contract.

### Expression-field relationship

The former free-text expression fields and the new selection fields are related, but they are not equivalent.

```text
carrier_image
carrier_movement
return_image
return_tone
```

were useful as an early playable placeholder and as human-readable transport content.

The render pipeline now requires stable, reviewable selections:

```text
image_id
image_response_id
scent_id
scent_response_id
movement_id
movement_response_id
wish_word
return_word
```

For V0.1 integration, these stable selections become the canonical chamber-expression payload.

The old free-text fields should remain readable during migration, but new rendering logic must not infer stable IDs from free prose.

## Proposed shared V0.1 contract

```json
{
  "artifact_version": "0.1",
  "artifact_type": "resonance-return",
  "module_id": "N01",
  "layer_id": "return-resonance-1",
  "origin_trace_id": "trace-demo-001",
  "return_slot_id": "return-slot-demo-001",
  "package_id": "nexus-01-demo-package",
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

## Required fields

All V0.1 fields above are required.

The structural fields must be copied from the validated Resonance Token and must not be supplied independently by the chamber UI.

The chamber contributes only:

```text
image_id
image_response_id
scent_id
scent_response_id
movement_id
movement_response_id
wish_word
return_word
```

This separation preserves the boundary:

```text
The token carries the route.
The chamber creates the response.
The artifact joins them without exposing private reasons.
```

## Validation responsibilities

### Token layer

The existing token validator remains responsible for:

- token version and token type
- module identity
- layer identity
- origin trace identity
- return slot identity
- package identity
- enabled chamber

### Chamber-expression layer

The rendering library remains responsible for:

- known selection IDs
- response compatibility with source selections
- one-word validation for `wish_word` and `return_word`
- supported library version
- approved Echo path availability
- exact `2-4-6-4-1` Echo validation

### Integration layer

The new bridge must be responsible for:

- copying structural identifiers from the validated token
- joining them with the validated chamber selections
- writing and reading the shared JSON artifact without information loss
- preserving private-channel warnings in surrounding UI or documentation
- refusing to render before Return Slot matching succeeds
- producing both local outputs from the same validated artifact

## Opening order

The intended local flow is:

```text
Resonance Token
-> Chamber selections
-> Resonance Return Artifact
-> Return Slot matching
-> local opening
   |- Resonance Artifact
   `- Nexus Echo
```

Rendering before slot matching is deliberately outside the V0.1 integration path.

The artifact may travel privately. The poetic opening belongs to the matched local Nexus.

## Migration boundary

The existing human-readable writer and parser are already tested and should remain unchanged during the first integration slice.

The next implementation should therefore add a parallel, explicitly named JSON bridge rather than silently changing the legacy format.

Suggested implementation files:

```text
return_resonance/resonance_render_bridge.py
return_resonance/tests/test_resonance_render_bridge.py
```

The bridge may initially accept a validated `ResonanceToken` plus a new typed chamber-selection object and return the shared JSON dictionary or dataclass.

Only after the complete integration test is green should we decide whether the legacy five-field `ResonanceExpression` remains as a compatibility layer, is adapted, or is retired.

## First integration test

The first complete test should prove:

```text
load token
-> create chamber selections
-> build shared Resonance Return Artifact
-> serialize to JSON
-> deserialize from JSON
-> match Return Slot
-> render Resonance Artifact
-> render Nexus Echo
-> verify exact expected outputs
```

The test must also verify rejection of:

- changed package ID
- changed layer ID
- unsupported artifact version
- unsupported language-library version
- unknown selection IDs
- incompatible response IDs
- artifact without an approved Echo path

## V0.1 non-goals

This integration does not introduce:

- automatic upload or synchronization
- public posting
- tracking or social graphs
- free-form language generation
- AI or language-model rendering
- inference from private meaning
- automatic conversion of old prose fields into selection IDs
- multiple language libraries in one artifact

## Decision summary

```text
One transport artifact.
One stable route.
One versioned language library.
Two local poetic outputs.
No inferred meaning.
No improvised prose.
```

## Next implementation slice

Create the typed bridge and its tests without modifying the existing writer/parser behavior.

The first target is not a CLI. It is a lossless, tested connection between the validated Resonance Token, the stable chamber selections, Return Slot matching, and both local renderers.
