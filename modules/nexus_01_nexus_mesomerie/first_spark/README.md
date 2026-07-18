# Nexus 0.1 - First Spark

First Spark is the first small playable slice of **Nexus 01 - Nexus-Mesomerie**.

It is a local terminal prototype in the **glossai-nexus** project.

First Spark can be played as a neutral public demo or combined with a private activation package to become a personal gift.

## Start options

There are two intended ways to run First Spark.

### 1. From the cloned repository

Use this path if you want to inspect the project, follow development, modify files, or run the current public seed directly from Git.

This path currently assumes:

- a Linux terminal,
- Git,
- Python 3,
- a local clone of this repository.

Clone the repository and enter the project folder:

```bash
git clone https://github.com/NataliReise/glossai-nexus.git
cd glossai-nexus
```

From the repository root, run:

```bash
python3 modules/nexus_01_nexus_mesomerie/first_spark/run_first_spark.py
```

If you are new to Git, Python, or terminal-based projects, see:

- [`docs/GETTING_STARTED_LINUX.md`](../../../docs/GETTING_STARTED_LINUX.md)

### 2. From a standalone First Spark package

Use this path if you received First Spark as a separate local folder.

This may be:

- a neutral public demo package,
- or a personalized private gift package.

Open a terminal in the First Spark folder and run:

```bash
python3 run_first_spark.py
```

A personalized package may include private activation data.

Do not post or commit private activation files publicly.

The standalone package path is part of the intended module workflow and may be refined as the project grows.

After completing First Spark, see:

- [`WHAT_NEXT.md`](WHAT_NEXT.md)

For project orientation, see the project wiki:

```text
https://github.com/NataliReise/glossai-nexus/wiki
```

For help, feedback, ideas, or public-safe resonance nodes, see project discussions:

```text
https://github.com/NataliReise/glossai-nexus/discussions
```

Use `Help and Support` for practical questions and `Resonance Nodes` for optional public-safe resonance node posts.

## What First Spark currently does

The current prototype contains the first complete mini game loop:

```text
arrival -> spark chamber -> read traces -> link spark -> unlock activation message -> after-play
```

It proves that a Nexus module can:

- run locally in a terminal,
- move between small game modules,
- keep simple state,
- complete a first activation-message ending,
- load a local private activation file,
- fall back to safe public demo data,
- show an optional public-safe resonance node draft,
- stay data-minimal and avoid automatic result saving,
- protect the main flow with a minimal automated test.

Development principle:

```text
First make the spark run.
Then widen the trace.
```

## Run

From the repository root:

```bash
python3 modules/nexus_01_nexus_mesomerie/first_spark/run_first_spark.py
```

Or from this directory:

```bash
python3 run_first_spark.py
```

Press `Ctrl-C` to interrupt First Spark and return to the terminal.

## Test

From the repository root:

```bash
python3 modules/nexus_01_nexus_mesomerie/first_spark/tests/test_first_spark_flow.py
```

Expected output:

```text
First Spark flow tests passed.
```

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

For the full local workflow, see:

- [`LOCAL_ACTIVATION_GUIDE.md`](LOCAL_ACTIVATION_GUIDE.md)

## Main commands

The exact available commands depend on the current module state.

Useful commands include:

- `/help` - Show available commands for the current module.
- `/look` - Look around or enter the next visible space.
- `/read <trace-name>` - Read a visible trace.
- `/link spark` - Link the first spark fragments after the required traces were read.
- `/unlock` - Open the activation message after the spark was linked.
- `/trace` - Reveal a gentle next hint.
- `/walkthrough` - Show the full solution path with a spoiler warning.
- `/resonance-node` - Show an optional public-safe resonance node draft after completion.
- `/quit` - Leave First Spark.

## Public / private boundary

The public repository contains public code, a public demo fallback, and safe public example data.

Real gift messages, real recipient data, real activation codes, return codes, private notes, and personal configuration belong to the private activation layer and must not be committed to the public repository.

See also:

- [`docs/PUBLIC_PRIVATE_BOUNDARY.md`](../../../docs/PUBLIC_PRIVATE_BOUNDARY.md)
- [`LOCAL_ACTIVATION_GUIDE.md`](LOCAL_ACTIVATION_GUIDE.md)
- [`PUBLIC_HANDOFF_CHECKLIST.md`](PUBLIC_HANDOFF_CHECKLIST.md)
- [`GIFT_PACKAGE_SPEC.md`](GIFT_PACKAGE_SPEC.md)
- [`FIRST_SPARK_AFTER_PLAY.md`](FIRST_SPARK_AFTER_PLAY.md)
- [`WHAT_NEXT.md`](WHAT_NEXT.md)
- [`FIRST_SPARK_0_1_REVIEW.md`](FIRST_SPARK_0_1_REVIEW.md)

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

## First Spark 0.1 review

For the current stability review, design freeze notes, and data-minimization decision, see:

- [`FIRST_SPARK_0_1_REVIEW.md`](FIRST_SPARK_0_1_REVIEW.md)

## Legal notice / Impressum

For legal notice and contact information for the project, see:

- [`LEGAL_NOTICE.md`](../../../LEGAL_NOTICE.md)

## Possible next running units

- Add optional activation field validation for future fields.
- Refine the resonance node draft language after external reading.
- Prepare resonance artifact and return artifact concepts after the after-play layer works.
