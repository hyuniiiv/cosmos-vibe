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

## Use Cases

Anything where multiple valid approaches exist and the right answer isn't obvious
upfront is a good candidate. The more the strategies can learn from each other,
the more value entanglement adds.

### Authentication & Authorization

```
/cosmos spawn \
  --goal "implement user authentication" \
  --strategies "jwt-stateless,session-redis,oauth2-pkce"
```

*What you learn:* JWT's stateless scaling advantage vs. session's instant revocation
vs. OAuth2's zero-credential-storage. Often alpha discovers sliding-window expiry
and gamma adopts it — different transport, same expiry pattern.

---

```
/cosmos spawn \
  --goal "implement role-based access control" \
  --strategies "rbac-flat,rbac-hierarchical,abac"
```

*What you learn:* Flat RBAC is simple to query; hierarchical handles org trees
naturally; ABAC is the only one that scales to dynamic policies. Entanglement
often reveals that hierarchical and ABAC converge on the same permission-check
interface.

---

### API Design

```
/cosmos spawn \
  --goal "design the public API for a task management service" \
  --strategies "rest-resource,graphql,grpc"
```

*What you learn:* REST is cache-friendly and widely understood; GraphQL eliminates
over-fetching for complex clients; gRPC wins on throughput for internal services.
Entanglement often surfaces pagination design — all three converge on cursor-based.

---

```
/cosmos spawn \
  --goal "handle API versioning" \
  --strategies "url-path,header,query-param"
```

*What you learn:* URL path is the most visible and cache-friendly; header versioning
keeps URLs clean but surprises reverse proxies; query param is easiest to test.
Divergence usually stays — these are genuinely different trade-offs with no clear winner.

---

### Database & Storage

```
/cosmos spawn \
  --goal "design the schema for a social feed" \
  --strategies "relational-normalized,document-denormalized,graph"
```

*What you learn:* Normalized schema handles write consistency well; document model
speeds up read-heavy feed rendering; graph makes follower traversal trivial.
Entanglement often reveals that relational and document both need a separate
activity table — they converge on that independently.

---

```
/cosmos spawn \
  --goal "implement full-text search" \
  --strategies "postgresql-fts,elasticsearch,meilisearch"
```

*What you learn:* PostgreSQL FTS has zero infra overhead but limited ranking;
Elasticsearch is the industry standard with rich scoring; Meilisearch is fast
to set up with typo-tolerance built in. Alpha's indexing strategy (partial update
vs. full reindex) often gets adopted by all three.

---

```
/cosmos spawn \
  --goal "design a caching layer for product listings" \
  --strategies "redis-aside,redis-write-through,cdn-edge"
```

*What you learn:* Cache-aside is simple and explicit; write-through keeps cache
always warm but couples writes; CDN edge caching is fastest but only for public
content. Entanglement typically surfaces TTL strategy — all three end up needing
to agree on what "stale" means.

---

### Performance Optimization

```
/cosmos spawn \
  --goal "reduce p99 latency on the order API from 800ms to under 200ms" \
  --strategies "db-indexing,query-rewrite,response-caching"
```

*What you learn:* Indexing fixes the root cause permanently; query rewrite can
eliminate N+1 without schema changes; caching masks latency but adds invalidation
complexity. Alpha's index choices often influence beta's query rewrites —
they converge on which columns matter most.

---

```
/cosmos spawn \
  --goal "optimize image delivery pipeline" \
  --strategies "cdn-offload,webp-conversion,lazy-loading"
```

*What you learn:* CDN reduces origin load most dramatically; WebP cuts payload
30-50%; lazy loading improves perceived performance without touching payload size.
These three often combine cleanly — entanglement surfaces the ordering
(convert first, then cache, then lazy-load at client).

---

### Refactoring & Architecture

```
/cosmos spawn \
  --goal "break apart the monolithic UserService (2000 lines)" \
  --strategies "extract-class,strangler-fig,event-driven"
```

*What you learn:* Extract-class is the safest and most mechanical; strangler fig
lets you migrate incrementally without a big-bang rewrite; event-driven decouples
future growth but adds async complexity. Strangler fig and event-driven often
converge on the same boundary lines — even though the execution differs.

---

```
/cosmos spawn \
  --goal "migrate from callbacks to async/await" \
  --strategies "incremental-per-module,codemods,full-rewrite"
```

