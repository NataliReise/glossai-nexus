# Resonance Composition Redesign V0.2

This document is the consolidated poetic, functional, and preliminary architectural direction for the next version of the **Nexus 01 Return Resonance** process.

It incorporates the decisions recorded in:

- `RESONANCE_COMPOSITION_DECISION_UPDATE_01.md`
- `RESONANCE_COMPOSITION_DECISION_UPDATE_02.md`

Those two files remain as a visible decision history. This document is the current implementation anchor for the next technical audit and poetic prototype.

It distinguishes three levels:

- **Decided direction**: a principle the redesign should follow.
- **Provisional decision**: a strong current rule that may still be adjusted if prototyping reveals a concrete problem.
- **Working hypothesis**: a promising mechanism that still requires technical or poetic testing.

---

## 1. Why the resonance process is being redesigned

The current implementation already preserves several important Nexus principles:

- the process remains local;
- no AI or remote service is required;
- Person A leaves an intentional trace;
- Person B answers that trace;
- the Return Artifact carries stable public-safe selections;
- local route and slot identity are validated;
- approved language forms are used instead of improvised grammar;
- a completed local result can be stored and revisited.

However, the visible poetic output is strongly deterministic. Fixed render-ready formulations and exact complete Echo paths make repeated language increasingly recognisable as more resonance processes occur.

The redesign should increase practical uniqueness without introducing semantic word analysis, external dependencies, tracking, or a large grammar engine.

```text
human choices
+ curated poetic profiles
+ small transparent composition rules
+ local first-opening randomness
= one persistent local composition
```

The intended solution is not unrestricted text generation.

---

## 2. The human resonance sequence remains intact

**Status: Decided direction**

The new composition layer must not replace or weaken the existing human sequence.

```text
Person A
  chooses an image
  chooses a scent
  chooses a movement
  leaves a wish word

Person B
  answers the image
  answers the scent
  continues the movement
  leaves a return word

Return Artifact
  carries both sides of the encounter
```

The composer enters only after this sequence has been completed and the Return Artifact has travelled back into a valid local Return Slot.

```text
The people create the resonance.
The local composer gives it a shape.
```

---

## 3. Composition happens once at the first successful opening

**Status: Decided direction**

The Return Artifact should not contain a pre-rendered poem and does not need a deterministic variation seed. It carries a structured possibility space.

At the first successful local opening:

```text
Return Artifact
  -> validate route and slot
  -> determine that no completed local result exists
  -> compose one compatible long-form Resonance Artifact
  -> derive one Nexus Echo from that completed long form
  -> save both visible outputs and relevant composition data
  -> mark the Return Slot as opened
```

At every later opening:

```text
completed local result exists
  -> read the saved result
  -> do not run the composer
  -> do not consult the composition library
  -> do not reroll any choice
```

The persistent opener should preserve the existing temporal principle:

```text
generate once
revisit often
```

A later opening must remain able to display the saved work even if the composition library has changed or is no longer available.

```text
The Return Artifact carries possibility.
The first opening gives it form.
The saved result preserves that form.
```

---

## 4. Independent local first openings may diverge

**Status: Decided direction**

The first-opening selection does not need to be reproducible from the Return Artifact alone.

The same still-unopened Return Artifact may create different completed compositions when independently actualised on different devices.

```text
one transported possibility
+ two independent local first openings
= two valid local actualisations
```

This is desired rather than defective. Each local result becomes stable only after its own first opening and persistence. No globally canonical poem is required.

---

## 5. No AI and no semantic interpretation of the free words

**Status: Decided direction**

The composer must remain small, local, transparent, and dependency-light.

It must not:

- classify the meaning of either free word;
- infer emotion or intention;
- translate the words;
- search for synonyms;
- consult a language model;
- assign psychological categories;
- rewrite the words;
- conjugate or decline them;
- pretend to understand an unknown word.

```text
The composer does not interpret the words.
It places them into poetic relations.
```

---

## 6. Wish word and return word are the human centre

**Status: Decided direction**

The image, scent, movement, and responses create the sensory and relational field. The wish word and return word are the freest and most personal public-safe elements in the Return Artifact and should therefore carry substantial compositional weight.

```text
image
  gives the encounter a visible or spatial field

scent
  gives it atmosphere and temporal depth

movement
  begins a direction

movement response
  defines how that direction is continued

wish word
  enters as the first human direction

return word
  enters as the answering direction
```

The two free words must influence the structure of the long-form composition and remain visible in the Nexus Echo.

---

## 7. Free-word input contract

**Status: Provisional decision**

