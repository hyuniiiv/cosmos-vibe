# 🌌 QuantumAgent

> Before you commit to one approach, explore three in parallel.
>
> *Parallel cosmos exploration harness for Claude Code.*

A Claude Code plugin that runs multiple AI agents simultaneously — each tackling
the same goal with a different strategy. Agents share discoveries in real time
through Quantum Memory. When they independently reach the same conclusion, that's
your signal to trust it. When they diverge, that's your actual tradeoff made visible.

```
/cosmos spawn --goal "implement user auth" --strategies "jwt,session,oauth2"
```

---

## What you get

A typical 30-minute run produces:

- **4–8 Resonance decisions** you can ship without second-guessing — multiple independent implementations agreed
- **2–4 Uncertainty decisions** made explicit — you now know the real tradeoff and can choose deliberately
- **Working code in N branches** — not a theoretical comparison but actual implementations that found real bugs
- **[TUNNEL] / [JUMP] breakthroughs** — solutions that wouldn't emerge from a single sequential agent

The signal-to-noise is high because the findings come from *doing*, not theorizing. Bugs surface during implementation, not after deployment.

---

## The problem

You're building something with Claude Code. Claude implements one approach. You
ship it. Three weeks later you're refactoring because the architecture didn't scale,
you discover a security edge case, or you realize a different approach would have
been cleaner.

The problem isn't Claude — it's that a single agent exploring a single path cannot
tell you what it didn't explore.

**QuantumAgent runs the exploration before you commit.** Not as a theoretical
comparison — as actual working implementations that discover real issues in real code.

---

## How it works

```
Your goal (pure potential — the wave)
         │
         ▼
 /cosmos spawn --strategies "A,B,C"
         │
    ┌────┴──────────────────────────────────────┐
    │                                           │
    ▼               ▼                           ▼
cosmos:alpha    cosmos:beta               cosmos:gamma
strategy A      strategy B                strategy C
    │               │                           │
    │   reads ◄─────┤──────────────────────► reads
    │               │           ↑               │
    ▼               ▼     .quantum/             ▼
 writes ──────────► * ◄────────────────── writes
    │               │                           │
    └────────────────────────────────────────────┘
         │
         ▼
 /cosmos observe
         │
         ├── ⚡ Resonance  — all strategies independently agreed → ship it
         ├── 🌀 Uncertainty — strategies genuinely diverged → you choose
         ├── ⚛️  Tunneling  — assumed-hard constraint bypassed → examine it
         └── ⚡ Jump        — single insight caused discontinuous leap → trace it
         │
         ▼
 /cosmos crystallize <id>   →   Schrödinger check → merge or keep
 /cosmos stop               →   clean up all worktrees
```

The key: agents don't just share conclusions — they share **discoveries in real time**.
If cosmos:gamma finds a security bug at step 7, cosmos:alpha reads it before step 8
and applies the same fix, all while staying on its own strategy. That's entanglement:
influence without convergence.

---

## Install

QuantumAgent ships as a self-marketplace Claude Code plugin. Inside Claude Code:

```
/plugin marketplace add hyuniiiv/quantum-agent
/plugin install cosmos@quantum-agent
/reload-plugins
```

After install, the `/cosmos` slash commands are available immediately.

No Python. No vector database. No subprocess. Pure markdown skills.
Quantum Memory is plain JSON Lines files on disk.

### Use in other AI agents

QuantumAgent's core is platform-neutral markdown + bash. It runs in **10+ environments** beyond Claude Code:

| Environment | Mechanism |
|---|---|
| Claude Code | Native plugin (above) |
| Cursor | `.cursor/rules/cosmos.mdc` |
| Windsurf | `.windsurfrules` |
| Cline / Roo Code | Custom Instructions or MCP |
| Continue.dev | `config.json` system message |
| Aider | `CONVENTIONS.md` via `--read` |
| OpenAI Codex CLI | `--prompt-file` |
| GitHub Copilot | `.github/copilot-instructions.md` |
| Zed AI | Assistant custom prompt |
| Claude Desktop / claude.ai | MCP server (`@hyuniiiv/quantum-agent-mcp`) |

The same `.quantum/` memory works across agents — spawn in Cursor, observe in Claude Code, crystallize in Aider. See **[INTEGRATIONS.md](INTEGRATIONS.md)** for per-platform setup and the universal **[`bundle/cosmos-instructions.md`](bundle/cosmos-instructions.md)** drop-in file.

#### Non-LLM CLI

For scripted environments without any AI agent, use the deterministic CLI:

```bash
npx -y @hyuniiiv/quantum-agent-cli init alpha
npx -y @hyuniiiv/quantum-agent-cli insight alpha "discovery text"
npx -y @hyuniiiv/quantum-agent-cli observe
npx -y @hyuniiiv/quantum-agent-cli stop --purge
```

The CLI manages worktrees and `.quantum/` memory directly. Pair it with any LLM agent that follows the same filesystem contract. Verified by 16-check conformance suite (`tests/conformance.sh`).

### Troubleshooting

**`git@github.com: Permission denied (publickey)` during install**

Claude Code clones the plugin over SSH by default. If you don't have a GitHub SSH key set up, rewrite SSH URLs to HTTPS for github.com:

```bash
git config --global url."https://github.com/".insteadOf git@github.com:
```

