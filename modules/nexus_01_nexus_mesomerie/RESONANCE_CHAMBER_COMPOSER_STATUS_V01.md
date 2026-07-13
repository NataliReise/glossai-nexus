# Resonance Chamber Composer Status V0.1

This note records the first working integration seam between the Resonance Chamber mechanics and the shared Resonance Return transport contract.

## Current milestone

The Resonance Chamber can now do more than complete its own internal grammar.

It can pass its typed result across a deliberately narrow boundary and receive a complete `ResonanceReturnArtifact` in return.

```text
Resonance Token
-> Resonance Chamber Flow
-> ChamberSelections
-> Resonance Chamber Composer
-> Resonance Return Artifact
```

The composer tests currently pass.

## Implemented components

```text
chambers/resonance/
├── choices.py
├── flow.py
├── composer.py
├── __init__.py
├── README.md
└── tests/
    ├── test_flow.py
    └── test_composer.py
```

### `choices.py`

Owns the first curated V0.1 choice catalog:

- visible player-facing labels
- stable internal IDs
- image-response compatibility
- scent-response compatibility
- movement-response compatibility

### `flow.py`

Owns the Resonance Chamber's fixed V0.1 grammar:

```text
image
-> image response
-> scent
-> scent response
-> movement
-> movement response
-> wish word
-> return word
```

It returns one shared `ChamberSelections` value.

### `composer.py`

Owns only the seam between Chamber mechanics and the shared transport bridge.

It receives:

```text
ResonanceToken
ChamberIO
ResonanceChamberFlow
```

It produces:

```text
ChamberSelections
ResonanceReturnArtifact
```

Its responsibility is intentionally small:

```text
run the Chamber
-> collect the typed Chamber result
-> combine that result with validated route identity
-> return the completed transport artifact
```

## Current architectural separation

The implementation now has three distinct responsibilities.

### Chamber

The Chamber owns its own mechanical language:

- decision order
- visible choices
- compatibility rules
- word-entry rules
- completion of the local flow

### Composer

The composer owns the integration seam:

- starts the Chamber flow
- receives `ChamberSelections`
- passes the selections and token to the existing bridge
- returns the composition result

### Shared bridge

The shared bridge owns the transport contract:

- validates route identity
- validates supported module and layer
- builds `ResonanceReturnArtifact`
- later supports matching and local opening

Working structure:

```text
Chamber
  owns the grammar

Composer
  joins grammar and route

Bridge
  owns the transport contract
```

## What the composer does not do

The composer does not:

- load token files
- write artifact files
- choose output paths
- overwrite existing files
- match Return Slots
- render Resonance Artifacts
- render Nexus Echoes
- mark slots as opened
- change Atrium state
- publish or transmit anything

These boundaries are intentional.

The composer returns values. It does not perform persistence or delivery.

## Tested behavior

The current composer tests verify that:

- the complete Chamber flow produces the expected selections
- route identity from the token is preserved
- the resulting transport artifact contains the exact Chamber selections
- artifact type and version remain controlled by the shared bridge
- module, layer, origin trace, return slot, and package identity are retained
- an invalid or non-enabling token is rejected through the existing bridge rules

The tests therefore cover the full current seam:

```text
scripted Chamber interaction
-> typed Chamber result
-> bridge composition
-> stable Resonance Return Artifact
```

## Privacy and meaning boundary

The composer does not attempt to infer why a player chose an image, scent, movement, or word.

It carries only the selected public-safe forms and the structural route identity required for return.

```text
Private meaning shapes the selection.
The selection does not expose the private reason.
```

The composer also introduces no network behavior, tracking, account logic, social graph, or automatic delivery.

## Current limit

The composition path is executable and tested, but it is not yet a player-facing experience.

The current flow still uses `ScriptedChamberIO` for deterministic tests.

There is not yet:

- a terminal interaction adapter
- readable numbered menus
- input retry behavior
- a confirmation preview
- a local artifact-writing command
- an Atrium entry path into the Chamber

This is the correct current boundary.

The integration contract should remain stable before adding a user interface around it.

## Next recommended slice

The next small implementation slice is a terminal adapter for the existing `ChamberIO` protocol.

Suggested component:

```text
chambers/resonance/terminal_io.py
```

It should:

- display player-facing labels instead of internal IDs
- accept simple numbered selections
- reject invalid input clearly
- allow retry without restarting the Chamber
- collect the two single-word entries
- contain presentation behavior only

It should not:

- change compatibility rules
- build artifacts
- write files
- know about slots or rendering

After that adapter is tested, a thin command can connect:

```text
load token
-> create TerminalChamberIO
-> run composer
-> preview artifact
-> save once by explicit confirmation
```

## Working sequence

```text
Mechanism
-> contract
-> integration
-> interface
```

The first three steps now exist in executable form.

The next task is to make the existing grammar approachable without moving the grammar into the interface.

## Working formula

```text
Each Chamber keeps its grammar.
The Nexus keeps the route.
The composer keeps the seam narrow.
```

## Closing note

```text
The Chamber can now complete its grammar.
The result can now cross the boundary.
Next, the player must be able to enter without seeing the machinery.
```
