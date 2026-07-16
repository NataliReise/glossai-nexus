# Lean Autonomous Nexus Principle 01

## Status

This document records a guiding architectural principle for the Resonance Composition V0.2 prototype and for later Nexus module design.

It supplements the existing commitments to autonomy, privacy, modularity, local actualisation, readable code, and inspectable composition.

## Core principle

A Nexus should remain lean enough to understand and rich enough to resonate.

```text
Autonomy without bloat.
Poetic depth without opaque complexity.
Readable structure without flattening the resonance process.
```

The goal is not to minimise line count at any price. The goal is to keep every layer of complexity purposeful, local, inspectable, and proportionate to the poetic or ethical function it serves.

## Why this principle is needed

Autonomy can produce two opposite risks.

A Nexus may become too dependent on external services, shared state, or hidden infrastructure. That would weaken local autonomy.

But an autonomous Nexus may also become overburdened by carrying too many unrelated responsibilities, duplicate abstractions, or opaque internal mechanisms. That would weaken readability, maintainability, transferability, and trust.

The design target is therefore not simply:

```text
self-contained
```

but:

```text
self-contained and legible
```

A module should carry what it needs to act locally, but it should not accumulate structure merely because local accumulation is technically possible.

## Readable code as hospitality

Readable code is a form of hospitality.

A Nexus should invite understanding rather than require excavation.

This means that a future reader should be able to discover, with reasonable effort:

- what the module does;
- why a rule exists;
- where poetic choices are made;
- which data is public structure and which meaning remains private;
- which parts are experimental;
- and how one component can be changed without silently disturbing unrelated behaviour.

Speaking names, local responsibilities, explicit data structures, and inspectable CompositionPlans are therefore not cosmetic preferences. They are part of the ethical architecture.

## Not a minimum-code doctrine

This principle must not be misread as:

```text
less code is always better
```

That would be too crude for the current Nexus module.

The poetic function and the resonance process are central, not optional embellishments. They may require:

- curated libraries;
- explicit routes;
- compatibility rules;
- composition plans;
- validation paths;
- special handling for lexically identical contributions;
- repetition and reprise policies;
- anti-formula weighting;
- and transparent metadata.

Such structure is justified when it directly protects or enables the intended poetic relation.

The correct standard is:

> As much structure as necessary, as little complexity as possible.

Or more fully:

> Poetic depth may require code. Complexity must remain purposeful, local, and readable.

## Purposeful complexity

Complexity is justified when it contributes directly to at least one of the following:

- poetic depth;
- relational integrity;
- privacy protection;
- local autonomy;
- stable local actualisation;
- inspectability;
- transferability;
- safety of composition;
- or prevention of a misleading machine stamp.

Complexity is not justified merely because it offers another abstraction, another configuration layer, or another theoretically possible extension.

Every addition should be able to answer:

```text
What poetic, ethical, or architectural function would be lost without this?
```

If that question cannot be answered clearly, the addition should be simplified, postponed, or omitted.

## Locality of responsibility

A clear module should own a coherent responsibility.

Useful separation may include:

```text
composer
-> selects and renders a composition

same-word policy
-> handles lexical identity without semantic interpretation

repetition policy
-> distinguishes accidental duplication from curated reprise

library
-> carries reviewed poetic possibilities

CompositionPlan
-> exposes the selected structure
```

This separation remains healthy only while each part represents a meaningful responsibility.

The project should avoid both extremes:

```text
one monolithic generator
-> too many hidden concerns in one place

excessive micro-modules
-> too many fragments without a clear whole
```

A module should carry one clear task, not merely one small piece of an unclear task.

## Complexity budget

Each Nexus module should be treated as having a complexity budget.

This budget is not a fixed number of files or lines. It is a review discipline.

For every significant extension, ask:

1. Does the Nexus truly need this function locally?
2. Does it contribute directly to the poetic or ethical purpose?
3. Is its responsibility clearly named and bounded?
4. Can a reader understand its role without reconstructing the whole system?
5. Does it introduce hidden state, indirect coupling, or surprising side effects?
6. Could the same function be expressed more simply without losing what matters?
7. Can it be removed or replaced without tearing apart unrelated parts of the module?
8. Does the addition preserve the neutrality of private free words?

