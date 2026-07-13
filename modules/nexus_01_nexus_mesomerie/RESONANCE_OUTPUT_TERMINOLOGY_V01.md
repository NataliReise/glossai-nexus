# Resonance Output Terminology V0.1

Status date: 2026-07-13

This note fixes the current terminology for the technical return object and the two player-facing poetic outputs of the Resonance Chamber.

## Core distinction

```text
Return Artifact
-> technical, transferable data object

Resonance Artifact
-> visible poetic long form

Nexus Echo
-> condensed poetic after-effect
```

The three terms describe related but distinct layers.

## Return Artifact

The Return Artifact is the technical object that carries the completed response back through the return chain.

It may contain:

```text
structured carried trace
structured answering response
stable ids
version information
matching metadata
rendering inputs
```

It remains part of the technical sequence:

```text
Resonance Token
-> Chamber Expression
-> Return Artifact
-> Slot Matching
-> Local Result
```

The Return Artifact is not itself the player-facing poem.

## Resonance Artifact

The Resonance Artifact is the visible poetic long form generated from the shared Resonance Composition after local opening.

It should:

```text
preserve all four resonance relations
remain close to the selected source material
show the joint authorship of both players
avoid hidden interpretation
remain calm, legible, and complete
```

Its source is:

```text
Resonance Composition
-> Resonance Artifact Renderer
-> Resonance Artifact
```

The Resonance Artifact preserves the shared resonance in readable form.

## Nexus Echo

The Nexus Echo is an additional, shorter poetic form generated from the same Resonance Composition.

For V0.1, the preferred form is the five-line `Nachhall` pattern:

```text
2 words
4 words
6 words
4 words
1 word
```

Its line functions are:

```text
1. image
2. movement
3. turning point
4. echo
5. aftersound
```

The Nexus Echo may select, condense, repeat, and transform approved motifs. It does not need to preserve every element of the composition.

It must not:

```text
explain the players
invent psychological meaning
introduce unrelated symbols
replace the chosen words with inferred themes
```

Its source is:

```text
Resonance Composition
-> Nexus Echo Renderer
-> Nexus Echo
```

## Shared architecture

```text
Resonance Composition
├── Resonance Artifact Renderer
│   └── Resonance Artifact
└── Nexus Echo Renderer
    └── Nexus Echo
```

The technical Return Artifact carries the structured material required for local opening. The local result may then reveal both poetic outputs:

```text
Return Artifact
-> local opening
-> Resonance Artifact
-> Nexus Echo
```

## Working formulas

```text
The Return Artifact carries.
The Resonance Artifact reveals.
The Nexus Echo remains.
```

```text
The players create the resonance.
The Resonance Artifact preserves it.
The Nexus returns an echo.
```

## Generator boundary

Both poetic outputs must be generated locally without AI or a language model.

They should share one curated language layer:

```text
stable ids
source text
approved render forms
relation metadata
```

The two renderers then use this material differently:

```text
Resonance Artifact Renderer
-> complete, restrained, transparent

Nexus Echo Renderer
-> selective, condensed, formally constrained
```

This means the project requires two renderers, but not two unrelated text systems.
