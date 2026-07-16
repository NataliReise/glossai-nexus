# Resonance Dependency Audit 01

Status: current transition audit — repository pass completed

Decision source: `CURRENT_DIRECTION.md`

Audit date: 2026-07-17

Purpose: identify the runtime, test, documentation, and packaging dependencies that must be migrated before V0.1 or V0.2 material can move into the intentional archive.

## Audit boundary

This pass used repository file inspection and repository-wide search. It did not execute the local test suite in a fresh checkout.

The findings therefore distinguish:

```text
confirmed source dependency
confirmed documentation reference
inferred migration requirement
local execution still required
```

No runtime file is moved by this audit.

---

# 1. Executive result

The current repository contains three different resonance generations:

```text
Earlier Return Resonance MVP
  human-readable Return Artifact
  -> simple generated local Markdown result

V0.1 deterministic render path
  JSON Resonance Return Artifact
  -> fixed long-form Resonance Artifact
  -> exact approved 2 / 4 / 6 / 4 / 1 Nexus Echo

V0.2 long-form experiment
  poetic profiles and weighted routes
  -> composed long form
  -> linked compact Echo
```

The new current direction is a fourth generation:

```text
V0.3 compact Nachhall direction
  Chamber selections and two free words
  -> curated micro-route and phrase variants
  -> one complete 2 / 4 / 6 / 4 / 1 Nachhall
  -> persistent local result
```

The main cleanup risk is not V0.2. V0.2 is deliberately isolated from production.

The main cleanup risk is the coexistence of two still-runnable older return paths:

```text
run_return_resonance.py
  -> earlier human-readable artifact and result.py

open_resonance_return.py
  -> richer JSON artifact and V0.1 deterministic language library
```

Both paths currently have tests and documentation. Neither may be moved merely for tidiness.

---

# 2. Runtime dependency graph

## 2.1 Package-level transitive dependency

### `return_resonance/__init__.py`

The package exports both the earlier MVP result helpers and the later local-opening helpers:

```text
artifact.py
result.py
local_opening.py
matching.py
slots.py
...
```

Important consequence:

```text
import return_resonance
  -> imports local_opening
  -> imports resonance_render_bridge
  -> imports resonance_language_library.render_resonance_output
```

This means that even callers using only the earlier parser or matcher may transitively load the V0.1 rendering path through the package initializer.

Migration requirement:

- stop treating `return_resonance/__init__.py` as a broad eager-export surface;
- prefer narrow module imports for active code;
- or defer renderer-specific imports until after the new opening seam exists;
- add a test proving that transport and matching can load without any legacy poetic renderer.

This package-level coupling must be removed before the V0.1 library can move.

## 2.2 Earlier human-readable Return Resonance path

### `run_return_resonance.py`

Directly imports from `return_resonance`:

```text
parse_return_artifact
load_return_slots
match_return_artifact
open_return_result
```

Flow:

```text
human-readable artifact text
-> legacy ReturnArtifact
-> slot match
-> result.py
-> generated local Markdown
```

### `run_return_resonance_demo.py`

Uses the same earlier path with public-safe fixtures.

### `return_resonance/result.py`

Depends on:

```text
return_resonance.artifact.ReturnArtifact
return_resonance.matching.MatchResult
return_resonance.matching.MatchStatus
```

It contains:

- the first generate-once/revisit-often implementation;
- direct local file creation;
- a five-line generated resonance unrelated to the later Nachhall contract;
- legacy poetic fields such as carrier image, return image, tone, and movement.

Classification:

```text
ARCHIVE_AFTER_DEPENDENCY_REVIEW
```

Migration requirement:

- preserve the persistence concept, not the legacy poem;
- decide whether the old text artifact CLI remains an explicit legacy demonstration;
- remove its exports from the active package surface when the new transport path becomes canonical;
- move its demo, fixtures, and focused tests together if archived.

## 2.3 Rich JSON artifact and V0.1 rendering path

### `return_resonance/resonance_render_bridge.py`

Direct imports:

```text
resonance_language_library.render_resonance_output
  RenderedResonanceOutput
  ResonanceOutputRenderError
  render_resonance_output
```

Current combined responsibility:

```text
transport dataclasses and JSON validation
+ route adaptation
+ slot matching
+ V0.1 poetic rendering
```

Reusable responsibilities:

