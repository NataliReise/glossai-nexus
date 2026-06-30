# Nexus 01 Terms

Status: orientation and terminology guide

This document gives a small shared vocabulary for Nexus 01.

It is meant to help readers distinguish the current implemented path from older or future design notes.

## Current implemented path

The current implemented return path is:

```text
slot-based Return Resonance
-> generated local return slot
-> matching return artifact
-> local result file
```

Milestone formula:

```text
A slot can be generated.
A return can answer it.
A local result can open.
```

Short implementation formula:

```text
Slot -> Artifact -> Local Result
```

## Legacy / future path

The older Return Unlock documents describe a possible later path:

```text
Return Unlock
-> encrypted return layer
-> private activation chain
-> optional real encryption later
```

These documents should be read as legacy/future design notes unless a later milestone explicitly revives them.

Current reading rule:

```text
Return Resonance Slots are the implemented path.
Return Unlock remains a legacy/future optional path.
```

## Terms

### Nexus 01

The first module line in the glossAI Nexus project.

It contains the first playable slice, First Spark, and may grow extension layers around it.

### First Spark

The first small playable terminal slice of Nexus 01.

It must remain complete on its own.

Boundary rule:

```text
Return Resonance may know about First Spark.
First Spark must not depend on Return Resonance.
```

### Activation

A local configuration for a run.

In First Spark, activation already exists as a small local component.

It can support neutral demo play and private local activation play.

Current boundary:

```text
Activation configures a run.
It does not become the whole social chain.
```

### Private activation

A private local activation file or private activation context.

It may contain personal meaning, private messages, recipient context, or gift context.

It must not be committed to the public repository.

For the current Return Resonance generator, private activation parsing is future work.

### Gift package

A private wrapper around a public module.

It may later contain a public module link, private activation, recipient instructions, optional gift note, and optional future return-layer material.

It is not currently implemented as an automated package generator.

### Return Resonance

The current local-first return layer.

It parses a return artifact, matches it against a local return slot, and creates or reuses a local result file.

Current formula:

```text
A waiting slot.
A returned artifact.
One local answer.
```

### Return slot

A local waiting place for a possible return.

A return slot contains safe matching fields such as:

```text
origin_trace_id
return_slot_id
module_id
package_id
layer_id
status
result_file
public_safe_label
```

The slot should not contain private gift meaning, real names, contact details, key material, or private relationship context.

Working formula:

```text
The activation knows why.
The slot only knows how to wait.
```

### Generated return slot

A return slot created by `make_return_slot.py` from explicit values.

The generator does not read private activation packages.

It does not publish anything online.

It does not implement encryption.

### Return artifact

A structured text artifact that may answer a waiting return slot.

In the current MVP, a return artifact is parsed and matched against a local slot.

It is not a public forum post.

For real use, a return artifact should be kept private.

### Matching

The local check that decides whether a return artifact belongs to a waiting or already opened slot.

Important statuses include:

```text
match_waiting
match_opened
unknown_slot
package_mismatch
layer_mismatch
```

Boundary formula:

```text
The Nexus does not open every return.
It opens only what belongs to a waiting or already opened slot.
```

### Local result

A local Markdown result file created after a matching return artifact answers a waiting slot.

It is reused on later matching runs.

It should stay outside public Git.

Working formula:

```text
Generate once.
Revisit often.
```

### Return Unlock

An older and possible future design direction for a deeper unlock mechanism.

It may later involve encrypted return layers, key derivation, or stronger private package flows.

It is not the current implemented MVP.

Current reading rule:

```text
Return Unlock = legacy/future design direction.
Return Resonance Slots = current implemented direction.
```

### Encrypted return layer

A possible later private layer that could be technically encrypted.

This is not implemented in the current MVP.

Until real encryption exists, the project should avoid implying a cryptographic security promise.

Rule:

```text
No custom cryptography as a security promise.
```

### Narrative decryption

A current conceptual phrase for making meaning readable without claiming real cryptographic decryption.

Working formula:

```text
The Nexus decrypts meaning, not necessarily ciphertext.
```

### Public-safe trace

A harmless optional public note that may say a spark was seen, carried, completed, or returned.

It must not contain private activation data, private gift messages, return artifacts, return keys, raw seeds, key material, encrypted layer content, or private relationship context.

### Private local workspace

A local folder outside the public repository for real slots, real return artifacts, real result files, and private context.

Suggested pattern:

```text
~/Dokumente/glossai-local/nexus-01-return-workspace/
```

The public repository shows the shape.

The private workspace carries the meaning.

### Public repository

The public repository may contain:

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

It must not contain:

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

The current implemented Return Resonance layer does not include:

```text
private activation parsing
private gift package generation
real encryption
identity verification
network behavior
automatic publishing
GitHub API behavior
contact matching
AI-generated live responses
```

## Reading guide

For the implemented path, read first:

```text
return_resonance/README.md
RETURN_RESONANCE_MVP.md
RETURN_RESONANCE_LOCAL_WORKSPACE.md
RETURN_SLOT_GENERATOR_WALKTHROUGH.md
RETURN_RESONANCE_GENERATED_SLOT_MILESTONE.md
```

For the bridge between old and new directions, read:

```text
RETURN_UNLOCK_CURRENT_DIRECTION.md
```

For older/future design ideas, read later:

```text
RETURN_UNLOCK_LAYER_MAP.md
RETURN_UNLOCK_DESIGN.md
```

## Working formulas

```text
Slot -> Artifact -> Local Result
```

```text
The public repo shows the shape.
The private workspace carries the meaning.
```

```text
Private meaning may create structure.
Structure must not expose private meaning.
```

```text
Build the bridge before carrying the secret across it.
```