*What you learn:* Incremental is lowest-risk but leaves mixed code for months;
codemods automate the mechanical parts but miss edge cases; full rewrite is fast
but requires feature-freeze. Entanglement typically surfaces the same edge cases
across all three — error propagation and cancellation are universally tricky.

---

### Security

```
/cosmos spawn \
  --goal "harden the login endpoint against credential stuffing" \
  --strategies "rate-limiting,captcha,device-fingerprinting"
```

*What you learn:* Rate limiting is table stakes but bypassable with distributed
IPs; CAPTCHA degrades UX for real users; device fingerprinting is invisible but
requires more storage. All three often converge on progressive friction —
block after N failures, not before.

---

```
/cosmos spawn \
  --goal "protect PII at rest in the user database" \
  --strategies "column-encryption,field-level-encryption,tokenization"
```

*What you learn:* Column encryption is simplest to implement; field-level gives
per-field granularity for compliance; tokenization replaces data with non-sensitive
tokens and works across systems. Key rotation strategy is the recurring entanglement
point — all three need to solve it.

---

### Testing Strategy

```
/cosmos spawn \
  --goal "increase confidence in the payment flow without slowing CI" \
  --strategies "unit-mocks,integration-real-db,contract-pact"
```

*What you learn:* Unit tests with mocks are fast but mock/prod divergence causes
silent failures; integration tests with a real DB catch real bugs but are slow;
contract tests (Pact) verify boundaries without full integration. Entanglement
often reveals that unit and contract tests complement each other — alpha adopts
contract boundaries from gamma's work.

---

### Infrastructure & Deployment

```
/cosmos spawn \
  --goal "implement zero-downtime deployment for the API server" \
  --strategies "blue-green,canary,rolling"
```

*What you learn:* Blue-green is the simplest mental model with instant rollback;
canary reduces blast radius by routing a percentage of traffic; rolling is
resource-efficient but makes rollback harder. Health-check design is the universal
entanglement point — all three need to agree on what "healthy" means.

---

```
/cosmos spawn \
  --goal "design the observability stack" \
  --strategies "prometheus-grafana,datadog,opentelemetry"
```

*What you learn:* Prometheus+Grafana is open-source and highly customizable;
Datadog has the best out-of-the-box UX; OpenTelemetry is vendor-neutral and
future-proof. Cardinality management surfaces as an entanglement — all three
hit the same wall on high-cardinality labels.

---

### AI & LLM Features

```
/cosmos spawn \
  --goal "add a document Q&A feature to the app" \
  --strategies "rag-vector,rag-bm25,fine-tuning"
```

*What you learn:* Vector RAG handles semantic similarity well; BM25 is faster
and better at exact keyword matching; fine-tuning bakes knowledge into the model
but is expensive to update. Chunking strategy is the entanglement hot spot —
alpha's chunking experiments get adopted by beta without beta needing to redo them.

---

```
/cosmos spawn \
  --goal "reduce LLM API costs by 60%" \
  --strategies "prompt-caching,model-routing,response-caching"
```

*What you learn:* Prompt caching (Anthropic's prefix cache) cuts costs on repeated
system prompts; model routing sends simple requests to cheaper models; response
caching is free for deterministic queries. These three stack — entanglement reveals
the order of operations that maximizes savings.

---

### Frontend & UX

```
/cosmos spawn \
  --goal "implement infinite scroll for the activity feed" \
  --strategies "intersection-observer,scroll-event-throttled,virtualized-list"
```

*What you learn:* Intersection Observer is the modern standard with low CPU cost;
scroll-event throttling is compatible with older browsers; virtualization handles
100k+ items but adds rendering complexity. All three converge on the same
cursor-based pagination contract with the API.

---

```
/cosmos spawn \
  --goal "manage client-side state for a multi-step form" \
  --strategies "react-hook-form,zustand,url-state"
```

*What you learn:* React Hook Form minimizes re-renders and handles validation;
Zustand persists state across navigation; URL state makes forms shareable and
browser-back-friendly. Entanglement surfaces validation timing — all three end up
needing to decide when to validate (on-change vs. on-blur vs. on-submit).

---

### When to NOT use Cosmos Vibe

- The implementation is deterministic — there's only one correct approach
- The task is very small (< 1 hour of work) — agent overhead exceeds the benefit
- You're already mid-implementation — spawn at decision points, not mid-execution
- You have a hard cost budget — N universes = N × API cost; 3 universes on a large
  codebase adds up quickly

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
