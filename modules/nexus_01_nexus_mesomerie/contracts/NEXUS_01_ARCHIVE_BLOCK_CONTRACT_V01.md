# Nexus 01 Archive Block Contract V0.1

Status: PROPOSED
Scope: Nexus 01 / Resonance Chamber / data-only Archive content
Purpose: first concrete Chamber Block contract for a future extensible Nexus architecture

## Concept lineage and normative relationship

Concept foundation:

```text
docs/concepts/NEXUS_ARCHIVE_CONCEPT.md
docs/concepts/NEXUS_ARCHIVE_FIRST_ENTRIES.md
docs/concepts/NEXUS_CONSTELLATIONS.md
```

Current Nexus 01 construction principles:

```text
modules/nexus_01_nexus_mesomerie/CURRENT_DIRECTION.md
modules/nexus_01_nexus_mesomerie/NEXUS_01_STRUCTURE.md
```

This document is the **normative technical contract for Archive Block V0.1**.

The concept documents define the larger narrative and architectural direction.
`CURRENT_DIRECTION.md` and `NEXUS_01_STRUCTURE.md` define the current Nexus 01
construction context. Where this V0.1 Block implementation needs a concrete,
machine-checkable rule, this contract defines that rule for the Archive Block
boundary.

It does not supersede broader Nexus concepts outside the Archive Block scope.

Earlier milestone-timing notes in the concept documents that deferred Archive
integration or Builder work until after the then-current gift milestone are
historical planning constraints. For this branch, the accepted Archive V0.1
implementation plan supersedes those timing notes only; the underlying concept,
privacy, ownership, and constellation principles remain in force.

## 1. Decision in one sentence

Nexus Chambers may expose explicit Block boundaries. Archive V0.1 introduces the
first such boundary as a **data-only `archive-content` Block** for the Nexus 01
Resonance Chamber.

This contract does **not** define a general plugin system.

## 2. Why this exists

Nexus 01 is designed as a local artifact that can travel without requiring an
online update service.

A travelling Nexus may therefore grow by receiving compatible local artifacts
that a person deliberately carries to it.

The Archive is the first suitable test case because new Archive material can be
added as content without granting an extension arbitrary executable behavior.

Working principle:

```text
The Nexus does not update itself.
A person may carry a compatible Block to it.
The Chamber decides whether it understands that Block type.
```

## 3. Relationship to current Nexus principles

This contract extends, rather than replaces, the current Nexus 01 structure.

It preserves:

- Chamber-specific local grammar;
- explicit human action before productive change;
- local-first behavior;
- calm validation and refusal;
- no automatic upload, discovery, synchronization, or publication;
- public/private separation;
- manual social transport.

A Block is not an activation.

A Block is not a Resonance Token.

A Block is not a Return Artifact.

A Block does not establish a relationship between people.

## 4. Block layers

The longer-term Nexus architecture may later distinguish several Block families.

For V0.1 only one family is implemented:

```text
Content Block
```

Possible future families such as Chamber Blocks or executable Logic Extensions
remain out of scope.

Archive V0.1 must not create an implicit executable-plugin API.

## 5. Archive Block identity

The first Block type is:

```text
archive-content
```

Canonical format identifier:

```text
nexus.chamber-block.v1
```

Target:

```text
module:  nexus-01
chamber: resonance
```

Schema version:

```text
1
```

A Block has a stable `block_id`.

Two Blocks with the same `block_id` represent the same logical Block identity.
V0.1 coupling must refuse to silently replace an already present Block with the
same identity.

## 6. Proposed on-disk shape

A Block is a directory with exactly one manifest and one content directory:

```text
n01-resonance-archive-origin/
├── manifest.json
└── content/
    ├── 001.json
    ├── 002.json
    └── 003.json
```

For V0.1:

- `manifest.json` must be a regular UTF-8 JSON file;
- `content/` must contain one or more regular UTF-8 `.json` files;
- nested directories inside `content/` are not allowed;
- symbolic links are not allowed anywhere inside the Block;
- unrelated extra files are not allowed.

The Block itself contains no Python file and no executable launcher.

The source directory name is not the Block identity. The normative identity is
the validated `block_id` in `manifest.json`. A Builder may therefore normalize
the published destination from `block_id` rather than trusting the source folder
name.

## 7. Manifest V0.1

The exact top-level field set is:

```text
format
block_type
block_id
target_module
target_chamber
schema_version
title
```

Example:

```json
{
  "format": "nexus.chamber-block.v1",
  "block_type": "archive-content",
  "block_id": "n01-resonance-archive-origin",
  "target_module": "nexus-01",
  "target_chamber": "resonance",
  "schema_version": 1,
  "title": "Resonance Archive — Origin"
}
```

