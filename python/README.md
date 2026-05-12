# QuantumAgent — Python primitives (Layer 3)

> Quantum-inspired decision primitives for Python — `ψ`, `entangle`, `observe`, `measure`, `constraint`.

The **programmable layer** of QuantumAgent. While Layer 1 (CLI) and Layer 2 (YAML DSL) orchestrate AI agents through Claude Code skills, Layer 3 exposes the underlying quantum-style decision primitives that can be composed directly in Python code.

```python
from quantumagent import psi, entangle, observe, measure, constraint

cache = psi(["redis-ttl", "cdn-edge", "in-memory-lru"], weights=[0.5, 0.3, 0.2])
storage = psi(["postgres", "redis", "memory"])

entangle(cache, storage, lambda c, s:
    (c == "redis-ttl"      and s == "redis") or
    (c == "cdn-edge"       and s == "postgres") or
    (c == "in-memory-lru"  and s == "memory")
)

cache = constraint("low-latency-pref", boost={"redis-ttl": 2.0}) @ cache

print(observe(cache))           # {'redis-ttl': 0.667, 'cdn-edge': 0.200, ...}
chosen_cache = measure(cache)   # collapses → 'redis-ttl' (probably)
chosen_store = measure(storage) # conditioned on entanglement → 'redis'
```

---

## Install

```bash
# From the quantum-agent repo:
pip install -e python/

# Or once published to PyPI:
pip install quantumagent
```

Python 3.9+ required. No runtime dependencies for the core (numpy/scipy not used).

---

## The five primitives

### `psi(states, weights=None, name=None)` — declare a wavefunction

Create a decision in superposition. The wavefunction holds a probability distribution over discrete states. Weights are auto-normalized; default is uniform.

```python
cache = psi(["redis", "cdn", "lru"])                    # uniform prior
cache = psi(["redis", "cdn", "lru"], [0.6, 0.3, 0.1])   # weighted prior
cache = psi(["redis", "cdn", "lru"], name="cache-strategy")
```

Alias: `ψ` (Greek psi) is exported and identical to `psi`.

### `observe(psi)` — non-destructive read

Returns `{state: probability}`. Does NOT collapse the wavefunction. Call as many times as you want.

```python
print(observe(cache))   # {'redis': 0.5, 'cdn': 0.3, 'lru': 0.2}
print(observe(cache))   # same — superposition intact
```

This is the **first-class distinction** that other frameworks miss: observation that doesn't force a decision.

### `measure(psi, seed=None)` — collapse to a single state

Samples one state per the current distribution (Born-rule analog), collapses the wavefunction, and propagates to entangled partners. Subsequent `measure` calls return the same state — no re-sampling.

```python
chosen = measure(cache)             # random sample
chosen = measure(cache, seed=42)    # deterministic (useful in tests)
```

### `entangle(a, b, correlation)` — link two decisions

Register a compatibility function between two wavefunctions. When one is measured, the other's distribution is conditioned on the result.

```python
auth = psi(["jwt", "session", "oauth"])
store = psi(["redis", "postgres", "memory"])

entangle(auth, store, lambda a, s:
    (a == "jwt"     and s in ("redis", "memory")) or
    (a == "session" and s == "redis")             or
    (a == "oauth"   and s in ("redis", "postgres"))
)

measure(auth, seed=7)        # → 'session' (for example)
print(observe(store))        # → {'redis': 1.0, 'postgres': 0.0, 'memory': 0.0}
# session requires redis — entanglement collapsed the alternatives.
```

If a measurement leaves no compatible state in the partner, `measure` raises `ValueError` — explicit failure rather than silent corruption.

### `constraint(name, *, boost=None, suppress=None, where=None)` — operators

Constraints are immutable operators applied via `op @ psi`, returning a NEW wavefunction. They curve the distribution — the General Relativity analog where mass curves spacetime.

Three patterns (composable):

```python
# where: keep only matching states (filter)
sql_only = constraint("sql-required", where=lambda s: s in {"postgres", "mysql"})

# boost: multiply specific weights
prefer_pg = constraint("postgres-preferred", boost={"postgres": 3.0})

# suppress: divide specific weights
penalty = constraint("avoid-postgres", suppress={"postgres": 2.0})

db = sql_only @ db        # filter
db = prefer_pg @ db       # then boost
db = penalty @ db         # then suppress
```

If a constraint zeros out all states, it raises `ValueError`.

---

## The philosophy

### Why "observe" vs "measure" matters

In most frameworks, "reading a value" forces a decision — you can't peek at a probabilistic state without collapsing it. Even probabilistic programming (Pyro, Stan) treats sampling as the primary operation.

QuantumAgent makes the distinction first-class:

| | `observe` | `measure` |
|---|-----------|-----------|
| **Reads distribution?** | Yes | Yes |
| **Collapses state?** | No | Yes |
| **Propagates to entangled?** | No | Yes |
| **Idempotent?** | Yes | Yes (after first call) |

