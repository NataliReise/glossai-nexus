# Return Resonance

Status: legacy runnable MVP and retained local infrastructure

Current direction: `../CURRENT_DIRECTION.md`

Documentation status: `../RESONANCE_DOCUMENTATION_STATUS_01.md`

Return Resonance is the first small return layer for Nexus 01. It belongs to the Nexus 01 extension layer, not to the First Spark core.

Its durable technical idea remains current:

```text
A waiting slot
A returned artifact
One local answer

Slot -> Artifact -> Local Result
```

Its original generated poetry is not the current compact Nachhall design.

## What remains valuable

This layer established:

- a human-readable return artifact;
- local Return Slot loading;
- explicit route and package matching;
- safe non-match behaviour;
- local result creation;
- generate-once and revisit-often;
- no automatic publication;
- the boundary that First Spark does not depend on Return Resonance.

These responsibilities remain part of the future Nexus even though the poetic result layer is being replaced.

## Legacy poetic boundary

The earlier MVP uses:

```text
return_resonance/artifact.py
return_resonance/result.py
run_return_resonance.py
run_return_resonance_demo.py
```

`result.py` creates an earlier five-line local resonance from legacy fields such as carrier image, return image, movement, tone, and return word.

Do not use that output as guidance for the V0.3 compact Nachhall composer.

The new current direction is:

```text
Chamber selections
+ wish word
+ return word
+ curated compact variants
= one persistent 2 / 4 / 6 / 4 / 1 Nachhall
```

## Boundary to First Spark

First Spark remains complete on its own.

```text
Return Resonance may know about First Spark
First Spark must not depend on Return Resonance
```

## Main earlier-MVP files

```text
return_resonance/
├── __init__.py
├── artifact.py
├── slots.py
├── matching.py
├── result.py
└── tests/
    └── test_return_resonance_mvp.py
```

The package has grown beyond this original set. The complete current dependency map is recorded in:

- `../RESONANCE_DEPENDENCY_AUDIT_01.md`

## Public demo files

```text
../examples/return_slot.demo.json
../examples/return_artifact.demo.txt
../examples/return_artifact.unknown_slot.demo.txt
../examples/return_artifact.quiet_garden.demo.txt
../examples/return_resonance_result.demo.md
```

These are fictional public-safe fixtures.

## Run the earlier public demo

From the repository root:

```bash
python3 modules/nexus_01_nexus_mesomerie/run_return_resonance_demo.py
```

The demo creates or reuses:

```text
modules/nexus_01_nexus_mesomerie/return_resonance_lantern_river.local.md
```

This command demonstrates the earlier MVP. It is not the future V0.3 poetic path.

## Run with explicit local paths

```bash
python3 modules/nexus_01_nexus_mesomerie/run_return_resonance.py \
  --artifact path/to/return_artifact.txt \
  --slots path/to/return_slots.json \
  --output-dir path/to/local-memory
```

Exit codes:

```text
0 -> matched and opened or reused a local result
1 -> artifact did not match a waiting or opened slot
2 -> file parsing slot-loading or result-opening error
```

## Create a local Return Slot

```bash
python3 modules/nexus_01_nexus_mesomerie/make_return_slot.py \
  --origin-trace-id n01-local-origin-a4m9 \
  --return-slot-id quiet-garden-01 \
  --package-id local-package-garden-01 \
  --result-file return_resonance_quiet_garden.local.md \
  --public-safe-label "quiet garden" \
  --output ~/Dokumente/glossai-local/nexus-01-return-workspace/slots/return_slots.local.json
```

The slot generator remains useful and is not deprecated by the poetic redesign.

It:

- uses explicit values only;
- does not inspect First Spark internals;
- does not publish;
- does not claim encryption;
- refuses to overwrite unless explicitly allowed.

## Non-match boundary

The Nexus does not open every return.

```text
It opens only what belongs
to a waiting or already opened slot
```

The unknown-slot public fixture demonstrates this boundary.

## Current migration classification

### Retain

```text
slots.py
matching.py
local-only operation
route identity
generate-once and revisit-often
```

### Split or modify

```text
__init__.py
local_opening.py
resonance_render_bridge.py
persistent opening orchestration
```

### Archive after dependency review

```text
artifact.py as the earlier text-artifact parser
result.py as the earlier poetic result generator
run_return_resonance.py
run_return_resonance_demo.py
focused legacy fixtures and tests
```

No file should move until replacement tests and command documentation exist.

## Related documents

Current:

- `../CURRENT_DIRECTION.md`
- `../RESONANCE_DOCUMENTATION_STATUS_01.md`
- `../RESONANCE_TRANSITION_INVENTORY_01.md`
- `../RESONANCE_DEPENDENCY_AUDIT_01.md`
- `../RETURN_RESONANCE_LOCAL_WORKSPACE.md`

Historical milestones:

- `../RETURN_RESONANCE_MVP.md`
- `../RETURN_RESONANCE_0_1_REVIEW.md`
- `../RETURN_RESONANCE_GENERATED_SLOT_MILESTONE.md`
- `../RETURN_SLOT_GENERATOR_REVIEW.md`
- `../RETURN_SLOT_GENERATOR_INTEGRATION_REVIEW.md`
- `../RETURN_SLOT_GENERATOR_WALKTHROUGH.md`

## Privacy boundary

This remains a local return layer.

Do not commit or publish:

- real return artifacts;
- real local slot files;
- local result files;
- private activation data;
- private gift messages;
- key material.

```text
The public repository may show the shape of a return
It must not expose the private return itself
```