- `ChamberSelections` transport fields;
- `ResonanceReturnArtifact` identity and serialization;
- exact field validation;
- adaptation to the existing route matcher.

Replacement responsibilities:

- `OpenedResonanceReturn` as a V0.1-render-specific combined type;
- `open_resonance_return` as a function that matches and renders in one step;
- the hard-coded `LANGUAGE_LIBRARY = "resonance-en-v0.1"` production assumption.

Migration requirement:

```text
transport parsing
!=
route matching
!=
poetic composition
```

These responsibilities must become separate seams before archive movement.

### `open_resonance_return.py`

Direct dependencies include:

```text
resonance_language_library.render_resonance_output.default_library_dir
return_resonance.resonance_render_bridge.open_resonance_return
OpenedResonanceReturn
```

Current order:

```text
load artifact
load slots
match and render through V0.1
then check whether a completed result already exists
```

This means a revisit still depends on the V0.1 library even though the completed result should be sufficient.

Required order:

```text
load transport artifact
load slots
match route without composing
resolve result path

if completed result exists
  read it
  do not load any composition library
  optionally repair waiting state
  return

if slot is opened and result is missing
  fail through an explicit recovery policy

if slot is waiting and result is absent
  compose one compact Nachhall
  write it atomically
  mark the slot opened
  return
```

Reusable code:

- CLI boundary;
- result path owned by the matched slot;
- atomic new-file replacement;
- no-overwrite behaviour;
- slot-state update;
- privacy reminder;
- calm errors.

### `return_resonance/local_opening.py`

Current preview flow:

```text
load
-> match
-> render full V0.1 output in memory
```

It directly imports the V0.1 default library and the render bridge.

Future classification:

```text
RETAIN_AND_REFRAME
```

Future preview should be one of:

```text
validation preview
  checks transport and slot compatibility only

candidate preview
  creates an explicitly ephemeral Nachhall
  warns that it is not the saved first-opening result
```

The validation-only option is the leaner default.

---

# 3. V0.1 language-library dependency set

The following currently form one legacy rendering unit:

```text
resonance_language_library/v0_1/
resonance_language_library/render_resonance_artifact.py
resonance_language_library/render_nexus_echo.py
resonance_language_library/render_resonance_output.py
resonance_language_library/validate_library.py
resonance_language_library/tests/
```

The internal chain is:

```text
render_resonance_output.py
  -> render_resonance_artifact.py
  -> render_nexus_echo.py

renderers
  -> resonance_language_library/v0_1/*.json

validator and exact-output tests
  -> the same V0.1 data and fixtures
```

Historical and reusable value:

- the original `2 / 4 / 6 / 4 / 1` Nachhall form;
- five approved canonical compact poems;
- exact five-line and word-count validation;
- strict placeholder validation;
- explicit no-path failure;
- useful JSON loading and error patterns;
- exact-output fixtures as regression history.

Superseded production behaviour:

- fixed long-form stanza rendering as the mandatory visible result;
- exact six-ID path matching as the only way to obtain a compact poem;
- independent sibling rendering of long form and Echo;
- hard coupling of transport parsing to a particular visible language library.

Move rule:

```text
Do not move individual V0.1 files piecemeal.
Move the data, renderers, fixtures, tests, and legacy README as one coherent unit
only after active imports and commands no longer depend on them.
```

---

# 4. Test dependency map

## 4.1 Earlier MVP tests

### `return_resonance/tests/test_return_resonance_mvp.py`

Directly protects:

- human-readable artifact parsing;
- slot loading and matching;
- `open_return_result` generation and reuse;
- missing-result behaviour for an opened slot;
- `run_return_resonance_demo.py`;
- `run_return_resonance.py`;
- slot generation;
- the First Spark import boundary.

It therefore belongs to the earlier MVP unit while also containing reusable matching and persistence intentions.

Required later split:

```text
active transport/matching tests
legacy text-artifact/result tests
shared persistence invariants
```

## 4.2 Rich JSON bridge tests

### `return_resonance/tests/test_resonance_render_bridge.py`

Protects:

- transport serialization;
- strict artifact fields and versions;
- V0.1 language-library identity;
- slot matching through the bridge;
- exact rendered outputs.

Classification:

```text
LEGACY_INTEGRATION_TEST_AFTER_REPLACEMENT
```

Reusable intentions:

- transport round-trip;
- unknown-field rejection;
- route mismatch rejection;
- calm errors.

