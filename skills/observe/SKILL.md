# cosmos:observe

Show the current superposition snapshot: all cosmos insights, resonance signals,
and uncertainty map. Uses Claude's semantic judgment — no vector database needed.

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

Parse each line as JSON: `{"content": "<text>", "ts": "<timestamp>"}`

Build a map: `cosmos_id → [insights sorted by ts]`

If `.quantum/` is empty or missing, output:
```
(no cosmos active — run /cosmos spawn first)
```

### Step 3 — Output superposition snapshot

For each cosmos (sorted alphabetically), output:

```
🌌 cosmos:<name>  (<N> insights)  — <strategy>
   └ <most recent insight, truncated to 120 chars>
   └ <second most recent insight, truncated to 120 chars>
```

### Step 4 — Detect Resonance and Uncertainty

Using all insights from Step 2, perform two analyses:

**Resonance** — decisions where 2+ cosmos independently reached the same conclusion.
These are answers you can trust regardless of which strategy you pick.
- List each resonant decision as one line
- Note how many cosmos converged on it

**Uncertainty** — decisions where cosmos reached genuinely different conclusions.
These are real tradeoffs with no universal answer. The developer must choose.
- List each uncertain decision as one line
- Briefly name what each cosmos chose

**Decoherence** — if a cosmos appears to have abandoned its core strategy and
simply copied another cosmos, flag it. Healthy entanglement is influence, not
wholesale adoption.

### Step 5 — Output quantum map

```
⚡ Resonance — trust these (all strategies converged):
   "<decision>" — N cosmos independently concluded this
   "<decision>" — N cosmos independently concluded this

🌀 Uncertainty — your call (strategies diverged):
   "<decision>" — alpha: <choice A>  |  beta: <choice B>  |  gamma: <choice C>
   "<decision>" — alpha: <choice A>  |  beta/gamma: <choice B>

⚠️  Decoherence detected: (only if applicable)
   cosmos:<name> appears to have lost its <strategy> identity — review its insights
```

If no resonance detected:
```
⚡ Resonance:
   (none yet — cosmos may still be in early stages)
```

### Output philosophy

- Resonance = the quantum signal that this answer is robust. Multiple independent
  paths found it. Ship with confidence.
- Uncertainty = the Heisenberg limit of this problem. You cannot optimize all
  dimensions simultaneously. Make a conscious choice.
- Decoherence = a cosmos that lost coherence. Its insights may still be valuable
  but its strategy is no longer a true independent sample.
