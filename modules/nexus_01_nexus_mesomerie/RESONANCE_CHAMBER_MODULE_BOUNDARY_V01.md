# Resonance Chamber Module Boundary V0.1

Status date: 2026-07-14

## Purpose

This note defines the internal boundary of the Resonance Chamber before its first playable composer is implemented.

The Resonance Chamber is an inner mechanical module of Nexus 01. It is not a screen, a helper function, or a collection of prompts attached directly to the Atrium.

It has its own local grammar, state, interaction flow, validation rules, and result type.

Its connection to the rest of the Nexus must remain narrow and explicit.

## Structural position

```text
Nexus 01
|- Nexus Atrium
|- Chambers
|  |- Spark Chamber
|  `- Resonance Chamber
|- Layers
|- Paths
|- shared transport contracts
`- local state
```

The Atrium determines whether the Resonance Chamber is currently available.

The Return Resonance Layer provides the route and activation context.

The Resonance Chamber determines how a player creates a response.

The shared Return Artifact contract transports the finished response.

The local opening system renders the response only after matching it to its intended Return Slot.

## Core rule

```text
A Chamber is an independent mechanical module
with a narrow, typed connection to the Nexus around it.
```

The Nexus may know:

```text
whether the Chamber is enabled
whether the Chamber has started
whether the Chamber has completed
what typed result the Chamber returned
```

The Nexus should not know:

```text
how the Chamber ordered its prompts
how the Chamber revealed its local vocabulary
how many internal steps the Chamber used
how compatibility between local choices was taught
how help, traces, or walkthroughs were expressed
```

## Chamber-owned responsibilities

The Resonance Chamber owns:

```text
local interaction states
choice presentation
choice compatibility
prompt wording
help wording
trace wording
walkthrough wording
progression between steps
preview of the selected response
confirmation before completion
creation of ChamberSelections
```

The Chamber may read approved display material from the versioned Resonance Language Library.

It must not rewrite, infer, or freely generate language outside the approved forms.

## Nexus-owned responsibilities

The surrounding Nexus owns:

```text
activation and availability
Resonance Token loading and validation
module, layer, package, trace, and slot identity
entry from and return to the Atrium
artifact transport contract
local persistence
Return Slot matching
local opening
privacy boundaries
```

The Atrium may announce that a Resonance path has become available.

It must not reproduce the Chamber's internal mechanics.

Working rule:

```text
The Atrium teaches that a Chamber may be entered.
The Chamber teaches how that Chamber can be played.
```

## Shared dependencies

The Resonance Chamber may depend on:

```text
resonance_language_library
  approved selectable content and display forms

return_resonance.resonance_render_bridge.ChamberSelections
  typed result contract for the completed Chamber
```

The Chamber should not depend directly on:

```text
Return Slot files
slot matching
local result writing
Nexus Echo rendering
Resonance Artifact rendering
opened-slot persistence
public repository packaging
First Spark internals
```

Those operations happen after the Chamber has completed.

## Input boundary

The first playable Resonance Chamber receives a small validated context.

Suggested typed input:

```text
ResonanceChamberContext
  language_library
  public_safe_label
  optional local note
```

The Resonance Token itself should remain outside the Chamber's mechanical core.

A thin application layer may load the token, verify that it enables the Chamber, and then start the Chamber with the approved context.

This avoids allowing route identity to leak into the Chamber's local puzzle logic.

## Output boundary

The completed Chamber returns exactly one typed result:

```text
ChamberSelections
  image_id
  image_response_id
  scent_id
  scent_response_id
  movement_id
  movement_response_id
  wish_word
  return_word
```

The Chamber does not write the final Resonance Return Artifact itself.

A thin application layer joins:

```text
validated Resonance Token
+ ChamberSelections
-> Resonance Return Artifact
```

This preserves the separation:

```text
The token carries the route.
The Chamber creates the response.
The artifact joins them.
```

## Proposed package structure

```text
chambers/
`- resonance/
   |- __init__.py
   |- README.md
   |- context.py
   |- choices.py
   |- state.py
   |- flow.py
   |- composer.py
   |- prompts.py
   `- tests/
      |- test_choices.py
      |- test_flow.py
      `- test_composer.py
```

The first implementation does not need every file immediately.

A minimal first slice may begin with:

```text
chambers/resonance/
|- __init__.py
|- README.md
|- choices.py
|- flow.py
`- tests/
   `- test_flow.py
