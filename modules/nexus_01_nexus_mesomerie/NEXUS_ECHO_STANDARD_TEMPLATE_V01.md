# Nexus Echo Standard Template V0.1

Status date: 2026-07-13

This note defines the first standard form for the local, rule-based Nexus Echo renderer.

It builds on:

```text
RESONANCE_COMPOSITION_AND_POEM_V01.md
RESONANCE_OUTPUT_TERMINOLOGY_V01.md
RESONANCE_RESPONSE_SETS_V01.md
```

## Purpose

The Nexus Echo is the short poetic output produced after the local opening of a Return Artifact.

It is not a summary of the Resonance Artifact. It is a compact, more ambiguous after-effect of the shared resonance.

```text
Return Artifact
-> local opening
-> Resonance Artifact
-> Nexus Echo
```

The Nexus Echo is generated locally, without AI, from a versioned library of approved language forms.

## Formal shape: Nachhall

The V0.1 Nexus Echo uses five lines with the exact word pattern:

```text
2 - 4 - 6 - 4 - 1
```

The form expands toward the middle and contracts toward a final single word.

## Line functions

### Line 1 - Image

```text
2 words
```

A concrete approved motif opens the poem.

```text
L1 = approved two-word motif form
```

Examples:

```text
Summer rain
Open books
Evening window
Painted stone
Narrow bridge
```

Line 1 should place something in the reader's path without interpreting it.

### Line 2 - Movement or atmosphere

```text
4 words
```

Line 2 extends Line 1 through a local action, spatial relation, or atmosphere.

```text
L2 = approved four-word continuation compatible with L1
```

Examples:

```text
opens one hidden path
wait beneath soft light
frames one distant light
sends one ripple outward
holds one quiet crossing
```

### Line 3 - Turning point

```text
6 words
```

Line 3 is the central relation line. At least two approved trace elements must meet, change, answer, cross, or otherwise enter into relation.

```text
L3 = approved six-word relation line
```

Examples:

```text
two feathers cross beneath waiting light
two voices meet; one knot loosens
tide and stream meet beneath wonder
circle opens where first snow waits
light and shadow share one silence
```

Line 3 must not add psychological interpretation.

### Line 4 - Echo

```text
4 words
```

Line 4 must explicitly reuse an approved motif from Line 1 or Line 2 and give it a changed function.

```text
L4 = approved four-word echo line
```

Examples:

```text
the path carries courage
the books leave room
the light turns homeward
the ripple turns playful
the bridge leaves room
```

The repeated motif should remain recognizable. Repetition is allowed when the motif deepens, shifts, or changes role.

### Line 5 - Aftersound

```text
1 word
```

For V0.1:

```text
L5 = return_word
```

Examples:

```text
trust
welcome
return
play
presence
```

The final word must not explain the poem. It should remain open.

## Standard template

```text
L1: concrete motif
L2: local action or atmosphere
L3: relation between at least two trace elements
L4: repeated motif in altered function
L5: returned word
```

## Canonical V0.1 examples

```text
Summer rain
opens one hidden path
two feathers cross beneath waiting light
the path carries courage
trust
```

```text
Open books
wait beneath soft light
two voices meet; one knot loosens
the books leave room
welcome
```

```text
Evening window
frames one distant light
tide and stream meet beneath wonder
the light turns homeward
return
```

```text
Painted stone
sends one ripple outward
circle opens where first snow waits
the ripple turns playful
play
```

```text
Narrow bridge
holds one quiet crossing
light and shadow share one silence
the bridge leaves room
presence
```

## Hard renderer rules

```text
1. The exact word pattern is 2 / 4 / 6 / 4 / 1.
2. Line 1 must contain a concrete approved motif.
3. Line 2 must be explicitly compatible with Line 1.
4. Line 3 must combine at least two trace elements.
5. Line 4 must reuse a motif from Line 1 or Line 2.
6. Line 5 must be the returned word.
7. Every content-bearing phrase must come from the local approved language library.
8. The renderer must not invent interpretation.
9. Repetition is allowed when the motif changes function.
10. If no valid standard echo exists, the renderer must use a predefined fallback rather than improvising.
```

## Allowed runtime operations

The renderer may:

```text
read IDs
select compatible approved forms
insert an approved one-word slot value
validate word counts
validate motif reuse
assemble the five lines
```

The renderer must not:

```text
conjugate freely
paraphrase freely
infer symbolism
add emotional conclusions
replace a player's word
invent new motifs
```

## Word counting

Word counting is a hard validation step.

For V0.1, a word is a whitespace-separated token after normalizing leading and trailing whitespace.

Hyphenated wish or return words remain one token if the input rules already accept them as one valid word.

The validator must compare the result to:

```json
[2, 4, 6, 4, 1]
```

## Fallback principle

The Nexus Echo must never depend on free generation.

If a selected combination has no valid standard path, the local library should provide a predefined compatible fallback or the renderer should choose another approved standard path.

```text
No valid approved path
-> no improvisation
-> approved fallback
```

## Design formula

```text
The players create the resonance.
The Nexus reveals one permitted poetic path through it.
```

The Nexus Echo is therefore best understood as a rule-bound poetic composition, not as an AI-generated poem.
