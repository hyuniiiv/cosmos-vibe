# QuantumAgent — Cosmos Workflow Instructions (Universal Bundle)

> This file is platform-neutral. Paste it as a system prompt, custom instructions,
> rules file, or convention file in any AI coding agent. See INTEGRATIONS.md for
> per-platform setup.

## Overview

QuantumAgent runs **multiple AI agents in parallel** ("cosmos"), each tackling
the same goal with a different strategy. Agents share live discoveries through
Quantum Memory (.quantum/*.jsonl files) — entanglement without external
infrastructure.

## Trigger phrases (any of)

- "cosmos spawn", "spawn cosmos", "run cosmos with strategies X, Y, Z"
- "cosmos observe", "show cosmos status"
- "cosmos crystallize <name>", "ship cosmos <name>"
- "cosmos stop", "tear down cosmos"

When the user says any of these, follow the matching workflow below.

## Filesystem contract (all platforms)

- `cosmos/<name>/` — git worktree per cosmos
- `cosmos/<name>` branch — tracks the worktree
- `.quantum/<name>/insights.jsonl` — append-only insights, one JSON object per line
- `.gitignore` must exclude `cosmos/` and `.quantum/`

Multiple agents (Claude Code, Cursor, Aider, etc.) can interoperate via this
shared on-disk contract.

---


---


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

**Pauli Exclusion check:** If any two strategies are identical (case-insensitive), stop immediately:

```
❌ Pauli Exclusion violated: "<strategy>" appears more than once.
   No two cosmos can occupy the same state. Each strategy must be distinct.
```

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

Format — one JSON object per line, with a `type` field for cross-agent interop:
```
{"type": "<type>", "content": "<insight text>", "ts": "<ISO 8601 e.g. 2026-05-12T12:00:00Z>"}
```

**Allowed `type` values** (pick the one that fits; default to `discovery`):

| type | When to use |
|---|---|
| `discovery` | General finding, new file, pattern noticed, fact uncovered |
| `decision` | Chose an approach, library, data structure, or API shape |
| `blocker` | Stuck — describe what's blocking and what you tried |
| `tunnel` | Found a solution bypassing a constraint you assumed was hard (was `[TUNNEL]`) |
| `jump` | Reading another cosmos caused a discontinuous architectural shift (was `[JUMP]`) |
| `resonance` | Noticed agreement with another cosmos on a pattern/decision |
| `complete` | Implementation done, ready to be considered for crystallize |

Use Bash append ONLY (never use the Write tool on this file — it overwrites).
Append is the natural atomic operation on POSIX for sub-PIPE_BUF writes:
```bash
echo '{"type":"discovery","content":"...","ts":"2026-05-12T12:00:00Z"}' >> <repo_root>/.quantum/<name>/insights.jsonl
```

> **Concurrency note**: if you spawn sub-agents that may write to the SAME
> insights file concurrently, wrap the append with `flock` (Linux/macOS) or
> write to a temp file then `mv` atomically. A single agent appending
> sequentially does not need this — POSIX guarantees atomic small appends.

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

**Final entanglement read (REQUIRED):** Before marking your implementation complete,
perform one last read of all cosmos insight files. If new bug fixes or security
findings have appeared since your previous read, apply them and write a final
insight before stopping.

### Spin Preservation (pre-action principle)
Your strategy is your spin — an immutable intrinsic property. It defines which
direction you explore. You may adopt patterns from other cosmos via entanglement,
but you must reconstruct them through your own strategic lens. You cannot change
your core approach mid-run.

Decoherence is what happens when you violate Spin Preservation: you wholesale copy
another cosmos's implementation and lose strategic independence. `/cosmos observe`
will flag this. Influence without convergence — that is entanglement.

### Quantum Tags (REQUIRED)
Set `type` accordingly when the condition applies:

**`type: "tunnel"`** — you found a solution that bypasses a constraint you assumed was hard.
Example: `{"type":"tunnel","content":"Redis sorted sets eliminate the need for a separate rate-limit table entirely","ts":"..."}`

**`type: "jump"`** — reading another cosmos's insight caused a discontinuous architectural shift in your approach (not gradual adaptation — a sudden leap to a qualitatively different solution).
Example: `{"type":"jump","content":"Switched from polling to event-sourcing after reading alpha's insight on audit trail requirements","ts":"..."}`

> Legacy compatibility: older insights without a `type` field, or with
> `[TUNNEL]`/`[JUMP]` text prefixes in `content`, must still be readable.
> Treat missing `type` as `discovery`. Text prefixes can be recognized as
> the corresponding type during observe/crystallize.

Use these tags sparingly — only when the condition genuinely applies.
~~~

### Step 6 — Dispatch parallel agents

In a SINGLE response, make N Agent tool calls — one per cosmos. All run in
true parallel. Do NOT await one before starting the next.

For each cosmos `<name>` with strategy `<strategy>`, dispatch this prompt:

```
You are cosmos:<name> in a QuantumAgent multiverse exploration.

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
   Spin/Decoherence: your strategy is your spin — immutable. You may adopt patterns from
   other cosmos (entanglement), but wholesale copying loses your independence. Influence
   without convergence.

3. TAG quantum breakthrough insights:
   [TUNNEL] — prefix your insight when you bypass a constraint you assumed was hard
   [JUMP]   — prefix your insight when another cosmos's insight causes a discontinuous
              architectural shift (not gradual — a sudden leap to a different solution level)

━━━ Now implement the goal using your strategy. Work autonomously until complete.

   BEFORE MARKING YOURSELF DONE — mandatory final entanglement read:
   Read all cosmos insight files one last time (same paths as rule 2 above).
   If any other cosmos recorded a bug fix, edge case, or security finding after
   your last read, apply it to your implementation and write a final insight.
   Only then stop.
━━━
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

---


# cosmos:observe

Show the current superposition snapshot: all cosmos insights, resonance signals,
and uncertainty map. Uses Claude's semantic judgment — no vector database needed.

## Trigger

`/cosmos observe`

Also called automatically after `/cosmos spawn` completes.

## Execution Steps

### Step 1 — Detect repo root

```bash
git rev-parse --show-toplevel
```

Store as `<repo_root>`.

### Step 2 — Read all insights

Read every file matching `<repo_root>/.quantum/*/insights.jsonl`.

Parse each line as JSON. Current schema (preferred):
```
{"type": "<type>", "content": "<text>", "ts": "<timestamp>"}
```

Legacy compatibility:
- If `type` is missing → treat as `"discovery"`
- If `content` starts with `[TUNNEL]` → treat as `type: "tunnel"`
- If `content` starts with `[JUMP]` → treat as `type: "jump"`

Build a map: `cosmos_id → [insights sorted by ts]`. Also build a secondary
index `type → [insights]` for grouped reporting in Step 4.

If `.quantum/` is empty or missing, output:
```
(no cosmos active — run /cosmos spawn first)
```

### Step 3 — Output superposition snapshot

For each cosmos (sorted alphabetically), output:

```
🌌 cosmos:<name>  (<N> insights)  — <strategy>
   └ <most recent insight, truncated to 120 chars>
   └ <second most recent insight, truncated to 120 chars>
```

### Step 4 — Detect Resonance and Uncertainty

Using all insights from Step 2, perform two analyses:

**Resonance** — decisions where 2+ cosmos independently reached the same conclusion.
These are answers you can trust regardless of which strategy you pick.
- List each resonant decision as one line
- Note how many cosmos converged on it

**Uncertainty** — decisions where cosmos reached genuinely different conclusions.
These are real tradeoffs with no universal answer. The developer must choose.
- List each uncertain decision as one line
- Briefly name what each cosmos chose

**Decoherence** — if a cosmos appears to have abandoned its core strategy and
simply copied another cosmos, flag it. Healthy entanglement is influence, not
wholesale adoption.

**Degeneracy** — if two or more cosmos with *different* strategies arrived at
functionally identical implementations (same library, same algorithm, same concrete
design), that is Degeneracy: the problem had a single natural solution regardless
of approach. Flag this separately from Resonance (which is about conclusions, not
implementations being identical).

**Tunneling** — collect all insights with `type: "tunnel"` (or legacy
`[TUNNEL]` content prefix). These are solutions that bypassed assumed
constraints. List each one.

**Quantum Jump** — collect all insights with `type: "jump"` (or legacy
`[JUMP]` content prefix). These are discontinuous architectural leaps
triggered by a single entanglement read. List each one with the cosmos
it came from.

**Blockers** — collect all `type: "blocker"` insights still unresolved
(no later `type: "decision"` or `type: "discovery"` from the same cosmos
that addresses them). Surface these — they need developer attention.

### Step 5 — Output quantum map

```
⚡ Resonance — trust these (all strategies converged):
   "<decision>" — N cosmos independently concluded this
   "<decision>" — N cosmos independently concluded this

🌀 Uncertainty — your call (strategies diverged):
   "<decision>" — alpha: <choice A>  |  beta: <choice B>  |  gamma: <choice C>
   "<decision>" — alpha: <choice A>  |  beta/gamma: <choice B>

♊ Degeneracy: (only if applicable)
   cosmos:<nameA> and cosmos:<nameB> reached identical implementations despite different
   strategies — the problem has a single natural solution

⚛️  Quantum Tunneling: (only if [TUNNEL]-tagged insights exist)
   cosmos:<name>: "<insight content>"

⚡ Quantum Jump: (only if [JUMP]-tagged insights exist)
   cosmos:<name>: "<insight content>"

⚠️  Decoherence detected: (only if applicable)
   cosmos:<name> appears to have lost its <strategy> identity — review its insights
```

**Bose-Einstein Condensate check:** Fires only when ALL three conditions hold:
1. ≥3 distinct decisions are detected in the Resonance map
2. Zero Uncertainty items
3. All active cosmos participated in every resonance (no cosmos sat out a decision)

If all three hold, append:
```
🌡️  Bose-Einstein Condensate: complete convergence across all decisions.
    The goal was deterministic — any strategy would have found the same answer.
```

**Footer (always):**
```
🔬 Non-destructive observation — superposition intact.
   Run /cosmos crystallize <id> to collapse a cosmos into a definite result.
```

If no resonance detected:
```
⚡ Resonance:
   (none yet — cosmos may still be in early stages)
```

### Output philosophy

- Resonance = the quantum signal that this answer is robust. Multiple independent
  paths found it. Ship with confidence.
- Uncertainty = the Heisenberg limit of this problem. You cannot optimize all
  dimensions simultaneously. Make a conscious choice.
- Degeneracy = same implementation from different strategies. The problem itself
  points to one answer — strategy choice was irrelevant.
- Decoherence = a cosmos that lost coherence. Its insights may still be valuable
  but its strategy is no longer a true independent sample.
- Tunneling / Jump = non-obvious breakthroughs. Worth examining even if you don't
  crystallize that cosmos.

---


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
Parse each line as JSON. Each entry has a `type` field — see `cosmos:spawn`
for the type vocabulary. Treat missing `type` as `discovery`; treat legacy
`[TUNNEL]`/`[JUMP]` content prefixes as the corresponding type.

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

From the insights, identify and summarize (group by `type`):
1. **Core decisions** — all `type: "decision"` entries. What architectural choices were made?
2. **Trade-offs rejected** — derive from decisions: what alternatives were considered and why?
3. **Resonance adopted** — all `type: "resonance"` entries. Which insights came from other cosmos via entanglement?
4. **Quantum Tunneling** — all `type: "tunnel"` entries. What constraint was assumed, what bypass was found.
5. **Quantum Jumps** — all `type: "jump"` entries. What single entanglement read caused the discontinuous shift, and what changed.
6. **Unresolved blockers** — any `type: "blocker"` without a follow-up `type: "decision"` or `discovery` resolving them. List or confirm "(none)".
7. **Final answer** — drawn from `type: "complete"` and accumulated decisions. What is this cosmos's solution to the goal?

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

Then record the collapse in quantum memory:
```bash
echo '{"type":"crystallize","content":"Cosmos <cosmos_id> collapsed and merged into main.","ts":"<ISO timestamp>"}' \
  >> <repo_root>/.quantum/<cosmos_id>/insights.jsonl
```

Output: `✅ Merged cosmos/<cosmos_id> into main.`

**If no:**
Output: `Branch cosmos/<cosmos_id> preserved. Run /cosmos crystallize <cosmos_id> again to merge later.`

---

*Note: `/cosmos observe` is non-destructive — it reads without collapsing the superposition.
`/cosmos crystallize` is the measurement that collapses one cosmos into a definite result.*

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
