# Resonance Composition Decision Update 01

This document records the first review decisions made after reading
`RESONANCE_COMPOSITION_REDESIGN_V0_2.md`.

It supplements the concept record until the decisions are folded into a later consolidated revision.
The decisions are strong current directions, but they may still be adjusted when poetic prototypes reveal a concrete problem.

---

## 1. Free-word input contract

**Status: Provisional decision**

Wish word and return word follow the same rules.

Each value should be:

- exactly one word;
- free of whitespace;
- free of hyphens;
- free of digits;
- free of standalone symbols;
- free of punctuation and quotation marks;
- accepted without any part-of-speech restriction;
- used without semantic interpretation;
- used without inflection, conjugation, translation, or rewriting.

The intended conceptual contract is therefore:

```text
one word
letters only
no part-of-speech restriction
same rules for wish and return
```

The exact technical definition of `letters only`, including Unicode handling, remains an implementation detail for the later library and validation contract.

### Display form

The lexical word should remain otherwise unchanged, but the poetic output should present it with an initial capital letter in order to strengthen its temporary figure or name character.

```text
submitted lexical value
  -> unchanged word identity
  -> capitalised poetic display form
```

The exact capitalisation function should be chosen carefully so that it does not unnecessarily rewrite the remainder of the submitted spelling.

---

## 2. Verse punctuation

**Status: Provisional decision**

The generated poetic lines should aim to work without punctuation marks and without quotation marks.

This applies especially to the Nexus Echo, whose line breaks should carry most of the visible structure.

```text
line break rather than punctuation
placement rather than quotation
```

Whether punctuation is prohibited by a hard validator or avoided by library design should be tested during the poetic micro-prototype.

---

## 3. Fixed Nexus Echo form

**Status: Provisional decision**

The Nexus Echo should retain the five-line Nachhall form with the mandatory word-count pattern:

```text
2 / 4 / 6 / 4 / 1
```

No rare alternative forms are currently desired.

Hyphenated words should not be used as a device for satisfying the word count.
The Echo library should be written with ordinary separate words.

The wish word may appear in any of the middle lines:

```text
line 2
line 3
or line 4
```

The return word remains the final one-word line.

Both free words should appear exactly once in their poetic display form.

---

## 4. The Echo as a relational riddle

**Status: Decided direction**

The Echo should not function as a summary of the long-form Resonance Artifact.

It should behave more like a small riddle or encrypted afterimage that:

- recreates and condenses the relational direction of the long form;
- recreates and condenses its movement or continuation logic;
- integrates the wish word;
- leaves the return word as the final remaining word;
- allows cryptic image combinations and substantial local randomness;
- remains related to the actual completed long-form composition.

```text
The long form unfolds the encounter.
The Echo puzzles over what remains.
```

The Echo may be highly surprising, but its surprise should occur inside the relational and movement space already established by the long form.

---

## 5. Minimum linkage between long form and Echo

**Status: Provisional decision**

All four proposed linkage conditions should be retained:

1. both free words appear;
2. at least one sensory motif from the long form is inherited;
3. at least one movement or relational operator remains recognisable;
4. at least one concrete text fragment is inherited from the long form.

These are cumulative conditions rather than alternatives.

The exact form and minimum length of the inherited text fragment remain open for poetic prototyping. It may prove sufficient to inherit a short phrase, a characteristic verb, or another clearly traceable lexical fragment.

The connection should be perceivable without forcing the Echo to paraphrase the long form.

---

## 6. Status of the five current canonical Echoes

**Status: Provisional decision**

The five existing complete Echoes should not remain privileged production outcomes in the redesigned composer.

They should instead move into an archive for earlier Nexus elements.

Possible archival roles include:

- historical origin forms;
- documentation of the development path;
- style references;
- stable legacy test fixtures where technically useful.

They should not constrain the new generator merely because they were created first.

No file should be moved yet.
The technical audit must first identify imports, tests, schemas, documentation links, and runtime dependencies.

The archive itself should be designed as an intentional part of the repository rather than as an unstructured discard folder.

```text
archive means preserved history
not abandoned debris
```

---

## 7. Independent first openings on different devices

**Status: Decided direction**

It is acceptable and positively desired that the same still-unopened Return Artifact may create different completed local compositions when independently actualised on different devices.

```text
one transported possibility
+ two independent local first openings
= two valid local actualisations
```

This is not considered a conflict or a defect.

Each completed local result becomes stable only after its own first opening and persistence.
No globally canonical poem is required.

---

## 8. Consequences for the main concept record

The following points can move out of the fully open-question category in a later consolidated revision:

- one-word requirement;
- no part-of-speech restriction;
- same validation rules for wish and return;
- no hyphenated inputs;
- no digits or standalone symbols;
- capitalised poetic display form;
- punctuation-free verse as the preferred design;
- mandatory `2 / 4 / 6 / 4 / 1` Echo form;
- no alternative Echo forms;
- wish word allowed in lines 2, 3, or 4;
- all four long-form-to-Echo linkage conditions;
- archival future for the five existing complete Echoes;
- desired multi-device divergence.

The following matters remain open or prototype-dependent:

- exact Unicode-aware definition of a permitted word;
- exact capitalisation behaviour;
- hard validation versus punctuation-free library discipline;
- final operator taxonomy and weighting;
- final completion-mode names;
- exact long-form composition structure;
- length and type of the inherited long-form fragment;
- exact persistence format for visible texts and Composition Plan;
- V0.1 artifact migration and legacy compatibility;
- physical archive layout and migration order.

---

## 9. Current compact rule set

```text
One free word from each person
No grammatical classification
No semantic interpretation
No hyphens digits symbols or punctuation
The words enter the poems as capitalised poetic figures

The long form unfolds the selected relationship
The Echo becomes its cryptic relational riddle

The Echo always follows 2 / 4 / 6 / 4 / 1
The wish appears once in line 2 3 or 4
The answer appears once as line 5

The Echo inherits both words
one sensory motif
one movement or relational operator
and one concrete fragment from the long form

A first opening may differ across devices
A completed local result does not change again

Earlier complete Echoes are preserved in an intentional archive
but no longer govern the future composer
```