Exact V0.1 poem assertions should not become V0.3 production assertions.

## 4.3 Persistent opener tests

### `return_resonance/tests/test_open_resonance_return.py`

Protects:

- first opening creates a local result;
- slot state changes to opened;
- second opening reuses the existing file;
- no overwrite;
- missing result for opened slot fails;
- mismatch creates no result.

These are high-value active behaviours.

Required new critical test:

```text
an existing completed result opens successfully
when the composition library is missing changed or invalid
```

## 4.4 V0.1 library tests

### `resonance_language_library/tests/`

Includes exact tests for:

- library validation;
- long-form rendering;
- Nexus Echo rendering;
- combined output;
- five canonical fixtures.

Classification:

```text
PRESERVE_WITH_V0_1_ARCHIVE
```

## 4.5 V0.2 experiment tests

The V0.2 prototype tests import files inside the experiment and do not form part of the production opening path.

They should move with the V0.2 experiment as historical executable evidence.

## 4.6 Active test commands after migration

The future active suite should make these boundaries explicit:

```text
First Spark tests
transport and Chamber tests
slot and matcher tests
compact Nachhall structural tests
persistent first-opening and revisit tests
packaging and privacy tests
archive-reference guard
```

Legacy V0.1 and V0.2 tests may remain runnable through explicit historical commands, but should not be mistaken for production acceptance.

No test command was executed during this repository-only audit.

---

# 5. V0.2 isolation and archive readiness

The V0.2 composer declares itself independent from the V0.1 production opener and imports only standard-library modules at its entry point.

Repository inspection found its implementation, policy, libraries, tests, probe series, and reviews under:

```text
experiments/resonance_composition_v0_2/
```

No active production import from that experiment was identified in this audit.

This makes V0.2 the easier archive candidate.

However, it should not move until:

- root design documents are visibly classified as superseded;
- documentation links are updated;
- its own internal relative commands are checked after the planned new location;
- an archive README explains what was learned and what survived into V0.3.

Recommended future unit:

```text
archive/resonance_v0_2_longform_composer/
  README.md
  experiment/
  design_history/
```

Do not dismantle the experiment into unrelated fragments. Its value lies partly in preserving the full chain from idea to probe evidence and abandonment decision.

---

# 6. Packaging audit

The current First Spark preview builder explicitly copies:

```text
run_first_spark.py
create_local_activation.py
activation.example.json
first_spark/
```

It does not recursively package the complete Nexus 01 module and does not include the V0.1 or V0.2 resonance systems.

Consequences:

- moving resonance implementation files later should not break the current First Spark package builder;
- the current gift package remains a First Spark package, not yet a complete Nexus-with-Nachhall package;
- a future complete gift package needs an explicit inclusion list for the compact resonance path;
- that inclusion list should never copy `archive/` or `experiments/` by default.

Required future packaging guard:

```text
active gift package contains no archive directory
active gift package contains no experiment directory
active gift package contains only the selected production Nachhall library
```

---

# 7. Documentation status map

## 7.1 Current sources of truth

```text
CURRENT_DIRECTION.md
RESONANCE_TRANSITION_INVENTORY_01.md
RESONANCE_DEPENDENCY_AUDIT_01.md
RESONANCE_DOCUMENTATION_STATUS_01.md
archive/README.md
experiments/nachhall_composition_v0_3/README.md
```

## 7.2 Current runnable but legacy poetic implementation

```text
return_resonance/README.md
RESONANCE_RENDER_PIPELINE_STATUS_V01.md
RESONANCE_RENDER_BRIDGE_STATUS_V01.md
RESONANCE_LOCAL_OPENING_STATUS_V01.md
RESONANCE_RETURN_ARTIFACT_INTEGRATION_V01.md
resonance_language_library/v0_1/STATUS.md
```

These may describe code that still runs, but they do not define the new poetic production direction.

## 7.3 Superseded V0.2 direction

```text
RESONANCE_COMPOSITION_DECISION_UPDATE_01.md
RESONANCE_COMPOSITION_DECISION_UPDATE_02.md
RESONANCE_COMPOSITION_REDESIGN_V0_2.md
RESONANCE_TECHNICAL_AUDIT_V0_2.md
experiments/resonance_composition_v0_2/
```

These should be read as design history and source lineage, not implementation guidance.

## 7.4 Earlier MVP and milestone history

