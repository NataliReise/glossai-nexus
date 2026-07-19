# Nexus 01 Gift Sprint — Status and Notes

## Document role

This document records the current implementation status, verified behavior,
manual observations, accepted programme additions, deferred improvements, and
immediate next steps for the Nexus 01 gift sprint.

It is not a normative architecture or design specification.

Canonical intended behavior remains defined by:

- `NEXUS_01_CHAMBER_STATES_AND_RESULTS_V02.md`
- `NEXUS_01_GIFT_SPRINT_PLAN_V02.md`

When this document conflicts with a current versioned planning document, the
planning document normally takes precedence. Accepted interaction changes added
after V0.2 are recorded here as the current working-tree contract until the
versioned planning examples are synchronized.

This document is intended to remain current. Superseded observations may be
removed or moved to a short resolved section rather than accumulated as a full
development diary.

---

## Current sprint position

- Branch: `gift/nexus-01-chamber-archive`
- Current concept: V0.2
- Mission 1 — completion semantics and corrected gift-path integration:
  implemented in the working tree, not yet committed
- Slice 2A — exploration commands and Resonance-local indentation:
  implemented and accepted
- Slice 2A.1 — safe handling of unknown slash commands:
  implemented and accepted
- Slice 2B — confirmed step-aware walkthrough:
  implemented and accepted
- Slice 2C — unified `/cancel` grammar in corrected Resonance:
  implemented and accepted
- Slice 2C.1 — cancellation consistency and player-facing threshold copy:
  implemented and accepted
- Slice 2D-A — strict slash-command grammar for the Atrium:
  implemented and accepted
- Slice 2D-B — strict slash-command grammar for First Spark:
  implemented and accepted
- Slice 2D-C — Resonance grammar consistency review:
  completed and accepted; Outcome A — already consistent
- Slice 3 — post-run behavior and explicit new cycles:
  implemented and accepted
- Slice 4A — same-process Resonance results:
  implemented, reviewed, automatically verified, and manually accepted
- Slice 4A.1 — automatic neutral Return Artifact filename:
  implemented, reviewed, automatically verified, and manually accepted
- Slice 4B — Resonance entry and known-source rereading after restart:
  entry/help and path-handoff inventories completed; architecture decisions
  recorded; subdivided into 4B.0a-c and 4B.1-2; not implemented or authorized
- Next implementation candidate:
  4B.0a — Neutral Resonance Entry; no implementation authorization exists
- Slice 4C — Atrium Exploration Surface:
  planned; not implemented and not authorized
- Slice 5 — Return, Local Completion, and Result Revisit:
  inventory completed and planning updated; operative technical Opening
  infrastructure exists, but 5A and 5B remain unimplemented and unauthorized
- Implementation authorization:
  none for Slice 4B or Slice 5
- Slice 4A / 4A.1 repository closure:
  committed and pushed
- Implementation commit:
  `0da16511d3c068b7afbad7632d36566a0d14de4d`
- Acceptance, status, and planning commit:
  `62dc94b0d08a57d8b61127d7f01bfb723981896e`
- Published branch:
  `origin/gift/nexus-01-chamber-archive`

---

## Accepted implementation

### Mission 1 — completion semantics

The current working tree distinguishes:

- successful completion of one productive Resonance cycle;
- the Atrium-level milestone that at least one successful cycle occurred;
- the continuing availability and future repeatability of the Resonance Chamber.

Current completion rules:

- COMPOSE completes only after both the travelling invitation and the private
  Return Workspace have been created successfully.
- ANSWER completes only after the Return Artifact has been written successfully.
- Cancellation, validation failure, publication failure, or incomplete
  destination entry does not mark the cycle complete.
- Existing output is not silently overwritten.
- A completed cycle must not restart automatically.

### Slice 2A — exploration commands and indentation

Corrected COMPOSE and ANSWER choice and word prompts support:

```text
/look
/help
/trace
```

Verified behavior:

- information commands do not advance the productive flow;
- information commands do not return a choice or word;
- earlier selections remain unchanged;
- later choices are not exposed early;
- the complete unchanged current prompt is rendered again afterward;
- prompt headings, underlines, and input prompts remain at zero indentation;
- choices, word guidance, Chamber prose, help, and traces use two-space
  indentation;
- plain `look`, `help`, and `trace` remain ordinary possible word values;
- `/cancel` retains its choice- and word-prompt behavior.

### Slice 2A.1 — unknown slash-command protection

When an information-command handler is active, every slash-prefixed input is
treated as Chamber command syntax.

Known commands retain their existing behavior.

Unknown slash-prefixed commands:

- are consumed as commands;
- are not accepted as numbered choices;
- are not accepted as wish or return words;
- do not advance mechanical progress;
- display a short neutral correction;
- redisplay the full unchanged current prompt.

Without an information-command handler, existing legacy behavior remains
unchanged.

### Slice 2B — confirmed step-aware walkthrough

Corrected COMPOSE and ANSWER choice and word prompts support:

```text
/walkthrough
```

Verified behavior:

- the walkthrough begins only after an explicit confirmation;
- declining leaves the productive prompt unchanged;
- guidance explains one current step at a time;
- all visible choices remain available;
- guidance never chooses, fills, validates, creates, or advances anything;
- each newly supplied mechanical step receives guidance at most once;
- invalid input and information-command prompt replays do not repeat guidance;
- `/walkthrough` while active ends guidance without leaving the Chamber;
- restarting later guides the current authoritative step once;
- plain `walkthrough` remains a valid wish or return word;
- walkthrough state remains transient to the current Chamber visit.

### Slice 2C and 2C.1 — unified full-cycle cancellation

The corrected Resonance Chamber now uses:

```text
/cancel
```

as the canonical safe full-cycle cancellation command at every interactive
boundary:

- choice prompts;
- one-word prompts;
- walkthrough confirmation;
- creation confirmation;
- local destination prompts.

Verified behavior:

- `/cancel` ends the entire current productive Resonance cycle;
- cancellation creates no new output and yields `completed=False`;
- `/walkthrough` while active still ends guided mode only;
- bare `cancel` at walkthrough confirmation still declines guidance locally;
- existing confirmation aliases remain compatible;
- blank destination input remains cancellation;
- only the complete normalized value `/cancel` is special at destination
  prompts;
- path values such as `/cancelled/example` remain ordinary paths;
- `allow_cancel=False` disables the nested walkthrough-confirmation command
  consistently;
- corrected threshold copy presents current player grammar rather than
  implementation history.

---

## Verification record

### Automated verification reported by Codex

After Slice 2D-B:

- focused First Spark flow and runtime-entry tests passed;
- related Atrium and activation integration tests passed;
- packaging-isolation tests passed: 11 tests;
- canonical Nexus 01 runner passed:
  344 tests, 0 failures, 0 errors, 0 skipped;
- `git diff --check` passed;
- no file was staged;
- no commit or push occurred.

These results are recorded as reported by Codex. The canonical test run was
also executed once more manually after an accidental multiline terminal paste
and again completed with 344 passing tests.

### Manual COMPOSE exploration smoke test

Verified manually:

- command case-folding;
- trailing-whitespace handling;
- prompt replay after information commands;
- unknown slash-command rejection;
- preservation of earlier choices;
- ordinary `help` accepted as a wish word;
- safe cancellation without output creation.

### Manual COMPOSE walkthrough smoke test

Verified manually:

- `/help` advertises `/walkthrough`;
- walkthrough confirmation activates guidance;
- the current step is guided once;
- `/look`, `/help`, `/trace`, and `/unknown` do not repeat guidance;
- the next mechanical step is guided once while active;
- `/walkthrough` ends guidance without changing the productive step;
- later steps remain unguided after stopping;
- a declined restart leaves the prompt unchanged;
- restarting later guides the current step once;
- plain `walkthrough` is accepted as a wish word;
- final refusal creates no invitation or private workspace;
- the cycle returns with `completed=False`.

### Manual COMPOSE unified-cancellation smoke tests

Verified manually:

- `/cancel` at walkthrough confirmation ends the full COMPOSE cycle;
- `/cancel` at creation confirmation ends the cycle without destination prompts;
- a destination path beginning with `/cancelled/` remains ordinary path input;
- exact `/cancel` at the following destination prompt cancels safely;
- no invitation or private Return Workspace is created;
- each tested cycle returns with `completed=False`.

### Manual Atrium strict-slash smoke test

Verified manually:

- bare `look` is rejected;
- bare `help` opens canonical slash help;
- `/LOOK` works after case normalization;
- bare `first-spark` is rejected;
- `/first-spark` enters First Spark;
- First Spark still uses its pre-2D-B bare grammar;
- bare `quit` leaves First Spark but is rejected after returning to the Atrium;
- `/quit` leaves Nexus 01;
- the visible transition between modernized Atrium grammar and the still
  unchanged First Spark grammar behaves as designed.

### Manual First Spark strict-slash smoke test

Verified manually through the integrated Atrium journey:

