# Nexus 01 - Nexus-Mesomerie

Nexus 01 - Nexus-Mesomerie is the first module line in the **glossai-nexus** project.

Its first stable playable slice is:

**[Nexus 0.1 - First Spark](first_spark/)**

First Spark is a local terminal prototype. It can be played as a neutral public demo or combined with a private activation package to become a personal gift.

## Read the current direction first

The primary source of truth for current Nexus 01 development is:

- [Nexus 01 Current Direction](CURRENT_DIRECTION.md)

The current resonance decision is:

```text
The complete visible resonance result
is one compact Nachhall poem

2 / 4 / 6 / 4 / 1
```

The Nachhall is no longer planned as a secondary Echo derived from a mandatory long-form poem. It is the complete poetic resonance form itself.

For the status of older V0.1, V0.2, milestone, and experiment documents, use:

- [Resonance Documentation Status](RESONANCE_DOCUMENTATION_STATUS_01.md)

For the controlled migration plan, use:

- [Resonance Transition Inventory](RESONANCE_TRANSITION_INVENTORY_01.md)
- [Resonance Dependency Audit](RESONANCE_DEPENDENCY_AUDIT_01.md)
- [Intentional Archive Policy](archive/README.md)

## Core idea

Nexus 01 is intended as a retro-terminal escape module for a single player or a team.

The Nexus itself is the object of play.

Players explore, read, configure, and activate an open software artifact. By learning how this Nexus works, they discover what a Nexus is: a local-first, readable, configurable structure whose connections grow through human interaction and carried traces.

## Intended feeling

Nexus 01 should feel like:

- a small retro terminal game;
- a software escape module;
- a readable open-source artifact;
- a cooperative puzzle space;
- a first encounter with the idea of a Nexus.

It should be playable at the surface and readable in the depth.

## Shared play grammar

The Chambers of Nexus 01 may perform very different functions, but they share
an exploration-based retro-terminal grammar.

Players perceive a space, inspect traces, discover its local vocabulary, request
layered guidance when needed, act, and observe how the Chamber responds.

`help`, `trace`, and spoiler-marked `walkthrough` support this exploration.
They are part of the gameplay, not merely documentation.

