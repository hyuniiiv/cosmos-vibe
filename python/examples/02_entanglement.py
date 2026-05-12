"""Example 02 — entangled decisions.

Demonstrates: registering a correlation between two wavefunctions,
measuring one and watching the other's distribution condition automatically.

Domain: authentication mechanism × session storage.
Not all combinations are valid — entanglement enforces those constraints.
"""

import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from quantumagent import psi, entangle, observe, measure


def main() -> None:
    # Two decisions that aren't independent.
    auth = psi(
        ["jwt-stateless", "session-cookie", "oauth2"],
        weights=[0.4, 0.4, 0.2],
        name="auth",
    )
    store = psi(
        ["redis", "postgres", "in-memory"],
        weights=[0.4, 0.4, 0.2],
        name="store",
    )

    # Compatibility rules:
    # - jwt-stateless doesn't actually need a store, but if used, redis or in-memory
    # - session-cookie requires a fast key-value store: redis
    # - oauth2 needs a durable store: postgres
    def compatible(a: str, s: str) -> bool:
        if a == "jwt-stateless":
            return s in ("redis", "in-memory")
        if a == "session-cookie":
            return s == "redis"
        if a == "oauth2":
            return s == "postgres"
        return False

    entangle(auth, store, compatible)

    print("BEFORE measurement:")
    print(f"  auth  → {observe(auth)}")
    print(f"  store → {observe(store)}")

    # Measure auth — store's distribution will be conditioned automatically.
    chosen_auth = measure(auth, seed=7)
    print(f"\nmeasure(auth, seed=7) → {chosen_auth!r}")

    print("\nAFTER measuring auth (entanglement propagates):")
    print(f"  auth  → {observe(auth)}")
    print(f"  store → {observe(store)}    ← distribution conditioned on auth")
    print(f"  store is_collapsed: {store.is_collapsed} (still in superposition over compatible states)")

    # Measuring store now uses the conditioned distribution.
    chosen_store = measure(store, seed=11)
    print(f"\nmeasure(store, seed=11) → {chosen_store!r}")

    print("\nFINAL state:")
    print(f"  auth  = {auth.collapsed_state!r}")
    print(f"  store = {chosen_store!r}")
    assert compatible(chosen_auth, chosen_store), "entanglement should guarantee compatibility"
    print("  ✓ entanglement guarantee held: pair is compatible")


if __name__ == "__main__":
    main()
