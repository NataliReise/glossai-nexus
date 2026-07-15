# Nexus First Spark Integration Status V0.1

This note records the first complete player-facing integration of the existing First Spark experience into the shared Nexus 01 Atrium.

## Current milestone

Nexus 01 now has a working outer runtime that can:

```text
load one validated activation
-> create the corresponding Atrium state
-> show the paths enabled by that activation
-> enter First Spark through a narrow adapter
-> observe First Spark's own completion signal
-> return to the changed Atrium
```

First Spark remains independently playable through its existing standalone launcher.

The shared Nexus runtime wraps the experience without taking ownership of First Spark's internal grammar.

## Current structure

```text
Nexus 01
├── Nexus Atrium
│   ├── activation bridge
│   ├── activation profiles
│   ├── shared state model
│   ├── runtime wrapper
│   ├── terminal navigation
│   └── First Spark adapter
├── First Spark Chamber
└── Resonance Chamber
```

Conceptually, the current First Spark arrival and ending are now understood as two states of the same Nexus Atrium:

```text
Atrium arrival state
-> First Spark Chamber
-> Atrium return state
```

The existing First Spark modules may remain technically separate while the Nexus interprets them through this larger structure.

## Implemented components

### Atrium state model

`atrium/state.py` represents one Atrium with several phases:

```text
sealed
arrival
return
```

It keeps separate track of:

- enabled Chambers
- completed Chambers
- visible paths
- unfinished paths

This allows the Atrium to represent both current activation profiles:

```text
first-spark
-> First Spark only

return-resonance
-> First Spark + Resonance
```

A Nexus without a validated activation remains present but sealed.

### Activation profiles

`atrium/profiles.py` owns the canonical Nexus 01 activation profiles.

Current rules:

- `first-spark` enables First Spark only
- `return-resonance` enables First Spark and Resonance
- every valid Nexus 01 profile enables First Spark
- `neutral-demo` is not a canonical gameplay profile
- no validated profile produces a sealed Atrium

Legacy First Spark activations without `profile_id` are normalized to `first-spark`.

### Activation bridge

`atrium/activation_bridge.py` translates a validated activation identity into the shared Atrium model:

```text
Activation.profile_id
-> ActivationProfile
-> AtriumState
```

The boundary depends only on a small structural contract exposing `profile_id`.

First Spark therefore does not need to import the Atrium package.

### Atrium runtime

`atrium/runtime.py` owns Nexus-level path availability and completion state.

It delegates each Chamber visit to one small runner:

```text
Chamber runner
-> ChamberRunResult(completed=...)
```

Only an explicit `completed=True` changes Atrium progress.

An interrupted or unfinished visit leaves the Atrium unchanged.

### First Spark adapter

`atrium/first_spark_adapter.py` connects the existing First Spark terminal runtime to the Atrium boundary.

The adapter observes only the First Spark completion signal:

```text
GameState.message_unlocked
```

Translation:

```text
message_unlocked = True
-> ChamberRunResult(completed=True)

message_unlocked = False
-> ChamberRunResult(completed=False)
```

The adapter does not infer completion from:

- the current First Spark module
- `spark_linked`
- the quit flag
- partial local progress

First Spark remains responsible for deciding when First Spark is complete.

### First Spark runtime return value

The existing `first_spark.runtime.run_terminal()` now returns its final `GameState`.

This is a backward-compatible change:

- the standalone terminal experience remains the same
- existing output and command behavior remain the same
- an outer Nexus runtime can now observe the final local state

### Nexus terminal launcher

`run_nexus.py` starts the first player-facing Nexus 01 runtime.

The current Atrium grammar is intentionally small:

```text
look
help
first-spark
quit
```

The initial Atrium view does not expose the full command list directly.

It follows the existing module convention:

```text
Type 'help' for available commands.
```

The command list remains behind `help`, allowing the Atrium to appear first as a place rather than as a menu.

## Working player path

The current executable path is:

```text
run_nexus.py
-> load local activation
-> create NexusAtriumRuntime
-> render Atrium arrival state
-> enter First Spark
-> run existing First Spark terminal
-> receive final GameState
-> translate message_unlocked
-> mark First Spark complete
-> render Atrium return state
```

