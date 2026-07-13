# Resonance Local Opening Status V0.1

Status date: 2026-07-14

## Current milestone

The shared Resonance Return Artifact can now be opened through a practical local workflow.

```text
Resonance Token
-> Chamber Selections
-> Resonance Return Artifact
-> private transport
-> local Return Slot matching
-> local opening
   |- Resonance Artifact
   `- Nexus Echo
-> stable result file
-> slot state: opened
```

This is the first point at which the complete Return Resonance path is not only validated in memory, but usable as a local file-based process.

## Implemented command

```text
open_resonance_return.py
```

The command accepts:

```text
--artifact
--slots
--output-dir
--library-dir   optional
```

It performs the following sequence:

1. load and validate the shared JSON Resonance Return Artifact
2. load the local Return Slot document
3. match route identity through the existing matcher
4. reject unknown or incompatible returns
5. render the approved Resonance Artifact
6. render the approved Nexus Echo
7. write one local Markdown result
8. mark the matching slot as `opened`
9. reuse the existing result on later openings

Nothing is uploaded or published.

## Result behavior

The local result contains:

- slot and route metadata
- language-library version
- the complete Resonance Artifact
- the complete Nexus Echo
- a privacy reminder

The result follows the existing local-first rule:

```text
Generate once.
Revisit often.
```

If the result file already exists, it is read and returned unchanged.

The command does not regenerate, replace, or normalize an existing result.

This allows a locally opened result to accumulate human annotations without later runs erasing them.

## Persistent slot state

A successful first opening changes the matching slot from:

```text
waiting
```

to:

```text
opened
```

The slot update is limited to the single entry identified by:

```text
origin_trace_id
return_slot_id
```

The command requires exactly one matching slot before changing local state.

## Protected behavior

The workflow currently protects against:

- unknown Return Slots
- package mismatches
- layer mismatches
- module mismatches
- unsupported artifact versions
- unsupported language-library versions
- unknown or incompatible selection IDs
- missing approved Echo paths
- overwriting an existing local result
- changing slot state after a failed match
- an `opened` slot whose result file is missing
- ambiguous slot-state updates

Temporary files are used when writing a new result and when replacing the slot JSON document.

## Verified test

```text
return_resonance/tests/test_open_resonance_return.py
```

Verified locally on 2026-07-14:

```text
Local Resonance Return opening tests passed.
```

The test covers:

- first opening creates the local result
- both poetic outputs are present
- slot state changes to `opened`
- repeated opening reuses the result
- local additions remain untouched
- a missing result for an opened slot is rejected
- package mismatch creates neither result nor state change

## Relationship to earlier paths

The older human-readable Return Artifact path remains available and unchanged:

```text
run_return_resonance.py
return_resonance/artifact.py
return_resonance/writer.py
return_resonance/result.py
```

The new local opening command uses the shared JSON contract and the approved language-library renderers.

The two paths are deliberately not merged yet.

This preserves the tested legacy behavior while the new Resonance Chamber contract matures.

## Current boundary

The opening workflow is operational, but it still expects the required files to exist already:

- a valid shared Resonance Return Artifact
- a local Return Slot document
- a writable local output directory
- the compatible language library

There is not yet a curated public-safe demonstration package that lets a new reader perform the whole workflow without assembling these pieces manually.

There is also not yet one command that creates a shared artifact from a token and chamber selections and then exports it for private transfer.

## Recommended next slice

Create a complete public-safe demonstration path with:

```text
examples/resonance_return_artifact.demo.json
examples/resonance_return_slots.demo.json
examples/local_opening_demo/
```

and a short walkthrough showing:

```text
copy demo workspace
-> run local opening command
-> inspect result
-> run command again
-> observe result reuse
```

The demo should use only invented identifiers and approved library selections.

It should not modify the canonical example files in place; the walkthrough should begin by copying them into a temporary or private local workspace.

## Working formula

```text
The route reaches the poem.
The poem now has a local place to remain.
```
