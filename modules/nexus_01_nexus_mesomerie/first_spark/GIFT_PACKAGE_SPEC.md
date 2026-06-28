# Gift Package Specification

Status: Draft  
Project: Nexus / First Spark  
Purpose: Define a narrow private gift package model without blurring the public/private boundary.

## Core Principle

The public module stays neutral.  
The gift is created by a private wrapper.

## Scope of This Specification

This specification describes a private gift package for First Spark.

It is intentionally narrow. It does not define the larger A -> B -> A resonance arc, carried activation, resonance codes, or return keys yet.

The goal is only to define how a concrete activated gift can be prepared and handed over privately while keeping the public module clean.

## Relationship to Public Handoff

A public handoff and a private gift handoff are different situations.

Public handoff:

- public Git repository
- open-source release
- public demo package
- neutral module
- no real private activation
- no real private gift text
- no recipient-specific configuration

Private gift handoff:

- private package for one specific recipient
- may include real private activation
- may include real private gift text
- must stay outside the public Git repository
- must be transferred through a private channel
- should include clear start instructions for the recipient

For public sharing, use:

```text
PUBLIC_HANDOFF_CHECKLIST.md
```

For private gifting, use this specification.

## Definition

A First Spark gift package is a private wrapper around the public First Spark module.

It may include a recipient-specific activation file and private start instructions.

It must not change the meaning of the public module:

- the public module remains neutral
- the public repository remains clean
- the private activation remains private
- the gift layer remains clearly separated

## Minimal Gift Package

The recommended minimal private gift package contains:

```text
first_spark_gift_package/
  README_FOR_RECIPIENT.md
  activation.local.json
```

The recipient also needs access to the public First Spark module, either by:

- cloning or downloading the public repository, or
- receiving a clean public copy of the module without private data.

The private gift package should be applied locally by placing `activation.local.json` at:

```text
modules/nexus_01_nexus_mesomerie/first_spark/activation.local.json
```

This keeps the public module and the private gift activation conceptually separate.

## Optional Expanded Gift Package

A private gift package may later contain:

```text
first_spark_gift_package/
  README_FOR_RECIPIENT.md
  activation.local.json
  gift-note.txt
  checksums.txt
```

Possible optional files:

- `gift-note.txt` - a private note outside the game activation file
- `checksums.txt` - optional integrity notes for transferred files
- additional recipient instructions, if needed

These optional files must remain private.

## Recommended Private Files

### activation.local.json

This file contains recipient-specific activation data.

It may contain:

- recipient alias
- activation purpose
- private message
- other future private activation fields

It must not be committed to the public Git repository.

### README_FOR_RECIPIENT.md

This file explains how the recipient can start First Spark with the private activation.

It should be short, kind, and practical.

It should explain:

- where to place `activation.local.json`
- how to start First Spark
- that the activation file is private
- that the public module can also run without the activation file
- what to do if something does not work

## What Must Never Enter Public Git

Absence check for the public repository:

- [ ] Real private activation data is absent.
- [ ] Real private gift text is absent.
- [ ] Recipient-specific configuration is absent.
- [ ] Private recipient instructions are absent.
- [ ] Local package folders are absent.
- [ ] Private transfer notes are absent.
- [ ] Secrets, tokens, keys, or credentials are absent.

## Recommended Local Package Location

A private gift package should be prepared outside the public repository when possible.

Suggested local location:

```text
~/Nexus-Gift-Packages/first_spark_<recipient_alias>/
```

or another private local folder that is not inside the Git working tree.

If a private gift package is temporarily prepared inside the repository for development convenience, it must be placed in an ignored private folder and checked carefully before any commit.

## Transfer Channel

A private gift package should be transferred through a private channel.

Examples:

- encrypted archive
- private cloud share
- direct local transfer
- private email attachment, if appropriate

Avoid public issue trackers, public repository branches, public release assets, public chats, or public paste services.

## Recipient Start Flow

A minimal recipient flow may look like this:

```text
1. Get the public First Spark module.
2. Receive the private gift package separately.
3. Copy activation.local.json into the First Spark folder.
4. Start First Spark.
5. Play the neutral module with private activation enabled locally.
```

Current start command from the repository root:

```bash
python3 modules/nexus_01_nexus_mesomerie/first_spark/run_first_spark.py
```

## Development Safety Check

Before creating or sending a private gift package, check:

- [ ] The public repository is clean.
- [ ] The public handoff checklist still passes.
- [ ] The private activation file is not tracked.
- [ ] The gift package is outside public Git or safely ignored.
- [ ] The private message is intended for this recipient.
- [ ] The recipient instructions are clear.
- [ ] No unrelated private files are included.
- [ ] The transfer channel is appropriate for private data.

Suggested public-repo check:

```bash
git status --short
git ls-files | grep 'modules/nexus_01_nexus_mesomerie/first_spark/activation.local.json'
```

Expected result:

- `git status --short` shows no unexpected public changes.
- `git ls-files | grep ...` returns nothing.

## Not Yet Specified

This document does not yet specify:

- resonance codes
- carried activation
- return keys
- encrypted return layers
- A -> B -> A gameplay
- multi-person gift chains
- public/private key exchange
- generated gift packages
- a packaging CLI

Those belong to a later game-flow or MVP specification.

Possible later files:

```text
MVP_NEXUS_01.md
GAME_FLOW.md
```

## Design Boundary

A gift package is not a public release.

A gift package is not a fork of the public module.

A gift package is not a new module version.

A gift package is a private activation wrapper around a clean public module.

## Working Formula

Public module:

```text
clean code + neutral fallback + safe example activation
```

Private gift package:

```text
private activation + recipient instructions + private transfer
```

Together, locally:

```text
public module + private wrapper = activated gift experience
```

The public module stays neutral.  
The gift is created by a private wrapper.