Then retry `/plugin install quantum-agent@quantum-agent`.

Alternatives:
- `gh auth login` → `gh auth setup-git` (uses HTTPS + credential helper)
- Add an SSH key: `ssh-keygen -t ed25519 -C "you@example.com"` and register the public key in GitHub → Settings → SSH Keys

---

## Quick start

```
/cosmos spawn --goal "implement rate limiting middleware" --strategies "token-bucket,sliding-window,fixed-window"
```

Three cosmos start in parallel. Each builds a working implementation.
Each reads the others' insights between every major step.

```
/cosmos observe
```

```
🌌 cosmos:alpha  (8 insights)  — token-bucket
   └ Redis HINCRBY for atomic counter update — avoids race condition under concurrent load
   └ Burst allowance: 2× rate for first 3s of a new window — documented as intentional

🌌 cosmos:beta   (7 insights)  — sliding-window
   └ Sliding log stored as Redis sorted set (score = timestamp)
   └ ZREMRANGEBYSCORE + ZCARD in a pipeline — single round trip regardless of log size

🌌 cosmos:gamma  (9 insights)  — fixed-window
   └ Fixed window boundary edge case: 2× burst possible — documented, not patched (by design)
   └ INCR + EXPIRE in Lua script for atomicity — prevents TOCTOU between the two operations

⚡ Resonance — trust these (all 3 strategies converged):
   "Redis Lua script or pipeline for atomicity" — all 3 cosmos found this independently
   "429 Too Many Requests + Retry-After header" — all 3 cosmos converged on this
   "X-RateLimit-Limit, X-RateLimit-Remaining, X-RateLimit-Reset headers" — 3/3 agree

🌀 Uncertainty — your call (strategies genuinely diverged):
   "burst handling"   — alpha: explicit 2× burst allowance  |  gamma: documented edge case only
   "memory per user"  — beta: O(requests) sliding log        |  alpha/gamma: O(1) counter

🔬 Non-destructive observation — superposition intact.
   Run /cosmos crystallize <id> to collapse a cosmos into a definite result.
```

Pick the result you want:

```
/cosmos crystallize beta    # extract beta — Schrödinger check, then optional merge
/cosmos stop                # clean up all worktrees and branches
```

---

## Full walkthrough: JWT authentication

A real run. Three strategies, 30 insights, one critical security bug caught.

### Spawn

```
/cosmos spawn --goal "implement JWT user authentication" \
  --strategies "jwt-stateless,rs256-keyrotation,hs256-refresh"
```

```
🌌 Spawning 3 cosmos...

  [alpha] cosmos/alpha  strategy: jwt-stateless
  [beta]  cosmos/beta   strategy: rs256-keyrotation
  [gamma] cosmos/gamma  strategy: hs256-refresh

⚛️  Quantum Memory: .quantum/

Agents running. Superposition snapshot when complete.
```

### Observe

```
🌌 cosmos:alpha  (10 insights)  — jwt-stateless
   └ JWT payload sub+email only; algorithms: [HS256] explicit — blocks algorithm confusion attacks
   └ User enumeration: dummy bcrypt.compare even on unknown users — constant ~250ms response time

🌌 cosmos:beta   (9 insights)   — rs256-keyrotation
   └ RS256 2048-bit over 4096-bit: doubles signing latency for negligible gain on 15-min tokens
   └ kid header = SHA-256(public key, first 16 hex) — key rotation without DB migration

🌌 cosmos:gamma  (11 insights)  — hs256-refresh
   └ Refresh token family revocation: stolen token detected → entire family invalidated immediately
   └ [BUG] Dummy hash was malformed literal — bcrypt.compare threw in <1ms, defeating anti-enumeration

⚡ Resonance — trust these (all 3 strategies converged):
   "15-minute access token expiry" — all 3 cosmos independently arrived here
   "{ error: { code: string, message: string } } response envelope" — all 3 converged
   "TOKEN_EXPIRED as distinct code from INVALID_TOKEN" — all 3 cosmos adopted this
   "constant-time bcrypt path even for unknown users (anti-enumeration)" — all 3 independently built this

🌀 Uncertainty — your call (strategies genuinely diverged):
   "signing algorithm"  — alpha/gamma: HS256 (simpler, single-server)  |  beta: RS256 (key rotation ready)
   "bcrypt cost factor" — alpha/gamma: rounds=12 (~250ms, security-first) |  beta: rounds=10 (NIST baseline, ~100ms)
   "refresh tokens"     — gamma: 7-day refresh + family revocation         |  alpha/beta: stateless only

🔬 Non-destructive observation — superposition intact.
   Run /cosmos crystallize <id> to collapse a cosmos into a definite result.
```

### What this tells you

**Ship these without debate** — Resonance confirmed all four:

| Decision | Why trust it |
|----------|-------------|
| 15-minute access tokens | jwt-stateless, rs256-keyrotation, and hs256-refresh all landed here independently via different reasoning |
| `{ error: { code, message } }` format | Identical shape across all three cosmos — zero negotiation needed |
| `TOKEN_EXPIRED` ≠ `INVALID_TOKEN` | Client-side UX depends on this distinction — all cosmos independently recognized this |
| Constant-time login for unknown users | All three implemented it — and gamma found a real bug others missed |

