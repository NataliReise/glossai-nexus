# Return Resonance Local Workspace

This document describes a safe local workspace shape for Return Resonance.

It is a bridge between the public demo and future private activation workflows.

It does not define a new protocol.
It does not add encryption.
It does not publish anything online.

It only answers one practical question:

```text
Where may private return work live locally without entering the public repository?
```

## Core idea

The public repository may contain the code, documentation, tests, and safe demo examples.

Private return work should live outside committed repository content.

A local workspace can hold:

```text
private return artifacts
private slot files
private local result files
local notes for the person running the Nexus
```

These files should be treated as private by default.

## Recommended location

Use a local workspace outside the public repository, for example:

```text
~/Dokumente/glossai-local/nexus-01-return-workspace/
```

or:

```text
~/Schreibtisch/glossai-local/nexus-01-return-workspace/
```

The exact path is not important.

The important rule is:

```text
Private return work should not live inside the public Git repository unless it is clearly ignored and intentionally local.
```

## Suggested folder shape

```text
nexus-01-return-workspace/
├── README.local.md
├── slots/
│   └── return_slots.local.json
├── artifacts/
│   └── return_artifact.local.txt
├── results/
│   └── return_resonance_example.local.md
└── notes/
    └── private_notes.local.md
```

Suggested meanings:

```text
slots/      -> local waiting slot files
artifacts/  -> local returned artifact files
results/    -> local generated return result files
notes/      -> optional private notes, never public by default
```

## Naming convention

Use `.local` in private or generated filenames:

```text
return_slots.local.json
return_artifact.local.txt
return_resonance_<name>.local.md
private_notes.local.md
```

This makes the privacy status visible at a glance.

## Running the CLI with a local workspace

From the public repository root:

```bash
python3 modules/nexus_01_nexus_mesomerie/run_return_resonance.py \
  --artifact ~/Dokumente/glossai-local/nexus-01-return-workspace/artifacts/return_artifact.local.txt \
  --slots ~/Dokumente/glossai-local/nexus-01-return-workspace/slots/return_slots.local.json \
  --output-dir ~/Dokumente/glossai-local/nexus-01-return-workspace/results
```

The CLI reads:

```text
the artifact from artifacts/
the slot file from slots/
```

It writes or reuses:

```text
a local result file in results/
```

## What belongs in the public repository

Safe public repository content may include:

```text
source code
safe documentation
safe templates
safe demo slots
safe demo artifacts
safe demo result shapes
public-safe tests
```

## What belongs in the local workspace

Private local workspace content may include:

```text
real return artifacts
real private slot files
local result files
private activation notes
private gift context
local recipient notes
local sender notes
```

These files should not be committed.

## What should not be public

Do not commit:

```text
real private activation packages
real gift messages
real return artifacts
real private relationship data
real encrypted private layers
real return keys
real key material
private local result files
private notes
```

## Why outside the repository?

A separate local workspace reduces accidental leakage.

It also keeps the public repository readable as a shared seed:

```text
The public repo shows the shape.
The local workspace carries the private meaning.
```

## If a local file is created inside the repository

Generated local result files such as:

```text
return_resonance_lantern_river.local.md
```

are ignored by Git through the repository `.gitignore`.

Even so, check before committing:

```bash
git status --short
```

If a private file appears in Git status, stop and do not commit it.

## First small manual setup

Create a local workspace:

```bash
mkdir -p ~/Dokumente/glossai-local/nexus-01-return-workspace/{slots,artifacts,results,notes}
```

Copy the safe demo files as a starting point:

```bash
cp modules/nexus_01_nexus_mesomerie/examples/return_slot.demo.json \
  ~/Dokumente/glossai-local/nexus-01-return-workspace/slots/return_slots.local.json

cp modules/nexus_01_nexus_mesomerie/examples/return_artifact.demo.txt \
  ~/Dokumente/glossai-local/nexus-01-return-workspace/artifacts/return_artifact.local.txt
```

Run the CLI:

```bash
python3 modules/nexus_01_nexus_mesomerie/run_return_resonance.py \
  --artifact ~/Dokumente/glossai-local/nexus-01-return-workspace/artifacts/return_artifact.local.txt \
  --slots ~/Dokumente/glossai-local/nexus-01-return-workspace/slots/return_slots.local.json \
  --output-dir ~/Dokumente/glossai-local/nexus-01-return-workspace/results
```

The first run creates a local result.
Later runs reuse it.

## Design boundary

This workspace guide is not a private activation generator.

It only prepares a safe place for future private work.

Future layers may later define how a private activation creates a return slot.
For now, the workspace simply gives private return files somewhere safe to live.

## Working formulas

```text
Keep the public seed clean.
Keep the private return local.
```

```text
The repository carries the pattern.
The workspace carries the meaning.
```

```text
The Nexus may remember locally before it learns to travel further.
```
