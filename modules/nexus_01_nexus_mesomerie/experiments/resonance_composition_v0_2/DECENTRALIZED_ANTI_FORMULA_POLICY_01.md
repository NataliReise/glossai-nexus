# Decentralized Anti-Formula Policy 01

## Status

This document records a binding architectural and poetic decision for the isolated Resonance Composition V0.2 prototype.

It applies first to the current `mixed-threshold-return-world` experiment and is intended to guide later library design. It does not yet change the V0.1 production opener, persistence, or transfer format.

## Decision summary

GlossAI must reduce formulaic output without introducing a central memory, cross-copy coordination, hidden usage history, or global frequency tracking.

The anti-formula strategy therefore relies on **curated scarcity inside each autonomous Nexus unit** rather than on any remembered history of what other copies have produced.

```text
No global cooldown
No cross-copy memory
No central usage history
No hidden frequency tracking
No remote coordination requirement
```

Variation must be carried by the local library, its routes, its weights, and its compatibility rules.

## Architectural reason

A transferred Nexus does not know what other Nexus copies have generated. It has no access to a shared poetic ledger and must not depend on one.

Each copy should remain capable of local actualisation with only:

- its own reviewed library;
- its own local random source;
- its own transfer data;
- and, where explicitly part of the artifact model, its own local persisted result.

The absence of global memory is not a missing feature. It is a deliberate property of the Nexus architecture.

> The unit knows its possibilities, but not the global activity around it.

This protects:

- local autonomy;
- transferability;
- privacy of meaning;
- independence from a central service;
- resistance to hidden behavioural analysis;
- and the modular character of the project.

## Relationship to the Nexus philosophy

The same principle appears at several levels of the project.

### Autonomous copies

A Nexus copy can be opened and completed locally without asking a central authority what it is allowed to generate.

### Autonomous modules

A module carries enough information to participate in a composition without understanding or controlling the whole system.

### Autonomous building blocks

A poetic block knows its role, operators, motifs, compatible modes, and local constraints. It does not need access to the private meaning of the free words or to a global history of previous poems.

### Convergence without fusion

Elements may enter relation without being merged into one central intelligence or one shared behavioural record.

```text
order without a centre
connection without total integration
transfer without surveillance
relation without loss of autonomy
```

The architecture therefore mirrors the poetic principle of `convergence-without-fusion`.

## Rejected mechanism: global cooldown

A global or cross-copy cooldown would require at least one of the following:

- a central registry of generated outputs;
- shared counters for block usage;
- network synchronisation between Nexus copies;
- user-linked or device-linked generation history;
- or a remote service deciding which lines are currently "too recent".

These mechanisms are rejected for the current Nexus model.

They would create dependencies and knowledge that the local artifact neither needs nor should possess.

A rule such as:

```text
this line was used recently elsewhere
therefore reduce its probability here
```

cannot be implemented without introducing a global observer or shared memory.

## Allowed local memory

This decision does not forbid every form of local state.

Local persistence may exist where it belongs to the artifact itself, for example when a completed local actualisation must remain stable after first opening.

However, such state must not be repurposed into a hidden behavioural profile or a cross-copy poetic history.

The distinction is:

```text
artifact state
→ may preserve this artifact's own completed result

behavioural history
→ must not track a person's or network's generation patterns

cross-copy memory
→ must not coordinate unrelated Nexus copies
```

## Accepted mechanism: curated scarcity

Formulaic output is reduced statically and locally through the reviewed structure of the library.

The preferred terms are:

```text
curated scarcity
static rarity
```

A memorable line may remain available while being structurally rarer than a neutral connective line.

This is not punishment for prior use. It is an intrinsic property of the block.

## Anti-formula instruments

### 1. Static block weights

Blocks may receive different weights according to how strongly they shape the recognisable surface of a poem.

Illustrative scale:

```text
low-signature support block      weight 4
medium-signature image block     weight 2 or 3
high-signature line              weight 1
```

The exact values remain world-specific and must be tested rather than universalised prematurely.

### 2. Route diversity

A strong line should not necessarily be reachable from every route.

Routes may distribute:

- different image fields;
- different relation types;
- different temporal movements;
- different syntactic shapes;
- and different forms of closure.

This reduces formulaic recurrence without requiring memory.

### 3. Pairwise compatibility

Two individually valid blocks may form an overly obvious machine pattern when combined.

Compatibility metadata may classify a pairing as:

```text
freely compatible
compatible but marked
rare pairing
emphatic reprise
avoid pairing
```

This classification concerns the function of the combination, not a semantic interpretation of the user's private words.

### 4. Curated emphatic reprise

Repetition remains a legitimate poetic instrument.

Related phrases, parallel syntax, and motif recurrence must not be automatically suppressed.

An exact duplicate rendered line is rejected by default, but may be allowed when explicitly curated as a reprise, echo, or answering return.

A pairing such as:

```text
their separate currents share one direction
the shared direction visible
```

may therefore remain available as an emphatic reprise while receiving a lower static weight than less marked pairings.

### 5. Syntax diversity

A library should not create apparent variety merely by exchanging nouns inside the same sentence pattern.