V0.1 validation rules:

- top-level value must be a JSON object;
- all seven fields must be present;
- unknown fields must be rejected in V0.1 unless explicitly added to this contract;
- `format` must equal `nexus.chamber-block.v1`;
- `block_type` must equal `archive-content`;
- `target_module` must equal `nexus-01`;
- `target_chamber` must equal `resonance`;
- `schema_version` must equal `1`;
- `block_id` must be a public-safe ASCII identifier of 1–80 characters using
  only letters, digits, `.`, `_`, and `-`, and must begin with a letter or digit;
- `title` must be a non-empty UTF-8 string intended for player-facing display;
- `block_id` must not collide with an already coupled Block.

A future contract may add compatibility ranges or content digests. They are not
required for the first minimal implementation unless review shows that they are
needed for safe packaging.

## 8. Archive entry V0.1

Archive V0.1 reuses the three-depth content model already developed in:

```text
docs/concepts/NEXUS_ARCHIVE_FIRST_ENTRIES.md
```

The implementation should adapt existing archive material to the machine-readable
Block format rather than invent a second parallel content model.

Each content file contains one Archive entry.

Proposed minimal shape:

```json
{
  "entry_id": "what-is-a-nexus",
  "title": "What is a Nexus?",
  "access": "open",
  "poetic_indication": [
    "A Nexus is not a net that holds people together.",
    "It is a small place carried between them."
  ],
  "clear_orientation": [
    "A Nexus is a local place of chambers, thresholds, and possible paths."
  ],
  "deeper_trace": [
    "Optional longer archive-safe material may follow here."
  ]
}
```

Required fields for an `open` entry:

```text
entry_id
title
access
poetic_indication
clear_orientation
```

Optional field:

```text
deeper_trace
```

Allowed V0.1 `access` values:

```text
open
sealed
```

`access` describes whether the entry may currently be read. It is deliberately
not called `status`, because the wider Archive concept already uses status-like
labels such as orientation, record, fragment, unopened, local, chamber-owned,
and public-safe for different conceptual purposes.

For all entries:

- the top-level value must be a JSON object;
- `entry_id` must be a public-safe ASCII identifier of 1–80 characters using
  only letters, digits, `.`, `_`, and `-`, and must begin with a letter or digit;
- `title` must be a non-empty UTF-8 string intended for player-facing display;
- unknown fields must be rejected in V0.1.

For `open` entries, the allowed field set is:

```text
entry_id
title
access
poetic_indication
clear_orientation
deeper_trace
```

`deeper_trace` is optional. All other fields in that set are required.

- `poetic_indication` is a non-empty array of UTF-8 text strings;
- `clear_orientation` is a non-empty array of UTF-8 text strings;
- `deeper_trace`, when present, is a non-empty array of UTF-8 text strings;
- the three levels preserve the established Archive reading depth:
  poetic indication -> clear orientation -> optional deeper trace.

For `sealed` entries, the allowed field set is:

```text
entry_id
title
access
poetic_indication
```

`poetic_indication` is optional. `entry_id`, `title`, and `access` are required.

- when present, `poetic_indication` is a non-empty array of UTF-8 text strings
  and acts only as a deliberately public-safe teaser;
- `clear_orientation` and `deeper_trace` must be absent in V0.1;
- the renderer must not imply that private or missing personal data exists
  behind the sealed entry unless such material is actually part of an accepted
  future public-safe Block contract.

The Archive must not manufacture a false claim of remote, private, or hidden
personal data.

The first built-in Block should preferentially adapt suitable entries from
`NEXUS_ARCHIVE_FIRST_ENTRIES.md`, preserving their established wording and
three-depth structure unless a reviewed player-facing edit is needed.

## 9. Content safety boundary

Archive Blocks are public-safe travelling content.

V0.1 Blocks must not contain:

- `activation.local.json`;
- recipient-specific activation data;
- real Resonance Tokens;
- Return Artifacts;
- Return Slots;
- private Return Workspace material;
- generated local Return Results;
- passwords, API keys, credentials, private keys, or access tokens;
- executable Python, shell, binary, or script payloads;
- filesystem paths whose meaning depends on the original creator's machine.

The renderer treats Archive content as data, not as instructions to execute.

## 10. Nexus storage boundary

The Resonance Archive has two conceptual sources:

```text
archive/
├── builtin/
└── coupled/
```

### `builtin/`

Contains the Archive Block or Blocks shipped with the Nexus Core package.

Built-in Blocks travel with the release candidate and are verified with it, but
they remain logically distinct Blocks rather than becoming part of the Core
identity itself.

### `coupled/`

Contains compatible Archive Blocks deliberately added later.

Nothing outside these explicit roots is searched for automatically.

