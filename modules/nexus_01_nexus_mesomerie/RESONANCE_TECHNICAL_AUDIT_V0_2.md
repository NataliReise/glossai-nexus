# Resonance Technical Audit V0.2

This document audits the current Nexus 01 Return Resonance implementation against the consolidated direction in `RESONANCE_COMPOSITION_REDESIGN_V0_2.md`.

It classifies responsibilities before any production refactor, archive migration, or deletion.

The audit focuses on the active technical path from Chamber choice to persistent local result. Historical planning notes are grouped separately and should receive a documentation pass before archive movement.

No runtime code or data file is changed by this audit.

---

## 1. Audit principles

Each component is classified as one of:

```text
retain
retain and reframe
modify
replace as production path
archive as legacy after dependency review
remove later only if proven unused
```

The classification is based on responsibility rather than filename.

Two questions are kept separate:

```text
Does this component still belong in the production path

Does this component still contain technical or poetic value
```

A component may leave production while remaining valuable as history, profile lineage, a test fixture, or a design reference.

---

## 2. Executive findings

The current implementation already has a useful separation between:

- Chamber-owned choices and interaction;
- transport identity;
- Return Slot matching;
- local rendering;
- result persistence;
- read-only preview behaviour.

The redesign does not require a whole-module rewrite.

The main production change is concentrated in this sequence:

```text
current
  Chamber selections
  -> V0.1 transport artifact
  -> exact deterministic long-form renderer
  -> exact complete Echo path
  -> persistent Markdown result

future
  Chamber selections
  -> stable transport artifact
  -> poetic profiles and completion mode
  -> one local Composition Plan
  -> new long-form composition
  -> linked cryptic Echo
  -> persistent completed result
```

The strongest reusable technical assets are:

- stable choice IDs;
- the Chamber interaction boundary;
- token-to-artifact route identity;
- Return Slot matching;
- result-path ownership by the slot;
- create-once and reuse behaviour;
- atomic new-file writing;
- explicit no-overwrite behaviour;
- structural Echo word-count validation.

The strongest replacement candidates are:

- fixed visible V0.1 language forms as normal production output;
- fixed stanza assembly;
- exact complete Echo-path matching;
- combined match-and-render orchestration before result reuse is checked.

---

## 3. Current dependency map

```text
chambers/resonance/choices.py
  -> player-facing options and one-to-one response compatibility

chambers/resonance/flow.py
  -> runs Chamber grammar
  -> returns ChamberSelections

chambers/resonance/composer.py
  -> joins ChamberSelections to ResonanceToken
  -> builds ResonanceReturnArtifact

return_resonance/resonance_render_bridge.py
  -> defines ChamberSelections and ResonanceReturnArtifact
  -> parses transport JSON
  -> adapts route identity to ReturnArtifact
  -> matches Return Slot
  -> invokes complete V0.1 rendering

resonance_language_library/render_resonance_output.py
  -> invokes long-form renderer
  -> invokes Echo renderer
  -> joins both visible outputs

resonance_language_library/render_resonance_artifact.py
  -> loads fixed V0.1 forms
  -> verifies selected IDs and compatibility
  -> assembles fixed stanzas

resonance_language_library/render_nexus_echo.py
  -> finds one exact approved complete path
  -> inserts free words
  -> validates 2 / 4 / 6 / 4 / 1

open_resonance_return.py
  -> loads artifact and slots
  -> currently matches and renders first
  -> then checks for an existing result
  -> writes a new result once
  -> marks slot opened

return_resonance/local_opening.py
  -> read-only load match and render preview
```

---

## 4. Resonance Chamber choice catalog

### File

`chambers/resonance/choices.py`

### Current responsibility

- owns five image choices;
- owns five image responses;
- owns five scent choices;
- owns five scent responses;
- owns five movement choices;
- owns five movement responses;
- validates known IDs;
- validates one-to-one response compatibility;
- provides player-facing labels.

### Finding

The stable IDs and player-facing choices remain central to V0.2. The visible labels describe the choices the players actually make; they are not the same thing as the old render-ready poem lines.

The current one-to-one compatibility tables also preserve the selected answer and movement continuation. They remain useful even when the visible poem becomes non-deterministic.

The file documentation currently says that the catalog seed contains five complete paths approved by the rendering library. That description will become outdated once exact complete render paths are no longer the production model.

