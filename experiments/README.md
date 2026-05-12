# `experiments/` — declarative quantum experiments (v2.0+)

This directory holds **declarative QuantumAgent experiments** — YAML files that
describe a quantum exploration completely, end-to-end. Run any of them with:

```
/cosmos run experiments/<name>.qa.yaml
```

Experiments are version-controlled artifacts. Same YAML, same configuration,
every time. The exploration outputs (insights, branches) still depend on agent
runs, but the *design of the experiment* is fixed.

## Files in this directory

- **`_template.qa.yaml`** — annotated template with every field documented.
  Copy this when starting a new experiment.
- **`rate-limiting.example.qa.yaml`** — real example showing a 3-strategy
  exploration of rate limiting algorithms. Runnable as-is.

## Naming convention

- `<short-kebab-name>.qa.yaml` for actual experiments
- `<name>.example.qa.yaml` for documented examples checked into the repo
- `_template.qa.yaml` (leading underscore) for the canonical template

## When to use `/cosmos run` vs `/cosmos spawn`

| Use `/cosmos spawn` | Use `/cosmos run` |
|---------------------|-------------------|
| Quick one-off question | The experiment will be repeated |
| Strategies still being chosen | Strategies are stable |
| You're prototyping the question | Question is well-defined |
| No audit trail beyond `.quantum/` | Provenance matters |

Both call the same underlying spawn logic. `/cosmos run` adds:
- YAML schema validation
- Macro-layer setup (spin + singularities) before spawn
- Experiment provenance tagged into every cosmos's first insight

## CI/CD integration

Quantum experiments can run on a schedule, in response to triggers, or as
part of release gates. Example workflow steps:

```yaml
# .github/workflows/quarterly-audit.yml (sketch)
on:
  schedule:
    - cron: '0 0 1 */3 *'   # first day of each quarter

steps:
  - uses: actions/checkout@v4
  - name: Run security audit experiment
    run: claude /cosmos run experiments/security-audit.qa.yaml
  - name: Upload .quantum/ as artifact
    uses: actions/upload-artifact@v4
    with:
      name: quantum-memory-${{ github.run_id }}
      path: .quantum/
```

The `.quantum/` directory becomes a recurring artifact — insights accumulate
over time and can be compared across runs.

## Schema versioning

Each YAML file declares `version: 1`. Future schema versions may add fields;
older files remain readable. See `skills/run/SKILL.md` for the full schema
reference and validation rules.