**Make a conscious call on each Uncertainty:**

- **Algorithm** — Single server or internal API only? HS256. Multiple independent services need to verify tokens, or key rotation is a near-term requirement? RS256.
- **bcrypt rounds** — Low-spec deployment hardware or demo usability matters? rounds=10. Production security-first? rounds=12. Both are correct; pick based on your constraints.
- **Refresh tokens** — User-facing app where session persistence matters? Gamma's 7-day refresh with family revocation. Internal API where simplicity beats UX? Stateless.

**The critical catch:** cosmos:gamma discovered that the standard dummy-hash anti-enumeration pattern was *silently broken* — a malformed literal string caused bcrypt to throw immediately in under 1ms, completely defeating the timing protection. This is the class of bug that shows up in security audits eighteen months after shipping. All three cosmos had the same vulnerable pattern; gamma caught it during smoke testing.

Without QuantumAgent: three separate implementations, each written once, none cross-reviewed. The bug ships.

### Crystallize

```
/cosmos crystallize gamma
```

```
💎 cosmos:gamma — Crystallization
════════════════════════════════════════

Strategy: hs256-refresh
Insights: 11
Branch: cosmos/gamma

Core Decisions:
  1. Two separate JWT secrets (JWT_ACCESS_SECRET / JWT_REFRESH_SECRET) — cross-type
     token confusion impossible even if type claim check were bypassed
  2. Refresh token rotation with familyId (UUID per login) — token reuse triggers
     full family revocation, which is the correct threat model for token theft
  3. Token store keyed by jti (UUID), not raw token string — O(1) lookup, no
     timing-sensitive string comparison
  4. bcrypt rounds=12 + precomputed DUMMY_HASH at module load — constant ~250ms
     for all login paths including unknown emails (verified: 227ms in smoke test)

Trade-offs Rejected:
  - RS256 → rejected: key-pair management overhead unjustified for single-server deployment
  - Single JWT secret → rejected: allows refresh tokens to be used as access tokens
  - Inline dummy hash literal → rejected: bcrypt.compare throws immediately on malformed input

Resonance Adopted (from other cosmos via entanglement):
  - TOKEN_EXPIRED distinct from INVALID_TOKEN (adopted from alpha's insight)
  - { error: { code, message } } shape (confirmed by all cosmos — zero divergence)

Quantum Tunneling: none
Quantum Jumps: none

Final Answer:
  Full JWT auth with access tokens (15min HS256) + refresh tokens (7-day) with
  family-based revocation. Constant-time login path verified at 227ms for unknown
  emails. Helmet middleware for HTTP security headers. 9/9 smoke tests pass,
  including token reuse attack and sibling family revocation scenarios.

🐱 Schrödinger's Cat collapses on crystallization — quality is now definite, not potential.
   Have you run your test suite against cosmos/gamma?

   - yes, tests pass — proceed to merge
   - yes, tests failed — do not merge; fix in the cosmos branch, then re-crystallize
   - no, not yet — run tests first; come back when ready
```

---

## Commands

### `/cosmos spawn`

```
/cosmos spawn --goal "<goal>" --strategies "<s1,s2,...>"
```

Launches one cosmos per strategy. Names assigned alphabetically: `alpha`, `beta`,
`gamma`, `delta`, `epsilon` (max 5). Each cosmos gets:

- An isolated git worktree at `cosmos/<name>`
- A dedicated branch `cosmos/<name>`
- A quantum memory file `.quantum/<name>/insights.jsonl`
- A `CLAUDE.md` with goal, strategy, entanglement rules, and quantum tag instructions

**Pauli Exclusion check:** Duplicate strategies are rejected immediately.

```
❌ Pauli Exclusion violated: "jwt" appears more than once.
   No two cosmos can occupy the same state. Each strategy must be distinct.
```

Agents run in parallel. When all finish, `/cosmos observe` runs automatically.

| Flag | Description |
|------|-------------|
| `--goal` | The task every cosmos works toward |
| `--strategies` | Comma-separated list — one cosmos per strategy |

---

### `/cosmos observe`

Reads all `.quantum/*/insights.jsonl` and outputs:

- Superposition snapshot (latest 2 insights per cosmos)
- **Resonance map** — decisions every strategy independently converged on
- **Uncertainty map** — decisions where strategies genuinely diverged
- **Degeneracy** — if different strategies reached functionally identical implementations
- **[TUNNEL] report** — constraints that were bypassed
- **[JUMP] report** — discontinuous architectural leaps
- **Decoherence warning** — if a cosmos lost its strategic identity
- **BEC** — if all cosmos converged on all decisions with zero uncertainty

Non-destructive: superposition stays intact. Run as many times as you want while agents work.

---

### `/cosmos crystallize <id>`

Collapses one cosmos into a standalone result:

1. Reads insights — identifies core decisions, rejected alternatives, Resonance adopted, [TUNNEL] / [JUMP] events
2. Shows last 10 commits and diff stats from the worktree branch
3. **Schrödinger check** — forces confirmation that tests pass before offering merge
4. Offers to merge (`git merge cosmos/<id> --no-ff`) or preserve the branch

Other cosmos are unaffected. Superposition holds for remaining cosmos until `/cosmos stop`.

---

### `/cosmos stop`

