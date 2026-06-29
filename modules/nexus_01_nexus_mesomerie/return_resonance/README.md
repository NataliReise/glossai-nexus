# Return Resonance

Return Resonance is the first small return layer for Nexus 01.

It belongs to the Nexus 01 extension layer, not to the First Spark core.

Core formula:

```text
A waiting slot.
A returned artifact.
One local answer.
```

## What this layer does

The first Return Resonance MVP can:

1. parse a human-readable return artifact,
2. load a local return slot file,
3. match the artifact against the waiting slot,
4. create a local result file on first opening,
5. reuse the same local result file on later runs.

This implements the rule:

```text
Generate once.
Revisit often.
```

## Boundary to First Spark

First Spark remains complete on its own.

Return Resonance may refer to First Spark as the first playable origin of Nexus 01, but First Spark must not depend on Return Resonance.

Boundary rule:

```text
Return Resonance may know about First Spark.
First Spark must not depend on Return Resonance.
```

## Files in this package

```text
return_resonance/
├── __init__.py
├── artifact.py
├── slots.py
├── matching.py
├── result.py
└── tests/
    └── test_return_resonance_mvp.py
```

Current responsibilities:

```text
artifact.py  -> parse structured return artifact text
slots.py     -> load local return slots from JSON
matching.py  -> match artifact and slot IDs safely
result.py    -> create or reuse local Markdown result files
tests/       -> protect the MVP behavior and First Spark boundary
```

## Demo files

The public demo uses safe example files from:

```text
../examples/return_slot.demo.json
../examples/return_artifact.demo.txt
../examples/return_artifact.unknown_slot.demo.txt
../examples/return_resonance_result.demo.md
```

These files contain fictional demo data only.

They show the shape of the return flow and the non-match boundary without exposing real private activation data, gift text, return artifacts, key material, or private relationship context.

## Run the demo

From the repository root:

```bash
python3 modules/nexus_01_nexus_mesomerie/run_return_resonance_demo.py
```

On the first run, the demo creates:

```text
modules/nexus_01_nexus_mesomerie/return_resonance_lantern_river.local.md
```

On later runs, the same file is reused.

Expected behavior:

```text
Local result created: return_resonance_lantern_river.local.md
```

Then:

```text
Local result reused: return_resonance_lantern_river.local.md
```

## Run with explicit local paths

For local experiments beyond the fixed public demo, use:

```bash
python3 modules/nexus_01_nexus_mesomerie/run_return_resonance.py \
  --artifact path/to/return_artifact.txt \
  --slots path/to/return_slots.json \
  --output-dir path/to/local-memory
```

This command uses the same Return Resonance layer as the demo, but it does not assume the demo paths.

It still stays local:

```text
no network access
no public posting
no First Spark dependency
no real encryption
no identity verification
```

Exit codes:

```text
0 -> matched and opened or reused a local result
1 -> artifact did not match a waiting or opened slot
2 -> file, parsing, slot-loading, or result-opening error
```

## Run the non-match demo

The unknown-slot demo artifact intentionally does not match the public demo slot.

Run:

```bash
python3 modules/nexus_01_nexus_mesomerie/run_return_resonance.py \
  --artifact modules/nexus_01_nexus_mesomerie/examples/return_artifact.unknown_slot.demo.txt \
  --slots modules/nexus_01_nexus_mesomerie/examples/return_slot.demo.json \
  --output-dir /tmp/glossai-return-non-match
```

Expected behavior:

```text
Match status: unknown_slot
No local result was opened because the artifact did not match a slot.
```

This demonstrates the protection boundary:

```text
The Nexus does not open every return.
It opens only what belongs to a waiting or already opened slot.
```

For a recommended private local folder layout, see:

```text
../RETURN_RESONANCE_LOCAL_WORKSPACE.md
```

For the boundary between private activations and public-safe return slots, see:

```text
../RETURN_SLOT_FROM_PRIVATE_ACTIVATION.md
```

## Local files and Git

Generated local result files should stay local.

They are ignored by Git through patterns such as:

```text
return_resonance_*.local.md
return_result.local.md
```

This protects the public/private boundary.

## Run the tests

From the repository root:

```bash
python3 modules/nexus_01_nexus_mesomerie/return_resonance/tests/test_return_resonance_mvp.py
```

To verify that First Spark still works independently:

```bash
python3 modules/nexus_01_nexus_mesomerie/first_spark/tests/test_first_spark_flow.py
```

Both should pass.

## Privacy boundary

Public repository files may contain:

```text
source code
documentation
safe examples
safe templates
demo slots
demo artifacts
demo result files
public-safe terminology
```

Public repository files must not contain:

```text
real private activation data
real gift messages
real private packages
real return artifacts
real return keys
real key material
real encrypted private layers
private relationship context
```

## Current non-goals

This MVP does not implement:

```text
real encryption
automatic online behavior
GitHub API integration
automatic public posting
full package generation
account or identity system
contact matching
AI-generated live responses
complex activity graph
```

## Working formulas

```text
The Nexus decrypts meaning, not necessarily ciphertext.
```

```text
Return slots wait.
Return artifacts answer.
The Nexus remembers what returned.
```

```text
The spark remains small.
The Nexus learns to answer.
```
