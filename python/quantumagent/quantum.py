"""Path B Phases 2-4 — quantum gates, CHSH test, density matrices.

This module completes the quantum-mechanics implementation in QuantumAgent:

- **Phase 2** — Pauli observables, rotation operators, multi-basis measurement,
  CHSH inequality test (Bell-violation demonstration).
- **Phase 3** — Standard quantum gate library (Pauli, Hadamard, phase, CNOT, ...)
  with composition and ``apply_gate`` for n-qubit systems.
- **Phase 4** — Density matrices, decoherence model, partial trace
  (the entanglement signature).

All implementations are pure-Python complex arithmetic — no external deps.
For multi-qubit systems, states are tuples of ``"0"``/``"1"`` strings in
*qubit-0-leftmost* convention (qubit 0 is the high bit).
"""

from __future__ import annotations

import cmath
import math
import random
from typing import Callable, Iterable, List, Optional, Tuple, Union

from .core import Wavefunction, _fmt_complex


Matrix = List[List[complex]]
Vector = List[complex]


# ────────────────────────────────────────────────────────────────────────────
# Matrix utilities (pure-Python complex linear algebra)
# ────────────────────────────────────────────────────────────────────────────


def _mat_mul(A: Matrix, B: Matrix) -> Matrix:
    """Matrix product A·B."""
    rows_a, cols_a = len(A), len(A[0])
    rows_b, cols_b = len(B), len(B[0])
    if cols_a != rows_b:
        raise ValueError(f"Matrix shape mismatch: {rows_a}×{cols_a} · {rows_b}×{cols_b}")
    return [
        [sum(A[i][k] * B[k][j] for k in range(cols_a)) for j in range(cols_b)]
        for i in range(rows_a)
    ]


def _mat_dagger(A: Matrix) -> Matrix:
    """Conjugate transpose A†."""
    rows, cols = len(A), len(A[0])
    return [[A[j][i].conjugate() for j in range(rows)] for i in range(cols)]


def _mat_tensor(A: Matrix, B: Matrix) -> Matrix:
    """Kronecker product A ⊗ B."""
    rows_a, cols_a = len(A), len(A[0])
    rows_b, cols_b = len(B), len(B[0])
    result = [[0 + 0j] * (cols_a * cols_b) for _ in range(rows_a * rows_b)]
    for i in range(rows_a):
        for j in range(cols_a):
            for k in range(rows_b):
                for l in range(cols_b):
                    result[i * rows_b + k][j * cols_b + l] = A[i][j] * B[k][l]
    return result


def _mat_apply(M: Matrix, v: Vector) -> Vector:
    """Matrix-vector product M·v."""
    rows, cols = len(M), len(M[0])
    if cols != len(v):
        raise ValueError(f"Cannot apply {rows}×{cols} matrix to vector of length {len(v)}")
    return [sum(M[i][j] * v[j] for j in range(cols)) for i in range(rows)]


def _mat_eye(n: int) -> Matrix:
    """n×n identity matrix."""
    return [[1.0 + 0j if i == j else 0 + 0j for j in range(n)] for i in range(n)]


def _mat_scale(M: Matrix, c: complex) -> Matrix:
    """Scalar multiple c·M."""
    return [[c * x for x in row] for row in M]


# ────────────────────────────────────────────────────────────────────────────
# Standard gate matrices (Phase 3)
# ────────────────────────────────────────────────────────────────────────────


_inv_sqrt2 = 1.0 / math.sqrt(2.0)

GATE_I: Matrix = [[1 + 0j, 0 + 0j], [0 + 0j, 1 + 0j]]
GATE_X: Matrix = [[0 + 0j, 1 + 0j], [1 + 0j, 0 + 0j]]
GATE_Y: Matrix = [[0 + 0j, 0 - 1j], [0 + 1j, 0 + 0j]]
GATE_Z: Matrix = [[1 + 0j, 0 + 0j], [0 + 0j, -1 + 0j]]
GATE_H: Matrix = [
    [_inv_sqrt2 + 0j, _inv_sqrt2 + 0j],
    [_inv_sqrt2 + 0j, -_inv_sqrt2 + 0j],
]
GATE_S: Matrix = [[1 + 0j, 0 + 0j], [0 + 0j, 0 + 1j]]
GATE_T: Matrix = [[1 + 0j, 0 + 0j], [0 + 0j, cmath.exp(1j * math.pi / 4)]]

