# Public Handoff Checklist

Status: Draft  
Project: Nexus / First Spark  
Purpose: Check whether the First Spark module can be safely shared publicly.

## Core Principle

First make the spark safe to carry.  
Then specify how the trace travels.

## Scope of This Checklist

This checklist is for public sharing only.

It applies to situations such as:

- a public Git repository
- an open-source release
- a public demo package
- a neutral downloadable version
- a version that may be copied, forked, inspected, or reused by unknown people

A public handoff must not contain real private activation data.

The public version of First Spark should be neutral, clean, safe to inspect, and usable without personal configuration.

## Not Covered Here

This checklist does not describe a private gift handoff.

A private gift handoff is a different situation. It may include a real activation for a specific person, but that activation must stay outside the public repository and outside the public module.

A private gift handoff needs a separate private activation package.

Possible later specification files:

```text
PRIVATE_GIFT_HANDOFF.md
```

or:

```text
GIFT_PACKAGE_SPEC.md
```

Those files should define how an activated gift version can be created, packaged, and handed over safely without blurring the public/private boundary.

## Public Handoff Definition

A public handoff means:

- the module is publicly shareable
- the module works in neutral mode
- no real private activation is included
- no personal gift text is included
- no local configuration is included
- no `activation.local.json` is included
- the demo or neutral fallback works
- the public/private boundary remains intact

## Private Gift Handoff Definition

A private gift handoff means:

- the module is prepared for a specific person
- a private activation may be included or provided separately
- the activation is not committed to the public Git repository
- the activation is not part of the public release
- the recipient receives clear private start instructions
- the gift package is transferred through a private channel

This checklist does not validate private gift packages.

## 1. Repository State

Before public handoff, check:

- [ ] `git status --short` shows no unexpected changes.
- [ ] All intended public changes are committed.
- [ ] No temporary files are present.
- [ ] No editor backup files are present.
- [ ] No local cache files are present.
- [ ] No generated private files are staged or tracked.
- [ ] The working tree is clean or all remaining changes are intentionally excluded from the public handoff.

Suggested command:

```bash
git status --short
```

## 2. Tests

Before public handoff, check:

- [ ] All current First Spark tests pass.
- [ ] The module starts successfully without private activation data.
- [ ] The neutral fallback path works.
- [ ] Invalid activation data produces a friendly explanation.
- [ ] The activation helper behaves safely.
- [ ] The activation helper does not overwrite existing local activation data.

Current First Spark test command:

```bash
python3 modules/nexus_01_nexus_mesomerie/first_spark/tests/test_first_spark_flow.py
```

Future pytest command, if pytest is introduced later:

```bash
python -m pytest
```

## 3. Public / Private Boundary

The public module must not contain private, local, or recipient-specific data.

Absence check:

- [ ] `activation.local.json` is absent.
- [ ] Real private activation data is absent.
- [ ] Real private gift messages are absent.
- [ ] Recipient-specific gift configuration is absent.
- [ ] Personal names that should not be public are absent.
- [ ] Private relationship references are absent.
- [ ] Local file paths are absent.
- [ ] Machine-specific paths are absent.
- [ ] Private notes are absent.
- [ ] Local test data with personal content is absent.
- [ ] Secrets, tokens, keys, or credentials are absent.

The public module may contain:

- [ ] safe example activation data
- [ ] neutral fallback text
- [ ] public documentation
- [ ] public source code
- [ ] public tests
- [ ] safe placeholder values
- [ ] safe demo messages that are clearly fictional or generic

## 4. Activation Files

Before public handoff, check:

- [ ] `activation.local.json` is ignored by Git.
- [ ] `activation.local.json` is not tracked.
- [ ] `activation.local.json` is not included in the public package.
- [ ] `activation.example.json` contains only safe demo data.
- [ ] The README explains the difference between local activation and example activation.
- [ ] The local activation helper creates local data only when explicitly run.
- [ ] The local activation helper refuses to overwrite existing activation data unless this behavior is explicitly and safely designed.

Suggested commands:

```bash
git check-ignore modules/nexus_01_nexus_mesomerie/first_spark/activation.local.json
git ls-files | grep 'modules/nexus_01_nexus_mesomerie/first_spark/activation.local.json'
```

Expected result:

