"""Example 05 — Bell state correlations (Path B, v3.1+).

Demonstrates: maximally-entangled 2-qubit states. The four Bell states each
exhibit perfect correlation (or anti-correlation) that no classical correlation
function can reproduce — and the Wavefunction over tuple states captures it.

We use ``bell_state("phi+")`` = (|00⟩ + |11⟩) / √2. Every measurement returns
either ('0','0') or ('1','1') with equal probability — never ('0','1') or
('1','0'). The two qubits are perfectly correlated.

Then we run thousands of trials and confirm:
- Each individual outcome is 50/50 (each qubit alone looks random)
- The PAIR correlation is 100%
"""

import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from quantumagent import bell_state, observe, measure


def main() -> None:
    print("━" * 70)
    print("  Bell state |Φ+⟩ = (|00⟩ + |11⟩) / √2")
    print("━" * 70)

    bell = bell_state("phi+")
    print(f"  {bell}")
    print(f"  observe → {observe(bell)}")
    print()
    print("  Half the amplitude on ('0','0'), half on ('1','1'); zero on")
    print("  the mixed states ('0','1') and ('1','0'). The two qubits are")
    print("  entangled — neither has a definite value, but they will agree.")
    print()

    print("━" * 70)
    print("  Run 2000 measurements — verify perfect correlation")
    print("━" * 70)

    n_trials = 2000
    outcomes = [measure(bell_state("phi+"), seed=i) for i in range(n_trials)]

    counts = {
        ("0", "0"): outcomes.count(("0", "0")),
        ("0", "1"): outcomes.count(("0", "1")),
        ("1", "0"): outcomes.count(("1", "0")),
        ("1", "1"): outcomes.count(("1", "1")),
    }

    print(f"  Trials: {n_trials}")
    for state, count in counts.items():
        bar = "█" * int(40 * count / n_trials)
        print(f"  {state!s:>12} : {count:5d}  {bar}")

    # Verify correlation
    correlated = counts[("0", "0")] + counts[("1", "1")]
    anti_correlated = counts[("0", "1")] + counts[("1", "0")]

    print()
    print(f"  Correlated outcomes (both 0, or both 1):     {correlated}/{n_trials} = {100*correlated/n_trials:.1f}%")
    print(f"  Anti-correlated outcomes (mixed):             {anti_correlated}/{n_trials} = {100*anti_correlated/n_trials:.1f}%")

    if anti_correlated == 0 and correlated == n_trials:
        print()
        print("  ✓ PERFECT correlation: 100% of measurements agree.")
        print("    No classical bit-pair distribution can produce this if")
        print("    each bit individually looks 50/50 (which they do — see below).")

    # Per-qubit marginals — each individually looks random
    print()
    qubit_a_zeros = sum(1 for o in outcomes if o[0] == "0")
    qubit_b_zeros = sum(1 for o in outcomes if o[1] == "0")
    print(f"  Qubit A alone — P(0): {100*qubit_a_zeros/n_trials:.1f}%   (expected 50%)")
    print(f"  Qubit B alone — P(0): {100*qubit_b_zeros/n_trials:.1f}%   (expected 50%)")
    print()
    print("  Each qubit looks like a fair coin. But the PAIR is perfectly")
    print("  correlated. This is the entanglement signature — invisible at")
    print("  the per-qubit level, undeniable at the joint level.")

    print()
    print("━" * 70)
    print("  The four Bell states")
    print("━" * 70)

    for kind in ["phi+", "phi-", "psi+", "psi-"]:
        b = bell_state(kind)
        dist = observe(b)
        # Show only non-zero outcomes
        nonzero = {s: p for s, p in dist.items() if p > 1e-9}
        print(f"  |{kind}⟩  →  {nonzero}")

    print()
    print("  |Φ⁺⟩ and |Φ⁻⟩: correlated  (both 0 or both 1)")
    print("  |Ψ⁺⟩ and |Ψ⁻⟩: anti-correlated  (always different)")
    print()
    print("  The minus-sign states (Φ⁻, Ψ⁻) look identical to the plus-sign")
    print("  states when measured in the computational basis — the phase")
    print("  difference only shows up in other bases. (CHSH/Bell inequality")
    print("  test that distinguishes them: reserved for v3.2.)")


if __name__ == "__main__":
    main()
