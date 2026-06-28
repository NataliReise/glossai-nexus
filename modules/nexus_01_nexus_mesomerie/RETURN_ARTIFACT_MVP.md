# Return Artifact MVP

A first minimal format for the artifact that returns from a carried spark.

Document status: early MVP planning draft  
Project: glossAI Nexus  
Module line: Nexus 01 - Nexus-Mesomerie  
Related prototype: Nexus 0.1 - First Spark  
Related design note: [Return Unlock Design](RETURN_UNLOCK_DESIGN.md)

---

## 1. Purpose

This document defines a first minimal working shape for a **Return Artifact** in Nexus 01.

A return artifact is the private artifact that travels backward after a carried spark has been played.

In the first full private resonance chain:

```text
A gives to B.
B may give to C.
C may return to B.
B may unlock a deeper layer.
```

The return artifact is the thing that C privately returns to B.

It may later allow B to unlock a deeper return layer.

This document does not implement encryption yet.

It only defines a first MVP format that can guide later implementation.

---

## 2. Core Rule

A return artifact is private by default.

It must not be posted publicly.

It is not a resonance node.

It is not a public-safe return trace.

It is not a social proof object.

It is the private return that may unlock or help unlock a deeper layer.

Working distinction:

```text
Return Artifact = private backward artifact
Public-Safe Return Trace = optional public reward after successful unlock
Resonance Node = optional public-safe trace that a spark was seen
```

Core formula:

```text
Return Artifact travels backward.
Return Trace may be shared only after it has been made public-safe.
```

---

## 3. MVP Format Direction

The first return artifact should be a **structured human-readable text block**.

It should not be only a single word.

It should not start as raw JSON for players.

It may later contain an encoded or opaque technical payload, but its outer form should be readable and copyable.

Preferred MVP direction:

```text
human-readable wrapper
+ clear privacy warning
+ safe identifiers
+ guided symbolic fields
+ opaque private return code
+ optional public-safe trace suggestion or preview
```

Why not only one short phrase?

```text
A short phrase is poetic, but too fragile and ambiguous.
```

Why not only JSON?

```text
JSON is useful for machines, but less friendly as a first player-facing artifact.
```

---

## 4. Minimal Text Block Shape

A first MVP return artifact may look like this:

```text
NEXUS RETURN ARTIFACT
Version: N01-RA-MVP-1
Module: Nexus 01 - First Spark
Package: <package_id>
Layer: <layer_id>
From carried run: <run_marker>

Carrier phrase:
<trace-generated phrase>

Human trace:
<guided public/private-safe resonance word or phrase>

Private return code:
<opaque private code or payload>

Public-safe trace suggestion:
<optional generated public-safe phrase preview>

Privacy:
Do not post this return artifact publicly.
Send it only to the previous giver through a private channel.
This artifact may contain private return material or future key material.
```

This shape is intentionally more verbose than the future technical minimum.

It should be understandable to a human recipient and safe enough to discourage accidental public posting.

---

## 5. Field Notes

### 5.1 Version

The version marks the artifact format.

Example:

```text
Version: N01-RA-MVP-1
```

This helps future versions remain compatible or fail gracefully.

### 5.2 Module

The module field names the module line and playable slice.

Example:

```text
Module: Nexus 01 - First Spark
```

This helps the previous giver understand where the artifact belongs.

### 5.3 Package

The package field points to the private package or activation context.

Example:

```text
Package: N01-PKG-7KQ2
```

The package id should be safe to display inside the private artifact.

It should not itself reveal private gift text or personal data.

### 5.4 Layer

The layer field identifies the return layer the artifact may unlock.

Example:

```text
Layer: N01-RL-001
```

The layer id may be checked before a deeper unlock is attempted.

### 5.5 From carried run

The run marker may identify the carried run in a lightweight way.

Example:

```text
From carried run: carried-spark-01
```

This should remain safe and non-identifying.

### 5.6 Carrier phrase

The carrier phrase may be generated from the carried run.

It may reflect guided choices or symbolic outcomes.

Example:

```text
Carrier phrase:
The trace returned with a locked lantern.
```

This phrase is part of the private return artifact unless explicitly made public-safe elsewhere.

### 5.7 Human trace

The human trace may contain a guided resonance word or short phrase.

Example:

```text
Human trace:
courage
```

The human trace may shape the return artifact and later generated revelation.

It may also participate in key derivation.

However, cryptographic strength must not rely on this short human phrase alone.

Important privacy note:

```text
The human trace is not automatically public-safe.
```

If a public-safe trace should include a human word, the system should ask for or provide a separate public-safe trace word.

### 5.8 Private return code

The private return code is the opaque part of the return artifact.

It may later contain or encode:

```text
key material
payload material
integrity information
run-derived material
random material
```

Example placeholder:

```text
Private return code:
N01-PRC-EXAMPLE-DO-NOT-POST
```

This field must never be posted publicly.

### 5.9 Public-safe trace suggestion

The public-safe trace suggestion is optional.

It is not the final return trace.

It is not the return artifact.

It cannot unlock anything.

It may be shown as a preview or raw ingredient, but it should not be treated as proof that the return layer has opened.

Example:

```text
Public-safe trace suggestion:
The lantern answered through courage.
```

If it is included inside the return artifact, it should still be treated carefully.

The final public-safe return trace should be generated or confirmed only after B successfully unlocks the return layer.

---

## 6. Public vs Private Parts

### Private by default

The full return artifact is private by default.

These fields must not be posted publicly:

