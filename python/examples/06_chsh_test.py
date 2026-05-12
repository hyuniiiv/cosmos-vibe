"""Example 06 — CHSH inequality test (Path B Phase 2, v3.2+).

The decisive experiment that distinguishes quantum mechanics from any classical
local-realistic theory. Run on a Bell state, the CHSH parameter S violates the
classical bound |S| ≤ 2, reaching the Tsirelson bound 2√2 ≈ 2.828.

This is what makes quantum entanglement *provable*: no classical correlation
function — no matter how cleverly designed — can reproduce the statistics.
"""

import math
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from quantumagent import bell_state, chsh_test, psi


def main() -> None:
    print("━" * 70)
    print("  CHSH Bell-inequality test")
    print("━" * 70)
    print()
    print("  Classical theories obey: |S| ≤ 2  (Bell's bound)")
    print("  Quantum mechanics:        |S| ≤ 2√2 ≈ 2.828  (Tsirelson's bound)")
    print()
    print("  Measuring a Bell state in 4 angle combinations:")
    print("    a  = 0,    a' = π/2")
    print("    b  = π/4,  b' = 3π/4")
    print()

    for kind in ["phi+", "phi-", "psi+", "psi-"]:
        bell = bell_state(kind)
        S, breakdown = chsh_test(bell, n_trials=2000, seed_base=42 * 100)

        e_ab = breakdown['E(a,b)']
        e_abp = breakdown["E(a,b')"]
        e_apb = breakdown["E(a',b)"]
        e_apbp = breakdown["E(a',b')"]
        print(f"  ── Bell state |{kind}⟩ ──")
        print(f"     E(a,b)   = {e_ab:+.4f}")
        print(f"     E(a,b')  = {e_abp:+.4f}")
        print(f"     E(a',b)  = {e_apb:+.4f}")
        print(f"     E(a',b') = {e_apbp:+.4f}")
        print(f"     S        = {S:+.4f}    "
              f"({'VIOLATES' if abs(S) > 2 else 'within'} classical bound |S| ≤ 2)")
        excess = (abs(S) - 2.0) / (2 * math.sqrt(2) - 2.0)
        print(f"     Reaches  {100 * excess:.1f}% of the quantum maximum (2√2)")
        print()

    print("━" * 70)
    print("  Why this matters")
    print("━" * 70)
    print()
    print("  Bell (1964) proved no classical local-realistic theory can produce")
    print("  |S| > 2. Aspect (1982) experimentally verified |S| > 2 with photons.")
    print("  Nobel Prize 2022.")
    print()
    print("  Above we just reproduced that violation in code. The Bell states")
    print("  are NOT classically simulable correlation functions — they require")
    print("  the full complex-amplitude quantum machinery.")
    print()
    print("  Compare to a classical analog: ψ with weights= instead of amplitudes=")
    print("  would never violate |S| ≤ 2 no matter how clever the correlation.")


if __name__ == "__main__":
    main()
