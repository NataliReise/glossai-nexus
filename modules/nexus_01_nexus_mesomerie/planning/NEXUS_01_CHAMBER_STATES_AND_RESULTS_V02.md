# Nexus 01 Chamber States and Results V0.2

## Document status

- Version: 0.2
- Status: Current
- Date: 2026-07-18
- Supersedes: Version 0.1
- Purpose: Canonical Chamber-state and result concept after the repeatable Resonance-cycle clarification and the Slice 1 technical inventory.

## Sprint principle

Nexus 01 should implement the smallest coherent experience that already feels
like a complete Nexus.

The current sprint must preserve:

- existing COMPOSE and ANSWER mechanics;
- explicit local creation;
- voluntary manual transfer;
- privacy boundaries;
- Chamber ownership;
- predictable and testable terminal interaction;
- the ability to create multiple independent Resonance cycles.

New concepts must not silently widen the implementation scope.

---

## 1. Shared Nexus 01 play grammar

Nexus 01 Chambers may perform very different functions.

They belong to the same module line through an exploration-based play grammar:

```text
perceive the space
-> explore its present state
-> discover traces and local vocabulary
-> request help or guidance when desired
-> act
-> observe how the Chamber changes
```

A Chamber should normally be experienced as a place before it is understood as
a menu.

---

## 2. Player-facing text layers

### Atmospheric room text

Atmospheric text presents:

- space;
- mood;
- perceptible objects;
- visible traces;
- changes caused by progress.

It may be poetic and relatively extensive.

It should not explain the entire mechanism in advance.

### `look`

`look` describes the Chamber in its current state.

Its response may depend on:

- entry form;
- current cycle;
- mechanical progress;
- exploration progress;
- prior successful cycles;
- available results.

### Traces and `trace`

Environmental traces belong to the world of the Chamber.

The `trace` command provides one gentle, state-aware orientation toward a useful
next step.

A trace should guide attention without selecting an answer or solving the
Chamber automatically.

### `help`

`help` explains only the current local grammar:

- commands presently available;
- expected input type;
- cancellation support;
- how to return or leave;
- how to begin another cycle when that action is available.

It must not advertise `/cancel` where the active prompt does not support it.

### Optional Chamber voice

A Chamber may possess a local voice.

The voice may:

- respond to the visitor;
- explain the present situation;
- clarify local boundaries;
- offer reassurance;
- provide state-aware guidance;
- lead a confirmed walkthrough.

A voice is optional and is not required in every Nexus Chamber.

The Resonance Chamber may use a voice because response, relation, repetition,
and guided attention belong naturally to its function.

The voice is local, not omniscient.

### `walkthrough`

A walkthrough requires an explicit spoiler warning and confirmation.

In the Resonance Chamber, the walkthrough may be delivered as guided dialogue:

- the Chamber voice reveals one remaining step at a time;
- the visitor still makes every choice;
- no step is skipped;
- no answer is selected automatically;
- the normal mechanics remain unchanged;
- guidance may be left again.

### System text

System text confirms only what technically occurred.

It should clearly distinguish:

- shaped but not yet created;
- created locally;
- cancelled;
- failed safely;
- unchanged existing material;
- optional manual transfer;
- a completed cycle;
- an explicitly requested new cycle.

### `results`

`results` provides access to stable results made available within the current
Nexus module.

It is a viewing function. It must not regenerate, overwrite, transmit, publish,
or mutate a result.

---

## 3. Terminal presentation

Player-facing Chamber output should be visually separated from player input.

```text
0 spaces   headings, input prompts, important system boundaries
2 spaces   room prose, Chamber voice, traces, help entries, choices
4 spaces   result details and local filesystem paths
```

Indentation is a presentation rule and should not be embedded independently in
every authored text.

For the sprint, one small Resonance-local formatting helper is sufficient.

Dynamic terminal width detection and advanced automatic wrapping are deferred.

After an information command, the full unchanged current prompt context should
be rendered again:

- stage heading;
- current choices or word guidance;
- input prompt.

---

## 4. Independent state axes

Nexus 01 must not collapse all state into one general Chamber status.

### 4.1 Atrium path and milestone status

The Atrium owns path visibility, entry permission, and cross-Chamber milestones.

Relevant states are conceptually:

```text
not enabled
open
recovery access
at least one successful cycle completed
```

For the gift path:

```text
First Spark available
-> First Spark completed
-> Resonance path revealed
```

A successful Resonance cycle may mark a milestone, but it does not exhaust or
close the Resonance Chamber.

### 4.2 Resonance entry form

When entry is permitted, the activation context determines the form taken by
the Resonance Chamber:

```text
COMPOSE
ANSWER
BLOCKED_ANSWER_RECOVERY
```

`LEGACY_CONTROLLER` is an older technical entry route, not a fourth canonical
ResonanceMode.