- `git check-ignore ...` confirms that the file is ignored.
- `git ls-files | grep ...` returns nothing.

## 5. Neutral Public Mode

Before public handoff, check:

- [ ] The module runs without `activation.local.json`.
- [ ] The experience remains coherent in neutral mode.
- [ ] No error occurs just because private activation is missing.
- [ ] The neutral fallback does not sound broken, unfinished, or accidentally intimate.
- [ ] The neutral fallback makes clear that personalization is optional.
- [ ] The public version feels intentionally neutral, not accidentally stripped.

## 6. Invalid Activation Handling

Before public handoff, check:

- [ ] Broken activation JSON does not crash the module obscurely.
- [ ] Missing required activation fields are handled gracefully.
- [ ] Invalid activation data produces a friendly explanation.
- [ ] The explanation does not expose technical internals unnecessarily.
- [ ] The user is guided toward using the example file or helper.

## 7. Documentation

Before public handoff, check that the documentation explains:

- [ ] what First Spark is
- [ ] how to run it publicly in neutral mode
- [ ] how neutral fallback works
- [ ] why no real activation is included in the public module
- [ ] what `activation.example.json` is for
- [ ] why `activation.local.json` is private
- [ ] what should never be committed
- [ ] what is intentionally public
- [ ] what is intentionally private
- [ ] that private gift handoff is a separate process

Relevant documentation files:

- [ ] `README.md`
- [ ] `LOCAL_ACTIVATION_GUIDE.md`
- [ ] `activation.example.json`
- [ ] this checklist

## 8. Manual Public Run Check

Before public handoff, run the module in public mode.

### Clean Public Mode

- [ ] Remove or temporarily move `activation.local.json`.
- [ ] Start the module.
- [ ] Confirm that neutral fallback works.
- [ ] Confirm that no private content appears.
- [ ] Confirm that the experience is understandable for someone who has no private activation package.

### Invalid Activation Check

- [ ] Temporarily create invalid activation data.
- [ ] Start the module.
- [ ] Confirm that the error is friendly and understandable.
- [ ] Restore valid or absent activation afterward.

A valid private activation may be tested during development, but it is not part of the public handoff check.

## 9. Public Package Check

Before public handoff, check the actual folder or archive that will be shared.

The public handoff package should include:

- [ ] source code required to run First Spark
- [ ] public documentation
- [ ] safe example activation
- [ ] tests if intended
- [ ] license if applicable

Absence check:

- [ ] `activation.local.json` is absent from the public package.
- [ ] Private activation data is absent from the public package.
- [ ] Personal gift data is absent from the public package.
- [ ] Local machine state is absent from the public package.
- [ ] Accidental hidden/private files are absent from the public package.

Suggested command for inspecting files:

```bash
find . -maxdepth 3 -type f | sort
```

Review the output manually before sharing.

## 10. Final Public Handoff Decision

Public handoff is allowed only if:

- [ ] tests are green
- [ ] git state is clean
- [ ] private activation is ignored
- [ ] private activation is not tracked
- [ ] private activation is not included
- [ ] neutral fallback works
- [ ] invalid activation is explained
- [ ] activation helper is safe and non-overwriting
- [ ] documentation is sufficient
- [ ] private gift text is absent
- [ ] local configuration is absent
- [ ] the public package has been manually inspected

## Handoff Result

Date:

Checked by:

Result:

- [ ] Ready for public handoff
- [ ] Not ready yet

Notes:

```text
Add any remaining concerns, known limitations, or follow-up tasks here.
```

## Next Step After Public Handoff Safety

After First Spark is safe to carry publicly, the next larger specification can describe how the trace travels.

Possible next file:

```text
MVP_NEXUS_01.md
```

or:

```text
GAME_FLOW.md
```

That later specification should describe the larger A -> B -> A resonance arc:

```text
A plays.
A receives a resonance code.
A gives the module and code to B.
B starts a carried activation.
B plays.
B creates a return key.
B gives the return key back to A.
A unlocks a deeper return layer.
```

This larger arc is intentionally not the next immediate Running Unit.

Before that, a separate private handoff specification may be useful:

```text
PRIVATE_GIFT_HANDOFF.md
```

or:

```text
GIFT_PACKAGE_SPEC.md
```

That file should describe how a concrete activated gift can be handed over privately and safely.