Wish word and return word follow the same rules.

Each value should be:

- exactly one word;
- free of whitespace;
- free of hyphens;
- free of digits;
- free of symbols;
- free of punctuation and quotation marks;
- accepted without a part-of-speech restriction;
- used without semantic interpretation;
- used without inflection, conjugation, translation, or rewriting.

The conceptual contract is:

```text
one word
letters only
no part-of-speech restriction
same rules for wish and return
```

The exact Unicode-aware technical definition of `letters only` remains part of the later validation contract.

### Poetic display form

The stored lexical identity should remain unchanged. In the visible poem, each word should receive an initial capital letter to strengthen its temporary character as a figure, name, place, substance, or force.

```text
submitted lexical value
  -> preserved word identity
  -> capitalised poetic display form
```

The capitalisation function must not unnecessarily rewrite the remainder of the submitted spelling.

---

## 8. Free words are treated as poetic figures

**Status: Decided direction**

The composition may place either word into a grammatically neutral poetic role without relying on its ordinary word class.

Examples of the principle:

```text
Hope waited beneath the light
Blue crossed the bridge
Perhaps remained beside the rain
Return entered the water
```

Occasional grammatical or semantic strangeness is not automatically an error. It may be part of the poetic encounter.

Robust templates must not require grammatical analysis.

Compatible pattern types may include:

```text
{wish_word} waited beneath the light
The rain carried {wish_word}
Between {wish_word} and {return_word} one path remained
{return_word} moved beside it
```

Patterns to avoid include:

```text
a {wish_word}
more {wish_word}
{wish_word}s
{wish_word}ing
{wish_word}ed
```

---

## 9. Verse punctuation

**Status: Provisional decision**

The generated poetic lines should work without punctuation marks and without quotation marks wherever possible.

This applies especially to the Nexus Echo, whose line breaks should carry most of the visible structure.

```text
line break rather than punctuation
placement rather than quotation
```

Whether punctuation is prohibited through a hard validator or avoided through library design should be decided during the poetic prototype.

---

## 10. Poetic meaning is created through operators

**Status: Decided direction**

The composer can create meaning without understanding the free words by placing them into curated poetic operations.

Candidate operator families include:

- personification;
- materialisation;
- spatialisation;
- juxtaposition;
- naming;
- inscription;
- echo and trace;
- crossing;
- carrying;
- opening;
- accompaniment;
- return;
- continuation;
- transformation;
- remaining.

The operator itself proposes a relationship. Not all operators are equally neutral.

```text
lower intervention
  juxtaposition
  spatialisation
  parallel placement
  trace

medium intervention
  personification
  materialisation
  naming
  echo

stronger interpretation
  transformation
  replacement
  origin-to-destination claims
```

The composer should normally draw more often from low- and medium-intervention forms. Stronger forms require strict compatibility rules and may remain rare or absent in V0.2.

---

## 11. The selected Chamber elements provide profiles rather than verses

**Status: Decided direction**

The current image, scent, movement, and response formulations should move behind the visible poem.

Fixed formulations create recognisable repetition. The redesigned composer should therefore not normally place the existing wording directly into the new long-form Resonance Artifact or Nexus Echo.

```text
The Resonance Chamber choices provide forces rather than verses.
```

The old texts should help define the possibility space beneath the poem through poetic profiles.

Profiles may preserve:

- sensory motifs;
- visible objects;
- spatial relations;
- atmosphere;
- temporal depth;
- direction;
- movement qualities;
- relational affordances;
- compatible poetic operators;
- restraint and openness of tone;
- forms of continuation and completion.

Example profile influence:

```text
open starry window
  motifs
    window
    light
    stars
    distance

  spatial affordances
    threshold
    framing
    inside and outside
    looking outward

  operators
    opening
    crossing
    answering
    naming
```

```text
summer rain
  atmospheres
    softening
    awakening
    nearness

  traces
    water
    forest
    passing through
    leaving a mark

  operators
    carrying
    writing
    touching
```

```text
returning tide
  directions
    return
    convergence
    homeward movement

  actions
    carrying back
    meeting
    echoing
```

These examples are conceptual. The final profile schema belongs to the prototype and technical design stages.

---

## 12. No required explicit reuse of old wording

**Status: Decided direction**

The redesigned production composer does not need to reproduce the old formulations explicitly.

There is no requirement that:

- an old full line appears;
- an old phrase appears;
- a fixed old stanza appears;
- a canonical old Echo appears;
- a rare production path restores old wording verbatim.

The relationship may remain entirely indirect:

