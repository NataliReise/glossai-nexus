# Nexus 01 Structure

This document defines the current structural language for **Nexus 01 - First Spark**.

It is a concept anchor before changing the playable flow.

```text
A Nexus Module is not a linear escape room.
It is a ring-shaped chamber structure around a changing atrium.
```

## Core terms

### Nexus Module

A **Nexus Module** is the outer artifact.

For this repository, the first public module is:

```text
Nexus 01 - First Spark
```

A Nexus Module may contain several inner play spaces and several activation layers.

### Nexus Atrium

The **Nexus Atrium** is the central entrance, return, and passage space.

The player starts in the Atrium.

After completing a Chamber, the player may return to the Atrium.

The Atrium can change according to:

```text
activated layers
visible doors
completed chambers
local resonance state
```

The Atrium should be readable, not mysterious for its own sake.

It changes because something has been activated, completed, opened, or returned.

### Chambers

**Chambers** are the inner play spaces of a Nexus Module.

A Chamber can contain traces, commands, small puzzles, or local generation steps.

Current and planned examples:

```text
Spark Chamber
Resonance Chamber
```

The word Chamber should be preferred over inner module in player-facing and concept-facing language, because Nexus Module already names the outer artifact.

### Layers

**Layers** are larger meaning or activation layers that can enable one or more Chambers.

Current and planned examples:

```text
First Spark Layer
Return Resonance Layer
```

A layer is not necessarily a separate program.

It can be a readable configuration, a set of available Chambers, or an additional local path through the same Nexus Module.

### Paths

**Paths** are concrete movements between the Atrium and Chambers.

A path may be linear inside a Chamber, but the larger Nexus structure should return to the Atrium when useful.

Example:

```text
Nexus Atrium
  -> Spark Chamber
  -> Nexus Atrium, changed
  -> Resonance Chamber
  -> Nexus Atrium, changed
```

## Ring structure

Nexus 01 should be imagined as a small ring around a central Atrium.

```text
                 Spark Chamber
                      |
                      |
Resonance Chamber -- Nexus Atrium -- future Chamber
                      |
                      |
               future Chamber
```

The Atrium is not just a start screen.

It is the place where the Nexus becomes legible.

At first, it may show only one door.

Later, it may show additional doors or traces.

## Current intended structure

```text
Nexus 01 - First Spark

Nexus Atrium
  central entrance and return space

Spark Chamber
  first playable Chamber
  reads visible traces
  links the spark
  opens the private activation message

Threshold / After-play state
  current ending logic
  shows the opened activation message
  explains public-safe resonance node sharing

Resonance Chamber
  planned second Chamber
  enabled by a resonance activation or resonance token
  collects or derives return elements
  creates a local return artifact
```

The current code still uses names such as `arrival` and `game_modules`.

Those names do not need to be renamed immediately.

For now, the concept language should guide new work:

```text
arrival -> Nexus Atrium concept
spark_chamber -> Spark Chamber
ending -> Threshold / after-play state
future resonance_chamber -> Resonance Chamber
```

## Activation modes and enabled chambers

Nexus 01 can support different activation modes.

A normal gift activation may enable only the First Spark path.

A resonance activation may enable the First Spark path and the Return Resonance path.

Possible future activation fields:

```json
{
  "activation_mode": "gift",
  "enabled_chambers": ["spark"]
}
```

```json
{
  "activation_mode": "resonance",
  "enabled_chambers": ["spark", "resonance"],
  "resonance_token": {
    "origin_trace_id": "...",
    "return_slot_id": "...",
    "package_id": "...",
    "layer_id": "return-resonance-1"
  }
}
```

These names are design candidates, not a frozen schema yet.

## Atrium behavior

The Atrium should show only what is available in the current activation.

A first gift activation may show:

```text
spark.door
```

A resonance activation may show:

```text
spark.door
resonance.door
```

After a Chamber has been completed, the Atrium should reflect that completion.

Examples:

```text
The spark.door is open now.
A small mark glows near the center.
```

```text
The resonance.door has answered.
The ring is no longer silent.
```

The Atrium should not simulate a social network.

It should not track people, engagement, delivery, or relationships.

It may show local state that belongs to this package and this run.

## Return Resonance direction

The Return Resonance Layer should not be a message-sending system.

It should remain local and manual.

A possible social path is:

```text
Person A gives Nexus 01 to Person B.
Person B plays First Spark.
Person B may carry the module onward.
Person C receives a resonance activation or resonance token.
Person C may enter the Resonance Chamber.
Person C may create a local return artifact.
Any sharing of that artifact remains manual.
```

The Resonance Chamber may generate or collect values such as:

```text
carrier_image
carrier_movement
return_word
return_image
return_tone
```

These values can later be used by the existing Return Resonance code to compose a local return result.

## Boundaries

This structure should preserve the core Nexus boundary:

```text
The artifact may travel digitally.
The resonance should be carried socially.
```

Therefore, Nexus 01 should not add:

```text
automatic delivery
automatic upload
accounts
tracking
engagement logic
social graph logic
remote relationship management
```

A feature belongs in the Nexus only if it supports the artifact without managing the relationship.

## Current implementation strategy

Do not rewrite the whole codebase first.

Prefer a small transition:

```text
1. Keep the current working First Spark flow stable.
2. Treat the current arrival module as the first version of the Nexus Atrium.
3. Add conceptual Atrium behavior gradually.
4. Add Resonance Chamber as a small second Chamber.
5. Return to the Atrium after completed Chambers where useful.
6. Keep gift packaging and verification reliable.
```

The first implementation goal is not a large world.

The first implementation goal is a clear second layer:

```text
First Spark Layer + Return Resonance Layer
around one changing Nexus Atrium.
```
