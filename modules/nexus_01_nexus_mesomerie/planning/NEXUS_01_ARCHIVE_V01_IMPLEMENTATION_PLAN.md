# Nexus 01 Archive V0.1 — Implementation Plan

Original plan status: PROPOSED
Baseline: accepted pre-Archive gift candidate at source commit `624fa79948c325edec66999add2ef23213457710`
Scope: one small read-only Archive plus the first data-only Chamber Block boundary

Implementation status at `1bec2232c5e7b7ed05362132e293245473bc7f30`:
Slices A–F are complete through safe Builder coupling, including the accepted
race and rollback gates. Slice G — Travelling Constellation Export is
**DEFERRED AFTER GIFT**. The final gift-release closeout for the Archive-capable
candidate remains pending; this status note does not rewrite the original plan.

## 1. Baseline and fallback

The currently accepted gift candidate remains the fallback release.

Fallback identity recorded before Archive work:

```text
source commit:
624fa79948c325edec66999add2ef23213457710

package:
nexus-01-neutral-carrier-gift-final.zip

SHA-256:
0f24deaf938490501da359cd33046fc2107ea93e12c17de216ec9de8afb7e0e7
```

The fallback artifact itself must remain unchanged. Its checksum identifies that
specific pre-Archive package only.

Archive work starts **after** that known-good checkpoint and must not overwrite,
delete, or silently replace the previously verified ZIP.

If Archive work is abandoned, the known-good pre-Archive package can still be
used as the gift release.

Any later accepted Archive code or documentation change invalidates the identity
of a newer release candidate until that newer candidate is rebuilt, verified,
tested, and checksummed again.

## 2. Development rule

Do not implement the Builder before the first Block contract and first real Block
exist.

Use this order:

```text
contract
-> reference Block
-> validator/loader
-> read-only Archive surface
-> focused tests
-> full regression
-> minimal Builder coupling slice
-> package/export integration
-> final release gate
```

The first four steps establish the real data model.

The Builder is then designed against something concrete rather than against an
abstract plugin system.

The older concept documents contain milestone-timing notes that postponed Archive
integration and Builder work until after the then-current gift milestone. The
present plan intentionally supersedes those timing notes for this branch while
retaining their architectural, narrative, privacy, and ownership principles.

## 3. Slice A — Contract and reference content

Use the existing Archive concept material as the content source of truth:

```text
docs/concepts/NEXUS_ARCHIVE_CONCEPT.md
docs/concepts/NEXUS_ARCHIVE_FIRST_ENTRIES.md
docs/concepts/NEXUS_CONSTELLATIONS.md
```

Do not invent duplicate Archive explanations where the existing first-entry
prototype already supplies suitable material.

Create:

```text
contracts/NEXUS_01_ARCHIVE_BLOCK_CONTRACT_V01.md
```

Create one built-in reference Block under an implementation path chosen after
the path review.

Suggested conceptual shape:

```text
resonance_archive/
├── builtin/
│   └── n01-resonance-archive-origin/
│       ├── manifest.json
│       └── content/
│           ├── 001.json
│           ├── 002.json
│           └── 003.json
└── coupled/
```

Do not create an empty tracked `coupled/` directory merely for appearance if the
runtime does not need it.

Acceptance:

- manifest and entries conform to the contract;
- entry data preserves the established three-depth model:
  poetic indication, clear orientation, optional deeper trace;
- `access` is used for `open` / `sealed` visibility rather than overloading the
  broader conceptual term `status`;
- suitable prose is adapted from `NEXUS_ARCHIVE_FIRST_ENTRIES.md` instead of
  being redundantly rewritten;
- content contains no private data;
- no executable file exists inside the Block.

## 4. Slice B — Archive loader and validator

Add a small Archive-specific module rather than embedding JSON parsing directly
inside the large Resonance controller.

Responsibilities:

```text
load one Block
validate manifest
validate entries
load explicit built-in/coupled roots
detect duplicate block_id
return immutable/read-only domain objects
```

Non-responsibilities:

```text
no rendering
no terminal input
no copying
no network
no activation changes
no Return state changes
```

Focused tests:

- valid built-in Block;
- missing manifest;
- malformed JSON;
- unknown manifest key;
- unknown entry key;
- wrong format;
- wrong module;
- wrong Chamber;
- unsupported schema;
- duplicate `block_id`;
- invalid entry;
- `open` / `sealed` access handling;
- nested content directory rejected;
- symbolic link rejected;
- unrelated extra Block file rejected;
- no arbitrary filesystem discovery.

## 5. Slice C — Resonance Archive surface

Integrate the Archive through the current corrected Resonance Chamber command
surface.

Keep the exploration-first rule:

- entering Resonance does not automatically dump the Archive;
- `/look` remains room/state description;
- `/help` reveals `/archive` only where intended;
- `/archive` opens a read-only Archive view;
- productive COMPOSE/ANSWER actions remain explicit and unchanged.

