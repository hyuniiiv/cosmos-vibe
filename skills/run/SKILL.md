---
name: cosmos:run
description: QuantumAgent — Execute a declarative quantum experiment defined in a YAML file. Parses spin/singularity/spawn config from experiment.qa.yaml and orchestrates the full workflow. The CI/CD-friendly entry point to QuantumAgent — quantum experiments as code.
---

# cosmos:run

Execute a **declarative quantum experiment** from a YAML file. This is the
programmable layer of QuantumAgent — experiments become version-controlled
artifacts that can be reviewed, diffed, and re-run.

While `/cosmos spawn` is imperative ("do this now"), `/cosmos run` is
declarative ("here's the experiment, execute it"). The same goal can be
captured as code, committed to git, and re-executed identically.

## Trigger

```
/cosmos run <path-to-yaml>
```

Example:

```bash
/cosmos run experiments/rate-limiting.qa.yaml
/cosmos run my-experiments/auth-review.qa.yaml
```

## YAML schema (v1)

```yaml
# experiment.qa.yaml — schema version 1

experiment: <kebab-case identifier>     # required, string
version: 1                              # optional, schema version, default 1

# Optional macro-layer setup (applied BEFORE spawn)
spin:                                   # optional block
  name: <string>                        # required if spin block present
  type: <string>                        # optional
  description: <string>                 # optional
  constraints:                          # optional list
    - <constraint string>
    - <constraint string>

singularities:                          # optional block, list
  - name: <string>                      # required
    invalidates:                        # required list
      - <pattern>
    trigger: <string>                   # optional
    description: <string>               # optional

# Required: the spawn configuration
spawn:                                  # required block
  goal: <string>                        # required

  # Two forms — pick ONE. Cannot use both.
  #
  # Form A — simple list (uniform model):
  strategies:                           # 2-5 unique entries
    - <strategy>
    - <strategy>

  # Form B — verbose (per-cosmos model, v3.3+):
  cosmos:                               # 2-5 unique entries
    - { strategy: <strategy>, model: <model-name> }
    - { strategy: <strategy>, model: <model-name> }

  entanglement: <mode>                  # optional: none|passive|active|strict
                                        # default: passive
  models:                               # optional list, only with strategies form
    - <model-name>                      # length must match strategies
    - <model-name>
```

**Validation rules:**
- Top-level keys: `experiment`, `version`, `spin`, `singularities`, `spawn`. Reject unknown keys.
- `experiment` must be present and a non-empty string.
- `spawn` must be present with `goal` (string) and EITHER `strategies` (list of 2-5 unique strings) OR `cosmos` (list of 2-5 unique entries with `strategy` field) — not both.
- `spawn.entanglement` if present must be one of `none`, `passive`, `active`, `strict`.
- `spawn.models` (optional, only with `strategies` form) must match `strategies` length.
- `spawn.cosmos` entries each require `strategy`; `model` is optional per entry.
- `spin.name` required if `spin` block exists.
- Each `singularities[]` entry needs `name` and `invalidates`.
- Strategy uniqueness (across forms) check enforces Pauli Exclusion at the declaration layer.

## Execution Steps

### Step 1 — Detect repo root

```bash
git rev-parse --show-toplevel
```

Store as `<repo_root>`.

### Step 2 — Resolve YAML path

If the argument is a relative path, resolve against `<repo_root>`. If the file does not exist:

```
❌ Experiment file not found: <path>
   Usage: /cosmos run <path-to-yaml>
   Templates available at: experiments/_template.qa.yaml
```

Then stop.

### Step 3 — Parse and validate YAML

Read the file. Parse as YAML. Apply validation rules from the schema above. On error:

```
❌ Invalid experiment YAML at <path>:
   <specific validation error>

   See schema: experiments/_template.qa.yaml or /cosmos run --schema
```

Then stop. Common errors to surface explicitly:
- Missing `experiment` → "Required field `experiment` missing at top level."
- Missing `spawn` → "Required block `spawn` missing."
- Missing `spawn.goal` → "Required field `spawn.goal` missing."
- Empty/short `spawn.strategies` → "`spawn.strategies` must list 2 to 5 unique strategies."
- Duplicate strategies → "Pauli Exclusion: strategy `<name>` listed more than once."
- Unknown `entanglement` value → "`spawn.entanglement` must be one of: none, passive, active, strict."
- Unknown top-level key → "Unknown key `<key>` at top level. Allowed: experiment, version, spin, singularities, spawn."

