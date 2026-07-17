# Resonance Documentation Status 01

Status: current documentation index

Decision source: `CURRENT_DIRECTION.md`

Date: 2026-07-17

This file prevents older design and milestone documents from being mistaken for the current Nexus 01 resonance direction.

When documents conflict, use this precedence order:

```text
CURRENT_DIRECTION.md
-> current transition and audit documents
-> active experiment documentation
-> runnable legacy implementation documentation
-> superseded design history
-> archive milestone history
```

---

# 1. Read these first

## Current direction

- `CURRENT_DIRECTION.md`

Defines the compact Nachhall as the complete production resonance form:

```text
2 / 4 / 6 / 4 / 1
```

It supersedes the mandatory V0.2 long-form production direction.

## Current transition control

- `RESONANCE_TRANSITION_INVENTORY_01.md`
- `RESONANCE_DEPENDENCY_AUDIT_01.md`
- `archive/README.md`

These files define classification, dependency boundaries, migration order, and archive rules.

## Production compact path and experimental lineage

The active production files are:

- `return_resonance/compact_generator.py`
- `open_resonance_return.py`

They enforce the five-line `2 / 4 / 6 / 4 / 1` visible contract and persistent
generate-once opening.

- `experiments/nachhall_composition_v0_3/README.md`

This experiment remains poetic review lineage. It is not the production entry
point.

---

# 2. Current stable opening and gift layer

The following remain current in responsibility:

```text
first_spark/
packaging/
chambers/resonance/
return_resonance/slots.py
return_resonance/matching.py
```

Their exact documentation may still contain older milestone wording, but the responsibilities of human choice, local matching, privacy, packaging, and persistent return remain part of the current direction.

Important current entry documents:

- `README.md`
- `first_spark/README.md`
- `first_spark/FIRST_SPARK_0_1_REVIEW.md`
- `packaging/README.md`
- `packaging/GIFT_PACKAGE_PLAN.md`
- `RETURN_RESONANCE_LOCAL_WORKSPACE.md`

---

# 3. Runnable earlier Return Resonance MVP

Status:

```text
legacy runnable implementation
not the future poetic production contract
```

Relevant files and documents:

- `return_resonance/README.md`
- `return_resonance/artifact.py`
- `return_resonance/result.py`
- `run_return_resonance.py`
- `run_return_resonance_demo.py`
- `RETURN_RESONANCE_MVP.md`
- `RETURN_RESONANCE_0_1_REVIEW.md`
- `RETURN_RESONANCE_GENERATED_SLOT_MILESTONE.md`
- `RETURN_SLOT_GENERATOR_REVIEW.md`
- `RETURN_SLOT_GENERATOR_INTEGRATION_REVIEW.md`
- `RETURN_SLOT_GENERATOR_WALKTHROUGH.md`

What remains valuable:

- local slots;
- route matching;
- generate-once and revisit-often;
- local-only storage;
- safe demo boundaries;
- no-overwrite behaviour.

What is not current poetic guidance:

- the earlier generated five-line text in `result.py`;
- legacy carrier-image, return-image, tone, and movement fields as the future resonance contract.

---

# 4. Runnable V0.1 deterministic resonance

Status:

```text
legacy runnable poetic implementation
source lineage for the compact Nachhall
not the future universal production model
```

Relevant files and documents:

- `resonance_language_library/v0_1/STATUS.md`
- `resonance_language_library/v0_1/`
- `resonance_language_library/render_resonance_artifact.py`
- `resonance_language_library/render_nexus_echo.py`
- `resonance_language_library/render_resonance_output.py`
- `resonance_language_library/validate_library.py`
- `RESONANCE_RENDER_PIPELINE_STATUS_V01.md`
- `RESONANCE_RENDER_BRIDGE_STATUS_V01.md`
- `RESONANCE_LOCAL_OPENING_STATUS_V01.md`
- `RESONANCE_RETURN_ARTIFACT_INTEGRATION_V01.md`

