# Return Unlock Design

How a carried spark returns as an unlockable hidden layer.

Document status: early design draft  
Project: glossAI Nexus  
Module line: Nexus 01 - Nexus-Mesomerie  
Related prototype: Nexus 0.1 - First Spark

---

## 1. Purpose

This document describes the planned return unlock mechanism for Nexus 01.

The return unlock is the moment when a privately returned artifact opens a deeper local return layer.

It grows out of the current First Spark prototype, but it is not part of the current First Spark 0.1 implementation yet.

For the modular responsibility map behind this extension, see:

- [Return Unlock Layer Map](RETURN_UNLOCK_LAYER_MAP.md)

The design goal is to connect:

```text
private resonance chain
return artifact
local unlock
encrypted return layer
human trace
public-safe return trace
```

The return unlock should remain:

```text
local-first
private by default
human-mediated
public-safe only by consent
understandable without server infrastructure
```

Core idea:

```text
The private return opens the layer.
The public trace shows only that the answer arrived.
```

---

## 2. Resonance Chain Context

The larger Nexus 01 resonance chain is not only a direct return from B to A.

The working pattern is:

```text
A gives to B.
B may give to C.
C may return to B.
B may unlock a deeper layer.
```

This means:

```text
A starts the first spark.
B receives it.
B may carry it onward.
C may answer.
B may receive the first deeper return.
```

The first complete private resonance chain for MVP Nexus 01 may therefore look like:

```text
A -> B -> C -> B
```

The origin giver A may begin the trace, but A does not need to be the first person who receives a return unlock.

The first deeper return experience may happen one generation later, when B passes the spark onward to C and receives a return artifact back.

---

## 3. Core Artifact Roles

Nexus 01 should distinguish clearly between different artifact types.

### 3.1 Resonance Artifact

A resonance artifact travels forward.

It may be created or revealed after a completed run.

It can be carried into a later private activation.

It may mark that a spark has travelled.

It may be embedded in a private resonance activation.

It should not contain private gift text.

Example placeholder:

```text
N01-RA-MIRROR-BOUNDARY-7KQ2
```

### 3.2 Return Artifact

A return artifact travels backward.

It is created or revealed after a carried run.

It is privately returned to the previous giver.

It may allow the previous giver to unlock a deeper local return layer.

It may contain or derive key material.

It must not be posted publicly.

For the first proposed player-facing return artifact shape, see:

- [Return Artifact MVP](RETURN_ARTIFACT_MVP.md)

Example placeholder:

```text
N01-RETURN-LANTERN-courage-827
```

### 3.3 Resonance Node Draft

A resonance node draft is public-safe.

It does not unlock gameplay.

It is not a private activation.

It is not a return artifact.

It is an optional visible trace that may be posted publicly by consent.

It should only show that a spark was seen, completed, carried, or returned in a public-safe way.

### 3.4 Public-Safe Return Trace

A public-safe return trace may be shown after a successful return unlock.

It is not the return artifact.

It is not key material.

It cannot unlock anything.

It may be shared publicly only if the people involved choose to share it.

It should show only that a return layer opened, not what private content it revealed.

Working distinction:

```text
Resonance Artifact travels forward.
Return Artifact travels backward.
Resonance Node stays public-safe.
Return Trace shows only that the answer arrived.
```

---

## 4. Minimal Return Unlock Flow

The minimal return unlock flow should remain small.

```text
1. B prepares or receives a private return layer.
2. B gives a resonance activation to C.
3. C plays the carried activation.
4. C receives a return artifact.
5. C privately returns it to B.
6. B enters or places it locally.
7. The deeper return layer opens.
```

More detailed MVP version:

```text
1. B prepares or receives a private resonance package for C.
2. The package contains:
   - public First Spark module or public repository link
   - private resonance activation for C
   - encrypted return layer for B
   - short recipient instructions
3. B gives the package to C through a private channel.
4. C plays the carried activation.
5. During or near the end of the run, C makes one or more guided choices.
6. C enters one resonance word or short guided response.
7. The system combines:
   - package/layer context,
   - carried resonance artifact,
   - C's guided choices,
   - C's resonance word,
   - optional locally generated random material.
8. C receives a return artifact.
9. C sends the return artifact back to B through a private channel.
10. B opens First Spark or a later return command.
11. B enters the return artifact.
12. The system checks package/layer/artifact compatibility.
13. The system derives or reconstructs the symmetric unlock key.
14. If valid, the encrypted return layer opens.
15. If invalid, a friendly error explains what to check.
```

