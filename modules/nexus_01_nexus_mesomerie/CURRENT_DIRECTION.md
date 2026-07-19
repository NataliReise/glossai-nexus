# Nexus 01 Current Direction

Status: current implementation direction

Decision date: 2026-07-17

This document is the primary source of truth for the current development direction of Nexus 01.

When an older design, status, audit, or experiment document conflicts with this file, this file takes precedence until a newer current-direction document explicitly replaces it.

## Current play grammar

Nexus 01 is a line of local retro-terminal escape modules.

Its Chambers may serve very different purposes and use very different mechanics.
Their shared identity does not come from repeating the same puzzle. It comes from
a common exploration-based play grammar:

```text
perceive the Chamber
-> explore its surroundings
-> discover and read traces
-> infer the local vocabulary
-> request layered guidance when desired
-> act
-> observe how the Chamber changes
```

Atmospheric Chamber text presents the space, its mood, its perceptible traces,
and its changes. It should not routinely explain the complete mechanic in advance.

Mechanical orientation is revealed through the Chamber's discoverable local
command language, its traces, optional help, and, where appropriate, the
Chamber's voice.

The shared support levels are:

- `help` explains the current local vocabulary and available action types;
- `trace` offers gentle, state-aware orientation toward a useful next step;
- `walkthrough` reveals the complete remaining path after a spoiler warning.

These layers are not auxiliary documentation or optional polish. They are part of
the core gameplay of the current Nexus 01 module line.

A Chamber may guide, compose, unlock, connect, transform, or reveal something
entirely different from another Chamber. What makes it part of this module line is
the way it allows its world and its rules to be discovered.

Working formula:

> The Chambers differ in what they do.
> They belong to the Nexus 01 module line through the way they allow themselves
> to be discovered.

## Exploration-first terminal principle

The following is a binding construction principle for corrected Atrium and
corrected Resonance. It is the confirmed target direction; it is not yet fully
implemented.

- A room describes itself and its current state.
- Entering a room never starts a productive action automatically.
- `/look` repeats only the room and state description.
- `/help` reveals the currently available actions.
- Full command lists do not appear automatically in room descriptions.
- Unknown input receives a calm short response and may point to `/help`.
- Productive actions begin only after an explicit command.
- Help and the local dispatcher should derive from the same small room-local
  capability source.
- Unavailable actions remain hidden instead of being advertised as disabled.
- No Nexus-wide general command framework is required.

First Spark is an existing design precedent for this exploration-first
principle. Legacy remains an isolated compatibility path and is not part of the
first Surface migration.

## Current resonance decision

The complete visible production resonance result of Nexus 01 is a compact
**Nachhall** poem.

```text
2 words
4 words
6 words
4 words
1 word
```

Words are whitespace-separated units. Attached punctuation does not add a
word, and a hyphenated form without whitespace is one word.

The compact poem is not a secondary Echo derived from a mandatory long-form poem. It is the complete poetic resonance form itself.

```text
human Chamber choices
+ wish word
+ return word
+ curated poetic profiles
+ small micro-routes
+ curated phrase variants
+ local first-opening selection
= one persistent Nachhall
```

## Current poetic principles

- The poem may remain partially enigmatic.
- Metaphorical openness is desirable when the poem retains an internal movement and at least one concrete or sensory anchor.
- The selected image, scent, and movement shape the poetic field without needing to be named literally.
- The wish word appears exactly once in line 2, 3, or 4.
- The return word appears exactly once as line 5.
- The composer performs no semantic analysis of either free word.
- Variation comes from curated micro-routes and reviewed phrase families rather than unrestricted grammar generation.
- Strong fixed lines may remain available as rare curated forms.
- The result is generated once at the first successful local opening and then reopened unchanged.

## Current technical principles

The following existing Nexus responsibilities remain valuable:

- First Spark and the human activation movement;
- the Resonance Chamber choices and responses;
- stable transport and route identity;
- Return Slot matching;
- local-only opening;
- create-once and revisit-often persistence;
- no-overwrite behaviour;
- explicit validation and calm failure;
- public and private data separation;
- strict five-line and word-count validation.

The current redesign is therefore a replacement of the visible poetic production layer, not a rejection of the entire Nexus structure.

## Superseded production directions

### V0.1 exact complete paths

The deterministic V0.1 Nachhall paths remain valuable historical references and poetic source material. They are no longer intended to be the universal production model because every supported Chamber combination would require an exact prewritten path.

### V0.2 long-form block composer

The V0.2 long-form experiment remains valuable design evidence. It demonstrated local weighted composition, linked Echo derivation, inspectable plans, signature risks, and anti-formula concerns.

It is no longer the intended production target. Nexus 01 will not require a long-form Resonance Artifact before producing its final Nachhall.

## Production implementation and experimental lineage

The production implementation lives in:

```text
return_resonance/compact_generator.py
open_resonance_return.py
```

The earlier compact-composition experiment remains as design and review
lineage in:

```text
experiments/nachhall_composition_v0_3/
```

It is not the active production path.

## Repository status language

Relevant files and directories should be classified as one of:

```text
CURRENT
ACTIVE_EXPERIMENT
RETAIN
REUSE_OR_EXTRACT
SUPERSEDED
ARCHIVE_AFTER_DEPENDENCY_REVIEW
REMOVE_FROM_HEAD_LATER
UNDECIDED
```

`SUPERSEDED` does not mean worthless. It means that the file must not be read as current implementation guidance.

## Transition rule

No historical runtime code, test, or data directory should be moved merely for tidiness before imports, fixtures, documentation links, and test commands have been reviewed.

The completed replacement followed this safe order:

```text
document current direction
-> classify the repository
-> build and test the compact experiment in parallel
-> confirm the replacement path
-> update active imports and documentation
-> enforce the accepted production contract
-> archive superseded systems in one controlled migration
-> run active tests and archive-reference checks
```

## Compact project formula

```text
The people create the resonance
The Nexus gives it one small form
The form remains open enough to echo
```