### Classification

**Retain and reframe.**

### Recommended action

- keep current IDs unless the poetic prototype discovers a concrete choice problem;
- keep player-facing labels;
- keep Chamber-owned response compatibility;
- revise V0.1-specific documentation later;
- do not embed poetic profiles directly into `ChoiceOption` yet;
- create a separate profile layer keyed by the stable choice IDs.

### Reason for a separate profile layer

The Chamber owns what the player may choose. The composition library owns what poetic forces those choices make available.

```text
Chamber choice ID
  != visible poem line
  != full poetic profile object
```

This keeps the Chamber mechanically clear and the composition system independently versionable.

---

## 5. Chamber flow and input boundary

### Files

- `chambers/resonance/flow.py`
- `chambers/resonance/terminal_io.py`

### Current responsibility

- defines a small `ChamberIO` protocol;
- supports scripted and terminal adapters;
- runs the fixed sequence of choices;
- returns typed `ChamberSelections`;
- currently accepts any non-empty whitespace-free free word.

### Finding

The separation between Chamber grammar and user-interface adapter is strong and should survive.

The current word validation is too permissive for the new contract. Values such as hyphenated forms, digits, punctuation-only tokens, or symbol sequences may pass because only whitespace is rejected.

The same rule is duplicated in scripted and terminal input paths and is weaker again inside `ChamberSelections`.

### Classification

**Retain and modify.**

### Recommended action

- keep `ChamberIO`, `ScriptedChamberIO`, `TerminalChamberIO`, and the ordered Chamber flow;
- introduce one shared Unicode-aware free-word validator;
- use that validator in all input adapters and artifact parsing;
- preserve the submitted lexical value;
- derive the capitalised poetic display form only during composition;
- improve player-facing error text to state the letter-only rule.

### Important ownership rule

Free-word admissibility belongs to the Chamber contract and transport validation, not to one particular renderer.

---

## 6. Chamber-to-transport integration seam

### File

`chambers/resonance/composer.py`

### Current responsibility

- runs the Chamber flow;
- joins selections to validated Resonance Token identity;
- returns both selections and the transport artifact;
- deliberately performs no rendering, slot matching, file writing, or Atrium state work.

### Finding

This is a good narrow boundary and closely matches the new architecture.

However, the name `composer.py` may become confusing once V0.2 introduces an actual poetic composer.

### Classification

**Retain; consider a later clarity rename.**

### Recommended action

- preserve the responsibility unchanged;
- do not mix poetic generation into this file;
- consider renaming it later to `artifact_builder.py` or another transport-focused name;
- delay any rename until imports and documentation are audited.

---

## 7. Stable transport artifact

### File

`return_resonance/resonance_render_bridge.py`

### Current valuable responsibilities

- `ChamberSelections` typed data;
- `ResonanceReturnArtifact` JSON transport contract;
- joining token identity to selections;
- exact field validation;
- route adaptation for the existing matcher;
- loading the shared JSON artifact.

### Current problematic responsibility

The same module also performs Return Slot matching and immediately invokes the deterministic renderer through `open_resonance_return`.

This combines:

```text
transport parsing
route matching
poetic production
```

The V0.2 first-opening order requires these to be separated.

### Classification

**Retain and split.**

### Recommended action

Retain or extract:

- `ChamberSelections`;
- `ResonanceReturnArtifact`;
- `build_resonance_return_artifact`;
- `parse_resonance_return_artifact`;
- `load_resonance_return_artifact`;
- route-identity adaptation.

Replace or move:

- `OpenedResonanceReturn` as a render-specific combined object;
- `open_resonance_return` as the function that both matches and renders.

A future separation may resemble:

```text
load transport artifact
match route and slot
resolve result path
reuse existing completed result if present
otherwise invoke V0.2 composition
```

### Artifact-version finding

The current JSON artifact already carries all human choices required to select profiles and a completion mode. V0.2 may therefore be able to accept V0.1 artifacts unchanged.

A new artifact version is not yet justified merely because the local composition process changes.

The `language_library` field does require review. It currently names `resonance-en-v0.1`, which directly identifies the old visible rendering library. Possible futures include:

- interpret it as the source choice/profile lineage version;
- add a separate local composition-library version only to the saved result;
- introduce a new transport version only if the field semantics cannot remain honest.

