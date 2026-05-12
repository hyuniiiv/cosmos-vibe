# /cosmos:observe output

> `/cosmos:observe` runs automatically at the end of `/cosmos:spawn`
> (see `skills/spawn/SKILL.md`, Step 8). The content below is the
> observe output for this run, reconstructed from the raw insights
> after the fact for inclusion here. The three `insights/*.jsonl`
> files are the authoritative source; the synthesis below is what
> observe surfaces on top of them.

## Superposition

```
cosmos:alpha    (vulnerability-hunter)   ●●●●●●●●●●●  11 insights
  └ CRITICAL: JWT has no expiration — perpetual tokens
  └ CRITICAL: refresh route clockTolerance: 999_999_999 — exp ignored even if present
  └ CRITICAL: cancel route trusts body.termId — cross-merchant cancellation possible

cosmos:beta     (architecture-auditor)   ●●●●●●●●       8 insights
  └ 3 auth schemes coexist with no central dispatcher
  └ revoke writes DB column but JWT verification is stateless — revocation is a no-op
  └ POST/GET on same URL use different auth schemes

cosmos:gamma    (client-dataflow)        ●●●●●●●●●●    10 insights
  └ Token dual storage (localStorage + IndexedDB) drifts on first activation
  └ [TUNNEL] Offline payment queue NEVER flushes when IDB token is null
  └ Electron CORS bypass injects Access-Control-Allow-Origin:* globally
```

## ⚡ Resonance — 3-way

**"Terminal JWT has no exp claim — tokens are effectively immortal"**
All three cosmos arrived at this independently from three different
angles:

- alpha (vuln hunter) — flagged it as CRITICAL by reading `createTerminalJWT` and `verifyTerminalJWT` for missing `setExpirationTime` / `exp` check.
- beta (architecture) — flagged it as a contract gap: token-lifetime policy is absent from `TerminalJWTPayload`.
- gamma (dataflow) — flagged it from the client side: `tokenExpiresAt` is server-managed via heartbeat, not in the JWT, so a stolen token is valid forever client-side.

Three independent lenses, same conclusion. **Ship with confidence: this is real, this is systemic, not a transcription error from any one reviewer.**

## ⚡ Resonance — 2-way

**"refresh route's clockTolerance: 999_999_999 makes the (already-missing) exp claim moot"**
alpha and beta both flagged. gamma did not look at the route code, so its silence is expected, not evidence against.

## 🌀 Uncertainty

There was no head-on disagreement. The three cosmos investigated overlapping but mostly disjoint sub-regions of the same system. This is the expected shape when strategies are *complementary lenses* on the same code, rather than *competing approaches* to the same problem. Compare to a "implement-a-rate-limiter" run where strategies actively diverge on algorithm choice.

## ✨ Tunneling

**gamma: offline payment queue silently never flushes.**

The audit goal was *security*. gamma — following the token through client storage layers — discovered a **money bug**: if `activateTerminal` only writes to `localStorage` but not `IndexedDB`, then `flushOfflineQueue` reads `deviceToken` from IDB, sees `null`, and returns `0 flushed` silently. Offline payments accumulate and never reach the server.

This is the canonical shape of a `[TUNNEL]` insight: cosmos was working inside one assumed boundary (security audit) and broke through into adjacent territory (revenue loss).

The lesson for cosmos design: **strategies that follow data, not categories, find adjacent bugs categorical audits miss.**

## ⚡ Quantum Jump

None observed in this run. No cosmos read another's insights and changed direction mid-flight. All three ran their lenses independently to completion.

## 🚧 Unresolved Blockers

None — all three cosmos completed their pass.

## Production decision (what the developer shipped)

Three concrete fixes pulled directly from the insights:

1. **Add `exp` to terminal JWT** (`setExpirationTime("24h")` in `createTerminalJWT`, remove the absurd `clockTolerance` on refresh). 3-way resonance → highest priority.
2. **Fix `cancel-request` to use `auth.payload.termId`** instead of `body.termId`. alpha-only finding but trivially exploitable cross-merchant — same-day fix.
3. **Make `activateTerminal` write both storage layers atomically.** gamma's tunneling find — not a security fix but the same single audit prevented a revenue regression.

Audit complete. No cosmos was `crystallize`'d — the deliverable was a set of fixes, not a single implementation to merge.
