# Return Slot from Private Activation

This document describes the boundary between a private activation and a public-safe Return Resonance slot.

It does not define a generator yet.
It does not implement encryption.
It does not add identity verification.
It does not publish private meaning.

It only clarifies the bridge:

```text
private activation
-> public-safe or local-safe return slot
-> returned artifact
-> local result
```

## Core rule

```text
A private activation may create a waiting slot.
The slot may be public-safe.
The meaning behind the slot remains private.
```

A return slot should be treated as a structural invitation, not as the private message itself.

## Why this bridge matters

First Spark can be played as a public-safe slice.

A private activation can turn that slice into a personal gift or local experience.

Return Resonance adds the possibility that something may come back later.

For that to work safely, the private activation needs a way to create a waiting return place without exposing the private meaning behind it.

```text
The activation knows why the slot matters.
The slot only knows how to wait.
```

## Intended flow

A future private activation may eventually create:

```text
private activation package
-> local slot file
-> local or carried return artifact
-> local result file
```

The public repository should only define the shape and safe rules.

The private workspace carries the actual meaning.

## What a private activation may know

A private activation may know things such as:

```text
private gift text
private relationship context
intended recipient context
private symbolic meaning
private timing
private local notes
private sender intention
private response expectations
```

These belong to the private activation package or local workspace.

They do not belong in the public repository.

## What a return slot may contain

A return slot may contain structural, public-safe, or local-safe fields such as:

```text
origin_trace_id
return_slot_id
module_id
package_id
layer_id
status
result_file
public_safe_label
note
```

These fields should be enough to match a returned artifact to a waiting place.

They should not reveal the private gift meaning.

## What must not be copied into a public-safe slot

Do not put these into a public-safe slot:

```text
real private gift message
real private relationship details
recipient identity details
sender identity details
private emotional context
real key material
private activation secrets
private return instructions that reveal meaning
```

A slot may point to a private context indirectly through local-only identifiers.
It should not publish that context.

## Local-safe versus public-safe slots

There are two useful categories:

```text
public-safe slot
local-safe slot
```

A public-safe slot can appear in the repository as demo or template data.
It must contain fictional or non-private information.

A local-safe slot can live in a private workspace.
It may contain more specific local information, but it should still avoid unnecessary private detail.

Even local-safe slots should follow data-minimal design.

## Suggested slot boundary

A good slot should answer:

```text
Which return does this belong to?
Which module/layer does it use?
Where should the local result be written?
Is the slot waiting or already opened?
```

A good slot should not answer:

```text
Who is this really for?
What is the private gift meaning?
What private story does this encode?
What secret should be unlocked?
```

Those belong elsewhere.

## Origin trace IDs

`origin_trace_id` should identify a local resonance arc or activation trace.

It should not identify a person directly.

Good:

```text
n01-demo-origin-7kq2
n01-local-origin-a4m9
```

Avoid:

```text
recipient-full-name
email-address
phone-number
private-event-name
```

The ID may be meaningful locally, but it should not expose private meaning by itself.

## Return slot IDs

`return_slot_id` identifies the waiting return place.

It may be symbolic, but should stay public-safe if committed.

Good:

```text
lantern-river-01
owl-window-02
quiet-garden-01
```

Avoid:

```text
private-confession-from-anna
birthday-secret-for-real-name
medical-crisis-return-slot
```

## Result files

`result_file` should usually use `.local.md` for generated local results:

```text
return_resonance_lantern_river.local.md
return_resonance_quiet_garden.local.md
```

Generated local results should not be committed.

## Slot template

A neutral copy-before-use template exists at:

```text
templates/return_slot.template.json
```

Use it as a starting point for a local workspace slot file.

Copy it before editing:

```bash
cp modules/nexus_01_nexus_mesomerie/templates/return_slot.template.json \
  ~/Dokumente/glossai-local/nexus-01-return-workspace/slots/return_slots.local.json
```

Then replace the `CHANGE-ME` values with local-safe identifiers.

Do not put private meaning, real names, contact details, key material, or private relationship context into the copied slot file unless it is intentionally private and kept outside the public repository.

## Private activation to slot translation

A future generator may translate a private activation into a slot by extracting only structural fields:

```text
private activation meaning -> stays private
origin trace -> safe local identifier
return slot -> safe symbolic identifier
result target -> local result filename
status -> waiting
```

This translation should be one-way for public-safe output:

```text
Private meaning may create a slot.
A slot should not reveal the private meaning.
```

## Current manual approach

Until a generator exists, a local slot file can be created manually in a private workspace.

Example shape:

```json
{
  "document_status": "private local return slots",
  "slots": [
    {
      "origin_trace_id": "n01-local-origin-a4m9",
      "return_slot_id": "quiet-garden-01",
      "module_id": "N01",
      "package_id": "local-package",
      "layer_id": "return-resonance-1",
      "status": "waiting",
      "result_file": "return_resonance_quiet_garden.local.md",
      "public_safe_label": "quiet garden",
      "note": "origin_trace_id identifies a local resonance arc, not a person"
    }
  ]
}
```

This file should live in the local workspace, for example:

```text
~/Dokumente/glossai-local/nexus-01-return-workspace/slots/return_slots.local.json
```

## Future generator boundaries

A future slot generator may:

```text
read a private activation package locally
create a local slot file
choose safe symbolic IDs
choose a local result filename
write only to a chosen local workspace
```

A future slot generator should not:

```text
commit private files
publish return slots automatically
send private meaning online
claim cryptographic security unless implemented
identify people directly
store more private data than needed
modify First Spark core
```

## Relationship to First Spark

First Spark remains complete on its own.

A private activation may create a return slot for a later return layer, but First Spark should not depend on Return Resonance.

Protected boundary:

```text
Return Resonance may know about First Spark.
First Spark must not depend on Return Resonance.
```

## Relationship to the local workspace

The local workspace is the natural home for generated private slots.

Suggested flow:

```text
public repo code
+ private local activation
-> local workspace slot file
-> local return artifact
-> local result file
```

The public repo carries the pattern.
The local workspace carries the meaning.

## Non-goals

This document does not define:

```text
real encryption
identity proof
network transport
account ownership
recipient authentication
public return registry
private package format
automatic slot generation code
```

Those may become later layers, but they are not part of this boundary note.

## Working formulas

```text
The activation may know why.
The slot only needs to know where to wait.
```

```text
Private meaning may create structure.
Structure must not expose private meaning.
```

```text
A waiting slot is not a confession.
It is only a place prepared for return.
```
