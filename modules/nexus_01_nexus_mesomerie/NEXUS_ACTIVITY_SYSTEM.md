# Nexus Activity System

Project: **glossAI Nexus**  
Module context: **Nexus 01 – Nexus-Mesomerie**  
Document status: First architecture note  

---

## 1. Purpose

This document describes the inner modular structure for Nexus modules.

The goal is to make Nexus 01 flexible enough to support different activation types and play experiences without turning the first module into an oversized project.

Nexus 01 should stay small.

At the same time, its structure should already point toward a reusable modular system that can later support other Nexus modules and module types.

Core idea:

> A Nexus module is not one fixed script.  
> It is a configured flow of smaller playable activities.

---

## 2. Design Balance

The activity system should balance two needs:

1. **Future modularity**  
   The architecture should make it possible to build new Nexus modules later without starting from zero.

2. **MVP simplicity**  
   Nexus 01 should remain small, playable, and realistically buildable.

For Version 1, this means:

- use a simple linear pipeline,
- allow optional steps,
- pass a shared game state from one activity to the next,
- avoid a complex graph engine,
- avoid heavy abstractions before the first game works.

Later versions may introduce a richer activity graph.

---

## 3. Core Concepts

The activity system has three core concepts:

1. **Activity**  
   A small playable unit.

2. **Activity Flow**  
   The configured sequence of activities for a specific activation.

3. **Game State**  
   The shared data object that carries results from one activity to the next.

Together, these make it possible to create variable inner playthroughs without writing a completely different game for every configuration.

---

## 4. Activity

An activity is a small internal game module.

Each activity should have:

- an `activity_id`,
- an `activity_type`,
- input requirements,
- player interaction,
- output data,
- an optional condition for being included in the flow.

Example:

```json
{
  "activity_id": "learn_echo",
  "activity_type": "mini_language_lesson",
  "requires": [],
  "writes": ["known_commands", "first_phrase"],
  "enabled_if": null
}
```

Activities should be small enough to understand, test, and reuse.

They should not become entire games by themselves.

---

## 5. Activity Flow

The activity flow defines which activities are played and in which order.

For Nexus 01 Version 1, the flow should be:

```text
linear_with_optional_steps
```

This means:

- activities are mostly played in a fixed order,
- some activities may be skipped depending on activation mode, purpose, play mode, or previous results,
- the system does not yet need a full branching graph engine.

Example neutral flow:

```text
boot_sequence
→ mini_language_lesson
→ file_inspection
→ fragment_connection
→ lore_unlock
→ resonance_code_generation
→ after_play_options
```

Example gift flow:

```text
personal_boot_sequence
→ mini_language_lesson
→ personalized_file_inspection
→ fragment_connection
→ gift_message_unlock
→ resonance_code_generation
→ after_play_options
```

Example carried flow:

```text
validate_resonance_code
→ carried_boot_sequence
→ read_carried_trace
→ choose_return_symbol
→ enter_resonance_word
→ return_key_generation
→ after_play_options
```

---

## 6. Game State

The game state is the shared data object that is passed from one activity to the next.

Activities read from it and write to it.

This allows a later activity to react to earlier choices without requiring a custom script for every possible playthrough.

Example:

```json
{
  "activation_mode": "personal_activation",
  "purpose": "gift",
  "play_mode": "solo",
  "player_alias": "recipient_name",
  "known_commands": ["look", "read", "echo"],
  "found_fragments": ["ACCESS", "BOUNDARY"],
  "chosen_symbol": "lantern",
  "resonance_word": "courage",
  "trace_integrity": 2
}
```

Possible uses:

- If `purpose = gift`, show personalized boot text.
- If `chosen_symbol = lantern`, use the lantern return fragment.
- If `found_fragments` contains `ACCESS` and `BOUNDARY`, unlock `RESPONSE`.
- If a `resonance_word` exists, use it as part of return key material.
- If `play_mode = team_play`, ask for a team alias.

---

## 7. User Contributions as Data

User ideas should be allowed to influence the playthrough, but only in controlled ways for Version 1.

The game should not need to semantically understand arbitrary free text.

Instead, user input can be treated as data.

Examples:

- a chosen symbol,
- a resonance word,
- a short phrase,
- a team alias,
- a guided choice.

The system may:

- store this input,
- display it later,
- use it as key material,
- include it in a resonance note,
- include it in a local Hall-of-Resonance draft,
- include it in a contact node draft if the player chooses.

This keeps the system expressive without requiring AI-generated live interpretation.

