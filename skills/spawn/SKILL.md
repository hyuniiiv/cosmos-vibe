# cosmos:spawn

Spawn N parallel cosmos agents to explore a goal using different strategies.
Each cosmos runs in its own git worktree. Agents write insights to
`.quantum/<name>/insights.jsonl` in real time and read each other's insights
between implementation steps — achieving live entanglement without external
infrastructure.

## Trigger

`/cosmos spawn --goal "<goal>" --strategies "<strategy1,strategy2,...>"`

## Execution Steps

### Step 1 — Parse arguments

From the user's trigger message, extract:
- `--goal` value → the shared objective
- `--strategies` value → comma-separated; split into a list

Assign cosmos names in order: `alpha`, `beta`, `gamma`, `delta`, `epsilon` (max 5).

Example: `--strategies "jwt,session,oauth2"` → alpha=jwt, beta=session, gamma=oauth2

### Step 2 — Detect repo root

Run:
```bash
git rev-parse --show-toplevel
```

Store the output as `<repo_root>`. All absolute paths below use this.

### Step 3 — Create quantum memory directories

For each cosmos `<name>`:

```bash
mkdir -p <repo_root>/.quantum/<name>
touch <repo_root>/.quantum/<name>/insights.jsonl
```

### Step 4 — Create git worktrees

For each cosmos `<name>`:

```bash
git worktree add <repo_root>/cosmos/<name> -B cosmos/<name>
```

If the branch already exists, append `--force`.

Verify with:
```bash
git worktree list
```

### Step 5 — Write CLAUDE.md into each worktree

For each cosmos `<name>` with strategy `<strategy>`, write the following to
`<repo_root>/cosmos/<name>/CLAUDE.md`:

~~~markdown
# cosmos:<name>

## Goal
<goal>

## Strategy
<strategy>

## Quantum Memory Rules

### Writing insights
After every significant decision or discovery (new file created, design decision
made, key pattern found, bug discovered), append one line to your insights file.

Your insights file (absolute path):
  <repo_root>/.quantum/<name>/insights.jsonl

Format — one JSON object per line:
{"content": "<insight text>", "ts": "<ISO 8601 timestamp e.g. 2026-05-12T12:00:00Z>"}

Use Bash append ONLY (never use the Write tool on this file — it overwrites):
```bash
echo '{"content": "...", "ts": "2026-05-12T12:00:00Z"}' >> <repo_root>/.quantum/<name>/insights.jsonl
```

### Entanglement (REQUIRED)
After EACH major implementation step, read all cosmos insight files:

  <repo_root>/.quantum/alpha/insights.jsonl   (skip if missing)
  <repo_root>/.quantum/beta/insights.jsonl    (skip if missing)
  <repo_root>/.quantum/gamma/insights.jsonl   (skip if missing)
  <repo_root>/.quantum/delta/insights.jsonl   (skip if missing)
  <repo_root>/.quantum/epsilon/insights.jsonl (skip if missing)

If another cosmos is converging on the same pattern → that is a Resonance signal.
Note it in your next insight. You may adopt it.

If another cosmos found a bug or edge case → read it carefully. Apply the fix if
it applies to your implementation too.

Decoherence warning: do NOT copy another cosmos's entire approach. Preserve your
core strategy. Entanglement means influence, not convergence.
~~~

### Step 6 — Dispatch parallel agents

In a SINGLE response, make N Agent tool calls — one per cosmos. All run in
true parallel. Do NOT await one before starting the next.

For each cosmos `<name>` with strategy `<strategy>`, dispatch this prompt:

```
You are cosmos:<name> in a Cosmos Vibe multiverse exploration.

Working directory: <repo_root>/cosmos/<name>
(This is a git worktree of the main repo.)

Goal: <goal>
Your strategy: <strategy>

━━━ QUANTUM MEMORY — follow these rules throughout ━━━

1. WRITE insights after every major step. Append to:
     <repo_root>/.quantum/<name>/insights.jsonl
   
   One JSON line per insight:
   {"content": "<insight>", "ts": "<ISO timestamp>"}
   
   Bash append only:
   echo '{"content": "...", "ts": "2026-05-12T12:00:00Z"}' >> <repo_root>/.quantum/<name>/insights.jsonl

2. READ all cosmos insights after each major step:
     <repo_root>/.quantum/alpha/insights.jsonl   (skip if missing)
     <repo_root>/.quantum/beta/insights.jsonl    (skip if missing)
     <repo_root>/.quantum/gamma/insights.jsonl   (skip if missing)
     <repo_root>/.quantum/delta/insights.jsonl   (skip if missing)
     <repo_root>/.quantum/epsilon/insights.jsonl (skip if missing)
   
   Resonance: if multiple cosmos independently reach the same conclusion — trust it.
   Decoherence: do not abandon your strategy to follow another cosmos. Influence only.

━━━ Now implement the goal using your strategy. Work autonomously until complete. ━━━
```

### Step 7 — Report launch status

Immediately before dispatching agents, output:

```
🌌 Spawning <N> cosmos...

  [alpha] cosmos/alpha  strategy: <strategy1>
  [beta]  cosmos/beta   strategy: <strategy2>
  [gamma] cosmos/gamma  strategy: <strategy3>

⚛️  Quantum Memory: .quantum/

Agents running. Superposition snapshot when complete.
```

### Step 8 — Auto-observe on completion

After all agents return, automatically run `/cosmos observe`.