# Two-qubit gates (4×4)
GATE_CNOT: Matrix = [
    [1 + 0j, 0 + 0j, 0 + 0j, 0 + 0j],
    [0 + 0j, 1 + 0j, 0 + 0j, 0 + 0j],
    [0 + 0j, 0 + 0j, 0 + 0j, 1 + 0j],
    [0 + 0j, 0 + 0j, 1 + 0j, 0 + 0j],
]
GATE_CZ: Matrix = [
    [1 + 0j, 0 + 0j, 0 + 0j, 0 + 0j],
    [0 + 0j, 1 + 0j, 0 + 0j, 0 + 0j],
    [0 + 0j, 0 + 0j, 1 + 0j, 0 + 0j],
    [0 + 0j, 0 + 0j, 0 + 0j, -1 + 0j],
]
GATE_SWAP: Matrix = [
    [1 + 0j, 0 + 0j, 0 + 0j, 0 + 0j],
    [0 + 0j, 0 + 0j, 1 + 0j, 0 + 0j],
    [0 + 0j, 1 + 0j, 0 + 0j, 0 + 0j],
    [0 + 0j, 0 + 0j, 0 + 0j, 1 + 0j],
]

_NAMED_GATES = {
    "I": (GATE_I, 1),
    "X": (GATE_X, 1),
    "Y": (GATE_Y, 1),
    "Z": (GATE_Z, 1),
    "H": (GATE_H, 1),
    "S": (GATE_S, 1),
    "T": (GATE_T, 1),
    "CNOT": (GATE_CNOT, 2),
    "CX": (GATE_CNOT, 2),
    "CZ": (GATE_CZ, 2),
    "SWAP": (GATE_SWAP, 2),
}


def _rx(theta: float) -> Matrix:
    """Rotation around X axis by angle θ."""
    c = math.cos(theta / 2)
    s = math.sin(theta / 2)
    return [[c + 0j, 0 - 1j * s], [0 - 1j * s, c + 0j]]


def _ry(theta: float) -> Matrix:
    """Rotation around Y axis by angle θ."""
    c = math.cos(theta / 2)
    s = math.sin(theta / 2)
    return [[c + 0j, -s + 0j], [s + 0j, c + 0j]]


def _rz(theta: float) -> Matrix:
    """Rotation around Z axis by angle θ."""
    return [
        [cmath.exp(-1j * theta / 2), 0 + 0j],
        [0 + 0j, cmath.exp(1j * theta / 2)],
    ]


# ────────────────────────────────────────────────────────────────────────────
# Gate class
# ────────────────────────────────────────────────────────────────────────────


class Gate:
    """A unitary operator acting on a fixed number of qubits.

    Constructed via the ``gate(...)`` factory. Apply to a wavefunction with
    ``apply_gate(psi, gate, qubits=...)`` — or use ``gate @ psi`` for
    single-qubit gates on a single-qubit state.

    Attributes:
        matrix: the unitary matrix (2^n_qubits × 2^n_qubits)
        n_qubits: number of qubits this gate acts on
        name: human-readable label
    """

    __slots__ = ("matrix", "n_qubits", "name")

    def __init__(self, matrix: Matrix, n_qubits: int, name: Optional[str] = None) -> None:
        expected_dim = 2 ** n_qubits
        if len(matrix) != expected_dim or len(matrix[0]) != expected_dim:
            raise ValueError(
                f"Gate matrix shape mismatch: expected {expected_dim}×{expected_dim} "
                f"for {n_qubits} qubits, got {len(matrix)}×{len(matrix[0])}"
            )
        self.matrix = matrix
        self.n_qubits = n_qubits
        self.name = name

    def __repr__(self) -> str:
        return f"<Gate {self.name or '?'} ({self.n_qubits}-qubit)>"

    def __matmul__(self, other):
        """``Gate @ Gate`` returns the composed gate (right-applied first).

        ``Gate @ Wavefunction`` applies the gate to a single-qubit state.
        For multi-qubit application, use ``apply_gate(psi, gate, qubits=...)``.
        """
        if isinstance(other, Gate):
            if self.n_qubits != other.n_qubits:
                raise ValueError(
                    f"Cannot compose {self.n_qubits}-qubit gate with "
                    f"{other.n_qubits}-qubit gate"
                )
            return Gate(
                matrix=_mat_mul(self.matrix, other.matrix),
                n_qubits=self.n_qubits,
                name=f"{self.name or '?'}·{other.name or '?'}",
            )
        if isinstance(other, Wavefunction):
            if self.n_qubits == 1:
                return apply_gate(other, self, qubits=[0])
            raise ValueError(
                f"Use apply_gate(psi, gate, qubits=[...]) for {self.n_qubits}-qubit gates"
            )
        return NotImplemented


