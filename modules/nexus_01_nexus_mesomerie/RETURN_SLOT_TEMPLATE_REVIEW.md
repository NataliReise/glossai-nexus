# Return Slot Template Review

Status: template bridge and first explicit local generator in place

This document reviews the first Return Resonance slot template.

It marks a small transition:

```text
conceptual boundary
-> copy-before-use template
-> explicit local generator
-> later private activation generator
```

The template does not create private slots automatically.
It gives a safe shape that can be copied into a private local workspace.

A first local generator now exists, but it only accepts explicit safe values.
It does not read private activation packages.

## Template file

The current template is:

```text
templates/return_slot.template.json
```

It is intentionally public-safe and contains only placeholder values.

## First local generator

The first explicit local slot generator is:

```text
make_return_slot.py
```

It writes a local slot JSON file from explicit CLI arguments.

It does not:

```text
read private activations
infer private meaning
generate secret keys
publish anything online
modify First Spark
```

## Why this template exists

The previous boundary document clarified this rule:

```text
A private activation may create a waiting slot.
The slot may be public-safe.
The meaning behind the slot remains private.
```

The template turns that rule into a concrete file shape.

It shows what a slot needs structurally, while making clear that private meaning must not be placed in the public repository.

## What the template provides

The template provides:

```text
an explicit document_status
a template name
a template version
a usage note
a privacy note
a single waiting slot shape
CHANGE-ME placeholders
safe default module and layer IDs
a .local.md result filename pattern
```

This makes it easier to create local slot files without guessing the expected structure.

## Current template shape

```json
{
  "document_status": "template - copy before use",
  "template_name": "Nexus 01 Return Resonance Slot Template",
  "template_version": "N01-RS-TEMPLATE-1",
  "usage": "Copy this file into a private local workspace before filling it with real local values.",
  "privacy_note": "Do not put private gift meaning, real names, contact details, key material, or private relationship context into a public-safe slot.",
  "slots": [
    {
      "origin_trace_id": "n01-local-origin-CHANGE-ME",
      "return_slot_id": "symbolic-slot-id-CHANGE-ME",
      "module_id": "N01",
      "package_id": "local-package-CHANGE-ME",
      "layer_id": "return-resonance-1",
      "status": "waiting",
      "result_file": "return_resonance_symbolic_slot.local.md",
      "public_safe_label": "symbolic label",
      "note": "Do not put private meaning into this slot. The slot only needs to know where to wait."
    }
  ]
}
```

## What this proves

### 1. A slot can be described without private meaning

The slot contains structural fields only.

It can wait for a return without revealing why the return matters.

```text
The slot only needs to know where to wait.
```

### 2. A generator has a clear target shape

The explicit local generator does not need to invent the slot format from scratch.

It fills the same fields the template already names.

### 3. Local users can start manually or with explicit generation

A user can copy the template into a local workspace and fill it by hand.

Alternatively, the explicit generator can write the local slot file from safe CLI values.

This keeps the project usable without adding premature private activation parsing.

### 4. The public/private boundary is visible inside the file

The template itself says:

```text
copy before use
private meaning stays out
local values replace placeholders
```

That makes the privacy boundary visible even when someone opens only the JSON file.

## What the template does not do

The template does not:

```text
generate slot IDs
generate origin trace IDs
read private activations
validate private meaning
create return artifacts
open return results
perform encryption
verify identity
publish anything online
```

It is a shape, not a private activation tool.

## Copy-before-use flow

Recommended manual use:

```bash
mkdir -p ~/Dokumente/glossai-local/nexus-01-return-workspace/{slots,artifacts,results,notes}

cp modules/nexus_01_nexus_mesomerie/templates/return_slot.template.json \
  ~/Dokumente/glossai-local/nexus-01-return-workspace/slots/return_slots.local.json
```

Then edit the copied local file.

Do not edit the template itself for private use.

## Explicit generator flow

Recommended explicit local generation:

```bash
python3 modules/nexus_01_nexus_mesomerie/make_return_slot.py \
  --origin-trace-id n01-local-origin-a4m9 \
  --return-slot-id quiet-garden-01 \
  --package-id local-package-garden-01 \
  --result-file return_resonance_quiet_garden.local.md \
  --public-safe-label "quiet garden" \
  --output ~/Dokumente/glossai-local/nexus-01-return-workspace/slots/return_slots.local.json
```

The generator refuses to overwrite an existing output file unless `--overwrite` is provided.

## Values to replace or provide

A local user should replace or provide:

```text
n01-local-origin-CHANGE-ME
symbolic-slot-id-CHANGE-ME
local-package-CHANGE-ME
return_resonance_symbolic_slot.local.md
symbolic label
```

The replacement values should be local-safe.

They should not expose private identity, private gift meaning, or private relationship context.

## Good local-safe examples

```text
origin_trace_id: n01-local-origin-a4m9
return_slot_id: quiet-garden-01
package_id: local-package-garden-01
result_file: return_resonance_quiet_garden.local.md
public_safe_label: quiet garden
```

## Values to avoid

Avoid values such as:

```text
real names
email addresses
phone numbers
medical details
private event names
private confessions
private relationship labels
real key material
```

## Relationship to current code

The current Return Resonance code already understands the slot shape through:

```text
return_resonance/slots.py
return_resonance/matching.py
return_resonance/result.py
```

The template and generator are intentionally compatible with the current local CLI:

```bash
python3 modules/nexus_01_nexus_mesomerie/run_return_resonance.py \
  --artifact path/to/return_artifact.txt \
  --slots path/to/return_slots.local.json \
  --output-dir path/to/results
```

## Relationship to a future private activation generator

A later generator may read a private activation package locally and derive safe structural slot fields from it.

That is not implemented yet.

The current generator accepts only explicit arguments such as:

```text
--origin-trace-id
--return-slot-id
--package-id
--result-file
--public-safe-label
--output
```

This moves from:

```text
manual template copy
```

to:

```text
safe explicit local slot creation
```

without introducing private activation parsing too early.

## Why not build the full private activation generator yet?

The template and explicit generator give the project time to stabilize the structure.

A private activation generator should come after the fields, naming rules, and privacy boundary feel clear.

```text
First make the shape visible.
Then automate the shape.
Then decide what private activation may safely translate.
```

## Review conclusion

The slot template is a useful bridge.

It is small enough to stay safe.
It is concrete enough to guide local use.
It is stable enough to support a first explicit generator.

Current milestone:

```text
Return slot boundary exists.
Return slot template exists.
Manual local slot creation is possible.
Explicit local slot generation is possible.
A future private activation generator has a clearer target.
```

## Working formulas

```text
The template carries the shape.
The local copy carries the meaning.
```

```text
First make the slot readable.
Then make it generatable.
Then decide what may become automatic.
```

```text
A template is not automation.
A first generator is not a private activation parser.
```
