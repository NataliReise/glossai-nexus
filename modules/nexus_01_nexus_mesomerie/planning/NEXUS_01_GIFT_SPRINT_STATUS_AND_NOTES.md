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
- Index:
  empty
- Current implementation work:
  uncommitted

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

The current information-command seam is ready to host later Chamber commands,
but these are not yet implemented:

```text
/results
```

Status: **deferred to its planned slice**

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

- local result viewing;
- COMPOSE post-run state;
- ANSWER post-run state;
- explicitly starting another independent COMPOSE cycle;
- selecting another Token for another ANSWER cycle;
- Legacy exploration;
- expanded blocked-recovery dialogue;
- persistent exploration state;
- a general result registry;
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
Slice 4       same-process results
Later         persistent existing sources, language editing, release freeze
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

### Deferred to Slice 4

```text
/results
```

Same-process result presentation, result selection, result registries, and
output-path indexing remain outside Slice 3.

### Persistence boundary

The Slice 3 gate is process-local only.

Preventing duplicate ANSWER cycles across process restarts would require a new
persistent answered/consumed marker or a broader activation lifecycle. That is
not part of the current gift sprint.

Status: **implemented and accepted**

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

Perform a read-only Slice 4 inventory for `/results` and same-process result
presentation.

The inventory must establish:

- which corrected COMPOSE and ANSWER values and output paths are currently lost
  when the productive controller call returns;
- the smallest typed result record needed for same-process viewing;
- whether one last result or multiple same-process results are required by the
  current gift sprint;
- how `/results` should appear on the completed COMPOSE and ANSWER post-run
  surfaces;
- how private-local values, public-safe values, and local paths must be labelled;
- how missing or removed output files should be reported;
- which persistence ideas remain explicitly deferred;
- the smallest production and test scope.

No code, tests, documentation, planning, or status file should be changed during
the inventory.

---

## Maintenance rule

Update this document after a slice is manually accepted or when a meaningful
programme addition or deferred observation is discovered.

Keep entries concise and status-oriented.

Do not place private names, local usernames, hostnames, absolute home-directory
paths, private email addresses, or other local machine identifiers in this
tracked document.
