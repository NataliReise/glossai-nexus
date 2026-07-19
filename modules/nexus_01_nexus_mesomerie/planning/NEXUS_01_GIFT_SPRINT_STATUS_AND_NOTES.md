# Nexus 01 Gift Sprint — Status and Notes

## Document role

This is the concise living status document for the Nexus 01 gift sprint. It
records the current technical checkpoint, accepted behavior, remaining release
work, and immediate next steps. It is not a substitute for the canonical
contracts:

- `NEXUS_01_CHAMBER_STATES_AND_RESULTS_V03.md`
- `NEXUS_01_GIFT_SPRINT_PLAN_V03.md`

When this document conflicts with a current versioned planning document, the
current versioned document takes precedence.

## Current sprint position

- Branch: `gift/nexus-01-chamber-archive`
- Technical baseline checkpoint: `59c6595`
- Commit: `feat(nexus-01): read stable local resonance results`
- Technical baseline status: committed and pushed
- Upstream: `origin/gift/nexus-01-chamber-archive`
- Local and upstream were synchronized at the last confirmed inventory.
- Last confirmed relation to `origin/main`: 17 commits ahead, 0 behind
- Major technical slices: complete through Stable-result Revisit
- Last confirmed canonical suite: 43 test files, 408 tests, 0 failures,
  0 errors, 0 skipped
- Current phase: planning-document synchronization before Slice 6A and
  Slice 7A

The checkpoint is technically implemented and automatically verified. Earlier
manual slice-level acceptance remains valid where explicitly recorded. Final
language-wide and full release-play acceptance has not yet occurred.

## Implemented technical checkpoint

All entries in this section are implemented and technically accepted at
checkpoint `59c6595`. Automatic verification is complete; final language-wide
and full release-play acceptance remains pending.

### Resonance entry and local capabilities

- **4B.0a — Neutral Resonance Entry:** corrected COMPOSE and ANSWER first enter
  a quiet `resonance>` Surface. Productive work starts only through explicit
  `/compose` or `/answer`.
- **4B.0b — Description, Help and Capabilities:** Pre- and Post-run share a
  small Resonance-local typed capability source used by both help and dispatch.
  `/look` renders room and state without a command list.
- **4B.0c — BLOCKED Resonance Surface:** BLOCKED exposes exactly:

  ```text
  /look
  /help
  /quit
  ```

  It performs no productive action, result reading, Token search, selection,
  repair, or mutation.

### Atrium exploration

- **4C — Atrium Exploration Surface:** room/state description and help are
  separate. `/look` shows the Atrium and perceptible paths. `/help` shows only
  currently available navigation actions. Help and dispatcher share one small
  Atrium-local capability source.
- The short `/help` orientation appears once per terminal process.
- First Spark and Legacy retain their existing scoped behavior.

### Known-source handoff and byte boundary

- **4B.1 — Explicit Known-source Handoff:**

  ```text
  --known-resonance-source ABSOLUTE_PATH
  -> run_corrected_nexus(...)
  -> ClassifiedResonanceController
  ```

  The lexical absolute path is explicit, process-local, not resolved, not
  searched, not persisted, and not serialized into Activation or the carrier.
- **4B.2 — Safe Known-source Boundary:** `read_known_source_bytes()` performs
  bounded raw-byte reading through a read-only descriptor with `O_NOFOLLOW`,
  validates the opened descriptor as a regular file, and returns immutable
  typed statuses without path or OS-error leakage.
- Accepted limitation: `O_NOFOLLOW` protects the final path segment;
  parent-directory symlinks are not fully excluded by this narrow boundary.

### Same-process and Stable-source results

- **4A — Same-process Results:** `CompletedComposeResult` and
  `CompletedAnswerResult` retain the latest successful current-process result
  for their existing allowlisted `/results` view.
- **5B — Stable-result Revisit:** `read_stable_resonance_result()` reads one
  explicit stable Markdown path only on an eligible explicit `/results`.
- The Stable-result reader requires strict UTF-8 and the complete canonical
  Markdown format. It validates the technical JSON trace but exposes only five
  compact-Nachhall lines through `StableResonanceView`.
- Failure statuses are `MISSING`, `SYMLINK`, `NOT_REGULAR`, `UNAVAILABLE`,
  `TOO_LARGE`, `INVALID_UTF8`, and `INVALID_FORMAT`. Display remains calm and
  limited to the exact known path and local status.
- Reading is lazy: not at construction, Chamber entry, `/look`, or `/help`.
- There is no cache. Every explicit Stable-source `/results` rereads the exact
  known path.
- Same-process result precedence is authoritative: when
  `_last_completed_result` exists, the Stable-result reader is not called and
  the known source path is not displayed.
- Same-process result types and `StableResonanceView` remain separate models.

### Existing deliberate Return Opening and Slice 5A hardening

- The deliberate manual Return Opening path existed before Slice 5A and
  remains preserved.
- The person places an Artifact deliberately in the known private Workspace
  `incoming/` directory and starts `OPEN_RETURN.sh` explicitly.
- Candidate inspection is limited to that known `incoming/*.json` boundary.
  Zero candidates fail; exactly one may be used; multiple candidates are not
  selected automatically.
- Opening validates the Artifact, structurally matches the Return Slot,
  creates the stable local result once without overwrite, and may update Slot
  state under the existing recovery contract.
- **5A — Duplicate Return Slot Identity Hardening:** all canonical Slot
  identities are checked globally after parsing and before any generator call,
  writer, directory creation, temporary file, result write, or Slot-status
  update. A duplicate causes total fail-closed abort with zero productive
  mutation.