- `/first-spark` enters First Spark;
- bare `help` opens canonical slash help;
- bare `look`, `read welcome.log`, `unlock`, and `quit` are rejected neutrally;
- `/look` renders the Chamber;
- `/read missing.log` preserves trace-specific validation;
- `/read welcome.log` and `/read spark.note` read both traces;
- `/link noon` preserves target-specific validation;
- `/link spark` links the fragments;
- `/unlock` opens the private message and completes First Spark;
- `/resonance-node` remains available only after completion and is view-only;
- `/quit` returns to the Atrium;
- the Atrium marks First Spark complete;
- a second `/quit` leaves Nexus 01.

### Manual recovery-path observation

When an activation expects an authoritative selected Token context that is
missing, invalid, altered, or mismatched:

- the Resonance path enters blocked recovery guidance;
- no productive Chamber interaction begins;
- no output is written;
- COMPOSE and legacy paths are not substituted automatically;
- control returns safely to the Atrium.

---

## Current interaction grammar

### Dedicated command surfaces

Atrium and First Spark use canonical slash commands.

Bare `help` remains an unadvertised rescue alias only at those dedicated command
prompts.

### Corrected Resonance choice and word prompts

```text
/look
/help
/trace
/walkthrough
/cancel
```

Only slash-prefixed forms ask the Chamber to act.

Plain one-word values remain ordinary requested content, including:

```text
help
look
trace
walkthrough
cancel
```

### Walkthrough confirmation

Accepted ordinary answers:

```text
yes
y
no
n
cancel
q
```

With cancellation enabled, exact `/cancel` ends the full productive Resonance
cycle.

With cancellation disabled, `/cancel` is invalid yes/no input and the
confirmation prompt repeats.

### Creation confirmation

Accepted ordinary answers:

```text
yes
y
no
n
cancel
q
```

Exact `/cancel` also ends the full cycle safely.

### Destination prompts

- exact normalized `/cancel` ends the cycle safely;
- blank input remains a compatibility cancellation form;
- slash-prefixed paths other than exact `/cancel` remain ordinary path input;
- `/cancelled/example` and `/tmp/cancelled/example` are preserved as paths.

---

## Accepted programme additions

### Slice 2D — resolved cross-surface grammar model

The accepted Nexus 01 interaction rule is:

```text
/system-command [argument]
ordinary input only when explicitly requested
```

Resolved behavior:

- Atrium and First Spark are dedicated command surfaces;
- all actions on those surfaces use slash commands;
- bare `help` is retained only as an unadvertised rescue alias there;
- corrected Resonance uses slash commands for Chamber actions;
- plain words, numbers, confirmation answers, and paths remain ordinary input
  when Resonance explicitly requests them;
- First Spark mechanical actions use `/read`, `/link`, and `/unlock`;
- `/cancel` belongs to cancellable productive Resonance interaction and is not
  added to Atrium or First Spark merely for symmetry;
- no shared or general parser is required.

Status: **implemented, reviewed, and accepted**


### Slice 2C — unified `/cancel` grammar

The canonical safe full-cycle cancellation grammar is now implemented across
the corrected Resonance interaction.

Status: **implemented and accepted**

### Slice 2D-A — strict Atrium slash-command grammar

The Atrium now exposes only:

```text
/look
/help
/first-spark
/resonance
/quit
```

as canonical system commands.

Verified behavior:

- bare `help` remains an unadvertised rescue alias;
- former bare navigation and exit commands are rejected neutrally;
- unknown input is not echoed and points to `/help`;
- slash commands remain stripped and case-normalized;
- `/resonance` remains state-dependent;
- routing, progression, cancellation, unavailable-door, and Ctrl-C semantics
  remain unchanged;
- integration and packaging fixtures use slash forms only at Atrium boundaries;
- First Spark internal bare commands remain unchanged until Slice 2D-B.

Status: **implemented and accepted**

### Slice 2D-B — strict First Spark slash-command grammar

First Spark now exposes slash commands for every action that instructs the
surface to act:

```text
/help
/look
/trace
/walkthrough
/read <trace-name>
/link spark
/unlock
/quit
/resonance-node
```

Verified behavior:

- bare `help` is the sole unadvertised rescue alias;
- former bare commands are rejected neutrally and do not mutate state;
- `/read` and `/link` retain module-owned argument validation;
- the puzzle sequence and completion boundary are unchanged;
- `/resonance-node` remains ending-only and view-only;
- help, walkthrough, and current player documentation use slash forms;
- integrated and standalone entry behavior remain intact;
- Atrium strict-slash behavior remains unchanged.

Status: **implemented and accepted**

### Slice 2D-C — Resonance grammar consistency review

The read-only review found corrected COMPOSE and ANSWER already consistent with:

```text
/system-command [argument]
ordinary input only when explicitly requested
```

Confirmed:

