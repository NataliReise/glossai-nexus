# First Spark After-Play Specification

Status: Draft  
Project: Nexus / First Spark  
Purpose: Define the first small after-play layer that connects First Spark to the larger Nexus 01 resonance chain.

## Core Principle

The gift remains complete.  
The spark may travel onward.

## Scope

This specification describes what may happen after the current First Spark ending.

It does not implement the full Nexus 01 resonance chain yet.

It prepares the next small running unit:

- show an optional after-play message
- invite private pass-on without pressure
- point to the public project
- optionally prepare a public-safe resonance node draft

It does not yet require:

- full resonance artifact generation
- full return artifact handling
- return-layer unlocking
- GitHub API integration
- automatic posting
- public contact nodes

## Current Ending

First Spark currently ends after the player unlocks the activation message.

The next step should not replace that ending.

Instead, it should add a small after-play layer after the final message.

The final message remains the primary result.

The after-play layer is optional orientation.

## After-Play Goals

After a completed First Spark run, the player should understand:

- the run is complete
- the gift or neutral message is complete
- no further action is required
- the spark may be passed onward privately
- the public project can be visited
- private activation data must not be posted publicly
- a public-safe resonance node may optionally be shared later

## Required Tone

The after-play message should be:

- calm
- clear
- non-pressuring
- public/private aware
- slightly poetic but not obscure
- understandable without reading project documentation

It must not sound like:

- a chain letter
- a growth hack
- a command
- a demand for public posting
- a social obligation

Important wording:

```text
Passing on a spark is an invitation, not an obligation.
A received gift remains complete even if it is never forwarded.
```

## Public / Private Boundary

The after-play layer must clearly distinguish:

### Private

- gift activation
- private gift message
- recipient-specific instructions
- resonance activation
- return artifact
- private relationship context

### Public-safe

- project repository link
- general documentation
- public-safe resonance node draft
- non-private completion note
- optional public alias

Rule:

```text
Never post private activation data, private gift text, or return artifacts publicly.
```

## Suggested After-Play Message

The first implementation may show a short text after the final message:

```text
The First Spark is complete.

You may keep this as a finished gift.
Nothing else is required.

If you want, you may let the spark travel further:
- give a clean public copy of First Spark or the Git link to someone you choose
- add a private activation package only through a private channel
- never post private activation data publicly

You can also visit the public project and, if you like, share a public-safe resonance node later.
A resonance node only says that a spark was seen.
It must not include private messages, activation files, or return artifacts.
```

A shorter later version may be used in the actual game.

## Public Git Invitation

The after-play layer may invite the player to visit the public Git repository.

The message may say:

```text
You can inspect the public First Spark module in the Git repository.
The public module is neutral and safe to share.
Private activations stay outside the public repository.
```

The concrete repository URL may be added later in configuration or documentation.

## Private Pass-On Invitation

The after-play layer may invite private pass-on.

Suggested text:

```text
If this spark should travel, choose one person privately.
Give them the public module or repository link.
Add a private activation package only through a private channel.
```

This is not required for completion.

## Resonance Node Draft

A resonance node draft is a public-safe local text draft.

It is not an activation artifact.

It is not used to unlock gameplay.

It is only an optional way to help make the growing Nexus network visible.

It may later be copied manually into a GitHub Discussion or another public project space.

No automatic posting is part of First Spark.

## Resonance Node Draft Safety

A resonance node draft must not contain:

- private activation data
- private gift text
- private return artifacts
- recipient names unless intentionally public
- email addresses
- phone numbers
- private contact details
- sensitive relationship context
- secrets, tokens, keys, or credentials

A resonance node draft may contain:

- module id
- module name
- run type
- completion marker
- optional public alias
- optional public note
- consent marker
- privacy reminder

## Possible Resonance Node Draft Format

```text
Resonance Node: N01-RN-0001
Module: Nexus 01 - First Spark
Run type: private gift / neutral / carried spark
Status: completed
Trace visibility: public-safe summary only
Forwarded: optional / yes / no / not shared
Return: optional / received / not shared
Public alias:
Public note:
Consent: I choose to share this public trace. No private activation data, gift text, or return artifact is included.
```

The first implementation may only display this template instead of generating a file.

## Implementation Options

### Option A: Text Only

Show the after-play message in the terminal.

Do not generate files yet.

This is the smallest implementation.

### Option B: Display Draft Template

Show the after-play message and display a public-safe resonance node template.

The player may copy it manually.

### Option C: Generate Local Draft File

Create a local file such as:

```text
modules/nexus_01_nexus_mesomerie/first_spark/generated/resonance_node_draft.md
```

If this option is used, the generated folder must be ignored by Git if it can contain user-specific local output.

## Recommended First Running Unit

Use Option A first.

Smallest next code step:

```text
After unlock, show a short after-play message.
```

No file generation yet.

No resonance artifact generation yet.

No return artifact handling yet.

## Later Running Units

After Option A works, possible next units are:

1. Add a command to show the after-play text again.
2. Add a public-safe resonance node template.
3. Generate a local resonance node draft file.
4. Add a first resonance artifact concept.
5. Add private resonance activation support.
6. Add return artifact input.
7. Add return-layer unlocking.

Each unit should remain small and runnable before the next one is added.

## Success Criteria

The after-play layer is successful if:

- the existing First Spark ending still works
- the final message remains the primary result
- the player sees that no further action is required
- the invitation to pass the spark onward is clearly voluntary
- the public/private boundary is explicit
- no private data is generated for public sharing
- no automatic online behavior is introduced
- the next larger Nexus 01 resonance chain becomes easier to understand

## Working Formula

First Spark ending:

```text
play -> unlock message -> complete
```

First after-play layer:

```text
complete -> optional private pass-on invitation -> optional public-safe trace idea
```

Core formula:

```text
The gift is complete.
The spark may travel.
The public trace reveals only that light was seen.
```
