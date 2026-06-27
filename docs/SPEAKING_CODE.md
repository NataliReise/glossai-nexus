# Speaking code

Speaking code is a core design idea of **glossai-nexus**.

For a Nexus, code is not only infrastructure. It can be part of the experience, part of the game layer, and part of the ethical architecture.

Speaking code has three layers:

1. clear code,
2. playful code,
3. ethical code.

A simple rule comes first:

> Speaking code should be clear before it becomes playful.

## 1. Clear code

Clear code is the foundation.

A Nexus should not hide its structure behind unnecessary cleverness, obscure naming, or avoidable complexity.

Code should generally aim for:

- meaningful names for files, functions, classes, and variables,
- small and focused functions,
- simple control flow where possible,
- helpful comments where they explain intent or context,
- readable error messages,
- minimal and well-documented dependencies,
- clear separation between module structure and private activation data,
- documentation that helps new contributors understand the project.

For Python modules, contributors should generally use **PEP 8** as a style orientation and **PEP 257** as a docstring orientation.

Other languages and tools may be used, but they should follow comparable community standards for readability, formatting, documentation, and maintainability.

## 2. Playful code

A Nexus may include a second game layer inside the code and repository structure.

This may happen through:

- meaningful comments,
- readable file and function names,
- optional hidden traces,
- developer notes,
- configuration patterns,
- Git history,
- structural choices that carry additional meaning.

This layer should remain optional for players.

A Nexus should be playable without reading the code. Reading the code may reveal additional traces, hints, meanings, or echoes.

Playful code should not make the functional code harder to understand.

## 3. Ethical code

A Nexus should also speak through its architecture.

Its design should reflect the values of the project:

- accessibility,
- non-elitist entry points,
- inspectability,
- respect for private activations,
- open structures,
- human responsibility,
- democratic imagination,
- cooperation rather than domination.

This can affect practical design choices:

- provide a simple way to start playing,
- avoid making code reading a requirement for basic play,
- keep installation steps as light as possible,
- document assumptions and limitations,
- support different depths of engagement,
- avoid unnecessary black-box dependencies,
- keep AI assistance optional and reviewable,
- use clear configuration patterns,
- separate public module files from private activation files.

## Language openness

The first reference implementation may use Python, but **glossai-nexus** is not bound to one programming language.

A Nexus module may be written in any open software form that keeps the module:

- playable,
- readable,
- inspectable,
- configurable,
- accessible,
- respectful of the distinction between public structure and private activation.

## Nexus-specific guidelines

- Do not make code reading mandatory for basic play.
- Do not use poetic or hidden code comments to obscure functional behavior.
- Do not place private activation data in public module files.
- Explain difficult or surprising design choices.
- Prefer clarity over cleverness.
- Let the deeper layer reward curiosity, not punish non-programmers.
- Let the code, file structure, and configuration patterns reflect the project values.

## Core sentence

> You do not have to read the code. But the code must be readable.
