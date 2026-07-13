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

## Personal meaning without private disclosure

The trace should be shaped by personal meaning, but it should not expose the reason behind that meaning.

```text
Private meaning shapes the trace.
The trace does not expose the private meaning.
```

The Chamber may ask the first player to hold a private intention while choosing, without storing that intention directly.

## Resonance Chamber V0.1

The first playable version currently focuses on four trace elements:

```text
image
scent
movement
wish_word
```

Image, scent, and movement use curated poetic choices. The wish word remains the only free input.

Sound and texture remain possible later extensions, but are not required for V0.1.

## Imprint entrance

The Imprint path should explain the action clearly without sounding like a form.

```text
This chamber does not ask you to leave a message.

It asks you to shape a trace
that another person may one day answer.

Choose with intention.

What you leave here will not tell them what to feel.
It will give them something to meet.
```

## Image imprint

Prompt:

```text
Choose an image you are willing
to place in another person's path.

Do not search for the perfect one.

Choose the one that feels right,
or simply speaks to you most.
```

Current curated choices:

```json
[
  {
    "id": "waiting-lantern",
    "text": "a lantern waiting in the dark"
  },
  {
    "id": "open-starry-window",
    "text": "an open window into a starry night"
  },
  {
    "id": "stone-in-water",
    "text": "a small, artfully painted wishing stone resting beneath clear water"
  },
  {
    "id": "book-bench",
    "text": "an empty bench beneath an old tree, with a book waiting for its next reader"
  },
  {
    "id": "bridge-in-mist",
    "text": "a narrow bridge connecting two unseen shores in the mist"
  }
]
```

Design reading:

```text
The light waits.
The window opens into distance.
The wishing stone rests beneath the surface.
The bench offers a place and leaves something to be continued.
The bridge connects what cannot yet be seen.
```

## Scent imprint

Prompt:

```text
Which scent would you place in another person's path?

Choose the one that should remain
after everything else has become quiet.
```

The scent entries should carry not only smell, but also place and atmosphere where useful.

Current curated choices:

```json
[
  {
    "id": "summer-rain",
    "text": "the scent of a forest after gentle summer rain"
  },
  {
    "id": "warm-bread",
    "text": "the scent of warm bread in a quiet, welcoming kitchen"
  },
  {
    "id": "first-snow",
    "text": "the scent of cold air before the first snow along a mountain path"
  },
  {
    "id": "books-and-cedar",
    "text": "the scent of old books and cedar wood in a softly lit library"
  },
  {
    "id": "evening-salt",
    "text": "the scent of salt air along a quiet beach in the evening sun"
  }
]
```

The entries do not need to follow exactly the same sentence shape. The important criterion is that each gives enough spatial ground for a later response.

## Movement imprint

Prompt:

```text
A movement can begin without showing where it ends.

Which movement would you leave unfinished
for another person to encounter?
```

Current curated choices:

```json
[
  {
    "id": "opening-circle",
    "text": "a circle slowly opening"
  },
  {
    "id": "falling-feather",
    "text": "a feather turning as it falls"
  },
  {
    "id": "returning-tide",
    "text": "a tide beginning to return"
  },
  {
    "id": "loosening-knot",
    "text": "a knot slowly loosening"
  },
  {
    "id": "crossing-light",
    "text": "a line of light moving across the floor"
  }
]
```

Movement qualities:

```text
opening
drifting
returning
releasing
passing
```

They should remain ambiguous and not force one emotional reading.

## Wish word

Prompt:

```text
What do you quietly wish for the next person?

Do not explain it.
Do not address them directly.

Leave one word.
```

Follow-up line:

```text
The chamber keeps the word,
but not the reason behind it.
```

Suggested constraints for V0.1:

```text
1-24 characters
letters from the supported alphabet
one optional internal hyphen
no spaces
no contact details
```

Player-facing guidance:

```text
Please leave a quality, state, or possibility,
not a person's name.
```

Examples should appear only in optional help, because they may influence the player's choice:

```text
courage
rest
clarity
belonging
wonder
self-trust
```

## Short identifiers and poetic display text

Curated elements should retain both layers:

```text
short stable id
poetic player-facing text
```

Example:

```json
{
  "id": "summer-rain",
  "text": "the scent of a forest after gentle summer rain"
}
```

The stable ID supports mechanics, matching, and tests. The poetic text supports play and the Return Artifact.

A possible Imprint payload:

```json
{
  "image": {
    "id": "open-starry-window",
    "text": "an open window into a starry night"
  },
  "scent": {
    "id": "summer-rain",
    "text": "the scent of a forest after gentle summer rain"
  },
  "movement": {
    "id": "opening-circle",
    "text": "a circle slowly opening"
  },
  "wish_word": "courage"
}
```

## Response entrance

The Response path should make clear that another person has already been present through the trace.

Preferred text:

```text
Someone has been here before you

and left a trace in this chamber,
placing it in your path.

It does not ask for a solution.
It is not a riddle to solve.

It invites you to answer
in your own voice.
```

This gives the Chamber a simple history:

```text
presence in the past
trace in the present
response in the future
```

## Response principle

The second player should not replace the original trace with a new object of the same category.

The stronger direction is associative response:

```text
The trace remains.
The response lets something arise from it.
```

The answer may become an image, feeling, mood, memory-like scene, movement, possibility, or something difficult to name.

Each trace element may have its own response grammar:

```text
image
-> what appears, shifts, or becomes possible around it

scent
-> what rises with it or how its scene continues

movement
-> how it continues, changes, or is met

wish word
-> what one word returns
```

This avoids a purely symmetrical pattern such as image answering image or scent answering scent.

## Image response direction

The earlier idea of simply placing a second image beside the first remains possible, but the stronger design direction is now an answering association.

Possible prompt:

```text
This image was left in your path.

Do not explain it.

What begins to appear around it?
```

The response should not decode the original image. It should extend, shift, or open it.

Examples of the response principle:

```text
a lantern waiting in the dark
-> the feeling of being expected
```

```text
an open window into a starry night
-> a room becoming larger than its walls
```

```text
a wishing stone resting beneath clear water
-> a promise resting beneath the surface
```

The actual curated Image response set still needs to be designed.

## Scent response direction

The preferred response is not necessarily another scent.

Instead, the carried scent scene may receive a poetic continuation:

```text
carried scent scene
+
chosen continuation
=
answered scent trace
```

Example:

```text
the scent of salt air along a quiet beach in the evening sun,
with two trails of footprints running side by side
```

### Universal scent continuations

The following currently work across all scent scenes:

```json
[
  {
    "id": "possibility-of-encounter",
    "text": "carrying the possibility of encounter"
  },
  {
    "id": "edge-of-beginning",
    "text": "at the edge of something beginning"
  },
  {
    "id": "sense-of-return",
    "text": "carrying a sense of return"
  },
  {
    "id": "inviting-stillness",
    "text": "inviting stillness"
  }
]
```

### Scene-compatible scent continuations

Some concrete continuations work only with compatible scenes.

Landscape-compatible examples:

```text
along a well-loved path
with two trails of footprints running side by side
```

These work naturally with forest, mountain, and beach scenes, but not with kitchen or library scenes.

Kitchen-compatible encounter image:

```text
with a second place quietly waiting at the table
```

Library-compatible encounter image:

```text
with two books left open beside one another
```

This leads to a two-layer response structure:

```text
universal continuations
+
scene-compatible continuations
```

The Chamber should remain consistent without forcing every scene into the same spatial grammar.

## Movement response direction

The movement should not merely be replaced by a second movement.

The answer may continue it, alter it, meet it, or create a counter-movement.

Working prompt:

```text
A movement has already begun.

How would you let it continue?
```

The actual curated Movement response set still needs to be designed.

## Return word

Possible prompt:

```text
One word was left in your path.

What one word would you leave in return?
```

The return word does not need to be a synonym, opposite, or explanation. It should represent the second player's own position.

## Return Artifact

The strongest current direction is to preserve the fullest poetic form of each carried trace and its response.

```text
original trace
+
answering association
```

The Return Artifact should therefore not be optimized for maximum brevity.

Example shape:

```text
A lantern waiting in the dark

and what began to appear around it:

the feeling of being expected


The scent of a forest after gentle summer rain,

with two trails of footprints running side by side


A circle slowly opening,

met by a tide beginning to return


One word was left:

courage

One word returned:

trust
```

The internal artifact should still retain short IDs for mechanics and tests:

```json
{
  "carrier": {
    "image_id": "waiting-lantern",
    "scent_id": "summer-rain",
    "movement_id": "opening-circle",
    "wish_word": "courage"
  },
  "response": {
    "image_association_id": "being-expected",
    "scent_continuation_id": "side-by-side-footprints",
    "movement_response_id": "returning-tide",
    "return_word": "trust"
  }
}
```

Separation of concerns:

```text
IDs
-> mechanics, matching, tests

poetic texts
-> playable Return Artifact
```

The Return Artifact is the place where the trace may take on its fullest shared form.

## Return opening

The Return opening is not another creative sequence.

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

The current implementation does not yet reflect all of the design decisions in this note. In particular, the existing `ResonanceExpression` and Return Artifact writer use an earlier field set and will need deliberate evolution after the playable sequence is stabilized.

## Next design slice

The next useful design tasks are:

```text
1. design the first curated Image association responses
2. design the first curated Movement responses
3. refine the universal and scene-compatible Scent continuations
4. run full example paths through Imprint and Response
5. decide the exact Return Artifact wording for each category
6. map the final playable structure onto a versioned token and artifact schema
7. update tests only after the play grammar is stable
```

## Working formulas

```text
The Chamber offers the material.
The first player gives the trace meaning.
The second player gives it resonance.
```

```text
A trace is placed in another person's path.
It is not decoded.
It is encountered.

The answer does not solve it.
It continues it.
```

```text
Private meaning may create structure.
Structure must not expose private meaning.
```

```text
The first player leaves a sensory trace with intention.
The second player does not decode it.
The second player lets something arise from it.
```