def gate(name: str, *params: float) -> Gate:
    """Construct a named gate.

    Standard gates (no params):
        ``"I"``, ``"X"``, ``"Y"``, ``"Z"``, ``"H"``, ``"S"``, ``"T"``,
        ``"CNOT"`` (alias ``"CX"``), ``"CZ"``, ``"SWAP"``.

    Parametric rotations (one ``theta`` arg, in radians):
        ``"Rx"``, ``"Ry"``, ``"Rz"``.

    Example::

        h = gate("H")
        cnot = gate("CNOT")
        rx_pi = gate("Rx", math.pi)
    """
    name_upper = name.upper()

    if name_upper in {"RX", "RY", "RZ"}:
        if len(params) != 1:
            raise ValueError(f"{name} requires one angle parameter (radians)")
        theta = params[0]
        m = {"RX": _rx, "RY": _ry, "RZ": _rz}[name_upper](theta)
        return Gate(matrix=m, n_qubits=1, name=f"{name_upper}({theta:.4g})")

    if name_upper in _NAMED_GATES:
        matrix, n = _NAMED_GATES[name_upper]
        return Gate(matrix=matrix, n_qubits=n, name=name_upper)

    raise ValueError(
        f"Unknown gate: {name!r}. Known: I, X, Y, Z, H, S, T, CNOT/CX, CZ, SWAP, Rx, Ry, Rz"
    )


# ────────────────────────────────────────────────────────────────────────────
# apply_gate — multi-qubit aware
# ────────────────────────────────────────────────────────────────────────────


def _canonical_states(n_qubits: int) -> List[Tuple[str, ...]]:
    """Generate canonical tuple states for n qubits in bin-counting order."""
    return [tuple(format(i, f"0{n_qubits}b")) for i in range(2 ** n_qubits)]


def _system_n_qubits(psi: Wavefunction) -> int:
    """Determine number of qubits in a multi-qubit Wavefunction."""
    if not psi.is_quantum:
        raise ValueError("Quantum gates require a quantum-mode wavefunction (amplitudes=...)")
    if psi.is_collapsed:
        raise ValueError("Cannot apply a gate to a collapsed wavefunction")
    first = psi.states[0]
    if isinstance(first, tuple):
        n = len(first)
    elif isinstance(first, str) and len(first) >= 1 and first in {"0", "1"}:
        n = 1
    else:
        raise ValueError(
            f"Cannot determine qubit count: states should be '0'/'1' or tuples "
            f"of '0'/'1'. Got: {first!r}"
        )
    if len(psi.states) != 2 ** n:
        raise ValueError(
            f"Expected {2**n} states for {n} qubits, got {len(psi.states)}"
        )
    return n


def _expand_single_qubit_gate(matrix: Matrix, qubit: int, n_total: int) -> Matrix:
    """Expand a 2×2 gate to a 2^n × 2^n matrix by tensoring with identity.

    Qubit 0 is the leftmost (most significant) — first in tensor product.
    """
    result: Matrix = [[1 + 0j]]  # 1×1 starting point
    for q in range(n_total):
        op = matrix if q == qubit else GATE_I
        result = _mat_tensor(result, op)
    return result


