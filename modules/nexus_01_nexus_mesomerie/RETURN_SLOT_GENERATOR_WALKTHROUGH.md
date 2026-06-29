# Return Slot Generator Walkthrough

Status: practical local walkthrough for the generated-slot return path

This walkthrough shows how to walk through the first generated-slot Return Resonance path.

It is meant to be practical, local, and safe.

Core movement:

```text
Create the waiting place.
Receive the answer.
Open the local memory.
```

This walkthrough uses only safe demo values.

It does not require private activation data.
It does not publish anything online.
It does not modify First Spark.

## What this walkthrough proves

This walkthrough makes the new Return Resonance layer usable by hand:

```text
local workspace
-> generated return slot
-> matching return artifact
-> local result
```

It follows the same path that is protected by the integration test:

```text
test_generated_slot_can_open_matching_return_artifact
```

## Starting point

Run all commands from the repository root:

```bash
cd ~/Schreibtisch/glossai-nexus
```

If needed, update the local clone first:

```bash
git pull --ff-only
```

## Step 1: Create a temporary local workspace

For a safe test run, use `/tmp`:

```bash
mkdir -p /tmp/glossai-quiet-garden/{slots,artifacts,results,notes}
```

This creates:

```text
/tmp/glossai-quiet-garden/
├── slots/
├── artifacts/
├── results/
└── notes/
```

For real private work, use a private local folder outside the public repository, for example:

```text
~/Dokumente/glossai-local/nexus-01-return-workspace/
```

## Step 2: Generate a local return slot

Create a quiet-garden slot:

```bash
python3 modules/nexus_01_nexus_mesomerie/make_return_slot.py \
  --origin-trace-id n01-local-origin-a4m9 \
  --return-slot-id quiet-garden-01 \
  --package-id local-package-garden-01 \
  --result-file return_resonance_quiet_garden.local.md \
  --public-safe-label "quiet garden" \
  --output /tmp/glossai-quiet-garden/slots/return_slots.local.json
```

Expected result:

```text
Slot file created: /tmp/glossai-quiet-garden/slots/return_slots.local.json
Origin trace: n01-local-origin-a4m9
Return slot: quiet-garden-01
Package: local-package-garden-01
Layer: return-resonance-1
```

The generated slot file should contain a waiting slot.

You can inspect it with:

```bash
cat /tmp/glossai-quiet-garden/slots/return_slots.local.json
```

## Step 3: Use the matching demo artifact

The matching safe demo artifact already exists in the repository:

```text
modules/nexus_01_nexus_mesomerie/examples/return_artifact.quiet_garden.demo.txt
```

It matches the generated slot through these fields:

```text
origin_trace_id: n01-local-origin-a4m9
return_slot_id: quiet-garden-01
package_id: local-package-garden-01
layer_id: return-resonance-1
```

For a local walkthrough, you may copy it into the temporary workspace:

```bash
cp modules/nexus_01_nexus_mesomerie/examples/return_artifact.quiet_garden.demo.txt \
  /tmp/glossai-quiet-garden/artifacts/return_artifact.quiet_garden.demo.txt
```

## Step 4: Open the return resonance

Run Return Resonance with explicit local paths:

```bash
python3 modules/nexus_01_nexus_mesomerie/run_return_resonance.py \
  --artifact /tmp/glossai-quiet-garden/artifacts/return_artifact.quiet_garden.demo.txt \
  --slots /tmp/glossai-quiet-garden/slots/return_slots.local.json \
  --output-dir /tmp/glossai-quiet-garden/results
```

Expected behavior:

```text
Match status: match_waiting
Message: The returned artifact fits. A deeper layer of this Nexus becomes readable.

Local result created: /tmp/glossai-quiet-garden/results/return_resonance_quiet_garden.local.md
```

This proves the full generated-slot path:

```text
A slot was generated.
A return answered it.
A local result opened.
```

## Step 5: Inspect the local result

Open the result file:

```bash
less /tmp/glossai-quiet-garden/results/return_resonance_quiet_garden.local.md
```

You should see:

```text
# Return Resonance: quiet-garden-01
```

and the return word:

```text
patience
```

## Step 6: Run it again

Run the same command again:

```bash
python3 modules/nexus_01_nexus_mesomerie/run_return_resonance.py \
  --artifact /tmp/glossai-quiet-garden/artifacts/return_artifact.quiet_garden.demo.txt \
  --slots /tmp/glossai-quiet-garden/slots/return_slots.local.json \
  --output-dir /tmp/glossai-quiet-garden/results
```

Expected behavior:

```text
Local result reused: /tmp/glossai-quiet-garden/results/return_resonance_quiet_garden.local.md
```

This demonstrates:

```text
Generate once.
Revisit often.
```

## Step 7: Try the overwrite protection

If you run the slot generator again with the same output path, it should refuse to overwrite the existing file:

```bash
python3 modules/nexus_01_nexus_mesomerie/make_return_slot.py \
  --origin-trace-id n01-local-origin-a4m9 \
  --return-slot-id quiet-garden-01 \
  --package-id local-package-garden-01 \
  --result-file return_resonance_quiet_garden.local.md \
  --public-safe-label "quiet garden" \
  --output /tmp/glossai-quiet-garden/slots/return_slots.local.json
```

Expected behavior:

```text
Error: output file already exists: ... Use --overwrite to replace it.
```

This is intentional.

The generator should not accidentally overwrite a local/private slot file.

## Step 8: Clean up the temporary workspace

The `/tmp` workspace can be removed after testing:

```bash
rm -rf /tmp/glossai-quiet-garden
```

Do not delete a real private workspace unless you are sure you no longer need it.

## Privacy boundary

This walkthrough uses safe public demo values.

For real use:

```text
keep real return artifacts private
keep local result files private
keep private activation data outside the public repository
do not put real names, email addresses, key material, or private relationship context into public-safe slots
```

The public repository may show the shape.

The local workspace carries the meaning.

## What this walkthrough does not do

This walkthrough does not:

```text
read private activation packages
generate private gift packages
perform encryption
verify identity
publish anything online
append to existing slot files
create multiple slots
```

That is intentional.

This is only the first walkable path through the generated-slot layer.

## Related files

```text
make_return_slot.py
run_return_resonance.py
examples/return_artifact.quiet_garden.demo.txt
RETURN_SLOT_GENERATOR_REVIEW.md
RETURN_SLOT_GENERATOR_INTEGRATION_REVIEW.md
RETURN_RESONANCE_LOCAL_WORKSPACE.md
RETURN_SLOT_FROM_PRIVATE_ACTIVATION.md
```

## Working formulas

```text
Create the waiting place.
Receive the answer.
Open the local memory.
```

```text
The template shows the path.
The generator prepares the place.
The artifact answers.
The local result remembers.
```

```text
The public repo shows the shape.
The private workspace carries the meaning.
```
