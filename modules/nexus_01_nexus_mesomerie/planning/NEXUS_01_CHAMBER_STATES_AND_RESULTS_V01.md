# Nexus 01 Chamber States and Results V0.1

## Document status

- Version: 0.1
- Status: Baseline
- Date: 2026-07-18
- Purpose: Initial Chamber-state and result concept before the repeatable-cycle clarification.

## Status

This document is the canonical working concept for Chamber state, exploration,
guided interaction, completion, revisiting, terminal presentation, and local
result access in Nexus 01.

It defines the intended player experience and architectural boundaries.

It does not define a final implementation, persistence schema, or universal
framework for future Nexus modules.

## Sprint principle

Nexus 01 should implement the smallest coherent experience that already feels
like a complete Nexus.

The current sprint must preserve:

- existing COMPOSE and ANSWER mechanics;
- explicit local creation;
- voluntary manual transfer;
- privacy boundaries;
- Chamber ownership;
- predictable and testable terminal interaction.

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

The following layers have separate responsibilities.

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
- mechanical progress;
- exploration progress;
- completion;
- available results.

Repeated use may reveal changed or deepened perception rather than repeating
exactly the same text.

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
- how to return or leave.

It should be direct, concise, and mechanically accurate.

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

The Resonance Chamber may use a voice because response, relation, and guided
attention belong naturally to its function.

The voice is local, not omniscient. It does not know private meanings that were
not explicitly entered, unrelated files, hidden state from other Chambers, or
anything outside its declared context.

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
- optional manual transfer.

It should remain terse and non-poetic where precision matters.

### `results`

`results` provides access to stable results made available within the current
Nexus module.

It is a viewing function. It must not regenerate, overwrite, transmit, publish,
or mutate a result.

---

## 3. Terminal presentation

Player-facing Chamber output should be visually separated from player input.

Recommended indentation:

```text
0 spaces   headings, input prompts, important system boundaries
2 spaces   room prose, Chamber voice, traces, help entries, choices
4 spaces   result details and local filesystem paths
```

Example:

```text
Resonance Chamber

  The Chamber widens around a dark central pane.

  Several forms pass behind its surface.

  1. A pale reflection
  2. A distant window
  3. A light beneath water

Enter a number:
```

Indentation is a presentation rule and should not be embedded independently in
every authored text.

For the sprint, one small shared formatting helper is sufficient.

Dynamic terminal width detection and advanced automatic wrapping are deferred.

---

## 4. Independent state axes

Nexus 01 must not collapse all state into one general Chamber status.

### 4.1 Atrium path status

The Atrium owns path visibility, entry permission, and cross-Chamber completion.

Relevant states are conceptually:

```text
not enabled
open
recovery access
completed and revisitable
```

For the gift path:

```text
First Spark available
-> First Spark completed
-> Resonance path revealed
```

For a return-resonance activation, the Resonance path may already be visible at
arrival.

The reveal after First Spark is a transition, not a permanent additional
Chamber mode.

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

### 4.3 Mechanical progress

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

Mechanical progress owns:

- valid next input;
- selections already made;
- review;
- confirmation;
- completion conditions.

Information commands must return to the unchanged current step.

### 4.4 Exploration progress

Exploration progress records what the visitor has already perceived or requested
during the current experience.

Possible observations include:

```text
room not yet examined
room examined
trace noticed
trace read or requested
help requested
voice engaged
walkthrough confirmed
```

The first sprint does not require persistent exploration state across process
restarts.

Only the minimum state needed for coherent responses should be implemented.

### 4.5 Result availability

Result availability is independent of Resonance completion:

```text
no available results
one available result
several available results
```

The `results` command may become available as soon as at least one suitable
result exists.

A First Spark result may therefore be visible in the Resonance Chamber before
the Resonance process itself has completed.

---

## 5. Meaning of `completed`

`completed` means that the productive movement of a Chamber has finished.

It does not mean that the Chamber ceases to be experiential.

For the Resonance Chamber:

```text
completed
= no second productive run in the same completed context
+ Chamber remains revisitable
+ completed room state may be observed
+ stable results may be viewed again
```

A revisit must not:

- create another invitation;
- create another private workspace;
- create another Return Artifact;
- overwrite an existing result;
- silently restart COMPOSE or ANSWER.

The completed Chamber may offer:

```text
look
help
trace
results
leave
```

