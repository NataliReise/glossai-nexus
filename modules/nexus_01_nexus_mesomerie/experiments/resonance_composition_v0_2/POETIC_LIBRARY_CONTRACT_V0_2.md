# Poetic Library Contract for the Resonance V0.2 Microprototype

This document defines the provisional library contract for the small local Resonance poetry composer.

It belongs to the isolated V0.2 microprototype and does not alter the V0.1 production path.

Its purpose is to describe how curated poetic knowledge can be stored in a transparent library and combined by a generator that performs no semantic interpretation.

```text
The generator does not understand the poem
The library defines what may be joined
```

The contract is a design and prototyping agreement, not yet a frozen data schema.

---

## 1. Central boundary

**Status: Decided direction**

The composer must not analyse the meaning of the wish word or return word.

It must not:

- classify either word by part of speech;
- infer whether a word is positive or negative;
- infer emotion, intention, topic, or symbolism;
- search for synonyms;
- translate or paraphrase a word;
- conjugate, decline, pluralise, or otherwise rewrite a word;
- use a language model or external semantic service.

All poetic and directional intelligence must be supplied in advance through:

- curated profiles;
- completion modes;
- reviewed text structures;
- compatibility metadata;
- transition rules;
- resonance-gain requirements;
- terminal avoidances.

```text
Human curation carries meaning
Machine selection carries structure
Human reading creates resonance
```

---

## 2. Five library layers

The prototype should distinguish five responsibilities.

```text
1. Poetic profiles
   describe the forces supplied by Chamber selections

2. Completion modes
   describe how the selected movement is continued relationally

3. Poetic building blocks
   provide reviewed word-neutral visible language

4. Access and transition rules
   define which blocks may be joined in which context

5. Composition Plan
   records one valid local selection from the available possibility space
```

No one layer should secretly perform the responsibilities of another.

---

## 3. Poetic profiles

Profiles are derived from the current curated Chamber elements, but they do not need to reproduce their wording.

A profile may describe:

```text
motifs
spatial affordances
atmospheric qualities
temporal qualities
movement qualities
relational affordances
operator affinities
resonant gains
allowed shadow states
terminal avoidances
```

Profiles answer questions such as:

```text
What kind of place may this image create
What kind of atmosphere may this scent contribute
What kind of movement may this selection begin
What kind of relation may this response permit
What must this selection not be made to imply
```

Profiles never answer:

```text
What does the player's free word mean
```

### Example profile fragment

```json
{
  "id": "open-starry-window",
  "motifs": ["window", "night", "light", "stars", "distance"],
  "spatial_affordances": [
    "threshold",
    "inside-and-outside",
    "framing",
    "open-distance"
  ],
  "operator_affinities": [
    "opening",
    "answering-across-distance",
    "remaining-visible"
  ],
  "resonant_gains": [
    "orientation",
    "visibility",
    "possibility-of-answer"
  ],
  "allowed_shadow_states": [
    "distance",
    "night",
    "uncertainty"
  ],
  "terminal_avoid": [
    "sealed-threshold",
    "total-extinguishing",
    "certainty-about-the-beyond"
  ]
}
```

The exact field names remain provisional.

---

## 4. Completion modes

A completion mode describes the relational grammar supplied by the selected movement response.

It does not interpret either free word.

It constrains how two poetic directions may be related.

For example:

```text
crossing-encounter
  two movements meet or cross
  neither absorbs the other

converging-return
  two directions move into relation
  return does not erase departure
  convergence does not require fusion

released-connection
  contact remains possible
  loosening creates room
  gathering does not tighten or bind
```

Each completion mode may define:

- accepted starting states;
- favoured relational operators;
- required gains, expressed as `one_of` or `all_of` sets;
- disfavoured operators;
- forbidden relational claims;
- compatible terminal states.

### Example completion-mode fragment

