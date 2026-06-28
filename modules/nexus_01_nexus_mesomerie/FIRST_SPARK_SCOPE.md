# Nexus 0.1 – First Spark Scope

Project: **glossAI Nexus**  
Parent module concept: **Nexus 01 – Nexus-Mesomerie**  
Document status: First implementation scope

---

## 1. Purpose

**Nexus 0.1 – First Spark** is the first small playable slice of Nexus 01.

It is not the full Nexus 01 concept.

It is not the full glossAI Nexus system.

It is the smallest version that can become a real gift mini-game.

Core goal:

> Build a small local terminal-style game that can be completed and that unlocks a personal gift message.

---

## 2. Intended Player Experience

The player should experience something like this:

1. They start a small terminal-style Nexus.
2. They notice that it has been personally activated for them.
3. They learn a few simple Nexus commands.
4. They inspect a small set of virtual files, logs, or traces.
5. They connect a few fragments.
6. They unlock a personal gift message.

The game should feel like:

- a tiny terminal escape game,
- a playful introduction to a small command language,
- a readable open-source artifact,
- a personal gift hidden inside a system.

It should not feel like:

- a programming exam,
- a large framework demo,
- a philosophical lecture,
- an unfinished architecture prototype.

---

## 3. MVP Boundary

First Spark should be deliberately small.

Included:

- local terminal play,
- one gift activation,
- solo play,
- a tiny command language,
- a simple activity pipeline,
- a very small shared game state,
- a few virtual files or traces,
- one fragment-connection puzzle,
- one gift message unlock.

Not included:

- carried activation,
- return key,
- encrypted return layer,
- Hall of Resonance,
- GitHub contact nodes,
- neutral activation,
- team play,
- multiple module types,
- complex activity graph,
- online features,
- AI-generated live responses.

Guiding rule:

> If it does not directly help the first gift game, it belongs to a later phase.

---

## 4. Development Principle: Small Running Units

First Spark should be developed in very small running units.

Each new unit should be:

- small enough to understand,
- runnable as early as possible,
- tested before the next unit is added,
- connected to the larger Nexus structure only as much as needed.

The project should not wait until many parts are finished before anything can run.

Recommended build order:

1. Start script runs and prints the boot text.
2. `help` works.
3. `look` works.
4. `read` works for a small set of virtual files.
5. `link` can connect fragments.
6. `unlock` opens the gift message.

After each step, the prototype should still be runnable.

Working formula:

> First make the spark run.  
> Then widen the trace.

---

## 5. Required Configuration

First Spark needs only one activation configuration.

```json
{
  "activation": {
    "mode": "personal_activation",
    "purpose": "gift",
    "recipient_alias": "recipient_name",
    "visible_personalization": true
  },
  "play": {
    "mode": "solo"
  },
  "result": {
    "primary_type": "message_unlock",
    "message_type": "gift_message"
  }
}
```

The concrete recipient alias and gift text should live in a local/private activation file.

Private gift activation files should not be committed publicly unless intentionally anonymized.

---

## 6. Activity Flow

First Spark should use a simple linear activity flow.

```text
personal_boot_sequence
→ mini_language_lesson
→ file_inspection
→ fragment_connection
→ gift_message_unlock
```

No graph engine is needed.

Optional steps should only be added if they make the gift game clearer, not larger.

---

## 7. Activities in Scope

### 7.1 `personal_boot_sequence`

Shows that the Nexus has been activated for the player.

Example tone:

```text
Nexus 0.1 – First Spark
Activation detected.
Recipient: Recipient Name
Private message: locked.
```

The personalization may be visible from the beginning.

The gift message itself remains locked until completion.

### 7.2 `mini_language_lesson`

Introduces a tiny command language.

The player should learn commands by using them.

Commands should be simple and discoverable.

### 7.3 `file_inspection`

Lets the player inspect a few virtual files, logs, or fragments.

The files should contain clues.

They should also make the Nexus feel like a small readable software artifact.

### 7.4 `fragment_connection`

Lets the player connect found fragments.

This should be the central small puzzle.

### 7.5 `gift_message_unlock`

Unlocks the final gift message.

This is the completion point of First Spark.

---

## 8. Tiny Command Language

First Spark should use only a very small command set.

Required commands:

```text
help
look
read
link
unlock
```

Optional command, only if useful:

```text
echo
```

Commands should be forgiving where possible.

The game should guide the player enough that non-programmers can play it.

Design principle:

> A technical player may enjoy the terminal feeling.  
> A non-technical player should still be able to follow the trail.

---

## 9. Minimal Game State

First Spark needs only a tiny game state.

Example:

```json
{
  "recipient_alias": "recipient_name",
  "known_commands": ["help", "look", "read"],
  "found_fragments": [],
  "linked_fragments": [],
  "gift_unlocked": false
}
```

The game state should be simple enough to inspect and understand.

---

## 10. Virtual Files and Fragments

First Spark should include only a few virtual files.

Possible examples:

```text
welcome.log
spark.note
access.fragment
boundary.fragment
response.locked
```

The actual names may change.

Recommended fragment count:

- minimum: 3
- maximum for First Spark: 5

This keeps the puzzle small.

---

## 11. Completion Criteria

First Spark is complete when:

1. the player can start the game locally,
2. the game shows visible gift personalization,
3. the player can use `help`, `look`, `read`, `link`, and `unlock`,
4. the player can inspect a few virtual files,
5. the player can connect the required fragments,
6. the gift message unlocks,
7. the full playthrough is short and understandable,
8. the code remains readable.

---

## 12. Explicit Parking Lot

The following ideas are important, but parked for later:

- `neutral_activation`
- `carried_activation`
- return keys
- resonance codes
- encrypted return layers
- Hall of Resonance drafts
- GitHub contact node drafts
- team play
- module templates
- additional Nexus module types
- activity graph engine
- browser interface

They are documented in the larger Nexus planning documents.

They should not be implemented in First Spark unless intentionally promoted later.

---

## 13. Working Formula

First Spark should stay small enough to finish.

> Not the whole Nexus.  
> Not the whole network.  
> One terminal.  
> One trace.  
> One unlocked gift.
