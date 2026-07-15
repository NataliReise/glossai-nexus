# Resonance V0.2 Probe Output Series 02 — Same Word Mode

This document records the first focused human-review corpus for lexically identical wish and return words.

The samples were reproduced locally from the current route order, block order, weights, proxy weights, and the new policy layer. The local environment could not import the repository directly because external DNS resolution was unavailable, so the current mixed-world library structure was reconstructed for this review run. The committed policy and its focused tests remain the source of truth.

## Policy under review

```text
casefold(wish_word) == casefold(return_word)
-> same_word_mode
```

In this mode:

- both original input fields remain present in provenance;
- the shared word appears once in the long form, in the return role;
- a curated proxy carries the earlier wish role;
- the shared word remains the complete fifth Echo line;
- exact accidental line duplication remains forbidden;
- related parallel phrasing remains allowed.

Current proxy pool:

```text
the first trace    weight 3
the opening trace  weight 2
```

## Important implementation finding

The first run exposed this malformed line:

```text
Rain leaves room for The first trace
```

The policy now capitalises a proxy only when the free-word slot begins the rendered line. Inside a sentence the proxy remains lowercase:

```text
The first trace crosses the open frame
Rain leaves room for the first trace
```

This is a placement rule, not semantic analysis.

---

## Output 01 — `Return` / `Return`

### Resonance Artifact

```text
At the open edge of night
The opening trace crosses the open frame

Wet air carries the nearness of encounter
The tide turns back without undoing departure

A stream returns by its own path
Two returns hold one interval open

Return remains where the passage stays open
```

### Nexus Echo

```text
Open distance
the opening trace crosses
two returns hold one interval open
the passage stays open
Return
```

### First observation

The awkward `Return returns` construction has disappeared. The shared word gains weight through delayed appearance, while the opening trace preserves the earlier relational role.

---

## Output 02 — `Hope` / `Hope`

### Resonance Artifact

```text
The window keeps two directions visible
The opening trace follows the light beyond the glass

Rain leaves a silver trace across the floor
The tide turns back without undoing departure

A narrow current answers from another direction
Two returns hold one interval open

Hope remains where the passage stays open
```

### Nexus Echo

```text
Open distance
the opening trace crosses
two returns hold one interval open
the passage stays open
Hope
```

### First observation

The proxy feels particularly natural here because the long form already contains a visible trace. This also exposes a possible concentration of the word family `trace`, which may be poetic parallelism rather than a defect.

---

## Output 03 — `Nähe` / `Nähe`

### Resonance Artifact

```text
At the open edge of night
The first trace follows the light beyond the glass

Summer rain softens the threshold
The tide gathers its scattered roads

Another current bends seaward through the dark
Two returns hold one interval open

Nähe remains where the passage stays open
```

### Nexus Echo

```text
Rain window
the first trace crosses
two returns hold one interval open
the passage stays open
Nähe
```

### First observation

The movement from night and darkness toward an open interval remains visible without forcing a bright conclusion. The German shared word functions cleanly as the final poetic name.

---

## Output 04 — `Perhaps` / `Perhaps`

### Resonance Artifact

```text
Wet air carries the nearness of encounter
An open frame lets distance enter

Returning water folds the shore inward
Rain leaves room for the first trace

A narrow current answers from another direction
Two returns hold one interval open

Perhaps remains where the passage stays open
```

### Nexus Echo

```text
Open distance
the first trace crosses
two returns hold one interval open
the passage stays open
Perhaps
```

### First observation

This sample confirms the corrected lowercase proxy inside a line. It also suggests that `Rain leaves room for the first trace` may be one of the most flexible same-word constructions in the current library.

---

## Output 05 — `Lumen` / `Lumen`

### Resonance Artifact

```text
The window keeps two directions visible
The first trace crosses the open frame

Rain leaves a silver trace across the floor
The tide turns back without undoing departure

A stream returns by its own path
Two returns hold one interval open

Lumen remains where the passage stays open
```

### Nexus Echo

```text
Rain window
the first trace crosses
two returns hold one interval open
the passage stays open
Lumen
```

### First observation

The result is structurally clean, but the same-word Echo route is already visibly narrow: lines three and four are currently fixed, and line two varies only with the proxy.

## Cross-series findings

### What appears successful

- The shared word no longer creates constructions such as `Return returns`.
- Both input roles remain represented without repeating the shared word.
- The shared word becomes a stronger final figure through delayed appearance.
- `the first trace` and `the opening trace` both remain grammatically neutral.
- The proxy-casing rule works at line start and inside a sentence.
- The ordinary composer path remains conceptually unchanged.

### What remains provisional

- The same-word route currently forces `relation.interval.01` and `remainder.passage.01`.
- The same-word Echo currently fixes:

```text
two returns hold one interval open
the passage stays open
```

- This protects coherence but will become repetitive quickly.
- The word `trace` may repeat through proxy, atmosphere, and Echo. This should be reviewed poetically, not automatically forbidden.
- `the opening trace` feels slightly more ceremonial; `the first trace` feels more neutral and adaptable.

## Immediate human-review questions

1. Does the proxy genuinely preserve the sense of two relational contributions?
2. Is the delayed single appearance of the shared word stronger than visible duplication?
3. Should `the first trace` become the default and `the opening trace` remain a rarer variant?
4. Which additional same-word relation and remainder structures could reduce repetition without weakening safety?
5. Should the Echo inherit the exact proxy movement selected in the long form, rather than always using `crosses`?

No production integration or persistence change is implied by this series.