```json
{
  "id": "converging-return",
  "starting_states": [
    "distance",
    "separate-directions",
    "uncertain-orientation"
  ],
  "favoured_operators": [
    "returning",
    "answering-as-current",
    "sharing-direction",
    "holding-an-interval-open"
  ],
  "required_gain_one_of": [
    "orientation",
    "reciprocity",
    "approach",
    "renewed-visibility",
    "held-open-relation"
  ],
  "forbidden_relations": [
    "wish-becomes-return",
    "return-solves-wish",
    "one-direction-erases-the-other",
    "return-cancels-departure"
  ],
  "forbidden_terminal_states": [
    "abandonment",
    "entrapment",
    "closed-path",
    "total-silence"
  ]
}
```

---

## 5. Resonance direction

**Status: Decided direction, implementation still provisional**

Resonance in the GlossAI world should carry a gentle generative tendency.

This does not require brightness, happiness, certainty, or resolution.

A poem may contain:

- darkness;
- dusk;
- distance;
- silence;
- uncertainty;
- separation;
- an incomplete meeting.

But the completed movement should leave at least one new possibility behind.

```text
The poem may enter darkness
Resonance must leave a passage
```

A valid composition must therefore contain at least one **resonant gain**.

Possible gain tags include:

```text
openness
orientation
visibility
answering
reciprocity
approach
accompaniment
mobility
room
continuation
gentle-connection
possibility
held-open-relation
```

This is a structural tag system, not semantic analysis.

The composer does not decide that a visible line is hopeful. The library author has already reviewed the block and assigned the gain tags that it is permitted to carry.

### Hard and soft direction rules

Hard rules should exclude only clear violations of the Nexus direction, such as:

```text
erasure
entrapment
abandonment as the final movement
total extinguishing
one word replacing the other
one response solving or judging the wish
all paths closing
```

Soft weighting should favour:

```text
opening
answering
carrying
approaching
accompanying
releasing
making room
remaining visible
continuing
```

Shadow states remain available as starting or intermediate material.

They should not become an unqualified closed terminal state.

---

## 6. Poetic building-block roles

A building block is a reviewed visible text structure with a defined compositional role.

The first prototype may use the following role families.

### `field`

Establishes place, spatial relation, or perceptual frame.

Examples of functions:

```text
threshold
interior
shore
open distance
edge of visibility
shared place
```

### `atmosphere`

Changes how the field is perceived through scent, weather, temporal depth, or texture.

Examples of functions:

```text
softening
recent passage
stored time
quiet duration
awakening
```

### `wish_entry`

Places the wish word into the field as a poetic figure, direction, presence, trace, or movement.

The slot must be grammatically neutral.

### `movement`

Begins or develops the selected motion.

### `response_movement`

Introduces the second direction according to the selected movement response.

### `relation`

Places both directions into a compatible relational form.

### `resonant_gain`

Makes at least one permitted gain structurally visible.

A relation block may also fulfil this role when tagged accordingly.

### `remainder`

Leaves the long form open without undoing its gain.

The return word may appear here as the remaining figure.

### `echo_trace`

Marks a visible phrase, verb sequence, motif, or relational core as eligible for inheritance by the Nexus Echo.

One block may carry more than one role only when that combination has been reviewed explicitly.

---

## 7. Minimum building-block metadata

Every production-eligible block should eventually contain at least:

```text
id
text template
role
allowed free-word slots
compatible profile tags
compatible completion modes
operators carried
resonant gains added
terminal status
weight
```

A provisional example:

```json
{
  "id": "relation.interval.01",
  "text": "two returns hold one interval open",
  "roles": ["relation", "resonant_gain", "echo_trace"],
  "word_slots": [],
  "requires_all_tags": ["return", "two-directions"],
  "requires_any_tags": ["distance", "threshold", "current"],
  "completion_modes": ["converging-return"],
  "operators": ["returning", "holding-open"],
  "adds_gains": ["held-open-relation", "openness"],
  "leaves_states": ["interval", "continued-separateness"],
  "forbids_after": ["fusion", "closed-path"],
  "terminal_allowed": true,
  "echo_eligible": true,
  "weight": 3
}
```

### Optional metadata

Later prototypes may also use:

```text
allowed previous roles
allowed next roles
excludes block IDs
requires one of block IDs
motifs made visible
lexical trace candidates
maximum uses per composition
style family
interpretive strength
line count or stanza preference
```

