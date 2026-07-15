# Resonance V0.2 Probe Output Series 01

This document records the first reproducible human-review corpus for the isolated `mixed-threshold-return-world` composer prototype.

The series uses fixed seeds and several free-word pairs. It is not production output and does not alter the V0.1 opening path.

## Series design

```text
13 valid runs in total
6 runs with Hope / Spirit
6 runs with deliberately varied or difficult word pairs
1 lexical-identity edge case with Return / Return
```

The corpus was reproduced locally from the current committed block order, weights, route rules, Echo eligibility rules, and deterministic Python random selection.

## Compact distribution

```text
13 distinct long forms
13 distinct Echoes
route A 8 times
route B 2 times
route C 3 times
wish word in Echo line 2: 2 times
wish word in Echo line 3: 8 times
wish word in Echo line 4: 3 times
```

These counts are descriptive only. The sample is too small for statistical conclusions.

---

## Output 01 — seed 3 — `Hope` / `Spirit`

### Resonance Artifact

```text
An open frame lets distance enter
Summer rain softens the threshold

Rain leaves room for Hope
The tide turns back without undoing departure

A narrow current answers from another direction
Two returns hold one interval open

Spirit keeps the shared direction visible
```

### Nexus Echo

```text
Night threshold
one light remains awake
two returns hold one interval open
light keeps Hope visible
Spirit
```

### Composition trace

```text
route       route.field-atmosphere-wish-movement-response-relation-remainder
blocks      field.frame.02
            atmosphere.rain.01
            wish.rain-room.03
            movement.departure.03
            response.current.01
            relation.interval.01
            remainder.direction.03
gains       answering approach continuation held-open-relation mobility openness orientation reciprocity room visibility
echo trace  two returns hold one interval open
wish line   4
```

---

## Output 02 — seed 7 — `Hope` / `Spirit`

### Resonance Artifact

```text
An open frame lets distance enter
Summer rain softens the threshold

Hope crosses the open frame
Returning water folds the shore inward

Another current bends seaward through the dark
Two returns hold one interval open

Spirit remains where the passage stays open
```

### Nexus Echo

```text
Open distance
Hope crosses wet glass
two returns hold one interval open
the passage stays open
Spirit
```

### Composition trace

```text
route       route.field-atmosphere-wish-movement-response-relation-remainder
blocks      field.frame.02
            atmosphere.rain.01
            wish.frame.01
            movement.shore.02
            response.seaward.03
            relation.interval.01
            remainder.passage.01
gains       approach continuation held-open-relation mobility openness orientation
echo trace  two returns hold one interval open
wish line   2
```

---

## Output 03 — seed 19 — `Hope` / `Spirit`

### Resonance Artifact

```text
An open frame lets distance enter
Rain leaves a silver trace across the floor

Hope waits where distance begins to answer
The tide turns back without undoing departure

A narrow current answers from another direction
Distance begins to answer without closing

Spirit keeps the shared direction visible
```

### Nexus Echo

```text
Scattered roads
one light remains awake
Hope returns without undoing its path
distance begins to answer
Spirit
```

### Composition trace

```text
route       route.field-atmosphere-wish-movement-response-relation-remainder
blocks      field.frame.02
            atmosphere.trace.02
            wish.distance.02
            movement.departure.03
            response.current.01
            relation.distance.04
            remainder.direction.03
gains       answering approach continuation held-open-relation mobility openness orientation possibility reciprocity visibility
echo trace  distance begins to answer
wish line   3
```

---

## Output 04 — seed 23 — `Hope` / `Spirit`

### Resonance Artifact

```text
The window keeps two directions visible
Hope follows the light beyond the glass

Summer rain softens the threshold
The tide turns back without undoing departure

A stream returns by its own path
Their separate currents share one direction

Spirit remains where the passage stays open
```

### Nexus Echo

```text
Night threshold
one light remains awake
Hope returns without undoing its path
the passage stays open
Spirit
```

### Composition trace

```text
route       route.field-wish-atmosphere-movement-response-relation-remainder
blocks      field.window.03
            wish.light.04
            atmosphere.rain.01
            movement.departure.03
            response.path.02
            relation.direction.02
            remainder.passage.01
gains       approach continuation gentle-connection mobility openness orientation visibility
echo trace  the passage stays open
wish line   3
```

---

## Output 05 — seed 47 — `Blue` / `Hush`

### Resonance Artifact

```text
At the open edge of night
Summer rain softens the threshold

Blue follows the light beyond the glass
Returning water folds the shore inward

A stream returns by its own path
Distance begins to answer without closing

Hush keeps the shared direction visible
```

### Nexus Echo

```text
Rain window
one light remains awake
Blue follows waters toward one shore
distance begins to answer
Hush
```

### Composition trace

```text
route       route.field-atmosphere-wish-movement-response-relation-remainder
blocks      field.threshold.01
            atmosphere.rain.01
            wish.light.04
            movement.shore.02
            response.path.02
            relation.distance.04
            remainder.direction.03
gains       answering approach continuation held-open-relation orientation visibility
echo trace  distance begins to answer
wish line   3
```

---

## Output 06 — seed 53 — `Perhaps` / `Return`

