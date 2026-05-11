# COSMOS.md — Cosmos Vibe Harness Constitution

This repository is managed as a Cosmos Vibe multiverse harness.

## Universe Rules

- Each Universe runs independently in its own `universes/<name>/` worktree
- Do NOT directly copy code from other universes
- Record every significant discovery to `.quantum/<name>/insights.jsonl`
- After each major implementation step, read `.quantum/*/insights.jsonl` to
  pick up insights from other universes
- Entanglement means influence, not convergence — preserve your strategy

## Quantum Memory

- Location: `.quantum/` at repo root (excluded from git)
- Each universe writes ONLY to its own namespace: `.quantum/<name>/insights.jsonl`
- All universes may READ all namespaces
- Format: one JSON object per line — `{"content": "...", "ts": "..."}`

## Skills

- `/cosmos spawn --goal "<goal>" --strategies "<s1,s2,s3>"` — launch universes
- `/cosmos observe` — superposition snapshot + entanglement map
- `/cosmos crystallize <id>` — extract a universe's result
- `/cosmos stop` — remove all worktrees and branches