- no remaining bare action command exists in corrected Resonance;
- no bare `help` rescue alias is appropriate at content prompts;
- plain command words remain valid wish or return words;
- unknown slash input is consumed and rerenders the same prompt;
- exact `/cancel` is special at every enabled productive boundary;
- bare confirmation declines remain requested answers, not action commands;
- destination paths preserve slash syntax except for exact `/cancel`;
- no production correction or 2D-C.1 slice is needed.

Useful later test clarification:

- explicitly assert that plain `cancel` remains a valid wish and return word;
- optionally assert that `/cancelled` is unknown command syntax at corrected
  word prompts.

Status: **completed and accepted — Outcome A**

---

## Observations and future improvements

### Guidance placement

The transient Resonance guidance session currently lives beside the
Resonance-specific terminal adapter.

Reason:

- the adapter is already included in packaged carriers;
- a separate guidance module caused packaging-isolation failures;
- no packaging file needed to be widened.

Status: **accepted for the gift sprint**

A later extraction would require an explicit packaging decision.

### Repeated information requests

Repeated `/help`, `/look`, and `/trace` requests currently return stable
step-specific responses.

Status: **accepted**

Future deepening or variation may be explored only if it remains predictable,
non-mutating, and testable.

### Walkthrough spoiler boundary

The current walkthrough explains that it reveals the purpose of remaining steps,
but does not literally use the word “spoiler”.

Status: **accepted for the current slice**

Review only during later language-wide editing.

### Result and post-run commands

Corrected completed COMPOSE and ANSWER post-run surfaces now expose:

```text
/results
```

The command is process-local and view-only. It is not available during an active
productive cycle, and bare `results` remains unknown.

Status: **implemented and accepted in Slice 4A**

Slice 4A is correct and remains in place. Its accepted contract is
Resonance-only, process-local, view-only, and limited to the most recent
successful COMPOSE or ANSWER result in the current process/controller session.
`/results` performs no filesystem search, registry lookup, regeneration,
Opening, mutation, transmission, or publication.

### Versioned command-example synchronization

Some V0.2 planning examples still show pre-strict bare command spellings.

This is documentation drift only; the current runtime contract is the accepted
strict slash grammar recorded in Slices 2D-A through 2D-C.

Status: **deferred to later documentation synchronization**

### Existing activation recovery

Blocked recovery correctly refuses to guess or discover a nearby Token.

Status: **accepted safety behavior**

Future work may improve the player-facing recovery dialogue without weakening
the authoritative selected-context boundary.

---

## Deferred scope

The following remain outside the accepted implementation:

- rereading known existing results after process restart;
- filesystem result discovery or selection;
- selecting another Token for another ANSWER cycle;
- Legacy exploration;
- expanded blocked-recovery dialogue;
- persistent exploration state;
- a general result registry;
- general filesystem search or automatic selection among multiple Artifacts;
- automatic Return Artifact transfer, return, publication, or Opening;
- cloud synchronization or archive integration;
- regeneration or overwrite of Resonance Artifact, Nexus Echo, Nachhall, or a
  stored stable local result;
- a new persistence architecture without a prior read-only inventory;
- multiple Return Artifacts for the same Return Slot;
- broad terminal-width or automatic-wrapping support;
- language-wide final editing.

---

## Revised sprint sequence

```text
Mission 1     completion semantics
Slice 2A      exploration and indentation
Slice 2A.1    unknown slash-command protection
Slice 2B      confirmed step-aware walkthrough
Slice 2C      unified /cancel grammar
Slice 2C.1    cancellation consistency hardening
Slice 2D-A    strict Atrium slash-command grammar
Slice 2D-B    strict First Spark slash-command grammar
Slice 2D-C    Resonance grammar consistency review
Slice 3       post-run and explicitly new cycles
Slice 4A      same-process results
Slice 4A.1    automatic neutral Return Artifact filename
Slice 4B.0a   neutral Resonance entry
Slice 4B.0b   Resonance description, help, and capabilities
Slice 4B.0c   BLOCKED Resonance surface
Slice 4B.1    known-source handoff
Slice 4B.2    known-source read-only rereading after restart
Slice 4C      Atrium Exploration Surface
Slice 5A      manual Return Opening and stable local result creation
Slice 5B      read-only revisit of that already created stable local result
Slice 6       language editing
Slice 7       tests and manual play verification
Slice 8       release freeze
```

Slices 2C and 2D are complete and accepted.

---


## Slice 3 — post-run behavior and explicit new cycles

Implemented behavior:

- a successful corrected COMPOSE or ANSWER cycle sets one transient,
  controller-owned completed-cycle gate;
- the Atrium milestone continues to mean only that at least one Resonance cycle
  succeeded;
