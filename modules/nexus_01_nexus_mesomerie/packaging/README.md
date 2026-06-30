# Nexus 01 Packaging

This folder contains small packaging helpers for **Nexus 01 - Nexus-Mesomerie**.

The current first helper builds a standalone preview package for:

```text
Nexus 0.1 - First Spark
```

The package is meant for manual, social-analog sharing: for example as a local folder, ZIP file, email attachment, messenger file, cloud link, or USB stick.

It does not upload, post, send, or track anything automatically.

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

## Test the package manually

After building the package, run:

```bash
cd dist/nexus-01-first-spark-preview
./START_HERE.sh
```

Alternative start command:

```bash
python3 run_first_spark.py
```

## Design boundary

The package builder supports the artifact.

It must not manage the relationship.

Working rule:

```text
The artifact may travel digitally.
The resonance should be carried socially.
```
