"""QuantumAgent — quantum-inspired decision primitives for Python.

The programmable layer (Layer 3) of QuantumAgent. While Layer 1 (CLI) and
Layer 2 (YAML DSL) orchestrate AI agents, Layer 3 exposes quantum-inspired
primitives that can be composed directly in code.

Core primitives:
    psi (ψ)     — declare a decision as a probability distribution over states
    entangle    — link two decisions so measurement of one informs the other
    observe     — non-destructive read of the distribution
    measure     — collapse to a single state via Born-rule sampling
    constraint  — operator that curves the distribution (constraint curvature)

Example::

    from quantumagent import psi, entangle, observe, measure, constraint

    cache = psi(["redis-ttl", "cdn-edge", "in-memory-lru"], weights=[0.4, 0.4, 0.2])
    storage = psi(["postgres", "dynamo", "sqlite"])
    entangle(cache, storage, lambda c, s: not (c == "in-memory-lru" and s != "sqlite"))

    cache = constraint("low-latency", boost={"redis-ttl": 1.5, "in-memory-lru": 2.0}) @ cache

    snapshot = observe(cache)              # non-destructive
    final = measure(cache, seed=42)        # collapse (deterministic with seed)

See `python/README.md` for the full guide and examples.
"""

from .core import (
    Wavefunction,
    psi,
    entangle,
    observe,
    measure,
    constraint,
    Constraint,
    Operator,
    superpose,
    bell_state,
)
from .quantum import (
    Gate,
    gate,
    apply_gate,
    measure_in_basis,
    chsh_test,
    DensityMatrix,
    density,
    decohere,
    partial_trace,
)

# Greek alias for fans of the notation
ψ = psi  # noqa: PLC2401 - intentional non-ASCII alias

__all__ = [
    "Wavefunction",
    "psi",
    "ψ",
    "entangle",
    "observe",
    "measure",
    "constraint",
    "Constraint",
    "Operator",
    # Path B Phase 1 (quantum mode, v3.1)
    "superpose",
    "bell_state",
    # Path B Phase 2 — CHSH (v3.2)
    "measure_in_basis",
    "chsh_test",
    # Path B Phase 3 — quantum gates (v3.2)
    "Gate",
    "gate",
    "apply_gate",
    # Path B Phase 4 — density matrices & decoherence (v3.2)
    "DensityMatrix",
    "density",
    "decohere",
    "partial_trace",
]

__version__ = "3.2.0"
