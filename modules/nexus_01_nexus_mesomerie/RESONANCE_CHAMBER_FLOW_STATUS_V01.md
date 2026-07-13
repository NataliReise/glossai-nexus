# Resonance Chamber Flow Status V0.1

This note records the first working internal flow of the Resonance Chamber in Nexus 01.

It marks the point at which the Chamber is no longer only a concept boundary. It now has a small executable mechanical core of its own.

## Current milestone

The Resonance Chamber now exists as a separate internal module:

```text
chambers/resonance/
├── __init__.py
├── README.md
├── choices.py
├── flow.py
└── tests/
    └── test_flow.py
```

The current implementation is intentionally small.

It does not yet provide a terminal interface, a graphical interface, artifact persistence, token loading, or Atrium integration.

Its purpose is narrower:

```text
prove the Chamber grammar
before building the Chamber surface
```

## Current Chamber grammar

The first deterministic response path is:

```text
image
→ image response
→ scent
→ scent response
→ movement
→ movement response
→ wish word
→ return word
```

The Chamber owns this sequence.

The Nexus does not need to know how the selections were made.

The Chamber returns only the shared typed result:

```text
ChamberSelections
```

## Responsibility split

The current code keeps the intended module boundary intact.

### `choices.py`

Owns the Chamber-visible choice material and compatibility rules.

It currently contains only the five curated reference paths already used by the V0.1 resonance language library and renderer fixtures.

It does not invent new combinations.

It does not render the final poem.

### `flow.py`

Owns the order of the Chamber interaction and the validation of each transition.

It asks for one valid selection at each stage and rejects:

- unknown option identifiers,
- incompatible response identifiers,
- missing scripted answers,
- extra scripted answers,
- invalid multi-word wish or return values.

### `ScriptedChamberIO`

Provides a deterministic input adapter for tests.

This keeps the Chamber flow independent from `input()` and `print()`.

A future terminal or graphical adapter may therefore use the same Chamber mechanism without changing its grammar.

### `ChamberSelections`

Remains the only value that crosses from the Chamber into the shared Return Resonance infrastructure.

The Chamber does not build the transport artifact itself.

## What remains outside the Chamber

The following responsibilities are intentionally not part of this package:

```text
Resonance Token loading
route identity
module, layer, package and slot metadata
Resonance Return Artifact construction
artifact JSON persistence
Return Slot matching
local opening
Resonance Artifact rendering
Nexus Echo rendering
Atrium state changes
manual sharing
```

This separation remains essential.

```text
The Chamber creates the response.
The route infrastructure carries it.
The opening infrastructure reveals it.
```

## Current tested guarantees

The local flow test now confirms that:

1. the canonical eight-step sequence completes successfully;
2. the result is returned as exact `ChamberSelections`;
3. unknown choices are rejected;
4. incompatible response pairs are rejected;
5. incomplete scripted input is rejected;
6. unused extra scripted input is rejected;
7. wish and return values must remain single words.

Confirmed local result:

```text
Resonance Chamber flow tests passed.
```

## Current full architecture

The tested system can now be read as three distinct regions.

### Chamber region

```text
curated Chamber choices
→ deterministic Chamber flow
→ ChamberSelections
```

### Transport and route region

```text
Resonance Token
+ ChamberSelections
→ Resonance Return Artifact
→ JSON roundtrip
→ Return Slot matching
```

### Local opening region

```text
matched Resonance Return Artifact
→ Resonance Artifact
+ Nexus Echo
→ persistent local result
```

The current Chamber milestone fills a previously missing part near the beginning of this chain.

## Important limitation

The current flow is mechanically valid but not yet a complete player experience.

The visible options are still primarily represented through stable identifiers and test-facing structures.

The Chamber does not yet answer questions such as:

- How are options introduced poetically?
- What does the player see before making a choice?
- How does the Chamber teach its local vocabulary?
- How does the player review or revise a composition?
- What does completion feel like before returning to the Atrium?

Those are interaction-design questions, not transport questions.

They should be addressed inside the Chamber module without weakening the shared contracts.

## Recommended next slice

The next implementation slice should connect the proven Chamber result to the existing artifact bridge without adding a user interface yet.

Suggested direction:

```text
chambers/resonance/composer.py
```

Its role should remain narrow:

```text
run or receive ChamberSelections
+ receive route context from outside
→ call the existing resonance artifact bridge
→ return a typed Resonance Return Artifact
```

The composer should not own token storage, file writing, slot matching, rendering, or terminal input.

After this integration boundary is tested, a thin terminal adapter can be added safely.

## Working sequence

```text
Mechanism
→ contract
→ integration
→ interface
```

## Working formula

```text
The Chamber now keeps its grammar in code.
The next step is to let that grammar cross the boundary cleanly.
```
