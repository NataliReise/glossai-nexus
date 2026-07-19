# Nexus 01 Chamber States and Results V0.3

## Document status

- Version: 0.3
- Status: Current
- Date: 2026-07-19
- Supersedes: Version 0.2
- Purpose: Canonical release-closeout Chamber-state, capability, result,
  privacy, and safety contract at checkpoint `59c6595`.

## 1. Scope and release principle

This contract records implemented behavior through Stable-result Revisit.
Nexus 01 remains local, explicit, exploration-first, and fail-closed. Entering
a room does not begin productive work. No feature may infer a private source,
discover an old result, or silently widen the publication boundary.

Technical completion at this checkpoint does not replace the pending
language-wide inventory and final manual release-play acceptance.

## 2. Shared play grammar and text layers

The corrected Atrium and Resonance surfaces follow this grammar:

```text
enter a room
-> perceive room and state
-> request /help when desired
-> start productive work only through an explicit action
-> observe the resulting state
```

Player-facing layers remain distinct:

- room description and `/look`: place, atmosphere, visible paths, and state;
- `/help`: only currently available visible actions;
- productive prompts: choices, words, confirmation, and cancellation;
- system text: only what actually completed, failed, or remained unchanged;
- `/results`: read-only views of an allowed result source.

Dispatcher and help derive from the same small room-local capability source.
Unavailable actions remain hidden. No Nexus-wide command framework exists.

## 3. Independent state axes

The implementation keeps these axes separate:

- Atrium position and enabled paths;
- Resonance mode: `COMPOSE`, `ANSWER`, or `BLOCKED_ANSWER_RECOVERY`;
- Surface phase: `PRE_RUN`, productive prompts, `POST_RUN`, or `BLOCKED`;
- productive cycle: not started, active, cancelled, failed, or completed;
- result availability: none, same-process completed result, or explicit stable
  known source;
- Return Slot state and stable-result existence.

`LEGACY_CONTROLLER` remains an isolated compatibility path, not a fourth
canonical Resonance mode.

## 4. Current capability matrices

### Atrium

When Resonance is available:

```text
/look
/help
/first-spark
/resonance
/quit
```

When Resonance is unavailable, `/resonance` is omitted. The Atrium description
shows room, perceptible paths, and state without an automatic command list. A
short `/help` orientation appears once per terminal process.

### Resonance COMPOSE PRE_RUN

Without an explicit known source:

```text
/look
/help
/compose
/quit
```

With an explicit known source, `/results` appears before `/compose`.

### Resonance ANSWER PRE_RUN

Without an explicit known source:

```text
/look
/help
/answer
/quit
```

With an explicit known source, `/results` appears before `/answer`.

### Active productive prompts

Corrected COMPOSE and ANSWER choice and word prompts expose:

```text
/look
/help
/trace
/walkthrough
/cancel
```

Confirmation prompts retain their explicit yes/no and cancellation grammar;
destination prompts retain exact `/cancel` and blank cancellation. `/results`
is not an active productive-prompt action.

### COMPOSE POST_RUN

```text
/look
/help
/trace
/results
/compose
/quit
```

### ANSWER POST_RUN

```text
/look
/help
/trace
/results
/quit
```

### BLOCKED

```text
/look
/help
/quit
```

BLOCKED offers no productive action, result reading, Token search, selection,
repair, or mutation.

## 5. Meaning of completed

The completed unit is one productive cycle, not the Chamber.

- COMPOSE completes only after the travelling invitation and private Return
  Workspace are both created successfully.
- ANSWER completes only after one Return Artifact is written successfully.
- Cancellation, validation failure, and write failure remain incomplete.
- Completion does not automatically start another cycle.
- COMPOSE may begin another independent cycle only through explicit
  `/compose`; ANSWER does not repeat automatically.

## 6. Result classes and ownership

Result models remain deliberately separate:

- `CompletedComposeResult` and `CompletedAnswerResult` belong to the current
  controller process and represent successful productive work;
- `StableResonanceView` belongs to read-only rereading of one existing stable
  Markdown result;
- a Return Artifact is a travelling transport object, not the stable result;
- the authoritative stable production result belongs to the private Return
  Workspace under `results/<ReturnSlot.result_file>`.

The models are not converted into one another and no general result registry
is created.

## 7. Same-process result behavior

Slice 4A exposes the most recent successful COMPOSE or ANSWER result retained
by the controller. The view is allowlisted and read-only. Missing known local
paths may be reported, but no filesystem search occurs.

When `_last_completed_result` exists, it has precedence: the same-process view
is rendered, the Stable-result reader is not called, and the configured known
source path is not displayed.

## 8. Explicit Known-source handoff

An optional deliberate launcher argument provides exactly one lexical absolute
local reference:

```text
--known-resonance-source ABSOLUTE_PATH
-> run_corrected_nexus(...)
-> ClassifiedResonanceController
```

