"""Core quantum-inspired primitives.

This MVP uses real-valued probability distributions and Born-rule sampling for
measurement. Complex amplitudes (true quantum interference) are reserved for a
future Path B release. The user-facing API is designed to be forward-compatible —
when complex amplitudes land, ``psi(states, weights)`` becomes ``psi(states,
amplitudes)`` with a ``quantum=True`` flag, but existing code continues to work
in classical-probability mode.

Design choices:
- Operators (constraints) are *immutable* and applied via ``op @ psi``, returning
  a NEW wavefunction. This matches the linear-algebra intuition where operators
  do not mutate their operands.
- ``measure`` is the only mutating operation — it collapses the wavefunction in
  place, matching quantum-mechanical semantics where measurement is irreversible.
- Entanglement is registered with a ``correlation`` callable that returns True
  for compatible state pairs. Measuring one wavefunction conditions its entangled
  partner's distribution accordingly.

All public names are re-exported from ``quantumagent``.
"""

from __future__ import annotations

import random
from typing import Callable, Iterable, Optional


# ────────────────────────────────────────────────────────────────────────────
# Wavefunction
# ────────────────────────────────────────────────────────────────────────────


class Wavefunction:
    """A decision in superposition — a probability distribution over discrete states.

    Attributes:
        states: ordered list of possible states (any hashable)
        weights: real-valued probability weights, normalized so they sum to 1
        name: optional human-readable label (used in ``repr`` and errors)
        is_collapsed: True after ``measure`` has been called
    """

    __slots__ = ("states", "weights", "name", "_entanglements", "_collapsed_to")

    def __init__(
        self,
        states: Iterable,
        weights: Optional[Iterable[float]] = None,
        name: Optional[str] = None,
    ) -> None:
        states_list = list(states)
        if not states_list:
            raise ValueError("Wavefunction requires at least one state")
        if len(set(map(_hashable, states_list))) != len(states_list):
            raise ValueError(
                "Pauli Exclusion: states must be unique within a wavefunction"
            )

        if weights is None:
            n = len(states_list)
            weights_list = [1.0 / n] * n
        else:
            weights_list = [float(w) for w in weights]
            if len(weights_list) != len(states_list):
                raise ValueError(
                    f"weights length ({len(weights_list)}) must match states "
                    f"length ({len(states_list)})"
                )
            if any(w < 0 for w in weights_list):
                raise ValueError("weights must be non-negative")
            total = sum(weights_list)
            if total <= 0:
                raise ValueError("sum of weights must be positive")
            weights_list = [w / total for w in weights_list]

        self.states = states_list
        self.weights = weights_list
        self.name = name
        self._entanglements: list[tuple["Wavefunction", Callable, str]] = []
        self._collapsed_to = None

    # ── properties ──

    @property
    def is_collapsed(self) -> bool:
        return self._collapsed_to is not None

    @property
    def collapsed_state(self):
        """The state this wavefunction collapsed to (None if not collapsed)."""
        return self._collapsed_to

    # ── observation ──

    def distribution(self) -> dict:
        """Return ``{state: probability}`` snapshot. Non-destructive."""
        return {s: w for s, w in zip(self.states, self.weights)}

    # ── representation ──

    def __repr__(self) -> str:
        label = self.name or "ψ"
        if self.is_collapsed:
            return f"<{label} collapsed → {self._collapsed_to!r}>"
        body = ", ".join(
            f"{state!r}:{weight:.3f}"
            for state, weight in zip(self.states, self.weights)
            if weight > 0
        )
        return f"<{label} {{{body}}}>"


def _hashable(x):
    """Try to use the value directly; if unhashable, fall back to repr."""
    try:
        hash(x)
        return x
    except TypeError:
        return repr(x)


# ────────────────────────────────────────────────────────────────────────────
# psi — the constructor
# ────────────────────────────────────────────────────────────────────────────


def psi(
    states: Iterable,
    weights: Optional[Iterable[float]] = None,
    name: Optional[str] = None,
) -> Wavefunction:
    """Declare a decision as a wavefunction in superposition.

    Args:
        states: discrete possible values the decision can take
        weights: optional prior probabilities (auto-normalized). Defaults to
            uniform distribution.
        name: optional label used in repr and error messages

    Example::

        cache = psi(["redis", "cdn", "lru"])                       # uniform
        cache = psi(["redis", "cdn", "lru"], [0.6, 0.3, 0.1])      # weighted
        cache = psi(["redis", "cdn", "lru"], name="cache-strategy")
    """
    return Wavefunction(states, weights, name)


