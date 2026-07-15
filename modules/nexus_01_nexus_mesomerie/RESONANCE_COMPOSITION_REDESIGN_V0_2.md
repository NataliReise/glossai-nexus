# Resonance Composition Redesign V0.2

This document gathers the poetic, functional, and preliminary architectural direction for the next version of the **Nexus 01 Return Resonance** process.

It was written after pausing implementation to compare the current deterministic renderer with the intended experience of a unique local resonance.

It is a **concept and decision record**, not yet a technical implementation specification.

The document distinguishes three levels:

- **Decided direction**: principles that should guide the redesign.
- **Working hypothesis**: promising mechanisms that still need poetic prototyping.
- **Open question**: points that should remain unsettled until examples or technical review provide enough evidence.

---

## 1. Why the resonance process is being reconsidered

The current implementation already preserves several important Nexus principles:

- the process remains local;
- no AI or remote service is required;
- Person A leaves an intentional trace;
- Person B answers that trace;
- the Return Artifact carries stable public-safe selections;
- local route and slot identity are validated;
- approved language forms are used instead of improvised grammar;
- a completed local result can be stored and revisited.

However, the current poetic output is still strongly deterministic.

The selected image, scent, movement, responses, wish word, and return word resolve to fixed render-ready forms. The Nexus Echo currently requires one complete approved path. Therefore, identical selections usually lead to the same visible composition.

The redesign should increase practical uniqueness without introducing AI, semantic language analysis, external dependencies, tracking, or a large grammar engine.

The intended solution is not unrestricted text generation.

```text
human choices
+ curated poetic material
+ small transparent composition rules
+ local first-opening randomness
= one unique persistent local composition
```

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

The generator enters only after this sequence has been completed and the Return Artifact has travelled back into a valid local Return Slot.

The generator does not create the resonance between the players.

It gives the already-created resonance a local poetic form.

```text
The people create the resonance.
The local composer gives it a shape.
```

---

## 3. Composition happens once, at the first successful opening

**Status: Decided direction**

The Return Artifact should not contain a pre-rendered poem and does not need to contain a deterministic variation seed.

It carries a structured possibility space.

At the first successful local opening:

```text
Return Artifact
  -> validate route and slot
  -> determine that no completed local result exists
  -> compose one compatible long-form Resonance Artifact
  -> derive one Nexus Echo from that composition
  -> save the completed result
  -> mark the Return Slot as opened
```

At every later opening:

```text
completed local result exists
  -> read the saved result
  -> do not run the composer
  -> do not consult the language library again
  -> do not reroll any choices
```

The old persistent opener already contains the central temporal idea:

```text
generate once, revisit often
```

The redesign should therefore refine that mechanism rather than replace it wholesale.

A later opening must be able to display the saved completed work even when the composition library has since changed or is no longer available.

### Consequence

The local composer is not the permanent source of the poem.

It is its birth mechanism.

```text
The Return Artifact carries possibility.
The first opening gives it form.
The saved result preserves that form.
```

---

## 4. Local randomness is allowed to be genuinely random

**Status: Decided direction**

The first-opening selection does not need to be reproducible from the Return Artifact alone.

A fresh local random selection may be made each time an as-yet-unopened valid Return Artifact is first actualised.

Once the completed result has been written, that exact result becomes stable.

Two independent devices could therefore actualise the same still-unopened Return Artifact differently.

This follows naturally from the present concept:

```text
The Return Artifact carries a possibility,
not one globally predetermined poem.
```

Whether multi-device divergence should remain an accepted property or later receive a transport convention is still an open product question. It is not a reason to make the initial composer deterministic.

---

## 5. No AI and no semantic interpretation of the free words

**Status: Decided direction**

The composer must remain small, local, transparent, and dependency-light.

It must not attempt to understand the semantic meaning of the wish word or the return word.

It should not:

- classify their meaning;
- infer emotion or intention;
- translate them;
- search for synonyms;
- consult a language model;
- assign psychological categories;
- rewrite them;
- conjugate or decline them;
- pretend to understand an unknown word.

The meaning should arise in the reading, not inside the program.

```text
The composer does not interpret the words.
It places them into poetic relations.
```

---

## 6. Wish word and return word are the human centre

**Status: Decided direction**

The image, scent, and movement choices create the sensory field.

The wish word and return word are the freest and most personal public-safe elements in the Return Artifact. They should therefore carry substantial compositional weight.

