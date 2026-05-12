# Example run — `auth-audit`

A real 3-cosmos audit run against a production Electron+Next.js payment
terminal codebase ("ExampleSYSTEM"). The goal was a security review of
terminal JWT and payment authentication; the actual run surfaced **3-way
resonance on a systemic auth flaw and a tunneling-class find that exposed
a separate revenue bug**.

## Domain context

ExampleSYSTEM is a hybrid Electron + Next.js payment terminal system:
backend serves portal + device APIs (Supabase + Next.js route handlers),
client runs as an Electron app on physical POS terminals. Auth is a
mix of Terminal JWT (HS256 via `jose`), Supabase cookies for the portal,
and an `X-Merchant-Key` header for merchant sync. Offline payment queueing
is supported.

All file paths, function names, and library choices below are real —
only company-identifying strings were masked.

## Why these strategies

Three **complementary lenses** on the same code, not three competing
implementations:

- **alpha — vulnerability-hunter:** classical CWE-class audit. CRITICAL/HIGH/MEDIUM/LOW severity grades. The kind of pass a pentester would do.
- **beta — architecture-auditor:** contracts, centralization, type-vs-runtime gaps. The shape of the system, not bugs in any one file.
- **gamma — client-dataflow:** follow the token. localStorage, IndexedDB, Electron main/preload, sync routes. Where could the state machine lose money?

Resonance *across* lenses is the high-confidence signal we wanted — if a
vulnerability-hunter, an architecture-auditor, and a dataflow-tracer all
flag the same thing independently, it is real and systemic.

## What we got

The run was executed **twice** on the same goal — a deliberate re-spawn
to test whether complementary findings would surface in a second round.
The headline resonance held across both rounds; the 2nd round added a
new CRITICAL and write-path account-takeover findings.

### 1st round (3 cosmos, 43 insights: alpha 22 / beta 11 / gamma 10)

| Signal | Finding |
|---|---|
| ⚡ **3-way resonance** | Terminal JWT has no `exp` claim → tokens are effectively immortal (compounded by stateless-JWT revocation gap + plaintext token storage) |
| ⚡ **2-way (α+β)** | No runtime JWT payload validation — `as unknown as TerminalJWTPayload` cast |
| ⚡ **2-way (α+γ)** | `jwtVerify` called without `algorithms: ['HS256']` allowlist |
| (alpha) | `/api/setup/merchant` allows self-registration as `platform_admin` (OWASP A01) |
| (alpha) | `cancel-request` trusts `body.termId` instead of authenticated payload |
| (alpha) | `/api/terminals` GET leaks cross-tenant data (IDOR) |
| (beta) | 3 auth schemes coexist with no central dispatcher; no `middleware.ts`; web-side `auth.getUser()` duplicated across 30+ routes |
| (gamma) | Token dual-storage drift → first offline queue flush can silently fail |
| (gamma) | Offline `pending_payments` IDB records have no HMAC → amount tampering possible |

### 2nd round (~33 insights — new findings)

| Signal | Finding |
|---|---|
| ✨ **[TUNNEL] gamma** | **Electron CORS wildcard injection** — `main.js` injects `Access-Control-Allow-Origin: *` + allows `Authorization` for any response missing the header. XSS or supply-chain compromise → token exfiltrated to any origin. 1st round missed this entirely. |
| (alpha) | `terminals/[id]/account` & `terminals/[id]/key` PUT routes don't verify merchant ownership → cross-tenant **write** path → full account takeover via password/key overwrite |
| (gamma) | `syncedIds ?? []` fallback → if server response is malformed, client retries → duplicate charge risk |
| (gamma) | PIN plaintext-fallback (`settingsStore.ts:68`) — migration leftover, timing-leak vector |
| (beta) | `heartbeat` re-parses Authorization header after `requireTerminalAuth` — structural defect: helper doesn't return full claims |

See [`observe-snapshot.md`](observe-snapshot.md) for the **verbatim
auto-observe output** from both rounds (Korean, as the run was executed
in a Korean session), and [`insights/`](insights/) for the raw, unedited
JSONL from each cosmos.

## What was shipped

Three concrete code changes (not a `crystallize`d merge — the deliverable
was a fix set, not a single implementation):

1. Add `setExpirationTime("24h")` to `createTerminalJWT`; remove the
   `clockTolerance: 999_999_999` from the refresh route.
2. Change `app/api/payment/cancel/route.ts` to read `termId` from the
   verified JWT payload, not the request body.
3. Make `activateTerminal` write the device token to **both**
   `localStorage` and IndexedDB atomically, so `flushOfflineQueue` always
   has it.

## Files in this run

- [`spawn-command.md`](spawn-command.md) — the exact `/cosmos:spawn` invocation and per-strategy intent
- [`insights/alpha.jsonl`](insights/alpha.jsonl) — 11 raw insights (vulnerability-hunter)
- [`insights/beta.jsonl`](insights/beta.jsonl) — 8 raw insights (architecture-auditor)
- [`insights/gamma.jsonl`](insights/gamma.jsonl) — 10 raw insights (client-dataflow)
- [`observe-snapshot.md`](observe-snapshot.md) — `/cosmos:observe` output (auto-run at end of `/cosmos:spawn`): superposition, resonance, tunneling, jumps, blockers

## Notes for the reader

**Re-spawning the same goal works.** The 2nd round was not a copy of the
1st — it surfaced a new CRITICAL (Electron CORS wildcard) and the actual
write-path takeover routes that the 1st round missed. Treat cosmos as
probabilistic: if the topic is high-stakes, run it twice.

**Tunneling is the headline.** The most-quoted use of QuantumAgent will be
the resonance signal ("3 cosmos agreed → ship"). But the *highest-leverage*
moment in this run was gamma's 2nd-round `[TUNNEL]` find — the Electron
CORS wildcard injection. A security audit found it because one cosmos
was tracing where the token *physically goes*, not enumerating CWE
categories. Strategies that **trace data** find things strategies that
**classify bugs** miss.

**No `crystallize` was run.** This was an audit, not a build. The
deliverable was a fix list extracted from the insights, not a merged
branch. `crystallize` exists for the build case — not every cosmos run
needs to end with it. The output of cosmos is *signal*, and signal is
useful whether or not it ends in a merge.

**Sanitization scope.** Company-identifying strings were masked to
`EXAMPLE_SYSTEM` / `example-system-settings`. All file paths, line
numbers, function names, library names (`jose`, `bcryptjs`, `Zustand`),
severity grades, and architectural decisions are verbatim from the
source codebase.
