# COSMOS.md — QuantumAgent Harness Constitution

This repository is managed as a QuantumAgent multiverse harness (parallel cosmos exploration).

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
- Format: one JSON object per line — `{"content": "...", "ts": "..."}`

## Quantum Signals

- **Resonance** — multiple cosmos independently reach the same conclusion → ship with confidence
- **Uncertainty** — cosmos diverge on a decision → conscious tradeoff, developer chooses
- **Degeneracy** — different strategies produce functionally identical implementations → single natural solution exists
- **Decoherence** — a cosmos loses its strategy by copying others → flag, not a true sample
- **Quantum Tunneling** (`[TUNNEL]`) — a cosmos bypasses an assumed hard constraint → unexpected solution path
- **Quantum Jump** (`[JUMP]`) — a single entanglement read causes discontinuous architectural shift → non-obvious leap
- **Bose-Einstein Condensate** — zero uncertainty + ≥3 resonant decisions + all cosmos participated → goal was deterministic

## Skills

- `/cosmos spawn --goal "<goal>" --strategies "<s1,s2,s3>"` — launch cosmos
- `/cosmos observe` — superposition snapshot + resonance/uncertainty map
- `/cosmos crystallize <id>` — collapse one cosmos into a result
- `/cosmos stop` — remove all worktrees and branches