- a later `/resonance` visit enters a Resonance-owned post-run command surface;
- no productive cycle restarts automatically.

### COMPOSE post-run surface

```text
/look
/help
/trace
/compose
/quit
```

Bare `help` is the sole unadvertised rescue alias.

`/compose` begins one fresh independent originating cycle.

### ANSWER post-run surface

```text
/look
/help
/trace
/quit
```

No `/answer` or in-process Token replacement exists.

Another ANSWER requires leaving Nexus 01 and deliberately activating or opening
it with another Token context.

### Exit grammar

Use `/quit`, not `/leave`.

- `/cancel` aborts an active productive cycle;
- `/quit` leaves the current non-productive Chamber surface;
- Atrium `/quit` leaves Nexus 01.

### Verification

Codex reported:

- focused COMPOSE tests: 20 passed;
- focused ANSWER tests: 15 passed;
- classified Resonance tests: 6 passed;
- related Atrium, Legacy, and packaging tests passed;
- canonical suite: 354 tests, 0 failures, 0 errors, 0 skipped;
- `git diff --check` passed.

Manual integrated COMPOSE verification confirmed:

- a failed first publication outside the allowed boundary creates no output and
  does not activate the post-run gate;
- a successful first cycle creates exactly one invitation/workspace pair;
- later `/resonance` enters the completed-cycle surface;
- bare `help` works, while bare `compose` and `/leave` are rejected;
- `/look`, `/LOOK`, and `/trace` remain non-productive;
- `/compose` explicitly begins a fresh cycle;
- `/cancel` aborts that second active cycle;
- the earlier completed milestone remains intact;
- later `/resonance` returns to the completed-cycle surface;
- post-run `/quit` returns to the Atrium;
- Atrium `/quit` leaves Nexus 01.

The ANSWER post-run contract is covered by focused tests and was not manually
replayed in this COMPOSE-oriented smoke session.

### Resolved by Slice 4A

```text
/results
```

Same-process presentation of the most recent successful corrected Resonance
result is implemented. Result selection, persistent registries, and output-path
indexing remain outside the accepted scope.

### Persistence boundary

The Slice 3 gate is process-local only.

Preventing duplicate ANSWER cycles across process restarts would require a new
persistent answered/consumed marker or a broader activation lifecycle. That is
not part of the current gift sprint.

Status: **implemented and accepted**

## Slice 4A — same-process Resonance results

Status: **implemented, reviewed, automatically verified, and manually accepted**

The corrected Resonance controller retains one typed latest-result anchor using
`CompletedComposeResult` or `CompletedAnswerResult`. It represents only the most
recent successful corrected Resonance cycle in the current controller session.
It is Resonance-only, process-local, and not a registry, history, selection menu,
or persistent record.

`/results` is available only on completed COMPOSE and ANSWER post-run surfaces.
Bare `results` remains unknown, and active productive flows do not expose the
command. Viewing is allowlist-based and causes no Opening, matching, generation,
Nachhall, transmission, publication, or state mutation.

The display separates:

```text
[private local]
[public-safe]
[local path]
```

COMPOSE shows only the retained originating contribution and its two known
output paths. ANSWER shows only the retained carried contribution, response
selections, return word, optional carried public-safe label or calm absence
message, and known Return Artifact path. Internal Token, Route, Return Slot,
package, activation, and object-representation details are not displayed.

A later successful COMPOSE replaces only the in-memory session view. Earlier
external invitations and private Return Workspaces remain separate and are not
deleted, overwritten, invalidated, hidden, or searched. Cancellation,
validation failure, publication failure, and Artifact-write failure do not
replace the last successful retained result.

For an unavailable known output, retained in-memory values remain visible. Only
the exact known path is checked; it is reported as no longer available at that
location, and the display states that no filesystem search was performed. No
substitute is discovered, no regeneration occurs, and no result state is
destroyed.

### Slice 4A.1 — automatic neutral Return Artifact filename

Status: **implemented, reviewed, automatically verified, and manually accepted**

Corrected ANSWER now asks:

```text
Parent directory for the Return Artifact (blank to cancel):
```

The player selects an existing external parent directory. The controller creates
one neutral name of the form:

```text
n01-return-artifact-<24 lowercase hexadecimal characters>.json
```

The opaque identifier uses secure random data equivalent to
`secrets.token_hex(12)`. It contains no timestamp, wish word, return word, name,
Token ID, Route ID, path fragment, username, or personal content. Up to eight
random candidates are attempted. Collisions never overwrite existing material;
exhaustion creates nothing. The existing atomic writer remains the final
no-overwrite boundary.

