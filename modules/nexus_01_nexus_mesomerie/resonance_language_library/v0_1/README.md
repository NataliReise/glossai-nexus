# Resonance Language Library V0.1

This directory contains the first machine-readable, local language library for the Resonance Chamber.

The library follows these principles:

```text
The Return Artifact carries selections, not prose rendering.

The Nexus renders those selections through a local,
versioned library of approved language forms.
```

The renderer does not generate grammar and does not use AI. It selects and arranges approved forms.

## Files

```text
images.json
image_responses.json
scents.json
scent_responses.json
movements.json
movement_responses.json
echo_paths.json
```

## Responsibilities

```text
Return Artifact
-> selected IDs, free words, artifact version, library version

Language library
-> approved player-facing source text
-> approved Resonance Artifact forms
-> approved Nexus Echo forms and paths

Renderer
-> ID lookup
-> compatibility checks
-> slot insertion
-> word-count validation
-> deterministic output
```

## Version identifier

```text
resonance-en-v0.1
```

## Current boundary

The five canonical Echo paths in `echo_paths.json` are reference paths derived from the manual test corpus. They are intentionally explicit. V0.1 should prefer known-valid paths over improvised combinations.