```text
old curated formulation
  -> analysed poetic qualities
  -> element profile
  -> compatible operator and motif space
  -> newly composed visible poem
```

```text
The formulation may disappear.
Its poetic force may remain.
```

The old texts become foundation rather than facade.

---

## 13. The selected Chamber elements must still matter

**Status: Decided direction**

Moving the old texts behind the visible poem must not make the Chamber choices decorative or interchangeable.

The completed long form should still be shaped by:

- at least one perceivable influence from the selected image profile;
- at least one perceivable influence from the selected scent profile;
- the selected movement and its continuation;
- the resulting completion mode;
- the wish word and return word as the human centre.

A perceivable influence does not always require literal naming. A starry-window profile may shape threshold, distance, framing, or outward movement without using the word `window`. A rain profile may shape softness, trace, passage, or nearness without using the word `rain`.

The prototype must test whether these influences remain perceptible enough without becoming predictable.

---

## 14. The movement response defines the completion mode

**Status: Decided direction; exact taxonomy remains a working hypothesis**

The return word must not be framed as a solution to the wish word.

The selected continuation of the movement defines what completion means in the particular encounter.

```text
The wish word begins a movement.
The return word continues it in the selected way.
The word is not completed.
The shape of the encounter is completed.
```

The current five movement-response pairs suggest these provisional completion modes:

| Movement | Response | Provisional completion mode |
|---|---|---|
| a feather turns as it falls | another feather crosses its path | encounter / crossing |
| a knot slowly loosens | threads gather without tightening | release with gentle connection |
| a tide begins to return | a stream flows back to the sea | convergence / return |
| a circle slowly opens | edges curl into playful waves | expansion / continuation |
| a line of light crosses the floor | a shadow moves alongside | accompaniment / coexistence |

These modes guide which relational operator templates are available.

The movement continuation is not decorative. It is a candidate for the relational grammar of the composition.

---

## 15. Curated randomness rather than unrestricted assembly

**Status: Decided direction**

The composer should filter by compatibility before choosing randomly.

```text
selected image scent movement and responses
  -> active poetic profiles
  -> completion mode
  -> compatible operator families
  -> compatible newly written forms
  -> local random selection inside that bounded set
```

The system must not blindly combine all valid lines with all other valid lines.

Each visible form should be:

- written and reviewed in advance;
- grammatically complete for its permitted slot;
- tagged with compatible motifs or roles;
- usable without modifying the free words;
- validated before release.

```text
The composer does not invent grammar.
It chooses and arranges approved poetic forms.
```

---

## 16. The role of the existing language material

**Status: Decided direction**

The existing texts remain valuable as:

- archived historical works;
- stylistic references;
- source material for profile design;
- evidence for why motifs, operators, and compatibilities were chosen;
- possible legacy test fixtures where technically necessary.

They should not normally remain as:

- directly selected production lines;
- mandatory fragments in new long forms;
- rare surprise quotations;
- privileged complete outcomes in the new composer.

The five current complete Echoes should move into an intentional archive after the technical audit has identified imports, tests, schemas, documentation links, and runtime dependencies.

```text
archive means preserved history
not abandoned debris
```

No file should be moved or deleted before that dependency and lineage review is complete.

---

## 17. Long-form Resonance Artifact and Nexus Echo have different jobs

**Status: Decided direction**

### Resonance Artifact

The long form should unfold the encounter with enough coherence that the selected sensory field and relational movement can be followed.

It should:

- use newly composed visible language;
- establish place and atmosphere;
- reflect the image and scent profiles;
- show the initial movement;
- show how Person B continues it;
- place the wish word and return word into that movement;
- remain poetic without becoming a prose explanation.

```text
The Resonance Artifact unfolds the encounter.
```

### Nexus Echo

The Echo should act as a cryptic relational riddle rather than a summary.

It may:

- omit some sensory elements;
- merge images;
- reverse familiar relations;
- use fragments rather than full explanatory sentences;
- create unusual noun groups;
- retain ambiguity;
- contain substantial local randomness;
- behave as an encrypted afterimage of the long form.

```text
The long form unfolds the encounter.
The Echo puzzles over what remains.
```

Cryptic is allowed. Arbitrary is not.

---

## 18. The Echo is derived from the completed long form

**Status: Decided direction**

The Echo must not reroll independently from the original Return Artifact.

```text
Return Artifact
  -> one composition plan
  -> newly composed long-form Resonance Artifact
  -> Nexus Echo derived from that exact completed composition
  -> save both together
```

The Echo should inherit all four of these links:

