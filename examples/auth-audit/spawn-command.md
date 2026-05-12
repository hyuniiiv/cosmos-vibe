# Spawn command

```
/cosmos:spawn \
  --goal "Audit terminal JWT and payment authentication for security and data-flow risks" \
  --strategies "vulnerability-hunter,architecture-auditor,client-dataflow"
```

```
🌌 Spawning 3 cosmos for security audit...

  cosmos:alpha    vulnerability-hunter      cosmos/alpha
  cosmos:beta     architecture-auditor      cosmos/beta
  cosmos:gamma    client-dataflow           cosmos/gamma

Each cosmos works in its own git worktree.
Insights stream to .quantum/<name>/insights.jsonl as they appear.
```

## Strategy intent

- **alpha — vulnerability-hunter:** classical security audit. Find CWE-class bugs: broken auth, IDOR, weak crypto, rate-limit bypass, info leaks. Severity-graded.
- **beta — architecture-auditor:** systemic shape, not bugs. Where are the contracts broken? Is auth centralized? Where is policy duplicated? What does the type system permit that the runtime forbids?
- **gamma — client-dataflow:** follow the token. Where is it stored? How does it move between localStorage / IndexedDB / Electron main / preload? What syncs to the server? Where could a state mismatch lose money?

Three lenses on the same code. Resonance across lenses = systemic issue, not a local bug.
