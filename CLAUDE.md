# COSMOS.md — QuantumAgent Harness Constitution

This repository is managed as a QuantumAgent multiverse harness (parallel cosmos exploration).

## Architecture — Git-Native Orchestration

QuantumAgent follows a two-layer architecture:

- **Control Plane** — intent, plans, context, memory, and review live as
  Markdown and JSONL files in the git working tree. Both humans and AI
  agents read/write the same artifacts; everything is diffable, reviewable,
  and reversible via standard git workflows.
- **Effector Layer** — external APIs, databases, browsers, and local
  execution are handled by whatever the host agent already has (its native
  tools, MCP servers, CLI access). QuantumAgent does not own this layer —
  it leaves effector choice to the host, keeping the Control Plane
  agent-agnostic.

The filesystem contract (`.quantum/<name>/insights.jsonl`, `cosmos/<name>/`
worktrees) is the interop boundary. Any agent that can read a markdown
file and run `git worktree` can participate.

## Cosmos Rules

- Each cosmos runs independently in its own `cosmos/<name>/` worktree
- Do NOT directly copy code from another cosmos
- Record every significant discovery to `.quantum/<name>/insights.jsonl`
- After each major implementation step, read `.quantum/*/insights.jsonl`
- Resonance (convergence) = trust the signal. Decoherence (wholesale copying) = forbidden.
- Entanglement means influence, not convergence — preserve your strategy

## Quantum Memory

- Location: `.quantum/` at repo root (excluded from git)
- Each cosmos writes ONLY to its own namespace: `.quantum/<name>/insights.jsonl`
- All cosmos may READ all namespaces
- Format: one JSON object per line:
  `{"type": "<type>", "content": "...", "ts": "<ISO 8601>"}`
- `type` vocabulary: `discovery` (default), `decision`, `blocker`,
  `tunnel`, `jump`, `resonance`, `complete`, `crystallize`
- Legacy entries without `type` (or with `[TUNNEL]`/`[JUMP]` content
  prefixes) remain readable; treat missing `type` as `discovery`.
- Concurrency: append is atomic on POSIX for sub-PIPE_BUF writes.
  Sequential single-agent appends are safe. If you spawn sub-agents that
  may write to the SAME insights file concurrently, wrap appends with
  `flock` or write-then-rename.

## Quantum Signals

- **Resonance** — multiple cosmos independently reach the same conclusion → ship with confidence
- **Uncertainty** — cosmos diverge on a decision → conscious tradeoff, developer chooses
- **Degeneracy** — different strategies produce functionally identical implementations → single natural solution exists
- **Decoherence** — a cosmos loses its strategy by copying others → flag, not a true sample
- **Quantum Tunneling** (`type: "tunnel"`) — a cosmos bypasses an assumed hard constraint → unexpected solution path
- **Quantum Jump** (`type: "jump"`) — a single entanglement read causes discontinuous architectural shift → non-obvious leap
- **Bose-Einstein Condensate** — zero uncertainty + ≥3 resonant decisions + all cosmos participated → goal was deterministic

## Skills

- `/cosmos spawn --goal "<goal>" --strategies "<s1,s2,s3>"` — launch cosmos
- `/cosmos observe` — superposition snapshot + resonance/uncertainty map
- `/cosmos crystallize <id>` — collapse one cosmos into a result
- `/cosmos stop` — remove all worktrees and branches
