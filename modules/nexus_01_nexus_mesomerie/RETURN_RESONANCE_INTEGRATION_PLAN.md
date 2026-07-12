# Return Resonance Integration Plan

This document maps the existing Return Resonance implementation onto the newer Nexus Atrium and Chamber structure for **Nexus 01 - First Spark**.

It is an integration plan, not a replacement specification.

```text
Do not rebuild what already works.
Connect the existing return path to a playable Chamber.
```

## 1. Current milestone

The repository already proves this end-to-end technical path:

```text
explicit safe values
-> generated local return slot
-> matching return artifact
-> local return result
```

Technical short formula:

```text
Slot -> Artifact -> Local Result
```

The missing piece is not the core return logic.

The missing piece is a playable and transferable path around it:

```text
Nexus Atrium
-> Resonance Chamber
-> Return Artifact
-> manual human transfer
-> local Return Result
```

## 2. Existing implementation inventory

### 2.1 Return slot generator

Existing file:

```text
make_return_slot.py
```

Already implemented:

```text
create one local slot document from explicit safe values
validate required values as non-empty
refuse overwrite unless explicitly requested
write local JSON
print a privacy reminder
```

Current boundary:

```text
The generator does not read private activation packages.
The generator does not read First Spark internals.
The generator does not publish anything online.
```

### 2.2 Return slot model and loader

Existing file:

```text
return_resonance/slots.py
```

Already implemented:

```text
ReturnSlot data model
waiting and opened states
JSON loading
required-field validation
friendly load errors
```

### 2.3 Return artifact parser

Existing file:

```text
return_resonance/artifact.py
```

Already implemented:

```text
human-readable structured text format
required header fields
optional poetic input fields
friendly parse errors
```

Current poetic input fields:

```text
carrier_image
carrier_movement
return_word
return_image
return_tone
```

### 2.4 Matching logic

Existing file:

```text
return_resonance/matching.py
```

Already implemented outcomes:

```text
matching waiting slot
matching opened slot
unknown slot
package mismatch
layer mismatch
```

Matching currently uses:

```text
origin_trace_id
return_slot_id
package_id
layer_id
```

### 2.5 Local result generation

Existing file:

```text
return_resonance/result.py
```

Already implemented:

```text
generate one local Markdown result
reuse an existing result instead of regenerating it
include return status and structural metadata
include origin and returned images
include a generated five-line resonance text
include a public-safe witness phrase
include a privacy reminder
```

Working rule:

```text
Generate once.
Revisit often.
```

The current generated five-line form is Elfchen-like, but not yet a strict word-count Elfchen.

### 2.6 Local CLI

Existing file:

```text
run_return_resonance.py
```

Already implemented:

```text
read an artifact file
read a slot file
match the artifact
create or reuse a local result
show friendly status messages
remain local-only
```

### 2.7 Proven integration path

Existing review:

```text
RETURN_SLOT_GENERATOR_INTEGRATION_REVIEW.md
```

Already proven by tests:

```text
the generator creates a consumable slot file
a matching artifact parses successfully
the artifact matches the generated slot
the local result opens
the expected result filename is used
the result contains returned poetic values
```

### 2.8 Local workspace

Existing guide:

```text
RETURN_RESONANCE_LOCAL_WORKSPACE.md
```

Recommended local separation:

```text
slots/
artifacts/
results/
notes/
```

The public repository carries the pattern.

The local workspace carries the meaning.

## 3. Architectural reconciliation

Earlier Return Resonance documents protect this boundary:

```text
Return Resonance may know about First Spark.
First Spark must not depend on Return Resonance.
```

The new Atrium and Chamber model should preserve that rule.

Therefore, the Resonance Chamber should belong to **Nexus 01**, beside the First Spark Chamber, rather than being embedded as a hard dependency inside the First Spark core.

Recommended structure:

```text
Nexus 01 runtime / Atrium layer
├── Nexus Atrium
├── Spark Chamber adapter
│   └── existing First Spark core
└── Resonance Chamber
    └── existing Return Resonance components
```

This means:

```text
First Spark remains independently playable.
The Nexus Atrium may route into First Spark.
The Nexus Atrium may route into Return Resonance.
Return Resonance may reuse First Spark origin context.
First Spark does not import Return Resonance.
```

