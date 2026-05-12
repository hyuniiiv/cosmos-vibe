"""Example 07 — quantum gates and circuit composition (Path B Phase 3, v3.2+).

Demonstrates: building a Bell state FROM SCRATCH using quantum gates instead
of a hardcoded amplitude vector. This is the canonical "quantum circuit":

  |00⟩ ─ H on q0 ─ CNOT(q0 → q1) ─ → |Φ+⟩ = (|00⟩ + |11⟩) / √2

Also shows: gate composition, parametric rotations, and the inverse direction
(starting from |Φ+⟩ and undoing the circuit back to |00⟩).
"""

import math
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from quantumagent import psi, gate, apply_gate, observe, measure, bell_state


def main() -> None:
    print("━" * 70)
    print("  Build a Bell state from gates")
    print("━" * 70)
    print()
    print("  Circuit:  |00⟩ ─ H₀ ─ CNOT(0→1) ─ |Φ+⟩")
    print()

    # Start with |00⟩
    psi00 = psi(
        states=[("0", "0"), ("0", "1"), ("1", "0"), ("1", "1")],
        amplitudes=[1, 0, 0, 0],
        name="|00⟩",
    )
    print(f"  Start:        {psi00}")
    print(f"                {observe(psi00)}")
    print()

    # Apply Hadamard to qubit 0 → (|00⟩ + |10⟩) / √2
    after_h = apply_gate(psi00, gate("H"), qubits=[0])
    print(f"  After H on q0: {after_h}")
    print(f"                 {observe(after_h)}")
    print("  (qubit 0 is now in superposition; qubit 1 still |0⟩)")
    print()

    # Apply CNOT(control=0, target=1) → (|00⟩ + |11⟩) / √2 = Bell |Φ+⟩
    after_cnot = apply_gate(after_h, gate("CNOT"), qubits=[0, 1])
    print(f"  After CNOT:    {after_cnot}")
    print(f"                 {observe(after_cnot)}")
    print()

    # Compare to the hardcoded Bell state
    bell = bell_state("phi+")
    print(f"  bell_state('phi+'): {bell}")
    print(f"                      {observe(bell)}")
    print()

    constructed = observe(after_cnot)
    target = observe(bell)
    all_match = all(
        abs(constructed.get(s, 0) - target.get(s, 0)) < 1e-9 for s in target
    )
    if all_match:
        print("  ✓ Circuit-constructed state matches bell_state('phi+') exactly")
    else:
        print("  ✗ MISMATCH (unexpected)")
    print()

    print("━" * 70)
    print("  Run the circuit in reverse — Bell state → |00⟩")
    print("━" * 70)
    print()
    print("  CNOT and H are self-inverse (CNOT·CNOT = I, H·H = I).")
    print("  So applying them in REVERSE order should disentangle the Bell state.")
    print()

    reversed_state = apply_gate(bell, gate("CNOT"), qubits=[0, 1])
    reversed_state = apply_gate(reversed_state, gate("H"), qubits=[0])
    print(f"  Inverse circuit: {observe(reversed_state)}")
    almost_pure_00 = observe(reversed_state).get(("0", "0"), 0)
    print(f"  P('00') = {almost_pure_00:.6f}  (expected 1.0)")
    if abs(almost_pure_00 - 1.0) < 1e-9:
        print("  ✓ Inversion confirmed — gates are unitary, no information lost")

    print()
    print("━" * 70)
    print("  Parametric rotation gates")
    print("━" * 70)
    print()
    print("  Rotate |0⟩ around the Y axis by θ: result depends continuously on θ.")
    print("  At θ = 0:      |0⟩")
    print("  At θ = π/2:    (|0⟩ + |1⟩) / √2 = |+⟩")
    print("  At θ = π:      |1⟩")
    print()

    qbit = psi(states=[("0",), ("1",)], amplitudes=[1, 0], name="|0⟩")
    for theta_name, theta in [
        ("0", 0.0),
        ("π/4", math.pi / 4),
        ("π/2", math.pi / 2),
        ("3π/4", 3 * math.pi / 4),
        ("π", math.pi),
    ]:
        rotated = apply_gate(qbit, gate("Ry", theta), qubits=[0])
        obs = observe(rotated)
        p0 = obs.get(("0",), 0)
        p1 = obs.get(("1",), 0)
        bar = "█" * int(40 * p1)
        print(f"  Ry(θ={theta_name:5})  → P(|0⟩) = {p0:.3f},  P(|1⟩) = {p1:.3f}  {bar}")

    print()
    print("  Smooth, continuous, unitary. Quantum rotations are first-class.")


if __name__ == "__main__":
    main()