def apply_gate(
    psi: Wavefunction, g: Gate, qubits: Optional[List[int]] = None
) -> Wavefunction:
    """Apply a quantum gate to a wavefunction.

    Args:
        psi: target wavefunction (must be quantum mode, not collapsed)
        g: the gate to apply
        qubits: which qubits of ``psi`` the gate acts on. If omitted:
            - For a 1-qubit gate on a 1-qubit ``psi`` → ``[0]``
            - For a gate acting on the same number of qubits as ``psi`` → all
            - Otherwise must be explicit, length matching ``g.n_qubits``.

    Returns:
        A new Wavefunction with the gate applied. Original ``psi`` is unchanged.

    Example::

        psi = bell_state("phi+")
        psi = apply_gate(psi, gate("X"), qubits=[0])    # flip first qubit
        # Result: (|10⟩ + |01⟩) / √2 = |ψ+⟩
    """
    n = _system_n_qubits(psi)

    if qubits is None:
        if g.n_qubits == n:
            qubits = list(range(n))
        elif g.n_qubits == 1 and n == 1:
            qubits = [0]
        else:
            raise ValueError(
                f"Cannot infer target qubits: gate is {g.n_qubits}-qubit, "
                f"state is {n}-qubit. Pass qubits=[...] explicitly."
            )

    if len(qubits) != g.n_qubits:
        raise ValueError(
            f"Gate is {g.n_qubits}-qubit but {len(qubits)} target qubits supplied"
        )
    if any(q < 0 or q >= n for q in qubits):
        raise ValueError(f"Qubit indices must be in 0..{n - 1}, got {qubits}")
    if len(set(qubits)) != len(qubits):
        raise ValueError(f"Duplicate qubit indices in {qubits}")

    # Build full-system matrix
    if g.n_qubits == 1:
        full = _expand_single_qubit_gate(g.matrix, qubits[0], n)
    elif g.n_qubits == 2 and len(qubits) == 2:
        full = _expand_two_qubit_gate(g.matrix, qubits[0], qubits[1], n)
    elif g.n_qubits == n:
        full = g.matrix
    else:
        raise NotImplementedError(
            f"apply_gate only supports 1-qubit, 2-qubit, or full-system gates "
            f"(got {g.n_qubits}-qubit gate on {n}-qubit state)"
        )

    new_amps = _mat_apply(full, psi.amplitudes)

    states = psi.states
    return Wavefunction(states=states, amplitudes=new_amps, name=psi.name)


def _expand_two_qubit_gate(
    matrix: Matrix, qubit_a: int, qubit_b: int, n_total: int
) -> Matrix:
    """Expand a 2-qubit (4×4) gate to a 2^n × 2^n matrix acting on qubits a, b.

    Handles arbitrary placement and ordering (a < b not required).
    Builds the full matrix by walking the 2^n state space and computing the
    image of each basis state under the gate (slow but clear).
    """
    if qubit_a == qubit_b:
        raise ValueError("Two-qubit gate requires distinct qubits")

    dim = 2 ** n_total
    full: Matrix = [[0 + 0j] * dim for _ in range(dim)]

    for i in range(dim):
        # Extract bits of source state
        bits_i = [(i >> (n_total - 1 - q)) & 1 for q in range(n_total)]
        # The pair (bits_i[qubit_a], bits_i[qubit_b]) is the input to the 2-qubit gate
        in_idx = bits_i[qubit_a] * 2 + bits_i[qubit_b]
        # The gate maps in_idx to a superposition over out_idx ∈ {0,1,2,3}
        for out_idx in range(4):
            amp = matrix[out_idx][in_idx]
            if amp == 0:
                continue
            out_a = (out_idx >> 1) & 1
            out_b = out_idx & 1
            bits_o = list(bits_i)
            bits_o[qubit_a] = out_a
            bits_o[qubit_b] = out_b
            j = sum(b << (n_total - 1 - p) for p, b in enumerate(bits_o))
            full[j][i] = full[j][i] + amp

    return full