```text
full return artifact
private return code
return key
key material
raw seed
private human trace if not explicitly public-safe
encrypted layer content
private activation data
private gift text
private relationship context
```

### Potentially public-safe after confirmation

These fields or derived values may be public-safe if explicitly prepared for sharing:

```text
module id
public status
public alias
public note
consent marker
generated public-safe phrase
statement that no private data is included
```

### Strong rule

```text
The Return Artifact itself is never the forum post.
The forum post may only be a public-safe trace generated or confirmed after the completed return.
```

---

## 7. Relationship to Public-Safe Return Trace

A public-safe return trace is a separate object.

It is the publishable reward that may appear after B successfully unlocks the return layer.

It may contain generated content, public aliases, public notes, and consent text.

It should be generated or confirmed at B's unlock stage, not treated as complete at C's return stage.

The return artifact may contain a suggestion or preview, but the final public-safe return trace should appear only after the private return has actually worked.

This preserves the meaning of the public trace:

```text
C brought the answer back.
B opened the layer.
Only then may the public trace appear.
```

A public-safe return trace may include:

```text
Return Trace: N01-RT-draft
Module: Nexus 01 - First Spark
Status: return layer opened
Trace visibility: public-safe summary only
Public phrase: <generated public-safe phrase>
Public alias B:
Public alias C:
Public note:
Consent:
We choose to share this public trace.
No private activation data, private gift text, return artifact, key material, or encrypted layer content is included.
```

This public-safe trace can be copied manually into a GitHub Discussion if the participants choose to share it.

It must not contain the private return artifact.

---

## 8. Relationship to Carrier Reward

C may receive a small carrier reward after producing or receiving the return artifact.

This reward should not reveal B's private return layer.

Example:

```text
You have returned a spark.
If the previous giver opens it, a deeper layer may answer.
```

C may also receive an optional public-safe carrier trace.

Example:

```text
Carrier Trace:
A spark was carried and returned.
```

This carrier trace is not proof of B's unlock.

The main return trace should be created after B successfully opens the return layer.

---

## 9. Human Trace and Public Trace Word

The human trace may be private.

The public trace word should be separate if there is any risk of leaking private or key-related material.

Possible future prompts:

```text
Choose one resonance word for the private return artifact.
```

and separately:

```text
Choose one public-safe word that may appear in a public return trace.
Leave blank to use a neutral generated phrase.
```

This keeps the poetic input useful without accidentally exposing key material or private meaning.

---

## 10. Current Design Decisions

This section records design decisions that have become stable enough to guide the next planning step.

### Decision 01: Public-safe return trace timing

The return artifact may include a public-safe trace suggestion or preview.

However, the final public-safe return trace should be generated or confirmed only after B successfully unlocks the return layer.

The public-safe return trace is the publishable reward.

It may include generated content, public aliases, public notes, and consent text.

It must never include:

```text
return artifact
private return code
return key
key material
raw seed
encrypted layer content
private return message
private gift text
private activation data
private relationship context
```

C may receive a carrier reward or carrier trace at the return stage.

B receives the main public-safe return trace after successful unlock.

Working formula:

```text
C brings the answer back.
B opens the layer.
Only then may the public trace appear.
```

---

## 11. MVP Example

Example private return artifact:

```text
NEXUS RETURN ARTIFACT
Version: N01-RA-MVP-1
Module: Nexus 01 - First Spark
Package: N01-PKG-DEMO-7KQ2
Layer: N01-RL-DEMO-001
From carried run: carried-spark-demo

Carrier phrase:
The trace returned with a locked lantern.

Human trace:
courage

Private return code:
N01-PRC-DEMO-DO-NOT-POST-8F4A

Public-safe trace suggestion:
The lantern answered through courage.

Privacy:
Do not post this return artifact publicly.
Send it only to the previous giver through a private channel.
This artifact may contain private return material or future key material.
```

Example public-safe return trace derived later after successful unlock:

```text
Return Trace: N01-RT-draft
Module: Nexus 01 - First Spark
Status: return layer opened
Trace visibility: public-safe summary only
Public phrase: The lantern answered through courage.
Public alias B:
Public alias C:
Public note:

Consent:
We choose to share this public trace.
No private activation data, private gift text, return artifact, key material, or encrypted layer content is included.
```

---

## 12. MVP Constraints

For the first MVP planning pass, the return artifact format should remain:

```text
copyable
human-readable
private by default
explicitly marked as not for public posting
structured enough for later parsing
simple enough for terminal use
compatible with future encryption work
```

It should not yet require:

```text
full encryption implementation
public-key infrastructure
server verification
GitHub API integration
automatic forum posting
complex binary packaging
```

---

## 13. Open Questions

Questions for the next design pass:

```text
Should the private return code be generated by the carried run, by the package, or by both?
Should the return artifact be parsed from the human-readable text block directly?
Should there also be an internal JSON representation behind the text block?
How long should the private return code be?
How should copy/paste errors be detected?
Should package_id and layer_id be human-readable, random, or both?
How should the system distinguish private human trace from public trace word?
Which fields become cryptographically relevant later?
```

---

## 14. Working Formulas

```text
The Return Artifact itself is never the forum post.
```

```text
The private artifact travels backward.
The public trace may appear only after safety has been checked.
```

```text
Human-readable outside.
Private payload inside.
Public-safe trace separate.
```

```text
The return artifact may open the layer.
The public trace only says that the answer arrived.
```

```text
C brings the answer back.
B opens the layer.
Only then may the public trace appear.
```
