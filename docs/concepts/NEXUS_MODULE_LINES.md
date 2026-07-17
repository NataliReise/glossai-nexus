# Nexus Module Lines

## Status

This document records a future architectural direction for **glossai-nexus**.

It is intentionally conceptual. It does not authorize or require a restructuring of the current code before the present Nexus 01 milestone is complete.

## Why module lines

A Nexus module does not need to be a one-off implementation.

A module line may define a family of compatible chambers, shared principles, reusable infrastructure, and characteristic forms of interaction. Different Nexus modules may then be composed from these parts in different arrangements.

A module line is therefore not one finished game. It is a space of possible Nexus modules.

## Working terms

### Module line

A family of Nexus modules that share a recognizable design logic, compatible chamber contracts, and common infrastructure.

A module line may define:

- characteristic forms of play and interaction
- reusable chamber building blocks
- shared state, artifact, and transfer conventions
- privacy and publication boundaries
- validation and packaging rules
- narrative motifs or atmospheric tendencies
- optional construction guidance

A module line does not require every module to look or feel identical.

### Chamber building block

A reusable chamber or chamber-capable component with a defined interface to the surrounding module line.

A chamber building block may declare:

- what it needs
- what it provides
- which states it can enter or leave
- which artifacts or traces it may produce
- which transitions it supports
- which line versions it is compatible with

Its internal implementation may remain independent from other chambers.

### Nexus module

A concrete constellation of chambers, transitions, content, atmosphere, and line infrastructure.

A module may use familiar chambers, introduce new ones, or arrange known chambers in a different sequence or topology.

### Playable slice

A stable and playable stage within a module line or module.

A playable slice may be smaller than the eventual full module while still being coherent, testable, and meaningfully usable.

## First module line

**Nexus 01 — Nexus-Mesomerie** is the first module line in the glossai-nexus project.

Its first stable playable slice is:

**Nexus 0.1 — First Spark**

First Spark is currently a local retro-terminal escape experience and the first working example of the Mesomerie line.

It should not become an accidental universal template for every future Nexus module.

## What may belong to Nexus-Mesomerie

The current implementation suggests that the Mesomerie line may eventually include shared conventions for:

- local-first execution
- readable and inspectable software artifacts
- chambers that support play, discovery, communication, and response
- voluntary manual transfer
- public/private separation
- carried traces, invitations, return slots, and local results
- stable identities for routes and artifacts
- generate-once and revisit-often behaviour
- explicit cancellation and non-automatic publication
- deterministic results at important boundaries

These are observations from the current codebase, not a final line specification.

## Current code as a reference implementation

The existing Nexus 01 code should be treated as a valuable first reference implementation, not as disposable prototype code.

It already contains several separable concerns:

- chamber logic
- Atrium and navigation logic
- activation and mode selection
- token and artifact models
- invitation publication
- private Return Workspaces
- persistence and local matching
- tests for privacy, identity, cancellation, and determinism

A future restructuring would mainly extract and formalize these existing boundaries.

It should not begin by rewriting the project from scratch.

## Future chamber contracts

A later Mesomerie specification may define a minimal chamber contract or manifest.

Such a contract could describe, for example:

```yaml
id: resonance
line: nexus-mesomerie
version: 0.1
entrypoint: chambers.resonance
requires:
  - activation
provides:
  - resonance_invitation
  - resonance_return
modes:
  - compose
  - answer
```

This example is illustrative only. No manifest format has been selected.

A chamber contract should make composition possible without forcing all chambers to share the same internal implementation.

## Complete chamber ownership

A chamber should own the complete experience and process that gives it meaning, even when it uses shared line infrastructure internally.

For the Resonance Chamber, this means that the chamber boundary should include the complete resonance journey rather than only the visible conversation step. Its responsibility may include:

- composing the originating resonance
- image, scent, and movement choices
- wish and return words
- Resonance Token creation
- route and artifact identities
- travelling invitations
- private Return Workspaces
- answer and return flows
- Return Artifacts
- local matching and persistence
- Nachhall generation and reopening
- cancellation, privacy, and publication rules

Shared services may still provide storage, activation, packaging, identity, or state support. The semantic ownership of the resonance process remains with the Resonance Chamber.

> The Resonance Chamber owns the complete resonance journey, even when parts of that journey use shared line infrastructure.

## Docking model and the Atrium

A useful architectural image is a modular station whose complete chambers dock through compatible thresholds.