The prototype should add metadata only when it solves a demonstrated compositional problem.

---

## 8. Free-word slot contract

Wish word and return word follow the same provisional input rules:

```text
exactly one word
letters only
no whitespace
no hyphens
no digits
no punctuation or quotation marks
no part-of-speech restriction
```

The lexical input identity is preserved.

The visible poetic display form begins with an uppercase letter without otherwise intentionally rewriting the word.

A block using a free-word slot must:

- remain grammatical for an unknown one-word value;
- require no article agreement;
- require no inflection;
- require no pluralisation;
- require no semantic category;
- avoid attaching prefixes or suffixes;
- avoid treating the word as a verb form.

Allowed structural examples include:

```text
{wish_word} crosses the open frame
rain leaves room for {wish_word}
between {wish_word} and {return_word} one current remains
{return_word} waits where the passage stays open
```

Normally disallowed examples include:

```text
a {wish_word}
more {wish_word}
{wish_word}s
{wish_word}ing
{wish_word}ed
```

The composer validates the slot form. It does not validate the meaning of the word inside it.

---

## 9. Access rules

A block is not available merely because it exists in the library.

The composer should build a candidate pool by filtering in stages.

```text
active Chamber profile IDs
  -> active profile tags
  -> selected completion mode
  -> allowed building-block roles
  -> profile compatibility
  -> completion-mode compatibility
  -> transition compatibility
  -> resonance-direction compatibility
  -> weighted random choice
```

A block may require:

- all listed tags;
- at least one listed tag;
- a particular completion mode;
- a prior role;
- the presence or absence of another operator;
- an available free-word slot;
- an unfinished required gain.

A block may exclude:

- incompatible completion modes;
- contradictory operators;
- specific terminal states;
- specific neighbouring roles;
- a second use of the same conspicuous phrase family.

---

## 10. Transition rules

The composer should not assemble arbitrary valid lines.

It should create a small valid movement through roles.

A first prototype may support several structural routes instead of one fixed stanza order.

### Example route A

```text
field
-> atmosphere
-> wish_entry
-> movement
-> response_movement
-> relation plus resonant_gain
-> remainder
```

### Example route B

```text
atmosphere
-> field
-> movement
-> wish_entry
-> response_movement
-> resonant_gain
-> remainder
```

### Example route C

```text
field
-> wish_entry
-> atmosphere
-> movement
-> relation
-> resonant_gain plus remainder
```

Every selected route must still ensure:

- perceptible image-profile influence;
- perceptible scent-profile influence;
- selected movement influence;
- selected movement-response influence;
- completion-mode fidelity;
- visible wish and return words;
- at least one resonant gain;
- no forbidden terminal state.

The route controls structure. It does not prescribe one fixed poem.

---

## 11. Composition validation

A proposed `CompositionPlan` should be accepted only after structural validation.

The validator should check at least:

1. all selected block IDs exist;
2. each block is permitted by the active profiles;
3. each block is permitted by the completion mode;
4. the role sequence is allowed;
5. required profile families are represented;
6. required free-word slots are present;
7. the wish and return words are not rewritten;
8. incompatible operators do not co-occur;
9. at least one resonant gain is present;
10. no forbidden terminal state is present;
11. at least one long-form lexical trace is marked for the Echo;
12. the resulting visible text contains no unresolved placeholders.

The validator does not judge literary quality.

It protects the curated boundaries inside which literary quality has a chance to emerge.

---

## 12. Composition Plan contract

A `CompositionPlan` records one local compositional decision before visible rendering.

It should be inspectable during development and storable as optional provenance beside the completed visible text.

A provisional form may contain:

```json
{
  "plan_version": "resonance-composition-plan-prototype-v0.2",
  "profile_ids": {
    "image": "open-starry-window",
    "image_response": "answering-distant-light",
    "scent": "summer-rain",
    "scent_response": "possibility-of-encounter",
    "movement": "returning-tide",
    "movement_response": "stream-back-to-sea"
  },
  "completion_mode": "converging-return",
  "route_id": "field-atmosphere-wish-movement-relation-remainder",
  "block_ids": [
    "field.threshold.02",
    "atmosphere.soft-trace.03",
    "wish-entry.frame.01",
    "movement.return.04",
    "response.current.02",
    "relation.interval.01",
    "remainder.visible-distance.02"
  ],
  "operators": [
    "opening",
    "returning",
    "answering-as-current",
    "holding-open"
  ],
  "resonant_gains": [
    "orientation",
    "held-open-relation"
  ],
  "echo_source": {
    "block_id": "relation.interval.01",
    "lexical_trace": "hold one interval open"
  },
  "echo_wish_line": 3
}
```

