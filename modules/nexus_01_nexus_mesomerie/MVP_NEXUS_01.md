# Nexus 01 - MVP Specification

Working title: **Nexus 01 - Nexus-Mesomerie**  
Project: **glossAI Nexus**  
Document status: Refocused working specification  
Suggested file name: `MVP_NEXUS_01.md`

---

## 1. Purpose

**Nexus 01 - Nexus-Mesomerie** is the first larger playable target state of the glossAI Nexus project.

It should grow out of the current First Spark prototype without losing the safety and clarity of the public/private boundary.

The MVP should demonstrate this limited but meaningful idea:

> A Nexus is not only played.  
> It can be activated, privately carried onward, answered, and remembered.

This version does not require a server, accounts, automatic networking, or GitHub API integration.

The first Nexus network is human-mediated.

---

## 2. Current Foundation

First Spark already provides:

- a local terminal prototype
- a neutral public fallback
- local private activation support
- safe example activation data
- friendly activation-file errors
- a helper for creating local activation data
- a public handoff checklist
- a private gift package specification

Relevant First Spark documents:

```text
first_spark/README.md
first_spark/LOCAL_ACTIVATION_GUIDE.md
first_spark/PUBLIC_HANDOFF_CHECKLIST.md
first_spark/GIFT_PACKAGE_SPEC.md
```

MVP Nexus 01 should build on this foundation instead of replacing it.

---

## 3. Core Design Principles

Nexus 01 should follow these principles:

- The module structure is open.
- The code is readable.
- The game can be played without reading the code.
- Personal activation content must not be required to be public.
- The public module stays neutral and inspectable.
- The private gift layer stays private.
- The social network created by Nexus is not automatic or digital by default.
- The spark travels from person to person.
- The forum does not carry the spark.
- The forum may only record voluntary public traces of sparks that have already travelled privately.
- Passing on a spark is an invitation, not an obligation.
- A received gift remains complete even if it is never forwarded.

Important guiding formulas:

> The code belongs in the light.  
> The message may remain protected.

> The public module stays neutral.  
> The gift is created by a private wrapper.

> The spark travels from person to person.  
> The forum only shows where light was seen.

---

## 4. MVP Goal

MVP Nexus 01 should define and later support one private human-mediated resonance chain:

```text
A -> B -> C -> B
```

This means:

1. A gives a First Spark gift to B.
2. B plays and receives the gift.
3. B may privately pass a spark onward to C.
4. C plays and returns a response artifact to B.
5. B enters or places the return artifact locally.
6. B unlocks a deeper return layer.

This is the first meaningful resonance chain.

The origin giver A may start the trace, but the first deeper return experience may happen one generation later, when B passes the spark onward to C and receives a return artifact back.

---

## 5. Actors

### 5.1 A - Origin Giver

A creates or chooses the first private gift activation.

A gives B:

- the public module or a link to it
- a private gift package
- optional start instructions

In the first real project use case, A may be the project creator.

A does not need to be the first person who receives a return unlock.

### 5.2 B - First Recipient / Next Giver

B receives and plays the First Spark gift.

At the end, B may receive:

- the gift message
- an invitation to pass a spark onward
- a link to the public Git repository
- a resonance artifact
- optionally a locally generated resonance node draft

B may stop here.

The gift remains complete even if B never passes it onward.

If B chooses to continue the trace, B creates or chooses a private First Spark activation for C.

### 5.3 C - Next Recipient / Return Sender

C receives and plays the First Spark gift or resonance activation from B.

At the end, C may receive:

- a final message, either neutral or gift-based
- an invitation to pass a spark onward
- a link to the public Git repository
- a new resonance artifact
- a return artifact for B
- optionally a locally generated resonance node draft

C may privately send the return artifact back to B.

### 5.4 Later Participants

Later participants may repeat the same pattern:

```text
B -> C -> D -> C
C -> D -> E -> D
D -> E -> F -> E
```

Longer chains may emerge socially, but MVP 01 only needs to specify and support the first full private chain.

---

## 6. Core Private Resonance Flow

### Step 1: Origin Gift

A creates or chooses a First Spark gift activation for B.

A privately gives B:

- the public module or a link to it
- a private gift package
- optional start instructions

### Step 2: Gift Play

B installs or opens First Spark locally.

B plays the activated First Spark.