```text
image
  gives the encounter a visible place

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

The words should not merely be inserted into the last two slots of an otherwise fixed poem.

Their relation should influence the structure of the long-form composition and remain visible in the Nexus Echo.

---

## 7. Free words may be treated as poetic names

**Status: Decided direction, with input details still open**

The current Return Artifact does not store or validate a part of speech for the wish word or return word.

The redesign should probably preserve that freedom.

Instead of using each word according to its ordinary grammatical category, the composition may treat it as an unchanged poetic name, sign, figure, place, substance, or force.

Examples of the principle:

```text
Hope waited beneath the light.
Blue crossed the bridge.
Perhaps remained beside the rain.
Return entered the water.
```

The occasional grammatical or semantic strangeness is not automatically an error. It may be part of the poetic encounter.

### Robust template rule

Free words should only be inserted into positions that do not require knowledge of their grammar.

Allowed pattern types may include:

```text
{wish_word} waited beneath the light.
The rain carried {wish_word}.
Between {wish_word} and {return_word}, one path remained.
{return_word} moved beside it.
```

Patterns that should normally be avoided include:

```text
a {wish_word}
more {wish_word}
{wish_word}s
{wish_word}ing
{wish_word}ed
```

The composer must not alter the submitted word in order to make a sentence work.

### Open input questions

- Must the value remain exactly one whitespace-free word?
- Are hyphenated words allowed and counted as one word?
- Is original capitalisation preserved or is a display form derived?
- Are punctuation marks accepted?
- Are numbers or symbols accepted?
- Do wish word and return word follow exactly the same validation rules?

---

## 8. Poetic meaning is created through operators

**Status: Decided direction**

The composer can create meaning without understanding the free words by placing them into curated poetic operations.

Possible operator families include:

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

Examples:

```text
Personification
  {wish_word} waited beneath the window.
  {return_word} answered from the shore.

Materialisation
  The rain carried {wish_word}.
  A feather held {return_word}.

Spatialisation
  Between {wish_word} and {return_word}, a path opened.

Naming
  The distant light was called {wish_word}.
  What returned was named {return_word}.

Inscription
  The rain wrote {wish_word} across the glass.
  The tide left {return_word} in the sand.

Echo
  {wish_word} crossed the water.
  Its echo returned with {return_word}.

Transformation
  What entered as {wish_word} returned as {return_word}.
```

The operator itself creates a proposed relationship. For this reason, not all operators are equally neutral.

A useful provisional distinction is:

```text
low intervention
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

The composer should normally draw more often from low- and medium-intervention forms. Strongly interpretive forms require careful compatibility rules and may remain rare.

---

## 9. Operators are derived from the selected sensory elements

**Status: Decided direction**

The operator pool should not be detached from the selected image, scent, and movement.

The curated elements are known to the Nexus. Their poetic affordances can therefore be described without analysing the free words.

### Image role

The image primarily suggests place, spatial relation, visible structure, and available objects.

Examples:

```text
open starry window
  opening
  framing
  distance
  threshold
  light
  looking outward

bridge in mist
  crossing
  between
  carrying
  connection
  approach
  accompaniment

book on an empty bench
  inscription
  reading
  opening
  keeping
  placing beside
  leaving room
```

### Scent role

The scent primarily suggests atmosphere, memory, temporal depth, and the quality of presence.

Examples:

```text
summer rain
  awakening
  softening
  passing through
  leaving a trace
  nearness

books and cedar
  remembering
  keeping
  rediscovery
  quiet duration

salt air at evening
  distance
  return
  horizon
  fading
  remembrance
```

### Movement role

The movement primarily suggests the event, direction, and relation between the two words.

Examples:

```text
returning tide
  return
  carrying back
  meeting
  homeward movement
  echo

loosening knot
  release
  opening
  untangling
  leaving room

opening circle
  expansion
  invitation
  continuation
  playful change
```

The selected elements should therefore determine a bounded pool of possible poetic movements.

They should not determine one fixed poem.

```text
The elements do not determine the poem.
They determine what kinds of poetic movement are possible.
```

---

## 10. The movement response defines the completion mode

**Status: Decided direction; exact taxonomy remains a working hypothesis**

The return word must not be framed as a solution to the wish word.

The selected continuation of the movement can instead define what completion means in this particular encounter.

