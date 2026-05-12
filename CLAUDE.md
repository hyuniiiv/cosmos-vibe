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

QuantumAgent's quantum memory operates at three scales (v1.2+):

```
.quantum/
  <name>/insights.jsonl        — cosmos scale (per-agent insights)
  project/spin.json            — macro scale: project identity (v1.2)
  singularities/events.jsonl   — macro scale: project-level events (v1.2)
```

**Cosmos scale (insights):**
- Each cosmos writes ONLY to its own namespace: `.quantum/<name>/insights.jsonl`
- All cosmos may READ all namespaces
- Format: one JSON object per line:
  `{"type": "<type>", "content": "...", "ts": "<ISO 8601>"}`
- `type` vocabulary: `discovery` (default), `decision`, `blocker`,
  `tunnel`, `jump`, `resonance`, `complete`, `crystallize`
- Legacy entries without `type` (or with `[TUNNEL]`/`[JUMP]` content
  prefixes) remain readable; treat missing `type` as `discovery`.

**Macro scale (v1.2 — project spin + singularities):**
- `project/spin.json` — optional, declares project's immutable identity.
  Auto-injected into every cosmos's CLAUDE.md as invariant constraints.
- `singularities/events.jsonl` — append-only log of project-level events
  (migrations, paradigm shifts, compliance changes). Each spawn reads
  this and treats pre-singularity insights matching `invalidates` patterns
  as stale.
- Both files are optional. A project without them runs as a "free"
  multiverse with no inherited constraints — useful for greenfield work.

**Concurrency:** append is atomic on POSIX for sub-PIPE_BUF writes.
  Sequential single-agent appends are safe. If you spawn sub-agents that
  may write to the SAME insights file concurrently, wrap appends with
  `flock` or write-then-rename.

## Entanglement Modes (v1.2 — extended in v1.3)

`/cosmos spawn` accepts `--entanglement <mode>`:

- `none` — cosmos do not read other cosmos insights (pure independent exploration)
- `passive` *(default)* — cosmos read insights between major steps (current behavior)
- `active` — cosmos read AND record `read_from: cosmos:<source>` when adopting another's pattern (traceability)
- `strict` *(v1.3)* — heartbeat protocol. Each cosmos publishes `heartbeat` per step AND must write `heartbeat-ack` for every unacknowledged heartbeat from other cosmos before its next step. `/cosmos observe` audits the heartbeat graph and reports entanglement quality (High/Medium/Low) plus any broken channels.

The mode chosen for a run determines how strictly entanglement is enforced. `none` is appropriate when you want true statistical independence; `active` is appropriate when audit traceability matters; `strict` is appropriate when you need observable proof of live agent communication (race conditions, distributed system semantics, compliance audits).

## Quantum Signals

- **Resonance** — multiple cosmos independently reach the same conclusion → ship with confidence
- **Uncertainty** — cosmos diverge on a decision → conscious tradeoff, developer chooses
- **Degeneracy** — different strategies produce functionally identical implementations → single natural solution exists
- **Decoherence** — a cosmos loses its strategy by copying others → flag, not a true sample
- **Quantum Tunneling** (`type: "tunnel"`) — a cosmos bypasses an assumed hard constraint → unexpected solution path
- **Quantum Jump** (`type: "jump"`) — a single entanglement read causes discontinuous architectural shift → non-obvious leap
- **Bose-Einstein Condensate** — zero uncertainty + ≥3 resonant decisions + all cosmos participated → goal was deterministic

## Architecture — three layers

QuantumAgent is layered. Each layer exposes the same quantum-decision model in a different idiom:

- **Layer 1 — CLI** (Claude Code skills): imperative, agent-backed. The original interface.
- **Layer 2 — YAML DSL** (`experiments/*.qa.yaml`): declarative, agent-backed. Reproducible experiments as code.
- **Layer 3 — Python primitives** (`pip install -e python/`): programmable, math-backed. Compose decisions directly in any Python program.

All three layers share concepts (ψ, entanglement, observe vs measure, constraint operators) but execute differently. Mix freely.

## Skills (Layer 1 + 2)

- `/cosmos spawn --goal "<goal>" --strategies "<s1,s2,s3>" [--entanglement <mode>] [--models <m1,m2,m3>]` — launch cosmos (v3.3: per-cosmos model)
- `/cosmos observe` — superposition snapshot + resonance/uncertainty map + macro context + entanglement quality
- `/cosmos crystallize <id>` — collapse one cosmos into a result
- `/cosmos stop` — remove all worktrees and branches
- `/cosmos singularity --name "<event>" --invalidates "<patterns>"` *(v1.2)* — declare a project-level event that reshapes context for all future spawns
- `/cosmos spin --name "<name>" [--type "<type>"] [--constraints "<c1,c2,c3>"]` *(v1.3)* — declare or update the project's immutable identity; auto-injected into every future spawn
- `/cosmos run <path-to-yaml>` *(v2.0)* — execute a declarative quantum experiment defined in YAML; orchestrates spin + singularities + spawn in one command for reproducible CI/CD-grade runs
- `/cosmos scan [--paths "..."] [--languages "..."] [--git-churn-threshold N]` *(v4.0)* — scan codebase for code-level quantum phenomena (type-system bypasses = tunnel, untested files = decoherence, feature flags = superposition, high churn = jump). Writes to `.quantum/code/findings.jsonl`. The micro scale.

## Python primitives (Layer 3, v3.0)

`pip install -e python/` exposes `quantumagent` as a Python package:

```python
from quantumagent import psi, entangle, observe, measure, constraint
```

- `psi(states, weights=…)` — declare a wavefunction in classical mode (real probabilities)
- `psi(states, amplitudes=…)` — *(v3.1)* declare a wavefunction in quantum mode (complex amplitudes)
- `observe(psi)` — non-destructive read of the distribution (works for both modes)
- `measure(psi, seed)` — Born-rule sampling, collapses + propagates to entangled
- `entangle(a, b, correlation)` — link two wavefunctions (classical-style soft entanglement)
- `constraint(name, boost=…, suppress=…, where=…)` — operator applied via `@` (classical mode only)
- *(v3.1)* `superpose(a, b)` — quantum superposition; amplitudes add → interference
- *(v3.1)* `bell_state(kind)` — construct a maximally-entangled 2-qubit Bell state
- *(v3.2)* `gate(name, *params)` + `apply_gate(psi, gate, qubits=…)` — quantum gates (I, X, Y, Z, H, S, T, CNOT, CZ, SWAP, Rx, Ry, Rz)
- *(v3.2)* `measure_in_basis(psi, θ_a, θ_b)` + `chsh_test(psi, n_trials)` — CHSH Bell-inequality test
- *(v3.2)* `density(psi)`, `decohere(rho, rate)`, `partial_trace(rho, qubit)` — density matrix formalism + decoherence model

**Path B is complete (v3.2).** The Python layer now implements canonical
quantum mechanics end-to-end: complex amplitudes, true Born rule, interference,
maximally-entangled Bell states, multi-basis measurement with CHSH violation
(S ≈ 2.83), full quantum gate library with circuit composition, density
matrices with exponential decoherence model, partial trace = entanglement
signature. All verified empirically against theoretical predictions.

**v3.3 adds Layer 1↔Layer 3 interop**:
- `from_cosmos(repo_path)` — reads `.quantum/` cosmos output into a Python
  `CosmosRun` (Wavefunction + insights + heuristic resonance/uncertainty).
  First bridge between agent-backed (Layers 1-2) and math-backed (Layer 3).

See `python/README.md` for the full reference and nine runnable examples.