This remains open until the prototype and persistence schema are designed.

---

## 8. Legacy human-readable Return Artifact

### File

`return_resonance/artifact.py`

### Current responsibility

- parses the earlier human-readable `NEXUS RETURN ARTIFACT` format;
- contains earlier fields such as carrier image, movement, return image, and tone;
- supplies the route-shaped `ReturnArtifact` object used by matching.

### Finding

The new JSON `ResonanceReturnArtifact` is the active richer transport contract, but it adapts itself back into this older object for matching.

The route matcher needs only stable route identity and the return word; it does not need most legacy poetic fields.

### Classification

**Retain as legacy temporarily; extract route identity later.**

### Recommended action

- do not delete while matching, old demos, and tests still depend on it;
- consider introducing a small route identity protocol or dataclass shared by both artifact formats;
- let the matcher depend on route identity rather than on the full legacy artifact;
- after migration, archive the old human-readable parser and its examples if they no longer serve production.

---

## 9. Return Slot matching

### Files

- `return_resonance/matching.py`
- `return_resonance/slots.py`

### Current responsibility

- identifies a slot by origin trace and return slot ID;
- verifies package and layer identity;
- distinguishes waiting from opened slots;
- stores result-file ownership in the slot;
- loads persistent local slot state.

### Finding

These responsibilities are independent of the poetic renderer and remain strongly aligned with V0.2.

The matcher is currently typed to the legacy `ReturnArtifact`, which should eventually be loosened or adapted through a smaller route identity type.

### Classification

**Retain with a small future interface refinement.**

### Recommended action

- preserve match statuses and route checks;
- preserve slot-owned result filenames;
- keep waiting/opened state;
- later remove the unnecessary dependency on legacy poetic artifact fields;
- add path-safety validation for `result_file` during the persistence contract review;
- keep local state separate from any remote or social relationship logic.

---

## 10. V0.1 language data

### Directory

`resonance_language_library/v0_1/`

### Current files

```text
images.json
image_responses.json
scents.json
scent_responses.json
movements.json
movement_responses.json
echo_paths.json
README.md
```

### Current responsibility

The V0.1 library contains:

- approved player-facing source text;
- fixed Resonance Artifact lines;
- fixed response lines;
- five exact complete Echo paths;
- deterministic compatibility and rendering data.

### Finding

The directory is the most important source corpus for deriving V0.2 poetic profiles, but it should not remain the normal visible production library.

It contains two different kinds of value that should be separated during migration:

```text
choice and profile lineage
  motifs
  atmosphere
  direction
  relational logic

legacy visible output
  fixed long-form lines
  exact complete Echo paths
```

### Classification

**Retain as source lineage; archive visible V0.1 production data after profile extraction and dependency migration.**

### Recommended action

- do not edit the V0.1 data into V0.2 in place;
- create a separate V0.2 prototype area;
- derive profiles from the old formulations with documented lineage;
- keep the old directory intact until legacy tests and documentation are relocated;
- later move it into an intentional archive or clearly mark it as legacy, depending on import stability.

---

## 11. V0.1 long-form renderer

### File

`resonance_language_library/render_resonance_artifact.py`

### Current responsibility

- loads all six fixed element and response documents;
- validates IDs and compatibility;
- capitalises free words;
- assembles a fixed five-part stanza structure;
- renders old language forms directly;
- appends fixed free-word sentences.

### Finding

This renderer embodies the visible determinism the redesign intends to remove.

Its useful responsibilities are smaller than the file as a whole:

- safe JSON loading patterns;
- ID lookup error handling;
- compatibility validation;
- initial-capital display behaviour;
- typed rendered-result precedent.

Its production assembly logic should not govern V0.2.

### Classification

**Replace as production path; retain temporarily as legacy renderer and reference.**

### Recommended action

- do not incrementally add randomness to this renderer;
- build the V0.2 composer separately;
- preserve exact V0.1 behaviour until archive and migration decisions are complete;
- reuse concepts rather than copying the entire implementation;
- move free-word validation to a shared contract.

---

## 12. V0.1 Nexus Echo renderer

### File

`resonance_language_library/render_nexus_echo.py`

### Current responsibility

- finds one exact complete path through a full `requires` match;
- inserts wish and return words;
- rejects unknown placeholders;
- validates exactly five lines;
- validates `2 / 4 / 6 / 4 / 1` at runtime;
- fails rather than improvising when no exact path exists.