# ────────────────────────────────────────────────────────────────────────────
# Measurement in basis + CHSH test (Phase 2)
# ────────────────────────────────────────────────────────────────────────────


def _clone(psi: Wavefunction) -> Wavefunction:
    """Deep-clone a wavefunction (independent collapse + state)."""
    if psi.is_quantum:
        return Wavefunction(
            states=list(psi.states), amplitudes=list(psi.amplitudes), name=psi.name
        )
    return Wavefunction(states=list(psi.states), weights=list(psi.weights), name=psi.name)


def _measure_z_basis(psi: Wavefunction, seed: Optional[int] = None) -> Tuple[str, ...]:
    """Sample a single outcome via Born rule. Doesn't mutate psi.

    Internal — uses a local RNG so multiple trials can be independent.
    """
    rng = random.Random(seed) if seed is not None else random
    probs = psi.weights  # |c|² when quantum
    return rng.choices(psi.states, weights=probs, k=1)[0]


def measure_in_basis(
    psi: Wavefunction,
    angle_a: float,
    angle_b: float,
    seed: Optional[int] = None,
) -> Tuple[int, int]:
    """For a 2-qubit state, measure qubit 0 in basis at angle_a and qubit 1 at angle_b.

    The measurement basis at angle θ (in the XZ plane of the Bloch sphere) has
    eigenvectors ``cos(θ/2)|0⟩ ± sin(θ/2)|1⟩``. We rotate the state by ``Ry(-θ)``
    on each qubit, then measure in the computational (Z) basis.

    Returns a pair of eigenvalues ``(±1, ±1)``: ``+1`` if outcome was ``"0"``,
    ``-1`` if ``"1"``.

    This is the building block of the CHSH test.
    """
    n = _system_n_qubits(psi)
    if n != 2:
        raise ValueError(f"measure_in_basis requires a 2-qubit state, got {n} qubits")

    psi_rot = apply_gate(_clone(psi), gate("Ry", -angle_a), qubits=[0])
    psi_rot = apply_gate(psi_rot, gate("Ry", -angle_b), qubits=[1])

    outcome = _measure_z_basis(psi_rot, seed=seed)
    e_a = +1 if outcome[0] == "0" else -1
    e_b = +1 if outcome[1] == "0" else -1
    return (e_a, e_b)


def chsh_test(
    psi: Wavefunction,
    n_trials: int = 2000,
    angles: Optional[Tuple[float, float, float, float]] = None,
    seed_base: int = 0,
) -> Tuple[float, dict]:
    """Run the CHSH inequality test on a 2-qubit state.

    Classical theories obey ``|S| ≤ 2`` (Bell's bound). Quantum mechanics
    can reach ``|S| ≤ 2√2 ≈ 2.828`` (Tsirelson's bound). A Bell state with
    optimal angles ``(a, a', b, b') = (0, π/2, π/4, 3π/4)`` achieves the
    Tsirelson bound, confirming genuine quantum entanglement.

    Args:
        psi: 2-qubit quantum-mode wavefunction
        n_trials: trials per correlation E(angle_a, angle_b)
        angles: ``(a, a', b, b')`` in radians; defaults to optimal Bell-state angles
        seed_base: deterministic RNG seed offset (for reproducible tests)

    Returns:
        ``(S, breakdown)`` where ``breakdown`` is a dict of the four
        correlations E(a,b), E(a,b'), E(a',b), E(a',b').

    Example::

        bell = bell_state("phi+")
        S, breakdown = chsh_test(bell, n_trials=10000)
        # Expect S ≈ 2.828 (well above classical |S| ≤ 2)
    """
    if angles is None:
        a, ap = 0.0, math.pi / 2
        b, bp = math.pi / 4, 3 * math.pi / 4
    else:
        a, ap, b, bp = angles

    def E(angle_a: float, angle_b: float, offset: int) -> float:
        total = 0
        for i in range(n_trials):
            e_a, e_b = measure_in_basis(psi, angle_a, angle_b, seed=seed_base + offset + i)
            total += e_a * e_b
        return total / n_trials

    e_ab = E(a, b, 0 * n_trials)
    e_abp = E(a, bp, 1 * n_trials)
    e_apb = E(ap, b, 2 * n_trials)
    e_apbp = E(ap, bp, 3 * n_trials)

    S = e_ab - e_abp + e_apb + e_apbp
    return S, {
        "E(a,b)": e_ab,
        "E(a,b')": e_abp,
        "E(a',b)": e_apb,
        "E(a',b')": e_apbp,
        "angles": {"a": a, "a'": ap, "b": b, "b'": bp},
        "classical_bound": 2.0,
        "tsirelson_bound": 2 * math.sqrt(2),
    }