### Resonance Artifact

```text
At the open edge of night
Perhaps crosses the open frame

Summer rain softens the threshold
The tide turns back without undoing departure

A stream returns by its own path
Their separate currents share one direction

Return remains where the passage stays open
```

### Nexus Echo

```text
Open distance
rain softens every boundary
Perhaps returns without undoing its path
the passage stays open
Return
```

### Composition trace

```text
route       route.field-wish-atmosphere-movement-response-relation-remainder
blocks      field.threshold.01
            wish.frame.01
            atmosphere.rain.01
            movement.departure.03
            response.path.02
            relation.direction.02
            remainder.passage.01
gains       continuation gentle-connection mobility openness orientation
echo trace  the passage stays open
wish line   3
```

---

## Output 07 — seed 71 — `Nähe` / `Weite`

### Resonance Artifact

```text
An open frame lets distance enter
Summer rain softens the threshold

Nähe follows the light beyond the glass
The tide turns back without undoing departure

Another current bends seaward through the dark
Two returns hold one interval open

Weite remains where the passage stays open
```

### Nexus Echo

```text
Night threshold
Nähe crosses wet glass
two returns hold one interval open
the passage stays open
Weite
```

### Composition trace

```text
route       route.field-atmosphere-wish-movement-response-relation-remainder
blocks      field.frame.02
            atmosphere.rain.01
            wish.light.04
            movement.departure.03
            response.seaward.03
            relation.interval.01
            remainder.passage.01
gains       approach continuation held-open-relation mobility openness orientation
echo trace  two returns hold one interval open
wish line   2
```

---

## Output 08 — seed 97 — `Return` / `Return`

### Resonance Artifact

```text
The window keeps two directions visible
Summer rain softens the threshold

Return follows the light beyond the glass
The tide turns back without undoing departure

A stream returns by its own path
One shore becomes visible between them

Return remains where the passage stays open
```

### Nexus Echo

```text
Scattered roads
rain softens every boundary
Return returns without undoing its path
the passage stays open
Return
```

### Composition trace

```text
route       route.field-atmosphere-wish-movement-response-relation-remainder
blocks      field.window.03
            atmosphere.rain.01
            wish.light.04
            movement.departure.03
            response.path.02
            relation.shore.03
            remainder.passage.01
gains       approach continuation mobility openness orientation visibility
echo trace  the passage stays open
wish line   3
```

---

## First cross-series observations

### Strong early signals

- All thirteen runs remained structurally valid and produced distinct complete long forms and Echoes.
- The free-word slots accepted ordinary nouns, adjectives, adverbs, German words, and identical words without semantic classification.
- The gentle resonance direction remained visible through opening, answering, orientation, continuation, or held-open relation tags.
- Several outputs show genuine local coherence rather than merely seven individually compatible lines.

### Repetition and collision signals

- `Two returns hold one interval open` appeared as the relation block in five of thirteen runs and became the inherited Echo trace each time. Its current weight and strong Echo support make it disproportionately dominant.
- `remainder.passage.01` appeared in seven runs. The phrase `the passage stays open` therefore becomes a conspicuous recurring closure.
- `Summer rain softens the threshold` appeared in ten runs. The atmospheric surface is narrower than the total combinatorics suggest.
- Some plans repeat a phrase family inside one poem. Output 03 uses `distance begins to answer` in both wish-entry and relation blocks. Other runs produced two nearby `Rain leaves ...` constructions. Pairwise exclusions or phrase-family limits are needed.

### Echo-linkage signals

- The current minimum lexical trace of two words can be too weak. One unlisted run with `Sol / Shadow` recorded only `sol follows`, which is technically exact but not especially characteristic.
- Longer traces such as `two returns hold one interval open` create unmistakable lineage, but their repeated use makes the Echo library feel narrower.
- Wish placement in line 4 works structurally and can be attractive, but currently relies heavily on `light keeps {wish_word} visible`.
- `rain keeps the distance` remains an interesting but directionally ambiguous line. Its low weight is appropriate; later rules may require a clearly generative counterweight elsewhere in the same Echo.

### Free-word edge cases

- `Blue / Hush`, `Perhaps / Return`, `Nähe / Weite`, and `Morgen / Geist` remained grammatically usable as poetic names. Some accidental meanings are striking, but the machine does not rely on them.
- A run with `Echo / Still` revealed a possible surface ambiguity because `Echo` is also the artifact name and `Still remains` can sound redundant. This is an unavoidable class of semantic collision unless addressed through optional human review rather than automated interpretation.
- `Return / Return` is technically representable as two relational placements, but produces `Return returns without undoing its path`. Identical free words should remain testable; human review must decide whether identical inputs need a separate lexically safer route.

## Immediate review questions

1. Which outputs feel like complete poems rather than compatible assemblies?
2. Which repeated blocks deserve lower weights, phrase-family limits, or additional alternatives?
3. Is a two-word Echo trace sufficient when it contains the free word, or should the inherited trace include at least two non-slot words?
4. Should identical wish and return words use the ordinary route or a lexically safer special route?
5. Which outputs best realise the intended movement from shadow toward a generative opening without becoming insistently bright?
