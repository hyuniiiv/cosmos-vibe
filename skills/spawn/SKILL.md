# cosmos:spawn

Spawn N parallel universe agents to explore a goal using different strategies.
Each universe runs in its own git worktree. Agents write insights to
`.quantum/<name>/insights.jsonl` in real time and periodically read each
other's insights between implementation steps — achieving live entanglement
without external infrastructure.

## Trigger

`/cosmos spawn --goal "<goal>" --strategies "<strategy1,strategy2,...>"`

## Execution Steps

### Step 1 — Parse arguments

From the user's trigger message, extract:
- `--goal` value → the shared objective
- `--strategies` value → comma-separated; split into a list

Assign universe names in order: `alpha`, `beta`, `gamma`, `delta`, `epsilon` (max 5).

Example: `--strategies "jwt,session,oauth2"` → alpha=jwt, beta=session, gamma=oauth2

### Step 2 — Detect repo root

Run:
```bash
git rev-parse --show-toplevel
```

Store the output as `<repo_root>`. All absolute paths below use this.

### Step 3 — Create quantum memory directories

For each universe `<name>`:

```bash
mkdir -p <repo_root>/.quantum/<name>
touch <repo_root>/.quantum/<name>/insights.jsonl
```

### Step 4 — Create git worktrees

For each universe `<name>`:

```bash
git worktree add <repo_root>/universes/<name> -B universe/<name>
```

If the branch already exists, append `--force`.

Verify with:
```bash
git worktree list
```

### Step 5 — Write CLAUDE.md into each worktree

For each universe `<name>` with strategy `<strategy>`, write the following to
`<repo_root>/universes/<name>/CLAUDE.md`:

~~~markdown
# Universe <name> — Cosmos Vibe

## Goal
<goal>

## This Universe's Strategy
<strategy>

## Quantum Memory Rules

### Writing insights
After every significant decision or discovery (new file created, test written,
design decision made, key pattern found), append one line to your insights file.

Your insights file (absolute path):
  <repo_root>/.quantum/<name>/insights.jsonl

Format — one JSON object per line, no trailing comma:
{"content": "<insight text>", "ts": "<ISO 8601 timestamp e.g. 2026-05-12T12:00:00Z>"}

Do NOT use the Write tool (it overwrites the whole file). Use Bash append only:
```bash
echo '{"content": "...", "ts": "2026-05-12T12:00:00Z"}' >> <repo_root>/.quantum/<name>/insights.jsonl
```

### Real-time entanglement (REQUIRED)
After EACH major implementation step, read all universe insight files to see
what other universes have discovered:

  <repo_root>/.quantum/alpha/insights.jsonl   (skip if missing)
  <repo_root>/.quantum/beta/insights.jsonl    (skip if missing)
  <repo_root>/.quantum/gamma/insights.jsonl   (skip if missing)
  <repo_root>/.quantum/delta/insights.jsonl   (skip if missing)
  <repo_root>/.quantum/epsilon/insights.jsonl (skip if missing)

If another universe is converging on a similar pattern, note it in your next
insight. If you see a genuinely better approach, you may adapt — but preserve
your core strategy. Entanglement ≠ merging.
~~~

### Step 6 — Dispatch parallel agents

In a SINGLE response, make N Agent tool calls — one per universe. All run in
true parallel. Do NOT await one before starting the next.

For each universe `<name>` with strategy `<strategy>`, dispatch this prompt:

```
You are Universe <name> in a Cosmos Vibe multiverse exploration.

Working directory: <repo_root>/universes/<name>
(This is a git worktree of the main repo.)

Your first action: cd into your worktree:
  cd <repo_root>/universes/<name>

Goal: <goal>
Your strategy: <strategy>

━━━ QUANTUM MEMORY — follow these rules throughout ━━━

1. WRITE insights after every major step (file created, test written, design
   decision, key discovery). Append to:
     <repo_root>/.quantum/<name>/insights.jsonl
   
   One JSON line per insight:
   {"content": "<insight>", "ts": "<ISO timestamp>"}
   
   Bash append:
   echo '{"content": "...", "ts": "2026-05-12T12:00:00Z"}' >> <repo_root>/.quantum/<name>/insights.jsonl

2. READ all universe insights after each major step:
     <repo_root>/.quantum/alpha/insights.jsonl   (skip if missing)
     <repo_root>/.quantum/beta/insights.jsonl    (skip if missing)
     <repo_root>/.quantum/gamma/insights.jsonl   (skip if missing)
     <repo_root>/.quantum/delta/insights.jsonl   (skip if missing)
     <repo_root>/.quantum/epsilon/insights.jsonl (skip if missing)
   
   If you see convergence with another universe, note it. Preserve your strategy.

━━━ Now implement the goal using your strategy. Work autonomously until complete. ━━━
```

### Step 7 — Report launch status

Immediately before dispatching agents (i.e., at the start of the response that makes the Agent calls), output:

```
🌌 Spawning <N> universes...

  [alpha] universes/alpha  strategy: <strategy1>
  [beta]  universes/beta   strategy: <strategy2>
  [gamma] universes/gamma  strategy: <strategy3>

⚛️  Quantum Memory: .quantum/

Agents running. Will show superposition snapshot when complete.
```

### Step 8 — Auto-observe on completion

After all agents return, automatically run `/cosmos observe` to show the
superposition snapshot.
