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

| Signal | Finding | Confidence |
|---|---|---|
| ⚡ **3-way resonance** | Terminal JWT has no `exp` claim → tokens are effectively immortal | Ship the fix |
| ⚡ **2-way resonance** | Refresh route's `clockTolerance: 999_999_999` would ignore `exp` even if it existed | Ship the fix |
| ✨ **Tunneling (gamma)** | Token dual-storage drift → offline payment queue silently never flushes (a **money** bug found by a **security** audit) | Adjacent revenue regression caught for free |
| (alpha-only) | `cancel-request` trusts `body.termId` instead of authenticated payload → cross-merchant cancellation | Same-day fix |
| (beta-only) | 3 auth schemes coexist, no central dispatcher, `revoke` is a no-op against stateless JWT | Tech-debt to schedule |

See [`observe-snapshot.md`](observe-snapshot.md) for the full synthesis,
and [`insights/`](insights/) for the raw, unedited JSONL from each cosmos.

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
- [`observe-snapshot.md`](observe-snapshot.md) — manual synthesis of the run (the `/cosmos:observe` command was not invoked; this is an editorial summary of the raw JSONL, called out as such)

## Notes for the reader

**Tunneling is the headline.** The most-quoted use of QuantumAgent will be
the resonance signal ("3 cosmos agreed → ship"). But the *highest-leverage*
moment in this run was the tunneling find from gamma: a security audit
discovered a payment-loss bug because one cosmos was following data
instead of categories. Strategies that **trace** find things strategies
that **classify** miss.

**No `crystallize` was run.** This was an audit, not a build. The
deliverable was a fix list extracted from the insights, not a merged
branch. `crystallize` exists for the build case, not every cosmos run
needs to end with it. The output of cosmos is *signal*, and signal is
useful whether or not it ends in a merge.

**Sanitization scope.** Company-identifying strings were replaced with
"ExampleSYSTEM". All file paths, function names, library names
(`jose`, `bcryptjs`, `Zustand`), and architectural decisions are real
from the source codebase.