See: [Current play grammar](CURRENT_DIRECTION.md#current-play-grammar)

## Current project layers

### 1. First Spark — stable small seed

Status:

```text
current playable and giftable layer
```

Entry points:

- [First Spark README](first_spark/README.md)
- [First Spark 0.1 Review](first_spark/FIRST_SPARK_0_1_REVIEW.md)
- [What Next](first_spark/WHAT_NEXT.md)
- [Packaging README](packaging/README.md)
- [Gift Package Plan](packaging/GIFT_PACKAGE_PLAN.md)

Start from the repository root:

```bash
python3 modules/nexus_01_nexus_mesomerie/first_spark/run_first_spark.py
```

### 2. Human Resonance Chamber — retained

The current direction preserves:

- image choice and answer;
- scent choice and answer;
- movement choice and continuation;
- wish word;
- return word;
- stable public-safe IDs;
- Chamber-owned compatibility.

The people create the resonance. The local poetic layer gives it a small form.

### 3. Return Slots and local memory — retained

The durable technical formula remains:

```text
Slot -> Artifact -> Local Result
```

The current direction preserves:

- local Return Slots;
- route and package identity;
- waiting/opened state;
- local-only matching;
- generate-once and revisit-often;
- no overwrite;
- public/private separation.

Operational references:

- [Return Resonance Local Workspace](RETURN_RESONANCE_LOCAL_WORKSPACE.md)
- [Return Slot from Private Activation](RETURN_SLOT_FROM_PRIVATE_ACTIVATION.md)
- [Return Slot Template](templates/return_slot.template.json)
- [Make Return Slot CLI](make_return_slot.py)

### 4. Compact Nachhall — production result

Status:

```text
production compact generator
generated once and reopened unchanged
```

Production entries:

- `return_resonance/compact_generator.py`
- `return_resonance/open_resonance_return.py`

The V0.3 experiment remains review lineage:

- [Nachhall Composition V0.3](experiments/nachhall_composition_v0_3/README.md)

The production result enforces:

- exact `2 / 4 / 6 / 4 / 1` structure;
- several small micro-routes;
- curated phrase variants;
- controlled metaphorical openness;
- one or more sensory anchors;
- wish word exactly once in line 2, 3, or 4;
- return word exactly once in line 5;
- Same-Word behaviour;
- enough variation without a large grammar engine.

## Older runnable resonance paths

Two older return paths remain in the repository temporarily because they are still connected to tests, commands, and historical fixtures.

### Earlier human-readable Return Resonance MVP

```text
run_return_resonance.py
run_return_resonance_demo.py
return_resonance/artifact.py
return_resonance/result.py
```

This path remains useful for matching and persistence history. Its generated poetry is not the current Nachhall design.

### Persistent compact opening and retained V0.1 renderer

```text
open_resonance_return.py
resonance_language_library/
```

`open_resonance_return.py` is the current persistent opening boundary. It
validates and matches a returned Artifact, creates the compact production
result once, and reuses its exact saved content thereafter. The separate V0.1
language-library renderer remains runnable lineage; it is not invoked by this
production opening path.

Do not infer current architecture from either path without reading the documentation status index.

## Local commands

### Recipient-controlled activation

The corrected activation boundary requires the recipient to choose explicitly:

```bash
python3 modules/nexus_01_nexus_mesomerie/run_nexus.py \
  --recipient-alias recipient_name \
  --activation-purpose gift \
  --private-message "PRIVATE_MESSAGE"
```

A private message supplied directly on a command line may appear in shell
history or process listings. Prefer a non-sensitive placeholder for testing and
use an appropriately private local invocation for real gift text.

Normal activation writes only the existing `first-spark` activation. It never
searches for or reads incidental Token files. Token activation accepts one path
chosen by the recipient, requires a strict Resonance Token V2, and retains a
byte-identical package-relative selected copy plus a small digest-bound context.
Moving the Nexus folder therefore does not break the selected reference.

The activation controller remains separate from Atrium presentation. The
`run_nexus.py` start boundary invokes it only when needed, classifies the
completed state, and opens the Atrium with this runtime interpretation:

```text
first-spark                                      -> COMPOSE
return-resonance + valid selected Token context -> ANSWER
return-resonance + missing/invalid context      -> BLOCKED_ANSWER_RECOVERY
```

After a successful corrected Resonance cycle, returning through `/resonance`
during the same Nexus run opens a quiet post-run Chamber instead of starting
productive work again.
In COMPOSE, `/compose` explicitly begins another independent invitation;
`/quit` returns to the Atrium. In ANSWER, another cycle requires leaving Nexus
01 and deliberately activating or opening it with another Token context.
On either corrected post-run surface, `/results` displays the most recent
successful corrected Resonance cycle retained by that controller in the current
session. It is a session view, not an inventory of Nexus outputs. Earlier local
invitations, private Return Workspaces, Return Artifacts, and later opening or
Nachhall results remain separate and unchanged. Replacing the session view does
not delete, overwrite, invalidate, or hide them. The view does not survive a
process restart, reread output files, or search for moved results. Missing known
output locations are reported without discovery or regeneration. No per-user
result data is added to the reusable neutral Nexus carrier.

In V1.1, First Spark completion and the post-completion Resonance reveal are
session-local Atrium progress. Restarting does not claim that this Chamber
progress was persisted.

Existing pre-activated Resonance packages remain a legacy-compatible path.
Their activation is not silently migrated, and no nearby Token is discovered
to repair missing selected context. Their generated launcher calls the explicit
`run_nexus.py --legacy-preactivated` compatibility path; corrected starts never
reach the legacy one-person Chamber controller.

### First Spark

```bash
python3 modules/nexus_01_nexus_mesomerie/first_spark/run_first_spark.py
```

### Create a local Return Slot

```bash
python3 modules/nexus_01_nexus_mesomerie/make_return_slot.py \
  --origin-trace-id n01-local-origin-a4m9 \
  --return-slot-id quiet-garden-01 \
  --package-id local-package-garden-01 \
  --result-file return_resonance_quiet_garden.local.md \
  --public-safe-label "quiet garden" \
  --output ~/Dokumente/glossai-local/nexus-01-return-workspace/slots/return_slots.local.json
```

### Earlier MVP return demonstration

```bash
python3 modules/nexus_01_nexus_mesomerie/run_return_resonance_demo.py
```

This remains a historical/local infrastructure demonstration, not the
production compact opening path.

## Privacy and packaging

Nexus 01 remains local-first and data-minimal.

The public repository must not contain:

- real `activation.local.json` files;
- private gift messages;
- real return artifacts;
- private local result files;
- key material;
- generated gift packages or ZIP archives.

The current First Spark builders copy only the explicit First Spark package set. They do not package V0.1, V0.2, the archive, or the V0.3 experiment.

The corrected travelling runtime is the **Neutral Nexus Carrier**:

```bash
python3 modules/nexus_01_nexus_mesomerie/packaging/prepare_neutral_nexus_carrier.py \
  --output-dir dist \
  --carrier-label nexus-gift \
  --zip
```

It contains no completed activation. On first start the recipient chooses
normal activation, deliberate Token V2 activation, or cancellation. An optional
Token may be attached at `invitation/resonance_token.v2.json`; it remains an
inert, manually selected invitation and may also travel separately. Private
Return Workspace data never enters the carrier.

The carrier's explicit runtime allowlist includes the production compact
generator and the opening dependencies needed when a new private Return
Workspace is created. The carrier itself still contains no private workspace
instance, Return Slot, Artifact, or generated result.

## Run the complete Nexus 01 test suite

From the repository root, run the canonical standard-library suite:

```bash
python3 modules/nexus_01_nexus_mesomerie/run_all_tests.py
```

It includes `unittest` cases, module-level production test functions, and the
public Return Resonance demo check. Historical experiment tests are excluded.

## Documentation navigation

Use this order:

```text
CURRENT_DIRECTION.md
-> RESONANCE_DOCUMENTATION_STATUS_01.md
-> RESONANCE_TRANSITION_INVENTORY_01.md
-> RESONANCE_DEPENDENCY_AUDIT_01.md
-> active implementation or experiment documentation
-> historical documents only when needed
```

General project documents:

- [Project README](../../README.md)
- [Design Notes](../../DESIGN_NOTES.md)
- [Code of Resonance](../../CODE_OF_RESONANCE.md)
- [Playing a Nexus](../../docs/PLAYING_A_NEXUS.md)
- [Speaking Code](../../docs/SPEAKING_CODE.md)
- [Resonance Arc](../../docs/RESONANCE_ARC.md)
- [Getting Started on Linux](../../docs/GETTING_STARTED_LINUX.md)

## Compact formula

```text
First Spark opens
A human trace returns
The Nexus gives it one small form
The form remains open enough to echo
```