### Finding

Exact path matching is incompatible with the V0.2 production model, but several structural validators are valuable.

The future Echo must be derived from the newly composed long form, not selected independently from `echo_paths.json`.

### Classification

**Replace as production path; extract structural validation concepts; preserve as legacy renderer.**

### Recommended action

Retain in V0.2 form:

- exact five-line validation;
- runtime word counts;
- strict placeholder validation;
- explicit error reporting;
- the final one-word line contract.

Replace:

- exact full-path matching;
- the five canonical paths as privileged production outcomes;
- no-path failure for otherwise admissible Chamber combinations;
- direct Echo derivation from the Return Artifact alone.

The current word-count tokenizer also needs review because it accepts apostrophes and hyphens while the new input and line policy avoids them.

---

## 13. Combined rendering facade

### File

`resonance_language_library/render_resonance_output.py`

### Current responsibility

- renders the long form and Echo independently from the same artifact;
- combines them into one visible text block;
- provides a small result dataclass and command-line interface.

### Finding

V0.2 requires the Echo to depend on the completed long form and shared Composition Plan. The current facade instead invokes two sibling renderers independently.

The idea of returning a typed object containing both outputs remains useful.

### Classification

**Replace orchestration; retain the typed combined-output pattern.**

### Recommended action

Create a new V0.2 composition service that produces:

```text
Composition Plan
long-form Resonance Artifact
Nexus Echo derived from that long form
combined visible output
```

Do not make the old facade silently switch semantics while legacy tests still import it.

---

## 14. Persistent local opener

### File

`open_resonance_return.py`

### Current valuable responsibilities

- command-line entry point;
- artifact and slot loading;
- result path derived from matched slot;
- create-once behaviour;
- reuse of existing local content;
- refusal to overwrite;
- temporary-file replacement for new results;
- persistent slot-state update;
- privacy reminder.

### Critical sequencing finding

The function currently calls `open_resonance_return`, which matches **and renders**, before it checks whether the completed result file already exists.

Therefore a revisit still depends on the V0.1 library and can fail before reaching the saved result.

This contradicts the intended rule:

```text
completed result exists
  -> read it
  -> do not invoke any composer or library
```

### Classification

**Retain and reorder substantially.**

### Recommended V0.2 sequence

```text
load transport artifact
load slots
match route and slot without composing
resolve result path

if completed result exists
  -> read result
  -> optionally repair waiting state to opened
  -> return

if slot is opened and result is missing
  -> fail clearly under the chosen recovery policy

if slot is waiting and no result exists
  -> invoke V0.2 composer once
  -> write completed result atomically
  -> mark slot opened
  -> return
```

### Persistence refinement

The current code writes the result atomically and then updates slot state separately. A crash between those operations can leave a result file with a waiting slot. This is recoverable because the result exists, but the recovery policy should become explicit and tested.

The reverse state, opened slot with missing result, is already rejected clearly and should remain an explicit case.

### Result format finding

The current Markdown result is human-readable and useful, but V0.2 may need a machine-readable sidecar or structured JSON result containing:

- completed long-form text;
- completed Echo text;
- word counts;
- Composition Plan or provenance fields;
- composition-library version;
- source artifact identity.

The visible Markdown may remain as a presentation artifact. The structured completed result should become the durable source of truth if reliable revisiting and future display formats are desired.

---

## 15. Read-only local opening preview

### File

`return_resonance/local_opening.py`

### Current responsibility

- loads artifact and slots;
- matches and renders in memory;
- writes no result;
- changes no slot state.

### Finding

This is useful as a diagnostic boundary, but its meaning changes under real randomness.

A V0.2 preview that composes a full candidate may produce a poem different from the later persistent first opening. That is not necessarily wrong, but it must not be mistaken for the future saved result.

### Classification

**Retain and reframe.**

### Possible future modes

```text
validation preview
  proves that the artifact matches
  proves that compatible profile pools exist
  does not create a final poem

candidate preview
  creates an explicitly ephemeral sample
  warns that the saved first opening may differ
```

The diagnostic function should no longer be forced through the legacy combined render bridge.

---

## 16. Earlier MVP result generator

### File

`return_resonance/result.py`

### Current responsibility

