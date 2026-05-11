# cosmos:crystallize

Collapse a specific cosmos from superposition into a concrete result.
Other cosmos remain in superposition — they are NOT affected.

This is the wave function collapse: you've observed long enough, now you choose
one reality.

## Trigger

`/cosmos crystallize <cosmos_id>`

Example: `/cosmos crystallize alpha`

## Execution Steps

### Step 1 — Detect repo root

```bash
git rev-parse --show-toplevel
```

Store as `<repo_root>`.

### Step 2 — Read insights

Read `<repo_root>/.quantum/<cosmos_id>/insights.jsonl`.
Parse each line as JSON.

If the file is empty or missing:
```
❌ cosmos:<cosmos_id> has no insights yet.
   Run /cosmos spawn first, or wait for agents to complete.
```
Then stop.

### Step 3 — Summarize worktree branch state

```bash
git -C <repo_root>/cosmos/<cosmos_id> log --oneline -10
git -C <repo_root>/cosmos/<cosmos_id> diff HEAD --stat
git -C <repo_root>/cosmos/<cosmos_id> status --short
```

Show:
- Current branch name
- Last 10 commits
- Changed/uncommitted files

If the worktree no longer exists (e.g., after `/cosmos stop`), skip this step
and proceed using only the insights file.

### Step 4 — Crystallization report

From the insights, identify and summarize:
1. **Core decisions** — What architectural choices were made?
2. **Trade-offs rejected** — What alternatives were considered and why?
3. **Resonance adopted** — Which insights came from other cosmos via entanglement?
4. **Quantum Tunneling** — Any `[TUNNEL]`-tagged insights? List each: what constraint was assumed, what bypass was found.
5. **Quantum Jumps** — Any `[JUMP]`-tagged insights? List each: what single entanglement read caused the discontinuous shift, and what changed.
6. **Final answer** — What is this cosmos's solution to the goal?

Present as:

```
💎 cosmos:<cosmos_id> — Crystallization
════════════════════════════════════════

Strategy: <strategy>
Insights: <N>
Branch: cosmos/<cosmos_id>

Core Decisions:
  1. <decision>
  2. <decision>

Trade-offs Rejected:
  - <option> → rejected because <reason>

Resonance Adopted (from other cosmos):
  - <insight adopted via entanglement, or "none">

Quantum Tunneling:
  - [TUNNEL] <bypassed constraint and how, or "none">

Quantum Jumps:
  - [JUMP] <what changed discontinuously and why, or "none">

Final Answer:
  <summary of what was built and why>
```

### Step 5 — Schrödinger check before merge

Before offering to merge, prompt the user:

```
🐱 Schrödinger's Cat collapses on crystallization — quality is now definite, not potential.
   Have you run your test suite against cosmos/<cosmos_id>?

   - yes, tests pass — proceed to merge
   - yes, tests failed — do not merge; fix in the cosmos branch, then re-crystallize
   - no, not yet — run tests first; come back when ready
```

Wait for user response.
- "yes, tests pass" → continue to Step 6
- "yes, tests failed" → stop; output: `❌ Do not merge a failing cosmos. Fix the issues in cosmos/<cosmos_id>, then run /cosmos crystallize <cosmos_id> again.`
- "no, not yet" → stop; output: `Run your tests first. Re-run /cosmos crystallize <cosmos_id> when ready.`

### Step 6 — Offer merge

Ask the user:

> Merge `cosmos/<cosmos_id>` into main?
>
> - **yes** — `git merge cosmos/<cosmos_id> --no-ff`
> - **no** — keep the branch for later

Wait for user response.

**If yes:**

Detect the default branch:
```bash
git symbolic-ref --short HEAD
```
Switch to main/master if not already on it, then:
```bash
git merge cosmos/<cosmos_id> --no-ff -m "feat: crystallize cosmos/<cosmos_id>"
```

Output: `✅ Merged cosmos/<cosmos_id> into main.`

**If no:**
Output: `Branch cosmos/<cosmos_id> preserved. Run /cosmos crystallize <cosmos_id> again to merge later.`

---

*Note: `/cosmos observe` is non-destructive — it reads without collapsing the superposition.
`/cosmos crystallize` is the measurement that collapses one cosmos into a definite result.*
