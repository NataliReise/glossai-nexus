# Nexus 0.1 - First Spark

First Spark is the first small playable slice of **Nexus 01 - Nexus-Mesomerie**.

This directory contains the local terminal prototype.

## Current running unit

The current prototype contains the first complete mini game loop:

> arrival -> spark chamber -> read traces -> link spark -> unlock activation message

This is still intentionally small. It proves that a Nexus module can start locally, move between small game modules, keep state, complete a first activation-message ending, offer optional gentle guidance through the `trace` command, provide a spoiler-protected `walkthrough`, load a local private activation file, and protect the main flow with a minimal automated test.

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

## Test

From the repository root:

```bash
python3 modules/nexus_01_nexus_mesomerie/first_spark/tests/test_first_spark_flow.py
```

Expected output:

```text
First Spark flow tests passed.
```

The test checks the current main flow from arrival to ending, including state changes for `trace`, `walkthrough`, `read`, `link spark`, `unlock`, and `quit`.

## Activation files

First Spark can load a local private activation file:

```text
modules/nexus_01_nexus_mesomerie/first_spark/activation.local.json
```

This file is ignored by Git and must not be committed.

A safe public example is included:

```text
modules/nexus_01_nexus_mesomerie/first_spark/activation.example.json
```

Minimal activation fields:

```json
{
  "recipient_alias": "recipient_name",
  "activation_purpose": "gift",
  "private_message": "This is a public demo placeholder. Real private messages belong to activation.local.json."
}
```

If no local activation file exists, First Spark uses public demo defaults.

## Current module flow

### Arrival module

The player starts in the arrival module.

Available commands:

- `help` - Show available commands for the current module.
- `look` - Enter the First Spark chamber.
- `trace` - Reveal a gentle next trace.
- `walkthrough` - Show the full solution path with a spoiler warning.
- `quit` - Exit First Spark.

### Spark chamber module

After `look`, the player enters the spark chamber.

Available commands:

- `help` - Show available commands for the current module.
- `look` - Look around the First Spark chamber.
- `read <trace-name>` - Read a visible trace.
- `link spark` - Link the first spark fragments after the required traces were read.
- `unlock` - Open the activation message after the spark was linked.
- `trace` - Reveal a gentle next trace based on the current state.
- `walkthrough` - Show the full solution path with a spoiler warning.
- `quit` - Exit First Spark.

Visible traces:

- `welcome.log`
- `spark.note`

### Ending module

After `unlock`, the player enters the ending module.

Available commands:

- `help` - Show available commands for the current module.
- `look` - Look at the opened activation message.
- `unlock` - Show the already opened activation message again.
- `trace` - Confirm that the First Spark is complete.
- `walkthrough` - Show the full solution path with a spoiler warning.
- `quit` - Exit First Spark.

## Guidance commands

First Spark separates four kinds of orientation:

- `help` shows the available commands for the current module.
- `look` describes the current room or state.
- `trace` gives a gentle next hint without showing a full walkthrough.
- `walkthrough` shows the complete solution path with a spoiler warning.

The walkthrough is intentionally available in all modules so players with little time or little puzzle energy can choose a direct route from anywhere.

## Suggested manual test run

```text
nexus> help
nexus> walkthrough
nexus> trace
nexus> look
nexus> walkthrough
nexus> trace
nexus> read welcome.log
nexus> trace
nexus> read spark.note
nexus> trace
nexus> link spark
nexus> trace
nexus> unlock
nexus> walkthrough
nexus> trace
nexus> quit
```

Expected behavior:

- `walkthrough` shows a spoiler warning and the complete path.
- `walkthrough` does not change the current module or game state.
- `trace` in the arrival module points toward the entrance.
- `trace` in the spark chamber changes according to the current state.
- `link spark` only succeeds after both visible traces were read.
- `unlock` opens the activation message after the spark was linked.
- `trace` in the ending module reports that the First Spark is complete.

## Public / private boundary

The public repository contains public code, a public demo fallback, and a safe public activation example.

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
10. Minimal automated flow test.
11. `walkthrough` command with spoiler warning.
12. Local private activation file structure.

Each unit should remain small and runnable before the next one is added.

## Possible next running units

- Improve activation validation and error messages.
- Add a safer helper script for creating a local activation file from the example.
