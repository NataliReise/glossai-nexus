# Resonance Chamber

This package contains the Chamber-specific mechanics for the Nexus 01 Resonance Chamber.

It owns:

- the order of Chamber decisions
- the visible choice labels
- compatibility between source and response choices
- the Chamber flow
- scripted interaction for deterministic tests
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

This first seed is intentionally deterministic and UI-independent. A terminal adapter may be added later without moving interaction rules into the CLI.

```text
Each Chamber keeps its grammar.
The Nexus keeps the route.
The composer keeps the seam narrow.
```