# ────────────────────────────────────────────────────────────────────────────
# Density matrices (Phase 4)
# ────────────────────────────────────────────────────────────────────────────


class DensityMatrix:
    """A density matrix ρ — represents pure OR mixed quantum states.

    For a pure state ``|ψ⟩``: ρ = |ψ⟩⟨ψ| (outer product). Tr(ρ²) = 1.
    For a mixed state: ρ = Σᵢ pᵢ |ψᵢ⟩⟨ψᵢ| with ``Σpᵢ = 1``. Tr(ρ²) < 1.

    The density matrix formalism is essential for describing decoherence:
    environmental coupling causes off-diagonal elements to decay, turning
    a pure superposition into a classical mixture.

    Attributes:
        matrix: the 2^n × 2^n Hermitian, positive-semidefinite matrix
        n_qubits: number of qubits this density matrix describes
        name: optional label
    """

    __slots__ = ("matrix", "n_qubits", "name")

    def __init__(
        self,
        matrix: Matrix,
        n_qubits: int,
        name: Optional[str] = None,
    ) -> None:
        expected_dim = 2 ** n_qubits
        if len(matrix) != expected_dim:
            raise ValueError(
                f"DensityMatrix expects {expected_dim}×{expected_dim} for "
                f"{n_qubits} qubits, got {len(matrix)}×{len(matrix[0])}"
            )
        self.matrix = matrix
        self.n_qubits = n_qubits
        self.name = name

    @property
    def dim(self) -> int:
        return 2 ** self.n_qubits

    def trace(self) -> complex:
        """Tr(ρ). Should equal 1 for properly-normalized states."""
        return sum(self.matrix[i][i] for i in range(self.dim))

    def purity(self) -> float:
        """Tr(ρ²) — purity. 1 for pure states, < 1 for mixed.

        For Hermitian ρ, Tr(ρ²) = Σᵢⱼ |ρᵢⱼ|².
        """
        total = 0.0
        for i in range(self.dim):
            for j in range(self.dim):
                total += abs(self.matrix[i][j]) ** 2
        return total

    @property
    def is_pure(self) -> bool:
        """True iff this density matrix represents a pure state."""
        return abs(self.purity() - 1.0) < 1e-9

    def __repr__(self) -> str:
        label = self.name or "ρ"
        kind = "pure" if self.is_pure else "mixed"
        purity_str = f"purity={self.purity():.4f}"
        header = f"<DensityMatrix {label} ({self.n_qubits} qubits, {kind}, {purity_str})>"
        rows = []
        for row in self.matrix:
            rows.append("  " + "  ".join(_fmt_complex(c) for c in row))
        return header + "\n" + "\n".join(rows)


def density(psi: Wavefunction, name: Optional[str] = None) -> DensityMatrix:
    """Convert a pure quantum wavefunction to its density matrix ``|ψ⟩⟨ψ|``.

    Args:
        psi: a quantum-mode wavefunction (constructed with amplitudes=...)
        name: optional label (defaults to ``f"ρ({psi.name})"``)

    Returns:
        A pure ``DensityMatrix`` with ``Tr(ρ²) = 1``.

    Raises:
        ValueError: if psi is not in quantum mode.
    """
    if not psi.is_quantum:
        raise ValueError(
            "density() requires a quantum-mode wavefunction "
            "(constructed with amplitudes=...). For classical wavefunctions, "
            "the diagonal density-matrix would just be the probability distribution."
        )

    n = _system_n_qubits(psi)
    amps = psi.amplitudes
    matrix: Matrix = [
        [amps[i] * amps[j].conjugate() for j in range(len(amps))]
        for i in range(len(amps))
    ]
    return DensityMatrix(matrix, n_qubits=n, name=name or f"ρ({psi.name or 'ψ'})")