```

The structure should grow only when a responsibility becomes real.

## File responsibilities

### `context.py`

Contains only the small validated input context needed to start the Chamber.

It must not contain transport, slot, or persistence logic.

### `choices.py`

Loads and exposes approved selectable options from the language library.

It provides player-facing labels separately from stable internal IDs.

It validates compatibility between source and response selections.

### `state.py`

Defines explicit Chamber states and progress data.

Suggested V0.1 state sequence:

```text
ENTERED
IMAGE_SELECTED
IMAGE_RESPONSE_SELECTED
SCENT_SELECTED
SCENT_RESPONSE_SELECTED
MOVEMENT_SELECTED
MOVEMENT_RESPONSE_SELECTED
WORDS_SELECTED
PREVIEW
COMPLETED
```

The exact names may change after the first interaction design review.

### `flow.py`

Owns legal transitions between Chamber states.

It should be deterministic and independent of terminal input/output.

It must be possible to test the complete flow without simulating a human terminal session.

### `prompts.py`

Contains Chamber-specific player-facing wording.

Prompt text belongs here rather than in the CLI or transport bridge.

### `composer.py`

Coordinates the Chamber's domain logic and produces `ChamberSelections` after explicit confirmation.

It should accept an input/output adapter rather than assuming a terminal forever.

This allows a later graphical or web-based surface to reuse the same Chamber mechanics.

## Thin application command

A future top-level command may be named:

```text
create_resonance_return.py
```

Its responsibility should remain small:

```text
load and validate Resonance Token
-> create Chamber context
-> run Resonance Chamber composer
-> receive ChamberSelections
-> build Resonance Return Artifact
-> preview transport artifact
-> write only after explicit confirmation
```

The command must not contain the Chamber's choice rules or prompt sequence.

## Interaction adapter

The Chamber composer should not directly call `input()` and `print()` throughout its domain logic.

A small adapter boundary is preferred:

```text
ChamberIO
  show(text)
  choose(prompt, options)
  ask_word(prompt)
  confirm(prompt)
```

The first implementation may provide:

```text
TerminalChamberIO
ScriptedChamberIO
```

`TerminalChamberIO` supports actual play.

`ScriptedChamberIO` supports deterministic tests and the full roundtrip demo.

This is the smallest useful abstraction that protects the Chamber from becoming terminal-specific.

## Language-library boundary

The Resonance Language Library remains a separate versioned component.

The Chamber may request:

```text
available image choices
compatible image responses
available scent choices
compatible scent responses
available movement choices
compatible movement responses
approved display labels
```

The Chamber may not request rendered final poems during play.

Final rendering remains downstream of artifact transport and Return Slot matching.

This distinction matters:

```text
The Chamber offers material.
The player composes a response.
The local opening reveals what returned.
```

## Help boundary

The Chamber owns three support levels:

```text
help
  explains the current local vocabulary and available action types

trace
  offers a gentle orientation toward a useful next step

walkthrough
  reveals the complete remaining path after a spoiler warning
```

The Atrium may announce that help is available inside the Chamber.

The Atrium should not contain the Chamber's help text.

## Privacy boundary

The Chamber works only with public-safe selections and one-word player contributions.

It must not ask the player to explain private meaning.

It must not store reasons, interpretations, personal relationships, or recipient identity.

Working rule:

```text
Private meaning may guide a choice.
The Chamber records only the chosen trace.
```

## Completion boundary

The Chamber reaches `COMPLETED` only after:

```text
all required selections exist
all compatibility rules pass
wish_word is one word
return_word is one word
a preview has been shown
the player has explicitly confirmed completion
```

Before confirmation, the player may revise selections.

After completion, the Chamber returns an immutable `ChamberSelections` value.

The Chamber itself does not send, upload, or open anything.

## Failure behavior

The Chamber must fail clearly rather than improvise.

It should reject:

```text
unknown library version
missing choice data
unknown IDs
incompatible response IDs
empty words
multi-word entries where one word is required
illegal state transitions
completion without confirmation
```

It should never silently replace a choice with a nearby one.

## Independence tests

The Chamber module should be testable without:

```text
real Return Slot files
real artifact files
a writable user workspace
an Atrium implementation
First Spark
network access
AI access
```

The core flow test should prove:

```text
approved choice source
-> deterministic state transitions
-> compatible selections
-> explicit preview
-> explicit confirmation
-> exact ChamberSelections
```

A separate application-level roundtrip test may then prove:

```text
Resonance Token
-> Resonance Chamber
-> ChamberSelections
-> Resonance Return Artifact
-> Return Slot match
-> local opening
```

## V0.1 non-goals

The first playable Chamber does not require:

```text
graphical interface
free spatial navigation
sound or animation
procedural language generation
AI interpretation
multiple simultaneous players
network transport
accounts
analytics
relationship tracking
automatic delivery
```

The first goal is a coherent local mechanic with a clean module boundary.

## First implementation slice

Create the minimal package shell and one deterministic flow model before building the terminal composer.

Recommended order:

```text
1. create chambers/resonance package
2. define choice and state data types
3. load approved options through a narrow library adapter
4. implement legal deterministic transitions
5. test the flow with scripted selections
6. add TerminalChamberIO
7. add the thin create_resonance_return.py command
8. test the full playable roundtrip
```

## Working formula

```text
Each Chamber keeps its grammar.
The Nexus keeps the route.
The artifact crosses the boundary.
```
