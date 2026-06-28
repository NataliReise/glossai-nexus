# Nexus 01 – MVP Specification

Working title: **Nexus 01 – Nexus-Mesomerie**  
Project: **glossAI Nexus**  
Document status: First working specification  
Suggested file name: `MVP_NEXUS_01.md`

---

## 1. Purpose

**Nexus 01 – Nexus-Mesomerie** is the first playable module of the glossAI Nexus project.

It should be a small, complete, locally playable software game artifact. It should work as:

- a standalone playable Nexus module,
- a neutral glossAI/Nexus lore experience,
- a personal activation for a person, group, or occasion,
- a gift activation as a special personal activation,
- a prototype for social resonance through carried codes and returned answers,
- an example of open code with protected activation content.

The MVP should not implement the full future vision of glossAI Nexus. It should demonstrate the core idea in a limited but meaningful form:

> A Nexus is not only played.  
> It can be activated, carried, answered, and returned.

---

## 2. Core Design Principles

Nexus 01 should follow these principles:

- The module structure is open.
- The code is readable.
- The game can be played without reading the code.
- Code reading may reveal additional layers, but should not replace the full resonance experience.
- Personal activation content must not be required to be public.
- The social network created by Nexus is not automatic or digital by default.
- Resonance codes are carried by people.
- A returned answer can unlock a deeper encrypted layer.
- A trace may be shared, but it should never be taken.

Important guiding formulas:

> The code belongs in the light.  
> The message may remain protected.

> You do not have to read the code.  
> But the code must be readable.

> A code can open a door.  
> Only a person can return through it.

---

## 3. Core Resonance Loop

The MVP should implement one complete resonance loop:

### Step 1: Origin Play

Player or Team A starts Nexus 01 with an activation.

This activation can be:

- a neutral activation,
- a personal activation,
- a gift activation as a personal activation with purpose `gift`.

Team A plays the main game and reaches the first ending.

At the end, Nexus 01 unlocks a primary result:

- a personal message,
- a gift message,
- or a lore fragment.

It also generates a resonance code.

### Step 2: Carrying the Trace

Team A gives the module and resonance code to Player or Team B.

This is not automatic. No online connection is required.

The trace is carried by a person.

### Step 3: Carried Play

Team B starts Nexus 01 with the resonance code from Team A.

This creates a carried activation.

Team B plays a modified version of the game.

During this run, Team B makes a small number of guided choices and contributes at least one human resonance word.

At the end, Nexus 01 generates a return key.

### Step 4: Return

Team B gives the return key back to Team A.

Team A enters the return key into the original Nexus activation.

The origin Nexus combines:

- the original resonance code,
- the return key,
- optional activation-specific secret material,
- and/or a resonance word.

If the combined key is valid, an encrypted return layer is decrypted and shown.

### Step 5: Returned Layer

The returned layer may reveal:

- a second message,
- a deeper lore fragment,
- a bonus resonance text,
- or a poetic answer connecting both playthroughs.

This completes the MVP resonance loop:

> A → B → A

Longer chains are not part of the MVP.

---

## 4. Module States

### 4.1 `module_only`

The module exists as open source structure.

It contains:

- code,
- module metadata,
- general fragments,
- game rules,
- documentation,
- schema files,
- example activation files,
- optional demo encrypted content.

This state is not playable as a concrete run.

A Nexus must be activated before it can be played.

### 4.2 `activated`

The Nexus has been activated through one of the supported activation modes.

The game can be started.

### 4.3 `completed`

The first playthrough has been completed.

A primary result has been unlocked.

A resonance code may be generated.

### 4.4 `carried`

The Nexus has been started with an incoming resonance code from another completed run.

This is a carried activation.

### 4.5 `returned`

A return key has been entered into the original activation.

If valid, the encrypted return layer has been opened.

---

## 5. Activation Model

The activation model has three separate layers:

1. **Activation mode** — how the Nexus is activated.
2. **Activation purpose** — why this activation exists.
3. **Play mode** — how the module is played.

This separation is important.

For example:

- `gift` is a purpose.
- `team_play` is a play mode.
- `personal_activation` is an activation mode.

---

## 6. Activation Modes

### 6.1 `neutral_activation`

A neutral activation is a playable activation without a private gift purpose and without a specific recipient.

It is suitable for:

- testing,
- public play,
- general lore access,
- sharing Nexus 01 without personal content.

