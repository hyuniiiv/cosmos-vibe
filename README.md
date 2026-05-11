# 🌌 Cosmos Vibe

> Before you commit to one approach, explore three in parallel.

A Claude Code plugin that runs multiple AI agents simultaneously — each tackling
the same goal with a different strategy. Agents share discoveries in real time.
When they independently reach the same conclusion, that's your signal to trust it.
When they diverge, that's your real tradeoff.

```
/cosmos spawn --goal "implement user auth" --strategies "jwt,session,oauth2"
```

---

## The problem it solves

You're building something with Claude Code. Claude implements one approach. You
ship it. Three weeks later you're refactoring because the architecture didn't
scale, or you discover a security edge case, or you realize a different approach
would have been cleaner.

Cosmos runs the exploration before you commit. Not as a theoretical comparison —
as actual working implementations that discover real issues.

---

## Quantum mechanics → development

Cosmos Vibe maps quantum physics to concrete development mechanics. Every concept
below has a direct operational meaning — none are decorative metaphors.

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
Cosmos Vibe runs every strategy simultaneously. The "most probable path" — the
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

---

## Install

```bash
claude plugins install https://github.com/hyuniiiv/cosmos-vibe
```

No Python. No vector database. No subprocess. Pure markdown skills.
Quantum Memory is plain JSON Lines files on disk.

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
   └ Chose Redis HINCRBY for atomic counter update — avoids race condition
   └ Burst allowance: 2× rate for first 3 seconds of a new window

🌌 cosmos:beta   (7 insights)  — sliding-window
   └ Sliding log stored as Redis sorted set (score = timestamp)
   └ ZREMRANGEBYSCORE + ZCARD in a pipeline — single round trip

🌌 cosmos:gamma  (9 insights)  — fixed-window
   └ Fixed window edge case: 2× burst at window boundary — documented
   └ INCR + EXPIRE in Lua script for atomicity

⚡ Resonance — trust these:
   "Redis Lua script or pipeline for atomicity" — all 3 cosmos found this independently
   "429 Too Many Requests with Retry-After header" — all 3 cosmos converged
   "rate limit headers (X-RateLimit-Limit, X-RateLimit-Remaining)" — all 3 cosmos converged

🌀 Uncertainty — your call:
   "burst handling" — alpha: explicit burst allowance | gamma: documented edge case only
   "memory per user" — beta: O(requests) sliding log | alpha/gamma: O(1) counter
```

Pick the result you want:

```
/cosmos crystallize beta    # extract beta — optionally merge to current branch
/cosmos stop                # clean up all worktrees and branches
```

---

## Commands

### `/cosmos spawn`

```
/cosmos spawn --goal "<goal>" --strategies "<s1,s2,...>"
```

Launches one cosmos per strategy. Names assigned alphabetically (alpha, beta,
gamma, delta, epsilon — max 5). Each cosmos gets:

- An isolated git worktree at `cosmos/<name>`
- A dedicated branch `cosmos/<name>`
- A quantum memory file `.quantum/<name>/insights.jsonl`
- A `CLAUDE.md` with goal, strategy, and entanglement rules

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
- Decoherence warning if a cosmos lost its strategic identity

---

### `/cosmos crystallize <id>`

Collapses one cosmos into a standalone result:

1. Summarizes core decisions, rejected alternatives, and entanglement influences
2. Shows the last 10 commits and diff stats
3. Offers to merge (`git merge cosmos/<id> --no-ff`) or preserve the branch

Other cosmos are unaffected — the superposition holds until you stop.

---

### `/cosmos stop`

Removes all cosmos worktrees and branches. Offers to wipe `.quantum/`
(insights are preserved by default).

---

## How entanglement works

Each agent prompt requires reading all `.quantum/*/insights.jsonl` files between
every major implementation step:

```bash
# Between every step, each agent runs:
for f in $(ls .quantum/*/insights.jsonl 2>/dev/null); do cat "$f"; done
```

```bash
# Each agent appends its own insights (never overwrites):
echo '{"content": "Redis Lua script for atomicity", "ts": "2026-05-12T10:31:00Z"}' \
  >> .quantum/alpha/insights.jsonl
```

If alpha writes "Redis Lua script prevents race conditions" at step 2, beta reads
it at step 3 and can adopt the pattern — while staying on its sliding-window
strategy. That's entanglement: influence without convergence.

---

## Quantum Memory

Location: `.quantum/` at repo root (git-ignored).

```
.quantum/
  alpha/insights.jsonl
  beta/insights.jsonl
  gamma/insights.jsonl
```

Each line is a JSON object:

```json
{"content": "Redis Lua script for atomic INCR+EXPIRE prevents race condition", "ts": "2026-05-12T10:31:00Z"}
```

- Each cosmos writes **only** to its own namespace
- All cosmos may **read** all namespaces
- Insights survive `/cosmos stop` by default

---

## When to use it

**Good fit:**
- Architecture decision with multiple valid approaches and non-obvious tradeoffs
- You want working code, not just a comparison
- The implementation details matter (bugs surface during coding, not theorizing)
- You'd otherwise spend hours researching which approach to take

**Not worth it:**
- The answer is obvious — just ask Claude directly
- Task is small (< 1 hour) — agent overhead exceeds the benefit
- You're already mid-implementation — spawn at decision points, not mid-execution
- Hard cost constraint — N cosmos = N × Claude API cost

---

## Use cases

### Authentication

```
/cosmos spawn --goal "implement user authentication" --strategies "jwt-stateless,session-redis,oauth2-pkce"
```
*Resonance usually finds:* token expiry strategy, error format, timing attack prevention
*Uncertainty usually reveals:* stateless vs revocable, key management complexity

---

### API design

```
/cosmos spawn --goal "design the public API for a task service" --strategies "rest,graphql,grpc"
```
*Resonance usually finds:* cursor-based pagination, error envelope shape
*Uncertainty usually reveals:* schema flexibility vs contract strictness, transport overhead

---

### Database schema

```
/cosmos spawn --goal "design schema for a social feed" --strategies "relational-normalized,document-denormalized,graph"
```
*Resonance usually finds:* need for a separate activity/event log
*Uncertainty usually reveals:* write vs read optimization tradeoff

---

### Performance optimization

```
/cosmos spawn --goal "reduce p99 latency on the order API" --strategies "db-indexing,query-rewrite,response-caching"
```
*Resonance usually finds:* which columns/queries are the actual bottleneck
*Uncertainty usually reveals:* cache invalidation complexity vs raw speed

---

### Refactoring

```
/cosmos spawn --goal "break apart the monolithic UserService" --strategies "extract-class,strangler-fig,event-driven"
```
*Resonance usually finds:* where the real boundaries are
*Uncertainty usually reveals:* migration risk vs clean architecture tradeoff

---

### Security hardening

```
/cosmos spawn --goal "harden the login endpoint against credential stuffing" --strategies "rate-limiting,captcha,device-fingerprinting"
```
*Resonance usually finds:* progressive friction is better than hard blocking
*Uncertainty usually reveals:* UX degradation vs security margin tradeoff

---

### LLM cost reduction

```
/cosmos spawn --goal "reduce LLM API costs by 60%" --strategies "prompt-caching,model-routing,response-caching"
```
*Resonance usually finds:* the order of operations that stacks savings
*Uncertainty usually reveals:* determinism assumptions in each approach

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

## Cost

N cosmos = N × Claude API cost. Quantum Memory reads/writes are local file I/O.
`/cosmos observe` uses one Claude call for semantic analysis.
`/cosmos crystallize` uses one Claude call for the summary report.

Start with 2 cosmos. Add more only if the first pair diverges interestingly.
