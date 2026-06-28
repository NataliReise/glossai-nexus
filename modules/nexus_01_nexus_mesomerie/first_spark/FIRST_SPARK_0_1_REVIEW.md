# First Spark 0.1 Review

Status: stable small seed

First Spark 0.1 is a small local terminal prototype for Nexus 01 - Nexus-Mesomerie.

It is intentionally narrow. It proves that a Nexus module can be played locally, activated privately, shared publicly in a safe form, and completed without collecting or storing unnecessary data.

## Current state

First Spark 0.1 is:

- playable from the terminal
- repeatable after completion
- usable as a neutral public demo
- usable as a private gift when combined with a private activation package
- protected by a minimal automated flow test
- clear about the boundary between public code and private activation data
- able to show an optional public-safe resonance node draft after completion

## Completed play flow

The current play flow is:

```text
arrival -> spark chamber -> read traces -> link spark -> unlock activation message -> after-play
```

The player can then optionally type:

```text
resonance-node
```

to show a public-safe resonance node draft in the terminal.

## Privacy and data minimization

First Spark 0.1 does not automatically save result files, resonance nodes, return artifacts, or play logs.

This is intentional.

The player can copy visible terminal text manually if they choose. This keeps the module simple and reduces accidental data creation.

Design principle:

> Completion may create meaning, but it does not need to create files.

## Public/private boundary

The public repository may contain:

- clean public code
- neutral demo behavior
- safe example activation data
- public-safe documentation
- public-safe resonance node drafts

The public repository must not contain:

- `activation.local.json`
- real private gift messages
- real recipient-specific activation data
- return artifacts
- private notes from a gift package

## Private gift layer

A private gift is created by combining the public module with a private activation package outside the public repository.

The public module remains neutral and inspectable.

The private gift layer may contain private activation data, but it must travel only through private channels.

## Resonance node behavior

The `resonance-node` command shows an optional public-safe draft.

It does not post anything.
It does not write a file.
It does not include the private activation message.

Players may copy the draft manually, edit only the public alias and public note, and share it only if they choose.

## Repeatability

First Spark 0.1 does not deactivate after completion.

This is intentional.

A completed gift should remain revisitable. The activation message can be read again, and the public-safe resonance node draft can be shown again.

Design principle:

> The Nexus is not consumed; it becomes remembered.

## Current documentation

Important files:

- `README.md` - technical entry point for First Spark
- `WHAT_NEXT.md` - short player-facing explanation after completion
- `LOCAL_ACTIVATION_GUIDE.md` - local private activation workflow
- `PUBLIC_HANDOFF_CHECKLIST.md` - safe public sharing checklist
- `GIFT_PACKAGE_SPEC.md` - private gift package boundary and structure
- `FIRST_SPARK_AFTER_PLAY.md` - after-play concept

## Manual acceptance test

From the repository root:

```bash
python3 modules/nexus_01_nexus_mesomerie/first_spark/tests/test_first_spark_flow.py
python3 modules/nexus_01_nexus_mesomerie/first_spark/run_first_spark.py
```

Expected core behavior:

- the automated flow test passes
- `walkthrough` shows the full path without changing state
- `unlock` only opens the activation message after the spark was linked
- the activation message and after-play message are separated by the Ankh divider
- the after-play message links to the public `WHAT_NEXT.md` guide
- `resonance-node` shows a public-safe draft
- `Ctrl-C` exits without a traceback

## What is deliberately not included yet

First Spark 0.1 does not yet include:

- automatic result saving
- automatic resonance node file creation
- automatic public posting
- return artifact generation
- persistent completion state
- multi-node trace maps
- advanced activation field validation

These omissions keep the seed small, safe, and understandable.

## Possible next steps

Reasonable future running units:

1. Add optional activation field validation for future fields.
2. Refine the resonance node draft language after external reading.
3. Explore optional result or resonance-node file saving only if there is a strong reason.
4. Prepare resonance artifact and return artifact concepts after the current public/private boundary remains stable.

Current preference:

Do not add automatic saving yet. Manual copying from the terminal fits the data-minimization principle better.
