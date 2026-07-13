# Resonance Composition and Poem V0.1

Status date: 2026-07-13

This note defines the first bridge between the playable Resonance Chamber and the poem generator.

It builds on:

```text
RESONANCE_CHAMBER_DESIGN_NOTE.md
RESONANCE_RESPONSE_SETS_V01.md
```

The purpose of this note is not yet to specify implementation details. It establishes a neutral shared composition, a small manual test corpus, and one restrained poem form for V0.1.

## Core sequence

```text
player choices
-> Resonance Composition
-> poem rendering
-> Return Artifact
```

The poem is not the composition itself. It is one poetic rendering of the composition.

The structured composition should remain available alongside the rendered poem.

## Design boundary

The generator should not invent hidden meaning, psychological explanation, or symbolic interpretation.

It may:

```text
order
connect
inflect
punctuate
line-break
lightly transform grammar
```

It should not:

```text
decode
explain
moralise
assign intention
add symbols that were not chosen
```

Working principle:

```text
The players create the relation.
The generator gives the relation a readable poetic form.
```

## Neutral Resonance Composition

The first shared intermediate form contains the carried trace and the answering response for each category.

```json
{
  "version": "0.1",
  "image": {
    "carried": {
      "id": "waiting-lantern",
      "text": "a lantern waiting in the dark"
    },
    "response": {
      "id": "appearing-path",
      "text": "a path beginning to appear"
    }
  },
  "scent": {
    "carried": {
      "id": "summer-rain",
      "text": "the scent of a forest after gentle summer rain"
    },
    "response": {
      "id": "possibility-of-encounter",
      "text": "carrying the possibility of encounter"
    }
  },
  "movement": {
    "carried": {
      "id": "falling-feather",
      "text": "a feather turning as it falls"
    },
    "response": {
      "id": "crossing-feather",
      "text": "another feather crossing its path",
      "relation": "meet"
    }
  },
  "words": {
    "carried": "courage",
    "returned": "trust"
  }
}
```

## Data layers under review

The manual tests should help decide whether the implementation needs two or three textual layers.

Possible three-layer model:

```text
stable id
source text
render-ready text
```

Example:

```json
{
  "id": "waiting-lantern",
  "source_text": "a lantern waiting in the dark",
  "render_text": "A lantern waits in the dark."
}
```

A two-layer model may be sufficient if the poem renderer can apply a small, explicit set of safe grammatical transformations.

No free generative paraphrasing is required for V0.1.

## Poem form V0.1

The first poem form should remain calm, legible, and close to the selected material.

```text
[image carried, grammatically inflected]

Around it,
[image response, grammatically inflected]

[scent carried]
[scent response]

[movement carried, grammatically inflected]
[movement response, grammatically inflected]

[carried word] was left here.
[returned word] answered.
```

The stanza structure is intentionally visible:

```text
image relation

scent relation

movement relation

word relation
```

This keeps the joint authorship readable and prevents the renderer from blending all elements into an opaque new text.

## Manual test corpus

The following five compositions are intentionally different. They are not canonical story outcomes. They are test cases for grammar, rhythm, openness, and combinability.

---

## Example 1 - A clear meeting

### Composition

```json
{
  "version": "0.1",
  "image": {
    "carried": {
      "id": "waiting-lantern",
      "text": "a lantern waiting in the dark"
    },
    "response": {
      "id": "appearing-path",
      "text": "a path beginning to appear"
    }
  },
  "scent": {
    "carried": {
      "id": "summer-rain",
      "text": "the scent of a forest after gentle summer rain"
    },
    "response": {
      "id": "possibility-of-encounter",
      "text": "carrying the possibility of encounter"
    }
  },
  "movement": {
    "carried": {
      "id": "falling-feather",
      "text": "a feather turning as it falls"
    },
    "response": {
      "id": "crossing-feather",
      "text": "another feather crossing its path",
      "relation": "meet"
    }
  },
  "words": {
    "carried": "courage",
    "returned": "trust"
  }
}
```

### Poem rendering

```text
A lantern waits in the dark.

Around it,
a path begins to appear.

The scent of a forest
after gentle summer rain
carries the possibility of encounter.

A feather turns as it falls.
Another feather crosses its path.

Courage was left here.
Trust answered.
```

### Initial observation

This is the easiest case. All four relations remain clear without additional connective language.

---

## Example 2 - A quiet interior

### Composition