### 4.3 Resonance cycle state

Each productive Chamber run is an independent Resonance cycle:

```text
not started
active
cancelled
failed safely
completed
```

The completed unit is the cycle, not the Chamber.

A completed cycle must not restart automatically.

The Resonance Chamber may remain repeatable. A visitor may explicitly begin
another independent cycle where the current entry context permits it.

### 4.4 Mechanical progress

COMPOSE currently follows:

```text
image
-> scent
-> movement
-> wish word
-> review
-> confirmation
-> local invitation and private workspace creation
```

Each successful COMPOSE cycle creates its own:

```text
Resonance Token
travelling invitation
private Return Workspace
matching Return Slot
```

Different COMPOSE cycles are independent and may coexist.

ANSWER currently follows:

```text
image response
-> scent response
-> movement response
-> return word
-> review
-> confirmation
-> local Return Artifact creation
```

An ANSWER cycle belongs to the deliberately selected carried Resonance Token.

Another ANSWER cycle requires another deliberately selected or activated Token
context.

The sprint retains one stable matching return per individual Return Slot:

```text
one selected Token / matching Slot
-> one Return Artifact
-> one stable local result
-> revisit unchanged
```

Multiple Return Artifacts for different Tokens and Slots remain expected.

Multiple Return Artifacts for the same Slot are deferred.

Information commands must return to the unchanged current step.

### 4.5 Exploration progress

Exploration progress records what the visitor has perceived or requested during
the current Chamber visit.

A minimal transient session may hold:

```text
entry form
room looked at
most recent help step
most recent trace step
walkthrough active
last guided step shown
```

The mechanical step is already supplied by the existing flow and must not be
duplicated as a second progress counter.

### 4.6 Result availability

Result availability is independent of the current cycle:

```text
no available results
one available result
several results from independent cycles
```

A First Spark result may be visible before the first Resonance cycle completes.

---

## 5. Meaning of `completed`

`completed` must be interpreted at the correct level.

### Atrium milestone

At the Atrium level, completion may mean:

```text
at least one successful Chamber cycle has occurred
```

This may support status display or later navigation, but it must not silently
make the Chamber nonproductive forever.

### Cycle completion

At the Chamber level:

```text
completed cycle
= this productive movement has finished
+ its results may remain viewable
+ it must not restart automatically
+ the Chamber may offer another explicit independent cycle
```

After a successful COMPOSE cycle, a post-run state may offer conceptually:

```text
look
help
trace
results
compose another
leave
```

The exact command spelling may be chosen during implementation.

After an ANSWER cycle, another productive answer must not begin silently for the
same selected Token. Another answer requires another deliberate Token context.

---

## 6. The Resonance Chamber as a local result space

The Resonance Chamber may display results from Chambers of the current Nexus
module when those results are deliberately made available.

It may also display several independent results created by repeated Resonance
cycles.

This is a special local function of the Resonance Chamber.

It is not equivalent to the public Nexus Archive.

### Result classes

#### Private local result

Examples:

- the opened First Spark activation message;
- carried originating resonance;
- selected image, scent, and movement;
- wish word;
- selected responses;
- return word;
- completed poetic Resonance result;
- results from multiple independent cycles.

Private local results must be clearly labelled as local and private.

#### Public-safe static result

Examples:

- the static First Spark Resonance Node text;
- neutral completion information;
- a public-safe trace deliberately authored for possible manual sharing.

The displayed Resonance Node must not absorb later personal additions such as a
manually entered public alias or public note.

#### Local path reference

Examples:

- travelling invitation location;
- private Return Workspace location;
- Return Artifact location;
- stable local result location.

A path reference may report whether its exact known location still exists.

The Nexus must not search the wider filesystem for moved or related files.

---

## 7. Result ownership

Each Chamber owns its complete internal journey and the results it creates.

A Chamber may deliberately expose a local result view.

The Resonance Chamber may render that view, but it must not infer it by
inspecting arbitrary internal state.

```text
source Chamber or completed Resonance cycle
-> owns complete internal result
-> exposes an allowed local result view

module runtime or narrow adapter
-> carries availability or a typed view

Resonance Chamber
-> displays one or more views

Atrium
-> knows only navigation, milestones, and possibly result availability
```

The Atrium must not display private message text, wish words, return words,
Artifact contents, or private paths.

---

## 8. Persistence and authoritative sources

Stable results should be revisitable across Nexus sessions when their
authoritative local source and exact access path still exist.

```text
generate once
revisit often
```

The result viewer should prefer existing authoritative sources rather than
creating duplicate shadow copies.

### Already suitable across restarts

- the validated local First Spark activation message;
- the static First Spark Resonance Node definition;
- the selected carried Resonance Token path published by recipient activation;
- an explicitly known existing result path.