Each chamber keeps its own interior, purpose, and implementation. It does not need to dissolve into one large central system in order to belong to a Nexus. What must remain compatible are the thresholds: the contracts through which chambers are discovered, entered, left, and connected.

This resembles a station assembled from complete docked modules:

- a chamber is a complete functional module
- a threshold is a compatible docking interface
- a constellation is the current arrangement of docked chambers
- an Atrium is a possible hub or connecting module
- line infrastructure supports the station without owning every chamber's meaning

> A Nexus grows by docking complete chambers, not by dissolving them into one system.

### Atrium metadata

A future Atrium may discover available chambers automatically and read only the metadata that those chambers explicitly expose for navigation.

A chamber might publish a public navigation surface such as:

```yaml
atrium:
  visible: true
  label: Enter Resonance
  description: Begin or answer a carried resonance.
  order: 20
  public_status: waiting
```

The exact format remains undecided.

The Atrium may use such metadata to determine:

- which chambers are docked
- which thresholds are visible
- which paths are currently available
- which public-safe status may be shown
- how a chamber names or describes its entrance
- how the current constellation should be presented

The Atrium must not inspect private chamber state merely because it can launch the chamber. A Resonance Chamber may reveal that a return is waiting without exposing a wish word, return word, private message, or artifact content.

> The Atrium does not define the chambers. It listens for the doors they choose to reveal.

### Atrium as role rather than fixed interface

The Atrium need not always be one terminal screen or one permanent central room.

Its deeper role may be to make several possible paths perceptible. Different implementations could render the same public chamber metadata as:

- a retro-terminal hub
- a graphical map
- an accessible text menu
- an audio environment
- a spatial installation
- a physical connecting object

Some constellations may have no Atrium. Others may contain several connecting hubs. The Atrium should therefore remain a possible docking and orientation form, not the universal owner of Nexus.

> Each chamber keeps its own interior. Nexus begins where their thresholds meet.

## Construction guides

Each mature module line may eventually provide a construction guide describing:

- which principles define the line
- which chambers are available
- how chambers communicate with line infrastructure
- how transitions and states are declared
- how artifacts move through the module
- how privacy rules are preserved
- how modules are validated, tested, packaged, and published
- what may be changed freely
- what must remain compatible

This guide should support both experienced developers and people learning the project.

## A future module builder

A future Module Builder may make it possible to compose a Nexus module without writing all of its code manually.

It might allow a person to choose:

- a module line
- a set of chambers
- a sequence or branching structure
- transfer and return behaviour
- atmosphere and presentation
- optional archive material
- packaging targets

The builder might then generate:

- a project structure
- chamber registration
- configuration and manifests
- transitions and placeholders
- tests
- documentation
- packaging scaffolding

The builder should help people compose rather than merely reproduce one fixed module.

For that reason, it should not be designed from First Spark alone. At least two meaningfully different module constellations should inform the first serious builder design.

## Different technologies remain possible

A Nexus module does not need to use the same interface, programming language, or technical framework as First Spark.

Future module lines may use entirely different technologies. Even modules within one line may eventually allow multiple compatible implementations when the line contract makes that safe.

Shared identity should come from principles and contracts, not from mandatory imitation of one user interface or one programming language.

## Relationship to the inner story

On the technical project level, module lines describe reusable architectures and construction practices.

Within the Nexus inner story, they may appear more like families of paths or recurring forms of constellation:

> A chamber may return in another Nexus,
> surrounded by different rooms and opening different paths.
>
> A new Nexus does not need to resemble the first one
> in order to belong to the same journey.

The inner story does not need to know about manifests, registries, builders, or programming languages directly.

## Not part of the current Sunday scope

This direction should be preserved now but implemented later.

Before the current milestone, the project should not introduce a broad refactor for:

- chamber registries
- declarative manifests
- generalized line runtimes
- module generation
- cross-language chamber contracts
- automatic Atrium discovery

The current playable and tested flow should remain stable.

## Suggested later sequence

After the current milestone, a careful exploration may proceed in this order:

1. map the existing Nexus 01 architecture
2. distinguish Mesomerie line infrastructure from First Spark-specific behaviour
3. define the smallest useful chamber contract
4. define a minimal public Atrium metadata surface
5. package one existing chamber against that contract
6. build a second, deliberately different module constellation
7. revise the contract from both examples
8. only then prototype a Module Builder

## Guiding principle

> First Spark is the first path through Nexus-Mesomerie.
> It is not the border of what Nexus-Mesomerie may become.
