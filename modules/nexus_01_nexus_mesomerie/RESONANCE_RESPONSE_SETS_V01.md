# Resonance Response Sets V0.1

Status date: 2026-07-13

This note records the curated Image and Movement response sets for the first playable Resonance Chamber design.

It supplements `RESONANCE_CHAMBER_DESIGN_NOTE.md`.

## Response principle

The second player does not decode or replace the original trace.

```text
The trace remains.
The response lets something arise from it.
```

For Image responses, the player chooses an association that appears, shifts, or becomes possible around the carried image.

For Movement responses, the player chooses a reaction that may continue, meet, transform, or counter the carried movement.

## Image response prompt

```text
This image was left in your path.

Do not explain it.

What begins to appear around it?
```

## Curated Image responses

### A lantern waiting in the dark

```json
{
  "image_id": "waiting-lantern",
  "image_text": "a lantern waiting in the dark",
  "responses": [
    {
      "id": "appearing-path",
      "text": "a path beginning to appear"
    },
    {
      "id": "being-expected",
      "text": "the feeling of being expected"
    },
    {
      "id": "before-arrival",
      "text": "the moment before someone arrives"
    },
    {
      "id": "opening-warmth",
      "text": "a small circle of warmth opening around it"
    }
  ]
}
```

### An open window into a starry night

```json
{
  "image_id": "open-starry-window",
  "image_text": "an open window into a starry night",
  "responses": [
    {
      "id": "quiet-pull-of-distance",
      "text": "the quiet pull of distance"
    },
    {
      "id": "room-beyond-walls",
      "text": "a room becoming larger than its walls"
    },
    {
      "id": "another-world-near",
      "text": "the feeling that another world is near"
    },
    {
      "id": "distant-light-answering",
      "text": "a distant light seeming to answer"
    }
  ]
}
```

### A wishing stone beneath clear water

```json
{
  "image_id": "stone-in-water",
  "image_text": "a small, artfully painted wishing stone resting beneath clear water",
  "responses": [
    {
      "id": "wish-kept-safe",
      "text": "a wish kept safe without being hidden"
    },
    {
      "id": "precious-waiting",
      "text": "something precious waiting to be noticed"
    },
    {
      "id": "colours-carried-outward",
      "text": "a ripple carrying its colours outward"
    },
    {
      "id": "quiet-sign-left",
      "text": "the sense that someone has left a quiet sign"
    }
  ]
}
```

### An empty bench beneath an old tree

```json
{
  "image_id": "book-bench",
  "image_text": "an empty bench beneath an old tree, with a book waiting for its next reader",
  "responses": [
    {
      "id": "room-made",
      "text": "the feeling that someone has just made room"
    },
    {
      "id": "story-continued",
      "text": "a story waiting to be continued"
    },
    {
      "id": "absent-companion",
      "text": "the quiet presence of an absent companion"
    },
    {
      "id": "voices-same-page",
      "text": "the possibility of two voices meeting on the same page"
    }
  ]
}
```

### A narrow bridge between unseen shores

```json
{
  "image_id": "bridge-in-mist",
  "image_text": "a narrow bridge connecting two unseen shores in the mist",
  "responses": [
    {
      "id": "one-more-step",
      "text": "the courage to take one more step"
    },
    {
      "id": "approaching-other-side",
      "text": "the sense that someone may be approaching from the other side"
    },
    {
      "id": "paths-recognising",
      "text": "two distant paths beginning to recognise one another"
    },
    {
      "id": "shared-silence",
      "text": "a silence becoming shared"
    }
  ]
}
```

## Movement response prompt

```text
A movement has already begun.

How would you let it continue?
```

The curated sets deliberately mix different response types:

```text
continue
meet
transform
counter
```

The categories are design aids rather than labels shown to the player.

## Curated Movement responses

### A feather turning as it falls

```json
{
  "movement_id": "falling-feather",
  "movement_text": "a feather turning as it falls",
  "responses": [
    {
      "id": "current-carrying-farther",
      "text": "a current carrying it farther",
      "relation": "continue"
    },
    {
      "id": "another-feather-crossing",
      "text": "another feather crossing its path",
      "relation": "meet"
    },
    {
      "id": "rising-breath-lifting",
      "text": "a rising breath lifting it once more",
      "relation": "transform"
    },
    {
      "id": "still-hand-waiting",
      "text": "a still hand waiting beneath it",
      "relation": "counter"
    }
  ]
}
```

### A circle slowly opening

```json
{
  "movement_id": "opening-circle",
  "movement_text": "a circle slowly opening",
  "responses": [
    {
      "id": "flowing-line-embracing",
      "text": "a flowing line gently embracing the opening circle",
      "relation": "meet"
    },
    {
      "id": "edges-playful-waves",
      "text": "the open edges beginning to curl into two playful waves",
      "relation": "continue"
    },
    {
      "id": "lines-growing-spiral",
      "text": "the two lines unfolding and dancing into an ever-growing spiral",
      "relation": "transform"
    },
    {
      "id": "curved-line-inward",
      "text": "a curved line gently drawing inward",
      "relation": "counter"
    }
  ]
}
```

### A tide beginning to return

```json
{
  "movement_id": "returning-tide",
  "movement_text": "a tide beginning to return",
  "responses": [
    {
      "id": "boat-turning-shore",
      "text": "a small boat turning toward the shore",
      "relation": "meet"
    },
    {
      "id": "water-lively-wave",
      "text": "the returning water gathering into a lively wave",
      "relation": "continue"
    },
    {
      "id": "shells-shifting",
      "text": "a line of shells shifting with the water",
      "relation": "transform"
    },
    {
      "id": "stream-back-to-sea",
      "text": "a narrow stream flowing back toward the sea",
      "relation": "counter"
    }
  ]
}
```

### A knot slowly loosening

```json
{
  "movement_id": "loosening-knot",
  "movement_text": "a knot slowly loosening",
  "responses": [
    {
      "id": "loosened-lines-new-space",
      "text": "two loosened lines beginning to open a new space",
      "relation": "continue"
    },
    {
      "id": "thread-between-strands",
      "text": "another thread slipping gently between the loosened strands",
      "relation": "meet"
    },
    {
      "id": "strands-new-pattern",
      "text": "the loose strands beginning to form a new pattern",
      "relation": "transform"
    },
    {
      "id": "hand-gathering-threads",
      "text": "a hand gathering the threads without tightening them",
      "relation": "counter"
    }
  ]
}
```

### A line of light moving across the floor

```json
{
  "movement_id": "crossing-light",
  "movement_text": "a line of light moving across the floor",
  "responses": [
    {
      "id": "another-beam-crossing",
      "text": "another beam crossing it",
      "relation": "meet"
    },
    {
      "id": "light-climbing-wall",
      "text": "the light climbing slowly up the wall",
      "relation": "continue"
    },
    {
      "id": "autumn-leaves-shimmering",
      "text": "scattered autumn leaves beginning to shimmer in its path",
      "relation": "transform"
    },
    {
      "id": "shadow-alongside",
      "text": "a shadow moving alongside it",
      "relation": "counter"
    }
  ]
}
```

## Design consequences

The Image responses repeatedly allow themes of resonance, encounter, communication, shared space, and continuation to appear without forcing a single interpretation.

The Movement responses remain more abstract. Their meaning arises from the visible relation between movements rather than from explanatory language.

These response sets are now stable enough to serve as input for the next design step:

```text
player choices
-> Resonance Composition
-> poem rendering
-> Return Artifact
```

The poem generator should preserve these relations and rhythmically compose them without assigning meanings that the players did not provide.