### Step 4 — Report parsed experiment

Before executing anything, summarize what will happen:

```
🧪 Experiment: <experiment-name> (schema v<version>)

   Spin operations:        <yes if spin block / no>
   Singularity operations: <N events / none>
   Spawn:
     Goal:           <goal>
     Strategies:     <strategy1>, <strategy2>, <strategy3>
     Entanglement:   <mode>

   Executing...
```

### Step 5 — Apply spin (if `spin` block present)

If the YAML contains a `spin:` block, invoke the same logic as `/cosmos spin`:
- Read existing `<repo_root>/.quantum/project/spin.json` if any
- Merge the YAML's spin block with existing values (the YAML wins on conflicts; `established` is preserved)
- Write `<repo_root>/.quantum/project/spin.json`
- Output: `✨ Spin applied: <name>`

If no `spin:` block in the YAML, skip silently.

### Step 6 — Apply singularities (if `singularities` block present)

For each entry in the `singularities:` list:
- Generate ISO 8601 timestamp `<ts>` (current time, or YAML-provided `ts` if present)
- Build the JSON event:
  ```json
  {"name":"<name>","ts":"<ts>","trigger":"<trigger>","invalidates":[...],"description":"<description>"}
  ```
- Append to `<repo_root>/.quantum/singularities/events.jsonl`
- Output: `☄️  Singularity declared: <name>`

If no `singularities:` block, skip silently.

### Step 7 — Execute spawn

Build the equivalent `/cosmos spawn` arguments from the `spawn:` block:
- `--goal "<goal>"`
- `--strategies "<comma-joined strategies>"`
- `--entanglement <mode>` (if not default)
- `--models "<comma-joined>"` (if either Form A `models:` or Form B `cosmos[].model` is present)

For **Form B (cosmos verbose form)**: extract `strategy` and `model` from each entry into parallel lists for the underlying spawn call.

Then invoke the same execution flow as `/cosmos spawn` (Steps 2 through 8 of `skills/spawn/SKILL.md`).

The macro context loaded in Step 2.5 of spawn will now include the spin and singularities applied in Steps 5 and 6 above.

### Step 8 — Echo experiment provenance

Add a `run` marker insight to each cosmos's namespace AFTER spawn dispatches but BEFORE agents begin:

```bash
echo '{"type":"run","experiment":"<experiment-name>","schema_version":<version>,"yaml_path":"<resolved-path>","ts":"<now>"}' \
  >> <repo_root>/.quantum/<name>/insights.jsonl
```

This makes every insight traceable back to the originating experiment file. Auditors can answer "which experiment produced this insight?" by reading the first line of the JSONL.

### Step 9 — Auto-observe completion

Identical to `/cosmos spawn` Step 8 — when all agents return, `/cosmos observe` runs automatically.

## Why declarative experiments

**Reproducibility** — the same YAML always produces the same spawn configuration. Discoveries depend on agent runs, but the experiment design itself is fixed and version-controlled.

**Review** — experiment files can be reviewed in pull requests. "Why are we testing these three strategies?" becomes a discussion in git, not a Slack thread.

**Re-execution** — `/cosmos run experiments/auth-review.qa.yaml` always means the same thing. Useful for periodic audits ("run the security audit every quarter").

**CI/CD** — quantum experiments can run on a schedule, in response to triggers, or as part of release gates.

**Composition** — multiple experiments can share spin and singularities through the same YAML file or evolve them across files.

## When to use `/cosmos run` vs `/cosmos spawn`

| Use `/cosmos spawn` when | Use `/cosmos run` when |
|--------------------------|------------------------|
| Quick one-off exploration | The experiment will be repeated |
| Strategies are still being chosen | Strategies are stable |
| You're prototyping the question | The question is well-defined |
| No need for audit trail beyond `.quantum/` | Provenance ("which experiment produced this?") matters |

Both ultimately call the same underlying spawn logic — `/cosmos run` is `/cosmos spawn` with a declarative façade and macro-layer integration.

## Schema versioning

The `version:` field declares the YAML schema version. Current: `1`. If absent, `1` is assumed.

Future schema versions may add fields. Older schema files remain readable — `/cosmos run` reads `version` to determine which validation rules to apply.

## Format reference

See `experiments/_template.qa.yaml` for an annotated template, and `experiments/rate-limiting.example.qa.yaml` for a real-world example.