What remains valuable:

- original approved Nachhall poems;
- exact `2 / 4 / 6 / 4 / 1` validation;
- strict placeholder validation;
- exact fixtures;
- local deterministic reference behaviour.

What is superseded as future production direction:

- mandatory long-form rendering;
- one exact complete path per supported selection combination;
- the V0.1 language library as a permanent transport identity.

---

# 5. Superseded V0.2 long-form direction

Status:

```text
superseded as production target
retain as design history and source lineage
```

Entry documents:

- `RESONANCE_COMPOSITION_DECISION_UPDATE_01.md`
- `RESONANCE_COMPOSITION_DECISION_UPDATE_02.md`
- `RESONANCE_COMPOSITION_REDESIGN_V0_2.md`
- `RESONANCE_TECHNICAL_AUDIT_V0_2.md`

Experiment:

- `experiments/resonance_composition_v0_2/STATUS.md`
- `experiments/resonance_composition_v0_2/`

What should survive conceptually:

- profiles behind visible wording;
- curated operators;
- static weights;
- seedable tests;
- Same-Word findings;
- signature-strength review;
- anti-formula principles;
- intentional reprise versus accidental template exposure.

What should not be treated as current architecture:

- mandatory long-form Resonance Artifact;
- seven-role long-form assembly;
- Echo derivation from a required long form;
- large long-form Composition Plans;
- full 125-combination long-form coverage as the next release target.

---

# 6. Earlier general design documents

Files such as the following may contain valid concepts but should not override the current direction:

- `RESONANCE_COMPOSITION_AND_POEM_V01.md`
- `NEXUS_ECHO_STANDARD_TEMPLATE_V01.md`
- earlier Return Unlock documents;
- old milestone and integration plans.

Read them as:

```text
historical but technically or poetically relevant
```

The current status of Return Unlock remains described by:

- `RETURN_UNLOCK_CURRENT_DIRECTION.md`

---

# 7. Command status

## Current stable gift command family

```text
run_first_spark.py
packaging/build_first_spark_package.py
packaging/build_first_spark_gift_package.py
packaging/verify_first_spark_package.py
packaging/verify_first_spark_gift_package.py
```

## Earlier MVP return command family

```text
run_return_resonance.py
run_return_resonance_demo.py
make_return_slot.py
```

This family remains runnable history and local infrastructure. Its poetic output is not the V0.3 target.

## Production compact opening and retained V0.1 rendering

```text
open_resonance_return.py
return_resonance/compact_generator.py
resonance_language_library/render_resonance_output.py
```

`open_resonance_return.py` and `compact_generator.py` form the current persistent
compact production path. The language-library renderer remains runnable legacy
lineage and is not invoked for the production visible result.

## V0.2 experimental command family

```text
experiments/resonance_composition_v0_2/prototype_composer.py
experiments/resonance_composition_v0_2/prototype_composer_policy.py
```

Experimental history only.

## Canonical production test command

```text
python3 modules/nexus_01_nexus_mesomerie/run_all_tests.py
```

It covers the production and integration suite, including module-level test
functions, while excluding historical experiment tests.

---

# 8. Archive rule

A file moves to `archive/` only when all of these are true:

```text
active imports have been removed
active tests have replacement coverage
active documentation links have been updated
historical execution instructions remain understandable
archive README explains the lineage
```

No active code may import from `archive/`.

No gift package may include `archive/` or `experiments/` by default.

---

# 9. Compact orientation

```text
Need the current vision?
  Read CURRENT_DIRECTION.md

Need the transition plan?
  Read RESONANCE_TRANSITION_INVENTORY_01.md

Need the technical dependency map?
  Read RESONANCE_DEPENDENCY_AUDIT_01.md

Need the current experiment?
  Read experiments/nachhall_composition_v0_3/README.md

Need to understand an old renderer or decision?
  Use this status index before reading the historical document
```
