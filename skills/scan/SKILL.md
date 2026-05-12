---
name: cosmos:scan
description: QuantumAgent — Scan the codebase for code-level quantum phenomena. Detects type-system bypasses (tunnel), untested code (decoherence), and feature flags (superposition). The micro scale of QuantumAgent — function/file/symbol-level quantum state tracking.
---

# cosmos:scan

Scan the codebase for **code-level quantum phenomena** and record them to
`.quantum/code/findings.jsonl`. The micro-scale layer of QuantumAgent —
while `/cosmos spawn` works at the cosmos scale (parallel implementations)
and `/cosmos singularity` at the project scale (macro events), `/cosmos scan`
works at the code scale (function/file/symbol quantum state).

Three phenomena detected:

| Type | Quantum analog | Code reality |
|------|---------------|--------------|
| **`code-tunnel`** | Particle passes through classically-forbidden barrier | Code bypasses the type system: `as unknown as`, `@ts-ignore`, `# type: ignore`, `eval`, dynamic property assignment |
| **`code-decoherence`** | Phase information lost to environment | Untested source file: state is "decohered" because nothing observed (= tested) it |
| **`code-superposition`** | System exists in multiple states simultaneously | Feature flags + A/B test branches: code that runs in *multiple states* at the same time, the active branch selected by environment |

This is the **first-class implementation of the third scale** of QuantumAgent's
multi-scale vision (micro/macro/cosmos). Findings are append-only, JSONL,
and integrate with `/cosmos observe` for cross-scale resonance detection.

## Trigger

```
/cosmos scan [--paths "<glob1,glob2,...>"] [--languages "<ts,py,go,...>"] [--include-tests] [--git-churn-threshold N]
```

Common forms:

```bash
# Default — scan everything from repo root, auto-detect languages
/cosmos scan

# Specific paths
/cosmos scan --paths "src/,lib/"

# Specific languages
/cosmos scan --languages "ts,py"

# Include git-churn-based code-jump detection (last 10 commits)
/cosmos scan --git-churn-threshold 50
```

## Execution Steps

### Step 1 — Detect repo root and prepare

```bash
git rev-parse --show-toplevel
mkdir -p <repo_root>/.quantum/code
touch <repo_root>/.quantum/code/findings.jsonl
```

Store the timestamp `<ts>` (ISO 8601 UTC) for this scan run.

### Step 2 — Parse arguments

- `--paths`: comma-separated list of glob roots. Default: `.` (repo root, all files).
- `--languages`: comma-separated short language codes (`ts`, `tsx`, `js`, `jsx`, `py`, `go`, `rs`). Default: auto-detect from files present.
- `--include-tests`: by default, files matching `*.test.*`, `*.spec.*`, `tests/`, `test/`, `__tests__/`, `__test__/` are EXCLUDED from tunnel/superposition scans (test code legitimately uses bypasses). Pass this flag to include them.
- `--git-churn-threshold`: integer line count. If positive, perform code-jump detection: any file with > N lines churned in last 10 commits is recorded as `code-jump`. Default: 0 (disabled).

### Step 3 — Detect `code-tunnel` (type-system bypasses)

Patterns to grep (per language). All matches are appended to `findings.jsonl`.

**TypeScript / JavaScript** (files matching `*.ts`, `*.tsx`, `*.js`, `*.jsx`):

| Pattern (regex) | subtype |
|----------------|---------|
| `\bas unknown as\b` | `as-unknown-as` |
| `\bas any\b` | `as-any` |
| `// @ts-ignore` | `ts-ignore` |
| `// @ts-nocheck` | `ts-nocheck` |
| `// @ts-expect-error` | `ts-expect-error` |
| `\beval\s*\(` | `eval` |
| `new Function\s*\(` | `function-constructor` |
| `Object\.defineProperty\(\s*(window\|global\|globalThis)` | `define-property-global` |

**Python** (files matching `*.py`):

| Pattern | subtype |
|---------|---------|
| `#\s*type:\s*ignore` | `type-ignore` |
| `\bcast\(\s*Any\b` | `cast-any` |
| `\beval\s*\(` | `eval` |
| `\bexec\s*\(` | `exec` |
| `\b__import__\s*\(` | `dynamic-import` |
| `setattr\([^,]+,\s*['"]_+` | `setattr-private` |

