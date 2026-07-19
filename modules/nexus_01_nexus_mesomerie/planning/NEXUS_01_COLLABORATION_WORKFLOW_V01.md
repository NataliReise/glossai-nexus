# Nexus 01 Collaboration Workflow V0.1

## Document status

- Version: 0.1
- Status: Current
- Date: 2026-07-19
- Purpose: Working agreement for planning, review, implementation, testing, documentation, and release work after the major technical gift-sprint slices.

## 1. Principle

Nexus 01 uses a document-driven, multi-stage workflow:

```text
plan
-> independent review in fresh context
-> roadmap
-> independent review
-> work cards
-> independent review
-> focused implementation
-> diff and test review
-> manual verification
-> acceptance or revision
```

No review suggestion authorizes a change automatically.

## 2. Why the workflow changed

Codex supported the preceding phase through bounded technical inventories, implementation slices, and focused test additions.

The current phase is primarily editorial, experiential, documentary, and release-oriented. It therefore benefits from smaller decisions, explicit work cards, close dialogue, fresh-context review, and frequent manual play verification.

Codex is not planned as a regular implementation tool in this phase. A later targeted use remains possible after an explicit decision.

## 3. Roles

### Natali

- decides project goals, language, atmosphere, and player experience;
- defines and approves scope;
- performs decisive manual play verification;
- accepts or rejects review findings;
- authorizes repository, Git, release, and publication actions.

### Synthea

- inspects the current repository state;
- separates concept, architecture, player experience, language, and documentation;
- drafts plans, roadmaps, inventories, and work cards;
- performs explicitly authorized small connector changes;
- reviews diffs and available test evidence;
- protects scope, privacy boundaries, and the project thread;
- states uncertainty and incomplete verification explicitly.

### Fresh-context reviewer

A separate chat or deliberately fresh context receives only the material needed for review:

- the frozen document or work card;
- the review goal;
- non-negotiable technical and privacy boundaries;
- concrete repository evidence where necessary.

The reviewer searches for contradictions, missing prerequisites, unclear completion criteria, hidden scope growth, documentation drift, and safety risks. The reviewer does not implement changes and does not decide acceptance.

## 4. Planning stages

### Stage A — Goal and constraints

Clarify:

- what the user or player should experience;
- what the current release must accomplish;
- what is explicitly outside scope;
- which technical and privacy invariants must remain unchanged;
- how success will be verified.

The result is written into a versioned Markdown plan.

### Stage B — Plan review

A fresh context checks the plan before implementation planning begins. Findings are decided individually.

### Stage C — Roadmap

The accepted plan is divided into phases and bounded packages. The roadmap records dependencies, order, review gates, and release boundaries.

### Stage D — Work cards

Each package is divided into small implementation cards. A card contains:

```text
ID
Title
Starting point
Player or repository problem
Desired result
In scope
Out of scope
Affected files
Unchanged invariants
Tests
Manual verification
Definition of done
Abort or rollback criterion
```

A work card should normally affect few files, avoid new architecture, and permit focused verification.

## 5. Implementation cycle

For each accepted card:

```text
confirm branch and synchronization
-> inspect exact files
-> implement only the card scope
-> inspect the resulting diff
-> run focused tests where available
-> perform a short manual verification
-> accept, revise, or revert
```

A completed card does not authorize the next card automatically.

## 6. Connector and local Git discipline

Current working branch:

```text
gift/nexus-01-chamber-archive
```

Before a new change, confirm:

```bash
git status -sb
git branch --show-current
git rev-parse --short HEAD
```

Local work and connector work must not create parallel divergent histories. Work occurs at one location at a time and synchronization happens before the other location resumes.

Connector writes create commits directly on the named remote branch. They require explicit authorization and must be followed by a local fast-forward pull before local work continues.

No branch change, merge, rebase, reset, history rewrite, push, pull request, tag, or release action occurs without explicit authorization.

## 7. Public identity and privacy

Public project identity:

```text
Natali / Natali Reise
info@glossai.de
```

The technical connector identity `eulisiller` is acceptable for connector commits.

Private professional identities and combinations of private first names with the family name must not appear in public repository files, commits, issues, Wiki pages, or release text.

Tracked documents must not contain private usernames, hostnames, home paths, addresses, private Token or Artifact contents, or other local machine identifiers.

## 8. Documentation workflow

Documentation work uses the same staged process:

```text
inventory
-> classify current, historical, working-note, drift, or later
-> define one primary home for each topic
-> roadmap
-> work cards
-> link and consistency review
-> outside-perspective manual use
```

Repository documentation is authoritative for exact commands, formats, technical contracts, and version-sensitive behavior. The Wiki summarizes, orients, and links; it must not become a conflicting second source of truth.

## 9. Repository cleanup boundary

Safe release-closeout cleanup includes current instructions, dead links, supersession labels, navigation, duplicate entry guidance, `.gitignore` review, and misleading release-facing placeholders.

Moves, renames, deletions, structural reorganization, Legacy removal, import changes, and history rewriting require separate cards and stronger review.

> Clean the visible present of the repository, not its history for cosmetic reasons.

## 10. Verification language

Claims must match evidence:

- `implemented` does not mean manually accepted;
- `focused test passed` does not mean the full suite passed;
- an older full-suite result remains historical evidence, not proof for later commits;
- a manual happy-path run does not prove every error path;
- a review finding remains a proposal until accepted.

## 11. Gift-sprint and post-gift boundary

Gift sprint:

```text
complete
-> simplify
-> document
-> verify
-> freeze
```

Post-gift development:

```text
retrospect
-> explore
-> extend
-> abstract
-> test new forms
```

The gift release remains a documented historical milestone. Normal project development begins with a separate retrospective and roadmap rather than silently extending the gift sprint.