Useful variation includes:

- declarative movement;
- spatial observation;
- temporal shift;
- sensory trace;
- restrained action;
- elliptical condensation;
- relation held open;
- image-led rather than abstract closure.

### 6. Image and motif diversity

Several lines with different wording may still carry the same machine stamp when they repeatedly rely on the same image family.

World libraries should therefore avoid overdependence on a small set of motifs such as:

```text
open
trace
direction
distance
return
threshold
```

These motifs may remain central to the current world, but they require sufficiently different companions, movements, and syntactic functions.

### 7. Echo derivation from the selected long form

A Nexus Echo should inherit visible movement, imagery, or lexical trace from its own Resonance Artifact.

The more the Echo is derived from the actual selected plan, the less it feels like a generic machine signature attached afterward.

### 8. Multiple equivalent alternatives

The most reliable local protection against a dominant signature line is a set of several alternatives with comparable poetic quality.

The goal is not maximum combinatorics. It is a reviewed plurality of genuinely different possibilities.

## Signature strength

A later review may classify blocks and pairings by `signature_strength`.

Provisional categories:

```text
low
medium
high
```

Signature strength is not a quality score.

A high-signature line may be one of the strongest lines in the library. Its strength is precisely why repeated appearance can reveal the machinery beneath the poem.

The classification asks:

> How strongly would repeated use make the generator recognisable?

It does not ask:

> Is this line poetically good or bad?

## Local and cross-output quality

Two forms of anti-formula quality must be distinguished.

### Within one composition

The composer may locally check:

- exact duplicate rendered lines;
- incompatible pairings;
- excessive clustering of a marked phrase family;
- unresolved placeholders;
- and route-specific structural constraints.

### Across possible outputs

Without memory, the composer cannot know which outputs actually occurred elsewhere.

It can only make the overall possibility space healthier through:

- static rarity;
- broader alternatives;
- balanced routes;
- pairwise weighting;
- and review of seeded output distributions during development.

Development-time corpus review is allowed and desirable. Runtime surveillance is not.

## Development review versus runtime tracking

During development, maintainers may generate large local test corpora to inspect:

- block frequency under fixed weights;
- route dominance;
- recurring syntactic patterns;
- overly narrow Echo inheritance;
- and visible machine signatures.

These test corpora concern the reviewed prototype library.

They must not become a runtime collection system for users' private inputs or distributed Nexus outputs.

```text
development simulation
→ allowed

runtime central collection
→ rejected
```

## Privacy boundary

Anti-formula quality must never justify collecting private meaning.

The generator may inspect structural metadata that belongs to the public library and the local CompositionPlan.

It must not require:

- semantic profiling of the free words;
- uploading free words for quality analysis;
- user identity;
- social graph data;
- engagement metrics;
- or a history of what a person previously entered.

> Private meaning may create structure. Structure must not expose private meaning.

## Current application to the same-word route

For the current same-word experiment, this policy supports the following direction:

- keep `the first trace` as the common proxy;
- retain `the opening trace` as a rarer tonal variant;
- allow several relation and remainder pairings;
- preserve movement inheritance from the selected wish-entry block;
- keep directional repetition available as an emphatic reprise;
- assign marked pairings lower static weight rather than banning them;
- and expand alternatives before production integration.

No global usage history is required for any of these measures.

## Non-goals

This policy does not attempt to guarantee that every generated poem is unique across all Nexus copies.

Such a guarantee would require coordination or an impractically enormous deterministic namespace and would not itself ensure poetic quality.

The goal is instead:

> Each autonomous Nexus should contain a sufficiently rich and carefully weighted possibility space that formulaic recurrence is unlikely to dominate its surface.

The policy also does not seek to remove every recognisable trait from GlossAI.

A coherent poetic character is desirable. A repeated construction stamp is not.

```text
recognisable poetic ethics
→ desirable

recognisable assembly template
→ undesirable
```

## Acceptance criteria for later implementation

A future anti-formula implementation should satisfy all of the following:

1. It operates without global memory or cross-copy communication.
2. It does not upload or centrally count generated outputs.
3. It does not require user identity or behavioural history.
4. It preserves poetic repetition where explicitly curated.
5. It reduces the dominance of high-signature blocks through static local means.
6. It remains inspectable in library metadata and the CompositionPlan.
7. It can be tested with reproducible local corpora.
8. It does not alter private-word neutrality.
9. It does not introduce runtime semantic AI.
10. It remains compatible with autonomous transfer and local actualisation.

## Next review step

The next focused task is to classify the current mixed-world blocks and same-word pairings by provisional signature strength.

That review should identify:

- high-signature individual lines;
- high-signature Echo traces;
- emphatic reprise pairings;
- neutral connective material;
- and areas where additional alternatives are needed.

Only after that review should concrete static weights and a relation–remainder pairing matrix be committed.

## Core formulation

> Anti-formula quality must be carried by the form of the Nexus, not by a central memory of its copies.

And in the broader language of the project:

> The public repo shows the shape.  
> The private workspace carries the meaning.  
> The autonomous Nexus carries its own possibility space.