```json
{
  "version": "0.1",
  "image": {
    "carried": {
      "id": "book-bench",
      "text": "an empty bench beneath an old tree, with a book waiting for its next reader"
    },
    "response": {
      "id": "two-voices-one-page",
      "text": "the possibility of two voices meeting on the same page"
    }
  },
  "scent": {
    "carried": {
      "id": "books-and-cedar",
      "text": "the scent of old books and cedar wood in a softly lit library"
    },
    "response": {
      "id": "open-books-beside-one-another",
      "text": "with two books left open beside one another"
    }
  },
  "movement": {
    "carried": {
      "id": "loosening-knot",
      "text": "a knot slowly loosening"
    },
    "response": {
      "id": "gathering-without-tightening",
      "text": "a hand gathering the threads without tightening them",
      "relation": "counter"
    }
  },
  "words": {
    "carried": "belonging",
    "returned": "welcome"
  }
}
```

### Poem rendering

```text
An empty bench waits beneath an old tree,
with a book for its next reader.

Around it,
appears the possibility
of two voices meeting on the same page.

The scent of old books and cedar wood
in a softly lit library,
with two books left open beside one another.

A knot slowly loosens.
A hand gathers the threads
without tightening them.

Belonging was left here.
Welcome answered.
```

### Initial observation

The image response is a noun phrase, not an action. The fixed line `Around it,` therefore needs more than one rendering pattern.

Possible controlled variants:

```text
Around it,
[response as verbal clause]
```

```text
Around it,
appears [response as noun phrase]
```

The scent pair also shows that some continuations are best preserved as one sentence fragment rather than forced into a finite sentence.

---

## Example 3 - Distance and return

### Composition

```json
{
  "version": "0.1",
  "image": {
    "carried": {
      "id": "open-starry-window",
      "text": "an open window into a starry night"
    },
    "response": {
      "id": "answering-distant-light",
      "text": "a distant light seeming to answer"
    }
  },
  "scent": {
    "carried": {
      "id": "evening-salt",
      "text": "the scent of salt air along a quiet beach in the evening sun"
    },
    "response": {
      "id": "sense-of-return",
      "text": "carrying a sense of return"
    }
  },
  "movement": {
    "carried": {
      "id": "returning-tide",
      "text": "a tide beginning to return"
    },
    "response": {
      "id": "stream-back-to-sea",
      "text": "a narrow stream flowing back toward the sea",
      "relation": "counter"
    }
  },
  "words": {
    "carried": "wonder",
    "returned": "return"
  }
}
```

### Poem rendering

```text
A window opens into a starry night.

Around it,
a distant light seems to answer.

The scent of salt air
along a quiet beach in the evening sun
carries a sense of return.

A tide begins to return.
A narrow stream flows back toward the sea.

Wonder was left here.
Return answered.
```

### Initial observation

The repetition of `return` is not grammatically wrong, but it may feel too deliberate when the movement, scent response, and returned word all carry the same root.

V0.1 should not silently replace a player's word. Repetition should therefore be accepted unless a separate player-facing composition warning is later designed.

---

## Example 4 - Playful transformation

### Composition

```json
{
  "version": "0.1",
  "image": {
    "carried": {
      "id": "stone-in-water",
      "text": "a small, artfully painted wishing stone resting beneath clear water"
    },
    "response": {
      "id": "colours-carried-outward",
      "text": "a ripple carrying its colours outward"
    }
  },
  "scent": {
    "carried": {
      "id": "first-snow",
      "text": "the scent of cold air before the first snow along a mountain path"
    },
    "response": {
      "id": "edge-of-beginning",
      "text": "at the edge of something beginning"
    }
  },
  "movement": {
    "carried": {
      "id": "opening-circle",
      "text": "a circle slowly opening"
    },
    "response": {
      "id": "playful-waves",
      "text": "the open edges beginning to curl into two playful waves",
      "relation": "continue"
    }
  },
  "words": {
    "carried": "curiosity",
    "returned": "play"
  }
}
```

### Poem rendering

```text
A small, artfully painted wishing stone
rests beneath clear water.

Around it,
a ripple carries its colours outward.

The scent of cold air before the first snow
along a mountain path,
at the edge of something beginning.

A circle slowly opens.
Its edges begin to curl
into two playful waves.

Curiosity was left here.
Play answered.
```

### Initial observation

This example shows why render-ready text may be useful. The movement response contains `the open edges`, which refers directly to the carried movement. In the poem, a controlled pronoun transformation to `Its edges` reads more naturally.

This should be an explicit rendering rule, not a free paraphrase.