---

## 5. Symmetric Encryption Idea

The return layer may be encrypted with a symmetric encryption mechanism.

Basic idea:

```text
encrypted return layer
+ matching return artifact
= local unlock
```

Or more explicitly:

```text
Return Artifact
-> key material
-> encrypted return layer
-> local unlock
```

The encrypted return layer may already exist locally.

However, it should not be readable without the matching return artifact.

This creates a clear dramatic structure:

```text
The layer is present.
But it waits for return.
```

Poetic formulation:

```text
The answer was already hidden in the artifact,
but it became readable only through resonance.
```

The unlock should happen locally.

It should not require:

```text
server infrastructure
user accounts
GitHub API
automatic online verification
database access
```

---

## 6. Security Boundary

Nexus should not invent its own cryptography.

Core rule:

```text
No custom cryptography as a security promise.
```

If real encryption is implemented later, it should use an established library or tool.

Possible technical directions:

```text
authenticated symmetric encryption
AEAD
AES-GCM
ChaCha20-Poly1305
XChaCha20-Poly1305
Fernet as a higher-level interface
```

Possible later Python-related tools:

```text
cryptography
PyNaCl
age as an external tool
```

The exact technical choice is not part of this design draft yet.

The specification should remain honest about its boundary:

```text
This is a local privacy mechanism, not a high-security communication system.
```

Or:

```text
This is a local protection and play mechanism, not a replacement for professional end-to-end security.
```

Open-source security rule:

```text
Security must not depend on the code being secret.
It may only depend on the key material being private.
```

---

## 7. Key Derivation

If the return artifact or return key is entered by a human, it should not automatically be treated as a raw cryptographic key.

A cleaner later approach would be:

```text
Return Artifact / Return Key / Passphrase
-> Key Derivation Function
-> symmetric decryption key
```

Relevant technical concepts:

```text
KDF
salt
nonce
iterations
memory cost
```

Possible logic:

```text
return_artifact_from_C
+ salt_from_encrypted_layer
+ package/layer context
-> derived key
-> decrypt encrypted_return_layer
```

A future `encrypted_return_layer.json` might include metadata such as:

```json
{
  "version": "N01-ERL-1",
  "algorithm": "chosen-aead-method",
  "kdf": "chosen-key-derivation-method",
  "salt": "...",
  "nonce": "...",
  "ciphertext": "...",
  "package_id": "...",
  "layer_id": "..."
}
```

This is not a final file format.

It is only a design anchor.

---

## 8. Human Unpredictability Component

The return unlock should not be fully predictable from public code alone.

If a second run produces a result that is completely deterministic from public source code, a technically skilled person could simulate the return without a meaningful human trace.

Therefore, a carried run should include at least one real human contribution.

Working formula:

```text
The return key is not only generated by the program.
It is completed by a human trace.
```

Poetic formulation:

```text
A key may be calculated.
But a return must be spoken.
```

Or:

```text
A word must return before the layer becomes readable.
```

### 8.1 Guided Human Input

A fully open text field may be risky for MVP 01.

It may produce input that is:

```text
too long
too short
too private
too random
hard to integrate
hard to explain
```

A better first version may use a semi-guided mini-narrative.

Example:

```text
C chooses:
- What did the trace find beyond the boundary?
  -> a locked lantern

C chooses:
- What did the trace carry back?
  -> a promise

C enters one resonance word:
  -> courage
```

Generated line:

```text
The trace returned with a locked lantern.
It did not bring a solution.
It carried a promise: courage.
```

The choices and resonance word may shape the return artifact.

They may also participate in key derivation.

However, the cryptographic strength should not rely on a short poetic word alone.

### 8.2 Combined Key Material

A stronger design may combine:

```text
1. Origin or previous-giver component
   e.g. resonance artifact, origin secret, package id, layer salt

2. Carried-run component
   e.g. guided choices during C's run

3. Human component
   e.g. resonance word, alias, or short guided answer

4. Technical random component
   e.g. locally generated strong random material

5. Package/layer context
   e.g. package_id, layer_id, module_id
```

Possible design formula:

```text
origin component
+ carried run choices
+ human resonance word
+ random key material
+ package/layer context
-> KDF
-> symmetric unlock key
```