**Go** (files matching `*.go`):

| Pattern | subtype |
|---------|---------|
| `\binterface\{\}` (in function signatures only — too noisy elsewhere) | `empty-interface` |
| `\.\((interface\{\}\|any)\)` | `type-assertion-any` |
| `unsafe\.\w+` | `unsafe` |

**Rust** (files matching `*.rs`):

| Pattern | subtype |
|---------|---------|
| `\bunsafe\s*\{` | `unsafe-block` |
| `\.unwrap\(\)` (warn — not strictly tunnel but invariant-bypass) | `unwrap` |
| `mem::transmute` | `transmute` |

Bash skeleton (TypeScript example):

```bash
# Find type-system bypasses in TS/TSX files
for pattern_subtype in \
  "as unknown as|as-unknown-as" \
  "as any|as-any" \
  "// @ts-ignore|ts-ignore" \
  "// @ts-nocheck|ts-nocheck" \
  "// @ts-expect-error|ts-expect-error"
do
  pat="${pattern_subtype%|*}"
  subtype="${pattern_subtype#*|}"
  # use ripgrep or grep -rn with appropriate flags
  rg -n --type ts --type tsx -e "$pat" "$root" 2>/dev/null | while IFS=: read -r file line content; do
    # skip test files unless --include-tests
    case "$file" in
      *.test.* | *.spec.* | */tests/* | */__tests__/* )
        [ "$include_tests" = "1" ] || continue ;;
    esac
    # emit JSON line
    echo "{\"type\":\"code-tunnel\",\"subtype\":\"$subtype\",\"file\":\"${file#$root/}\",\"line\":$line,\"evidence\":$(printf '%s' "$content" | python -c 'import json,sys; print(json.dumps(sys.stdin.read().strip()))'),\"ts\":\"$ts\"}" >> "$repo_root/.quantum/code/findings.jsonl"
  done
done
```

In practice the agent executing this skill should use `Grep` tool calls (one per pattern + language) and assemble the JSON lines, then write all of them to `findings.jsonl` with a single bash append.

### Step 4 — Detect `code-decoherence` (untested source files)

For each source file in scanned paths, look for a corresponding test file using these heuristics (first match wins):

| Source pattern | Test patterns to look for |
|---------------|---------------------------|
| `src/foo.ts` | `src/foo.test.ts`, `src/foo.spec.ts`, `tests/foo.test.ts`, `test/foo.test.ts`, `__tests__/foo.test.ts` |
| `src/foo.py` | `tests/test_foo.py`, `tests/foo_test.py`, `test_foo.py`, `foo_test.py` |
| `src/foo.go` | `src/foo_test.go` (same dir is conventional) |
| `src/foo.rs` | inline `#[cfg(test)] mod tests` inside foo.rs OR `tests/foo.rs` |

If NO corresponding test exists, append:

```json
{"type":"code-decoherence","file":"src/foo.ts","reason":"no test file found","searched":["src/foo.test.ts","src/foo.spec.ts","tests/foo.test.ts"],"ts":"<ts>"}
```

Exclude files whose own name matches test patterns (those are tests, not source).

### Step 5 — Detect `code-superposition` (feature flags / A/B branches)

Patterns to grep (per language):

**TypeScript / JavaScript:**
- `process\.env\.[A-Z_]+_FLAG\b`
- `process\.env\.FEATURE_[A-Z_]+`
- `getFeatureFlag\(`
- `featureFlags?\[\s*['"]?`
- `if\s*\([^)]*\.enabled\b`

**Python:**
- `os\.environ\.get\(\s*['"]FEATURE_`
- `settings\.FEATURE_[A-Z_]+`
- `if.*feature_flag.*\.enabled`

For each match append:

```json
{"type":"code-superposition","file":"src/foo.ts","line":42,"evidence":"if (process.env.FEATURE_NEW_UI)","subtype":"env-feature-flag","ts":"<ts>"}
```