This is the first complete end-to-end path in which a player can enter an existing Chamber from the Nexus and return to the Nexus afterward.

## Architectural boundary

The integration follows the current modular rule:

```text
Each Chamber keeps its grammar.
The Nexus keeps the route.
The artifact crosses the boundary.
```

For First Spark, the boundary currently carries only completion information:

```text
First Spark owns:
- its commands
- its internal modules
- its local state
- its completion condition

Nexus Atrium owns:
- activation profile interpretation
- path visibility
- Chamber entry permission
- cross-Chamber completion state
- return navigation
```

The Atrium does not dispatch First Spark commands and does not duplicate First Spark mechanics.

## Standalone compatibility

First Spark remains independently playable through its original launcher.

The direct flow test still passes after the integration change.

This preserves two valid entry modes:

```text
standalone First Spark

Nexus 01
-> Atrium
-> First Spark
-> Atrium return
```

The Nexus integration therefore extends the seed without erasing its original form.

## Activation behavior

### `first-spark`

The Atrium exposes only the First Spark path.

After First Spark is completed, the Atrium enters its return phase and marks First Spark as completed.

### `return-resonance`

The Atrium exposes both:

```text
first-spark
resonance
```

After First Spark is completed:

- First Spark is marked completed
- Resonance remains visible and unfinished
- the Atrium enters its return phase

The Resonance path is currently rendered honestly as structurally open but not yet connected to a terminal passage.

## Tested behavior

The current test set covers:

- Atrium state transitions
- canonical activation profiles
- legacy First Spark profile normalization
- activation-to-Atrium translation
- sealed behavior without validated activation
- Chamber entry permission
- completion and non-completion handling
- First Spark adapter translation
- preservation of the standalone First Spark flow
- player-facing Atrium terminal navigation
- return to the changed Atrium after First Spark completion
- continued visibility of unfinished Resonance after First Spark completion
- `help`-based command discovery in the Atrium

The following tests have been run successfully during this integration slice:

```text
Nexus Atrium state tests passed.
Nexus Atrium activation profile tests passed.
First Spark activation profile tests passed.
Nexus activation bridge tests passed.
Nexus Atrium runtime wrapper tests passed.
Nexus First Spark adapter tests passed.
First Spark flow tests passed.
Nexus Atrium terminal launcher tests passed.
```

The player-facing Nexus path has also been exercised manually through the terminal.

## Privacy and dependency boundary

This integration introduces no:

- network behavior
- tracking
- account system
- automatic synchronization
- automatic upload
- social graph
- analytics
- hidden transfer of private activation meaning

The activation continues to provide local configuration.

The Atrium receives only the validated structural identity required to decide which paths exist.

```text
Private meaning may create structure.
Structure must not expose private meaning.
```

## Current limit

The First Spark integration is working, but Nexus 01 is not yet a complete multi-Chamber terminal experience.

The Resonance path is:

- represented in activation profiles
- represented in the Atrium state
- visible in the terminal when enabled
- preserved as unfinished after First Spark completion

It is not yet connected to:

- a Nexus-level Resonance adapter
- token loading at Chamber entry
- the existing Resonance terminal grammar
- artifact preview and explicit local saving
- return from Resonance into the Atrium

This is the next major integration boundary.

## Next recommended slice

The next implementation slice should connect the existing Resonance Chamber without moving its grammar into the Atrium.

Suggested sequence:

```text
Atrium Resonance adapter
-> validate/load the local Resonance Token
-> create TerminalChamberIO
-> run the existing Resonance composer
-> return a ChamberRunResult
-> preserve the composed Return Artifact for explicit local handling
-> return to the Atrium
```

Before writing this adapter, the current Resonance terminal components and their exact test status should be reviewed together.

The adapter should remain narrow:

- the Atrium decides whether the path may be entered
- the Resonance Chamber owns its selections and interaction grammar
- the composer owns the seam to the Return Artifact
- persistence remains explicit and local

## Working formula

```text
First Spark keeps its grammar.
The Atrium keeps the route.
The adapter reports only completion.
```

## Closing note

```text
The Nexus now has an entrance.
First Spark now has a place within it.
The player can leave one room and return to a changed whole.
```