Typical primary result:

- `lore_unlock`

A neutral activation is not the same as `module_only`.

`module_only` is not playable.  
`neutral_activation` is a playable activation.

### 6.2 `personal_activation`

A personal activation is a concrete activation for a person, team, occasion, or relationship context.

It may contain:

- recipient alias,
- group or team alias,
- occasion,
- tone,
- personal message,
- optional gift instruction,
- optional private secret material for encrypted layers.

Typical primary result:

- `message_unlock`

Personal activation files should not be committed to the public repository unless intentionally anonymized.

### 6.3 Gift Activation

A gift activation is not a separate activation mode.

It is a personal activation with:

```json
"purpose": "gift"
```

A gift activation may show visible personalization from the beginning.

Example:

> Nexus 01 has been activated for Sascha.  
> Occasion: birthday.  
> Private message: locked.  
> Resonance layer: waiting.

The actual gift message remains locked until the module is completed.

Typical primary result:

- `message_unlock`

Typical message type:

- `gift_message`

### 6.4 `carried_activation`

A carried activation starts when a player or team enters a resonance code received from another completed Nexus run.

It may change:

- intro text,
- available fragments,
- response prompts,
- return key generation,
- resonance wording,
- final carried result.

Typical primary result:

- a return key,
- possibly also a small lore or reflection fragment.

### 6.5 `return_input`

This is not a full new activation mode.

It is a return action inside the original activation.

A player enters a return key received from another carried activation.

If the key is valid, the encrypted return layer opens.

---

## 7. Activation Purposes

For Version 1, the following purposes should be supported or prepared:

### 7.1 `public_play`

Used with `neutral_activation`.

Purpose:

- general play,
- public demo,
- lore exploration,
- testing without private content.

Typical primary result:

- `lore_unlock`

### 7.2 `gift`

Used with `personal_activation`.

Purpose:

- gift,
- invitation,
- birthday,
- symbolic present,
- personal surprise.

Typical primary result:

- `message_unlock`

Typical message type:

- `gift_message`

### 7.3 `personal_resonance`

Used with `personal_activation`.

Purpose:

- personal note,
- shared reflection,
- friendship or group resonance,
- individually configured play without gift character.

Typical primary result:

- `message_unlock`

Typical message type:

- `personal_note`

### 7.4 Later Possible Purposes

Possible later values:

- `workshop`
- `learning_context`
- `community_play`
- `module_test`
- `artistic_prompt`

These are not required for Version 1.

---

## 8. Play Modes

### 8.1 `solo`

The module is played by one person.

This is suitable for:

- neutral play,
- personal play,
- gift play,
- carried activation.

### 8.2 `team_play`

The module is played by two or more people as a team.

This is suitable for:

- cooperative puzzle solving,
- gift play for a couple or group,
- neutral group play,
- carried activation by a team.

`team_play` is not a purpose.

It is a play mode.

Example:

```json
"play": {
  "mode": "team_play",
  "team_alias_enabled": true
}
```

---

## 9. Primary Result Types

### 9.1 `message_unlock`

A personal message, gift message, invitation, dedication, or concrete instruction is unlocked.

This is mainly used in personal activations.

The message may be:

- plain in a private local activation file,
- or encrypted, if the activation creator chooses this.

Possible message types:

- `gift_message`
- `personal_note`
- `invitation`
- `dedication`
- `return_prompt`

### 9.2 `lore_unlock`

A general Nexus/glossAI lore fragment is unlocked.

This is mainly used in neutral activations.

It may reveal:

- a fragment of the Nexus mythos,
- a reflection about openness, boundaries, access, response, or resonance,
- a small text from the glossAI matrix.

### 9.3 `encrypted_return_layer`

This is not the first primary result.

It is an optional second layer.

It opens only after a return key is entered into the original activation.

It should be symmetrically encrypted in Version 1.

---

## 10. Encryption in Version 1

Nexus 01 MVP should include one symmetrically encrypted return layer.

Recommended approach:

- Python implementation,
- `cryptography` library,
- preferably Fernet for the first version.

The full decryption key should not be stored directly in the public code.

The decryption key should be derived from multiple parts, for example:

- origin resonance code,
- return key from carried play,
- optional activation-specific secret,
- optional resonance word contributed by Team B.

The encrypted layer may be public if it contains general lore.

Private messages should remain in local activation files and should not be committed publicly.