The Archive surface should not claim that it contains a complete history of
players, Tokens, invitations, Return Artifacts, or results.

Suggested first interaction:

```text
/archive
-> show Archive heading and entry index
-> allow explicit inspection of one entry
-> return to Resonance surface
```

Exact subcommand shape should be chosen only after reviewing the existing
corrected command dispatcher in `atrium/classified_resonance.py`.

Focused tests:

- `/archive` appears in the correct capability set;
- `/look` does not dump Archive content;
- Archive entry can be read;
- sealed entry stays sealed;
- unknown entry fails calmly;
- invalid Block cannot break COMPOSE/ANSWER;
- `/quit`, `/results`, `/compose`, ANSWER behavior remain unchanged.

## 6. Slice D — First Archive acceptance checkpoint

Before any Builder work:

1. inspect tracked diff;
2. run Archive-focused tests;
3. run Resonance focused tests;
4. run the canonical complete suite;
5. perform one short manual Resonance Archive play check;
6. review before commit.

If this slice is not stable, stop here and retain the pre-Archive gift fallback.

## 7. Slice E — Minimal Nexus Builder V0.1

Only after the Archive contract has survived implementation.

Builder V0.1 is a local command-line/terminal utility over safe reusable
functions.

Minimum operations:

```text
inspect Nexus
inspect one Archive Block
show Archive constellation
couple one compatible Archive Block
verify resulting local constellation
```

Optional in the same slice only if small and safe:

```text
prepare travelling constellation
```

Do not build a GUI yet.

Do not add a universal plugin framework.

## 8. Builder Core design rule

Reuse existing preparation principles already present in Nexus packaging:

- stage before publication;
- validate before copy;
- refuse overwrite;
- roll back incomplete publication;
- keep travelling and private roots separate;
- verify after staging;
- never upload, send, sync, or track.

The Builder UI must not become a second independent implementation of safety
rules.

Reusable operations should live in importable functions, with the terminal
interface acting only as a thin front end.

## 9. Slice F — Coupling operation

Conceptual flow:

```text
builder selects source Block
-> validate source
-> inspect target Nexus
-> verify target Chamber compatibility
-> reject duplicate block_id
-> stage under target Archive area
-> validate staged Block again
-> publish exclusively
-> display resulting constellation
```

Failure must leave the target Nexus unchanged.

Focused tests:

- successful coupling;
- wrong Chamber;
- wrong module;
- unsupported schema;
- duplicate Block;
- malformed content;
- existing destination race/refusal where practical;
- no copy of unrelated sibling files;
- no mutation of activation or Return state.

## 10. Slice G — Travelling constellation

If included before gift release, extend the existing neutral-carrier preparation
path rather than inventing an unrelated package copier.

Two products should remain distinguishable:

```text
Neutral Nexus Carrier
Carried Nexus Constellation
```

A carried constellation may include:

- Core;
- built-in public-safe Blocks;
- deliberately selected coupled public-safe Blocks.

It must not include private activation/Return state.

The existing carrier verifier should either be safely extended or complemented
by a narrow constellation verifier.

## 11. Documentation in parallel

While coding, maintain:

```text
contracts/NEXUS_01_ARCHIVE_BLOCK_CONTRACT_V01.md
planning/NEXUS_01_ARCHIVE_V01_IMPLEMENTATION_PLAN.md
planning/NEXUS_01_GIFT_SPRINT_STATUS_AND_NOTES.md
```

Do not yet rewrite all public documentation.

Public README, player guide, privacy documentation, packaging documentation, and
Wiki should be synchronized after the Archive/Builder behavior is accepted.

Historical plans remain historical unless a short status note is genuinely
needed.

## 12. Release invalidation rule

The existing pre-Archive gift candidate remains a fallback artifact.

The moment a new release-relevant tracked change is accepted for the Archive
candidate, the previous package checksum does **not** identify the new source.

For the new final release:

```text
accepted final source commit
-> canonical full suite
-> package build
-> directory verification
-> ZIP verification
-> manual final-path check as needed
-> SHA-256
-> release identity record
-> freeze
```

Any accepted later release-relevant change repeats that gate.

## 13. Stop conditions

Archive V0.1 should be deferred from the gift if implementation requires:

- a general plugin API;
- executable third-party Blocks;
- major refactoring of COMPOSE/ANSWER;
- migration of activation schemas;
- network functionality;
- broad package format replacement;
- unresolved regression in the existing full gift path.

The pre-Archive candidate exists specifically so that this experiment can remain
optional rather than becoming a release emergency.

## 14. Original immediate next action — historical

The following was the immediate next action when this implementation plan was
proposed. Slices A–F have since been completed, so it is retained as planning
history and is not a current work instruction.

After review of this plan and the Block contract:

```text
A1. choose the exact Archive implementation path
A2. create the reference origin Block
A3. implement validator/loader
A4. add focused tests
A5. review diff before integrating /archive
```

This keeps the first coding step small and independently testable.
