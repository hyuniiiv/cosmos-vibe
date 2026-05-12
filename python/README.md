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

### Why probability distributions (not complex amplitudes) — for now

This MVP uses real-valued probability weights. Measurement is Born-rule-flavored: sample proportional to weight. Constraints adjust weights additively/multiplicatively.

**True quantum amplitudes** (complex numbers with phase, capable of interference) are reserved for **Path B** — a future release. The API is designed to be forward-compatible: `psi(states, weights)` will become `psi(states, amplitudes, quantum=True)` when Path B lands, and existing code will continue to work in classical-probability mode.

Why defer? Complex amplitudes require:
- A Hilbert space implementation (not just a probability simplex)
- Hermitian operators for constraints (linear algebra)
- True interference patterns between entangled wavefunctions
- Bell-test demonstrations to prove the quantum behavior

That's a substantial separate effort. The classical-probability MVP delivers most of the value (observe/measure distinction, entanglement, constraint curvature) and is shipping today.

---

## Examples

Three runnable examples in `examples/`:

- **`01_basic_psi.py`** — declare, observe, measure with seed
- **`02_entanglement.py`** — auth × storage compatibility, entanglement propagation
- **`03_constraint_curvature.py`** — composing filter / boost / suppress constraints

Run them:

```bash
cd python/
pip install -e .
python examples/01_basic_psi.py
python examples/02_entanglement.py
python examples/03_constraint_curvature.py
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

Roadmap:
- **Agent backend** — `ψ.spawn()` to invoke real cosmos via Claude Code
- **Quantum mode** — complex amplitudes with phase, true interference, Bell-test demonstrations (Path B)
- **`.quantum/` interop** — read existing cosmos insights as a Python wavefunction
- **Visualization** — render a wavefunction / entanglement graph as ASCII or HTML

---

## License

MIT. See repo root `LICENSE`.
