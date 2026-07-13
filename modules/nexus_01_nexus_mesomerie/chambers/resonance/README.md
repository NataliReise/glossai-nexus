# Resonance Chamber

This package contains the Chamber-specific mechanics for the Nexus 01 Resonance Chamber.

It owns:

- the order of Chamber decisions
- the visible choice labels
- compatibility between source and response choices
- the Chamber flow
- scripted interaction for deterministic tests

It does not own:

- Resonance Token validation
- Return Artifact transport identity
- Return Slot matching
- poetic rendering
- local result persistence

The package returns one typed `ChamberSelections` value through the existing shared bridge contract.

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
```
