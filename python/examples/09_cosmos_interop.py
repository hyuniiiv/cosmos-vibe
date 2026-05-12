"""Example 09 — Layer 1 ↔ Layer 3 interop via from_cosmos (v3.3+).

Demonstrates the bridge between the CLI-level cosmos output (.quantum/ JSONL
files) and the Python primitives layer. You run /cosmos spawn from the shell,
let the agents complete, then load the result into Python for statistical
analysis or composition with other ψ-primitives.

This example reads whatever .quantum/ data exists in the current repo. If the
repo has the JWT-auth test data (the alpha/beta/gamma case from v1.x), you'll
see those insights. Otherwise it will report no cosmos found.
"""

import os
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from quantumagent import from_cosmos, observe, measure, constraint


def main() -> None:
    # Find the repo root — walk up from this file until we see .quantum/
    here = os.path.dirname(os.path.abspath(__file__))
    repo = here
    for _ in range(5):
        if os.path.isdir(os.path.join(repo, ".quantum")):
            break
        parent = os.path.dirname(repo)
        if parent == repo:
            break
        repo = parent
    else:
        print("No .quantum/ found walking up from this example.")
        print("Run /cosmos spawn first, then re-run this example from a repo with .quantum/")
        return

    print("━" * 70)
    print(f"  Reading cosmos run at: {repo}")
    print("━" * 70)
    print()

    try:
        run = from_cosmos(repo)
    except FileNotFoundError as e:
        print(f"  ✗ {e}")
        return

    print(f"  {run}")
    print()

    # Insight counts per cosmos
    print("  Insights per cosmos:")
    for name in run.names:
        n = len(run.insights[name])
        bar = "█" * n
        print(f"    {name:>10} : {n:3d}  {bar}")
    print()

    # The wavefunction (weighted by insight count)
    print(f"  Wavefunction (weights ∝ insight count):")
    dist = observe(run.psi)
    for state, prob in dist.items():
        print(f"    P({state}) = {prob:.3f}")
    print()

    # Heuristic resonance/uncertainty (token overlap only — crude)
    print("━" * 70)
    print("  Heuristic resonance (tokens appearing in ALL cosmos)")
    print("━" * 70)
    print()
    if run.resonance:
        for r in run.resonance[:15]:
            print(f"    • {r}")
    else:
        print("    (no token-level resonance — cosmos use very different vocabulary)")
    print()

    print("━" * 70)
    print("  Heuristic uncertainty (tokens in exactly ONE cosmos)")
    print("━" * 70)
    print()
    if run.uncertainty:
        for u in run.uncertainty[:15]:
            print(f"    • {u}")
    else:
        print("    (no purely-distinct tokens)")
    print()

    print("    NOTE: this is a crude token-overlap heuristic. For semantic-quality")
    print("    Resonance/Uncertainty analysis, run /cosmos observe (which uses")
    print("    Claude's judgment) and read the output.")

    # Macro layer
    if run.spin:
        print()
        print("━" * 70)
        print("  Project spin")
        print("━" * 70)
        print()
        print(f"    Name: {run.spin.get('name', '(none)')}")
        print(f"    Type: {run.spin.get('type', '(none)')}")
        constraints_list = run.spin.get("immutable_constraints", [])
        if constraints_list:
            print(f"    Constraints:")
            for c in constraints_list:
                print(f"      • {c}")

    if run.singularities:
        print()
        print("━" * 70)
        print(f"  Singularities ({len(run.singularities)} event(s))")
        print("━" * 70)
        for ev in run.singularities[-5:]:
            print(f"    {ev.get('ts', '?')}  {ev.get('name', '?')}: "
                  f"invalidates {ev.get('invalidates', [])}")

    # Demonstrate composing with quantum primitives
    print()
    print("━" * 70)
    print("  Composing with quantum primitives — Born-rule sample")
    print("━" * 70)
    print()
    print("    Treat the cosmos-weighted ψ as input to standard primitives.")
    print("    Example: sample 1000 times to confirm the distribution.")
    print()

    samples = [measure(from_cosmos(repo).psi, seed=i) for i in range(1000)]
    print(f"    Sampled distribution over 1000 measures:")
    for name in run.names:
        count = samples.count(name)
        bar = "█" * int(40 * count / 1000)
        print(f"      {name:>10} : {count:4d}  {bar}")
    print()
    print("    The cosmos run's distribution is now first-class in Python — you can")
    print("    compose it with constraints, entanglement, observe/measure, etc.")


if __name__ == "__main__":
    main()
