---
name: cosmos:stop
description: Tear down all cosmos worktrees and branches, optionally purging Quantum Memory (.quantum/) — clean shutdown of the multiverse harness.
---

# cosmos:stop

Remove all cosmos worktrees and branches. Optionally clean quantum memory.

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

From the output, identify worktrees whose branch column starts with `cosmos/`.
Extract the cosmos name as the part after `cosmos/`
(e.g., `[cosmos/alpha]` → name is `alpha`).

If no cosmos worktrees are found:
```
(no active cosmos)
```
Then skip to Step 5.

### Step 3 — Remove each worktree

For each cosmos worktree `<name>`:

```bash
git worktree remove <repo_root>/cosmos/<name> --force
```

If the command fails (worktree already removed), continue.

### Step 4 — Delete cosmos branches

For each cosmos that had a worktree:

```bash
git branch -D cosmos/<name>
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
🛑 All cosmos stopped.

   Worktrees removed: alpha, beta, gamma
   Branches deleted:  cosmos/alpha, cosmos/beta, cosmos/gamma
   Quantum memory: <deleted | preserved at .quantum/>
```
