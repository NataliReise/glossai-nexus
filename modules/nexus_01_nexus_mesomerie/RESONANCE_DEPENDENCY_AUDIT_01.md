# Resonance Dependency Audit 01

Status: current transition audit

Decision source: `CURRENT_DIRECTION.md`

Purpose: identify concrete dependencies that must be migrated before V0.1 or V0.2 files can move into the intentional archive.

This document records only dependencies inspected in the first transition pass. It is not yet a complete repository-wide import graph.

## 1. Current V0.1 rendering chain is still wired into active opening code

### `return_resonance/resonance_render_bridge.py`

Direct imports:

```text
resonance_language_library.render_resonance_output
  RenderedResonanceOutput
  ResonanceOutputRenderError
  render_resonance_output
```

The bridge also imports and adapts the older human-readable `ReturnArtifact` for slot matching.

Current combined responsibility:

```text
transport parsing
+ route adaptation
+ slot matching
+ V0.1 poetic rendering
```

Migration requirement:

- preserve the transport dataclasses and JSON validation;
- preserve route adaptation temporarily;
- split matching from poetic production;
- replace the rendered-output type only after the compact Nachhall contract exists.

## 2. Persistent opener depends on V0.1 before checking saved results

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
then check whether the result file already exists
```

This means a revisit still depends on the V0.1 library even when a completed local result is already present.

Migration requirement:

```text
load artifact
load slots
match without composing
resolve result path
if result exists
  read and return it
else
  compose one compact Nachhall
  persist it
  mark slot opened
```

The current atomic new-file write, no-overwrite behaviour, privacy reminder, and slot-state update remain valuable.

## 3. Read-only preview also depends directly on V0.1

### `return_resonance/local_opening.py`

Direct dependencies include:

```text
resonance_language_library.render_resonance_output.default_library_dir
return_resonance.resonance_render_bridge.open_resonance_return
OpenedResonanceReturn
```

The current preview means:

```text
load
match
render full V0.1 output in memory
```

Migration question:

The future preview should be explicitly one of:

```text
validation preview
  proves artifact and slot compatibility only

candidate preview
  creates an ephemeral Nachhall and warns that it is not the saved result
```

No decision is required before the V0.3 microprototype works.

## 4. Earlier MVP result generator remains coupled to legacy artifact types

### `return_resonance/result.py`

Direct dependencies:

```text
return_resonance.artifact.ReturnArtifact
return_resonance.matching.MatchResult
return_resonance.matching.MatchStatus
```

It contains:

- an earlier generate-once/revisit-often implementation;
- an earlier five-line generated resonance;
- direct file writing without the later atomic replacement helper;
- legacy poetic fields such as carrier image, returned image, tone, and movement.

Current classification:

```text
ARCHIVE_AFTER_DEPENDENCY_REVIEW
```

Do not merge its legacy poetry into V0.3. Preserve its historical persistence role until imports, demos, and tests are mapped.

## 5. Search findings for `render_resonance_output`

The first repository search found references in:

```text
resonance_language_library/render_resonance_output.py
RESONANCE_RENDER_PIPELINE_STATUS_V01.md
return_resonance/local_opening.py
return_resonance/resonance_render_bridge.py
RESONANCE_TECHNICAL_AUDIT_V0_2.md
open_resonance_return.py
resonance_language_library/tests/test_render_resonance_output.py
return_resonance/tests/test_resonance_render_bridge.py
```

This proves that the V0.1 renderer cannot yet be moved as a directory-only cleanup.

The active opener, preview, bridge, and tests must be migrated or explicitly retained first.

## 6. Immediate no-move set

The following should remain in place during the V0.3 poetic experiment:

```text
resonance_language_library/v0_1/
resonance_language_library/render_resonance_artifact.py
resonance_language_library/render_nexus_echo.py
resonance_language_library/render_resonance_output.py
resonance_language_library/validate_library.py
resonance_language_library/tests/
return_resonance/resonance_render_bridge.py
return_resonance/local_opening.py
open_resonance_return.py
return_resonance/tests/test_resonance_render_bridge.py
```

Their status is now clearer, but their paths must remain stable until the replacement seam is implemented and tested.

## 7. Safe reusable seam

The most promising migration seam is:

```text
ResonanceReturnArtifact
  keep transport fields and validation

match_return_artifact
  keep route and slot validation

compact Nachhall composer
  new isolated responsibility

completed local result
  reuse create-once and no-overwrite behaviour
```

The future compact composer should not be inserted into `resonance_render_bridge.py` merely by replacing one import. The bridge currently owns too many responsibilities and should first be split into transport, matching, and composition orchestration.

## 8. Remaining audit work

Before archive movement, search and classify:

- all imports of `resonance_language_library`;
- all imports of `return_resonance.artifact` and `return_resonance.result`;
- all CLI and README commands referencing old renderers;
- all exact-output fixtures;
- all tests that expect long-form output;
- all links into `experiments/resonance_composition_v0_2/`;
- packaging inclusion rules that may copy superseded files;
- module-level README statements that call V0.1 or V0.2 current.

## 9. Current conclusion

The repository can be made unambiguous immediately through direction and status documents, but physical archive movement must wait.

The active code still uses V0.1 as its rendering implementation. The V0.2 long-form system is isolated and can be archived more easily later, but only after its documentation references and any test commands have been mapped.

The safe next technical move is therefore:

```text
build the V0.3 compact Nachhall experiment
while preserving all current runtime paths
```

The safe next cleanup move is:

```text
complete the dependency and documentation-link map
before moving any executable directory
```