- Slice 5A hardened the existing Opening; it did not introduce the complete
  Opening mechanism.

### Neutral-carrier packaging

- **5B.0 — Neutral Carrier Known-source Packaging Bridge:** the existing safe
  known-source boundary was added explicitly to the neutral runtime package.
- `atrium/known_source.py` and `atrium/stable_result.py` are explicitly present
  in the static neutral-runtime allowlist.
- Both are copied byte-identically and are isolated-import capable from the
  carrier.
- No scanner, registry, or dynamic dependency discovery was introduced.

## Opening and `/results` separation

Opening:

- validates a deliberately returned Artifact;
- matches its Return Slot;
- creates or reuses one stable local result;
- may update Slot state under the existing contract.

`/results`:

- reads only an already existing allowed result source;
- never invokes Opening;
- never reads a Return Artifact as a prerequisite for Revisit;
- never validates or modifies a Return Slot;
- never starts a generator;
- never writes, regenerates, repairs, or overwrites.

## Verification status

### Current canonical baseline

At checkpoint `59c6595`:

```text
43 test files
408 tests
0 failures
0 errors
0 skipped
```

The checkpoint and neutral-carrier packaging are committed and pushed.

### Historical manual acceptance

Earlier accepted manual records remain applicable to the slices they covered,
including corrected COMPOSE exploration, walkthrough and cancellation;
strict Atrium and First Spark slash grammar; Slice 3 post-run behavior; and
Slice 4A/4A.1 same-process results and neutral Return Artifact naming.

These historical records do not claim final Slice-7 acceptance of every newer
entry, BLOCKED, Known-source, Opening-hardening, Stable-result, and carrier
combination.

## Release boundaries

The current checkpoint preserves:

- no Workspace, Downloads, Token, Artifact, or old-result discovery;
- no filename guessing or general result registry;
- no automatic candidate selection under ambiguity;
- no automatic transfer, publication, regeneration, repair, or overwrite;
- separate same-process and Stable-source result models;
- Same-process precedence;
- lazy uncached Stable-source rereading;
- exact nonproductive BLOCKED capabilities;
- strict separation of Opening and `/results`;
- private Workspace paths and stable results outside the travelling carrier.

## Remaining release work

The accepted future release sequence is:

```text
Slice 6
-> Slice 7
-> Slice 7.5
-> Slice 8
```

None of these slices is complete at the current checkpoint.

### Slice 6A — read-only language-surface inventory

Inventory all player-facing text without source edits. Classify findings as
`MUSS`, `SOLLTE`, or `SPÄTER`, and as language error,
text/state mismatch, technical error, or documentation drift.

### Slice 7A — manual baseline play verification

In controlled overlap with Slice 6A, run a baseline play verification against
a fresh carrier/gift copy frozen at checkpoint `59c6595`. No source edits occur
during that baseline.

The later final play arc must cover:

```text
COMPOSE
-> ANSWER
-> RETURN OPENING
-> RESULT REVISIT
```

It also covers second COMPOSE, BLOCKED, cancellation, repeated unchanged
Opening, Same-process precedence, missing and invalid Known Source, and the
no-discovery/no-regeneration/no-overwrite boundaries.

### Slice 7.5 — read-only whole-project release audit

Slice 7.5 begins only after accepted Slice 6 and Slice 7 work and a clean,
committed, pushed checkpoint. Its first task is a completely read-only audit of
the project concept, architecture and responsibility boundaries, repository
orientation, documentation drift, and small evidenced cleanup candidates.

Findings are classified as `RELEASE-BLOCKER`,
`KLEINER SICHERER ABSCHLUSSFIX`, or
`NACHFOLGEARBEIT NACH DEM RELEASE`. The audit also proposes, without writing,
a GitHub short description, README introduction, and concise conceptual project
description. No suggestion authorizes a change automatically. Selected work
receives separate narrow tasks; authorized mini-documentation synchronization
occurs in this slice. A Wiki defaults to post-release work. Slice 8 requires a
new clean, committed, pushed checkpoint after the Slice-7.5 decisions.
A confirmed unresolved `RELEASE-BLOCKER` blocks entry into Slice 8 and cannot
be declined without evidence-based reclassification.

### Slice 8 — Release Freeze

Slice 8 verifies and freezes the accepted result. Planned orientation and
mini-documentation synchronization belong to Slice 7.5, not Slice 8. The freeze
permits only demonstrated release-error corrections, final tests, package
creation and isolated package verification before separate PR, merge, and tag
decisions.

## Immediate next step

1. Finish and review this planning-document synchronization.
2. After explicit authorization, establish a clean committed and pushed
   planning checkpoint.
3. Run Slice 6A read-only language-surface inventory.
4. In controlled overlap, run Slice 7A manual baseline play verification
   against frozen checkpoint `59c6595`.
5. Combine both finding sets before authorizing any language edits.

Slice 7.5 is the later gate after completed and accepted Slice 6 and Slice 7;
its audit does not begin now.

No language edit, documentation expansion outside the authorized planning
scope, PR, merge, or tag is authorized by this status update.

## Maintenance rule

Update this document after an accepted slice, a meaningful verified checkpoint,
or an approved release decision. Keep it concise and status-oriented.

Do not place private names, local usernames, hostnames, absolute home-directory
paths, private addresses, private Artifact or Token content, or other local
machine identifiers in this tracked document.
