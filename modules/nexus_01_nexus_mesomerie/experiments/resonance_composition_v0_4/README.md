# Resonance Composition V0.4 Experiment

Status: isolated experimental spike  
Production use: no

This directory tests a compact, profile-driven Resonance Return composer. It
does not import from, write to, or replace any active activation, Atrium,
Chamber, return-opening, Return Slot, Return Artifact, or packaging path.

## Smallest useful design

The visible result retains the compact `2 / 4 / 6 / 4 / 1` shape: five lines
and seventeen whitespace-delimited words. Three micro-routes place the wish
word early, centrally, or late and give it a different grammatical function.
The return word remains the complete final line.

Every supported source ID resolves to a curated lexical profile. Profiles
contain reviewed fragments, grammatical roles, visible-noun annotations, and
content-verb annotations. They are not a free thesaurus. A route joins one
fragment from every one of the six ID profiles with the two unanalysed free
words.

Selection is local and seedable. Candidate compositions are rejected when
they contain unresolved placeholders, repeat the same annotated content verb
on adjacent lines, repeat an annotated visible noun more than twice, displace
the wish slot, lose the final return word, or violate the visible form.

## Supported scope

The library supports only the five exact current Chamber reference paths
listed in `profiles.v0_4.json`. Mixing otherwise known IDs is intentionally not
treated as supported. This is a reviewed sample, not complete combinatorial
coverage.

## Reused ideas

From V0.2:

- curated profiles and operator-aware fragments;
- inspectable composition plans and seeded probe corpora;
- static local weights instead of global memory;
- pair/collision checks and explicit same-word slot handling;
- readable, bounded failure rather than forced output.

From V0.3:

- the compact poem as the complete result;
- exact structural validation;
- curated complete phrase fragments;
- genuinely different wish-placement routes;
- Unicode letter-only free words and deterministic test randomness.

## Intentionally rejected

- mandatory long-form composition before the compact result;
- production integration, persistence, opening, or packaging changes;
- semantic analysis, inflection, translation, or proxying of free words;
- unconstrained verb/noun recombination or a free thesaurus;
- global cooldowns, usage history, or remote coordination;
- claims that unsupported combinations are complete;
- variation made only by reordering identical lines.

## Commands

From this directory:

```text
python3 -m unittest -v test_composer.py
python3 generate_review_corpus.py
python3 composer.py --world clear-meeting --wish courage --return-word trust --seed 17 --show-plan
```