```text
The wish word begins a movement.
The return word continues it in the selected way.
The word is not completed.
The shape of the encounter is completed.
```

The current five movement and response pairs suggest these provisional completion modes:

| Movement | Response | Provisional completion mode |
|---|---|---|
| a feather turns as it falls | another feather crosses its path | encounter / crossing |
| a knot slowly loosens | threads gather without tightening | release with gentle connection |
| a tide begins to return | a stream flows back to the sea | convergence / return |
| a circle slowly opens | edges curl into playful waves | expansion / continuation |
| a line of light crosses the floor | a shadow moves alongside | accompaniment / coexistence |

These modes should guide which relational operator templates are available.

For example:

```text
completion mode: accompaniment

compatible
  {wish_word} crossed the light.
  {return_word} moved beside it.

incompatible or strongly disfavoured
  {wish_word} became {return_word}.
```

The movement continuation is therefore not merely one more decorative motif.

It is a candidate for the relational grammar of the composition.

---

## 11. Curated randomness, not unrestricted assembly

**Status: Decided direction**

The composer should first filter by compatibility and only then choose randomly.

```text
selected image, scent, movement, and responses
  -> available motif tags
  -> completion mode
  -> compatible operator families
  -> compatible render-ready templates and fragments
  -> random selection inside that bounded set
```

The system should never blindly combine all valid lines with all other valid lines.

Each selected text unit remains:

- written and reviewed in advance;
- grammatically complete for its permitted slots;
- tagged with compatible motifs or roles;
- usable without conjugating the free words;
- validated before release.

The composer may select and arrange approved forms. It should still not generate grammar.

```text
The composer does not invent grammar.
It chooses and arranges approved poetic forms.
```

---

## 12. Existing language material should be preserved where it helps

**Status: Decided direction**

The current image, scent, movement, response, Resonance Artifact, and Nexus Echo texts should not be discarded merely because the composition becomes more flexible.

They already contain much of the desired tone:

- quietness;
- openness;
- non-solution;
- room for interpretation;
- restrained metaphor;
- sensory clarity;
- careful relational language.

They may continue in several roles:

1. **Canonical works**  
   The five existing complete Echoes may remain unchanged as origin forms.

2. **Curated fragments**  
   Suitable phrases or lines may be detached from one fixed complete path and reused under explicit compatibility rules.

3. **Composition material**  
   Existing long-form lines may remain sensory anchors inside more flexible compositions.

4. **Style references**  
   New library material should be evaluated against their tone and restraint.

5. **Test fixtures**  
   Existing complete paths may remain useful as stable reference cases.

A useful working principle is:

```text
Preserve as much existing language as the new poem can genuinely carry.
Do not preserve a line merely to protect earlier work.
Do not discard a line merely because the architecture has matured.
```

The exact future role of each existing file and line belongs in the later technical audit.

---

## 13. Long-form Resonance Artifact and Nexus Echo have different jobs

**Status: Decided direction**

The two visible poetic outputs should no longer be treated as parallel renderings of the same input.

They have different functions.

### Resonance Artifact

The long form should unfold the encounter with enough coherence that the selected world and relational movement can be followed.

It may:

- retain existing sensory lines;
- establish place and atmosphere;
- show the initial movement;
- show how Person B continues it;
- place the wish word and return word into that movement;
- remain poetic without becoming a prose explanation.

```text
The Resonance Artifact unfolds the encounter.
```

### Nexus Echo

The Echo may be much more condensed, cryptic, surprising, and random.

It may:

- omit some sensory elements;
- merge images;
- reverse familiar relations;
- use fragments rather than full explanatory sentences;
- create unusual noun groups;
- retain ambiguity;
- act as an afterimage rather than a summary.

```text
The Nexus Echo preserves what cannot be fully explained.
```

Kryptic is allowed.

Arbitrary is not.

---

## 14. The Echo should be derived from the completed long-form composition

**Status: Decided direction; minimum linkage rules remain open**

The Echo should not independently reroll from the original Return Artifact as if the long form did not exist.

The preferred sequence is:

```text
Return Artifact
  -> one composition plan
  -> long-form Resonance Artifact
  -> Nexus Echo derived from that completed composition
  -> save both together
```

The Echo may use:

- motifs actually selected for the long form;
- its completion mode;
- its primary or secondary operators;
- concrete verbs or fragments used in the long form;
- transformed combinations of its sensory images;
- the same wish and return words.

