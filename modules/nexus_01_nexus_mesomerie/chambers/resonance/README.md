# Resonance Chamber

This package contains the Chamber-specific mechanics for the Nexus 01 Resonance Chamber.

It owns:

- the order of Chamber decisions
- the visible choice labels
- compatibility between source and response choices
- the Chamber flow
- scripted interaction for deterministic tests
- a human-facing terminal adapter
- a thin composer at the Chamber boundary

It does not own:

- Resonance Token loading or schema validation
- Return Slot matching
- poetic rendering
- local result persistence
- Atrium state

The mechanical flow returns one typed `ChamberSelections` value.

The boundary composer then joins that value to validated route identity by delegating to the existing shared bridge:

```text
ResonanceToken + ChamberIO
-> ResonanceChamberFlow
-> ChamberSelections
-> build_resonance_return_artifact
-> ResonanceReturnArtifact
```

The composer does not write files, render poetry, open a Return Slot, or alter Nexus state.

Current V0.1 flow:

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

`TerminalChamberIO` presents only numbered player-facing labels. Internal IDs remain behind the interaction boundary. Invalid numbers and invalid word entries are retried locally without changing the Chamber flow.

This first adapter is intentionally small. It makes the existing grammar playable in a terminal, but it does not yet load a token, preview an artifact, ask for final confirmation, or save a file. Those responsibilities belong to a later thin command-line entry point outside the Chamber package.

```text
Each Chamber keeps its grammar.
The Nexus keeps the route.
The composer keeps the seam narrow.
The interface keeps the machinery out of sight.
```