# ────────────────────────────────────────────────────────────────────────────
# Operators — constraints curve the distribution
# ────────────────────────────────────────────────────────────────────────────


class Operator:
    """A transformation applied to a wavefunction via ``op @ psi``.

    Operators are immutable — applying one returns a NEW wavefunction. This
    matches the linear-algebra intuition: operators don't mutate their operands.
    """

    __slots__ = ("name", "_apply")

    def __init__(self, name: str, apply_fn: Callable[[Wavefunction], Wavefunction]) -> None:
        self.name = name
        self._apply = apply_fn

    def __matmul__(self, other: Wavefunction) -> Wavefunction:
        if not isinstance(other, Wavefunction):
            return NotImplemented
        return self._apply(other)

    def __repr__(self) -> str:
        return f"<Operator: {self.name}>"


class Constraint(Operator):
    """A named constraint that adjusts a wavefunction's weights.

    Constraints curve the solution space — states matching the constraint's
    preference get amplified, others suppressed. This is the General Relativity
    analog: constraints bend the geodesics through the decision landscape.

    Supports three patterns (can be combined):
        boost: dict — multiply specific states' weights
        where: callable — keep only states where ``where(state)`` is truthy
        suppress: dict — divide specific states' weights
    """


def constraint(
    name: str,
    *,
    boost: Optional[dict] = None,
    suppress: Optional[dict] = None,
    where: Optional[Callable] = None,
) -> Constraint:
    """Construct a constraint operator.

    Args:
        name: label for this constraint (appears in repr and trace)
        boost: ``{state: multiplier}`` — weights for matching states are
            multiplied by their multiplier
        suppress: ``{state: divisor}`` — weights for matching states are
            divided by their divisor (use values > 1 to suppress)
        where: ``callable(state) -> bool`` — keep only states for which this
            returns truthy. Equivalent to setting non-matching weights to 0.

    Returns:
        A ``Constraint`` operator usable as ``constraint(...) @ psi``.

    Example::

        cache = psi(["redis", "cdn", "lru"])
        cache = constraint("low-latency", boost={"redis": 2.0}) @ cache
        cache = constraint("no-external", where=lambda s: s != "cdn") @ cache

    Raises:
        ValueError: if the constraint zeros out all states.
    """
    def apply(psi_in: Wavefunction) -> Wavefunction:
        new_weights = list(psi_in.weights)

        if where is not None:
            new_weights = [
                w if where(s) else 0.0
                for s, w in zip(psi_in.states, new_weights)
            ]

        if boost:
            for state, multiplier in boost.items():
                if state in psi_in.states:
                    idx = psi_in.states.index(state)
                    new_weights[idx] *= multiplier

        if suppress:
            for state, divisor in suppress.items():
                if state in psi_in.states:
                    idx = psi_in.states.index(state)
                    if divisor == 0:
                        raise ValueError(
                            f"suppress divisor for {state!r} cannot be 0; "
                            f"use where=... or boost with 0 instead"
                        )
                    new_weights[idx] /= divisor

        total = sum(new_weights)
        if total <= 0:
            raise ValueError(
                f"Constraint {name!r} zeroed out all states of "
                f"{psi_in.name or 'ψ'} — at least one state must survive"
            )

        return Wavefunction(
            states=psi_in.states,
            weights=new_weights,
            name=psi_in.name,
        )

    return Constraint(name, apply)


# ────────────────────────────────────────────────────────────────────────────
# Entanglement
# ────────────────────────────────────────────────────────────────────────────


