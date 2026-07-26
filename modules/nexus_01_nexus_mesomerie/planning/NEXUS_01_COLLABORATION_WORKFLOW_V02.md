# Nexus 01 Collaboration Workflow V0.2

## Document status

- Version: 0.2
- Status: Current
- Date: 2026-07-26
- Supersedes: NEXUS_01_COLLABORATION_WORKFLOW_V01.md
- Purpose: Working agreement for planning, review, implementation, testing, documentation, repository curation, and release work after the major technical gift-sprint slices.

## 1. Principle

Nexus 01 uses a document-driven, multi-stage workflow:

```text
plan
-> independent review in fresh context
-> roadmap
-> independent roadmap review
-> work cards
-> independent work-card review
-> focused implementation
-> diff and test review
-> manual verification
-> acceptance, revision, or a decision that restoration is required
```

No review suggestion authorizes a change automatically. Reviews apply to completed planning levels or ready work-card packages; they do not require a new chat for every tiny wording correction.

## 2. Why the workflow changed

Codex supported the preceding phase through bounded technical inventories, implementation slices, and focused test additions.

The current phase is primarily editorial, experiential, documentary, repository-facing, and release-oriented. It therefore benefits from smaller decisions, explicit work cards, close dialogue, fresh-context review, and frequent manual play verification.

Codex is not planned as a regular implementation tool in this phase. A later targeted use remains possible after an explicit decision.

## 3. Roles

### Natali

- decides project goals, language, atmosphere, and player experience;
- defines and approves scope;
- performs decisive manual play verification;
- accepts or rejects review findings;
- authorizes work packages and high-impact repository, Git, release, and publication actions.

### Synthea

- inspects the current repository state;
- separates concept, architecture, player experience, language, documentation, and repository presentation;
- drafts plans, roadmaps, inventories, and work cards;
- performs authorized scope-conforming connector changes;
- reviews diffs and available test evidence;
- protects scope, privacy boundaries, history integrity, and the project thread;
- states uncertainty and incomplete verification explicitly;
- chooses connector or local work according to the task shape and explains the choice when risk is non-trivial;
- stops after an unexpected write result instead of starting an improvised repair chain.

### Fresh-context reviewer

A separate chat or deliberately fresh context receives only the material needed for review:

- the frozen document, roadmap, or work-card package;
- the review goal;
- non-negotiable technical, privacy, and release boundaries;
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

A completed roadmap receives a fresh-context review before work cards are treated as implementation-ready.

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

A work card should normally affect few files, avoid new architecture, and permit focused verification. A ready card package receives a fresh-context review before implementation begins.

## 5. Implementation cycle

For each accepted card:

```text
confirm branch and synchronization
-> inspect exact files
-> choose connector or local work
-> implement only the card scope
-> inspect the resulting changed-file set and diff
-> run focused tests where available
-> perform a short manual verification
-> accept, revise, or decide that restoration is required
```

A decision that restoration is required does not authorize a specific Git command. The restoration method is proposed, assessed, and approved within the applicable work-package or high-impact-action boundary.

A completed card does not authorize the next card automatically.

## 6. Work-package authorization and Git discipline

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

Local work and connector work must not create parallel divergent histories. Work occurs at one location at a time, and synchronization happens before the other location resumes.

An explicit approval applies to one clearly described work package. It includes the ordinary scope-conforming file reads, file writes, connector commits, diff checks, and branch synchronization steps needed to complete that package on the named working branch. Individual confirmation is not required for every routine substep.

Read-only inspection within an agreed review task likewise does not require separate confirmation for every read operation.

A new discussion and explicit approval are required when:

- the agreed scope would expand materially;
- files would be deleted, broadly moved, renamed, or structurally reorganized;
- architecture, imports, packaging, security boundaries, or test organization would change materially;
- another branch or `main` would be changed or checked out for write work;
- a merge, rebase, reset, force operation, or amend of published work is proposed;
- published Git history would be rewritten;
- a pull request, tag, release, or publication action is proposed;
- an unexpected risk requires a substantially different solution.

A normal fast-forward synchronization after an authorized connector work package belongs to that work package. It must still be shown transparently and must not conceal divergence, conflicts, or an unexpected branch state.

### 6.1 Choosing between connector work and local work

The connector remains an accepted repository tool for both read-only inspection and bounded write work.

Connector use is valuable because it can substantially reduce implementation effort and speed up small, well-scoped changes. The workflow does not require error-free connector work. It requires that unexpected results remain visible, bounded, reviewable, and repairable through Git.

Before every connector write, Synthea must verify that:

- the complete current content of every affected file is available;
- the complete intended replacement content has been prepared;
- the expected changed-file set is known;
- the work can safely create an immediate remote commit;
- no required test or manual verification must occur before that commit;
- the task can be completed without relying on an improvised repair sequence.

`update_file` replaces the complete file. It is not a patch operation.

Connector work is generally suitable when:

- the scope is small and clearly bounded;
- the complete affected file content is available;
- the intended replacement can be prepared and checked in full;
- the expected changed-file set is small and known;
- an immediate commit is acceptable;
- the resulting commit can be inspected immediately.

Local work is preferred when:

- displayed content is truncated, partial, paginated, or uncertain;
- production code and existing tests must change together;
- multiple files must form one atomic change;
- tests or manual terminal verification should run before commit;
- exact formatting, Unicode, indentation, or line endings are especially sensitive;
- the task involves rollback, restoration, or repair;
- a previous connector write in the same work package produced an unexpected result;
- the full replacement would be disproportionately difficult to verify compared with a small local patch.

The choice is based on the task shape and the available evidence, not on a fixed line-count or file-size threshold.

### 6.2 Immediate post-write verification

After every connector write, inspect immediately:

1. the changed-file set;
2. the complete diff;
3. the commit message and scope;
4. whether the result matches the approved work card;
5. whether any unexpected deletion, truncation, formatting change, or unrelated edit occurred.

A connector write is not treated as successful merely because a commit was created.

### 6.3 Unexpected connector results

If a connector write produces an unexpected result:

```text
stop
-> inspect read-only
-> describe the exact difference
-> inform Natali
-> propose one controlled repair path
```

No further connector write or repair commit is started automatically.

A failed or imperfect connector commit is not automatically a reason for history rewriting. Git may preserve a transparent correction history when that is safer and clearer.

A repair may continue through a normal follow-up commit when:

- the faulty state is understood;
- the repair scope is bounded;
- the repair method is explicitly accepted;
- the resulting diff can be verified;
- no hidden history change is involved.

Local restoration is preferred when the repair would otherwise require repeated full-file replacements or when confidence in the connector payload is reduced.

### 6.4 Git as a recovery and accountability mechanism

Git is expected to record both successful changes and occasional corrected mistakes.

The goal is not cosmetic history at any cost. The goals are:

- traceable decisions;
- bounded changes;
- reversible states;
- visible corrections;
- reliable current content;
- no concealed divergence or silent history manipulation.

A small number of transparent corrective commits is acceptable when they preserve safety and clarity.

No reset, rebase, amend, force push, branch-ref rewrite, squash of published work, or other history rewrite may be performed without explicit approval.

## 7. Public identity and privacy

Public project identity:

```text
Natali / Natali Reise
info@glossai.de
```

The technical connector identity `eulisiller` is acceptable for connector commits.

Private professional identities and combinations of private first names with the family name must not appear in public repository files, commits, issues, Wiki pages, release text, tags, or other public metadata.

Tracked documents must not contain private usernames, hostnames, home paths, addresses, private Token or Artifact contents, or other local machine identifiers.

Before release, a read-only metadata check covers relevant author names, author emails, committer names, committer emails, commit messages, and tag metadata where applicable. A problematic finding requires a separate decision and does not automatically authorize history rewriting.

## 8. Documentation workflow

Documentation work uses the same staged process:

```text
inventory
-> classify current, historical, working-note, drift, or later
-> define one primary home for each topic
-> roadmap
-> roadmap review
-> work cards
-> work-card review
-> link and consistency review
-> outside-perspective manual use
```

Repository documentation is authoritative for exact commands, formats, technical contracts, and version-sensitive behavior. The Wiki summarizes, orients, and links; it must not become a conflicting second source of truth.

## 9. Repository curation and cleanup boundary

The repository is not only a code store. It is part of the public, explorable Nexus project space and may be visited by players. Release-closeout work may therefore curate its visible current state.

Release-relevant public curation includes:

- current instructions and entry paths;
- dead-link repair;
- supersession and historical labels;
- clear navigation and document hierarchy;
- reduction of misleading duplicate entry guidance;
- `.gitignore` review against real local by-products;
- removal or correction of misleading release-facing placeholders;
- small documentation moves or renames when they materially improve player orientation and are separately reviewed.

Technical or historical restructuring is normally post-gift work. This includes broad code-directory reorganization, import-path changes for tidiness, test-architecture reorganization, broad Legacy removal, large file consolidation, and history rewriting.

Such technical restructuring enters the gift sprint only when a confirmed release blocker cannot be repaired safely by a smaller measure.

Published history is not rewritten for cosmetic cleanup during the gift sprint.

> Curate the visible present of the repository; preserve its history unless a separately approved exceptional decision is necessary.

## 10. Verification language

Claims must match evidence:

- `implemented` does not mean manually accepted;
- `focused test passed` does not mean the full suite passed;
- an older full-suite result remains historical evidence, not proof for later commits;
- a manual happy-path run does not prove every error path;
- a review finding remains a proposal until accepted;
- a created connector commit does not by itself prove that the intended change was applied correctly;
- a successful repair does not erase the historical fact that a correction was needed.

## 11. Gift-sprint and post-gift boundary

Gift sprint:

```text
complete
-> simplify
-> document
-> curate
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