A full completed-state experience may be simplified during the sprint if the
runtime change proves too risky.

---

## 6. The Resonance Chamber as a local result space

The Resonance Chamber may display results from Chambers of the current Nexus
module when those results are deliberately made available.

This is a special local function of the Resonance Chamber.

It is not equivalent to the public Nexus Archive.

The Resonance Chamber may show private local material because the visitor is
inside their own deliberately opened local Nexus.

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
- other deliberately available personal Chamber output.

Private local results must be clearly labelled as local and private.

They are not automatically public-safe.

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

Conceptual boundary:

```text
source Chamber
-> owns complete internal result
-> exposes an allowed local result view

module runtime or narrow adapter
-> carries availability or a typed view

Resonance Chamber
-> displays the view

Atrium
-> knows only navigation, completion, and possibly that results are available
```

The Atrium must not display private message text, wish words, return words, or
private artifact contents.

---

## 8. Persistence and authoritative sources

Stable results should be revisitable across Nexus sessions when their
authoritative local source still exists.

The principle is:

```text
generate once
revisit often
```

The result viewer should prefer existing authoritative sources rather than
creating duplicate shadow copies.

Possible authoritative sources include:

- the validated local activation for the First Spark message;
- the static First Spark Resonance Node definition;
- the selected Token or private workspace for originating Resonance data;
- a Return Artifact for an answering contribution;
- an already persisted local Resonance result;
- remembered exact output paths.

Viewing a result must not:

- regenerate poetic output;
- overwrite files;
- alter completion state;
- mark material as public;
- transmit anything.

When an authoritative source is unavailable, the Chamber should explain calmly
that the known result cannot currently be reopened.

---

## 9. Privacy and publication boundary

Local visibility and public safety are different permissions.

The Resonance Chamber may locally display personal results without making them
public.

The Nexus Archive or a public Resonance Node may receive only material
deliberately defined as public-safe.

```text
private local result
!= public-safe result
!= archive-safe record
```

The system must not silently transform one category into another.

Nothing is sent, uploaded, synchronized, or published automatically.

---

## 10. Minimal command expectations for the sprint

During an active corrected COMPOSE or ANSWER step:

```text
look
help
trace
walkthrough
/cancel
```

`/cancel` appears only where supported by the active interaction.

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

No productive Resonance interaction begins.

During completed revisit:

```text
look
help
trace
results
leave
```

---

## 11. Sprint implementation boundaries

### Required

- atmospheric entry;
- `look`;
- `help`;
- `trace`;
- confirmed guided `walkthrough`;
- unchanged COMPOSE and ANSWER mechanics;
- no state mutation by information commands;
- explicit local creation and manual transfer;
- light, consistent indentation of Chamber output;
- focused and canonical tests.

### Desired when small and safe

- completed Resonance revisit;
- prevention of a second productive run;
- persistent `results`;
- First Spark private message;
- static First Spark Resonance Node;
- Resonance choices and stable local result;
- remembered local output paths.

### Explicitly deferred

- unrestricted natural-language dialogue;
- a universal result registry for all future Chambers;
- persistent exploration state;
- automatic filesystem search;
- complex `inspect` and named trace-object systems;
- full Archive integration;
- cross-module result collections;
- graphical interfaces;
- automatic publication or transfer;
- dynamic terminal width detection;
- advanced automatic text wrapping.

---

## 12. Simplification rules

If a general result registry would require broad architectural change, the gift
release may support only:

```text
First Spark private message
+ static First Spark Resonance Node
+ current Resonance result
+ remembered exact local paths
```

If a dialogue system becomes too large, the Chamber voice is limited to the
confirmed guided walkthrough.

If completed revisit becomes risky, result access may temporarily appear
immediately after completion or through a narrow Atrium command, while the full
revisitable Chamber is deferred.

If shared terminal formatting touches too many outputs or tests, the sprint may
limit indentation to the Resonance Chamber only.

Safety, clarity, and release readiness take priority over abstraction.

---

## Working formulas

> The Atrium opens the path.  
> The entry context gives the Chamber its form.  
> Mechanical progress determines what may happen.  
> Exploration progress determines what has been revealed.  
> Each Chamber owns what it creates.  
> The Resonance Chamber may show what the Chambers deliberately make available.

And:

> The room shows.  
> Traces suggest.  
> Help explains.  
> The voice responds.  
> The walkthrough guides only when invited.  
> The system confirms only what occurred.