No recursive discovery of nearby directories, Downloads folders, USB devices,
home folders, repositories, or network locations is permitted.

## 11. Read behavior

The Resonance Chamber may read Archive Blocks only from the explicit Archive
roots belonging to that Nexus.

Reading is:

- local;
- read-only from the Chamber's point of view;
- deterministic for the same on-disk constellation;
- independent of activation mode unless a later contract explicitly says otherwise.

A malformed Block must not crash the whole Nexus.

The Archive surface should report a calm local failure or omit the invalid Block
according to the accepted implementation design, while preserving enough
technical information for diagnosis in tests or developer output.

## 12. Coupling behavior

Coupling is a deliberate Builder action, not an automatic Chamber action.

V0.1 coupling should follow this conceptual sequence:

```text
select one Block path
-> validate structure
-> validate manifest
-> validate target
-> validate entries
-> check duplicate block_id
-> stage copy
-> verify staged copy
-> publish into coupled/
```

The Builder must refuse overwrite.

The Builder must not modify private activation or Return state.

## 13. Constellation

A Nexus **constellation** is the Nexus Core together with the compatible
travelling Blocks currently coupled to it.

Private local state is not part of the exportable constellation by default.

Conceptually:

```text
Nexus constellation
=
Core
+ built-in Blocks
+ deliberately coupled public-safe Blocks
```

Not included by default:

```text
activation
selected Resonance Token context
Return Artifacts
private Return Workspaces
local Return Results
other private/generated state
```

A later Builder slice may write a machine-readable constellation manifest. It is
not required for the first Archive reader slice.

## 14. Travelling behavior

A future "prepare this Nexus to travel" operation may preserve the current
public-safe Block constellation.

This produces a carried constellation rather than an online-updated installation.

The existing neutral carrier remains a distinct valid product:

```text
fresh neutral carrier
```

A future product may be:

```text
neutral/current Core
+ selected travelling Blocks
= carried constellation
```

Both must remain locally built and explicitly verified.

## 15. Player-facing Archive V0.1

Archive V0.1 is a read-only Resonance Chamber surface.

The intended first player-facing capability is:

```text
/archive
```

It may show:

- the Archive title;
- a small list of open entries;
- one or more deliberately sealed entries;
- an invitation to inspect an entry;
- no claim of network access or automatic memory.

Exact command grammar is an implementation decision to be reviewed against the
current exploration-first Chamber grammar before coding.

## 16. Explicit non-goals

Archive Block V0.1 does not include:

- a GUI;
- online updates;
- automatic Block discovery;
- executable plugins;
- arbitrary Chamber replacement;
- dependency resolution;
- Block migration;
- Block deletion from a live Nexus;
- remote repositories;
- package registries;
- accounts;
- cloud synchronization;
- private-history export;
- automatic merging of conflicting Blocks.

## 17. Compatibility failure principle

If a Nexus does not understand a carried Block, nothing should be changed.

Useful conceptual outcomes include:

```text
valid and compatible
valid but already present
valid but for another Chamber
valid but unsupported schema
invalid Block
```

All refusal paths should preserve the existing Nexus unchanged.

## 18. First reference Block

The first implementation should include one built-in Block:

```text
block_id:
n01-resonance-archive-origin
```

Its purpose is twofold:

1. give the Resonance Chamber a small real Archive at gift-release time;
2. act as the reference fixture for validation, rendering, packaging, and later
   Builder coupling tests.

Its prose content should be drawn first from the existing prototype in
`docs/concepts/NEXUS_ARCHIVE_FIRST_ENTRIES.md`.

The first implementation should avoid creating redundant alternative explanations
when an existing entry already fits the intended Archive surface. New prose should
be added only where the reference Block needs material that the existing prototype
does not yet provide.

## 19. Acceptance boundary for V0.1

This contract is successfully implemented when:

- one built-in `archive-content` Block, based primarily on the existing Archive
  entry prototype, is validated and rendered;
- `/archive` is available on the intended Resonance Chamber surface;
- Archive reading performs no filesystem-wide discovery;
- no Archive Block executes code;
- invalid Archive data fails calmly;
- current COMPOSE, ANSWER, Return, and Stable-result behavior remains unchanged;
- packaging contains the built-in Archive;
- the canonical Nexus test suite passes;
- the neutral carrier verifier passes for the rebuilt candidate.

## 20. Future direction

If Archive V0.1 proves the Block boundary useful, later work may add:

- deliberate coupling of external `archive-content` Blocks;
- a small Nexus Builder / Workshop interface;
- a constellation manifest;
- carried-constellation export and verification;
- additional data-only Chamber Block types.

Those additions should grow from real Chamber needs rather than from a universal
plugin abstraction.