Only an absolute path is accepted, and its exact lexical form is preserved.
Handoff performs no normalization, resolution, existence check, or file read;
startup likewise does not read the source. The reference remains process-local
and is never placed in Activation, the travelling carrier, or a persistent
registry. After a restart the waiting person must provide it deliberately
again.

## 9. Safe Known-source byte boundary

`read_known_source_bytes()` opens only the exact supplied path and provides an
immutable typed result. Its contract preserves:

- read-only access with `O_NOFOLLOW`;
- regular-file validation on the opened descriptor;
- bounded raw-byte reading and reliable descriptor closure;
- no `resolve()`, discovery, mutation, path leakage, or OS-error leakage in the
  typed result.

Accepted limitation: `O_NOFOLLOW` protects the final path segment.
Parent-directory symlinks are not fully excluded by this narrow boundary.

## 10. Stable-result reader and visible allowlist

`read_stable_resonance_result()` uses only the known-source byte boundary. It
requires strict UTF-8 and the complete canonical Markdown grammar. It validates
the uniquely delimited technical JSON trace but exposes exactly the five
compact-Nachhall lines in `StableResonanceView`.

An explicit Stable-source `/results` displays only:

```text
[local path]
exact configured path
short availability status

[private local]              # AVAILABLE only
exact five compact-Nachhall lines
```

The technical trace, IDs, seed, plan, pairings, Slot metadata, raw Markdown,
and footer are never rendered.

Failure states are `MISSING`, `SYMLINK`, `NOT_REGULAR`, `UNAVAILABLE`,
`TOO_LARGE`, `INVALID_UTF8`, and `INVALID_FORMAT`. Failure display contains
only the exact known path and a calm local status: no private content, OS
detail, traceback, discovery, repair, or regeneration.

Reading is lazy: not at construction, entry, `/look`, or `/help`; only on an
explicit eligible `/results`. There is no cache, so every such request rereads
the exact source.

## 11. Existing deliberate Return Opening

The existing manual path remains:

```text
place a returned Artifact deliberately in known incoming/
-> start OPEN_RETURN.sh explicitly
-> use the sole candidate only when exactly one is present
-> validate and structurally match its Return Slot
-> create or reuse one stable local result
```

Candidate determination is limited to the known Workspace `incoming/*.json`.
Zero candidates fail calmly; multiple candidates are listed and never selected
automatically. This deliberate Opening existed before Slice 5A.

## 12. Slice 5A duplicate-identity hardening

Slice 5A hardened the existing Opening path. After Artifact and Slot parsing,
all canonical Return Slot identities `(origin_trace_id, return_slot_id)` are
checked globally. Any repeated occurrence invalidates the entire typed Slot
list before any generator call, writer construction, directory creation,
temporary file, result write, or Slot-status update.

Any duplicate identity invalidates the whole Opening. No slot is selected,
deduplicated, renamed, generated, written, or repaired. Unique slots preserve
their existing order and Opening behavior.

## 13. Opening versus `/results`

Opening and rereading are independent boundaries.

Opening validates a deliberately returned Artifact, matches a Return Slot,
creates the stable result once, and may update Slot state under the existing
contract.

`/results` reads only an already existing stable result. It never imports or
invokes Opening, parses a Return Artifact, validates or updates a Return Slot,
starts a generator, writes, regenerates, repairs, or overwrites.

## 14. Privacy and publication boundary

Nothing is uploaded, synchronized, transferred, or published automatically.
Travelling invitation and Return Artifact may be moved only deliberately. The
private Return Workspace, stable result, known local result path, and technical
trace remain with the waiting person's local environment and never enter the
travelling carrier.

## 15. Carrier boundary

The neutral carrier uses an explicit static runtime allowlist. It includes
`atrium/known_source.py` and `atrium/stable_result.py` byte-identically. Both
modules and their exported symbols are isolated-import capable from the
carrier. No scanner or dynamic dependency discovery was introduced.

## 16. Release invariants

- no Workspace, Downloads, Token, Artifact, or result discovery;
- no filename guessing, fallback source, or general registry;
- no automatic candidate choice under ambiguity;
- no silent overwrite, regeneration, repair, transfer, or publication;
- room entry and `/look` remain nonproductive;
- help and dispatch share room-local capabilities;
- same-process and Stable-source results remain separate;
- same-process result precedence remains authoritative;
- BLOCKED remains nonproductive;
- Opening and `/results` remain separate.

## 17. Explicitly deferred architecture

Deferred beyond this checkpoint:

- final language-wide editing and complete release-play acceptance;
- manual-note detection or display in Stable-result views;
- a canonical `/atrium` replacement for Chamber `/quit`;
- direct return to the same Resonance Surface after a productive cycle;
- migration of Legacy or standalone First Spark to further shared conventions;
- any graphical launcher or non-terminal accessibility layer;
- any registry, discovery service, cache, database, or second persistence
  architecture.