1. both free words;
2. at least one sensory motif from the long form;
3. at least one movement or relational operator from the long form;
4. at least one concrete lexical fragment from the long form.

These are cumulative rather than alternative conditions.

The exact minimum length and type of the inherited fragment remain prototype-dependent. It may be a short phrase, a characteristic verb, or another clearly traceable fragment.

The inherited fragment refers to the **newly composed long form**, not to the old deterministic Chamber texts.

```text
profiles influence the new long form
new long form creates its own visible language
Echo inherits and transforms a trace of that exact language
```

---

## 19. Fixed Nexus Echo form

**Status: Provisional decision**

Every Echo should retain the mandatory five-line word-count pattern:

```text
2 / 4 / 6 / 4 / 1
```

No rare alternative forms are currently desired.

Hyphenated words must not be used as a word-count device. The Echo library should use ordinary separate words.

The wish word:

- appears exactly once;
- uses its capitalised poetic display form;
- may appear in line 2, 3, or 4.

The return word:

- appears exactly once;
- uses its capitalised poetic display form;
- forms the final one-word line.

```text
The wish enters the Echo.
The answer is what remains.
```

The prototype must still verify that the fixed form remains varied across many random runs and works safely with all admissible free words.

---

## 20. A shared internal Composition Plan

**Status: Working hypothesis**

The long form and Echo should probably be produced from one internal composition decision rather than two unrelated random processes.

A small `CompositionPlan` may record only curated structural decisions, for example:

```json
{
  "completion_mode": "convergence",
  "primary_operator": "return",
  "secondary_operator": "echo",
  "image_profile_id": "open-starry-window-v02",
  "scent_profile_id": "summer-rain-v02",
  "movement_profile_id": "returning-tide-v02",
  "relation_template_id": "two-directions-meet-01",
  "echo_structure_id": "wish-line-3-02"
}
```

The plan must not contain an interpretation of the free words.

Potential benefits:

- long form and Echo remain related;
- compatibility decisions can be inspected;
- tests can verify selected structures;
- profile and template provenance can be recorded;
- the completed visible text remains the final source of truth.

The saved local result should always include the completed visible outputs even if the plan is also stored.

---

## 21. The 125-combination map changes role

**Status: Decided direction**

The current Chamber exposes five image families, five scent families, and five movement families, producing 125 sensory triples.

The map should no longer represent a requirement to author 125 fixed Echoes.

It becomes:

- a coverage map;
- a compatibility audit;
- a prototype sampling tool;
- an automated test matrix;
- a way to detect empty operator pools;
- a way to verify that no admissible Chamber composition is rejected at opening.

```text
125 sensory combinations
!= 125 predetermined poems

125 sensory combinations
= 125 bounded poetic possibility spaces
```

```text
What the Chamber permits
the composition library must be able to express
```

---

## 22. Preliminary composition sequence

**Status: Working target architecture**

```text
Person A selections
  + wish word

Person B responses
  + movement continuation
  + return word

Return Artifact
  -> load and validate
  -> match local Return Slot
  -> determine local result path

if completed result exists
  -> read completed result
  -> stop

if no completed result exists
  -> load active poetic profiles
  -> determine completion mode
  -> build compatible operator and form pool
  -> choose primary and optional secondary operators
  -> create Composition Plan
  -> compose new long-form Resonance Artifact
  -> derive cryptic Nexus Echo from that exact long form
  -> validate both outputs
  -> atomically save the completed local result
  -> mark the slot opened
```

Matching, composition, persistence, and revisit behaviour should remain separate responsibilities.

---

## 23. Preliminary implications for existing technical elements

**Status: Initial orientation only; requires the dedicated audit**

| Existing element | Preliminary direction |
|---|---|
| Resonance Token | retain |
| Person A Chamber selection flow | retain |
| Person B response flow | retain |
| slim Return Artifact | retain; version impact to be reviewed |
| route and Return Slot matching | retain |
| local result persistence | retain and strengthen |
| persistent opener | retain and reorder so existing results are read before composition |
| read-only preview | retain as development and diagnostic support |
| current player-facing choices | retain unless the audit reveals a concrete issue |
| fixed render-ready formulations | preserve as profile lineage and archive material rather than normal production output |
| current long-form renderer | replace as the only production composer; inspect reusable responsibilities first |
| five current complete Echoes | archive after dependency review |
| exact complete Echo-path matching | replace as the production route; possibly preserve for legacy tests or compatibility |
| no-path failure for valid Chamber combinations | remove through complete V0.2 coverage |
| 125-combination workbook | retain as coverage and test map |