---

## 8. Mini Language

Nexus 01 should feel like learning a tiny terminal language.

This may be especially enjoyable for players who like programming, Linux, open source, or terminal environments.

At the same time, the language should be simple enough for non-programmers.

The player should learn by doing.

Possible commands:

```text
help
look
scan
read
echo
set
link
unlock
carry
return
```

The language should feel like a small puzzle interface, not like a programming exam.

Design principle:

> A technical player may recognize the structure.  
> A non-technical player should still be able to follow the trail.

---

## 9. Version 1 Activity Types

For Nexus 01 Version 1, the following activity types are enough:

### 9.1 `boot_sequence`

Introduces the activation.

May be neutral, personal, gift-oriented, or carried.

### 9.2 `mini_language_lesson`

Introduces one or more small Nexus commands.

Example commands:

- `read`
- `echo`
- `set`
- `link`
- `unlock`

### 9.3 `file_inspection`

Lets the player inspect virtual files, logs, fragments, or traces.

### 9.4 `fragment_connection`

Lets the player connect found fragments.

This may unlock a concept, door, response, or result layer.

### 9.5 `choice_node`

Lets the player make a guided choice.

This is especially useful for carried activations.

### 9.6 `message_or_lore_unlock`

Unlocks the primary result:

- `message_unlock`,
- `gift_message`,
- or `lore_unlock`.

### 9.7 `resonance_code_generation`

Creates a resonance code after a completed origin playthrough.

### 9.8 `return_key_generation`

Creates a return key after a carried activation.

### 9.9 `encrypted_return_gate`

Accepts a return key in the original activation and attempts to open the encrypted return layer.

### 9.10 `after_play_options`

Offers voluntary local follow-up options:

- pass-on trace,
- Hall-of-Resonance draft,
- resonance note,
- contact node draft.

---

## 10. Nexus Module Types

The activity system should make it possible to define module types later.

A module type describes the general style and base structure of a Nexus module.

Possible future module types:

### 10.1 `terminal_escape_nexus`

Terminal-style commands, virtual files, logs, fragments, unlocks.

Nexus 01 belongs to this type.

### 10.2 `text_choice_nexus`

Interactive text, guided choices, branching narrative fragments.

### 10.3 `git_trace_nexus`

Git history, commits, branches, issues, discussions, and repository traces become part of the play space.

### 10.4 `cipher_grid_nexus`

Grids, coordinates, ciphers, layered reading paths.

### 10.5 `dialogue_reflection_nexus`

Dialogue prompts, reflection notes, group play, workshop-like structures.

These module types are future-facing concepts.

Nexus 01 should only implement `terminal_escape_nexus` in a small MVP form.

---

## 11. Nexus 01 MVP Flow Recommendation

Nexus 01 should use the following simple architecture:

```json
{
  "module_type": "terminal_escape_nexus",
  "flow_type": "linear_with_optional_steps",
  "state_model": "shared_game_state"
}
```

Recommended base flow:

```text
boot_sequence
→ mini_language_lesson
→ file_inspection
→ fragment_connection
→ message_or_lore_unlock
→ resonance_code_generation
→ after_play_options
```

Carried flow:

```text
validate_resonance_code
→ carried_boot_sequence
→ choice_node
→ resonance_word_input
→ return_key_generation
→ after_play_options
```

Return flow:

```text
return_key_input
→ encrypted_return_gate
→ returned_layer_display
```

This is intentionally modest.

The goal is not to make every configuration a completely different game.

The goal is to let configurations create meaningful variation by:

- changing the boot sequence,
- enabling or skipping activities,
- changing which virtual files/fragments appear,
- changing the final unlock type,
- using earlier player input in later activities,
- carrying state into return key generation.

---

## 12. Complexity Boundary for Version 1

Version 1 should not implement:

- a full branching graph engine,
- a visual editor for flows,
- nested activities,
- complex scripting,
- AI interpretation of arbitrary text,
- online activity exchange,
- automatic GitHub interaction,
- a large library of reusable activities.

Version 1 should implement only enough modularity to prove the concept.

Recommended rule:

> Build the smallest activity system that can carry Nexus 01 without forcing a rewrite later.

---

## 13. Working Formula

The activity system should make this possible:

> Different activations do not merely reveal different endings.  
> They can move through the Nexus in slightly different ways.

For Nexus 01, this should remain small:

> A simple pipeline.  
> Optional steps.  
> Shared state.  
> Meaningful variation.  
> No architecture cathedral yet.
