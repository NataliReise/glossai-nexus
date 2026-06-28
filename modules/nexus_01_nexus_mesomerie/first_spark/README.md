# Nexus 0.1 - First Spark

First Spark is the first small playable slice of **Nexus 01 - Nexus-Mesomerie**.

This directory contains the local terminal prototype.

## Current running unit

The current prototype contains the first complete mini game loop:

> arrival -> spark chamber -> read traces -> link spark -> unlock activation message

This is still intentionally small. It proves that a Nexus module can start locally, move between small game modules, keep state, complete a first activation-message ending, offer optional gentle guidance through the `trace` command, provide a spoiler-protected `walkthrough`, load a local private activation file, explain confusing pasted input on unknown commands, document the local activation workflow, show friendly activation-file errors, provide a safe helper for creating the local activation file, show a first after-play message, and protect the main flow with a minimal automated test.

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

The test checks the current main flow from arrival to ending, including state changes for `trace`, `walkthrough`, `read`, `link spark`, `unlock`, `quit`, unknown-command recovery text, activation-file validation errors, the local activation creation helper, and the after-play message.

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

You can create the local activation file safely from the example:

```bash
python3 modules/nexus_01_nexus_mesomerie/first_spark/create_local_activation.py
```

The helper does not overwrite an existing `activation.local.json` file.

Minimal activation fields:

```json
{
  "recipient_alias": "recipient_name",
  "activation_purpose": "gift",
  "private_message": "This is a public demo placeholder. Real private messages belong to activation.local.json."
}
```

If no local activation file exists, First Spark uses public demo defaults.

If a local activation file exists but cannot be loaded, First Spark shows a friendly error message and points back to `activation.example.json`.

For the full local workflow, see:

- [`LOCAL_ACTIVATION_GUIDE.md`](LOCAL_ACTIVATION_GUIDE.md)

## Current module flow

### Arrival module

The player starts in the arrival module.

Available commands:

- `help` - Show available commands for the current module.
- `look` - Enter the First Spark chamber.
- `trace` - Reveal a gentle next trace.
- `walkthrough` - Show the full solution path with a spoiler warning.
- `quit` - Exit First Spark and return to your terminal.

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
- `quit` - Exit First Spark and return to your terminal.

Visible traces:

- `welcome.log`
- `spark.note`

### Ending module

After `unlock`, the player enters the ending module.

Available commands:

- `help` - Show available commands for the current module.
- `look` - Look at the opened activation message and after-play message.
- `unlock` - Show the already opened activation message and after-play message again.
- `trace` - Confirm that the First Spark is complete.
- `walkthrough` - Show the full solution path with a spoiler warning.
- `quit` - Exit First Spark and return to your terminal.

## Guidance commands

First Spark separates four kinds of orientation:

- `help` shows the available commands for the current module.
- `look` describes the current room or state.
- `trace` gives a gentle next hint without showing a full walkthrough.
- `walkthrough` shows the complete solution path with a spoiler warning.

The walkthrough is intentionally available in all modules so players with little time or little puzzle energy can choose a direct route from anywhere.

## Unknown command recovery

Unknown commands show the text First Spark actually received. This can help explain confusing terminal copy-and-paste situations where pasted input was still waiting in the terminal.

Example:

```text
Unknown command: git statusquit

This may include pasted input that was still waiting in the terminal.
Type 'help' for available commands.
Type 'quit' on a fresh prompt to leave First Spark.
```

## Suggested manual test run

```text
nexus> help
nexus> git statusquit
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

- Unknown commands show a short explanation about possible pasted input.
- `walkthrough` shows a spoiler warning and the complete path.
- `walkthrough` does not change the current module or game state.
- `trace` in the arrival module points toward the entrance.
- `trace` in the spark chamber changes according to the current state.
- `link spark` only succeeds after both visible traces were read.
- `unlock` opens the activation message after the spark was linked.
- The after-play message explains that the gift is complete, passing the spark onward is optional, and public traces must stay public-safe.
- `trace` in the ending module reports that the First Spark is complete.

## Public / private boundary

The public repository contains public code, a public demo fallback, and a safe public activation example.

Real gift messages, real recipient data, real activation codes, return codes, private notes, and personal configuration belong to the private activation layer and must not be committed to the public repository.

See also:

- [`docs/PUBLIC_PRIVATE_BOUNDARY.md`](../../../docs/PUBLIC_PRIVATE_BOUNDARY.md)
- [`LOCAL_ACTIVATION_GUIDE.md`](LOCAL_ACTIVATION_GUIDE.md)
- [`PUBLIC_HANDOFF_CHECKLIST.md`](PUBLIC_HANDOFF_CHECKLIST.md)
- [`GIFT_PACKAGE_SPEC.md`](GIFT_PACKAGE_SPEC.md)
- [`FIRST_SPARK_AFTER_PLAY.md`](FIRST_SPARK_AFTER_PLAY.md)

## Public handoff

Before sharing First Spark publicly, use:

- [`PUBLIC_HANDOFF_CHECKLIST.md`](PUBLIC_HANDOFF_CHECKLIST.md)

Public handoff means sharing a neutral, inspectable version of First Spark without real private activation data.

Private gift handoff is a separate process and should use a separate private activation package.

## Private gift package

A private gift package is a private wrapper around the public First Spark module.

It may carry private activation for a specific recipient, but it must not redefine what belongs to the public module or the public repository.

For the current narrow specification, see:

- [`GIFT_PACKAGE_SPEC.md`](GIFT_PACKAGE_SPEC.md)

## After-play layer

The first after-play layer appears after the unlocked final message.

It makes clear that the gift is complete, passing the spark onward is optional, and any public resonance node must be public-safe.

For the current narrow specification, see:

- [`FIRST_SPARK_AFTER_PLAY.md`](FIRST_SPARK_AFTER_PLAY.md)

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
13. Clearer unknown-command recovery text.
14. Local activation guide.
15. Friendly activation-file validation errors.
16. Safe local activation creation helper.
17. Public handoff checklist.
18. Gift package specification.
19. First Spark after-play specification.
20. After-play message after the final activation message.

Each unit should remain small and runnable before the next one is added.

## Possible next running units

- Add a public-safe resonance node draft template.
- Add optional activation field validation for future fields.
- Prepare resonance artifact and return artifact concepts after the after-play layer works.
