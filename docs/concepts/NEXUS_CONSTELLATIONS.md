# Nexus Constellations

## Status

This document defines a conceptual bridge between Nexus module lines, complete chambers, Atrium behaviour, shared runtime concerns, and archive material.

It is intentionally architectural and narrative. It does not require a code refactor before the current Nexus 01 milestone is complete.

## Core idea

A Nexus module is not merely a collection of files and not merely a sequence of screens.

It is a **constellation**: a concrete arrangement of complete chambers, thresholds, transitions, shared line infrastructure, and optional orientation or archive layers.

> A constellation is the form taken by a Nexus when its chambers meet.

The same chamber may appear in more than one constellation without becoming identical to the constellation around it.

## Complete chambers

A chamber should remain a coherent experiential and functional unit.

It may use shared line infrastructure, but it should retain ownership of the complete process that gives the chamber its meaning.

For the Resonance Chamber, this means that the chamber conceptually owns the whole resonance journey, including:

- originating composition
- sensory and symbolic choices
- wish word and return word
- token creation
- invitation preparation
- manual transfer boundaries
- answer flow
- Return Artifact creation
- local matching
- Nachhall generation
- persistence and revisit behaviour
- cancellation, privacy, and publication rules

These responsibilities may be implemented across several internal files and services. They still belong to one chamber contract from the perspective of the constellation.

> A chamber may have many internal systems and still remain one complete room.

## Docking and thresholds

A useful architectural image is a modular station.

Each chamber keeps its own interior while exposing a compatible threshold through which it can join a larger Nexus.

A threshold may describe:

- how the chamber can be entered
- which states it accepts
- which public outcomes it provides
- which transitions it supports
- which shared line services it needs
- which navigation information it chooses to reveal
- which compatibility version it follows

Thresholds are not permission for other chambers to inspect private interiors.

> A Nexus grows by docking complete chambers, not by dissolving them into one system.

## Constellation and module line

A module line defines compatible possibilities.

A constellation selects and arranges some of those possibilities.

For example, Nexus-Mesomerie may eventually define compatible chamber contracts, line services, privacy rules, artifact identities, and packaging conventions.

A particular Nexus-Mesomerie module might then form a constellation such as:

```text
First Spark -> Atrium -> Resonance Chamber
```

Another may be:

```text
First Spark -> Resonance Chamber
```

A larger constellation may be:

```text
                 Archive Threshold
                        |
First Spark -> Atrium -> Resonance Chamber
                        |
                 Unknown Chamber
```

The module line does not prescribe one permanent arrangement.

## The Atrium

The Atrium is a possible orientation and docking space within a constellation.

It should not be treated as the owner of every chamber or as the universal controller of Nexus.

A future Atrium may discover the chambers present in a constellation and read only the navigation metadata that those chambers explicitly expose.

Possible Atrium-facing metadata may include:

- public title
- door label
- short orientation text
- visibility
- public availability state
- public-safe status message
- ordering or grouping hints
- accessibility presentation
- entry action
- permitted return path

The Atrium must not infer private chamber state from internal files or artifacts.

For example, a Resonance Chamber may expose:

```text
A return is waiting.
```

It must not expose the private answer, wish word, return word, carried message, or generated artifact unless the chamber explicitly presents that material inside its own experience.

> The Atrium does not define the chambers.
> It listens for the doors they choose to reveal.

## Atrium as role and presentation

The Atrium need not always appear as the same interface.

The same public navigation surface might be rendered as:

- a retro terminal room
- a textual list of doors
- a graphical map
- an audio environment
- a physical installation
- a conversational guide
- an accessibility-first navigation layer

A constellation may also omit an Atrium entirely when its route is linear or when another orientation form is more appropriate.

There may eventually be more than one Atrium-like node in a large constellation.

## Transitions

A transition is a permitted movement between chamber states or chamber thresholds.

Transitions should belong to the constellation rather than being hidden entirely inside the Atrium.

This allows:

- direct chamber-to-chamber paths
- branching routes
- conditional openings
- revisits
- multiple orientation nodes
- constellations without an Atrium

A transition may depend on public state, completed actions, available artifacts, activation mode, or explicit visitor choice.

Private content should not become a transition condition unless the owning chamber safely reduces it to an appropriate public state.

## Shared line infrastructure

Some capabilities belong neither to one chamber nor to the visible Atrium.

A module line may provide shared infrastructure such as:

- activation and mode selection
- local persistence
- route and artifact identity
- package validation
- safe path handling
- public/private separation
- shared cancellation conventions
- accessibility support
- module discovery
- chamber loading

A chamber may use these services while retaining ownership of its domain-specific journey.

The shared runtime supports the constellation. It should not become a hidden all-knowing chamber.

## Archive material within a constellation

The Nexus Archive is a narrative and explanatory layer, not necessarily one universal chamber.

A constellation may expose archive material in several ways:

- an Archive Chamber
- an Archive Threshold in the Atrium
- chamber-specific archive fragments
- optional deeper entries reached from help or lore
- traces unlocked after an encounter
- a separate local archive surface

No single constellation needs to contain the whole archive.

Archive material may describe chambers, module lines, old paths, Resonance Nodes, recurring symbols, or partial records of prior constellations.

The archive should explain Nexus from within its own world. It should not reveal outer fictional framing, repository history, private visitor material, or technical secrets that belong to another narrative layer.

> No visitor has seen the whole archive.

## Ownership boundaries

A healthy constellation keeps several responsibilities distinct:

### Chamber-owned

- the chamber's complete meaningful process
- chamber-specific state
- private content
- domain-specific validation
- chamber artifacts and public-safe summaries
- Atrium-facing metadata chosen by the chamber

### Constellation-owned

- which chambers are present
- how thresholds connect
- permitted transitions
- initial route
- optional Atrium placement
- optional archive access
- module-level atmosphere and composition

### Module-line-owned

- compatibility contracts
- shared services
- packaging and validation conventions
- privacy and publication principles
- common identity rules

### Presentation-owned

- how public navigation and public chamber metadata are rendered
- terminal, graphical, audio, physical, or other interface forms

These boundaries may evolve, but they provide a useful first map.

## Implications for a future Module Builder

A future Module Builder should compose constellations rather than merely copy a fixed directory tree.

It may eventually help a person choose:

- a module line
- complete chambers
- one or more Atrium or orientation forms
- transitions and branching
- archive material
- presentation style
- packaging target

The builder should then validate that chamber thresholds are compatible and that private material remains inside the owning chamber.

It should not flatten all chambers into one generated controller.

## Relationship to the inner story

Within the Nexus inner story, a constellation is less a software graph than a family of rooms whose thresholds have met.

> Each chamber keeps its own interior.
> Nexus begins where their thresholds meet.

A constellation may change without erasing the chambers that formed it.

A chamber may return elsewhere, joined to different paths, carrying traces of earlier arrangements without becoming bound to them.

## Not part of the current Sunday scope

This document records direction only.

Before the current milestone, the project should not require:

- automatic chamber discovery
- runtime manifest loading
- generalized transition engines
- Atrium metadata contracts
- archive integration into the playable flow
- a Module Builder

The current tested Nexus 01 flow should remain stable.

## Later exploration sequence

After the current milestone, a careful exploration may proceed in this order:

1. map the current First Spark, Atrium, and Resonance responsibilities
2. identify the complete Resonance Chamber boundary
3. distinguish chamber-owned logic from Mesomerie line services
4. define a minimal public threshold contract
5. define the smallest safe Atrium metadata surface
6. model the current playable route as one explicit constellation
7. create a second meaningfully different constellation
8. revise contracts from both examples
9. only then prototype automatic docking or a Module Builder

## Guiding principles

> A Nexus grows by docking complete chambers, not by dissolving them into one system.

> The Atrium does not define the chambers. It listens for the doors they choose to reveal.

> Each chamber keeps its own interior. Nexus begins where their thresholds meet.
