# Module concept: Nexus 01 - Nexus-Mesomerie

Status: concept seed

Subtitle / start motif: *INSERT RESPONSE*

## Short description

**Nexus 01 - Nexus-Mesomerie** is planned as a retro-terminal escape module for a single player or a team.

The Nexus itself is the object of play. Players encounter an activated but not yet fully aligned Nexus and learn its structure by exploring it.

By playing, they discover what a Nexus is: an open software artifact that can be played at the surface, read in the depth, configured through activations, and connected to other activations through human action and carried traces.

## Core play question

What does it mean to open a Nexus?

Possible in-game questions:

- What is this artifact?
- Why is it open?
- What is an activation?
- What is a trace?
- What is the difference between access and resonance?
- How can a connection be carried without hidden connectivity?
- What kind of result should this activation open?

## Intended play style

Nexus 01 should be:

- local-first,
- playable without an internet connection,
- playable without reading code,
- richer when players choose to inspect the code,
- suited for single-player or team play,
- puzzle-oriented rather than purely narrative,
- small enough to finish, but deep enough to reward curiosity.

## Possible interface

The first implementation may use a retro terminal style.

A small Nexus command language may be discovered during play.

Possible commands:

- `help`
- `status`
- `scan`
- `read`
- `connect`
- `rotate`
- `echo`
- `unlock`
- `carry`

These commands are provisional.

## Activation concept

A module contains the shared open structure.

An activation contains the concrete situational configuration.

For Nexus 01, an activation may configure:

- result type,
- play mode,
- difficulty,
- code layer,
- quest traces,
- fragment set,
- tone,
- optional private message,
- optional pass-on or Hall of Resonance behavior.

Private activation data should not be published by default.

## Planned result types

Nexus 01 may eventually support several result types.

### `message_unlock`

Unlocks a personal message, gift note, dedication, or invitation.

### `quest_trace`

Unlocks a general lore or quest trace.

### `action_prompt`

Invites players to take a voluntary action after play.

### `pass_on`

Creates or reveals a non-private pass-on trace that can be carried to another person.

### `return_trace`

Allows a trace from another activation to unlock an additional result.

### `hall_entry`

Creates a local draft entry for the Hall of Resonance.

No result should be uploaded or shared automatically.

## Possible fragment set

A first fragment set may contain five main fragments and two optional deeper fragments.

Possible fragments:

- access,
- boundary,
- openness,
- conflict,
- response,
- responsibility,
- resonance.

The final set is not decided yet.

## Spoiler and code design

Nexus 01 should follow the general play guide in `docs/PLAYING_A_NEXUS.md`.

It should distinguish between:

- surface play,
- open code,
- trace areas,
- spoiler-marked areas,
- activation data.

The main path should be playable without reading code.

Reading code may reveal additional traces, hints, or meanings, but should not simply reduce the module to a trivial answer file.

## Data and network principles

Nexus 01 should be local-first.

Its core play experience should work without an internet connection.

If activations connect, they should do so through traces that people choose to carry: resonance keys, shared files, returned codes, pull requests, Hall of Resonance entries, or other voluntary acts of exchange.

Personal data should be minimized. Aliases and local files should be preferred over real names or automatic sharing.

## Open questions

- What is the strongest central play objective: align the Nexus, open the answer channel, reconstruct a signature, or something else?
- Which commands belong to the first version of the Nexus command language?
- Which result types should be implemented first?
- Should the first playable version include `pass_on` and `hall_entry`, or only prepare them conceptually?
- How difficult should the first gift activation be?
- How strongly should Roman/blog connections be visible in the first module?