### Initially suitable in the current process

- current COMPOSE choices;
- current ANSWER choices;
- newly created invitation path;
- newly created private workspace path;
- newly created Return Artifact destination.

The current controllers do not durably index all generated destination paths.

A general result registry is therefore not required for the gift sprint.

Viewing a result must not:

- regenerate poetic output;
- overwrite files;
- alter slot state;
- alter completion state;
- mark material as public;
- transmit anything.

`open_resonance_return_files()` must not be used as a general view-only results
command because it may create output or update slot state.

---

## 9. Privacy and publication boundary

Local visibility and public safety are different permissions.

```text
private local result
!= public-safe result
!= archive-safe record
```

The Resonance Chamber may locally display personal results without making them
public.

The Nexus Archive or a public Resonance Node may receive only material
deliberately defined as public-safe.

Nothing is sent, uploaded, synchronized, or published automatically.

---

## 10. Minimal command expectations for the sprint

During an active COMPOSE or ANSWER step:

```text
look
help
trace
walkthrough
/cancel
```

`/cancel` appears only where supported.

Where results already exist, `results` may be available without changing the
current step.

During BLOCKED_ANSWER_RECOVERY:

```text
look
help
trace or recovery guidance
results, when available
leave or return
```

A static one-shot recovery explanation remains an acceptable first-sprint
simplification.

During a COMPOSE post-run state:

```text
look
help
trace
results
explicitly begin another independent cycle
leave
```

During an ANSWER post-run state:

```text
look
help
trace
results
leave
```

Another ANSWER cycle requires another deliberately selected Token context.

---

## 11. Current implementation findings

The Slice 1 technical inventory established:

- `TerminalChamberIO.choose()` and `TerminalChamberIO.enter_word()` are the
  smallest shared seams for information-command interception.
- An optional callback or tiny dispatcher is sufficient.
- COMPOSE and ANSWER already supply explicit step names.
- Information commands can render output and continue the existing input loop.
- The full current prompt should be rendered again after an information command.
- The compose and answer mechanics do not need modification.
- The smallest first implementation slice is `look`, `help`, `trace`, and
  Resonance-only indentation.
- Guided walkthrough, post-run, and results should build on the proven seam.
- BLOCKED recovery does not currently use the shared prompt adapter and may
  remain one-shot initially.
- Legacy cancellation differs and must not receive false `/cancel` guidance.

---

## 12. Sprint implementation boundaries

### Required

- atmospheric entry;
- `look`;
- `help`;
- `trace`;
- confirmed guided `walkthrough`;
- unchanged COMPOSE and ANSWER mechanics;
- no state mutation by information commands;
- explicit local creation and manual transfer;
- light, consistent indentation of Resonance output;
- no automatic new cycle after success;
- explicit support for another independent COMPOSE cycle;
- focused and canonical tests.

### Desired when small and safe

- post-run Chamber state;
- persistent `results` from already authoritative sources;
- First Spark private message;
- static First Spark Resonance Node;
- Resonance choices and stable local result;
- remembered local output paths;
- clear separation of several independent cycle results.

### Explicitly deferred

- unrestricted natural-language dialogue;
- a universal result registry for all future Chambers;
- multiple Return Artifacts for the same Return Slot;
- automatic filesystem search;
- persistent exploration state;
- complex `inspect` and named trace-object systems;
- full Archive integration;
- cross-module result collections;
- graphical interfaces;
- automatic publication or transfer;
- dynamic terminal width detection;
- advanced automatic text wrapping.

---

## 13. Simplification rules

If a dialogue system becomes too large, the Chamber voice is limited to one
confirmed, non-prescriptive current-step hint.

If post-run routing becomes risky, the Chamber may initially expose only:

```text
results
compose another
leave
```

after a successful COMPOSE cycle.

If a general result registry would be required, the gift release supports only:

```text
First Spark private message
+ static First Spark Resonance Node
+ current-process Resonance summary
+ remembered exact local paths
```

If shared terminal formatting touches too many outputs or tests, indentation is
limited to the Resonance Chamber only.

Safety, clarity, and release readiness take priority over abstraction.

---

## Working formulas

> The Atrium opens the path.  
> The entry context gives the Chamber its form.  
> A Resonance cycle determines one productive movement.  
> Mechanical progress determines what may happen within that cycle.  
> Exploration progress determines what has been revealed.  
> Each Chamber owns what it creates.  
> The Resonance Chamber may show what the Chambers and completed cycles deliberately make available.

And:

> A completed run must not restart automatically.  
> The Resonance Chamber may remain repeatable.  
> Each new cycle opens an independent path.

And:

> The room shows.  
> Traces suggest.  
> Help explains.  
> The voice responds.  
> The walkthrough guides only when invited.  
> The system confirms only what occurred.
