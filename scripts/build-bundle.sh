#!/usr/bin/env bash
# Regenerate bundle/cosmos-instructions.md from skills/*/SKILL.md.
#
# This is the single source of truth for how the universal bundle is built.
# Run after editing any SKILL.md, and commit the bundle along with the change.
# CI runs this and diffs against the committed bundle to detect drift.
#
# Usage:
#   scripts/build-bundle.sh                # writes to bundle/cosmos-instructions.md
#   scripts/build-bundle.sh --check        # writes to stdout, exit 1 if drift

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO_ROOT"

generate() {
  cat <<'HEADER'
# QuantumAgent — Cosmos Workflow Instructions (Universal Bundle)

> This file is platform-neutral. Paste it as a system prompt, custom instructions,
> rules file, or convention file in any AI coding agent. See INTEGRATIONS.md for
> per-platform setup.

## Overview

QuantumAgent runs **multiple AI agents in parallel** ("cosmos"), each tackling
the same goal with a different strategy. Agents share live discoveries through
Quantum Memory (.quantum/*.jsonl files) — entanglement without external
infrastructure.

## Trigger phrases (any of)

- "cosmos spawn", "spawn cosmos", "run cosmos with strategies X, Y, Z"
- "cosmos observe", "show cosmos status"
- "cosmos crystallize <name>", "ship cosmos <name>"
- "cosmos stop", "tear down cosmos"

When the user says any of these, follow the matching workflow below.

## Filesystem contract (all platforms)

- `cosmos/<name>/` — git worktree per cosmos
- `cosmos/<name>` branch — tracks the worktree
- `.quantum/<name>/insights.jsonl` — append-only insights, one JSON object per line
- `.gitignore` must exclude `cosmos/` and `.quantum/`

Multiple agents (Claude Code, Cursor, Aider, etc.) can interoperate via this
shared on-disk contract.

---

HEADER

  for skill in spawn observe crystallize stop; do
    echo ""
    echo "---"
    echo ""
    # tail -n +5 skips the YAML frontmatter (---, name, description, ---) and the blank line after it
    tail -n +5 "skills/$skill/SKILL.md"
  done
}

if [ "${1:-}" = "--check" ]; then
  tmp=$(mktemp)
  trap 'rm -f "$tmp"' EXIT
  generate > "$tmp"
  if ! diff -q "$tmp" bundle/cosmos-instructions.md >/dev/null 2>&1; then
    echo "❌ bundle/cosmos-instructions.md is out of sync with skills/*/SKILL.md" >&2
    echo "   Regenerate with: scripts/build-bundle.sh" >&2
    echo "" >&2
    diff "$tmp" bundle/cosmos-instructions.md | head -50 >&2
    exit 1
  fi
  echo "✓ bundle is in sync with skills/"
else
  generate > bundle/cosmos-instructions.md
  echo "✓ wrote bundle/cosmos-instructions.md ($(wc -l < bundle/cosmos-instructions.md) lines)"
fi
