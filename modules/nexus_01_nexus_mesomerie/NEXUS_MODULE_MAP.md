# Nexus Module Map

Project: **glossAI Nexus**  
Module context: **Nexus 01 – Nexus-Mesomerie**  
Document status: First map of the possibility space

---

## 1. Purpose of this Map

This document is a map of the larger possibility space around Nexus modules.

It is not a task list for Version 1.

It exists to separate two things:

1. the long-term modular Nexus system,
2. the small first playable slice.

This helps keep the first implementation small without losing the larger idea.

Guiding distinction:

> The map may be wide.  
> The first path must be narrow.

---

## 2. Overall Nexus Architecture

A Nexus module can be understood as a configurable software game artifact.

Its long-term architecture may include:

- module type,
- activation mode,
- activation purpose,
- play mode,
- activity flow,
- shared game state,
- result or unlock type,
- optional return or resonance layers,
- optional after-play traces,
- optional social connection points.

The current core model:

```text
Nexus Module
  ├─ Module type
  ├─ Activation
  │   ├─ mode
  │   └─ purpose
  ├─ Play mode
  ├─ Activity flow
  ├─ Game state
  ├─ Result / unlock layer
  └─ After-play options
```

The first playable slice will use only a small part of this model.

---

## 3. Module Types

A module type describes the general style and base structure of a Nexus module.

### 3.1 `terminal_escape_nexus`

Terminal-style commands, virtual files, logs, fragments, unlocks.

This is the type intended for Nexus 01.

### 3.2 `text_choice_nexus`

Interactive text, guided choices, branching narrative fragments.

### 3.3 `git_trace_nexus`

Git history, commits, branches, issues, discussions, and repository traces become part of the play space.

### 3.4 `cipher_grid_nexus`

Grids, coordinates, ciphers, layered reading paths.

### 3.5 `dialogue_reflection_nexus`

Dialogue prompts, reflection notes, group play, workshop-like structures.

For now, only `terminal_escape_nexus` belongs to the first implementation path.

---

## 4. Activity Types

Activities are small internal play modules.

They can be chained, skipped, or configured.

Possible activity types include:

- `boot_sequence`
- `mini_language_lesson`
- `file_inspection`
- `log_trace`
- `fragment_connection`
- `choice_node`
- `cipher_layer`
- `message_or_lore_unlock`
- `resonance_code_generation`
- `return_key_generation`
- `encrypted_return_gate`
- `resonance_note_generation`
- `hall_entry_draft`
- `contact_node_draft`

Nexus 01 should start with only a small subset.

---

## 5. Activation Modes

Activation modes describe how a Nexus becomes playable.

### 5.1 `module_only`

The module exists as open source structure.

It is readable and inspectable, but not yet playable as a concrete run.

### 5.2 `neutral_activation`

A playable activation without personal recipient or gift purpose.

Typical result:

- `lore_unlock`

### 5.3 `personal_activation`

A playable activation for a person, team, occasion, or relationship context.

Typical result:

- `message_unlock`

### 5.4 Gift Activation

A gift activation is not a separate activation mode.

It is a `personal_activation` with:

```json
"purpose": "gift"
```

The game may show visible personalization from the beginning, while the actual gift message remains locked until the player completes the module.

### 5.5 `carried_activation`

A carried activation starts with a resonance code from another completed run.

It belongs to the larger resonance model and is not required for the first playable slice.

### 5.6 `return_input`

A later return action inside an origin activation.

It is used to enter a return key and may unlock a return layer.

This is not required for the first playable slice.

---

## 6. Activation Purposes

Activation purpose describes why this activation exists.

Possible purposes:

- `public_play`
- `gift`
- `personal_resonance`
- `workshop`
- `learning_context`
- `community_play`
- `module_test`
- `artistic_prompt`

For the first playable slice, only `gift` is needed.

---

## 7. Play Modes

Play mode describes how the module is played.

Possible play modes:

- `solo`
- `team_play`

`team_play` is not a purpose. It is a way of playing.

For the first playable slice, `solo` is enough.

---

## 8. Result and Unlock Types

Possible result or unlock types:

- `message_unlock`
- `gift_message`
- `personal_note`
- `lore_unlock`
- `resonance_code`
- `return_key`
- `encrypted_return_layer`
- `resonance_note`
- `hall_entry_draft`
- `contact_node_draft`

For the first playable slice, only the gift message unlock is required.

A resonance code may remain a later or optional feature.

---

## 9. Social Resonance Features

The larger Nexus vision may include social resonance features.

These are not automatic network features.

They are voluntary traces carried or shared by people.

Possible features:

- pass-on resonance code,
- carried activation,
- return key,
- encrypted returned layer,
- Hall of Resonance draft,
- GitHub Discussion contact node,
- resonance note,
- module fork seed,
- future module templates.

For the first playable slice, these are parked.

Important principle:

> The social network is not hidden digital connectivity.  
> It grows through human interaction and carried traces.

---

## 10. Configuration Dimensions

A Nexus configuration may vary along several dimensions:

- module type,
- activation mode,
- activation purpose,
- play mode,
- enabled activities,
- activity order,
- virtual files or fragments,
- player-facing tone,
- visible personalization,
- result type,
- after-play options.

For the first playable slice, configuration should remain minimal.

The only required configuration dimensions are:

- `activation.mode = personal_activation`
- `activation.purpose = gift`
- `play.mode = solo`
- a short activity flow
- one gift message result

---

## 11. Future Expansion Paths

Possible later expansions:

- neutral lore activation,
- carried activation,
- return key generation,
- encrypted return layer,
- Hall of Resonance,
- contact nodes in GitHub Discussions,
- team play,
- additional activity types,
- additional module types,
- module templates,
- module creation guide,
- browser-based interface,
- accessibility improvements,
- translations.

These are part of the map, not part of the immediate build.

---

## 12. First Playable Slice: Nexus 0.1 – First Spark

The first playable slice should be called:

**Nexus 0.1 – First Spark**

It is the smallest useful playable version inside the larger Nexus 01 concept.

It should prove only this:

> A person can start a small terminal-style Nexus, learn a tiny command language, inspect a few virtual traces, connect fragments, and unlock a personal gift message.

Included:

- `terminal_escape_nexus`
- `personal_activation`
- `purpose = gift`
- `play.mode = solo`
- `boot_sequence`
- `mini_language_lesson`
- `file_inspection`
- `fragment_connection`
- `gift_message_unlock`
- very small `game_state`

Parked for later:

- `neutral_activation`
- `carried_activation`
- `return_key_generation`
- `encrypted_return_layer`
- Hall of Resonance
- GitHub contact nodes
- multiple module types
- complex activity graph
- advanced configuration

Working boundary:

> First Spark is not the full Nexus.  
> It is the first visible spark of the Nexus idea.
