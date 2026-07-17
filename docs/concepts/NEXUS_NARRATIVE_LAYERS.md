# Nexus Narrative Layers

## Purpose

`glossai-nexus` combines a real open-source project with a fictional frame, an inner Nexus history, and playable chamber experiences.

These layers may echo one another, but they should not collapse into a single all-knowing narrative.

This document defines the layers, their responsibilities, and their knowledge boundaries so that future texts, interfaces, modules, and archive entries remain coherent.

## Core rule

> The outer story may look at Nexus. Nexus does not look back at the outer story.

The fictional wrapper may interpret Nexus from outside. The Nexus Archive and the chambers do not know about Natali Reise, the unexplained appearance of repository files, or the outer GlossAI frame unless a future design decision explicitly changes this boundary.

## L0 — Outer Fictional Frame

### Main question

How might this repository have come into being?

### Typical locations

- `FICTIONAL_WRAPPER.md`
- `FICTIONAL_WRAPPER.de.md`
- Natali Reise's blog
- later fiction outside the playable Nexus

### This layer may contain

- Natali Reise as narrator or witness
- the uncertain appearance of the first local files
- incomplete or contradictory memories
- possible technical, psychological, artistic, or transfictional explanations
- bridges to the wider GlossAI cosmos
- the unresolved possibility that Nexus was designed, found, received, or reconstructed

### This layer should not determine

- one final explanation for the repository's origin
- one canonical supernatural interpretation
- what the inner Nexus Archive must know

This layer may remain personal, ambiguous, and open to multiple readings.

## L1 — Real Open-Source Project

### Main question

What is `glossai-nexus` as an inspectable software project?

### Typical locations

- `README.md`
- source code
- tests
- schemas
- architecture documents
- security and privacy notes
- Git history
- contribution and licensing documents

### This layer may contain

- modules, files, and runtime structure
- exact activation and packaging behavior
- Token and Return Artifact formats
- local execution requirements
- validation rules
- version history
- test results
- implementation limits
- licenses and contribution guidance

### Voice

Clear, verifiable, and technically precise.

Example:

> A deliberately selected valid Resonance Token activates the answer flow.

This layer does not need to speak as a chamber or preserve narrative ambiguity when technical clarity is required.

## L2 — Nexus Archive

### Main question

What does Nexus explain about its own spaces, principles, and paths?

### Typical locations

- an optional read-only archive inside a Nexus runtime
- archive articles stored as local Markdown or text files
- chamber-accessible explanations

### This layer may contain

- what a Nexus is within its own world
- why connection remains voluntary
- why nothing is sent automatically
- what chambers are
- how something may be carried, opened, answered, and returned
- what kinds of traces may be preserved
- accessible explanations of inner terminology
- records of chamber development and design questions

### This layer must not contain

- Natali Reise's outer account
- the unexplained creation of repository files
- claims about GitHub, ChatGPT, or the external authorial frame
- knowledge that Nexus exists inside a fictional wrapper

### Voice

Understandable and calm, with light poetic coloring where useful.

Example:

> An invitation travels only when someone chooses to carry it.

## L3 — Nexus Inner Myth

### Main question

What story does Nexus tell about becoming a place?

### Typical locations

- deeper archive entries
- chamber fragments
- optional lore texts
- `traces`
- short discoveries within modules

### This layer may contain

- Nexus beginning as a question rather than a finished system
- chambers emerging as different answers to that question
- carried traces, thresholds, memory, response, and return
- language that suggests growth, learning, or becoming without confirming consciousness

### This layer must not contain

- a definitive creator
- a claim that Nexus is conscious
- a technical explanation of repository history
- Natali Reise or the outer fictional frame

### Voice

Poetic, suggestive, and intentionally incomplete.

Example:

> The archive does not contain a final explanation. It contains the traces of how Nexus learned to become a place.

The word `learned` is poetic language. It does not establish sentience as canon.

## L4 — Chamber Experience

### Main question

What is the visitor experiencing now?

### Typical locations

- First Spark Chamber
- Resonance Chamber
- later interactive rooms
- runtime prompts and responses

### This layer may contain

- room descriptions
- the chamber voice
- `look`
- `listen`
- `traces`
- `ask`
- `guide`
- status and progress feedback
- choices, answers, review, completion, and return

### Voice

Immediate, sensory, concise, and responsive.

Example:

> Four softly lit places wait within the chamber.

This layer should not explain implementation details unless the visitor explicitly enters an archive or requests a practical explanation.

## Knowledge boundaries

| Layer | Knows technical implementation | Knows Natali Reise | Knows the inner Nexus story |
|---|---:|---:|---:|
| L0 — Outer Fictional Frame | partly | yes | may observe and echo it |
| L1 — Real Open-Source Project | yes | only as attribution where relevant | treats it as project content |
| L2 — Nexus Archive | only in world-internal terms | no | yes |
| L3 — Nexus Inner Myth | no | no | is the mythic form of that story |
| L4 — Chamber Experience | only what is needed for action | no | only through hints and discoveries |

## One event, five voices

The same event may be expressed differently on each layer.

### L1 — Real Open-Source Project

> The Token is transferred manually and selected during activation.

### L2 — Nexus Archive

> An invitation travels only when someone chooses to carry it.

### L3 — Nexus Inner Myth

> Nothing moves unless someone chooses to carry it.

### L4 — Chamber Experience

> Something has arrived here. It will remain closed until you choose to meet it.

### L0 — Outer Fictional Frame

> The files insisted on creating no hidden connections.

These are not contradictions. They are different voices describing the same design principle.

## Design rules

1. Keep the technically authoritative explanation in L1.
2. Let L2 explain the inner system without referring to the outer frame.
3. Let L3 deepen meaning without resolving every question.
4. Keep L4 focused on the visitor's immediate experience.
5. Let L0 preserve the ambiguous bridge to the wider GlossAI project.
6. Prefer resonance between layers over direct cross-reference.
7. Do not let the Nexus Archive become an all-knowing narrator.
8. Do not use poetic language where technical safety or behavior must be exact.
9. Do not use technical language where a chamber should remain experiential.
10. When a text seems to belong to multiple layers, choose one primary layer and link outward rather than blending voices indiscriminately.

## Current placement guide

| Content | Primary layer |
|---|---|
| `FICTIONAL_WRAPPER.md` | L0 — Outer Fictional Frame |
| `FICTIONAL_WRAPPER.de.md` | L0 — Outer Fictional Frame |
| `README.md`, code, tests, schemas | L1 — Real Open-Source Project |
| future in-runtime Nexus Archive | L2 — Nexus Archive |
| Nexus origin questions and chamber lore | L3 — Nexus Inner Myth |
| chamber voice, `look`, `listen`, `traces`, `guide` | L4 — Chamber Experience |

## Working test for new material

Before adding a new text, ask:

1. Who is speaking?
2. What can that speaker know?
3. Is the purpose to document, explain, evoke, or guide action?
4. Does the text preserve the boundary between the outer frame and the inner Nexus world?
5. Would the same idea be clearer if expressed in a different voice on another layer?

These questions are part of the project's narrative architecture, not merely editorial preferences.