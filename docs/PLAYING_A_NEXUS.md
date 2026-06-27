# Playing a Nexus

This document describes general play expectations for **glossai-nexus** modules.

Individual modules may vary these rules. If a module changes, extends, or replaces parts of this guide, it should say so clearly in its own module README or play instructions.

## Basic idea

A Nexus is meant to be played at the surface and readable in the depth.

You do not have to read code to play a Nexus. But the code, structure, configuration, and documentation should remain open to inspection.

A Nexus may include:

- a playable surface,
- optional deeper layers,
- readable code,
- configuration files,
- activation data,
- hidden traces,
- developer notes,
- optional result files.

## Recommended first path

Unless a module says otherwise, the recommended first path is:

1. Read the module's start instructions.
2. Play the surface game first.
3. Use built-in hints if you want them.
4. Read the code or developer notes later, or earlier if that is how you enjoy playing.

The code is open. Curiosity is allowed.

But some doors may be more satisfying when opened from the inside.

## Code and spoilers

Because a Nexus is open source, reading the code may reveal hints, mechanics, puzzle structures, or spoilers.

This is not a failure of the project. It is part of the tension between openness and play.

A Nexus should handle this tension openly:

- The main path should be playable without reading code.
- Code reading may be an optional path, not a requirement.
- Spoiler-heavy files or sections should be marked clearly.
- Functional code should remain readable and should not be made obscure just to protect puzzles.
- Hidden traces should reward curiosity, not punish players who stay on the surface.

A useful rule:

> Open code may contain spoilers. A Nexus should mark spoiler-heavy areas clearly and design its main play experience so that reading the code becomes an optional path, not a required shortcut.

## Suggested code areas

Modules may organize their code and files into areas with different spoiler expectations.

### Surface area

The surface area contains start instructions, player-facing text, commands, and ordinary gameplay files.

It should be safe to read before playing.

Example names:

- `README.md`
- `START_HERE.md`
- `play.py`
- `docs/player_guide.md`

### Open code area

The open code area contains the functional code of the module.

It should be readable, well structured, and documented. It may reveal mechanics and some indirect hints.

Example names:

- `src/`
- `nexus_engine/`
- `commands.py`
- `state.py`

### Trace area

The trace area may contain optional deeper clues, developer notes, comments, lore fragments, Git-related hints, or other discoverable meanings.

It may contain mild spoilers.

Example names:

- `traces/`
- `dev_notes/`
- `lore_fragments/`

### Spoiler area

The spoiler area contains solution notes, ending templates, puzzle explanations, or files that reveal major outcomes.

It should be clearly marked.

Example names:

- `spoilers/`
- `solution_notes.md`
- `ending_templates.md`

### Activation area

The activation area contains configuration or private situational data for a specific activation.

It may contain personal messages, gift notes, result settings, or local play data.

Activation data should not be published by default.

Example names:

- `activation/`
- `activation_private/`
- `activation.json`
- `final_message.md`

## Spoiler markers

Modules should mark spoiler-heavy areas clearly.

Suggested markers:

```text
[SPOILER]
```

```text
[SPOILER: PUZZLE SOLUTION]
```

```text
[SPOILER: ENDING]
```

```text
[SPOILER: ACTIVATION DATA]
```

A module may define its own markers, but it should explain them.

## Module variations

A specific Nexus module may intentionally vary this guide.

For example, a module may:

- invite players to read code from the beginning,
- hide major traces in Git history,
- use a browser interface instead of a terminal,
- include no spoiler area,
- include a stronger developer-note layer,
- treat source inspection as an intended advanced mode.

If a module does this, it should explain the variation clearly.

## Optional result files

Some modules may create local result files.

These may include:

- a team alias,
- difficulty,
- fragments found,
- hints used,
- traces unlocked,
- pass-on traces,
- Hall of Resonance entry drafts.

Result files should not be uploaded automatically.

Players should decide whether to keep, delete, or share them.

## Consent and privacy

A Nexus should not take personal information silently.

If a module asks for a team name, alias, or result entry, it should explain:

- what will be stored,
- where it will be stored,
- whether it is local or public,
- how it may be shared,
- that sharing is optional.

A useful rule:

> The Hall of Resonance only remembers what players choose to share.

## Core play principle

A Nexus trusts its players.

It does not need to lock every door. It should make the doors meaningful.
