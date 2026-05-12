---
name: cosmos:spin
description: QuantumAgent — Declare or update the project's immutable identity (project spin). The spin defines invariant constraints that every future cosmos inherits automatically. Macro-scale anchor for the QuantumAgent harness.
---

# cosmos:spin

Declare or update the project's **immutable quantum identity** — its spin. Every `/cosmos spawn` reads the spin and injects it into every cosmos as invariant constraints. A strategy that violates the project spin is not exploring the goal; it is exploring a different problem.

This is the **macro-scale anchor** of QuantumAgent. While `/cosmos singularity` records *events* that reshape context, `/cosmos spin` declares *identity* that persists throughout the project's lifetime.

## Trigger

```
/cosmos spin --name "<name>" [--type "<type>"] [--description "<text>"] [--constraints "<c1,c2,c3>"]
```

Or with no arguments to display current spin:

```
/cosmos spin
```

Examples:

```bash
# Declare a fresh spin
/cosmos spin \
  --name "QuantumAgent" \
  --type "claude-code-plugin" \
  --description "Parallel cosmos exploration harness" \
  --constraints "no external runtime dependencies,git-native control plane,claude code compatible"

# Display current spin
/cosmos spin
```

## Execution Steps

### Step 1 — Detect repo root

```bash
git rev-parse --show-toplevel
```

Store as `<repo_root>`.

### Step 2 — Parse arguments

From the trigger message, extract:
- `--name` *(required for create/update)* — short identifier of the project
- `--type` *(optional)* — project category (e.g., `claude-code-plugin`, `web-app`, `cli-tool`, `library`)
- `--description` *(optional)* — one-line description
- `--constraints` *(optional)* — comma-separated list of immutable constraints

If NO arguments provided → operate in **display mode** (skip to Step 5).

If `--name` missing in modify mode:
```
❌ Project spin requires --name when declaring or updating.
   Usage: /cosmos spin --name "<name>" [--type "..."] [--description "..."] [--constraints "..."]
   Display current spin: /cosmos spin
```

### Step 3 — Read existing spin (if any)

```bash
[ -f <repo_root>/.quantum/project/spin.json ] && cat <repo_root>/.quantum/project/spin.json
```

If exists → parse and use as base (this is an **update**). Capture existing fields not overridden by new arguments.

If not exists → this is a **fresh declaration**.

### Step 4 — Compose spin object

Merge provided arguments with existing values (if any):

```json
{
  "name": "<name>",
  "type": "<type or existing or null>",
  "description": "<description or existing or null>",
  "immutable_constraints": ["<c1>", "<c2>", ...],
  "established": "<existing established timestamp, or now if first time>",
  "updated": "<now>"
}
```

**Rules:**
- `name` is the only required field
- `established` is set ONCE on first declaration and preserved on updates (the identity is anchored to that timestamp)
- `updated` reflects the most recent change
- `immutable_constraints` — when `--constraints` is provided, REPLACE the list (not merge). Updating constraints is a deliberate act; provide the full new list.

### Step 5 — Write spin.json (or display)

**Modify mode** (arguments provided):

```bash
mkdir -p <repo_root>/.quantum/project
```

Write the composed JSON to `<repo_root>/.quantum/project/spin.json` using the Write tool (this file is small, single-document JSON — Write is appropriate, not append).

**Display mode** (no arguments):

If `spin.json` exists, output its contents pretty-printed:

```
🌍 Project Spin

   Name:        <name>
   Type:        <type>
   Description: <description>
   Established: <established>
   Updated:     <updated>

   Immutable constraints:
     • <constraint 1>
     • <constraint 2>
     • <constraint 3>
```

If `spin.json` does not exist:

```
(no project spin declared yet — run /cosmos spin --name "..." to establish one)
```

Then stop.

### Step 6 — Check for active cosmos

```bash
git -C <repo_root> worktree list | grep -E '\[cosmos/' || true
```

If active cosmos exist after a modify, output:

```
⚠️  Active cosmos detected: <list>
   This spin change will NOT retroactively affect running cosmos.
   New /cosmos spawn calls will inherit the updated spin automatically.
```

If no active cosmos, skip.

### Step 7 — Confirm

For a modify operation, output:

```
✨ Project spin <declared|updated>

   Name:        <name>
   Type:        <type or "(unspecified)">
   Description: <description or "(unspecified)">

   Immutable constraints (<N>):
     • <constraint 1>
     • <constraint 2>

🌌 All future /cosmos spawn calls will inherit this spin as invariant context.
   Strategies that violate these constraints will be flagged as exploring the wrong problem.

   Stored at: .quantum/project/spin.json
```

## When to declare a spin

**Good fit:**
- Project has moved past prototyping — its identity is stable
- Multiple cosmos runs are planned over time (consistency matters)
- Compliance/architectural constraints must not be violated
- Team wants shared understanding of "what this project IS"

**Not yet:**
- Greenfield exploration — identity itself is one of the things being explored
- Single one-off cosmos run — overhead exceeds benefit
- Project in major pivot (declare spin AFTER pivot stabilizes)

## When to update a spin

**Reasonable updates:**
- Add a new immutable constraint discovered through experience
- Clarify the description as understanding deepens
- Re-categorize the type if the project's nature became clearer

**Not appropriate as a spin update:**
- "Pivot" — that's a singularity (use `/cosmos singularity` instead)
- Removing a constraint that was previously load-bearing — declare a singularity first to mark the era change

## Why this matters

A project without a declared spin is a *free* multiverse — every cosmos explores from a blank slate. That's fine for greenfield work but wasteful for mature projects. Declaring spin tells cosmos: "*these* are the things I will never trade away. Don't propose them as alternatives, don't optimize against them. Find solutions that respect them."

In the General Relativity analog: spin is the project's intrinsic mass — it permanently curves the solution space, and every cosmos follows geodesics through that curved field automatically.

## Format reference

`.quantum/project/spin.json` is a single JSON object:

```json
{
  "name": "string (required)",
  "type": "string (optional)",
  "description": "string (optional)",
  "immutable_constraints": ["string", ...],
  "established": "ISO 8601 timestamp (set once)",
  "updated": "ISO 8601 timestamp (most recent change)"
}
```

Every `/cosmos spawn` and `/cosmos observe` reads this file to inject project context.