- implements an earlier human-readable Return Artifact result;
- creates a simple five-line generated resonance from legacy fields;
- implements an earlier generate-once and revisit-often rule.

### Finding

This file is not the current rich JSON rendering path, but it contains historical evidence for the persistence concept.

Its poetic output and legacy fields should not be merged into V0.2.

### Classification

**Archive as legacy after dependency review.**

### Recommended action

- identify remaining imports, demos, and tests;
- preserve it with the earlier human-readable artifact path;
- extract no production poetry from it;
- retain its historical role in explaining the origin of result persistence.

---

## 17. Validation layer

### File group

- `resonance_language_library/validate_library.py`
- V0.1 validator tests

### Current responsibility

The V0.1 validator checks:

- valid JSON;
- consistent versions;
- unique IDs;
- existing references;
- compatibility references;
- approved render lines;
- exact Echo word pattern;
- line-specific Echo requirements.

### Finding

The validator architecture is valuable, but most schema rules are V0.1-specific.

### Classification

**Retain the validation approach; create a new V0.2 validator.**

### Future V0.2 checks should include

- unique profile and template IDs;
- all Chamber choices have profiles;
- every movement-response pair has a completion mode;
- every admissible sensory triple has a non-empty compatible composition pool;
- all templates use only permitted placeholders;
- no template grammatically modifies a free word;
- punctuation policy is respected;
- every Echo has five lines and `2 / 4 / 6 / 4 / 1`;
- wish appears exactly once in line 2, 3, or 4;
- return appears exactly once in line 5;
- both words use display forms rather than rewritten values;
- Echo linkage metadata identifies a motif, operator, and lexical fragment inherited from the long form.

Poetic quality must remain a human review task.

---

## 18. Tests

### Exact V0.1 renderer tests

Files include:

- `resonance_language_library/tests/test_render_resonance_artifact.py`
- `resonance_language_library/tests/test_render_nexus_echo.py`
- shared exact-output fixtures.

These tests intentionally assert five exact outputs and exact path IDs.

### Classification

**Preserve as legacy tests while V0.1 remains accessible; do not convert them into V0.2 production tests.**

### Reusable test intentions

Retain conceptually:

- unknown IDs fail safely;
- incompatible response pairs fail safely;
- unsupported versions fail safely;
- missing library files fail clearly;
- unknown placeholders fail;
- runtime word-count validation remains enforced.

Replace for V0.2:

- exact long-form equality as the main success test;
- exact canonical Echo equality;
- exact-path ID requirement;
- no-improvisation failure for valid mixed combinations.

### Persistent opener tests

`return_resonance/tests/test_open_resonance_return.py` already verifies:

- first opening creates a result;
- slot becomes opened;
- second opening reuses local modifications without overwrite;
- opened slot with missing result is rejected;
- mismatch creates no output and changes no state.

These are strong behavioural tests and should be retained with updated types and composition fixtures.

A new critical test must prove:

```text
an existing completed result opens successfully
when the composition library is missing broken or changed
```

### New random-composition tests

V0.2 should test invariants rather than exact poems:

- all 125 sensory triples can compose;
- many random seeds or injected random sources remain structurally valid;
- both free words remain present under their exact rules;
- selected profile influences are represented in plan metadata;
- completion-mode compatibility is never violated;
- Echo linkage conditions are cumulative;
- repeated runs produce more than one valid composition where the pool permits;
- saved results never reroll.

For deterministic tests, randomness should be injectable even though production first openings use fresh local randomness.

---

## 19. Documentation and status files

Current repository notes include multiple V0.1 milestone, review, integration, and status documents.

Examples found during this audit include:

- `RETURN_RESONANCE_MVP.md`
- `RETURN_RESONANCE_0_1_REVIEW.md`
- `RETURN_RESONANCE_INTEGRATION_PLAN.md`
- `RETURN_RESONANCE_SLOTS.md`
- `RETURN_UNLOCK_CURRENT_DIRECTION.md`
- `RESONANCE_RETURN_ARTIFACT_INTEGRATION_V01.md`
- `RESONANCE_RENDER_BRIDGE_STATUS_V01.md`
- `RESONANCE_RENDER_PIPELINE_STATUS_V01.md`
- `RESONANCE_LOCAL_OPENING_STATUS_V01.md`
- `RETURN_SLOT_GENERATOR_WALKTHROUGH.md`
- `RETURN_SLOT_GENERATOR_INTEGRATION_REVIEW.md`
- `RETURN_RESONANCE_GENERATED_SLOT_MILESTONE.md`

