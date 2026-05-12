"""Example 08 — density matrices, decoherence, and partial trace (Path B Phase 4, v3.2+).

Demonstrates the density-matrix formalism and the two phenomena it exposes:

1. **Decoherence**: a pure superposition coupled to an environment becomes a
   classical mixture as off-diagonal coherences decay exponentially.

2. **Partial trace = entanglement signature**: tracing out one qubit of a Bell
   state yields the maximally mixed state I/2 on the other qubit. This is
   the strongest possible signature of entanglement — purely classical
   correlations cannot produce this.
"""

import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from quantumagent import bell_state, psi, density, decohere, partial_trace


def main() -> None:
    print("━" * 70)
    print("  PURE STATE → DENSITY MATRIX")
    print("━" * 70)
    print()
    print("  ρ = |ψ⟩⟨ψ|.  For pure states: Tr(ρ²) = 1.")
    print()

    bell = bell_state("phi+")
    rho = density(bell)
    print(rho)
    print()
    print(f"  Trace(ρ)   = {rho.trace().real:.4f}     (should be 1)")
    print(f"  Purity(ρ)  = {rho.purity():.4f}     (1 = pure, < 1 = mixed)")
    print(f"  is_pure    = {rho.is_pure}")
    print()
    print("  Note the off-diagonal blocks at (0,0)↔(1,1) — those are the")
    print("  coherences. They encode the quantum superposition.")

    print()
    print("━" * 70)
    print("  DECOHERENCE — coupling to the environment")
    print("━" * 70)
    print()
    print("  As the system interacts with its surroundings, phase information")
    print("  leaks into the environment. Off-diagonal density-matrix elements")
    print("  decay exponentially. The diagonal (classical probabilities)")
    print("  is preserved — it becomes a classical mixture, not nothing.")
    print()

    for rate, label in [(0.0, "rate=0 (no decoherence)"),
                        (0.5, "rate=0.5 (mild)"),
                        (1.0, "rate=1.0 (moderate)"),
                        (2.0, "rate=2.0 (strong)"),
                        (10.0, "rate=10.0 (essentially classical)")]:
        rho_d = decohere(rho, rate=rate)
        # Off-diagonal magnitude (proxy for remaining coherence)
        off_diag = abs(rho_d.matrix[0][3])
        purity = rho_d.purity()
        bar = "█" * int(40 * off_diag * 2)  # max ~0.5 for Bell state
        print(f"  {label:38} → off-diagonal |ρ[00][11]| = {off_diag:.4f}  "
              f"purity = {purity:.4f}  {bar}")

    print()
    print("  At high rate, purity → 0.5 — the diagonal mixed state.")
    print("  The Bell correlation 'both 0 or both 1' is preserved classically,")
    print("  but the quantum phase coherence is gone. Decoherence is the")
    print("  bridge from quantum mechanics to the classical world.")

    print()
    print("━" * 70)
    print("  PARTIAL TRACE — the entanglement signature")
    print("━" * 70)
    print()
    print("  For ANY pure entangled state, tracing out a subsystem gives a")
    print("  MIXED reduced state on the remainder. For a maximally-entangled")
    print("  Bell state, the result is I/2 — maximally mixed.")
    print()

    reduced_a = partial_trace(rho, qubit=0)
    print("  Tr_0(ρ_Bell) (qubit 0 traced out, qubit 1 reduced):")
    print(reduced_a)
    print()
    print(f"    Purity = {reduced_a.purity():.4f}")
    print("    Diagonal: 0.5 + 0.5 (maximally mixed)")
    print("    Off-diagonal: 0 (zero coherence)")
    print()

    if abs(reduced_a.purity() - 0.5) < 1e-9:
        print("  ✓ purity = 0.5 — maximally mixed reduced state confirms ENTANGLEMENT")
        print()
        print("    Each qubit alone has no quantum information.")
        print("    Yet the pair is pure (purity 1.0).")
        print("    This is impossible for any classical correlation —")
        print("    only entangled quantum states have this property.")

    print()
    print("━" * 70)
    print("  Contrast: a SEPARABLE 2-qubit state (no entanglement)")
    print("━" * 70)
    print()

    # |0⟩ ⊗ |+⟩ = (|00⟩ + |01⟩) / √2 — separable
    separable = psi(
        states=[("0", "0"), ("0", "1"), ("1", "0"), ("1", "1")],
        amplitudes=[1, 1, 0, 0],
        name="|0⟩⊗|+⟩",
    )
    rho_sep = density(separable)
    print(f"  Original purity (separable state): {rho_sep.purity():.4f}")
    reduced_sep = partial_trace(rho_sep, qubit=0)
    print(f"  Reduced purity (after tracing q0):  {reduced_sep.purity():.4f}")
    print()
    if abs(reduced_sep.purity() - 1.0) < 1e-9:
        print("  ✓ For a SEPARABLE state, the reduced state stays pure.")
        print("    Partial trace distinguishes entanglement from mere correlation.")


if __name__ == "__main__":
    main()