The completed visible long form and Echo remain the final local result.

The plan records provenance and validation decisions, not hidden human meaning.

---

## 13. Nexus Echo derivation

The Echo must be derived from the completed long form and its `CompositionPlan`.

It must not independently select a second unrelated poetic world.

The Echo contract remains:

```text
five lines
2 / 4 / 6 / 4 / 1 words
wish word exactly once in line 2 3 or 4
return word exactly once as line 5
no punctuation
```

It must inherit cumulatively:

- both free words;
- at least one sensory motif visible in the long form;
- at least one movement or relational operator from the long form;
- at least one concrete lexical trace from the long form.

The Echo may compress, reorder, or create a cryptic relation among those inherited materials.

It may not contradict the completion mode or reverse the verified resonance direction.

```text
The long form unfolds the encounter
The Echo puzzles over what remains
```

---

## 14. Randomness

Production first openings may use fresh local randomness.

Prototype and test code should accept an injected random source or seed so that a result can be reproduced during review.

Randomness may choose among already compatible options such as:

- structural route;
- primary and secondary operator;
- visible motif;
- block variant;
- wish-word position;
- eligible Echo trace;
- Echo structure compatible with the chosen trace.

Randomness must not bypass compatibility filtering.

```text
filter first
choose second
validate third
persist once
```

Once a completed local result exists, no further random choice is allowed during reopening.

---

## 15. Hard rules and weighted preferences

### Hard rules

```text
no semantic analysis of free words
no grammatical rewriting of free words
profile compatibility required
completion-mode compatibility required
at least one resonant gain required
forbidden terminal states rejected
both free words visible
Echo derived from the completed long form
Echo pattern fixed at 2 / 4 / 6 / 4 / 1
completed local result never rerolled
```

### Weighted preferences

```text
low and medium interpretive operators preferred
strong transformation rare or absent in the first prototype
concrete image before abstract explanation
relational movement before relational thesis
open remainder before final solution
varied block families before conspicuous repetition
```

A weighted preference should never be used to permit a hard-rule violation.

---

## 16. First-prototype scope

The first executable prototype should remain deliberately small.

It should support only the three existing profile worlds:

```text
canonical-origin-world
mixed-threshold-return-world
interior-release-world
```

It should use a limited reviewed library sufficient to test:

- more than one valid long form per world;
- more than one valid Echo per world;
- word-neutral free-word insertion;
- resonance-direction enforcement;
- completion-mode fidelity;
- lexical linkage from long form to Echo;
- avoidance of old fixed visible formulations.

It should not yet claim complete coverage of all 125 sensory triples.

---

## 17. Questions left for the next prototype stage

The following points should be decided through actual generated examples:

- how many structural routes are needed before variety becomes convincing;
- whether one primary and one secondary operator are sufficient;
- how many visible motifs should normally appear;
- how abstract a `resonant_gain` block may become before it feels explanatory;
- how short an inherited Echo trace may be while remaining perceptible;
- whether strong transformation operators belong in V0.2 at all;
- how aggressively conspicuous phrase families should be repetition-limited;
- whether terminal-state validation can rely entirely on block metadata;
- which metadata fields prove useful and which merely decorate the schema.

No field should become permanent merely because it appeared in this first contract.

---

## 18. Current guiding formulations

```text
The generator does not understand the poem
The library defines what may be joined
```

```text
The poem may enter darkness
Resonance must leave a passage
```

```text
Shadow may shape the field
A generative direction must shape the movement
```

```text
The Resonance Chamber supplies forces rather than verses
The composer gives those forces one local form
```

```text
Filter first
Choose second
Validate third
Persist once
```
