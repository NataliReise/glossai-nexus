# Return Unlock Layer Map

A modular responsibility map for the planned return unlock extension.

Document status: early architecture note  
Project: glossAI Nexus  
Module line: Nexus 01 - Nexus-Mesomerie  
Related prototype: Nexus 0.1 - First Spark  
Related architecture note: [Nexus Modularity Rules](NEXUS_MODULARITY_RULES.md)  
Related design notes:

- [Return Unlock Design](RETURN_UNLOCK_DESIGN.md)
- [Return Artifact MVP](RETURN_ARTIFACT_MVP.md)

---

## 1. Purpose

This document maps the planned return unlock extension into separate conceptual layers.

The goal is to keep Nexus 01 modular while larger features grow around First Spark.

Core modularity rule:

```text
The spark must remain small.
The Nexus may grow around it.
```

The return unlock should extend First Spark, but it should not make First Spark dependent on the whole return system.

Working formula:

```text
First Spark is complete on its own.
Return Unlock extends it, but does not redefine it.
```

---

## 2. Layer Overview

The planned return unlock flow can be split into these conceptual layers:

```text
first_spark
activation
gift_package
resonance_artifact
return_artifact
return_unlock
crypto_layer
public_trace
community_bridge
```

These are conceptual layers.

They do not all need to become folders or Python packages immediately.

They define responsibility boundaries.

---

## 3. first_spark

### Responsibility

`first_spark` is the small playable terminal prototype.

It should remain playable without return unlock.

It may provide:

```text
neutral play
private activation play
after-play message
optional public project invitation
optional resonance-node draft command
clean exit behavior
```

### Should not own

`first_spark` should not own:

```text
full return artifact parsing
encryption implementation
private return-layer generation
public forum posting
GitHub API integration
package-building workflow
```

### Modularity check

```text
Can First Spark still be played if the return unlock layer does not exist?
```

Expected answer:

```text
yes
```

---

## 4. activation

### Responsibility

`activation` describes how a run is locally configured.

It may support:

```text
neutral activation
personal activation
gift activation
resonance activation
```

A resonance activation may carry an incoming resonance artifact when a spark is passed onward.

### Should not own

`activation` should not own:

```text
private gift package transfer
return artifact generation
decryption or crypto details
public-safe trace publishing
```

### Boundary rule

```text
Activation configures a run.
It does not become the whole social chain.
```

---

## 5. gift_package

### Responsibility

`gift_package` is the private wrapper around a public module.

It may include:

```text
private activation
recipient instructions
optional gift note
optional resonance artifact
optional future return-layer material
```

It coordinates what is privately given from one person to another.

### Should not own

`gift_package` should not own:

```text
runtime gameplay
decryption logic
public forum trace generation
GitHub workflow
```

### Boundary rule

```text
The public module stays neutral.
The gift is created by a private wrapper.
```

---

## 6. resonance_artifact

### Responsibility

A `resonance_artifact` travels forward.

It marks that a spark may continue.

It may be embedded in a later private resonance activation.

It may be symbolic, structured, or both.

### Should not own

A resonance artifact should not contain:

```text
private gift text
return key material
encrypted return layer content
public forum post text
```

### Boundary rule

```text
Resonance Artifact travels forward.
Return Artifact travels backward.
```

---

## 7. return_artifact

### Responsibility

A `return_artifact` travels backward.

It is privately returned from the carried recipient to the previous giver.

In the first full private chain:

```text
B gives to C.
C returns to B.
```

The return artifact may help B unlock a deeper local return layer.

For the first proposed text shape, see:

- [Return Artifact MVP](RETURN_ARTIFACT_MVP.md)

### May contain or derive

```text
safe identifiers
carrier phrase
private human trace
private return code
future key material
future integrity information
optional public-safe trace suggestion or preview
```

### Must not be

```text
a forum post
a public proof object
a public resonance node
a public-safe return trace
```

### Boundary rule

```text
The Return Artifact itself is never the forum post.
```

---

## 8. return_unlock

### Responsibility

`return_unlock` handles the local moment when B uses the returned artifact to open a deeper layer.

It may later handle:

```text
reading or receiving the return artifact
checking package_id and layer_id
showing friendly mismatch errors
calling crypto_layer for decryption
assembling the return revelation
creating or offering a public-safe return trace draft
```

### Should not own

`return_unlock` should not own:

```text
low-level encryption implementation
GitHub Discussion posting
private gift package creation
core First Spark completion
```

