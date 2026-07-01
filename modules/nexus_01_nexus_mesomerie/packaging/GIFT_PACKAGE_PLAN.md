# First Spark Gift Package Plan

This document prepares the next packaging step for **Nexus 01 - First Spark**.

The current preview package is public-safe. A later personal gift package may carry local meaning for one intended person. That makes the gift workflow more delicate than the preview workflow.

The goal of this plan is to keep the boundary clear before adding more automation.

```text
Open structure. Private meaning. Careful resonance.
```

## Current status

The public preview workflow already exists.

It can:

```text
build a standalone preview folder
build an optional ZIP archive
verify that the preview folder is public-safe
```

Relevant files:

```text
modules/nexus_01_nexus_mesomerie/packaging/build_first_spark_package.py
modules/nexus_01_nexus_mesomerie/packaging/verify_first_spark_package.py
modules/nexus_01_nexus_mesomerie/packaging/README.md
```

The First Spark game core should stay stable for now.

The next work should improve gift safety and package clarity, not add new rooms, mechanics, or puzzle text.

## Package types

### Preview package

A preview package is public-safe.

It is meant for testing, demonstration, and early feedback.

It may be shared through manual channels such as:

```text
local folder
ZIP file
email attachment
messenger file
cloud link
USB stick
```

It must not contain local personal gift data.

Expected activation data:

```text
activation.example.json
```

Files that must stay out of the preview package:

```text
activation.local.json
*.local.json
*.local.txt
*.local.md
```

The preview package may travel digitally.

It must not manage relationships.

### Personal gift package

A personal gift package is created for one intended person.

It may contain a real local activation file.

Expected local activation data:

```text
activation.local.json
```

A personal gift package should be created locally and deliberately.

It should not be committed to Git.

It should not be uploaded automatically.

It should not be sent automatically.

It should only be shared manually by the person who created it.

## Boundary rules

### Public repo

The public repository may contain:

```text
source code
public documentation
public example activation data
preview package builder
preview package verifier
gift package planning documentation
```

The public repository must not contain:

```text
real local activation files
person-specific notes
person-specific generated artifacts
local result files
local return files
built ZIP packages
built dist folders
```

### Local workspace

The local workspace may contain local files while a personal gift package is being prepared.

Examples:

```text
activation.local.json
return_slot.local.json
return_artifact.local.txt
local_result.md
```

These files should remain local.

They are meaningful because they are not part of the public structure.

They should not become public by accident.

### Generated package output

Generated package output belongs in:

```text
dist/
```

The `dist/` folder is ignored by Git and should stay untracked.

Preview and gift ZIP archives should also remain untracked build artifacts.

## Safety principles

A personal gift builder should follow these principles:

```text
1. Refuse to run if the required local activation file is missing.
2. Refuse to overwrite an existing gift package unless explicitly requested.
3. Copy only the files needed for the gift package.
4. Copy local activation data only from the local workspace.
5. Never create commits.
6. Never upload, post, send, or sync anything.
7. Print clear next steps for manual sharing.
8. Make the public/local boundary visible in generated documentation.
```

A personal gift verifier should follow a different rule set from the preview verifier.

The preview verifier rejects local activation files.

The gift verifier may require exactly one local activation file.

## Proposed next workflow

A careful gift workflow could look like this:

```bash
python3 modules/nexus_01_nexus_mesomerie/first_spark/create_local_activation.py
# edit modules/nexus_01_nexus_mesomerie/first_spark/activation.local.json locally
python3 modules/nexus_01_nexus_mesomerie/packaging/build_first_spark_gift_package.py --gift-label first-gift --zip
python3 modules/nexus_01_nexus_mesomerie/packaging/verify_first_spark_gift_package.py dist/nexus-01-first-spark-gift-first-gift
```

The exact names may still change.

The important point is the order:

```text
create local activation
review local activation
build gift package locally
verify gift package locally
share manually
```

## Proposed files for the next implementation step

Possible future files:

```text
modules/nexus_01_nexus_mesomerie/packaging/build_first_spark_gift_package.py
modules/nexus_01_nexus_mesomerie/packaging/verify_first_spark_gift_package.py
```

The gift builder should probably reuse ideas from the preview builder, but it should not blur the public/local boundary.

The gift verifier should probably reuse ideas from the preview verifier, but it should intentionally check a different package type.

## Naming idea

Default preview package:

```text
nexus-01-first-spark-preview
```

Possible gift package pattern:

```text
nexus-01-first-spark-gift-<gift-label>
```

The `<gift-label>` should be optional and local. It should not need to be a real name.

Safe examples:

```text
first-gift
linux-test
personal-copy
```

Avoid sensitive labels in folder names.

## Manual sharing rule

The Nexus may create an artifact.

It should not create a social graph.

It should not remember who received what unless the creator records that locally and deliberately.

```text
The artifact may travel digitally.
The resonance should be carried socially.
```

## Stop condition

If a feature starts managing people, relationships, reactions, engagement, delivery, reminders, or networks, it does not belong in First Spark packaging.

Guiding question:

```text
Does this feature support the artifact,
or does it start managing the relationship?
```

## Current recommendation

Do not build the personal gift package builder until the preview workflow has stayed stable through at least one local build-and-verify run.

Once that is confirmed, the next code step can be:

```text
build_first_spark_gift_package.py
```

The gift builder should be small, explicit, local-only, and boring in the best possible way.

Readable code is a form of hospitality.
Reliable packaging is a form of care.
