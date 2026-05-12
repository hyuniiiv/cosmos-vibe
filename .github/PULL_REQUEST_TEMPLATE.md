<!-- Thanks for opening a PR. A few quick checks below — feel free to delete sections that don't apply. -->

## What changed

<!-- One-paragraph summary of the change. -->

## Why

<!-- The problem this solves or the value it adds. -->

## How

<!-- Approach and any noteworthy implementation details. -->

## Verification

- [ ] `bash tests/conformance.sh` passes locally (16/16)
- [ ] Manually tested in: <!-- Claude Code / Cursor / Cline / Aider / other -->
- [ ] No new dependencies (or justified below)

## Filesystem contract

- [ ] No changes to `.quantum/` or `cosmos/` semantics
- [ ] If yes → conformance test in `tests/conformance.sh` updated accordingly

## If this is a new integration

- [ ] Row added to compatibility matrix in `INTEGRATIONS.md`
- [ ] Per-platform setup section added with concrete install commands
- [ ] Verified the agent can honor the filesystem contract

## Skill sync (if `skills/*/SKILL.md` changed)

- [ ] Ran `cd mcp && npm run sync-skills` (or copied manually) so `mcp/skills/` matches
- [ ] Regenerated `bundle/cosmos-instructions.md` if needed

## CHANGELOG

- [ ] Added an entry under `## [Unreleased]` (if user-visible)
