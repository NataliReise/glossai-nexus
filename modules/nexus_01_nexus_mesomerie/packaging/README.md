# Nexus 01 Packaging

This folder contains small packaging helpers for **Nexus 01 - Nexus-Mesomerie**.

## Prepare a Neutral Nexus Carrier

The canonical corrected travelling product is the **Neutral Nexus Carrier**: an
activation-ready Nexus with no completed activation and no preselected mode.

```bash
python3 modules/nexus_01_nexus_mesomerie/packaging/prepare_neutral_nexus_carrier.py \
  --output-dir dist \
  --carrier-label sunday-gift \
  --zip
```

Optionally attach one strictly validated Token V2 as an inert sidecar:

```text
--token path/to/resonance_token.v2.json
```

The unchanged bytes are stored at
`invitation/resonance_token.v2.json`. Presence alone has no effect. Normal
activation leaves it unused; Token activation requires the recipient to choose
that path deliberately. The Token may instead travel separately.

Verify the directory and ZIP independently:

```bash
python3 modules/nexus_01_nexus_mesomerie/packaging/verify_neutral_nexus_carrier.py \
  dist/nexus-01-neutral-carrier-sunday-gift

python3 modules/nexus_01_nexus_mesomerie/packaging/verify_neutral_nexus_carrier.py \
  --zip dist/nexus-01-neutral-carrier-sunday-gift.zip
```

The carrier contains neither a Return Slot nor a private Return Workspace. All
transport remains manual.

The earlier First Spark and explicitly legacy Resonance gift boundary remains:

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
  --private-message "PRIVATE_MESSAGE" \
  --zip
```

To accept an existing activation instead, add:

```text
--activation path/to/activation.local.json
```

The preparation command validates it through the actual First Spark runtime
parser and requires `profile_id` to be `first-spark` before building.

## Prepare a corrected Resonance invitation and private Return Workspace

The corrected compose/initiate boundary produces an inert Resonance Token V2.
Given a saved Token V2, prepare its travelling invitation and matching retained
workspace with:

```bash
python3 modules/nexus_01_nexus_mesomerie/packaging/prepare_resonance_invitation.py \
  --token path/to/resonance_token.v2.json \
  --invitation-root path/to/travelling-output \
  --private-root path/to/private-output \
  --carrier-root path/to/travelling-nexus-carrier
```

Both publication roots must remain outside the travelling carrier root. The
command rejects either the invitation or the private Return Workspace beneath
that boundary before staging or publication.

The travelling invitation contains only `README.md` and
`resonance_token.local.json`. It contains no activation, runtime, Return Slot,
or Return Artifact. Token presence does not activate a Nexus; the recipient
will choose later whether to use it. The matching private Return Workspace is
built by the existing allowlisted workspace builder and contains the Return
Slot but no Token.

Both outputs are staged and validated before publication, refuse overwrite,
and are rolled back together if publication cannot complete. Verify the
travelling invitation independently with:

```bash
python3 modules/nexus_01_nexus_mesomerie/packaging/verify_resonance_invitation.py \
  path/to/n01-resonance-invitation-opaque
```

## Legacy-compatible pre-activated Resonance gift

The following established command remains temporarily available for the V1
one-person flow. It creates a `return-resonance` activation and must not be
described as the corrected invitation flow:

```bash
python3 modules/nexus_01_nexus_mesomerie/packaging/prepare_nexus_gift.py \
  resonance \
  --gift-label resonance-gift \
  --recipient-alias recipient_name \
  --private-message "PRIVATE_MESSAGE" \
  --public-safe-label "resonance path" \
  --zip
```

Its generated `START_HERE.sh` deliberately invokes:

```text
python3 run_nexus.py --legacy-preactivated
```

The corrected default `run_nexus.py` path requires the recipient activation
controller and never interprets the bundled legacy V1 Token as a V2 invitation.

The legacy command prints the travelling outputs separately from the retained private
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

Private messages passed directly as command-line arguments may be visible in
shell history or process listings. Keep documentation and test commands on
placeholders, and use an appropriately private local invocation for real text.

## Run all Nexus 01 production and integration tests

From the repository root:

```bash
python3 modules/nexus_01_nexus_mesomerie/run_all_tests.py
```

This standard-library runner includes module-level test functions that ordinary
`unittest` discovery does not collect, and excludes historical experiments.

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
