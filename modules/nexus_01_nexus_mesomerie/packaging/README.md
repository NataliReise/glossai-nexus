# Nexus 01 Packaging

This folder contains small packaging helpers for **Nexus 01 - Nexus-Mesomerie**.

The preferred private gift boundary is now the two-mode preparation command:

```bash
python3 modules/nexus_01_nexus_mesomerie/packaging/prepare_nexus_gift.py --help
```

It prepares files locally only. It never uploads, sends, syncs, or tracks a gift.

## Prepare a normal First Spark gift

Create a validated `first-spark` activation and delegate to the unchanged
standalone First Spark gift builder:

```bash
python3 modules/nexus_01_nexus_mesomerie/packaging/prepare_nexus_gift.py \
  first-spark \
  --gift-label first-gift \
  --recipient-alias recipient_name \
  --private-message "A local gift is waiting." \
  --zip
```

To accept an existing activation instead, add:

```text
--activation path/to/activation.local.json
```

The preparation command validates it through the actual First Spark runtime
parser and requires `profile_id` to be `first-spark` before building.

## Prepare a Resonance gift and private Return Workspace

```bash
python3 modules/nexus_01_nexus_mesomerie/packaging/prepare_nexus_gift.py \
  resonance \
  --gift-label resonance-gift \
  --recipient-alias recipient_name \
  --private-message "A local gift is waiting." \
  --public-safe-label "resonance path" \
  --zip
```

The command prints the travelling outputs separately from the retained private
workspace:

```text
Travelling gift: .../nexus-01-resonance-gift-resonance-gift/
Travelling ZIP: .../nexus-01-resonance-gift-resonance-gift.zip
Private Return Workspace: .../n01-return-workspace-<opaque-id>/
```

The travelling gift contains `first_spark/activation.local.json` and
`resonance_token.local.json`. The private workspace contains the matching Return
Slot, the persistent compact opening runtime, an empty `incoming/` directory,
and an empty `results/` directory. The workspace never enters the gift folder or
ZIP. When the existing Resonance Chamber requests the token path, the recipient
enters:

```text
resonance_token.local.json
```

The generated token and slot are checked for identical `module_id`, `layer_id`,
`origin_trace_id`, `return_slot_id`, and `package_id`. Structural IDs are opaque
random values and are not derived from the recipient alias or private message.

Preparation refuses existing destinations. It stages and validates all outputs
before publishing them; there is deliberately no overwrite option.

Keep the Return Workspace private. After the recipient deliberately transfers
the Return Artifact back, copy its JSON file into the workspace's `incoming/`
directory and run:

```bash
./OPEN_RETURN.sh
```

The launcher requires Python 3.11 or newer. It uses only workspace-relative
runtime, slot, and results paths. It automatically opens the sole JSON file in
`incoming/`; if more than one is present, it refuses ambiguity and asks for one
explicit path:

```bash
./OPEN_RETURN.sh incoming/returned-artifact.json
```

The saved result is created once in `results/`. Reopening returns the saved
content unchanged, including later manual edits. The launcher never sends,
moves, renames, or deletes the returned Artifact.

Verify a published Resonance gift and its retained slot independently:

```bash
python3 modules/nexus_01_nexus_mesomerie/packaging/verify_resonance_gift_package.py \
  path/to/nexus-01-resonance-gift-resonance-gift \
  --private-slot path/to/n01-return-workspace-opaque/private/return_slots.local.json
```

Verify the private workspace independently:

```bash
python3 modules/nexus_01_nexus_mesomerie/packaging/verify_return_workspace.py \
  path/to/n01-return-workspace-opaque \
  --gift path/to/nexus-01-resonance-gift-resonance-gift
```

The current helpers build and verify two package types for:

```text
Nexus 0.1 - First Spark
```

The packages are meant for manual, social-analog sharing: for example as a local folder, ZIP file, email attachment, messenger file, cloud link, or USB stick.

They do not upload, post, send, or track anything automatically.

## Current milestone

The First Spark package workflow now has a small complete shape:

```text
preview package: build, ZIP, verify
personal gift package: build, ZIP, verify
```

The preview package is public-safe and must not contain `activation.local.json`.

The personal gift package is local-only and must contain `activation.local.json`.

Both workflows are intentionally manual at the sharing boundary.

## Build a First Spark preview package

From the repository root, run:

```bash
python3 modules/nexus_01_nexus_mesomerie/packaging/build_first_spark_package.py
```

