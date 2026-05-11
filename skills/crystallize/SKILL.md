# cosmos:crystallize

Extract a specific universe's insights and branch state as a standalone result.
Other universes remain in superposition — they are NOT affected by crystallize.

## Trigger

`/cosmos crystallize <universe_id>`

Example: `/cosmos crystallize alpha`

## Execution Steps

### Step 1 — Detect repo root

```bash
git rev-parse --show-toplevel
```

Store as `<repo_root>`.

### Step 2 — Read insights

Read `<repo_root>/.quantum/<universe_id>/insights.jsonl`.
Parse each line as JSON.

If the file is empty or missing:
```
❌ Universe '<universe_id>' has no insights yet.
   Run /cosmos spawn first, or wait for agents to record insights.
```
Then stop.

### Step 3 — Summarize worktree branch state

```bash
git -C <repo_root>/universes/<universe_id> log --oneline -10
git -C <repo_root>/universes/<universe_id> diff HEAD --stat
git -C <repo_root>/universes/<universe_id> status --short
```

Show:
- Current branch name
- Last 10 commits
- Changed/uncommitted files

### Step 4 — Extract key decisions

From the insights, identify and summarize:
1. **Core design decisions** — What architectural choices were made?
2. **Key trade-offs** — What alternatives were considered and rejected?
3. **Final approach** — What is the universe's answer to the goal?
4. **Entanglement influence** — Did this universe adapt from another universe's insights?

Present as:

```
💎 Universe <universe_id> — Crystallization Report
════════════════════════════════════════════════

Strategy: <strategy>
Insights recorded: <N>
Branch: universe/<universe_id>

Core Decisions:
  1. <decision>
  2. <decision>

Key Trade-offs:
  - <trade-off>

Final Approach:
  <summary>

Entanglement Influence:
  <any cross-universe adaptation, or "none detected">
```

### Step 5 — Offer merge

Ask the user:

> Crystallization complete. Merge `universe/<universe_id>` into main?
>
> - **yes** — `git merge universe/<universe_id> --no-ff`
> - **no** — keep the branch for later

Wait for user response.

**If yes:**
```bash
git merge universe/<universe_id> --no-ff -m "feat: crystallize universe/<universe_id>

Insights recorded: <N>
Strategy: <strategy>"
```

Output: `✅ Merged universe/<universe_id> into main.`

**If no:**
Output: `Branch universe/<universe_id> preserved. Run /cosmos crystallize <universe_id> again to merge later.`
