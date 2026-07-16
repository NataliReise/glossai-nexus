# Nexus 01 Intentional Archive

Status: current archive policy

This directory preserves selected superseded implementations, tests, fixtures, and design history that still have technical, poetic, migration, or explanatory value.

It is not a dumping ground.

Git history remains the complete historical record. Material belongs in this visible archive only when a present-day reader may still need to understand, execute, compare, migrate, or learn from it.

## Archive rules

1. Active production code must never import from `archive/`.
2. Archived code must not be presented as the current Nexus implementation.
3. Every archived system must have its own README explaining its historical role and status.
4. Runtime code, tests, and fixtures move together when they form one historical executable unit.
5. Imports, documentation links, and active test commands must be updated before a move is considered complete.
6. Files with no continuing reference value should be removed from the current tree and left to Git history rather than copied into the archive.
7. Private local data, generated gifts, result files, and personal activation material must never be archived in the public repository.

## Planned structure

```text
archive/
  README.md

  resonance_v0_1_deterministic/
    README.md
    language_library/
    renderers/
    fixtures/
    tests/
    design_history/

  resonance_v0_2_longform_composer/
    README.md
    prototype/
    probe_series/
    reviews/
    design_history/
```

The exact structure may be simplified after the dependency inventory. The important requirement is a clear separation between active code and historical systems.

## Required archive README fields

Each archived system README should state:

```text
Status
Active production use
Historical period
What the system demonstrated
Why it was superseded
Which ideas survived
Whether the code is still executable
How historical tests may be run
Known dependencies
Current successor
```

## Migration safety

No directory move should occur before:

- active and historical imports have been searched;
- tests and fixtures have been mapped;
- command-line entry points have been identified;
- documentation links have been classified;
- the current replacement direction has been recorded;
- a clean baseline commit is known.

The transition baseline immediately before the Nachhall pivot is:

```text
153522ce5f72d04560797503ba99bbbd62e61a72
Document relation and remainder pairing matrix
```

This commit remains an easy historical reference even before a local Git tag is created.

## Archive principle

```text
The active tree explains how the Nexus works now
The archive explains how that understanding was reached
```