At the end, B receives:

- the gift message
- a public Git/project invitation
- an invitation to pass a Nexus spark onward
- a resonance artifact

Optional message idea:

```text
You may keep this spark as a completed gift.
If you want, you may also let it travel further.
```

### Step 3: Private Pass-On

B may create or choose a First Spark activation for C.

B privately gives C:

- the public module or a link to it
- a private gift package
- optional start instructions
- the resonance artifact, either separately or embedded in the activation

This may be called a `resonance_activation` if the activation carries an incoming resonance artifact.

### Step 4: Carried Gift Play

C plays the activated First Spark locally.

At the end, C receives:

- the final message, either neutral or gift-based
- a public Git/project invitation
- an invitation to pass a Nexus spark onward
- a new resonance artifact
- a return artifact for B

### Step 5: Private Return

C privately gives the return artifact back to B.

The return artifact is not posted publicly.

It may be:

- a short text phrase
- a structured text block
- a local JSON file
- another simple locally transferable artifact

MVP 01 should prefer a simple human-readable text form unless a file becomes clearly necessary.

### Step 6: Return Unlock

B places or enters the return artifact locally.

B unlocks a deeper return layer.

The return layer may reveal:

- a second message
- a deeper lore fragment
- a reflection about the trace
- a poetic answer connecting B's gift and C's response

---

## 7. Voluntary Pass-On Rule

Passing on a spark must remain voluntary.

A Nexus gift must never become a chain letter, obligation, or growth hack.

The game may invite continuation, but it must not pressure the player.

Suggested rule text:

```text
Passing on a spark is an invitation, not an obligation.
A received gift remains complete even if it is never forwarded.
```

Anti-chain-letter boundary:

```text
Nexus does not demand continuation.
It offers a trace that may be carried onward.
```

---

## 8. Artifact Terms

MVP 01 should prefer the word `artifact` over `token` unless a more technical implementation requires token language.

Reason:

- `token` may sound like a secret, permission object, access credential, or security-sensitive value.
- `artifact` can mean a portable symbolic result without implying secrecy or authorization.

### 8.1 Resonance Artifact

A resonance artifact travels forward.

It marks that a spark may continue.

It may be embedded in a private activation for the next recipient.

It should not contain private gift text.

It may be human-readable.

Example placeholder format:

```text
N01-RA-MIRROR-BOUNDARY-7KQ2
```

### 8.2 Return Artifact

A return artifact travels backward.

It is created or revealed after a carried gift run.

It allows the previous giver to unlock a deeper return layer.

It should be privately returned to the previous giver.

Example placeholder format:

```text
N01-RETURN-LANTERN-courage-827
```

### 8.3 Resonance Node Draft

A resonance node draft is not an activation artifact.

It is not used to unlock gameplay.

It is a public-safe local text draft that a player may optionally post in a GitHub Discussion or other public project space to help make the spread of Nexus visible.

---

## 9. Activation Types

### 9.1 Neutral Activation

A neutral activation is playable without private gift content.

It is suitable for:

- public demo play
- testing
- lore exploration
- general First Spark access

### 9.2 Gift Activation

A gift activation is a private activation for a specific person, group, occasion, or relationship context.

It may contain:

- recipient alias
- occasion
- tone
- private message
- optional gift instruction

It must not be committed to the public repository.

### 9.3 Resonance Activation

A resonance activation is a private activation that also carries an incoming resonance artifact.

It is used when B passes the spark onward to C.

It may contain:

- recipient alias
- private gift message
- incoming resonance artifact
- optional instructions for return

It must not be committed to the public repository.

---

## 10. Forum / GitHub Discussion Role

GitHub Discussions are not part of the private handoff path in MVP 01.

The forum does not carry:

- private activations
- private gift messages
- private resonance activations
- private return artifacts
- personal contact data
- private relationship context

The forum may later help make the spread of Nexus visible through voluntary public resonance nodes.

Core rule:

```text
The forum does not carry the spark.
It only records voluntary public traces of sparks that have already travelled privately.
```

Poetic rule:

```text
The spark travels from person to person.
The forum only shows where light was seen.
```

---

## 11. Resonance Nodes

A resonance node is a voluntary public trace.

It may be posted after a player has completed a run.

It should help make the growing Nexus network visible without exposing private data.

A resonance node should not contain:

