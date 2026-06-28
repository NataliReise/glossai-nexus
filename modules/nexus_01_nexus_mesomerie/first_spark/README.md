# Nexus 0.1 - First Spark

First Spark is the first small playable slice of **Nexus 01 - Nexus-Mesomerie**.

This directory contains the local terminal prototype.

## Current running unit

The current prototype only starts and prints a small boot sequence.

This is intentional.

Development principle:

> First make the spark run.  
> Then widen the trace.

## Run

From the repository root:

```bash
python3 modules/nexus_01_nexus_mesomerie/first_spark/run_first_spark.py
```

Or from this directory:

```bash
python3 run_first_spark.py
```

## Next running units

1. Add `help` command.
2. Add `look` command.
3. Add `read` command for virtual files.
4. Add `link` command for fragments.
5. Add `unlock` command for the gift message.

Each unit should remain small and runnable before the next one is added.