Only existing directories outside the travelling Nexus carrier are accepted.
Files and nonexistent destinations are rejected calmly. Completion and
`CompletedAnswerResult` retention occur only after successful writing, and a
later failed write does not replace an earlier successful result.

### Slice 4A verification and manual acceptance

During the Slice 4A.1 implementation and acceptance sequence, Codex reported:

- ANSWER: 21 tests, passed;
- COMPOSE: 22 tests, passed;
- packaging regression: 11 tests, passed;
- canonical runner: 363 tests, 0 failures, 0 errors, 0 skipped;
- `git diff --check`: successful.

These tests are historical acceptance facts and were not rerun by the later
documentation-only status update.

Manual COMPOSE acceptance in a fresh integrated Nexus copy confirmed that
`/results` is absent during productive work; a successful cycle creates one
invitation and one private Return Workspace; the completed surface shows the
retained values and exact known paths; a second explicit COMPOSE becomes the
session view while both external output pairs coexist; and cancelling a third
cycle preserves the second result. No prior output was removed or overwritten,
and no internal identifier was displayed.

Manual ANSWER acceptance in a fresh integrated Nexus copy with a deliberately
selected valid Token V2 confirmed true ANSWER mode, one automatically named
Return Artifact in the selected external directory, the neutral 24-hex naming
contract, non-productive completed re-entry, and allowlisted `/results` output.
When no carried public-safe summary exists, the display says so calmly. Moving
the Artifact away left all retained values visible, marked the exact known path
unavailable, stated that no search occurred, and generated nothing new. No
Token, Route, Return Slot, package, or object internals were shown.

The earlier manual use of an existing directory at the former full-file-path
prompt was safely rejected by the writer without overwriting anything. This was
a usability mismatch, not a safety failure, and Slice 4A.1 corrected it before
final acceptance.

### Persistence boundary

```text
4A: same current process/controller -> in-memory result -> /results
4B: new process -> deliberately selected known source -> read existing content
```

Slice 4A does not survive restart, discover old output folders, scan the
filesystem, guess filenames, gather Tokens automatically, build an archive or
registry, synchronize remotely, or reread files to reconstruct same-process
state. The Slice 4B/5 read-only inventory is complete; implementation remains a
separate, unapproved problem.

## Planned result stages and future boundaries

The result stages are distinct:

```text
1. COMPOSE
   -> originating contribution
   -> travelling invitation
   -> private Return Workspace

2. ANSWER
   -> answer contribution
   -> Return Artifact

3. RETURN OPENING
   -> returned Return Artifact
   + matching Return Slot
   -> stable local Resonance result
```

The Return Artifact produced by ANSWER is initially a transport object. It is
not itself the final stable local result. The inventory confirmed that the
current operative production Opening is implemented by
`open_resonance_return.py`, centrally through
`open_resonance_return_files()`. It creates, atomically and without overwrite,
exactly one stable Markdown file at:

```text
<private Return Workspace>/results/<ReturnSlot.result_file>
```

Decision taken: this existing Markdown file is the authoritative stable local
production result for the gift sprint. It contains the visible compact Nachhall,
an embedded technical trace, and may later contain manual additions. In the
current production path, the compact Nachhall is not an optional later component
but the complete visible stable result form. No new separate production files
for Resonance Artifact or Nexus Echo will be introduced for the gift sprint.
Existing renderers and terminology for those outputs are legacy material, not
the current production contract.

### Slice 4B — Resonance entry and known-source rereading

Status: **entry/help and path-handoff inventories completed; decisions taken;
planning updated; all subsections not implemented and not authorized**

The read-only inventory left the repository unchanged. It confirmed these
current facts:

- `ClassifiedResonanceController.__call__()` immediately starts
  `_run_compose()` or `_run_answer()` on first entry today;
- the Slice 4A post-run Surface already provides the useful base model for a
  shared Resonance Surface;
- Atrium description and help/menu behavior are currently functionally mixed;
- help and dispatch are partly maintained from separate sources;
- no Nexus-wide command framework is required.

The confirmed target contract is `/resonance` -> state-dependent description ->
`resonance>` prompt. `/help` alone reveals currently available actions; `/look`
describes only room and state. COMPOSE may expose `/compose`, ANSWER may expose
`/answer`, and BLOCKED exposes no productive action. `/results` appears only
when an allowed source exists. A room description may hint atmospherically that
a result is present without naming `/results`. Unavailable actions remain
hidden.

`/cancel` exists only inside an active productive cycle, and `/results` is not
visible there. `/compose` is absent in ANSWER and BLOCKED; `/answer` is absent in
COMPOSE and BLOCKED. `/quit` remains the current return command to the Atrium.
After a productive cycle, the existing return-to-Atrium contract remains in
place for now; a later direct return to the same Surface is deferred.