- private activation data
- private gift text
- private return artifacts
- email addresses
- phone numbers
- real names unless intentionally shared
- sensitive information
- instructions that pressure others to continue the chain

A resonance node may contain:

- module id
- module name
- public run type
- completion marker
- optional public alias
- optional public note
- consent marker
- statement that no private activation data is included

Possible local draft format:

```text
Resonance Node: N01-RN-0001
Module: Nexus 01 - First Spark
Run type: private gift / neutral / carried spark
Status: completed
Trace visibility: public-safe summary only
Forwarded: optional / yes / no / not shared
Return: optional / received / not shared
Public alias:
Public note:
Consent: I choose to share this public trace. No private activation data, gift text, or return artifact is included.
```

This draft may be copied manually into a GitHub Discussion.

No automatic posting is part of MVP 01.

---

## 12. Public Git Invitation

At the end of a run, First Spark may show a short public project invitation.

This message should invite the player to:

- visit the public Git repository
- inspect or fork the project
- read the documentation
- optionally post a public-safe resonance node draft
- optionally pass the spark onward privately

It must not pressure the player.

Suggested tone:

```text
This First Spark can end here.
If you want, you may visit the public project, read how it works, or leave a public-safe resonance node to show that a spark was seen.
No private message or activation data should be posted publicly.
```

---

## 13. Local Draft Generation

MVP 01 may later generate local text drafts.

Possible drafts:

- `resonance_node_draft.md`
- `recipient_start_note.md`
- `return_artifact_note.txt`

For the current MVP specification, only the resonance node draft is relevant as a public-facing optional after-play artifact.

A generated resonance node draft must be public-safe by design.

It should include an explicit privacy reminder.

---

## 14. In Scope for MVP 01

MVP 01 should specify or prepare:

- local terminal play
- neutral play
- private gift activation
- private resonance activation
- private pass-on flow from B to C
- private return artifact flow from C back to B
- local return unlock for B
- resonance artifact concept
- return artifact concept
- optional public Git/project invitation
- optional local resonance node draft
- documentation of the public/private boundary
- no automatic online behavior

---

## 15. Out of Scope for MVP 01

MVP 01 should not include:

- automatic online networking
- GitHub API integration
- automatic GitHub Discussion posting
- GitHub Discussions as a token or artifact transfer channel
- public matching between strangers
- public exchange of private activations
- public exchange of private return artifacts
- user accounts
- server infrastructure
- database
- moderation system
- full Hall of Resonance workflow
- advanced cryptographic protocol design
- AI-generated live responses
- graphical interface
- dependency-heavy packaging

---

## 16. Later Extensions

Possible later extensions:

- GitHub Discussion templates for resonance nodes
- Hall of Resonance contribution workflow
- public-safe resonance map
- optional contact nodes for people seeking resonance partners
- longer resonance chains
- multiple return layers
- encrypted return layers
- browser-based version
- module templates
- module creation guide
- additional Nexus modules
- cooperative two-person puzzle modes
- Git history as optional puzzle layer
- translations
- accessibility improvements
- workshop activations
- learning-context activations

Contact nodes may be reconsidered later, but they are not part of the first private resonance-chain MVP.

---

## 17. MVP Success Criteria

The MVP direction is successful if:

1. First Spark remains publicly shareable in neutral form.
2. A private gift package can activate First Spark for B.
3. B can complete the gift without any obligation to continue.
4. B can optionally pass a spark onward to C through a private channel.
5. C can complete the carried gift or resonance activation.
6. C can produce or receive a return artifact for B.
7. B can enter or place the return artifact locally.
8. B can unlock a deeper return layer.
9. The public repository never contains private activation data.
10. The forum is used only for optional public-safe resonance traces, not private transfer.
11. Any generated resonance node draft is safe to post publicly.
12. The project remains understandable without server infrastructure.

---

## 18. Working Formula

Public module:

```text
clean code + neutral fallback + safe example activation
```

Private gift package:

```text
private activation + recipient instructions + private transfer
```

Private resonance chain:

```text
A gives to B.
B may give to C.
C may return to B.
B may unlock a deeper layer.
```

Public resonance node:

```text
public-safe trace that a spark was seen
```

Core formula:

> The spark travels privately.  
> The network may become visible publicly.  
> The gift remains complete even if the trace stops.