No file should be removed solely on the basis of this preliminary table.

---

## 24. Questions that remain open before implementation

### Input validation

- Exact Unicode-aware definition of a permitted letter-only word.
- Exact capitalisation behaviour.
- Hard punctuation validation versus punctuation-free library discipline.

### Operator system

- Final operator taxonomy.
- Number of operator families required for V0.2.
- Compatibility representation through tags, explicit lists, or both.
- Weighting versus simple random choice.
- Whether stronger-interpretation operators belong in V0.2.

### Completion modes

- Final names for the five current modes.
- Whether each mode belongs directly to one movement-response pair.
- Whether future movement responses may share one mode.

### Long-form structure

- Number and organisation of visible lines or stanzas.
- Whether one primary and one secondary operator are sufficient.
- How often each free word should appear in the long form.
- How selected profile influences remain perceptible without literal naming.

### Echo structure

- Exact minimum length and type of the inherited long-form fragment.
- Degree of allowed image merging and syntactic fragmentation.
- How to preserve high variation inside the mandatory `2 / 4 / 6 / 4 / 1` form.

### Persistence

- Exact completed-result format.
- Whether the `CompositionPlan` is stored beside the visible text.
- How profile, template, and library versions are recorded.
- Behaviour when a slot is marked opened but the result file is missing.

### Migration and compatibility

- Whether existing V0.1 Return Artifacts open through the V0.2 composer unchanged.
- Whether a new artifact version is required.
- Whether V0.1 exact paths remain directly renderable as legacy behaviour.
- How tests distinguish legacy rendering from the V0.2 production path.
- Physical archive layout and migration order.

---

## 25. Non-goals

The redesign must not introduce:

- AI-generated poetry;
- online semantic services;
- automatic upload or delivery;
- user accounts;
- tracking;
- a social graph;
- relationship management;
- engagement logic;
- opaque scoring of a player response;
- quality ranking of wish or return words;
- rejection of an admissible composition after the players have completed it;
- a large general-purpose natural-language grammar engine.

The Nexus continues to manage the artifact, not the relationship.

---

## 26. Next steps

### Step 1: Technical audit

Create:

```text
RESONANCE_TECHNICAL_AUDIT_V0_2.md
```

Inspect each relevant component and classify it as:

```text
retain
retain and reframe
modify
replace
archive as legacy
remove later
```

No classification should be based on filename alone. The actual responsibility, dependencies, hidden value, and poetic lineage of each mechanism must be inspected.

### Step 2: Poetic micro-prototype

Prototype three contrasting profile combinations:

1. one current canonical combination as source lineage;
2. the mixed starry-window / summer-rain / returning-tide composition;
3. one contrasting interior or knot-based composition.

Generate many first-opening candidates and review:

- variety;
- coherence;
- visibility of both free words;
- completion-mode fidelity;
- perceivable profile influence;
- relationship between long form and Echo;
- productive versus arbitrary strangeness;
- template repetition.

### Step 3: Define the V0.2 library contract

Only after the micro-prototype succeeds, define:

- profile schema;
- operator schema;
- template or form schema;
- compatibility rules;
- Composition Plan schema;
- validation rules;
- persistence format.

### Step 4: Integrate first-opening composition

Refine the persistent opener so that:

- an existing result is read before any composition runs;
- an unopened valid return is composed once;
- both visible outputs are saved atomically;
- later openings remain independent of the composition library.

### Step 5: Coverage testing

Use the 125-combination map across many random runs.

The goal is not to prove literary quality automatically. The goal is to prove structural safety and complete coverage while leaving poetic judgment to human review.

---

## 27. Current guiding formulations

```text
The people create the resonance.
The local composer gives it a shape.
```

```text
The composer does not interpret the words.
It places them into poetic relations.
```

```text
The image gives the words a place.
The scent gives the encounter an atmosphere.
The movement gives it a direction.
The continuation defines how the encounter is completed.
```

```text
The wish word begins a movement.
The return word continues it in the selected way.
The word is not completed.
The shape of the encounter is completed.
```

```text
The Resonance Chamber choices provide forces rather than verses.
```

```text
The old text becomes foundation rather than facade.
```

```text
The elements do not determine the poem.
They determine what kinds of poetic movement are possible.
```

```text
The Resonance Artifact unfolds the encounter.
The Nexus Echo puzzles over what remains.
```

```text
The wish enters the Echo.
The answer is what remains.
```

```text
The Return Artifact carries possibility.
The first opening gives it form.
The saved result preserves that form.
```