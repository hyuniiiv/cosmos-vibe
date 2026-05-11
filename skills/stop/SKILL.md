# cosmos:stop

Remove all universe worktrees and branches. Optionally clean quantum memory.

## Trigger

`/cosmos stop`

## Execution Steps

### Step 1 — Detect repo root

```bash
git rev-parse --show-toplevel
```

Store as `<repo_root>`.

### Step 2 — List active worktrees

```bash
git worktree list
```

From the `git worktree list` output, identify worktrees whose branch column
(the `[branch-name]` in square brackets) starts with `universe/`.
Extract the universe name as the part after `universe/`
(e.g., `[universe/alpha]` → name is `alpha`).

If no universe worktrees are found:
```
(no active universes)
```
Then skip to Step 5.

### Step 3 — Remove each worktree

For each universe worktree `<name>`:

```bash
git worktree remove <repo_root>/universes/<name> --force
```

If the command fails (worktree already removed), continue to the next.

### Step 4 — Delete universe branches

For each universe that had a worktree:

```bash
git branch -D universe/<name>
```

Ignore errors for branches that don't exist.

### Step 5 — Offer quantum memory cleanup

Ask the user:

> Delete `.quantum/` directory (all recorded insights)?
>
> - **yes** — permanently delete all insights
> - **no** — keep insights for reference

**If yes:**
```bash
rm -rf <repo_root>/.quantum/
```

**If no:**
Insights preserved at `.quantum/`.

### Step 6 — Confirm

Output:

```
🛑 All universes stopped.

   Worktrees removed: alpha, beta, gamma
   Branches deleted:  universe/alpha, universe/beta, universe/gamma
   Quantum memory: <deleted | preserved at .quantum/>
```