The human input shapes the return.

The cryptographic strength should come from strong random material and sound key derivation.

---

## 9. Generated Return Revelation

The return layer does not need to be only a static encrypted text.

It may combine:

```text
fixed encrypted private core
prepared fragments
guided choices from the carried run
human resonance word
deterministic generation seed
```

This creates a generated return revelation.

The return revelation is what B sees after a successful unlock.

It may feel partly surprising or responsive, while remaining reproducible when the same return artifact is entered again.

Important distinction:

```text
Encrypted Return Layer
= protected private core

Generated Return Revelation
= revealed output after unlock, possibly shaped by return artifact and guided choices

Public-Safe Return Trace
= harmless optional public note that only says the answer arrived
```

### 9.1 Deterministic Randomness

If the return revelation uses randomness, it should probably not use fresh randomness every time the layer opens.

Otherwise, reopening the same return layer might show a different answer each time.

A better approach is deterministic generation:

```text
Return Artifact + Layer ID + Salt + guided choices
-> seed
-> select prepared fragments
```

This makes the result:

```text
unpredictable before return
reproducible after return
local
testable
```

Possible generated elements:

```text
symbol: lantern / mirror / river / owl / gate
tone: quiet / luminous / playful / solemn
line: one of several prepared return lines
public-safe phrase: one harmless return trace
```

---

## 10. Public-Safe Return Trace

After a successful return unlock, the system may show an optional public-safe return trace.

This trace is a reward, but it must remain safe.

It should not be called proof in a strict technical or social sense unless carefully framed.

Better names:

```text
public-safe return trace
return witness phrase
visible return trace
public completion phrase
```

The return trace may say:

```text
A return layer was opened.
A spark returned.
An answer arrived.
```

It must not reveal:

```text
private activation data
private gift message
return artifact
return key
encrypted layer content
raw seed
key material
personal relationship context
```

Possible draft:

```text
Return Trace: N01-RT-draft
Module: Nexus 01 - First Spark
Status: return layer opened
Trace visibility: public-safe summary only
Public phrase: The lantern answered through the river.

Consent:
We choose to share this public trace.
No private activation data, gift text, return artifact, key material, or encrypted layer content is included.
```

Core distinction:

```text
Public reward != Return Artifact
Public reward != key material
Public reward != encrypted private content
```

The public-safe trace shows only that the answer arrived.

---

## 11. Reward for Both Participants

The return unlock may offer a reward to both participants, but the rewards should remain role-sensitive.

### 11.1 Reward for B

B is the person who receives the return artifact and opens the deeper layer.

B may receive:

```text
private return revelation
public-safe return trace draft
```

B should see the deeper private layer.

B may optionally share only the public-safe trace.

### 11.2 Reward for C

C is the person who carried the spark and returned the artifact.

C may receive a different reward, such as:

```text
You have returned a spark.
If the previous giver opens it, a deeper layer may answer.
```

C may also receive a public-safe carrier trace.

Example:

```text
Carrier Trace:
A spark was carried and returned.
```

C should not automatically see B's private return layer if that layer is meant for B.

This preserves the role structure.

---

## 12. Package ID and Layer ID

To avoid confusing failures, return artifacts and encrypted layers should be linkable by safe identifiers.

Possible identifiers:

```text
module_id
package_id
layer_id
run_id
```

The return artifact may show which package or layer it belongs to.

The encrypted return layer may contain the same ID.

The system can first check:

```text
Does this return artifact seem to belong to this layer?
```

If not, it can show a friendly error before or instead of a low-level decryption failure.

Example:

```text
This return artifact does not seem to belong to this Nexus layer.

Please check:
- Did you enter the complete return artifact?
- Does it belong to this gift package?
- Was the package changed after the artifact was created?
```

---

## 13. Friendly Failure

Errors should remain gentle and understandable.

A failed return unlock should not look like a Python crash or a cryptographic wall of text.

Possible message:

```text
Return artifact could not unlock this layer.

Please check:
- Did you enter the complete return artifact?
- Does it belong to this gift package?
- Was the package changed after the artifact was created?
```

The message should:

```text
avoid blame
avoid leaking sensitive details
help with copy/paste errors
help with wrong package/layer confusion
remain calm
```

---

## 14. Public / Private Boundaries

The public/private boundary remains central.

### Public Repository May Contain