def entangle(
    a: Wavefunction,
    b: Wavefunction,
    correlation: Callable,
) -> None:
    """Link two wavefunctions so that measuring one conditions the other.

    The correlation function is called with state pairs; True means the pair
    is compatible. When one wavefunction is measured, its entangled partner's
    distribution is restricted to states compatible with the measured value
    (then re-normalized).

    Args:
        a: first wavefunction
        b: second wavefunction
        correlation: ``callable(state_a, state_b) -> bool`` — True if the
            pair is jointly possible

    Example::

        auth = psi(["jwt", "session", "oauth"])
        store = psi(["redis", "postgres", "memory"])
        # JWT can be stateless or use redis. Session needs redis.
        entangle(auth, store, lambda a, s:
            (a == "jwt"     and s in ("redis", "memory")) or
            (a == "session" and s == "redis")             or
            (a == "oauth"   and s in ("redis", "postgres"))
        )

    After measuring ``auth`` to e.g. "session", ``store``'s distribution is
    reduced to just {"redis": 1.0}.

    Raises:
        ValueError: if a or b is already collapsed.
    """
    if a.is_collapsed or b.is_collapsed:
        raise ValueError("Cannot entangle a collapsed wavefunction")
    if a is b:
        raise ValueError("Cannot entangle a wavefunction with itself")

    a._entanglements.append((b, correlation, "a"))
    b._entanglements.append((a, correlation, "b"))


# ────────────────────────────────────────────────────────────────────────────
# Observation (non-destructive) and Measurement (collapse)
# ────────────────────────────────────────────────────────────────────────────


def observe(psi_in: Wavefunction) -> dict:
    """Non-destructive read of the wavefunction's current distribution.

    Returns ``{state: probability}``. Does NOT collapse the wavefunction —
    call ``observe`` as many times as you want.

    This is the QuantumAgent distinction made first-class: ``observe`` is
    the weak measurement (always available), ``measure`` is the collapsing
    measurement (irreversible).

    Example::

        cache = psi(["redis", "cdn"], [0.7, 0.3])
        print(observe(cache))   # {"redis": 0.7, "cdn": 0.3}
        print(observe(cache))   # same — superposition intact
    """
    return psi_in.distribution()


def measure(psi_in: Wavefunction, seed: Optional[int] = None):
    """Collapse the wavefunction to a single state via Born-rule sampling.

    Side effects:
        - ``psi_in`` becomes collapsed; subsequent ``measure`` calls return
          the same state (no re-sampling)
        - Entangled partners have their distributions conditioned on this
          measurement and re-normalized

    Args:
        psi_in: the wavefunction to collapse
        seed: optional RNG seed for deterministic measurement (useful in tests)

    Returns:
        The single state that ``psi_in`` collapsed to.

    Example::

        cache = psi(["redis", "cdn", "lru"], [0.5, 0.3, 0.2])
        chosen = measure(cache, seed=42)   # deterministic with seed
        assert chosen in ("redis", "cdn", "lru")
        assert cache.is_collapsed

    Raises:
        ValueError: if measuring contradicts an entangled partner that's
            already constrained to no compatible states.
    """
    if psi_in.is_collapsed:
        return psi_in._collapsed_to

    rng = random.Random(seed) if seed is not None else random
    chosen = rng.choices(psi_in.states, weights=psi_in.weights, k=1)[0]

    # Collapse
    psi_in._collapsed_to = chosen
    psi_in.weights = [1.0 if s == chosen else 0.0 for s in psi_in.states]

    # Propagate to entangled partners
    for partner, corr, side in psi_in._entanglements:
        if partner.is_collapsed:
            # Partner already collapsed — verify compatibility
            other = partner._collapsed_to
            ok = corr(chosen, other) if side == "a" else corr(other, chosen)
            if not ok:
                raise ValueError(
                    f"Entanglement violation: measurement "
                    f"{psi_in.name or 'ψ'}={chosen!r} is incompatible with "
                    f"already-collapsed partner {partner.name or 'ψ'}={other!r}"
                )
            continue

        # Restrict partner's distribution to compatible states
        new_weights = []
        for s, w in zip(partner.states, partner.weights):
            ok = corr(chosen, s) if side == "a" else corr(s, chosen)
            new_weights.append(w if ok else 0.0)

        total = sum(new_weights)
        if total == 0:
            raise ValueError(
                f"Entanglement collapse: no states in {partner.name or 'ψ'} "
                f"are compatible with {psi_in.name or 'ψ'}={chosen!r}. "
                f"Check the correlation function or relax constraints."
            )
        partner.weights = [w / total for w in new_weights]

    return chosen