Documents such as the Return Resonance MVP, 0.1 review, slot milestones, generator reviews, and earlier local workspace guides remain useful for historical responsibilities and local-first safety.

They should be consolidated later into:

```text
current operational guides
historical milestone notes
archive design history
```

They do not need immediate deletion.

---

# 8. File-by-file move map

## Keep active now

```text
first_spark/
packaging/
chambers/resonance/
return_resonance/slots.py
return_resonance/matching.py
return_resonance/token.py
return_resonance/artifact_store.py
return_resonance/writer.py
make_return_slot.py
```

Some of these require later documentation or interface updates, but their responsibilities survive.

## Split before any move

```text
return_resonance/__init__.py
return_resonance/resonance_render_bridge.py
return_resonance/local_opening.py
open_resonance_return.py
```

## Keep temporarily as one runnable earlier-MVP unit

```text
return_resonance/artifact.py
return_resonance/result.py
run_return_resonance.py
run_return_resonance_demo.py
examples/return_artifact*.txt
examples/return_resonance_result.demo.md
relevant portions of test_return_resonance_mvp.py
```

## Keep temporarily as one runnable V0.1 unit

```text
resonance_language_library/v0_1/
resonance_language_library/render_resonance_artifact.py
resonance_language_library/render_nexus_echo.py
resonance_language_library/render_resonance_output.py
resonance_language_library/validate_library.py
resonance_language_library/tests/
relevant bridge and opener integration tests
```

## Archive coherently after V0.3 confirmation

```text
experiments/resonance_composition_v0_2/
RESONANCE_COMPOSITION_DECISION_UPDATE_01.md
RESONANCE_COMPOSITION_DECISION_UPDATE_02.md
RESONANCE_COMPOSITION_REDESIGN_V0_2.md
RESONANCE_TECHNICAL_AUDIT_V0_2.md
```

## Remove from current head only after consolidation

No file is approved for deletion yet.

Duplicate summaries and temporary checklists may later be removed after their unique decisions have been mapped into the current documentation or archive README.

---

# 9. Required guards before physical archive migration

## Source guards

- active Python must not import from `archive/`;
- active Python must not import from `experiments/`;
- transport and matching must import without loading a poetic renderer;
- reopening an existing completed result must not load the composition library;
- the active package initializer must not eagerly import legacy renderers.

## Test guards

- baseline First Spark tests pass;
- matching and slot tests pass;
- V0.3 structural tests pass;
- first-opening persistence tests pass;
- a saved result survives missing or changed library files;
- archive-reference guard passes;
- package verifiers pass.

## Documentation guards

- module README points first to `CURRENT_DIRECTION.md`;
- superseded V0.2 documents carry visible status;
- V0.1 docs say `legacy runnable implementation`, not `current direction`;
- commands are separated into active and historical sections;
- archive READMEs explain execution status and lineage.

## Packaging guards

- no private files;
- no archive files;
- no experimental files;
- no absolute local paths;
- only production libraries are copied.

---

# 10. Controlled migration order

## Phase A — documentation clarity

```text
create current documentation index
update the module README
mark V0.1 as legacy runnable
mark V0.2 as superseded
```

## Phase B — compact experiment

```text
build V0.3 Nachhall composer in isolation
review seeded samples
confirm final small-form contract
```

## Phase C — active code seam

```text
slim return_resonance package imports
separate transport from matching
separate matching from composition
check existing result before composer loading
```

## Phase D — production switch

```text
integrate compact Nachhall composer
persist one completed poem
reuse it unchanged
update active tests and gift packaging
```

## Phase E — archive migration

```text
move V0.2 as one coherent historical unit
move V0.1 only after all active dependencies are removed
move earlier MVP only after its explicit legacy fate is decided
run active tests and historical smoke tests
verify no active archive imports
```

---

# 11. Current conclusion

The repository is not yet ready for physical movement of V0.1 or the earlier MVP.

It is ready for:

```text
clear documentation classification
+ compact V0.3 experimentation
+ planned separation of active seams
```

The V0.2 long-form experiment is source-isolated and can likely be archived first after documentation cleanup and path verification.

The V0.1 renderer cannot move until the package initializer, render bridge, local preview, persistent opener, integration tests, and command documentation have been migrated.

The safest next implementation step remains:

```text
build the smallest useful V0.3 Nachhall prototype
without changing the current runnable paths
```