### 10.1 Key Principle

The encryption should not pretend to be unbreakable magic.

It should provide meaningful protection against simply reading the answer in the source code.

It should also embody the project idea:

> The text is present in the Nexus.  
> But it becomes readable only when an answer returns.

### 10.2 Human Contribution

At least one element of the return key should depend on a human contribution by Team B.

Examples:

- a resonance word,
- a guided choice,
- a short answer,
- a team alias,
- a combination of choice and word.

This makes the returned layer less predictable from code inspection alone.

---

## 11. Resonance Codes

A resonance code is generated after a completed origin playthrough.

It should be:

- readable,
- short enough to share,
- thematically meaningful,
- parseable by the game,
- not secret in the same way as a password.

Example format:

```text
N01-MIRROR-BOUNDARY-314
```

Possible parts:

- module id,
- fragment signature,
- symbolic pair,
- short checksum or code suffix.

The resonance code is not the full key.

It is a carried trace.

---

## 12. Return Keys

A return key is generated after a carried activation has been completed.

It should depend on:

- incoming resonance code,
- carried play choices,
- at least one human resonance word,
- possibly difficulty or fragment result.

Example format:

```text
N01-RETURN-LANTERN-courage-827
```

The return key is given back to the origin player or team.

It should not need to be published anywhere.

---

## 13. Player Inputs

The MVP should keep player inputs small and manageable.

### 13.1 Command Input

Terminal-style commands such as:

```text
status
scan
read
connect
unlock
return
help
```

### 13.2 Guided Choices

Small choices during carried activation.

Example:

```text
Choose what the trace found behind the boundary:

1. a mirror
2. a lantern
3. a fox
```

### 13.3 Resonance Word

One freely entered word from the carried player or team.

Example:

```text
Leave one word inside the returning trace:
> courage
```

This word may become part of the return key or encrypted-layer key derivation.

---

## 14. Game Content Scope

The MVP should include:

- a small terminal interface,
- a limited command language,
- 5 main fragments,
- 2 optional bonus fragments,
- a neutral activation,
- a personal activation example,
- a gift activation example,
- a carried activation path,
- one encrypted return layer,
- after-play options.

Possible main fragments:

- ACCESS
- BOUNDARY
- OPENNESS
- TRACE
- RESPONSE

Possible bonus fragments:

- RESONANCE
- RETURN

These names may change during writing.

---

## 15. After-Play Options

After a completed run, the game may offer optional follow-up actions.

These are not primary results.

### 15.1 Show Pass-On Trace

The game displays the resonance code and explains how it may be carried to another person.

### 15.2 Generate Hall-of-Resonance Draft

The game may generate a local Markdown or JSON file.

This file may include:

- module id,
- activation type,
- play mode,
- team alias,
- completion status,
- fragments found,
- hints used,
- optional player note,
- consent marker.

No automatic publication.

### 15.3 Generate Resonance Note

The game may offer a reflection prompt and create a local note.

Example prompt:

> Which boundary protected resonance in this run?

This note may remain private or be shared voluntarily.

### 15.4 Generate Contact Node Draft

The game may prepare a short text for a GitHub Discussion contact node.

No automatic posting.

The player decides whether to copy and publish it.

---

## 16. Hall of Resonance

The Hall of Resonance is not a score table.

It is a voluntary collection of shared traces.

In Version 1, the game should only generate a local draft.

Possible future repository structure:

```text
hall_of_resonance/
  README.md
  entries/
```

Or initially:

```text
HALL_OF_RESONANCE.md
```

The Hall should only include what players choose to share.

---

## 17. Contact Nodes

A contact node is a voluntary public invitation for resonance.

It may be posted in GitHub Discussions.

Purpose:

- find someone to carry a trace,
- invite a return response,
- start a small social resonance chain,
- connect players without automatic tracking.

A contact node should not contain:

- private activation data,
- personal gift text,
- full private return keys,
- real names unless intentionally shared,
- sensitive information.

Possible draft format:

```text
Contact Node: N01-CN-0001
Module: Nexus 01 – Nexus-Mesomerie
Trace type: carried response
Team/Alias:
Looking for:
Public note:
```

GitHub Discussions may later use structured Discussion Forms.

This is not required for the playable MVP.

---

## 18. Example Configurations

### 18.1 Neutral Solo Activation