This matters when LLM agents are expensive: you want to look at the state, *think about* what to do, and then decide — without paying the cost of every intermediate "check" forcing a fresh decision.

### Two modes — classical and quantum *(quantum: Path B, v3.1+)*

The library auto-detects which mode you want from the constructor arguments to `psi()`:

| Mode | Constructor | Math |
|------|------------|------|
| **Classical** *(default)* | `psi(states, weights=[...])` or `psi(states)` | Real probability weights, normalized so Σ = 1 |
| **Quantum** *(v3.1+)* | `psi(states, amplitudes=[...])` | Complex amplitudes, normalized so Σ\|c\|² = 1 |

In quantum mode:
- **True Born rule**: `P(i) = |amplitude_i|²`
- **Phase is preserved** — amplitudes have direction in the complex plane
- **Interference is real** — combining wavefunctions via `superpose()` adds amplitudes (not probabilities), producing constructive or destructive patterns
- **Entanglement via `bell_state()`** — maximally-entangled 2-qubit states for genuine quantum correlations

```python
from quantumagent import psi, superpose, bell_state, observe, measure

# Two equal sources, OPPOSITE phase — classical impossible
slit_a = psi(["screen-A", "screen-B"], amplitudes=[1,  1])   # |+⟩
slit_b = psi(["screen-A", "screen-B"], amplitudes=[1, -1])   # |-⟩
mixed = superpose(slit_a, slit_b)
print(observe(mixed))    # → {'screen-A': 1.0, 'screen-B': 0.0}
                         # DESTRUCTIVE INTERFERENCE — classical theory cannot
                         # produce 100/0 from two 50/50 sources.

# Bell state — maximally entangled
bell = bell_state("phi+")          # (|00⟩ + |11⟩) / √2
outcomes = [measure(bell_state("phi+"), seed=i) for i in range(1000)]
# Every outcome is ('0','0') or ('1','1'). Never mixed.
# Each qubit alone is 50/50; the PAIR is 100% correlated.
```

Run `examples/04_quantum_interference.py` and `examples/05_bell_state.py` to see this in action.

### Quantum mode capabilities (v3.2 — Path B complete)

All four Path B phases shipped:

| Phase | Capability | Primitives |
|-------|-----------|------------|
| **Phase 1** *(v3.1)* | Complex amplitudes + interference | `psi(amplitudes=…)`, `superpose`, `bell_state` |
| **Phase 2** *(v3.2)* | CHSH Bell test, multi-basis measurement | `measure_in_basis`, `chsh_test` |
| **Phase 3** *(v3.2)* | Quantum gates + circuit composition | `gate`, `apply_gate`, `Gate.__matmul__` |
| **Phase 4** *(v3.2)* | Density matrices + decoherence | `density`, `decohere`, `partial_trace`, `DensityMatrix` |

The library now implements the full canonical quantum-mechanics machinery — verified empirically in `examples/06_chsh_test.py` through `08_decoherence.py`:

- **CHSH violation**: Bell state achieves S ≈ 2.83 (Tsirelson bound), violating the classical |S| ≤ 2 bound. No classical local-realistic theory can produce this.
- **Circuit composition**: |00⟩ → H₀ → CNOT(0→1) reproduces the Bell state exactly, matching the hardcoded `bell_state("phi+")`. Inverse circuit recovers |00⟩.
- **Entanglement signature**: Partial trace of the Bell state gives I/2 (maximally mixed, purity = 0.5). Separable states keep their reduced purity at 1.0.

### Classical-mode operations still apply

`constraint(...) @ psi` raises `NotImplementedError` for quantum-mode wavefunctions because the API maps to weight adjustment (not Hermitian operators on amplitudes). To constrain a quantum state, use gates — they're the proper Hermitian-operator equivalent.

Classical mode remains the default and is unchanged from v3.0. Quantum mode is opt-in via `amplitudes=`.

---

## Examples

Nine runnable examples in `examples/`:

**Classical mode (v3.0):**
- **`01_basic_psi.py`** — declare, observe, measure with seed
- **`02_entanglement.py`** — auth × storage compatibility, entanglement propagation
- **`03_constraint_curvature.py`** — composing filter / boost / suppress constraints

**Quantum mode — Phase 1 (v3.1):**
- **`04_quantum_interference.py`** — destructive interference: two 50/50 sources produce 100/0 outcome (impossible classically)
- **`05_bell_state.py`** — maximally-entangled 2-qubit Bell states with perfect correlation

**Quantum mode — Phases 2-4 (v3.2):**
- **`06_chsh_test.py`** — CHSH Bell-inequality test: |Φ+⟩ achieves S ≈ 2.83, violating the classical |S| ≤ 2 bound (genuine quantum entanglement)
- **`07_quantum_gates.py`** — build a Bell state from gates: |00⟩ → H₀ → CNOT → |Φ+⟩, plus parametric Ry rotations and inverse circuits
- **`08_decoherence.py`** — pure→mixed via exponential decay of off-diagonals, plus partial trace = I/2 (entanglement signature)

