"""Example 01 — basic ψ usage.

Run from python/ directory:
    python -m examples.01_basic_psi
Or directly:
    python python/examples/01_basic_psi.py

Demonstrates: declaring a wavefunction, observing without collapse,
measuring with a deterministic seed.
"""

import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from quantumagent import psi, observe, measure


def main() -> None:
    # Declare a decision in superposition.
    # Three caching strategies, with prior probabilities.
    cache = psi(
        states=["redis-ttl", "cdn-edge", "in-memory-lru"],
        weights=[0.5, 0.3, 0.2],
        name="cache-strategy",
    )

    print(f"Initial wavefunction: {cache}")
    print(f"  is_collapsed: {cache.is_collapsed}")

    # Observe is non-destructive — call as many times as you want.
    print(f"\nobserve() → {observe(cache)}")
    print(f"observe() → {observe(cache)}")
    print(f"observe() → {observe(cache)}")
    print(f"  (superposition still intact: {cache.is_collapsed=})")

    # Measure collapses to one state. Use seed for deterministic test runs.
    chosen = measure(cache, seed=42)
    print(f"\nmeasure(seed=42) → {chosen!r}")
    print(f"  cache now collapsed: {cache}")
    print(f"  is_collapsed: {cache.is_collapsed}")

    # Measuring again returns the same state — no re-sampling.
    again = measure(cache, seed=999)
    print(f"\nmeasure() again → {again!r} (same as before — collapsed state preserved)")

    # observe() on a collapsed wavefunction shows the certainty.
    print(f"\nobserve() after collapse → {observe(cache)}")


if __name__ == "__main__":
    main()