```json
{
  "activation": {
    "mode": "neutral_activation",
    "purpose": "public_play"
  },
  "play": {
    "mode": "solo"
  },
  "result": {
    "primary_type": "lore_unlock",
    "return_layer_enabled": true,
    "encrypted_layer_id": "n01_return_layer_01"
  },
  "after_play": {
    "offer_pass_on_trace": true,
    "offer_hall_entry": true,
    "offer_resonance_note": true,
    "offer_contact_node": true
  }
}
```

### 18.2 Personal Resonance Activation

```json
{
  "activation": {
    "mode": "personal_activation",
    "purpose": "personal_resonance",
    "recipient_alias": "Terminal Owls",
    "visible_personalization": true
  },
  "play": {
    "mode": "team_play",
    "team_alias_enabled": true
  },
  "result": {
    "primary_type": "message_unlock",
    "message_type": "personal_note",
    "return_layer_enabled": true
  },
  "after_play": {
    "offer_pass_on_trace": true,
    "offer_hall_entry": true,
    "offer_resonance_note": true,
    "offer_contact_node": true
  }
}
```

### 18.3 Gift Activation

```json
{
  "activation": {
    "mode": "personal_activation",
    "purpose": "gift",
    "recipient_alias": "Sascha",
    "occasion": "birthday",
    "visible_personalization": true
  },
  "play": {
    "mode": "solo"
  },
  "result": {
    "primary_type": "message_unlock",
    "message_type": "gift_message",
    "return_layer_enabled": true
  },
  "after_play": {
    "offer_pass_on_trace": true,
    "offer_hall_entry": true,
    "offer_resonance_note": true,
    "offer_contact_node": true
  }
}
```

### 18.4 Carried Activation

```json
{
  "activation": {
    "mode": "carried_activation",
    "incoming_resonance_code": "N01-MIRROR-BOUNDARY-314"
  },
  "play": {
    "mode": "solo"
  },
  "result": {
    "primary_type": "lore_unlock",
    "generates_return_key": true
  },
  "after_play": {
    "offer_hall_entry": true,
    "offer_resonance_note": true,
    "offer_contact_node": true
  }
}
```

---

## 19. In Scope for Version 1

Version 1 should include:

- local terminal play,
- neutral activation,
- personal activation support,
- gift activation as personal activation with purpose `gift`,
- solo and team play mode as configuration values,
- carried activation support,
- return input support,
- `message_unlock`,
- `lore_unlock`,
- one encrypted return layer,
- resonance code generation,
- return key generation,
- guided choices in carried activation,
- one human resonance word,
- local Hall-of-Resonance draft generation,
- local resonance note generation,
- local contact node draft generation,
- clear documentation.

---

## 20. Out of Scope for Version 1

Version 1 should not include:

- automatic online networking,
- automatic GitHub posting,
- GitHub API integration,
- user accounts,
- server infrastructure,
- database,
- long resonance chains beyond A → B → A,
- multiple modules,
- full module creation wizard,
- complex community governance,
- advanced cryptographic protocol design,
- AI-generated live responses,
- dependency-heavy packaging,
- graphical interface.

---

## 21. Later Extensions

Possible later extensions:

- longer resonance chains,
- multiple return layers,
- module templates,
- browser-based version,
- GitHub Discussion templates,
- Hall-of-Resonance contribution workflow,
- module creation guide,
- additional Nexus modules,
- cooperative two-person puzzle modes,
- Git history as optional puzzle layer,
- translations,
- accessibility improvements,
- workshop activations,
- learning-context activations.

---

## 22. MVP Success Criteria

The MVP is successful if:

1. A neutral activation can be played from start to finish.
2. A personal activation can unlock a message.
3. A gift activation can show visible personalization from the beginning and unlock a gift message only after completion.
4. A completed origin playthrough generates a resonance code.
5. A carried activation accepts that resonance code.
6. The carried activation produces a return key.
7. The origin activation accepts the return key.
8. The encrypted return layer decrypts only with the correct combined key material.
9. Solo and team play are represented as configuration options.
10. The game remains playable without code reading.
11. The code remains readable for people who want to inspect it.
12. The after-play options are voluntary and local.

---

## 23. Working Formula

Nexus 01 Version 1 should prove this idea:

> Open code can carry protected meaning.  
> A message can be unlocked by play.  
> A deeper answer can be unlocked only by return.

Or shorter:

> A Nexus becomes deeper when someone carries a trace back.
