# QuantumAgent — Example runs

This directory collects real `/cosmos:*` workflow outputs from actual projects.

## Why this exists

The README and INTEGRATIONS docs explain *how* QuantumAgent works in the abstract. This directory shows *what an actual run produced* — the spawn command, real `.quantum/*.jsonl` insights, the `observe` snapshot, and the crystallize report. Real signal-to-noise from real cosmos doing real work.

## Status

No real runs collected yet. We deliberately do **not** ship fabricated examples — the difference between "this is what the framework looks like" (covered by the README's visualization section) and "this is what *a real session produced*" matters for credibility.

If you've run cosmos on a goal and the result is worth sharing, contributions are welcome. See [`_template/`](_template/) and the contribution guide below.

## Contributing a run

1. **Run cosmos on a real goal** in any of the supported environments. Keep it small enough that a reader can follow the whole story (one focused utility, one well-bounded feature).
2. **Capture the artifacts** while the cosmos is alive (don't `stop` until you've copied):
   - The spawn command you used (with exact `--goal` and `--strategies`)
   - Each cosmos's `.quantum/<name>/insights.jsonl` (raw, unedited)
   - The full `observe` output (run it once with all cosmos active)
   - The full `crystallize` report (run it on the winning cosmos)
3. **Copy `_template/` to `<your-run-name>/`** and fill in the placeholders. Don't normalize or pretty-print the JSONL — keep it as the agents wrote it.
4. **Sanitize** any secrets, internal URLs, customer data, or proprietary information. The bundled `.quantum/` files become public.
5. **Add a brief `README.md`** at the top of your run directory explaining:
   - Domain context (without leaking anything)
   - Why you picked the strategies you did
   - One sentence about what you'd ship in production after seeing the results
6. **Open a PR** titled `examples: <your-run-name>`.

The bar is "would a stranger reading this learn something concrete about how cosmos behaves?" not "is this perfect" — partial or messy real runs are more valuable than polished fakes.

## Suggested first runs (looking for contributors)

If you're picking a goal, these tend to produce illustrative quantum signals:

- **`debounce`** — leading / trailing / leading-and-trailing — usually produces strong resonance on the core timing logic and uncertainty on the leading-edge behavior.
- **`slug normalization`** — regex / whitelist / Unicode-aware — usually surfaces a `[TUNNEL]` insight around `normalize("NFKD")`.
- **`rate limiter`** — token-bucket / sliding-window / fixed-window — typical real-world cosmos run, used as the example in the README.
- **`url parsing`** — regex / WHATWG URL / split-and-validate — uncertainty around edge cases (port:0, userinfo, etc).
- **`exponential backoff`** — full jitter / decorrelated / capped — strong resonance on jitter being mandatory, uncertainty on cap shape.

## Layout

```
examples/
├── README.md               (this file)
├── _template/              (copy this for a new run)
│   ├── README.md           (per-run context)
│   ├── spawn-command.md    (the exact /cosmos:spawn invocation)
│   ├── insights/
│   │   ├── alpha.jsonl     (raw insights, append-only)
│   │   ├── beta.jsonl
│   │   └── gamma.jsonl
│   ├── observe-snapshot.md (full /cosmos:observe output)
│   └── crystallize-report.md (full /cosmos:crystallize output)
└── <your-run-name>/        (contributed runs land here)
```

Empty `_template/` slots are intentional — they signal "this is where the agent's real output goes". A contribution that fills them in correctly is more valuable than a polished essay.