An extension does not fail merely because it adds code. It fails when its cost becomes harder to explain than its function.

## Relationship to the resonance process

The current module is allowed to be richer than a minimal random text generator because it is not trying merely to produce variation.

It aims to create a bounded resonance process in which:

- two contributions retain distinct provenance;
- neither contribution is semantically profiled;
- relation emerges through curated structure;
- repetition can carry poetic function;
- the Echo is born from the selected long form;
- and the result remains inspectable.

The same-word route is an example of justified complexity.

It exists because lexically identical contributions create a real poetic and relational problem. The special route preserves two contributions without forcing clumsy duplication such as `Return returns` and without pretending that the two inputs were only one event.

The policy therefore adds code in order to protect the meaning of the interaction, not merely to handle an edge case mechanically.

## Data over hidden machinery

Where possible, poetic variation should remain visible in reviewed data rather than disappear into opaque algorithmic behaviour.

Prefer:

- explicit weights;
- named routes;
- compatibility maps;
- visible signature-strength metadata;
- curated movement mappings;
- and inspectable block roles.

Avoid unnecessary:

- semantic inference at runtime;
- adaptive behavioural profiles;
- hidden heuristics;
- global state;
- remote orchestration;
- and algorithmic layers whose poetic effect cannot be explained.

This does not mean that all logic must become data. It means that the boundary between curation and mechanism should remain understandable.

## Autonomy and leanness reinforce each other

A lean Nexus is easier to transfer, inspect, fork, preserve, and trust.

A readable Nexus also makes its autonomy more credible. A module is not meaningfully autonomous when its behaviour depends on internal machinery that almost nobody can understand or safely modify.

```text
local autonomy
+ readable structure
+ bounded responsibility
= practical independence
```

Leanness therefore supports the same project values as decentralisation:

- no central authority is needed to explain the unit;
- no hidden service is required to complete its function;
- no single maintainer should become indispensable;
- and no private meaning must be exposed merely to operate the mechanism.

## Tension to preserve

The project should consciously preserve the productive tension between richness and restraint.

```text
too little structure
-> shallow, arbitrary, or fragile poetry

too much structure
-> opaque, rigid, or overengineered machinery

proportionate structure
-> rich resonance with readable causes
```

The aim is not maximal simplicity and not maximal sophistication.

The aim is proportion.

## Review signal: speaking code

Code should reveal intent through names and local shape.

Prefer names that say what a component contributes, for example:

```text
same_word_mode
wish_role_proxy
relation_id
remainder_id
echo_movement
signature_strength
explicit_reprise
```

Avoid compressed or overly generic names that force readers to infer poetic function from implementation details.

Comments and decision documents should explain why a rule exists, especially when a rule protects a poetic distinction rather than a technical invariant.

## Current application to Resonance V0.2

The current prototype already reflects this principle in several ways:

- the production V0.1 opener remains untouched;
- the V0.2 experiment is isolated;
- the CompositionPlan exposes selected structure;
- free words are not semantically analysed;
- the same-word policy is explicit;
- repetition rules are separated from lexical identity;
- anti-formula quality is carried by local weights and compatibility;
- and development decisions are documented alongside the code.

At the same time, the prototype should later be reviewed for possible simplification before production integration.

Experimental separation is allowed to create temporary layers. Production integration should retain only layers that still clarify responsibility.

## Acceptance criteria for future extensions

A future extension is consistent with this principle when:

1. Its poetic, ethical, or architectural purpose is explicit.
2. Its responsibility is local and named.
3. It does not introduce unnecessary central dependency.
4. It does not require private semantic profiling.
5. Its behaviour remains inspectable.
6. Its complexity is proportionate to the function protected.
7. It does not duplicate an existing responsibility without a clear reason.
8. It can be tested in isolation where appropriate.
9. It does not turn one module into a container for unrelated concerns.
10. It preserves the possibility of later simplification.

## Core formulations

> A Nexus should remain lean enough to understand and rich enough to resonate.

> Autonomy without bloat.

> Poetic depth may require code. Complexity must remain purposeful, local, and readable.

> Readable code is a form of hospitality.

> Architecture is an ethical statement.