#### 4B.0a — Neutral Resonance Entry

Status: **next implementation candidate; not implemented and not authorized**

First COMPOSE or ANSWER entry no longer starts productive work in the target
contract. `/compose` or `/answer` explicitly starts the existing
`_run_compose()` or `_run_answer()` mechanics. Success, cancellation, and error
continue to return to the Atrium initially, and Slice 4A remains unchanged.

#### 4B.0b — Resonance Description, Help and Capabilities

Status: **not implemented and not authorized**

This planned slice provides one local pre-/post-run Surface. `/look` renders
only room and state; `/help` and the dispatcher derive from the same small
Resonance-local capability source. It introduces neither a general registry nor
a general command framework and preserves the Slice 4A `/results` source.

#### 4B.0c — BLOCKED Resonance Surface

Status: **not implemented and not authorized**

The planned BLOCKED Surface is calm and nonproductive: `/look`, `/help`, safe
recovery information, and `/quit`, with no COMPOSE, ANSWER, Legacy action, Token
search, or automatic repair.

#### 4B.1 — Known-source Handoff

Status: **not implemented and not authorized**

4B.1 is the shared explicit handoff for a deliberately known local source:
`run_nexus.py` -> `run_corrected_nexus()` ->
`ClassifiedResonanceController`. The source is process-local and supplied again
after restart. Source-specific types remain separate. No persistence, registry,
discovery, private-source Activation schema, or private travelling-carrier field
is introduced. The exact stable-result Markdown path remains the preferred
later 5B application of this seam; 4B.1 does not implement that complete revisit.

#### 4B.2 — Known-source Rereading

Status: **not implemented and not authorized**

4B.2 is the shared source-specific read-only safety boundary: explicit known
source, source-specific validation, allowlist-based rendering, and no mutation.
It keeps source types and readers separate, may prepare common calm
missing/unavailable semantics and capability wiring, and performs no discovery,
Opening, matching, generation, regeneration, repair, or mutation. It does not
implement the stable-result-specific Markdown reader, Compact Resonance parsing,
or complete 5B `/results` revisit.

### Slice 4C — Atrium Exploration Surface

Status: **planned; not implemented and not authorized**

4C separates Atrium description from menu behavior. `/look` shows the room,
perceptible paths, and current states; `/help` shows only available navigation
actions. Help and dispatch derive from the same small Atrium-local capability
source. Unknown input remains calm and may briefly point to `/help`; there is no
new `/chambers` command or general menu framework.

One short `/help` hint appears on the first Atrium entry of a process start, not
after every Chamber change. First Spark and Legacy remain outside this initial
migration. 4C follows 4B.2 unless a later implementation inventory proves a
strictly smaller prerequisite.

### Slice 5 — Return, Local Completion, and Result Revisit

Status: **planning only; not implemented and not authorized**

#### 5A — Return Opening

Status: **operative technical infrastructure present; integrated, hardened, and
manually accepted play slice not implemented and not authorized**

The deliberate player action is decided:

```text
copy the Artifact deliberately into incoming/
-> start OPEN_RETURN.sh explicitly
-> use it when exactly one Artifact is present
-> refuse every automatic selection when several are present
```

This is sufficiently deliberate because the person manually brings the Artifact
into the private Return Workspace and explicitly starts Opening afterward. The
launcher performs bounded candidate determination only inside the known
Workspace's `incoming/*.json`; it rejects zero candidates, automatically uses
only one deliberately placed candidate, lists multiple candidates, and refuses
to select among them. No additional prompt is required for exactly one such
candidate. This is not general discovery.

5A must use the existing production Opening infrastructure rather than introduce
a parallel architecture. Existing idempotency and no-overwrite boundaries remain
valuable: an existing result is read unchanged; an opened slot with a missing
result is rejected without regeneration; atomic creation prevents overwrite;
symlinks and unsafe targets are rejected; manual additions remain intact; and a
preserved result can repair a failed slot update later without regeneration.

Prioritized hardening finding: duplicate identical Return Slot identities may be
rejected unambiguously only during the slot update, after the result file has
already been created. This can leave a partial state:

```text
result file exists
-> slot update fails because identity is ambiguous
```

The relevant slot identity must be proven unique before any generation or file
creation. This hardening is not implemented or authorized, must be implemented
and tested separately before or within 5A integration, and must not be mixed with
5B.

#### 5B — Local Result Revisit

Status: **inventory completed; Option C established; not implemented and not
authorized**

The existing public Opening orchestrator is not an admissible reader for
`/results`. Depending on state it can create a result, parse and match Return
Artifact and Return Slot, call the generator, change slot state, or perform
recovery and slot repair. The only existing pure file reader is currently a
private helper inside this mutating Opening path.