This creates:

```text
dist/nexus-01-first-spark-preview/
```

The package contains:

```text
START_HERE.sh
README_FOR_PLAYER.md
SHORT_NOTE_FOR_TESTER.md
run_first_spark.py
create_local_activation.py
activation.example.json
first_spark/
```

It does not copy private local files such as:

```text
activation.local.json
*.local.json
*.local.txt
*.local.md
__pycache__/
.git/
```

## Build and replace an existing package

```bash
python3 modules/nexus_01_nexus_mesomerie/packaging/build_first_spark_package.py --overwrite
```

## Build a ZIP archive

```bash
python3 modules/nexus_01_nexus_mesomerie/packaging/build_first_spark_package.py --overwrite --zip
```

This also creates:

```text
dist/nexus-01-first-spark-preview.zip
```

## Verify the preview package

After building the preview package, run:

```bash
python3 modules/nexus_01_nexus_mesomerie/packaging/verify_first_spark_package.py
```

The verifier checks the default preview package folder:

```text
dist/nexus-01-first-spark-preview/
```

It verifies that the expected public package files are present, that `START_HERE.sh` is executable, and that private or generated files such as `activation.local.json`, `*.local.json`, `*.local.txt`, `*.local.md`, `__pycache__/`, `.git/`, and Python bytecode are not present.

You can also verify a specific package folder:

```bash
python3 modules/nexus_01_nexus_mesomerie/packaging/verify_first_spark_package.py path/to/package-folder
```

Recommended preview build-and-check flow:

```bash
python3 modules/nexus_01_nexus_mesomerie/packaging/build_first_spark_package.py --overwrite --zip
python3 modules/nexus_01_nexus_mesomerie/packaging/verify_first_spark_package.py
```

## Build a First Spark personal gift package

Read the planning note first:

```text
modules/nexus_01_nexus_mesomerie/packaging/GIFT_PACKAGE_PLAN.md
```

Create a local activation file if it does not exist yet:

```bash
python3 modules/nexus_01_nexus_mesomerie/first_spark/create_local_activation.py
```

Review and edit the generated local activation file:

```text
modules/nexus_01_nexus_mesomerie/first_spark/activation.local.json
```

Then build the local gift package:

```bash
python3 modules/nexus_01_nexus_mesomerie/packaging/build_first_spark_gift_package.py --gift-label first-gift --zip
```

This creates a local package such as:

```text
dist/nexus-01-first-spark-gift-first-gift/
dist/nexus-01-first-spark-gift-first-gift.zip
```

The gift builder requires `activation.local.json`, validates that it is a JSON object, copies it into the package, and writes a recipient README plus a gift note.

It does not commit, upload, send, sync, or track anything.

## Verify the personal gift package

After building a gift package, run:

```bash
python3 modules/nexus_01_nexus_mesomerie/packaging/verify_first_spark_gift_package.py dist/nexus-01-first-spark-gift-first-gift
```

The gift verifier checks that the expected package files are present, that `START_HERE.sh` is executable, and that `activation.local.json` is present and valid JSON with an object at the top level.

It rejects `.git/`, `__pycache__/`, `.pytest_cache/`, Python bytecode, local result files, local return files, and extra `*.local.json` files other than `activation.local.json`.

Recommended gift build-and-check flow:

```bash
python3 modules/nexus_01_nexus_mesomerie/packaging/build_first_spark_gift_package.py --gift-label first-gift --overwrite --zip
python3 modules/nexus_01_nexus_mesomerie/packaging/verify_first_spark_gift_package.py dist/nexus-01-first-spark-gift-first-gift
```

## Test the package manually

After building the preview package, run:

```bash
cd dist/nexus-01-first-spark-preview
./START_HERE.sh
```

After building a gift package, use the generated folder name, for example:

```bash
cd dist/nexus-01-first-spark-gift-first-gift
./START_HERE.sh
```

Alternative start command inside either package:

```bash
python3 run_first_spark.py
```

## Sharing checklist

Before sharing a package manually, check:

```text
1. The package was built intentionally.
2. The matching verifier passed.
3. The package folder or ZIP was reviewed locally.
4. No unintended local result or return files are present.
5. The package is shared manually, not by an automated workflow.
```

## Design boundary

The package builder supports the artifact.

It must not manage the relationship.

Working rule:

```text
The artifact may travel digitally.
The resonance should be carried socially.
```