```text
public source code
neutral demo data
safe example activation
documentation
test data without private meaning
encrypted_return_layer.example.json
safe demo ciphertext
placeholder return artifacts
```

### Public Repository Must Not Contain

```text
real private activation
real gift message
real recipient data
real return artifact
real return key
real encrypted return layer for a real person
real key material
private relationship context
```

Important rule:

```text
A real encrypted return layer does not automatically belong in public Git just because it is encrypted.
```

Encryption reduces readability.

It does not turn private material into public documentation.

### Public Forum May Contain

```text
public-safe resonance node
public-safe return trace
public alias
public note
consent marker
statement that no private data is included
```

### Public Forum Must Not Contain

```text
private activation data
private gift messages
return artifacts
return keys
encrypted return layers
key material
raw seeds
private relationship context
```

Core formula:

```text
The spark travels privately.
The network may become visible publicly.
```

---

## 15. MVP Scope

For MVP Nexus 01, this design may specify or prepare:

```text
return artifact concept
encrypted return layer concept
local return unlock concept
human unpredictability component
generated return revelation concept
public-safe return trace concept
privacy boundaries
friendly failure behavior
possible file format direction
possible key derivation direction
```

---

## 16. Out of Scope for Now

This design should not yet require:

```text
full package generator
GitHub API integration
automatic GitHub Discussion posting
contact matching
Hall of Resonance workflow
server infrastructure
database
user accounts
graphical interface
complex cryptographic protocol
AI-generated live responses
automatic public proof
```

A complete implementation is also out of scope for this document.

This document should stabilize the concept before code is written.

---

## 17. Open Questions

Important questions for the next design pass:

```text
Who creates the encrypted return layer?
Does the previous giver know the layer content before unlock?
Is the layer fully encrypted, partly generated, or both?
How much of the revelation is fixed?
How much is generated from the return artifact?
How human-readable should the return artifact be?
Should the return artifact be a text phrase, structured text block, or JSON?
Which established encryption library or tool should be used later?
How much random key material is needed?
How is the human resonance word included without weakening security?
Does C receive a separate reward?
What exactly may be shared as public-safe return trace?
Should the public trace be generated at B's unlock stage, C's return stage, or both?
```

---

## 18. Current Design Decisions

This section records design decisions that have become stable enough to guide the next planning step.

They may still be refined later, but they should be treated as the current working direction.

### Decision 01: Return layer structure and public-safe rewards

The private return message should be prepared and encrypted.

It should be similar to the current after-play messages in spirit: a deliberately written message that waits inside the Nexus or private package.

It should not be generated from scratch by the return artifact.

The return artifact unlocks the prepared message.

The human trace may shape how the prepared message appears.

Working formula:

```text
The message is prepared.
The return unlocks it.
The human trace colors its revelation.
The public trace may be generated.
```

This means the return layer may combine:

```text
prepared encrypted private message
+ generated return frame
+ optional public-safe generated trace
```

B receives the private return revelation after a successful unlock.

B may also receive an optional public-safe return trace.

C should not automatically see B's private return layer if that layer is meant for B.

C may receive a separate carrier reward after returning the artifact.

C may also receive an optional public-safe carrier trace.

Public-safe traces may include:

```text
module id
public status
generated public-safe phrase
public aliases
public note
consent marker
statement that no private data is included
```

Public-safe traces must never include:

```text
return artifact
return key
key material
raw seed
encrypted layer content
private return message
private gift text
private activation data
private relationship context
```

A public-safe carrier trace may appear at C's return stage.

The main public-safe return trace should appear at B's unlock stage, after the return artifact has successfully opened the private return layer.

---

## 19. Working Formulas

```text
The private return opens the layer.
The public trace shows only that the answer arrived.
```

```text
Resonance Artifact travels forward.
Return Artifact travels backward.
Resonance Node stays public-safe.
```

```text
Return Artifact -> symmetric key material -> encrypted return layer -> local unlock.
```

```text
A key may be calculated.
But a return must be spoken.
```

```text
A word must return before the layer becomes readable.
```

```text
The layer is present.
But it waits for return.
```

```text
The answer was already hidden in the artifact,
but it became readable only through resonance.
```

```text
Public reward != Return Artifact.
Public reward != key material.
Public reward != encrypted private content.
```

```text
The spark travels privately.
The network may become visible publicly.
```

```text
No private return travels through the public forum.
Only light may be seen there.
```
