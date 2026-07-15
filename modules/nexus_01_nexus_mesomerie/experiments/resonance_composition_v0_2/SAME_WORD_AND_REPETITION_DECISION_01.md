# Same-Word and Repetition Decision 01

This note records two poetic decisions for the isolated Resonance V0.2 microprototype.

It does not alter the V0.1 production path.

## 1. Repetition is not treated as an error by default

Parallel wording, recurrence, and gradual reformulation remain available as poetic means.

The prototype should distinguish:

```text
parallel or related wording
  allowed

exact duplicate rendered line
  rejected by default

exact duplicate rendered line marked as an explicit reprise
  allowed
```

The machine does not infer whether a repetition is meaningful. A library author must explicitly curate an exact reprise.

## 2. Same-word mode

Same-word mode is activated only by lexical identity after Unicode case folding:

```text
wish_word.casefold() == return_word.casefold()
```

No synonymy, translation, morphological similarity, or semantic relation is inferred.

When active:

- both original input fields remain preserved in provenance;
- the shared submitted word remains visible in the return role;
- the wish role uses one curated world-compatible proxy;
- the shared word should normally appear only once in the visible long form;
- the shared word remains the complete fifth line of the Nexus Echo;
- the selected proxy is recorded in the Composition Plan.

The first provisional proxy pool for `mixed-threshold-return-world` is:

```text
the first trace
the opening trace
```

`the first trace` receives the stronger initial weight.

## 3. Implementation seam

The first implementation is deliberately separated into:

```text
same_word_policy.py
```

It currently provides:

- lexical identity detection;
- weighted proxy choice with injectable randomness;
- rejection of accidental exact rendered-line duplication;
- explicit permission for curated reprises;
- no restriction on non-identical parallel lines.

The policy should be integrated into the executable composer only after its isolated tests and interface have been reviewed.

## 4. Current boundary

This decision does not yet define:

- final same-word Echo templates;
- persistence representation;
- production artifact migration;
- proxy pools for the other two prototype worlds;
- whether one or several proxies should survive poetic review.

Those decisions should be based on generated same-word examples rather than schema preference alone.
