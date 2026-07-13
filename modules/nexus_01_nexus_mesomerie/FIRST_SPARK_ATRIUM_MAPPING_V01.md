# First Spark to Nexus Atrium Mapping V0.1

This note maps the current First Spark implementation before any structural refactor.

The purpose is to identify the smallest safe path from the existing linear prototype to the intended Nexus 01 structure.

No code is changed by this document.

## Current executable flow

The current runtime follows this route:

```text
run_terminal
-> arrival
-> spark_chamber
-> ending
-> quit
```

The transition is controlled by `GameState.current_module` and the `MODULES` dispatch table in:

```text
first_spark/first_spark/runtime.py
```

Current module names:

```text
arrival
spark_chamber
ending
```

The runtime already treats them as separate stateful regions connected through explicit `next_module` values.

## Current implementation map

```text
first_spark/first_spark/runtime.py
  owns terminal loop and module dispatch

first_spark/first_spark/game_modules/arrival.py
  owns first visible entrance state

first_spark/first_spark/game_modules/spark_chamber.py
  owns the original First Spark puzzle grammar

first_spark/first_spark/game_modules/ending.py
  owns the opened-message and after-play state

first_spark/first_spark/state.py
  owns shared local run state

first_spark/first_spark/activation.py
  owns the current First Spark activation model and demo fallback

first_spark/first_spark/config.py
  loads activation data at import time and exposes runtime constants
```

## Conceptual remapping

The current implementation can be re-read as the intended Nexus 01 structure without immediately merging or renaming code:

```text
Nexus 01

Nexus Atrium
  arrival state
    implemented by game_modules/arrival.py

First Spark Chamber
  implemented by game_modules/spark_chamber.py

Nexus Atrium
  returned / opened state
    currently implemented by game_modules/ending.py
```

This means:

```text
arrival and ending are not two Chambers.
They are two implementations of states belonging to one Atrium.
```

The player-facing spatial model should therefore become:

```text
Atrium, before First Spark
-> First Spark Chamber
-> Atrium, changed by First Spark
```

## Why the mapping is low-risk

The current code already contains the required structural seams.

### Explicit entrance transition

In `arrival.py`:

```text
look
-> next_module = spark_chamber
```

### Explicit return transition

In `spark_chamber.py`:

```text
unlock
-> ending.open_ending
-> next_module = ending
```

### Shared local state

`GameState` already carries:

```text
current_module
read_traces
spark_linked
message_unlocked
should_quit
```

The current `message_unlocked` flag can serve as the first reliable signal that the Atrium has changed after returning from the First Spark Chamber.

## Current First Spark Chamber boundary

The existing `spark_chamber.py` is already a strong candidate for a stable Chamber implementation.

It owns its own mechanical grammar:

```text
look
read <trace-name>
link spark
unlock
trace
walkthrough
```

Its completion condition is explicit:

```text
both required traces read
-> spark linked
-> private message unlocked
```

This file should remain as stable as possible during the first Atrium transition.

## Current Atrium-like entrance behavior

The present `arrival.py` already performs several Atrium functions:

```text
receives the player
shows activation presence
shows recipient alias
announces the locked private message
exposes currently available commands
provides the entrance into First Spark
```

Its current command:

```text
look
```

both inspects and enters the First Spark Chamber.

For a future multi-path Atrium, inspection and entry may eventually need to become separate actions. That change is not required for the first mapping step.

## Current Atrium-like return behavior

The present `ending.py` already performs several return-state functions:

```text
shows the opened private message
marks First Spark as complete
offers after-play orientation
exposes a public-safe resonance-node draft
remains interactive until quit
```

Conceptually, this is already a changed return space rather than a separate puzzle Chamber.

Its player-facing framing should gradually shift from:

```text
ending
```

toward:

```text
Atrium after First Spark
```

The file does not need to be renamed or merged immediately.

## Important activation finding

The current activation loader has three fields:

```text
recipient_alias
activation_purpose
private_message
```

When `activation.local.json` is absent, it silently returns a public demo activation.

Current fallback behavior:

```text
no local activation file
-> default_activation
-> public demo message
-> First Spark remains playable
```

This creates the neutral no-activation play mode discussed during the Nexus 01 redesign.

If Nexus 01 should require a real activation for canonical play, this fallback is the main behavior that must later be reconsidered.

It should not be removed during the first Atrium refactor. It is currently part of the stable test and public development workflow.

A safe later transition could distinguish:

```text
canonical activation
public development fixture
sealed Nexus without activation
```

without treating the development fixture as a canonical player mode.

## Import-time activation constraint

`config.py` loads activation data when imported:

```text
ACTIVATION = load_activation()
```

This means activation selection currently happens before the terminal runtime begins.

A future Nexus-level activation model should take care not to introduce a second conflicting loader beside it.

The first Atrium step should therefore avoid changing activation ownership until the new activation profiles have been specified explicitly.

## Existing tests that protect the current flow

The current flow test verifies:

```text
arrival help and guidance
arrival -> spark_chamber
trace reading
spark linking
message unlocking
spark_chamber -> ending
opened message behavior
resonance-node draft
ending interaction
quit behavior
activation fallback and validation
```

File:

```text
first_spark/tests/test_first_spark_flow.py
```

These tests should remain green throughout the first Atrium transition.

## Minimal first intervention

The safest first code intervention is not to merge `arrival.py` and `ending.py`.

Instead:

```text
1. Preserve runtime dispatch and current module names.
2. Introduce a small Atrium-facing conceptual layer or state description.
3. Treat arrival as Atrium arrival state.
4. Treat ending as Atrium returned state.
5. Keep spark_chamber as the First Spark Chamber implementation.
6. Keep the complete existing First Spark flow test unchanged and green.
```

A first implementation may add Atrium state vocabulary without changing the underlying transitions.

Possible minimal model:

```text
AtriumPhase
  ARRIVAL
  RETURNED_FROM_SPARK
```

This model should describe the Nexus-facing meaning of the current modules, not replace their code immediately.

## What should not happen yet

Do not yet:

```text
rename all First Spark packages
merge arrival.py and ending.py
rewrite spark_chamber.py
replace GameState wholesale
add the Resonance Chamber directly to the old dispatch table
remove the demo fallback before defining its replacement
create a second activation loader
```

## Recommended next slice

The next slice should define a tiny Atrium state contract around the existing implementation.

It should answer:

```text
Which Atrium phase is active?
Which Chambers are available?
Which Chamber has been completed?
Which paths should the player be shown?
```

For the first slice, it can remain independent of terminal presentation and independent of the Resonance Chamber runtime.

Only after that contract is stable should activation profiles be connected to it.

## Working map

```text
Existing arrival module
= Nexus Atrium, arrival state

Existing spark_chamber module
= First Spark Chamber

Existing ending module
= Nexus Atrium, returned and opened state
```

## Working principle

```text
The Atrium is not added before First Spark.
The entrance and return of First Spark become the Atrium of Nexus 01.
```