## 4. Social resonance arc

The first intended human-mediated arc is:

```text
Person A
  prepares a personal activation for Person B
  prepares a local waiting return slot

Person B
  receives and plays the First Spark gift
  may carry Nexus 01 onward with a resonance activation or token

Person C
  receives Nexus 01 plus resonance context
  enters the Resonance Chamber
  creates a Return Artifact through play

Person B or Person A
  receives the Return Artifact manually
  opens it against the waiting local slot
  receives the stable local Return Result
```

The exact return destination may vary by activation.

The software should not infer or manage the relationship.

```text
The slot knows where to wait.
It does not need to know who is waiting.
```

## 5. Activation and package roles

The first implementation should distinguish three related but separate structures.

### 5.1 Gift activation

Makes a First Spark run personal.

Possible responsibilities:

```text
recipient alias
private gift message
activation purpose
available Chambers
```

### 5.2 Return slot

Creates a waiting local place in the origin workspace.

Responsibilities:

```text
safe structural identifiers
waiting/opened state
local result filename
public-safe label
```

It must not contain the private gift meaning.

### 5.3 Resonance activation or token

Travels with the carried module and enables the Resonance Chamber.

Possible minimal fields:

```json
{
  "activation_mode": "resonance",
  "enabled_chambers": ["spark", "resonance"],
  "resonance_token": {
    "origin_trace_id": "...",
    "return_slot_id": "...",
    "package_id": "...",
    "layer_id": "return-resonance-1"
  }
}
```

This is still a design candidate, not a frozen schema.

The token should carry only what the Return Artifact needs in order to find the waiting slot later.

## 6. Nexus Atrium integration

The Nexus Atrium is the primary orientation space.

A gift activation may initially show:

```text
spark.door
```

A resonance activation may show:

```text
spark.door
resonance.door
```

The Atrium may allow either order:

```text
Atrium -> Spark Chamber -> Atrium -> Resonance Chamber -> Atrium
```

or:

```text
Atrium -> Resonance Chamber -> Atrium -> Spark Chamber -> Atrium
```

Direct Chamber-to-Chamber paths may later exist when meaningful, but they are not required for the first integration slice.

The Atrium help should be state-dependent.

```text
The Atrium teaches the current grammar of the Nexus.
```

## 7. Resonance Chamber responsibility

The Resonance Chamber should not reimplement slot loading, artifact parsing, matching, or local result generation.

Its first responsibility is narrower:

```text
turn a resonance activation into a small playable experience
collect or derive the five poetic return values
write a valid Return Artifact
return the player to the Nexus Atrium
```

The Chamber may collect:

```text
carrier_image
carrier_movement
return_word
return_image
return_tone
```

The structural identifiers should come from the resonance token:

```text
origin_trace_id
return_slot_id
package_id
layer_id
```

The player should not have to type those identifiers manually.

## 8. First playable Resonance Chamber MVP

A first small Chamber could use this flow:

```text
look
read token.trace
inspect echoes
choose carrier <value>
choose movement <value>
choose word <value>
choose image <value>
choose tone <value>
weave return
```

This vocabulary is provisional.

The Chamber may use guided choices, discovered words, or a mixture of both.

The mechanism may be hidden at first.

It must remain internally consistent.

```text
Each Chamber speaks its own mechanical language.
The player may have to learn it, but the Chamber must keep its grammar.
```

The first MVP should favor a small reliable mechanism over a large puzzle.

## 9. Return Artifact generation

When the Chamber is complete, it should create a local file such as:

```text
return_artifact.local.txt
```

The file should use the existing parser-compatible format:

```text
NEXUS RETURN ARTIFACT
Version: N01-RA-GEN-1
Module: Nexus 01 - First Spark
Origin Trace: <from token>
Return Slot: <from token>
Package: <from token>
Layer: return-resonance-1

Carrier image:
<from Chamber>

Carrier movement:
<from Chamber>

Return word:
<from Chamber>

Return image:
<from Chamber>

Return tone:
<from Chamber>
```

The Chamber should:

```text
write locally only
never upload or send
avoid overwriting an existing artifact without confirmation
show the exact output path
explain manual sharing
return to the Atrium after creation
```

## 10. Return opening remains a separate local action

The carried Return Artifact should later be opened with the existing local Return Resonance path:

```text
run_return_resonance.py
```

For the first implementation, the Nexus does not need to automate transport.

The artifact may be copied, attached, or carried through a chosen private human channel.

At the origin workspace:

```text
Artifact + waiting Slot -> stable local Return Result
```

The existing result generator then creates the Elfchen-like resonance text.

## 11. What already works versus what is missing

### Already works

```text
slot document generation
slot loading and validation
artifact parsing
slot/artifact matching
waiting/opened distinction
local result creation
existing result reuse
Elfchen-like five-line resonance generation
local CLI
public demo data
integration tests
local workspace guidance
```

### Missing for the playable A-B-C flow

```text
frozen resonance activation/token schema
Nexus Atrium runtime above the existing First Spark core
state-dependent Chamber availability
Resonance Chamber game state
Resonance Chamber commands and help
playful collection of poetic values
parser-compatible Return Artifact writer
safe overwrite behavior for the artifact
Gift Package support for resonance activation
Gift Package recipient instructions for Person C
package verification rules for a resonance gift/carried package
end-to-end manual test from carried activation to returned result
```

## 12. Implementation slices

### Slice 1 - Freeze the minimum carried token

Decide:

```text
filename
schema
required fields
public-safe/local-safe boundary
how it enters a carried package
```

No game changes yet.

### Slice 2 - Add a standalone Return Artifact writer

Create a small reusable writer that accepts:

```text
token identifiers
five poetic values
output path
```

It should generate parser-compatible text and refuse unsafe overwrite by default.

Test it independently.

### Slice 3 - Build the Resonance Chamber as a standalone playable slice

Implement:

```text
local Chamber state
Chamber-specific help
value discovery/selection
weave return
local artifact output
```

Do not require the Atrium yet.

### Slice 4 - Introduce the minimal Nexus Atrium router

The router should:

```text
read available Chambers from activation context
show visible doors
enter Spark Chamber
enter Resonance Chamber
remember Chamber completion for the current run
return to a changed Atrium
```

Preserve the independent First Spark entry point.

### Slice 5 - Add resonance package support

Extend packaging carefully so a carried resonance package can include:

```text
public runtime structure
resonance activation/token
recipient instructions
artifact output location guidance
```

It must not include the origin waiting slot or origin local result.

### Slice 6 - End-to-end manual test

Test the real sequence:

```text
create waiting slot
build carried resonance package
play Resonance Chamber
create Return Artifact
move artifact manually
open artifact against waiting slot
inspect generated local result
run git status --short
```

## 13. Thursday decision gate

By Thursday, decide between these paths.

### Path A - Return Layer ready for the birthday gift

Use it only if:

```text
Resonance Chamber is playable
artifact output is valid
packaging is understandable
verification passes
manual end-to-end test passes
First Spark remains stable
```

### Path B - First Spark gift fallback

Use the already working First Spark gift package if any core Return Layer step remains fragile.

The Return Layer may remain in development without weakening the gift.

### Path C - Bonus work

Only after Path A is stable:

```text
small speaking-code puzzle
one hidden code trace
one optional Chamber link
minor poetic refinements
```

## 14. Non-goals for this week

Do not add:

```text
automatic transfer
automatic email or messenger delivery
accounts
identity verification
social graph logic
network synchronization
real cryptography
multi-user server state
inter-module bridges
large world redesign
```

Inter-module paths remain a future possibility.

## 15. Recommended immediate next step

The next code step should be:

```text
freeze a minimal resonance token schema
and implement a tested Return Artifact writer
```

This is the smallest missing bridge between the already working Return Resonance core and a future playable Resonance Chamber.

## 16. Working formulas

```text
The public repo shows the shape.
The local workspace carries the meaning.
```

```text
Private meaning may create structure.
Structure must not expose private meaning.
```

```text
The generator prepares the waiting place.
The Chamber shapes the return.
The artifact carries it.
The local result remembers it.
```

```text
A Nexus may guide the artifact.
People still carry the relationship.
```
