# cosmos:observe

Show the current superposition snapshot: all universe insights and detected
entanglements. Uses Claude's semantic judgment rather than cosine similarity.

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

For each file that exists, parse each line as JSON:
`{"content": "<text>", "ts": "<timestamp>"}`

Build a map: `universe_id → [insights sorted by ts]`

If `.quantum/` is empty or missing, output:
```
(no universes active — run /cosmos spawn first)
```

### Step 3 — Output superposition snapshot

For each universe (sorted alphabetically), output:

```
🌌 Universe <name>  (<N> insights)
   └ <most recent insight, truncated to 100 chars>
   └ <second most recent insight, truncated to 100 chars>
```

Example:
```
🌌 Universe alpha  (12 insights)
   └ JWT sliding window expiry: access 15m, refresh 7d with rotation
   └ Chose RS256 over HS256 for key rotation support

🌌 Universe beta  (9 insights)
   └ Redis hash TTL 24h, no sliding window — simpler but less flexible
   └ Session store key: sess:<user_id>:<device_id>

🌌 Universe gamma  (14 insights)
   └ OAuth2 refresh token rotation + sliding expiry on access token
   └ Convergence with alpha detected: both using sliding expiry
```

### Step 4 — Detect entanglements

Using the full dataset read in Step 2 (not just the 2 displayed insights),
analyze all insights semantically. Identify pairs of universes where the
same pattern, strategy, or conclusion is emerging independently.

For each detected entanglement pair:
- Name the pair (e.g., `alpha ↔ gamma`)
- Explain WHY they are entangled in one sentence (what pattern is converging)

Also identify strong divergences that are interesting:
- Pairs exploring fundamentally different approaches to the same sub-problem

### Step 5 — Output entanglement map

```
⚛️  Entanglements:
   alpha ↔ gamma  — both converging on sliding window token expiry strategy
   beta  ↔ gamma  — both handling refresh token rotation, different TTL values

🔀 Notable divergences:
   alpha vs beta  — stateless JWT (alpha) vs stateful Redis session (beta): fundamentally different trust models
```

If no entanglements:
```
⚛️  Entanglements:
   (none detected yet — agents may still be in early stages)
```
