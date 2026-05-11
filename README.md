# 🌌 Cosmos Vibe

> Parallel AI agents that observe, entangle, and explore — not compete.

A Claude Code plugin implementing quantum-physics metaphors for AI development:
**superposition** (multiple solutions coexist), **entanglement** (agents influence
each other in real time), and **crystallization** (selective collapse).

## Install

```bash
claude plugins install <repo-url>
```

## Usage

```
/cosmos spawn --goal "implement user auth" --strategies "jwt,session,oauth2"
```

This creates 3 git worktrees (`universes/alpha`, `universes/beta`, `universes/gamma`)
and dispatches 3 parallel Claude agents. Each agent:

1. Implements the goal with its own strategy
2. Records insights to `.quantum/<name>/insights.jsonl` after each step
3. Reads all `.quantum/*/insights.jsonl` between steps — live entanglement

```
/cosmos observe
```

Shows the superposition snapshot:

```
🌌 Universe alpha  (12 insights)
   └ JWT sliding window expiry: 15m access, 7d refresh with rotation
   └ Chose RS256 for key rotation support

🌌 Universe beta  (9 insights)
   └ Redis TTL 24h — simpler but no sliding window
   └ Session key: sess:<user_id>:<device_id>

⚛️  Entanglements:
   alpha ↔ gamma  — both converging on sliding window expiry
```

```
/cosmos crystallize alpha   # extract alpha's result (merge optional)
/cosmos stop                # clean up all worktrees
```

## How entanglement works

The `Agent` tool runs subagents to completion in their own context — there's no
mid-run hook injection. Instead, each agent prompt explicitly instructs the agent
to **re-read `.quantum/*/insights.jsonl` between every major implementation step**.

If alpha writes "chose sliding window expiry" at step 3, gamma will read it at
step 4 and can adapt — while still maintaining its own OAuth2 strategy.

## No external dependencies

Pure markdown skills. No Python, no ChromaDB, no subprocess. Quantum Memory is
plain JSON Lines files. Resonance is Claude's semantic judgment.

## Cost

N universes = N × Claude API cost. All `.quantum/` reads/writes use local files.
