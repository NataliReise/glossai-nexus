# Nexus 0.1 - First Spark

First Spark is the first small playable slice of **Nexus 01 - Nexus-Mesomerie**.

This directory contains the local terminal prototype.

## Current running unit

The current prototype contains the first complete mini game loop:

> arrival -> spark chamber -> read traces -> link spark -> unlock public demo message

This is still intentionally small. It proves that a Nexus module can start locally, move between small game modules, keep state, complete a first public demo ending, and offer optional gentle guidance through the `trace` command.

Development principle:

> First make the spark run.  
> Then widen the trace.

## Run

From the repository root:

```bash
python3 modules/nexus_01_nexus_mesomerie/first_spark/run_first_spark.py
```

Or from this directory:

```bash
python3 run_first_spark.py
```

## Current module flow

### Arrival module

The player starts in the arrival module.

Available commands:

- `help` - Show available commands for the current module.
- `look` - Enter the First Spark chamber.
- `trace` - Reveal a gentle next trace.
- `quit` - Exit First Spark.

### Spark chamber module

After `look`, the player enters the spark chamber.

Available commands:

- `help` - Show available commands for the current module.
- `look` - Look around the First Spark chamber.
- `read <trace-name>` - Read a visible trace.
- `link spark` - Link the first spark fragments after the required traces were read.
- `unlock` - Open the public demo message after the spark was linked.
- `trace` - Reveal a gentle next trace based on the current state.
- `quit` - Exit First Spark.

Visible traces:

- `welcome.log`
- `spark.note`

### Ending module

After `unlock`, the player enters the ending module.

Available commands:

- `help` - Show available commands for the current module.
- `look` - Look at the opened public demo message.
- `unlock` - Show the already opened public demo message again.
- `trace` - Confirm that the First Spark is complete.
- `quit` - Exit First Spark.

## Guidance commands

First Spark separates three kinds of orientation:

- `help` shows the available commands for the current module.
- `look` describes the current room or state.
- `trace` gives a gentle next hint without showing a full walkthrough.

A future running unit may add a stronger spoiler-style command such as `walkthrough` or `spoiler` for players who have little time or little puzzle energy. That command should include a warning before revealing the full solution path.

## Suggested test run

```text
nexus> help
nexus> trace
nexus> look
nexus> trace
nexus> read welcome.log
nexus> trace
nexus> read spark.note
nexus> trace
nexus> link spark
nexus> trace
nexus> unlock
nexus> trace
nexus> quit
```

Expected behavior:

- `trace` in the arrival module points toward the entrance.
- `trace` in the spark chamber changes according to the current state.
- `link spark` only succeeds after both visible traces were read.
- `unlock` opens the public demo message after the spark was linked.
- `trace` in the ending module reports that the First Spark is complete.

## Public / private boundary

The public repository contains only a public demo message.

Real gift messages, real recipient data, real activation codes, return codes, private notes, and personal configuration belong to the private activation layer and must not be committed to the public repository.

See also:

- [`docs/PUBLIC_PRIVATE_BOUNDARY.md`](../../../docs/PUBLIC_PRIVATE_BOUNDARY.md)

## Completed running units

1. Start script with boot sequence.
2. `help` command.
3. `look` command.
4. `read` command for virtual traces.
5. Modular runtime with autonomous game modules.
6. `link spark` command with shared game state.
7. `unlock` command with public demo message.
8. Dedicated ending module.
9. `trace` command for gentle state-based guidance.

Each unit should remain small and runnable before the next one is added.

## Possible next running units

- Add a spoiler-style command with a warning and a full walkthrough.
- Add a small private activation file format for local-only use.
- Add a safe example activation file that contains only demo placeholders.
- Add minimal automated checks for the current command flow.