### Finding

These documents are valuable development history, but several will describe V0.1 mechanisms as current production direction after V0.2 is introduced.

### Classification

**Retain now; later divide into current documentation and intentional archive history.**

### Recommended documentation pass

Each file should later receive one of:

```text
current
historical but still technically relevant
superseded by V0.2
archive milestone
```

Do not delete milestone documents merely because the implementation has matured.

---

## 20. Intentional archive proposal

The archive should not be created as a dumping ground.

A possible later structure is:

```text
archive/
  resonance_v0_1/
    README.md
    language_library/
    renderers/
    fixtures/
    earlier_mvp/
    design_history/
```

The archive README should explain:

- what V0.1 demonstrated;
- which ideas survived into V0.2;
- why deterministic visible rendering was replaced;
- how old formulations informed poetic profiles;
- which files remain executable legacy references;
- which files are documentation only.

No movement should occur before import and test paths are updated in one controlled migration.

---

## 21. Recommended target module boundaries

The exact filenames remain open, but V0.2 should aim for responsibilities similar to:

```text
chambers/resonance/
  choices.py
    player-facing choices and Chamber compatibility

  flow.py
    Chamber grammar and free-word collection

return_resonance/
  transport.py
    selections and shared artifact parsing

  matching.py
    route and slot matching

  profiles.py
    load and validate poetic profiles

  completion_modes.py
    movement-response relational grammar

  composition_plan.py
    inspectable selected structure

  compose_long_form.py
    new visible Resonance Artifact

  compose_echo.py
    linked cryptic 2 / 4 / 6 / 4 / 1 Echo

  completed_result.py
    structured persisted result contract

  opening.py
    first-opening and revisit orchestration
```

This is a responsibility sketch, not a frozen file plan.

---

## 22. Migration order

The safest implementation order is:

### 1. Preserve the current baseline

- do not move V0.1 files yet;
- retain all current tests;
- document the audit commit.

### 2. Build the poetic micro-prototype outside production

- create three small profile combinations;
- define provisional completion modes;
- generate long forms and linked Echoes;
- inject randomness for repeatable tests;
- review many outputs manually.

### 3. Define V0.2 contracts

- shared free-word validator;
- profile schema;
- operator and form schema;
- Composition Plan;
- completed-result persistence schema;
- library version semantics.

### 4. Implement new composition as a parallel path

- do not alter the V0.1 renderer in place;
- add V0.2 structural tests;
- add coverage tests.

### 5. Reorder persistent opening

- separate matching from composition;
- check result existence before any composer is loaded;
- persist completed result once;
- retain no-overwrite and privacy behaviour.

### 6. Switch production entry point

- route new openings through V0.2;
- preserve explicit legacy commands or tests only where useful.

### 7. Archive V0.1 intentionally

- update imports and documentation first;
- move files in one controlled step;
- keep lineage documentation.

---

## 23. Decisions supported by the audit

The audit supports these current conclusions:

```text
The Chamber choices can remain.
The transport identity can largely remain.
The Return Slot model can remain.
The matching logic can remain.
The persistent opening principle can remain.

The visible deterministic render path should not remain production.
The exact Echo paths should not remain production.
The old texts should inform profiles rather than surface verses.
The existing result must be checked before any future composer runs.
```

---

## 24. Remaining technical questions

The next stages still need to decide:

- whether the transport artifact stays version `0.1`;
- future semantics of `language_library`;
- exact Unicode word validation;
- whether completed results use JSON plus Markdown or one structured format;
- how a result file and slot-state update recover from partial completion;
- final profile and operator schemas;
- final completion-mode names;
- whether preview means validation-only or ephemeral candidate generation;
- exact archive location and timing.

These questions do not block the poetic micro-prototype.

---

## 25. Audit conclusion

The redesign is a bounded replacement of the poetic production layer, not a rejection of the current Nexus structure.

```text
retain the human choices
retain the route
retain the local opening
retain the memory

replace the deterministic surface
with a curated field of possibilities
```

The next recommended step is the **poetic micro-prototype**, built in parallel and without changing the active V0.1 opening path.