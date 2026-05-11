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

Cosmos Vibe maps six quantum physics concepts to concrete development signals:

**Wave-Particle Duality** (파동-입자 이중성) — Your goal, before implementation,
is pure wave: a probability distribution of all possible solutions, with no
definite form. Each cosmos is a measurement at a different angle — it collapses
the wave into a concrete particle (working code). Different strategies are
different measurement angles on the same wave. This is why the same goal produces
genuinely different implementations across cosmos: not because any of them is
wrong, but because each reveals a different facet of the underlying solution space.

**Superposition** (중첩) — N cosmos run simultaneously, each with a different
strategy. The solution space exists in superposition — no winner is forced until
you deliberately collapse it. You get N explorations in the time it would take to
build one.

**Entanglement** (얽힘) — Agents read each other's insights between every
implementation step. A discovery in one cosmos propagates to others in real time
without merging their strategies. If alpha finds a race condition fix, beta and
gamma read it and can apply it to their own implementations.

**Resonance** (공명) — When multiple cosmos independently reach the same conclusion
without copying each other, that decision is robust. Every strategy found it.
Ship it without second-guessing.

```
⚡ Resonance — trust these:
   "15-minute token expiry" — 3 cosmos converged independently
   "{ error: { code, message } } format" — 3 cosmos converged independently
   "dummy bcrypt on unknown email" — 3 cosmos converged independently
```

**Uncertainty** (불확정성) — When cosmos genuinely disagree, that's not a failure —
it's a real tradeoff. You cannot optimize all dimensions simultaneously. Make a
conscious choice.

```
🌀 Uncertainty — your call:
   "signing algorithm" — alpha: HS256 (single-server simplicity)
                          beta:  RS256 (multi-service key distribution)
   "bcrypt rounds"     — alpha/gamma: 12 (security margin)
                          beta: 10 (NIST baseline, faster)
```

**Observation** (관측) — In quantum mechanics, observing a system doesn't collapse
it — it just reads the current state. `/cosmos observe` works the same way: you
can run it as many times as you want while cosmos are still running. The
superposition is unaffected. Each observation gives you a snapshot of where every
cosmos is right now, without forcing a decision.

**Crystallization** (결정화) — Wave function collapse. You've observed long enough.
`/cosmos crystallize <id>` picks one reality, extracts the result, and optionally
merges it into your main branch. The other cosmos remain in superposition until
you stop them.

**Decoherence** (결어긋남) — If a cosmos abandons its strategy and simply copies
another, it loses value as an independent sample. The entanglement rules
explicitly prevent this: influence is allowed, wholesale adoption is not.

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