---

## Example 5 - Shared silence and counter-movement

### Composition

```json
{
  "version": "0.1",
  "image": {
    "carried": {
      "id": "bridge-in-mist",
      "text": "a narrow bridge connecting two unseen shores in the mist"
    },
    "response": {
      "id": "shared-silence",
      "text": "a silence becoming shared"
    }
  },
  "scent": {
    "carried": {
      "id": "warm-bread",
      "text": "the scent of warm bread in a quiet, welcoming kitchen"
    },
    "response": {
      "id": "second-place-at-table",
      "text": "with a second place quietly waiting at the table"
    }
  },
  "movement": {
    "carried": {
      "id": "crossing-light",
      "text": "a line of light moving across the floor"
    },
    "response": {
      "id": "shadow-alongside",
      "text": "a shadow moving alongside it",
      "relation": "counter"
    }
  },
  "words": {
    "carried": "rest",
    "returned": "presence"
  }
}
```

### Poem rendering

```text
A narrow bridge connects
 two unseen shores in the mist.

Around it,
a silence becomes shared.

The scent of warm bread
in a quiet, welcoming kitchen,
with a second place quietly waiting at the table.

A line of light moves across the floor.
A shadow moves alongside it.

Rest was left here.
Presence answered.
```

### Initial observation

The image and scent create different physical settings. This is acceptable because the composition is not required to form one literal scene.

The poem renderer should not force spatial unity where the players did not create it.

The line break before `two unseen shores` must not contain a leading space in implementation.

## First grammar findings

The manual examples suggest at least four controlled transformations.

### 1. Participial source text to finite sentence

```text
a lantern waiting in the dark
-> A lantern waits in the dark.
```

```text
a feather turning as it falls
-> A feather turns as it falls.
```

### 2. Response participle to finite clause

```text
a path beginning to appear
-> a path begins to appear.
```

```text
a distant light seeming to answer
-> a distant light seems to answer.
```

### 3. Context-dependent reference adjustment

```text
the open edges beginning to curl into two playful waves
-> Its edges begin to curl into two playful waves.
```

This transformation depends on the carried movement and should therefore be stored or encoded explicitly.

### 4. Noun-phrase image responses

Some image responses are not naturally rendered after `Around it,` without a small frame.

Example:

```text
the possibility of two voices meeting on the same page
```

Possible controlled rendering:

```text
Around it,
appears the possibility
of two voices meeting on the same page.
```

Alternative future solution:

```text
What appears around it is
[response noun phrase].
```

The first V0.1 renderer may need a response-shape field such as:

```json
{
  "shape": "verbal_participle"
}
```

or:

```json
{
  "shape": "noun_phrase"
}
```

## First structural findings

### The composition should retain source text

The original selected wording belongs to the players' shared trace and should not be lost after rendering.

### The poem should retain category boundaries

V0.1 should keep image, scent, movement, and words visibly separate.

### Repetition is not automatically an error

The renderer should not replace a player's word merely to improve style.

### Spatial inconsistency is not automatically an error

The four elements may create a constellation rather than one continuous literal scene.

### The renderer needs controlled grammar, not unrestricted generation

A small rule-based renderer remains the preferred V0.1 direction.

## Candidate Return Artifact structure

```json
{
  "artifact_version": "0.1",
  "composition": {
    "image": {},
    "scent": {},
    "movement": {},
    "words": {}
  },
  "rendering": {
    "form_id": "trace-poem-v01",
    "language": "en",
    "text": "..."
  }
}
```

This preserves the distinction:

```text
composition
-> shared structured relation

rendering
-> poetic surface
```

## Open questions after the first corpus

```text
1. Do curated choices need explicit render_text values?
2. Is a response-shape field sufficient for image associations?
3. Should scent continuations remain fragments in the poem?
4. Should movement relation labels affect connective wording?
5. Should word repetition be shown without intervention in all cases?
6. Does the poem form need one optional introductory or closing line?
7. Which exact text belongs in the Return Artifact outside the poem?
```

## Recommended next step

Review the five example poems manually and revise only the rendering grammar.

After the poem form is stable enough:

```text
1. define the versioned Resonance Composition schema
2. add render metadata to curated response sets where needed
3. implement a deterministic poem renderer
4. test every curated response at least once
5. evolve the Return Artifact writer without breaking the existing matching chain
```

Working formula:

```text
The trace is chosen.
The response creates relation.
The composition preserves it.
The poem lets it be heard.
```
