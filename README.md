# 🌌 Cosmos Vibe

> Parallel AI agents that observe, entangle, and explore — not compete.

A Claude Code plugin that applies quantum physics metaphors to AI-assisted development.
Instead of running isolated agents and picking a winner, Cosmos Vibe lets agents
**influence each other in real time** while preserving every strategy until you
deliberately collapse the superposition.

```
/cosmos spawn --goal "implement user auth" --strategies "jwt,session,oauth2"
```

Three agents start in parallel. Each builds its own solution. Each reads the others'
discoveries between every implementation step. The best ideas propagate. No strategy
is discarded until you choose.

---

## Concepts

| Quantum | Cosmos Vibe |
|---------|-------------|
| **Superposition** | N universes run simultaneously — no forced winner |
| **Entanglement** | Agents share a live insight stream; ideas propagate without merging |
| **Observation** | `/cosmos observe` — snapshot of all live universes |
| **Crystallization** | `/cosmos crystallize <id>` — extract one universe's result |

### Why not just run N isolated agents?

Isolated agents duplicate work and discard 90% of it. Cosmos Vibe agents are
*entangled*: if alpha discovers "sliding window expiry is safer than fixed TTL,"
gamma reads that at its next step and can adopt, adapt, or consciously reject it —
while staying on its own OAuth2 path. You get N explorations *and* cross-pollination.

---

## Install

```bash
claude plugins install https://github.com/hyuniiiv/cosmos-vibe
```

No Python. No ChromaDB. No subprocess. Pure markdown skills — Quantum Memory is
plain JSON Lines files on disk.

---

## Quick Start

```
/cosmos spawn --goal "implement user auth" --strategies "jwt,session,oauth2"
```

This creates three git worktrees (`universes/alpha`, `universes/beta`,
`universes/gamma`) and dispatches three parallel Claude agents. Each agent:

1. Implements the goal using its assigned strategy
2. Writes insights to `.quantum/<name>/insights.jsonl` after each step
3. Reads all `.quantum/*/insights.jsonl` before the next step — live entanglement

When all three complete:

```
/cosmos observe
```

```
🌌 Universe alpha  (12 insights)
   └ JWT sliding window expiry: 15m access / 7d refresh with rotation
   └ Chose RS256 over HS256 for key rotation support

🌌 Universe beta  (9 insights)
   └ Redis TTL 24h — simpler ops, no sliding window needed
   └ Session key: sess:<user_id>:<device_id> for multi-device support

🌌 Universe gamma  (14 insights)
   └ OAuth2 + PKCE — delegates trust to provider, no token storage
   └ Refresh token rotation copied from alpha — both now agree on 7d window

⚛️  Entanglements:
   alpha ↔ gamma  — both converging on sliding window token expiry
   beta  ↔ alpha  — beta adopted RS256 after reading alpha's key-rotation insight

Notable divergences:
   beta holds on Redis TTL 24h (simpler ops priority vs. alpha's security-first stance)
```

Pick the result you want:

```
/cosmos crystallize alpha   # extract alpha — optionally merge to current branch
/cosmos stop                # remove all worktrees and branches when done
```

---

## Commands

### `/cosmos spawn`

```
/cosmos spawn --goal "<goal>" --strategies "<s1,s2,...>"
```

Launches one universe per strategy. Universe names are assigned alphabetically
(alpha, beta, gamma, delta, ...). Each universe gets:

- An isolated git worktree at `universes/<name>`
- A dedicated branch `universe/<name>`
- A quantum memory file `.quantum/<name>/insights.jsonl`
- A `CLAUDE.md` containing its goal, strategy, and entanglement rules

Agents run in parallel via a single `Agent` tool dispatch. When all finish,
`/cosmos observe` runs automatically.

**Options**

| Flag | Description |
|------|-------------|
| `--goal` | The task every universe works toward |
| `--strategies` | Comma-separated list — one universe per strategy |

---

### `/cosmos observe`

Reads all `.quantum/*/insights.jsonl` files and outputs:

- A superposition snapshot (latest 2 insights per universe)
- Entanglement detections — pairs converging on the same decision
- Notable divergences — interesting strategic differences worth preserving

Entanglement detection uses Claude's semantic judgment. No vector database,
no cosine similarity threshold to tune.

---

### `/cosmos crystallize <id>`

Extracts a universe's result:

1. Reads its quantum memory and prints key decisions, trade-offs, and entanglement influences
2. Shows the last 10 commits and diff stats from its worktree
3. Asks whether to merge (`git merge universe/<id> --no-ff`) or keep the branch intact

Other universes are unaffected — the superposition remains until you explicitly stop.

```
/cosmos crystallize gamma
```

---

### `/cosmos stop`

Removes all universe worktrees and branches. Offers to wipe `.quantum/` (insights
are preserved by default so you can review them after the session).

```
/cosmos stop
```

---

## How entanglement works

The `Agent` tool runs subagents to completion in their own context window —
there is no mid-run hook injection. Instead, each agent prompt explicitly requires
the agent to **re-read `.quantum/*/insights.jsonl` between every major
implementation step**.

```bash
# Each agent runs this between steps:
for f in $(ls .quantum/*/insights.jsonl 2>/dev/null); do cat "$f"; done
```

```bash
# Each agent appends its own insights (never overwrites):
echo '{"content": "RS256 chosen for key rotation support", "ts": "2026-05-12T10:31:00Z"}' \
  >> .quantum/alpha/insights.jsonl
```

If alpha writes "sliding window expiry" at step 3, gamma reads it at step 4
and can adapt — while staying on its own OAuth2 path.

**Entanglement is influence, not convergence.** Universes are not forced to agree.
They can consciously reject each other's discoveries and record why.

---

## Quantum Memory

Location: `.quantum/` at the repo root (git-ignored).

```
.quantum/
  alpha/insights.jsonl
  beta/insights.jsonl
  gamma/insights.jsonl
```

Each line is a JSON object:

```json
{"content": "sliding window expiry safer than fixed TTL under load", "ts": "2026-05-12T10:31:00Z"}
```

- Each universe writes **only** to its own namespace
- All universes may **read** all namespaces
- Insights survive `/cosmos stop` by default — wipe manually or confirm during stop

---

## Cost

**N universes = N × Claude API cost.**

Quantum Memory reads and writes are local file I/O — no additional API calls.
`/cosmos observe` uses one Claude call to detect entanglements semantically.
`/cosmos crystallize` uses one Claude call to summarize decisions.

To reduce cost: start with 2 universes and add more only if the first pair
diverges interestingly.

---

## Universe rules

- Each universe works in its own git worktree — no shared working directory
- Do not copy code directly from another universe; let insights influence your design
- Record every significant discovery to `.quantum/<name>/insights.jsonl`
- After each major implementation step, read `.quantum/*/insights.jsonl`
- Entanglement means influence, not convergence — preserve your strategy

---

## Repository layout

```
skills/
  spawn/SKILL.md        — /cosmos spawn implementation
  observe/SKILL.md      — /cosmos observe implementation
  crystallize/SKILL.md  — /cosmos crystallize implementation
  stop/SKILL.md         — /cosmos stop implementation
.claude-plugin/
  plugin.json           — plugin manifest
universes/              — runtime git worktrees (git-ignored)
.quantum/               — runtime insight files (git-ignored)
```
