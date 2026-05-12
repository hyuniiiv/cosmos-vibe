---
name: cosmos:observe
description: QuantumAgent — Inspect the live superposition of running cosmos agents. Read insights, detect resonance (agreement), uncertainty (divergence), tunneling, and condensate signals across all cosmos namespaces.
---

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

Parse each line as JSON. Current schema (preferred):
```
{"type": "<type>", "content": "<text>", "ts": "<timestamp>"}
```

Legacy compatibility:
- If `type` is missing → treat as `"discovery"`
- If `content` starts with `[TUNNEL]` → treat as `type: "tunnel"`
- If `content` starts with `[JUMP]` → treat as `type: "jump"`

Build a map: `cosmos_id → [insights sorted by ts]`. Also build a secondary
index `type → [insights]` for grouped reporting in Step 4.

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

**Degeneracy** — if two or more cosmos with *different* strategies arrived at
functionally identical implementations (same library, same algorithm, same concrete
design), that is Degeneracy: the problem had a single natural solution regardless
of approach. Flag this separately from Resonance (which is about conclusions, not
implementations being identical).

**Tunneling** — collect all insights with `type: "tunnel"` (or legacy
`[TUNNEL]` content prefix). These are solutions that bypassed assumed
constraints. List each one.

**Quantum Jump** — collect all insights with `type: "jump"` (or legacy
`[JUMP]` content prefix). These are discontinuous architectural leaps
triggered by a single entanglement read. List each one with the cosmos
it came from.

**Blockers** — collect all `type: "blocker"` insights still unresolved
(no later `type: "decision"` or `type: "discovery"` from the same cosmos
that addresses them). Surface these — they need developer attention.

### Step 5 — Output quantum map

```
⚡ Resonance — trust these (all strategies converged):
   "<decision>" — N cosmos independently concluded this
   "<decision>" — N cosmos independently concluded this

🌀 Uncertainty — your call (strategies diverged):
   "<decision>" — alpha: <choice A>  |  beta: <choice B>  |  gamma: <choice C>
   "<decision>" — alpha: <choice A>  |  beta/gamma: <choice B>

♊ Degeneracy: (only if applicable)
   cosmos:<nameA> and cosmos:<nameB> reached identical implementations despite different
   strategies — the problem has a single natural solution

⚛️  Quantum Tunneling: (only if [TUNNEL]-tagged insights exist)
   cosmos:<name>: "<insight content>"

⚡ Quantum Jump: (only if [JUMP]-tagged insights exist)
   cosmos:<name>: "<insight content>"

⚠️  Decoherence detected: (only if applicable)
   cosmos:<name> appears to have lost its <strategy> identity — review its insights
```

**Bose-Einstein Condensate check:** Fires only when ALL three conditions hold:
1. ≥3 distinct decisions are detected in the Resonance map
2. Zero Uncertainty items
3. All active cosmos participated in every resonance (no cosmos sat out a decision)

If all three hold, append:
```
🌡️  Bose-Einstein Condensate: complete convergence across all decisions.
    The goal was deterministic — any strategy would have found the same answer.
```

**Footer (always):**
```
🔬 Non-destructive observation — superposition intact.
   Run /cosmos crystallize <id> to collapse a cosmos into a definite result.
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
- Degeneracy = same implementation from different strategies. The problem itself
  points to one answer — strategy choice was irrelevant.
- Decoherence = a cosmos that lost coherence. Its insights may still be valuable
  but its strategy is no longer a true independent sample.
- Tunneling / Jump = non-obvious breakthroughs. Worth examining even if you don't
  crystallize that cosmos.