### Boundary rule

```text
Return Unlock extends First Spark.
It does not redefine First Spark completion.
```

---

## 9. crypto_layer

### Responsibility

`crypto_layer` is the isolated technical layer for future encryption work.

If implemented, it should use established libraries or tools.

It may later handle:

```text
KDF choice
authenticated symmetric encryption
decryption verification
salt and nonce handling
safe error categories
example encrypted layer format
```

### Should not own

`crypto_layer` should not own:

```text
poetic text generation
public-safe trace wording
gift package semantics
GitHub Discussion behavior
player-facing narrative decisions
```

### Boundary rule

```text
No custom cryptography as a security promise.
```

and:

```text
Security must not depend on the code being secret.
It may only depend on the key material being private.
```

---

## 10. public_trace

### Responsibility

`public_trace` creates or formats public-safe text that may be shared by consent.

It may later handle:

```text
resonance node draft
carrier trace draft
return trace draft
public-safe phrase generation
public alias fields
public note fields
consent text
privacy warnings
```

### Should not own

`public_trace` should not receive or expose:

```text
private activation data
private gift text
return artifact
private return code
return key
key material
raw seed
encrypted layer content
private relationship context
```

### Boundary rule

```text
The public trace shows only that the answer arrived.
```

For return unlock:

```text
C brings the answer back.
B opens the layer.
Only then may the public trace appear.
```

---

## 11. community_bridge

### Responsibility

`community_bridge` may later help players find public spaces.

It may point to:

```text
public Git repository
wiki
GitHub Discussions
contribution guide
public-safe resonance node category
```

### Should not own

`community_bridge` should not become required infrastructure.

It should not carry private sparks or private return artifacts.

It should not require automatic online behavior.

### Boundary rule

```text
The forum does not carry the spark.
It only records voluntary public traces of sparks that have already travelled privately.
```

---

## 12. Suggested Return Unlock Flow by Layer

A modular return unlock flow could look like this:

```text
1. first_spark completes a playable run for B.
2. resonance_artifact may be offered to B.
3. gift_package or activation helps B pass a spark to C privately.
4. first_spark completes the carried run for C.
5. return_artifact is produced or revealed for B.
6. C privately sends return_artifact to B.
7. return_unlock receives the artifact locally.
8. return_unlock checks safe identifiers.
9. crypto_layer may decrypt the prepared return layer.
10. return_unlock assembles the private return revelation.
11. public_trace may generate a public-safe return trace draft.
12. community_bridge may point to a public place where that trace can be shared manually.
```

No step should require automatic online networking.

---

## 13. Data Boundary Map

### Private data may exist in

```text
private activation
gift package
return artifact
private return code
encrypted return layer
local unlock input
```

### Public-safe data may exist in

```text
public repository
neutral demo data
safe example activation
resonance node draft
carrier trace draft
return trace draft
wiki/discussion guidance
```

### Must not cross into public trace

```text
private activation data
private gift text
return artifact
private return code
return key
key material
raw seed
encrypted layer content
private relationship context
```

---

## 14. Failure Boundaries

Each layer should fail gently and locally.

Examples:

```text
first_spark:
  can finish without return unlock

activation:
  can fall back to neutral or show a friendly activation error

return_artifact:
  can show copy/paste or completeness guidance

return_unlock:
  can say the artifact does not match this layer

crypto_layer:
  can return a safe failure category without leaking sensitive details

public_trace:
  can refuse to create a trace if private material is detected or unclear

community_bridge:
  can show links manually without needing API access
```

---

## 15. Open Questions

Questions for the next architecture pass:

```text
Should these conceptual layers later become Python packages, folders, or only documentation boundaries?
Where should return_unlock live if First Spark remains small?
Should public_trace be a shared helper used by resonance nodes and return traces?
How should return_artifact parsing be separated from return_unlock?
Where should friendly failure messages live?
How much of this belongs in First Spark 0.2, and how much should wait for Nexus 01 MVP?
```

---

## 16. Working Formulas

```text
The spark must remain small.
The Nexus may grow around it.
```

```text
Optional layer, not hidden dependency.
```

```text
First Spark is complete on its own.
Return Unlock extends it, but does not redefine it.
```

```text
Resonance Artifact travels forward.
Return Artifact travels backward.
```

```text
The Return Artifact itself is never the forum post.
```

```text
Private material travels privately.
Public trace appears only by consent.
```

```text
Extension points, not entanglement.
```