def decohere(rho: DensityMatrix, rate: float = 0.5) -> DensityMatrix:
    """Apply exponential decay to off-diagonal elements (decoherence model).

    Models environmental coupling: superposition phase information leaks into
    the environment, causing off-diagonal density-matrix entries to decay
    exponentially. The diagonal (classical probabilities) is preserved.

    Args:
        rho: input density matrix
        rate: decoherence rate. 0 → no change. Larger → faster decoherence.
            At rate = ∞, all off-diagonals → 0 (complete classical mixture).

    Returns:
        A new ``DensityMatrix`` with off-diagonals scaled by ``exp(-rate)``.

    Example::

        bell = bell_state("phi+")
        rho = density(bell)             # pure: purity = 1
        rho_d = decohere(rho, rate=2.0) # mostly mixed: purity ≈ 0.5
    """
    if rate < 0:
        raise ValueError(f"rate must be ≥ 0, got {rate}")
    decay = math.exp(-rate)
    new_matrix: Matrix = [
        [rho.matrix[i][j] * (1.0 if i == j else decay) for j in range(rho.dim)]
        for i in range(rho.dim)
    ]
    return DensityMatrix(
        new_matrix, n_qubits=rho.n_qubits, name=f"decohere({rho.name or 'ρ'}, {rate:.3g})"
    )


def partial_trace(rho: DensityMatrix, qubit: int) -> DensityMatrix:
    """Trace out one qubit, returning the reduced density matrix on the rest.

    The partial trace is the entanglement detector: if a 2-qubit state is
    entangled, tracing out either qubit yields a *mixed* state on the other
    (purity < 1). For separable states, the reduced state remains pure.

    For a Bell state, ``partial_trace`` over either qubit gives the maximally
    mixed state ``I/2`` (purity 0.5) — the strongest possible signature of
    entanglement.

    Args:
        rho: input density matrix
        qubit: which qubit to trace out (0-indexed, qubit 0 = leftmost)

    Returns:
        A new ``DensityMatrix`` on ``rho.n_qubits - 1`` qubits.

    Example::

        bell = bell_state("phi+")
        rho = density(bell)
        reduced = partial_trace(rho, qubit=0)
        # reduced is I/2 — maximally mixed, purity = 0.5
        # This proves the original bell was entangled.
    """
    n = rho.n_qubits
    if n < 2:
        raise ValueError(f"Cannot partial-trace a {n}-qubit density matrix")
    if not (0 <= qubit < n):
        raise ValueError(f"qubit must be in 0..{n - 1}, got {qubit}")

    new_n = n - 1
    new_dim = 2 ** new_n
    new_matrix: Matrix = [[0 + 0j for _ in range(new_dim)] for _ in range(new_dim)]

    for full_i in range(rho.dim):
        for full_j in range(rho.dim):
            bits_i = [(full_i >> (n - 1 - q)) & 1 for q in range(n)]
            bits_j = [(full_j >> (n - 1 - q)) & 1 for q in range(n)]

            # Trace contribution only when the traced qubit matches in i and j
            if bits_i[qubit] != bits_j[qubit]:
                continue

            reduced_bits_i = bits_i[:qubit] + bits_i[qubit + 1 :]
            reduced_bits_j = bits_j[:qubit] + bits_j[qubit + 1 :]
            ri = sum(b << (new_n - 1 - p) for p, b in enumerate(reduced_bits_i))
            rj = sum(b << (new_n - 1 - p) for p, b in enumerate(reduced_bits_j))
            new_matrix[ri][rj] += rho.matrix[full_i][full_j]

    return DensityMatrix(
        new_matrix, n_qubits=new_n, name=f"Tr_{qubit}({rho.name or 'ρ'})"
    )
