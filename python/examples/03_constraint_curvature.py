"""Example 03 — constraints curve the distribution.

Demonstrates: applying constraints as operators that bend the probability
landscape (General Relativity analog — constraints curve solution space).

Each constraint is named and immutable. Applying it returns a new wavefunction;
the original is unchanged.
"""

import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from quantumagent import psi, constraint, observe, measure


def main() -> None:
    # Five database options, uniform prior.
    db = psi(
        ["postgres", "mysql", "sqlite", "dynamodb", "redis"],
        name="database",
    )

    print("Uniform prior (no constraints):")
    print(f"  {observe(db)}")

    # Constraint 1: must support full SQL (excludes redis, dynamodb).
    sql_only = constraint("sql-required", where=lambda s: s in {"postgres", "mysql", "sqlite"})
    db1 = sql_only @ db
    print(f"\nAfter 'sql-required' (where=): {observe(db1)}")

    # Constraint 2: production-grade preference (postgres × 3, mysql × 2).
    prod_pref = constraint(
        "production-grade",
        boost={"postgres": 3.0, "mysql": 2.0},
    )
    db2 = prod_pref @ db1
    print(f"After 'production-grade' (boost): {observe(db2)}")

    # Constraint 3: low ops overhead — suppress postgres (it's the most opinionated).
    low_ops = constraint("low-ops-overhead", suppress={"postgres": 2.0})
    db3 = low_ops @ db2
    print(f"After 'low-ops-overhead' (suppress): {observe(db3)}")

    print(f"\nFinal curved distribution: {observe(db3)}")
    print(f"Original wavefunction unchanged: {observe(db)}")

    # Measurement now samples from the curved distribution.
    chosen = measure(db3, seed=42)
    print(f"\nmeasure(seed=42) → {chosen!r}")
    print("(constraints made the choice non-uniform — the result reflects the curvature)")


if __name__ == "__main__":
    main()
