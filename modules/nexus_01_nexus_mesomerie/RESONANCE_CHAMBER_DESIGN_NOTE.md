# Resonance Chamber Design Note

Status date: 2026-07-13

This note records the current design direction for the playable Resonance Chamber in Nexus 01.

## Core idea

The Resonance Chamber should support three related play processes:

```text
1. Imprint
   A first player shapes a trace with intention.

2. Response
   A later player encounters that trace and answers it.

3. Return opening
   The returned artifact is matched to a waiting local slot and opened into a local result.
```

Working formula:

```text
The first player leaves an unfinished pattern.
The second player does not decode it.
The second player answers it.
```

## Why the Chamber needs more than atmosphere

The player should understand, in a condensed and poetic way, what the Chamber is asking them to do.

The Chamber should not produce a random token from unexplained aesthetic choices.

Instead, it should invite deliberate choices:

```text
This chamber does not ask you to leave a message.
It asks you to shape a trace
that another person may one day answer.

Choose with intention.
What you leave here will not tell them what to feel.
It will give them something to meet.
```

The response path should likewise make its role clear:

```text
Someone shaped this trace with intention.

You are not asked to guess what they meant.
You are invited to notice what it awakens in you
and to answer from your own position.
```

## Personal meaning without private disclosure

The trace should be shaped by personal meaning, but it should not expose the reason behind that meaning.

A useful boundary is:

```text
Private meaning shapes the trace.
The trace does not expose the private meaning.
```

The Chamber may ask the first player to hold a private intention while choosing, without storing that intention directly.

Example:

```text
What do you quietly wish for the next person?

Do not explain it.
Do not address them directly.
Leave one word.
```

The one-word answer may become the most open and personal part of the trace.

## Sensory trace direction

The current preferred direction is a multisensory trace rather than a purely symbolic token.

Possible trace elements:

```text
image
sound
texture
scent
movement
wish_word
```

The Chamber may describe this as:

```text
Leave a trace that can be seen,
heard,
felt,
followed,
and named.
```

Scent is especially useful as a poetic memory image.

Example:

```text
the forest after gentle summer rain
```

## Curated choice and free input

Not every trace element should require free creative writing.

A promising balance is:

```text
image      -> curated poetic choice
sound      -> curated poetic choice
texture    -> curated poetic choice
scent      -> curated poetic choice
movement   -> curated poetic choice
wish_word  -> free input, exactly one word
```

This keeps the Chamber accessible and testable while preserving one strong point of personal authorship.

The Chamber should frame curated choices intentionally:

```text
Do not choose what looks best.
Choose what you would be willing
to place in another person's path.
```

## Short identifiers and poetic display text

Curated elements should have two layers:

```text
short stable id
poetic player-facing text
```

Example:

```json
{
  "id": "summer-rain",
  "text": "the forest after gentle summer rain"
}
```

The stable ID is useful for mechanics, tests, and compact artifacts.
The poetic text preserves atmosphere and can be shown again in the Response path.

This pattern may be used across curated sensory elements:

```json
{
  "image": {
    "id": "lantern",
    "text": "a lantern waiting in the dark"
  },
  "sound": {
    "id": "distant-rain",
    "text": "rain heard through an open window"
  },
  "scent": {
    "id": "summer-rain",
    "text": "the forest after gentle summer rain"
  }
}
```

## Imprint path

In Imprint mode, the first player should not feel that they are filling in token fields.

They should feel that they are shaping an unfinished sensory pattern.

Possible sequence:

```text
choose an image to carry
choose a sound to accompany it
choose a texture to leave beneath the hand
choose a scent to remain in the room
choose a movement to begin
leave one wish word
```

The resulting token should carry playable traces, not a finished answer.

Working formula:

```text
A token does not carry the answer.
It carries what the next player may answer.
```

## Response path

In Response mode, the second player should encounter the Imprint elements as traces in the room rather than raw data fields.

Examples:

```text
A lantern appears in the glass.
What image answers it?
```

```text
The chamber carries the scent
of a forest after gentle summer rain.

Do not guess why it was chosen.
What scent answers it?
```

```text
A movement has already begun.
How does it continue?
```

The response should create a relation between the original trace and the answering trace.

```text
carried trace
+
player response
=
return expression
```

## Return opening

The Return opening is not another creative sequence.

It is the precise local recognition of a returned artifact:

```text
Return Artifact
-> waiting Return Slot
-> Local Result
```

This step may feel ritual-like, but its mechanics should remain calm, clear, and reliable.

## Current implementation boundary

The technical chain already works:

```text
Resonance Token
-> Chamber Expression
-> Return Artifact
-> Slot Matching
-> Local Result
```

What remains is to design the playable Imprint and Response sequences that create these values through meaningful interaction.

## Next design slice

The next useful design task is to define:

```text
1. the first curated option sets
2. the exact Imprint prompts
3. the exact Response prompts
4. which trace elements remain short IDs
5. which poetic texts appear in the Return Artifact
6. how the Chamber help changes during progress
```

## Working formulas

```text
The Chamber offers the material.
The player gives the choice meaning.
```

```text
Private meaning may create structure.
Structure must not expose private meaning.
```

```text
The first player leaves a sensory trace with intention.
The second player does not decode it.
The second player answers it.
```