### Step 6 — (Optional) Detect `code-jump` via git churn

If `--git-churn-threshold N` was supplied with `N > 0`:

```bash
# For each file changed in last 10 commits, count net lines changed
git -C <repo_root> log -10 --numstat --pretty=format:"" \
  | awk 'NF>=3 && $1 ~ /^[0-9]+$/ { totals[$3] += $1 + $2 } END { for (f in totals) print totals[f], f }' \
  | sort -rn \
  | while read churn file; do
      [ "$churn" -ge "$N" ] || break
      echo "{\"type\":\"code-jump\",\"file\":\"$file\",\"churn_lines\":$churn,\"window\":\"last-10-commits\",\"ts\":\"<ts>\"}" >> "$repo_root/.quantum/code/findings.jsonl"
    done
```

A high-churn file is *not necessarily* a problem — it might be normal feature work. But a *recent* sudden churn often signals a discontinuous architectural shift (`code-jump`) worth examining.

### Step 7 — Report summary

After all findings appended, output:

```
🔬 Code scan complete

   Files scanned:     <total>
   Findings:          <total>

   ⚛️  Tunnels (type-system bypass):    <count>   <bar>
   🌫️  Decoherence (untested files):    <count>   <bar>
   ☯️  Superposition (feature flags):    <count>   <bar>
   ⚡ Jumps (high recent churn):        <count>   <bar>   (if --git-churn-threshold)

   Top tunnel hotspots:
     <file>:<line>  <subtype>  <evidence>
     <file>:<line>  <subtype>  <evidence>
     ...

   Top decoherent files:
     <file>  (no test found)
     <file>  (no test found)

   Stored at: .quantum/code/findings.jsonl
```

## Integration with /cosmos observe

`/cosmos observe` (v4.0+) reads `.quantum/code/findings.jsonl` and surfaces:
- Total counts per finding type
- Cross-scale resonance: a `code-tunnel` in a file that multiple cosmos
  modified during their runs becomes a candidate for project-level decision

## When to scan

**Run when:**
- Onboarding a new codebase — get a quantum-state baseline
- Before a major refactor — know where the tunnels are
- Before a security review — `code-tunnel` findings are review-worthy
- Periodically (CI) — track decoherence over time as test coverage evolves

**Don't run when:**
- Active development on a single file (use lint/type-check instead)
- Vendored / generated code (use `--paths` to exclude)

## Format reference

`.quantum/code/findings.jsonl` is append-only JSONL. Schemas by type:

```jsonl
{"type":"code-tunnel","subtype":"<subtype>","file":"<rel-path>","line":<n>,"evidence":"<text>","ts":"<ISO>"}
{"type":"code-decoherence","file":"<rel-path>","reason":"no test file found","searched":["<path>","<path>"],"ts":"<ISO>"}
{"type":"code-superposition","subtype":"<subtype>","file":"<rel-path>","line":<n>,"evidence":"<text>","ts":"<ISO>"}
{"type":"code-jump","file":"<rel-path>","churn_lines":<n>,"window":"last-10-commits","ts":"<ISO>"}
```

Re-running `/cosmos scan` appends new findings; the file is the *history*
of scans, not a snapshot. To get the latest state, take the most recent
timestamp group.

## Why this completes the architecture

QuantumAgent's three scales — cosmos / project / code — were the original
multi-scale vision. v1.2 shipped the macro layer (project spin + singularities).
v3.2 shipped Path B (canonical quantum mechanics for Layer 3). **v4.0
ships the micro layer**, completing the architecture:

```
🌌 Cosmos scale   (v1.x) — /cosmos spawn — N parallel implementations
🌍 Project scale  (v1.2) — /cosmos spin + /cosmos singularity — macro context
⚛️ Code scale     (v4.0) — /cosmos scan — function/file/symbol quantum state
```

Cross-scale resonance becomes possible: a `code-tunnel` finding in `src/auth.ts`
plus a cosmos-level Resonance on "JWT no expiration" plus a project-level
singularity "auth migration" = three independent signals pointing at the
same problem from different scales. This is the multi-scale quantum
mechanics of development the original vision called for.
