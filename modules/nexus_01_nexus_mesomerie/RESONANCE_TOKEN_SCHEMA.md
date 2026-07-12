# Nexus 01 Resonance Token Schema

This document defines the first minimal schema for a **Nexus 01 Resonance Token**.

The token is a small, transferable structural artifact. It may travel with a Nexus 01 package from one person to another and make the **Return Resonance Layer** available without exposing the private meaning behind the original activation.

```text
The activation may know why.
The token only needs to know which path it may open.
```

## Purpose

The first Resonance Token connects three existing ideas:

```text
waiting return slot
-> resonance activation
-> Resonance Chamber
-> return artifact
```

It has two jobs:

```text
1. Identify the waiting resonance arc that a later return artifact may answer.
2. Make the Resonance Chamber available in a compatible Nexus 01 package.
```

It must not:

```text
carry the private gift message
identify a person
prove identity
send anything automatically
contain cryptographic claims
contain hidden relationship context
```

## Boundary

A Resonance Token is not:

```text
a private activation
a return artifact
a return result
a user account
an authentication credential
a social graph edge
```

It is a structural invitation.

```text
A slot waits locally.
A token carries the path.
An artifact may return through that path.
```

## Minimal schema

The first schema uses JSON.

```json
{
  "token_version": "N01-RT-1",
  "token_type": "resonance-activation",
  "module_id": "N01",
  "layer_id": "return-resonance-1",
  "origin_trace_id": "n01-local-origin-a4m9",
  "return_slot_id": "quiet-garden-01",
  "package_id": "local-package-garden-01",
  "enabled_chambers": ["resonance"],
  "public_safe_label": "quiet garden",
  "note": "This token identifies a resonance arc, not a person."
}
```

## Required fields

### `token_version`

Format identifier for the token schema.

First value:

```text
N01-RT-1
```

This allows later schema revisions without silently changing the meaning of older tokens.

### `token_type`

Declares the purpose of the document.

First value:

```text
resonance-activation
```

The token opens or enables a resonance path. It is not itself the returned answer.

### `module_id`

Identifies the compatible Nexus Module line.

First value:

```text
N01
```

### `layer_id`

Identifies the Return Resonance layer.

First value:

```text
return-resonance-1
```

The value should match the waiting Return Slot and the later Return Artifact.

### `origin_trace_id`

Identifies the local resonance arc that prepared the waiting slot.

It must not identify a person directly.

Good:

```text
n01-local-origin-a4m9
n01-origin-r7k2
```

Avoid:

```text
full-person-name
email-address
birthday-secret-for-name
```

### `return_slot_id`

Identifies the waiting return place.

It should be symbolic and safe to carry.

Examples:

```text
quiet-garden-01
lantern-river-01
owl-window-02
```

### `package_id`

Identifies the compatible carried package or resonance package.

It must match the package identifier expected by the waiting Return Slot and later copied into the Return Artifact.

It should remain structural rather than personal.

### `enabled_chambers`

Lists the Chambers made available by this token.

For the first MVP:

```json
["resonance"]
```

The existing First Spark path remains independently available through the package activation. The token only adds the Resonance Chamber.

## Optional fields

### `public_safe_label`

A short symbolic label that may be shown in the Nexus Atrium or Resonance Chamber.

Example:

```text
quiet garden
```

It must not reveal private meaning.

### `note`

A short structural or privacy note.

Recommended default:

```text
This token identifies a resonance arc, not a person.
```

The note must not carry private relationship context.

## Deliberately excluded fields

The first token must not contain:

```text
recipient name
sender name
contact details
private message
private activation purpose
private emotional context
return text
carrier image
carrier movement
return word
return image
return tone
result filename
local filesystem path
automatic delivery target
```

Reasons:

- private activation meaning stays with the private activation
- return content should emerge inside the Resonance Chamber
- local result paths belong to the waiting Return Slot
- transport remains manual and human-mediated

## Relationship to the Return Slot

A Resonance Token carries a subset of the structural identifiers already known by a waiting Return Slot.

Shared matching fields:

```text
origin_trace_id
return_slot_id
package_id
layer_id
```

The Return Slot remains local to the earlier giver or origin Nexus.

The Resonance Token may travel onward.

```text
Return Slot: waits locally
Resonance Token: carries the compatible path
Return Artifact: carries the answer back
Return Result: opens locally
```

## Relationship to activation

A private activation and a Resonance Token have different responsibilities.

```text
Private activation:
  makes a concrete run personal
  may contain recipient-facing private meaning

Resonance Token:
  enables the Return Resonance path
  carries only structural identifiers
```

A future resonance package may contain both:

```text
activation.local.json
resonance_token.local.json
```

The files should remain separate even when bundled together.

## Relationship to the Nexus Atrium

When a valid token is present, the Atrium may reveal an additional path:

```text
resonance.door
```

The Atrium may show the optional `public_safe_label`, but it must not display or infer private meaning.

The token does not force the player to enter the Resonance Chamber.

```text
The token makes the path available.
The player decides whether to enter it.
```

## Relationship to the Resonance Chamber

The Resonance Chamber may use the token identifiers to build the structural header of a Return Artifact:

```text
Module
Origin Trace
Return Slot
Package
Layer
```

The Chamber should generate or collect the expressive fields through play:

```text
carrier_image
carrier_movement
return_word
return_image
return_tone
```

This keeps structural matching separate from human resonance.

## Validation rules for the first implementation

A token is valid only if:

```text
it is valid JSON
its top level is an object
all required fields are present and non-empty
its token_version is N01-RT-1
its token_type is resonance-activation
its module_id is N01
its layer_id is return-resonance-1
its enabled_chambers is a list containing resonance
its structural ID fields are strings
```

The first validator should reject unknown required-version values calmly and explicitly.

Optional fields may be absent.

Extra fields should initially be rejected or warned about rather than silently trusted. This keeps the first schema small and readable.

## File naming

Public template:

```text
templates/resonance_token.template.json
```

Local carried token:

```text
resonance_token.local.json
```

Real local tokens must not be committed to the public repository.

## First implementation boundary

The first implementation should provide:

```text
schema documentation
a public-safe copy-before-use template
a parser and validator
tests for valid and invalid tokens
```

It should not yet provide:

```text
automatic token delivery
identity verification
cryptographic signing
a central registry
automatic activation parsing
network behavior
```

## Working formulas

```text
Private meaning may create structure.
Structure must not expose private meaning.
```

```text
The slot waits.
The token carries.
The Chamber transforms.
The artifact returns.
```

```text
The token opens a possibility.
It does not manage the relationship.
```