Therefore Option C applies: before Slice 5B integration, a narrow separation is
required between reading an existing result and opening a Return. 5B receives
the exact path through the 4B.1 handoff and uses the 4B.2 read-only boundary. Its
own stable-result Markdown reader accepts only a regular non-symlink UTF-8 file,
parses the Compact Resonance sections, and provides the stable-result-specific
allowlist to `/results`. It must never import or call Opening orchestration,
Return Artifact parsing as a prerequisite for revisit, slot matching, generator
logic, slot updates, regeneration, repair, candidate search, or candidate
selection.

The initial explicit rendering allowlist is:

```text
[private local]
stored compact Nachhall

[local path]
exact deliberately known result path
availability of that path
```

The complete Markdown file must never be rendered unfiltered. The technical
trace, `artifact_identity`, `slot_identity`, route/package/slot/origin IDs,
deterministic seed and derivation, Composition Plan, generator internals,
profile/source IDs, slot status, slot notes, generic object representations, and
unclassified manual additions are not player-facing.

Manual notes remain an interesting possible personal extension, but they are not
part of the initial 5B allowlist. Until a separate privacy, format, and player-
experience decision is taken, they are neither detected nor displayed
automatically.

Slice 5B is the stable-result-specific application of the 4B.1 handoff and 4B.2
read-only boundary to the special result already created by 5A. It creates no
second independent persistence or loading architecture, remains read-only, and
never invokes 5A Opening, so 4B and 5B are not identical.

The order is strict:

```text
Return Artifact deliberately opened
-> stable local result already exists
-> /results reads and displays that existing result
```

`/results` never opens a Return Artifact; validates or modifies a Return Slot;
creates Resonance Artifact, Nexus Echo, Nachhall, or a stable result; regenerates,
replaces, or overwrites stored output; searches for Workspaces or result files;
selects candidates; or invokes Opening code directly or indirectly.

### Inventory conclusion and planned sequence

The entry/help and path-handoff inventories are complete, and their decisions
are documented. The cautious next sequence is:

```text
1. 4B.0a — Neutral Resonance Entry
2. 4B.0b — Resonance Description, Help and Capabilities
3. 4B.0c — BLOCKED Resonance Surface
4. 4B.1 — Known-source Handoff
5. 4B.2 — Known-source Rereading
6. 4C — Atrium Exploration Surface
7. harden 5A by rejecting duplicate slot identities before every write
8. integrate the existing Opening as a deliberate play step
9. implement the stable-result-specific 5B reader and /results revisit only
   through the authorized 4B.1 handoff and 4B.2 read-only boundary
10. edit recovery and result language
```

This is planning, not implementation authorization. Slice 4A remains complete
and unchanged. 4B.0a is the next implementation candidate, but it is not
authorized. The remaining 4B subsections, 4C, 5A, and 5B are likewise
unimplemented and unauthorized.

The following questions are deliberately deferred and do not block 4B.0a:
whether `/atrium` later supplements or replaces `/quit` as the canonical return
command; whether a productive cycle later returns directly to the Resonance
Surface; whether the exploration/help principle later extends to Legacy;
whether standalone First Spark `/look` semantics are unified; and when manual
notes receive a separate allowlist-based area.

Older documentation and legacy modules still describe Resonance Artifact and
Nexus Echo as result forms. Current production code and current direction use
the compact Nachhall as the complete stable result. Those legacy terms will be
synchronized in a later documentation cleanup; historical files are unchanged
by this update.

## Deferred accessibility layer

A simpler non-terminal activation and launch experience remains desirable for
future recipients, for example:

- a double-clickable launcher;
- a local activation assistant;
- graphical Token selection or drag-and-drop;
- an optional local graphical Chamber surface.

This is not required for the current gift package because the intended
recipient is comfortable with Linux and terminal workflows.

Status: **deferred beyond the current gift sprint**

## Immediate next step

The decisions are documented. The next implementation candidate is 4B.0a —
Neutral Resonance Entry, but no implementation is authorized yet. Request
separate authorization before any implementation or Git action.

Slices 4B.0a-c, 4B.1-2, 4C, 5A, and 5B are not approved for implementation. This
documentation-only update runs no new tests. Any staging, commit, push,
implementation, or other Git write action requires separate explicit
authorization.

---

## Maintenance rule

Update this document after a slice is manually accepted or when a meaningful
programme addition or deferred observation is discovered.

Keep entries concise and status-oriented.

Do not place private names, local usernames, hostnames, absolute home-directory
paths, private email addresses, or other local machine identifiers in this
tracked document.
