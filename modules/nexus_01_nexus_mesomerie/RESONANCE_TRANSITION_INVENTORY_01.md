# Resonance Transition Inventory 01

Status: current transition working document

Decision source: `CURRENT_DIRECTION.md`

Purpose: classify the existing Nexus 01 resonance material before any archive movement, deletion, or production-path switch.

This inventory is responsibility-based. A file may leave production while remaining valuable as executable history, migration support, poetic lineage, or a test reference.

## Classification vocabulary

```text
CURRENT
  defines the present direction or active user-facing system

ACTIVE_EXPERIMENT
  current experimental work; not yet production

RETAIN
  responsibility remains part of the future Nexus

REUSE_OR_EXTRACT
  selected concepts or validators should survive in new code

SUPERSEDED
  useful history but not current implementation guidance

ARCHIVE_AFTER_DEPENDENCY_REVIEW
  should leave the active tree only after imports, tests, and links are mapped

REMOVE_FROM_HEAD_LATER
  no continuing visible reference value after consolidation; Git history is sufficient

UNDECIDED
  requires inspection before classification
```

## A. Current direction and active gift layer

### CURRENT

- `CURRENT_DIRECTION.md`
- `archive/README.md`
- `first_spark/`
- `packaging/`

### RETAIN

First Spark remains the opening movement and a stable small playable seed.

The packaging layer remains valuable for:

- local personal gift creation;
- public/private separation;
- explicit verification;
- manual sharing;
- no automatic upload or social tracking.

No First Spark gameplay expansion is required merely because the resonance production layer changes.

## B. Resonance Chamber and human-choice layer

### RETAIN

- `chambers/resonance/choices.py`
- `chambers/resonance/flow.py`
- `chambers/resonance/terminal_io.py`
- the stable image, scent, movement, and response IDs;
- the ordered human choice sequence;
- the two free words;
- Chamber-owned response compatibility.

### MODIFY_LATER

- centralise free-word validation;
- clarify current documentation where it refers to complete deterministic render paths;
- avoid embedding full poetic libraries directly into player-facing choice objects.

## C. Transport, matching, and local memory

### RETAIN

- stable route and package identity;
- Return Slot ownership;
- waiting/opened state;
- slot matching;
- result-path ownership by the slot;
- local-only operation;
- no-overwrite behaviour;
- atomic new-file writing;
- generate-once and revisit-often behaviour.

Likely files include:

- `return_resonance/matching.py`
- `return_resonance/slots.py`
- the transport portions of `return_resonance/resonance_render_bridge.py`
- the persistence portions of `open_resonance_return.py`

### MODIFY_LATER

- separate matching from poetic production;
- check for an existing completed result before loading any composition library;
- loosen matching from legacy poetic artifact fields where possible;
- define a compact completed-result contract for the Nachhall;
- test recovery from partial slot/result updates.

## D. V0.1 deterministic resonance system

### ARCHIVE_AFTER_DEPENDENCY_REVIEW

Candidate directory and related files:

```text
resonance_language_library/v0_1/
resonance_language_library/render_resonance_artifact.py
resonance_language_library/render_nexus_echo.py
resonance_language_library/render_resonance_output.py
resonance_language_library/validate_library.py
resonance_language_library/tests/
```

### Historical value

V0.1 demonstrated:

- a deterministic local rendering chain;
- five exact canonical compositions;
- the original Nachhall form `2 / 4 / 6 / 4 / 1`;
- strict path matching;
- strict placeholder and word-count validation;
- no-improvisation failure;
- exact-output fixtures and tests.

### REUSE_OR_EXTRACT

- exact five-line validation;
- runtime word counts;
- strict placeholder checks;
- clear error messages;
- typed rendered-result precedent;
- approved short-form examples as poetic lineage.

### Superseded production behaviour

- mandatory exact full-path matching for every supported Chamber combination;
- deterministic long-form stanza rendering as the normal visible result;
- direct independent rendering of long form and Echo from the same artifact.

## E. Earlier Return Resonance MVP

### UNDECIDED_PENDING_DEPENDENCY_REVIEW

Candidate material includes:

- `return_resonance/artifact.py`
- `return_resonance/result.py`
- earlier text-artifact examples, demos, and tests;
- early Return Resonance milestone documents.

The old parser and result generator may still be imported by demos or tests. They must not move before those dependencies are mapped.

Historical value includes the origin of local result persistence and the first generate-once/revisit-often behaviour.

## F. V0.2 long-form composition direction

### SUPERSEDED_AS_PRODUCTION_TARGET

- `RESONANCE_COMPOSITION_DECISION_UPDATE_01.md`
- `RESONANCE_COMPOSITION_DECISION_UPDATE_02.md`
- `RESONANCE_COMPOSITION_REDESIGN_V0_2.md`
- `RESONANCE_TECHNICAL_AUDIT_V0_2.md`
- `experiments/resonance_composition_v0_2/`

### ARCHIVE_AFTER_NEW_EXPERIMENT_CONFIRMATION

The V0.2 experiment should eventually move as a coherent historical system rather than be dismantled piecemeal.

It demonstrated:

- poetic profiles instead of direct quotation;
- weighted routes and reviewed complete-line blocks;
- seedable local composition;
- inspectable Composition Plans;
- linked Echo derivation;
- Same-Word route work;
- signature-strength review;
- anti-formula policy;
- relation/remainder pairing analysis;
- the limits of long-form combinatorial composition for this Nexus.

### REUSE_OR_EXTRACT

- profile lineage from Chamber choices;
- curated operator vocabulary;
- static weighting ideas;
- Same-Word safety findings;
- anti-formula principles;
- phrase-family and signature-strength observations;
- local seed injection for tests;
- the distinction between intentional reprise and template exposure.

### Do not carry forward automatically

- mandatory seven-role long-form assembly;
- a long-form Resonance Artifact as prerequisite for the final poem;
- large Composition Plans designed around long-form provenance;
- pair-weight machinery that is unnecessary in a five-line Nachhall.

## G. New compact Nachhall experiment

### ACTIVE_EXPERIMENT

```text
experiments/nachhall_composition_v0_3/
```

The experiment should test:

- the Nachhall as the complete resonance result;
- exact `2 / 4 / 6 / 4 / 1` structure;
- several small micro-routes;
- curated phrase variants rather than unrestricted word slots;
- one controlled metaphorical leap;
- one or more sensory anchors;
- wish word exactly once in line 2, 3, or 4;
- return word exactly once in line 5;
- Same-Word behaviour;
- local seeded reproducibility for tests;
- enough surface variation without a large grammar engine.

## H. Documentation cleanup

### SUPERSEDED documents should receive one of

```text
status banner in place
move to archive design_history
consolidate and remove from current head
```

### REMOVE_FROM_HEAD_LATER candidates

Only after a content map is created:

- duplicate temporary summaries;
- superseded checklists whose decisions are fully preserved elsewhere;
- repeated status snapshots without unique technical or poetic evidence.

No file should be deleted merely because its filename contains an older version number.

## I. Controlled migration phases

### Phase 1 — completed by this transition start

- record current Nachhall direction;
- define archive policy;
- create this initial inventory;
- create the isolated V0.3 experiment area.

### Phase 2 — next

- add visible superseded status markers to the V0.2 long-form entry documents;
- search imports, fixtures, command references, and documentation links;
- produce a precise file-by-file move map;
- establish active and historical test commands.

### Phase 3

- build the compact Nachhall microprototype in parallel;
- compare generated samples with original V0.1 Nachhalle;
- confirm that no mandatory long form is needed.

### Phase 4

- define the compact production contract;
- integrate the new Nachhall composer with first opening and persistence;
- preserve result reuse independently of later library changes.

### Phase 5

- switch the active production entry point;
- move V0.1 and V0.2 historical systems in one controlled archive migration;
- update imports, links, and test commands;
- verify that active code has no imports from `archive/`.

## Immediate stop rule

Do not start moving runtime files yet.

The next repository operation should be a dependency and documentation-link audit, followed by visible superseded markers. This prevents a tidy-looking tree from hiding broken commands or lost historical context.