**Layer interop (v3.3):**
- **`09_cosmos_interop.py`** — read a cosmos run's `.quantum/` output into a Python `CosmosRun` and compose with quantum primitives

Run them:

```bash
cd python/
pip install -e .
for f in examples/*.py; do python "$f"; done
```

Each example prints its execution so you can read what happened.

---

## Relationship to the CLI/DSL layers

```
Layer 1 (v1.x) — CLI                 Layer 2 (v2.0) — YAML DSL          Layer 3 (v3.0) — Python
────────────────────────             ─────────────────────────          ────────────────────────
/cosmos spawn --goal "..."           experiment: rate-limiting          cache = psi(...)
/cosmos observe                      spawn:                             entangle(cache, store, ...)
/cosmos crystallize alpha              goal: "..."                      constraint("...") @ cache
                                       strategies: [...]                measure(cache)
                                     /cosmos run experiment.qa.yaml

Backed by: LLM agents in worktrees   Backed by: same agents via YAML    Backed by: pure math
                                                                        (LLM integration: future)
```

Layer 3 is **mathematically standalone** in this MVP — no LLM calls, no `.quantum/` files, no external infrastructure. Pure Python primitives that obey the same conceptual model as the CLI/DSL layers but execute in-process.

A future release will add an `agent` backend that uses Layer 3 to *orchestrate* Layer 1/2 — letting you express agentic experiments in Python and have ψ/entangle/measure invoke real cosmos runs. For now, Layer 3 is the simulation/decision-modeling counterpart.

---

## When to use Python primitives vs CLI/DSL

| Use Python primitives when | Use CLI/DSL when |
|---------------------------|-------------------|
| Modeling decisions without code execution | You want real working code in N branches |
| What-if analysis / quick exploration | Production-grade exploration |
| Building tools that compose decisions | Agentic exploration is the goal |
| Probabilistic reasoning is the output | Implementations are the output |
| Tests / dry-runs of constraint algebra | Real LLM-backed work |

---

## Roadmap

Implemented (v3.0):
- ✓ Probability-distribution-based ψ
- ✓ Entanglement with conditional propagation
- ✓ Constraint operators (boost / suppress / where)
- ✓ Born-rule-flavored measure + non-destructive observe
- ✓ Pure-Python, zero runtime dependencies

Implemented (v3.1, Path B Phase 1):
- ✓ Complex amplitudes via `psi(states, amplitudes=…)`
- ✓ True Born rule `P(i) = |c|²`
- ✓ `superpose(a, b)` — amplitudes add → real interference (constructive/destructive)
- ✓ `bell_state(kind)` — four maximally-entangled 2-qubit states

Implemented (v3.2, Path B Phases 2-4 — **complete**):
- ✓ CHSH Bell-inequality test (`chsh_test`) — verified S ≈ 2.83 for Bell states
- ✓ Multi-basis measurement (`measure_in_basis`) — rotate then measure in Z
- ✓ Standard gate library: I, X, Y, Z, H, S, T, CNOT/CX, CZ, SWAP, Rx(θ), Ry(θ), Rz(θ)
- ✓ Gate composition via `gate @ gate` and `apply_gate(psi, gate, qubits=…)` for arbitrary n-qubit systems
- ✓ Density matrices (`density`, `DensityMatrix`) — pure ↔ mixed states
- ✓ Exponential decoherence model (`decohere`) — off-diagonals decay
- ✓ Partial trace (`partial_trace`) — entanglement signature via reduced purity

Implemented (v3.3, vision-gap fills):
- ✓ **`from_cosmos(repo_path)`** — Layer 1 ↔ Layer 3 bridge. Reads `.quantum/`
  cosmos output into a `CosmosRun` (Wavefunction + insights + heuristic
  resonance/uncertainty + macro context).
- ✓ Heuristic resonance/uncertainty via token overlap (cheap signal — for
  semantic quality use `/cosmos observe`)

**Path B is complete.** v3.3 fills the largest remaining vision gaps
(model diversity in CLI/DSL, .quantum/ interop). The micro-scale layer
remains the one untaken vision branch — see below.

Roadmap:
- **v4.0 (planned) — Micro-scale (code) layer** — `.quantum/code/<symbol>/`
  with static-analysis integration. Function-level quantum state tracking,
  automatic `[TUNNEL]` detection for type-system bypasses (`as unknown as`,
  `@ts-ignore`, etc.), code-level decoherence (untested code = lost
  coherence). This is the third scale of the original vision; major work,
  separate track from the Python lib.
- **Agent backend** — `ψ.spawn(use_agent=True)` to invoke real LLMs from
  Python. Requires optional `anthropic` SDK dependency. Future v3.x release.
- **Visualization** — render wavefunctions / entanglement graphs.

---

## License

MIT. See repo root `LICENSE`.