Possible minimum linkage rules include:

- both free words remain present;
- at least one sensory motif is inherited;
- at least one movement or relational operator is inherited;
- at least one phrase or verb is drawn from the long-form composition.

The exact minimum should be chosen through poetic prototypes rather than assumed in advance.

---

## 15. Both free words should remain visible in the Nexus Echo

**Status: Decided direction**

The wish word and return word should not disappear in the strongest condensation of the encounter.

Current preferred structure:

```text
wish word
  appears exactly once and unchanged
  appears in line 2, 3, or 4

return word
  appears exactly once and unchanged
  forms the final one-word line
```

The wish word can therefore enter at different moments:

- line 2: it initiates the poetic motion;
- line 3: it enters the crossing or encounter;
- line 4: it appears as the last trace before the answer;
- line 5: the return word remains.

Working formulation:

```text
The wish enters the Echo.
The answer is what remains.
```

---

## 16. The 2-4-6-4-1 Nachhall form remains promising

**Status: Working hypothesis**

The existing Echo form has five lines and the word-count pattern:

```text
2 / 4 / 6 / 4 / 1
```

This form is highly recognisable, compact, and well suited to cryptic compression.

It also gives the return word a strong final position.

However, it should be explicitly re-evaluated under the new composition model rather than preserved by inertia.

Questions to test:

- Can every accepted single word fit without breaking the count?
- How are hyphenated words counted?
- Can the wish word move freely between lines 2, 3, and 4?
- Does the form remain varied across many random runs?
- Are rare alternative Echo forms useful, or would they weaken identity?

Until prototypes show otherwise, the 2-4-6-4-1 form remains the preferred V0.2 Echo structure.

---

## 17. A shared internal composition plan is likely useful

**Status: Working hypothesis**

The long form and Echo should probably be generated from one internal composition decision rather than two unrelated random processes.

A small `CompositionPlan` may record the chosen structural materials, for example:

```json
{
  "completion_mode": "convergence",
  "primary_operator": "return",
  "secondary_operator": "echo",
  "image_fragment_id": "window-light-03",
  "scent_fragment_id": "rain-trace-02",
  "movement_fragment_id": "tide-homeward-04",
  "relation_template_id": "two-directions-meet-01",
  "echo_structure_id": "wish-line-3-02"
}
```

The plan would not contain an interpretation of the free words.

It would only record which curated forms were chosen.

Potential benefits:

- long form and Echo remain related;
- the composition can be inspected during development;
- tests can verify compatibility decisions;
- the selected library forms can be recorded for provenance;
- the completed text remains the final source of truth.

The saved local result should always include the completed visible texts even if a plan is also stored.

---

## 18. The 125-combination map changes role

**Status: Decided direction**

The current Chamber exposes five image families, five scent families, and five movement families.

This produces 125 sensory triples.

The composition map should no longer be understood as a requirement to author exactly 125 fixed Echoes.

Instead, it becomes:

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

The central contract remains:

```text
What the Chamber permits,
the local composition library must be able to express.
```

---

## 19. Preliminary composition sequence

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
  -> load curated source elements
  -> derive motif affordances
  -> determine completion mode
  -> build compatible operator pool
  -> choose a primary and optional secondary operator
  -> choose compatible sensory fragments and transitions
  -> create Composition Plan
  -> compose long-form Resonance Artifact
  -> derive cryptic Nexus Echo from that composition
  -> validate both outputs
  -> atomically save the completed local result
  -> mark the slot opened
