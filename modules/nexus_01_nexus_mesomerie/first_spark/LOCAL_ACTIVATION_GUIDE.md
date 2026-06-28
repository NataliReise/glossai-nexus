# Local Activation Guide

This guide explains how to add a private local activation to **Nexus 0.1 - First Spark** without committing personal data to the public repository.

Core rule:

> The module may be public.  
> The activation remains private.

## What belongs in the public repository?

The public repository may contain:

- reusable module code,
- public documentation,
- public demo placeholders,
- safe example activation files,
- tests that do not depend on private local data.

The public repository must not contain:

- real recipient names,
- real private gift messages,
- private notes,
- real activation codes,
- real return codes,
- contact data,
- secrets or access data.

## Local activation file

First Spark looks for this local file:

```text
modules/nexus_01_nexus_mesomerie/first_spark/activation.local.json
```

This file is ignored by Git. It is meant for your local machine only.

A public example file is included here:

```text
modules/nexus_01_nexus_mesomerie/first_spark/activation.example.json
```

## Create a local activation file

From the repository root:

```bash
cp modules/nexus_01_nexus_mesomerie/first_spark/activation.example.json \
   modules/nexus_01_nexus_mesomerie/first_spark/activation.local.json
```

Then edit the local file:

```bash
xed modules/nexus_01_nexus_mesomerie/first_spark/activation.local.json
```

Use your preferred editor if `xed` is not available.

## Minimal local activation

Example structure:

```json
{
  "recipient_alias": "Testname",
  "activation_purpose": "gift",
  "private_message": "This is a private local message. Do not commit this file."
}
```

Only use safe test values while experimenting.

## If the activation file is broken

If `activation.local.json` is not valid JSON, or if its top-level value is not a JSON object, First Spark stops with a friendly error instead of a Python traceback.

The error message points to the local file, names the problem, and reminds you to compare the file with `activation.example.json`.

Fix the JSON and start First Spark again.

## Check that the local file stays private

Run:

```bash
git status
```

Expected result:

```text
nichts zu committen, Arbeitsverzeichnis unverändert
```

or in English:

```text
nothing to commit, working tree clean
```

You can also inspect ignored files explicitly:

```bash
git status --ignored modules/nexus_01_nexus_mesomerie/first_spark/activation.local.json
```

The local activation file should appear as ignored, not as a file to be committed.

## Start First Spark with local activation

From the repository root:

```bash
python3 modules/nexus_01_nexus_mesomerie/first_spark/run_first_spark.py
```

You should see the local recipient alias in the boot sequence:

```text
Activation detected.
Recipient: Testname
Private message: locked.
```

The private message appears only after the spark has been linked and unlocked.

## Run the automated test

From the repository root:

```bash
python3 modules/nexus_01_nexus_mesomerie/first_spark/tests/test_first_spark_flow.py
```

Expected output:

```text
First Spark flow tests passed.
```

The test is activation-agnostic. It should pass with or without a valid local `activation.local.json` file.

## Safe sharing workflow

Before sharing the module or pushing changes:

```bash
git status
```

If Git is clean, the local activation file has not been staged or committed.

When sharing the public module, share only the repository files. Do not share your local `activation.local.json` unless you intentionally want to send that private activation to one specific person through a private channel.

## If something feels confusing

If terminal commands are accidentally pasted into First Spark, the module may show an unknown-command message. This is expected and safe.

Use:

```text
help
```

for available Nexus commands, or:

```text
quit
```

on a fresh prompt to leave First Spark and return to your terminal.
