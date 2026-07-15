# Resonance V0.2 Prototype Composer Status V0.1

This document records the first executable experiment built from the reviewed
`mixed-threshold-return-world` building-block library.

The prototype remains isolated from the V0.1 production path.
It does not modify the Return Artifact schema, persistent opener, slot state,
production renderers, or archived language material.

## Implemented experiment

The executable file is:

```text
prototype_composer.py
```

It currently performs this sequence:

```text
load and validate prototype library
-> validate two free words without semantic interpretation
-> choose one weighted structural route
-> choose one compatible reviewed block per route role
-> render one long-form Resonance Artifact
-> verify free-word placement and resonance gains
-> derive one linked Nexus Echo from selected blocks and operators
-> validate 2 / 4 / 6 / 4 / 1
-> return visible texts plus inspectable Composition Plan
```

## Current boundaries

The composer supports only:

```text
world_id          mixed-threshold-return-world
completion_mode   converging-return
```

It is not a production renderer and does not claim coverage of the other two
prototype worlds or all 125 Chamber combinations.

## Randomness

The production concept permits fresh local randomness at first opening.
The prototype accepts an injected `random.Random` instance or a CLI seed so that
examples and failures remain reproducible during review.

```text
same library + same words + same seed
= same prototype result
```

No persistence is implemented in this experiment.
That belongs to a later integration stage after poetic review.

## Composition Plan

Each result records:

```text
library and world identity
completion mode
selected route
selected block IDs and roles
operators
resonant gains
remaining states
visible motifs
selected Echo line IDs
inherited lexical trace
wish-word Echo line
```

The plan stores compositional provenance, not hidden human meaning.

## Echo derivation

The Echo candidate pool is filtered by the actual completed long-form plan.
Candidates may require:

```text
selected source block IDs
visible motifs
inherited operators
```

A middle-line combination is accepted only when:

```text
exactly one middle line contains the wish word
one concrete phrase of at least two words is shared with the long form
all Echo word counts are valid
line 5 consists only of the return word
```

This is deliberately stricter than free thematic resemblance.

## Local validation performed before commit

The prototype was syntax-checked and exercised locally against a complete
in-memory reconstruction of the current JSON building-block library.

One review run used 100 deterministic seeds with `Hope` and `Spirit`.
It produced:

```text
100 structurally valid compositions
98 distinct long forms
48 distinct Nexus Echoes
```

These figures describe only that local experiment.
They are not a literary-quality score and not a guarantee of future production
variety.

The local checks also exercised difficult free words such as:

```text
Blue
Perhaps
Hush
Return
```

The executable test file is:

```text
test_prototype_composer.py
```

It checks:

```text
seed reproducibility
variation across seeds
exact Echo word counts
wish and return placement
long-form free-word uniqueness
presence of a required resonant gain
rejection of invalid free-word shapes
calm failure for a missing library
```

## Known limitations and first review questions

### 1. Blocks are currently selected independently inside a valid route

The first prototype filters by active tags and completion mode, but it does not
yet model detailed pairwise block exclusions or phrase-family repetition limits.
Generated examples must therefore be inspected for local redundancy and tonal
collisions.

### 2. Echo linkage is lexical but still library-authored

The Echo inherits an actual phrase from the long form, but its candidate lines
remain curated templates. This is intentional for the first experiment, though
later review must determine whether the resulting Echoes feel sufficiently born
from the exact long form rather than merely licensed by it.

### 3. Motif coverage is aggregated rather than assigned by profile family

The plan records visible motifs, but the first executable version does not yet
prove separately that one image-profile motif and one scent-profile motif are
present. The current world usually supplies both through its route roles, but a
future validator should make that family-level coverage explicit.

### 4. Text remains line-based

The prototype chooses complete reviewed lines. It does not yet compose smaller
phrase units within a line. This protects grammatical quality but may reveal a
recognisable template surface when the library is used repeatedly.

### 5. No persistence or production integration

The experiment does not save completed results, update Return Slots, or interact
with the existing opener. This separation is intentional until the generated
texts have received human poetic review.

## Current conclusion

The first executable experiment demonstrates that the library contract can be
translated into a small transparent machine without semantic word analysis.

```text
The generator does not understand the poem
It follows curated permissions and prohibitions
```

The next decision should be based on generated examples rather than additional
schema design alone.
