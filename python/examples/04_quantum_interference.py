"""Example 04 — quantum interference (Path B, v3.1+).

Demonstrates: the defining quantum signature. Where classical probabilities
just add up to 50/50 from two equal sources, quantum amplitudes can interfere
constructively (1.0) or destructively (0.0) depending on phase.

This is impossible in classical probability theory. It's the double-slit
experiment in code.
"""

import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from quantumagent import psi, superpose, observe, measure


def main() -> None:
    print("━" * 70)
    print("  CLASSICAL view: two equal sources give 50/50 — no interference")
    print("━" * 70)

    classical_a = psi(["screen-A", "screen-B"], weights=[0.5, 0.5], name="slit-a")
    classical_b = psi(["screen-A", "screen-B"], weights=[0.5, 0.5], name="slit-b")

    # Classical combination: probabilities add. With two equal sources,
    # outcome is uniform.
    combined_classical = {
        s: 0.5 * pa + 0.5 * pb
        for (s, pa), pb in zip(observe(classical_a).items(), observe(classical_b).values())
    }
    print(f"  Slit A: {observe(classical_a)}")
    print(f"  Slit B: {observe(classical_b)}")
    print(f"  Mixed (classical avg): {combined_classical}")
    print("  → Both screens hit ~50%. No pattern.")

    print()
    print("━" * 70)
    print("  QUANTUM view: same probabilities, but amplitudes have phase")
    print("━" * 70)

    # |+⟩ on the screen basis — same amplitudes, same phase
    slit_a = psi(["screen-A", "screen-B"], amplitudes=[1, 1], name="slit-a")
    # |-⟩ on the screen basis — same amplitudes, OPPOSITE phase on B
    slit_b = psi(["screen-A", "screen-B"], amplitudes=[1, -1], name="slit-b")

    print(f"  Slit A: {slit_a}")
    print(f"  Slit B: {slit_b}")
    print(f"  Both individually look 50/50: A={observe(slit_a)}, B={observe(slit_b)}")

    print()
    print("  ────  CONSTRUCTIVE interference (in-phase superposition)  ────")
    constructive = superpose(slit_a, slit_a, name="A+A")
    print(f"    superpose(A, A) → {constructive}")
    print(f"    → {observe(constructive)}")
    print("    ✓ Same as A alone (renormalized amplification, identical distribution)")

    print()
    print("  ────  DESTRUCTIVE interference (out-of-phase superposition)  ────")
    interfered = superpose(slit_a, slit_b, name="A+B")
    print(f"    superpose(A, B) → {interfered}")
    print(f"    → {observe(interfered)}")
    obs = observe(interfered)
    a_prob = obs.get("screen-A", 0)
    b_prob = obs.get("screen-B", 0)
    print()
    print(f"    P(screen-A) = {a_prob:.3f}")
    print(f"    P(screen-B) = {b_prob:.3f}")
    print()

    if abs(b_prob) < 1e-9 and a_prob > 0.99:
        print("    ✓ DESTRUCTIVE interference confirmed:")
        print("        screen-B amplitudes cancelled exactly")
        print("        all probability concentrated on screen-A")
        print()
        print("    Classical impossible: two equal 50/50 sources cannot")
        print("    produce a 100/0 outcome. Phase matters. Quantum is real.")
    else:
        print("    (unexpected — check the math)")

    print()
    print("━" * 70)
    print("  Born rule sampling — the quantum die")
    print("━" * 70)

    # Sample many times to confirm Born rule
    samples = []
    for i in range(1000):
        ψ_fresh = superpose(
            psi(["screen-A", "screen-B"], amplitudes=[1, 1]),
            psi(["screen-A", "screen-B"], amplitudes=[1, -1]),
        )
        samples.append(measure(ψ_fresh, seed=i))

    a_count = samples.count("screen-A")
    b_count = samples.count("screen-B")
    print(f"  1000 trials of measure(superpose(A, B)):")
    print(f"    screen-A: {a_count} hits")
    print(f"    screen-B: {b_count} hits")
    print(f"  Expected from theory: 1000 and 0 (perfect destructive interference)")


if __name__ == "__main__":
    main()