Removes all cosmos worktrees and branches. Offers to wipe `.quantum/`
(insights are preserved by default — you may want them for retrospectives).

---

## Reading the signals

### ⚡ Resonance

Multiple cosmos independently reached the same conclusion.

**What to do:** Ship it without debate. The interference pattern is constructive — multiple
paths through the solution space all arrived here. This is the point of the system.

**Strength signal:** All N cosmos participated, and they arrived via genuinely different
paths (different libraries, different reasoning chains, different constraints). A 3/3
Resonance is much stronger than 2/3.

**When to be skeptical:** Resonance on trivial decisions ("use a try/catch", "validate
inputs") is noise. Resonance on decisions with long-lived architectural consequences
(token expiry strategy, error format contract, consistency model) is the signal you're
paying for.

---

### 🌀 Uncertainty

Strategies reached genuinely different conclusions.

**What to do:** Make a conscious choice — not a random one. You now know the exact
tradeoff: alpha chose HS256 for operational simplicity, beta chose RS256 for
future key rotation. Read both positions and pick based on your actual constraints.

**This is not a failure state.** Uncertainty is valuable output. A problem with zero
Uncertainty either has a deterministic answer (BEC) or your strategies weren't distinct
enough. Real architectural decisions almost always have genuine Uncertainty.

**How to use it:** For each Uncertainty item, ask: "Which cosmos's constraints match
my actual deployment context?" That's your answer.

---

### ⚛️ Quantum Tunneling `[TUNNEL]`

A cosmos bypassed a constraint you assumed was hard — going through the wall
instead of over it.

**What to do:** Read it carefully even if you're not crystallizing that cosmos.
Tunneling insights often look like "we don't need X at all" — eliminating an assumed
requirement rather than implementing it more cleverly.

**Example:** `[TUNNEL] Redis sorted sets eliminate the need for a separate rate-limit
table entirely` — the table you were about to design just isn't necessary.

---

### ⚡ Quantum Jump `[JUMP]`

A cosmos read another's insight and made a discontinuous architectural shift —
not a gradual adaptation but a sudden leap to a qualitatively different solution.

**What to do:** Trace the jump. Find which insight triggered it and what changed.
Jumps often contain the most non-obvious solutions in the run — the kind that require
reading someone else's constraint to realize your own assumed constraint doesn't exist.

---

### ♊ Degeneracy

Different strategies produced functionally identical implementations.

**What to do:** Pick any cosmos — the problem has a single natural solution. The
constraints are strong enough that all strategies converged on the same design.

**Distinction from Resonance:** Resonance = same conclusion reached independently.
Degeneracy = same *implementation* despite different strategies. Degeneracy is the
stronger signal.

---

### 🌡️ Bose-Einstein Condensate

Complete convergence: ≥3 resonant decisions, zero uncertainty, all cosmos
participated in every resonance item.

**What to do:** The goal was deterministic — the constraints left only one answer.
Crystallize any cosmos; they're equivalent. The problem had a right answer all along.

**When it fires:** Rare. Strongly constrained problems where hard requirements
(strict compliance, hard performance ceiling, immovable API contract) eliminate
all architectural freedom. High BEC rate on a domain means it's a mature, well-solved space.

---

### ⚠️ Decoherence

A cosmos abandoned its strategy and copied another wholesale.

**What to do:** Treat it as a compromised sample. Its insights are still readable,
but it's no longer an independent data point. Resonance/Uncertainty analysis
becomes less reliable when a decoherent cosmos is included.

**How it happens:** An agent reads another cosmos's implementation and reconstructs
it wholesale instead of adapting the pattern through its own strategic lens.
Healthy entanglement = "I adopted the Redis pipeline optimization into my sliding-window
implementation." Decoherence = "I switched to token-bucket after reading alpha."

The Spin Preservation rule in each cosmos's `CLAUDE.md` is designed to prevent this.
`/cosmos observe` will flag it if it happens.

---

## Designing good strategies

Strategies are the slits in Young's double-slit experiment. Their job is to force
genuinely different paths through the same solution space. Poor strategies produce
trivial Resonance and absent Uncertainty — the system runs but learns nothing.

### Stay at the same level of abstraction

```
✅ Good: "token-bucket,sliding-window,fixed-window"   (all: rate limiting algorithms)
✅ Good: "jwt-stateless,session-redis,oauth2-pkce"    (all: auth mechanisms)
❌ Bad:  "add-caching,refactor-database,jwt"          (mixed levels: optimization + schema + auth)
```

### Make strategies genuinely mutually exclusive

**The test:** Would a competent engineer implementing strategy A naturally arrive at
strategy B as a byproduct? If yes, they're not distinct enough.

```
✅ Distinct: "jwt"        vs "session"               (fundamentally different statefulness model)
✅ Distinct: "rest"       vs "graphql"               (different query paradigm)
✅ Distinct: "relational" vs "document"              (different data model)
❌ Too close: "jwt-hs256" vs "jwt-rs256"             (same mechanism, one implementation detail)
❌ Too close: "postgres"  vs "postgres-partitioned"  (same database, one feature flag)
❌ Too close: "redis-ttl" vs "redis-sliding-window"  (both Redis; strategy is the algorithm, not the store)
```

### Cover the real axes of the decision

Map the decision space first. What are the independent dimensions that actually matter?
Write strategies that each explore a different axis.

```
Goal: "cache expensive computation"
Axes: where the cache lives, invalidation strategy, storage backend

Better strategies:
  "client-side-etag"         (browser cache + conditional HTTP requests)
  "server-redis-ttl"         (server cache + time-based expiry)
  "server-content-hash"      (server cache + content-fingerprint invalidation)
```

### Two cosmos is usually enough

Start with 2. Add a third only if the first pair diverges interestingly and a
third perspective would add information a tiebreaker or new axis would bring.

```
# Default — covers most architecture decisions
/cosmos spawn --goal "..." --strategies "approach-a,approach-b"

# Add gamma only after observing significant Uncertainty between alpha and beta
/cosmos spawn --goal "..." --strategies "approach-a,approach-b,approach-c"
```

A third cosmos that agrees with one of the first two strengthens Resonance but
doesn't expand Uncertainty. Add it only when you need that confidence, not by default.

---

## Writing good insights

An insight should capture something that would change another cosmos's decision
if it read it. The Quantum Memory is only as useful as what's written into it.

### Good insight patterns

```json
{"content": "bcrypt.compare returns <1ms if comparison string is malformed — always precompute DUMMY_HASH = bcrypt.hashSync('__dummy__', ROUNDS) at module load, never inline", "ts": "..."}
{"content": "Redis ZREMRANGEBYSCORE + ZCARD in a single pipeline = one round trip regardless of log size — O(n) naive approach unacceptable at scale", "ts": "..."}
{"content": "[TUNNEL] Token store keyed by jti UUID eliminates need for a separate revocation table — the token identifier IS the lookup key", "ts": "..."}
{"content": "[JUMP] Reading alpha's audit trail insight — switched entire approach from polling to event-sourcing; audit is not a feature, it's the data model", "ts": "..."}
{"content": "TOKEN_EXPIRED must be distinct from INVALID_TOKEN — clients need to show 'session expired, please log in again' vs 'invalid credentials', different UX flows", "ts": "..."}
```

### Bad insight patterns (skip these)

```json
{"content": "Implemented the auth middleware", "ts": "..."}           ← status, not discovery
{"content": "Using Express for routing", "ts": "..."}                 ← obvious, zero decision value
{"content": "Tests pass", "ts": "..."}                                ← status, not insight
{"content": "See cosmos:alpha's implementation for details", "ts": "..."} ← pointer, not content
{"content": "Chose JWT", "ts": "..."}                                 ← decision without reasoning
```

**The test:** Would a cosmos on a *different* strategy make a different decision after
reading this? If yes, write it. If no, skip it.

### Tag threshold

Use `[TUNNEL]` and `[JUMP]` sparingly — only when the condition genuinely applies.

- `[TUNNEL]`: You found a path that bypasses a constraint you explicitly assumed was hard. Not "a clever optimization" — a *bypass* of an assumed requirement.
- `[JUMP]`: Reading another cosmos's insight caused you to discard your current architecture and rebuild at a qualitatively different level. Not gradual adaptation — a discontinuous leap.

A false positive dilutes the signal. A false negative just means the insight runs without emphasis. When in doubt, don't tag.

---

## How entanglement works

Each agent reads all `.quantum/*/insights.jsonl` files between every major
implementation step — and once more as a mandatory final read before completing.

```bash
# Between every major step, each agent reads all cosmos insights:
for f in .quantum/*/insights.jsonl; do [ -f "$f" ] && cat "$f"; done

# Each agent appends its own insights (never overwrites):
echo '{"content": "Redis Lua script for atomicity", "ts": "2026-05-12T10:31:00Z"}' \
  >> .quantum/alpha/insights.jsonl
```

**The mandatory final read:** Before marking itself done, each cosmos reads all
insight files one last time. This ensures late-stage findings — security bugs caught
during smoke testing, edge cases found in final review — propagate before the
superposition is observed. The final read is built into the spawn prompt.

**Why files instead of a shared API:**
- Zero infrastructure — works in any repo, any environment
- Each append is atomic — no write conflicts between parallel agents
- Git-ignored — insights don't pollute your history
- Human-readable — debug the quantum memory by opening the files

**The No-Cloning principle in practice:** Alpha cannot `cp -r cosmos/beta cosmos/alpha`.
It can *read* beta's insight that Redis sorted sets eliminate a separate rate-limit table,
then reconstruct that pattern inside its own token-bucket architecture. The discovery
transfers; the implementation doesn't. Influence without convergence.

---

## Quantum Memory

Location: `.quantum/` at repo root (git-ignored).

```
.quantum/
  alpha/insights.jsonl    ← alpha writes here, all cosmos read
  beta/insights.jsonl     ← beta writes here, all cosmos read
  gamma/insights.jsonl    ← gamma writes here, all cosmos read
```

Each line is a JSON object — one insight per line, append-only:

```json
{"content": "Redis Lua script for atomic INCR+EXPIRE prevents TOCTOU race condition", "ts": "2026-05-12T10:31:00Z"}
{"content": "[TUNNEL] Sorted set score-as-timestamp eliminates separate TTL management entirely", "ts": "2026-05-12T10:45:00Z"}
```

Rules:
- Each cosmos writes **only** to its own namespace
- All cosmos may **read** all namespaces
- Insights survive `/cosmos stop` by default — useful for retrospectives
- Never overwrite; always append (`>>`, never `>`)

---

## When to use QuantumAgent

### High-value fit

| Situation | Why Cosmos helps |
|-----------|-----------------|
| Architecture decision with multiple valid approaches | Resonance/Uncertainty map surfaces the real tradeoffs |
| You want working code, not a theoretical comparison | Bugs surface during implementation, not theorizing |
| Decision has long-lived architectural consequences | Exploration cost << cost of the wrong choice |
| Security-sensitive implementation | Multiple implementations catch different attack vectors |
| You'd otherwise spend hours researching approaches | Parallel exploration compresses that into one run |

### Not worth it

| Situation | Why to skip |
|-----------|-------------|
| The answer is obvious | Ask Claude directly — no interference pattern needed |
| Task takes < 1 hour | Agent overhead exceeds the benefit |
| You're already mid-implementation | Spawn at decision points, not mid-execution |
| Hard cost constraint | N cosmos = N × Claude API cost |
| Strategies aren't genuinely distinct | Resonance will be trivial; Uncertainty absent |

**The decision heuristic:** If you can write down 2–3 meaningfully different strategies
without hesitation, spawn. If you're struggling to distinguish them, the problem is
already well-defined enough to implement directly.

---

## Troubleshooting

### No Resonance after a full run

Strategies diverged completely — nothing converged. Either:

1. The problem is genuinely underdetermined (no universal answer exists for your constraints)
2. Strategies were at different abstraction levels and never faced the same decisions

→ Check: did all cosmos implement the same goal? If strategies diverged in scope, not
just approach, there's no interference surface to produce Resonance.

### No Uncertainty after a full run

Either BEC (good — the problem was deterministic) or decoherence (bad — cosmos copied each other).

→ Read each cosmos's strategy-specific choices. If they look identical despite different
strategies, decoherence occurred. If they diverged in implementation but agreed on every
conclusion, BEC. The distinction matters for confidence.

### A cosmos appears decoherent

Read its entanglement insights. Healthy entanglement:
> "I read alpha's insight about Redis pipelines and adopted the same pipeline pattern
> in my sliding-window implementation while keeping the sorted-set data structure."

Decoherence:
> "After reading alpha's token-bucket insights, I switched my approach to token-bucket."

The former adapts a pattern through its own strategy. The latter abandons the strategy.

### Critical bug propagated to some cosmos but not others

The mandatory final entanglement read (built into the spawn prompt) catches most
late-stage findings. If a cosmos finished before the bug was discovered, it may not
have the fix.

→ After crystallizing, check the other cosmos's insight files manually. If the bug
pattern applies to multiple strategies, apply the fix to your chosen implementation
before merging.

### `git worktree add` fails

Usually means a previous run's worktrees weren't cleaned up.

```bash
git worktree list                    # see all active worktrees
git worktree remove cosmos/alpha     # remove a specific one
git worktree prune                   # clean up stale references
```

Or run `/cosmos stop` to clean up all cosmos worktrees at once.

### Cosmos ran but produced no insights

The agent completed without writing to `.quantum/<name>/insights.jsonl`. This usually
means the agent didn't follow the Quantum Memory rules in `CLAUDE.md`.

→ The cosmos's work may still be useful — check the branch commits directly
(`git log cosmos/<name>`). The missing insights mean `/cosmos observe` will have
nothing to analyze for that cosmos, reducing Resonance/Uncertainty signal quality.

---

## Use cases

### Authentication

```
/cosmos spawn --goal "implement user authentication" \
  --strategies "jwt-stateless,session-redis,oauth2-pkce"
```
*Resonance usually finds:* token expiry strategy, error format contract, timing attack prevention
*Uncertainty usually reveals:* stateless vs revocable, key management operational overhead

---

### API design

```
/cosmos spawn --goal "design the public API for a task service" \
  --strategies "rest,graphql,grpc"
```
*Resonance usually finds:* cursor-based pagination, error envelope shape
*Uncertainty usually reveals:* schema flexibility vs contract strictness, transport and tooling overhead

---

### Database schema

```
/cosmos spawn --goal "design schema for a social feed" \
  --strategies "relational-normalized,document-denormalized,graph"
```
*Resonance usually finds:* the need for a separate activity/event log regardless of primary store
*Uncertainty usually reveals:* write vs read optimization tradeoff, query pattern assumptions

---

### Performance optimization

```
/cosmos spawn --goal "reduce p99 latency on the order API" \
  --strategies "db-indexing,query-rewrite,response-caching"
```
*Resonance usually finds:* which specific columns/queries are the actual bottleneck
*Uncertainty usually reveals:* cache invalidation complexity vs raw speed, cold-start behavior

---

### Refactoring

```
/cosmos spawn --goal "break apart the monolithic UserService" \
  --strategies "extract-class,strangler-fig,event-driven"
```
*Resonance usually finds:* where the real domain boundaries lie (they're rarely where the file is split)
*Uncertainty usually reveals:* migration risk tolerance vs clean architecture; incremental vs big-bang

---

### Security hardening

```
/cosmos spawn --goal "harden the login endpoint against credential stuffing" \
  --strategies "rate-limiting,captcha,device-fingerprinting"
```
*Resonance usually finds:* progressive friction beats hard blocking; logging is essential regardless
*Uncertainty usually reveals:* UX degradation vs security margin; bot detection accuracy tradeoffs

---

### LLM cost reduction

```
/cosmos spawn --goal "reduce LLM API costs by 60%" \
  --strategies "prompt-caching,model-routing,response-caching"
```
*Resonance usually finds:* the stacking order of savings (cache first, then route, then store)
*Uncertainty usually reveals:* determinism assumptions that break each approach differently

---

## Quantum mechanics → development

Every concept below has a direct operational meaning — none are decorative metaphors.

### Quick reference

| Concept | Quantum | Development |
|---------|---------|-------------|
| **Wave-Particle Duality** | Particles are both wave and particle depending on measurement | Goal = wave (pure potential); each cosmos = particle (concrete implementation) |
| **Young's Double Slit** | Wave through two slits creates interference pattern | Same goal through N strategies reveals resonance (constructive) and uncertainty (destructive) |
| **Superposition** | System exists in multiple states simultaneously | N cosmos run in parallel — no winner until crystallization |
| **Path Integral** | Particle takes all paths simultaneously; result from interference | Every implementation path explored at once; resonance emerges from their overlap |
| **Quantum Annealing** | Quantum tunneling escapes local optima to find global minimum | Parallel cosmos escape architectural local optima a single sequential approach would get stuck in |
| **Entanglement** | Particles affect each other regardless of distance | Real-time insight sharing between cosmos without merging strategies |
| **Quantum Teleportation** | Quantum state transferred via entanglement + classical channel | Insight travels via `.quantum/` files (classical) + entanglement rules (quantum) — no implementation copying |
| **No-Cloning Theorem** | Unknown quantum state cannot be perfectly copied | A cosmos cannot clone another's implementation — each must evolve independently |
| **Pauli Exclusion Principle** | No two fermions can occupy the same quantum state | No two cosmos can run the same strategy — distinct strategies required |
| **Spin** | Intrinsic immutable property of a particle | Each cosmos has an intrinsic strategic identity that defines which direction it explores |
| **Quantum Coherence** | Phase relationships maintained across the system | Each cosmos maintains strategic integrity; coherence = independent sample value |
| **Quantum Tunneling** | Particle passes through a classically forbidden barrier | A cosmos finds a solution path that bypasses an assumed hard constraint |
| **Quantum Jump** | Electron transitions between energy levels discontinuously | A single insight causes a cosmos to make a discontinuous leap — not gradual, not incremental |
| **Quantum Interference** | Waves amplify (constructive) or cancel (destructive) | Constructive → Resonance; Destructive → Uncertainty |
| **Resonance** | Waves in phase amplify each other | Multiple cosmos independently converge → trust the signal, ship with confidence |
| **Uncertainty Principle** | Position and momentum cannot both be precisely known | Cannot optimize all dimensions simultaneously; some tradeoffs are fundamental |
| **Schrödinger's Cat** | System in superposition is simultaneously all states until measured | Each cosmos is simultaneously the best and worst solution until crystallized and tested |
| **Degeneracy** | Multiple distinct states with identical energy levels | Different strategies reaching the same conclusion = degenerate solutions; equality proves robustness |
| **Bose-Einstein Condensate** | All particles collapse to the same ground state | Total resonance across all decisions — the goal was deterministic; any cosmos would do |
| **Measurement Problem** | Observation collapses wave function | `/cosmos observe` ≠ collapse; `/cosmos crystallize` = collapse. Distinction is intentional |
| **Observation** | Reading state without collapsing it (in non-destructive measurement) | `/cosmos observe` runs freely while cosmos work — superposition unaffected |
| **Crystallization** | Wave function collapse — one eigenstate selected | One cosmos chosen, result merged; superposition ends |
| **Decoherence** | Loss of quantum coherence from environmental interaction | Cosmos that copies another loses strategic independence — no longer a valid sample |
| **Reference Frame** *(Special Relativity)* | Observer's frame determines which quantities are relative and which are invariant | Resonance = frame-invariant answer (true regardless of constraint set); Uncertainty = frame-dependent answer (shifts with constraints — e.g., "stateless scalability" frame vs. "instant revocability" frame) |
| **Geodesics + Spacetime Curvature** *(General Relativity)* | Mass curves spacetime; free particles follow locally straightest paths (geodesics) | Strong problem constraints curve the solution space; each strategy follows its natural geodesic — when constraints are extreme, all geodesics converge → BEC |
| **Equivalence Principle** *(General Relativity)* | Locally, gravitational acceleration and inertial acceleration are indistinguishable | Locally, a workaround and a proper solution behave identically; only the wider architectural view reveals the difference — `/cosmos observe` provides that view |

---

### Key mechanics in depth

**Wave-Particle Duality + Young's Double Slit**

Your goal, before implementation, is pure wave: it has no definite form, only
potential. Sending it through N strategies (the slits) produces an interference
pattern. Where strategies agree — constructive interference → Resonance. Where
they disagree — destructive interference → Uncertainty. The pattern tells you
exactly which decisions are robust and which are genuine tradeoffs.

**Path Integral + Quantum Annealing**

Feynman's path integral says a particle simultaneously takes every possible path.
QuantumAgent runs every strategy simultaneously. The "most probable path" — the
one that survives interference — is your Resonance output. Quantum annealing adds
the optimization dimension: sequential decision-making gets trapped in local optima.
Parallel cosmos escape them by exploring the full solution space at once.

**No-Cloning Theorem + Pauli Exclusion + Spin**

These three together define why cosmos must stay independent. No-Cloning: you
cannot duplicate an unknown quantum state — so a cosmos cannot copy another's
implementation wholesale. Pauli Exclusion: no two fermions occupy the same state —
so no two cosmos can run the same strategy. Spin: each particle's intrinsic
identity is immutable — so each cosmos's core strategy must be preserved throughout.
Break any of these rules and you lose independent sample value.

**Entanglement + Quantum Teleportation**

Entanglement is the channel; teleportation is the mechanism. When alpha writes an
insight to `.quantum/alpha/insights.jsonl` and beta reads it, the insight
"teleports" — information travels via the classical channel (file I/O) + the
entanglement relationship (the read requirement in each agent's prompt). The
original implementation in alpha is untouched. Beta reconstructs the relevant
pattern in its own strategic context.

**Quantum Tunneling + Quantum Jump**

Two distinct breakthrough types. Tunneling: a cosmos finds a solution that bypasses
a constraint you assumed was hard — it goes *through* the wall instead of over it.
Jump: a cosmos reads an insight from another and makes a *discontinuous* architectural
shift — not a gradual adaptation but a sudden transition to a qualitatively
different implementation level. Both produce non-obvious solutions that sequential
exploration would rarely find.

**Schrödinger's Cat + Measurement Problem**

Each cosmos is simultaneously the best and worst solution until you crystallize
and run tests. `/cosmos observe` is a non-destructive measurement — it reads state
without collapsing the superposition. `/cosmos crystallize` is the destructive
measurement — it collapses one cosmos into a definite result. The distinction is
intentional: observe as many times as you want; crystallize only when ready.

**Resonance + Degeneracy + Bose-Einstein Condensate**

Resonance is constructive interference — multiple cosmos reaching the same
conclusion independently. Degeneracy deepens this: when *different* strategies
produce *identical* solutions, those solutions have equal "energy" — they're
equivalent at the ground state. If all decisions resonate across all cosmos,
you've reached a Bose-Einstein Condensate: the goal was deterministic, any cosmos
would have found the same answer. High resonance = high confidence. Full
condensate = the problem had one correct answer all along.

**Reference Frame (Special Relativity)**

In special relativity, some measurements are relative to the observer's frame;
others are invariant across all frames. The same logic applies to decisions.
Resonance identifies **frame-invariant** conclusions — answers that hold true
regardless of which constraints you're optimizing for. Uncertainty marks
**frame-dependent** decisions: the right answer changes depending on whether
your frame is "stateless scalability" or "instant revocability." The strategies
*are* the frames. What survives across all of them is your invariant truth.

**Geodesics + Spacetime Curvature (General Relativity)**

In general relativity, mass curves spacetime and free particles follow geodesics
— locally straightest paths through curved space. Problem constraints curve the
solution space the same way: each strategy follows its natural geodesic through
that landscape. When constraints are mild, geodesics diverge widely (high
Uncertainty). When constraints are extreme — a hard performance ceiling, a strict
compliance requirement — all geodesics curve toward the same region. At the limit,
every strategy arrives at the same point: Bose-Einstein Condensate. The
constraints, not the strategies, determine the curvature. BEC signals a strongly
constrained problem; Uncertainty signals a weakly constrained one.

**Equivalence Principle (General Relativity)**

Einstein's equivalence principle: locally, you cannot distinguish between
gravitational and inertial acceleration. In development: locally, a clever
workaround and a properly designed solution look identical — same behavior, same
tests passing. Only broader context reveals the difference. `/cosmos observe`
provides that wider view: when strategies diverge in their *reasoning* for the
same conclusion, that's your signal that one path may be a local workaround
dressed as a proper design.

---

## Repository layout

```
skills/
  spawn/SKILL.md        — /cosmos spawn
  observe/SKILL.md      — /cosmos observe
  crystallize/SKILL.md  — /cosmos crystallize
  stop/SKILL.md         — /cosmos stop
.claude-plugin/
  plugin.json           — plugin manifest
cosmos/                 — runtime git worktrees (git-ignored)
.quantum/               — runtime insight files (git-ignored)
```

---

## Cost

N cosmos = N × Claude API cost. Quantum Memory reads/writes are local file I/O.
`/cosmos observe` uses one Claude call for semantic analysis.
`/cosmos crystallize` uses one Claude call for the summary report.

| Setup | Relative cost | When to use |
|-------|--------------|-------------|
| 2 cosmos | 2× | Default starting point — covers most architecture decisions |
| 3 cosmos | 3× | First pair showed significant Uncertainty; a third perspective breaks ties or adds a new axis |
| 4–5 cosmos | 4–5× | Rarely justified — diminishing returns; only for highly contested decisions with well-defined axes |

**The cost-value calculation:** If the wrong architectural decision costs you a week of
refactoring, a 30-minute 3-cosmos run is cheap. If the decision is reversible in an
hour, skip the spawn and ask Claude directly.