```

The future technical design should keep matching, composition, persistence, and revisit behaviour as separate responsibilities.

---

## 20. Preliminary implications for existing technical elements

**Status: Initial orientation only; requires a dedicated audit**

| Existing element | Preliminary direction |
|---|---|
| Resonance Token | retain |
| Person A Chamber selection flow | retain |
| Person B response flow | retain |
| slim Return Artifact | retain; version impact to be reviewed |
| route and Return Slot matching | retain |
| local result persistence | retain and strengthen |
| persistent opener | retain and reorder so existing results are read before composition |
| read-only preview | retain as a development and diagnostic tool |
| current image, scent, and movement libraries | retain and reclassify as source material |
| current long-form renderer | likely refactor into composition-aware stages |
| five canonical Echoes | retain; exact future role remains open |
| exact complete Echo-path matching | replace as the only production route; possibly preserve as canonical or legacy path support |
| no-path rendering failure for valid Chamber combinations | remove through complete generator coverage |
| 125-combination workbook | retain as coverage and test map |

No files should be removed solely on the basis of this preliminary table.

A separate technical audit must inspect each relevant file, responsibility, dependency, and test before any removal or migration decision.

---

## 21. Open questions before implementation

### Free-word input contract

- Exact definition of one word.
- Hyphens, apostrophes, numbers, symbols, and punctuation.
- Capitalisation and display behaviour.
- Input safety without semantic restriction.

### Operator system

- Final operator taxonomy.
- Number of operator families needed for V0.2.
- Compatibility representation: tags, explicit lists, or both.
- Weighting versus simple random choice.
- Whether strong-interpretation operators are included in V0.2.

### Completion modes

- Final names for the five current modes.
- Whether the mode is owned by the movement-response pair or by a broader composition rule.
- Whether future movement responses may share one mode.

### Long-form structure

- How much of the current fixed stanza order should remain.
- Which current lines work as reusable fragments.
- Whether one primary operator and one secondary operator are sufficient.
- How often both free words should appear.

### Echo structure

- Final status of the 2-4-6-4-1 pattern.
- Minimum connection to the long form.
- Degree of allowed image merging and syntactic fragmentation.
- Whether canonical Echoes may appear as random outcomes.

### Persistence

- Exact format of the completed result.
- Whether the `CompositionPlan` is stored beside the visible text.
- How library version and selected fragment IDs are recorded.
- Behaviour when a slot is marked opened but the result file is missing.
- Behaviour when the same unopened Return Artifact is actualised independently on two devices.

### Migration and compatibility

- Whether existing V0.1 Return Artifacts open through the V0.2 composer unchanged.
- Whether a new artifact version is needed.
- Whether canonical V0.1 exact paths remain directly renderable.
- How tests distinguish legacy rendering from the new composition path.

---

## 22. Non-goals

The redesign must not introduce:

- AI-generated poetry;
- online semantic services;
- automatic upload or delivery;
- user accounts;
- tracking;
- a social graph;
- relationship management;
- engagement logic;
- opaque scoring of a player's response;
- quality ranking of wish or return words;
- rejection of an admissible composition after the players have completed it;
- a large general-purpose natural-language grammar engine.

The Nexus continues to manage the artifact, not the relationship.

---

## 23. Recommended next steps

### Step 1: Review this concept record

Check whether it accurately separates:

- settled direction;
- working hypotheses;
- open questions.

Revise it before treating it as an implementation anchor.

### Step 2: Technical audit

Create a separate document:

```text
RESONANCE_TECHNICAL_AUDIT_V0_2.md
```

Inspect each existing component and classify it as:

```text
retain
retain and reframe
modify
replace
archive as legacy
remove
```

No classification should be based on filename alone. The actual responsibility and hidden value of each mechanism must be inspected.

### Step 3: Poetic micro-prototype

Before full integration, prototype a small composition library for three contrasting sensory combinations:

1. one existing canonical path;
2. the mixed starry-window / summer-rain / returning-tide test composition;
3. one contrasting interior or knot-based composition.

Generate many first-opening candidates and review:

- variety;
- coherence;
- visibility of both free words;
- completion-mode fidelity;
- use of existing language;
- relationship between long form and Echo;
- productive versus arbitrary strangeness;
- template repetition.

### Step 4: Define the V0.2 library contract

Only after the micro-prototype succeeds, define:

- fragment schema;
- operator schema;
- compatibility rules;
- composition-plan schema;
- validation rules;
- persistence format.

### Step 5: Integrate first-opening composition

Refine the persistent opener so that:

- an existing completed result is read before any composition runs;
- an unopened valid return is composed once;
- both outputs are saved atomically;
- later openings remain independent of the language library.

### Step 6: Coverage testing

Use the 125-combination map to test all currently admissible sensory combinations across many random runs.

The goal is not to prove literary quality automatically.

The goal is to prove structural safety and complete coverage while leaving poetic judgment to human review.

---

## 24. Current guiding formulations

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
The elements do not determine the poem.
They determine what kinds of poetic movement are possible.
```

```text
The Resonance Artifact unfolds the encounter.
The Nexus Echo preserves what cannot be fully explained.
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
