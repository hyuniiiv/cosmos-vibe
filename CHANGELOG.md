# Changelog

All notable changes to QuantumAgent are documented here. Format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/). Versioning follows
[Semantic Versioning](https://semver.org/).

## [Unreleased]

## [4.1.0] — 2026-05-13 — verifiable concept-to-code mapping

A user-prompted honesty release. v3.3 claimed "정직성 보완" (honesty
improvements) for two small fixes; on review, the bigger issue remained:
the README headline claim "every concept has direct operational meaning —
none are decorative metaphors" was unverifiable. Users had to take it
on faith.

After v4.0 shipped, MOST concepts in the 26-row quantum table actually
do have real operational implementations — but that wasn't visible.
v4.1 makes it visible.

### Added — verifiable mapping section

New "Where every concept lives" section in both READMEs (after the
in-depth concept descriptions, before Repository layout) that cites
the specific file / skill / function where each of the 26 quantum
concepts is implemented. Concepts are classified into four tiers:

- **🧮 Real math** — Path B implements the literal quantum-mechanical
  operation. Verifiable empirically.
  - *Quantum Interference* — `superpose()` produces 1000/0 destructive
    cancellation in `examples/04_quantum_interference.py`
  - *Decoherence (math)* — `decohere()` density-matrix model in
    `python/quantumagent/quantum.py`

- **🔧 Enforced** — system has a real check, mechanism, or output.
  - *Pauli Exclusion* — `skills/spawn/SKILL.md` Step 1 rejects duplicate
    strategies with explicit error
  - *Schrödinger's Cat* — `skills/crystallize/SKILL.md` Step 5 forces
    test-pass confirmation before merge
  - *Measurement Problem* — observe ≠ crystallize is a first-class
    distinction across all skills; Python lib `observe()` vs `measure()`
  - …18 concepts total

- **🔍 Detected** — tooling automatically surfaces instances.
  - *Quantum Tunneling* — `[TUNNEL]` insight tag (spawn) + automatic
    `code-tunnel` detection in `/cosmos scan` (v4.0)
  - *Decoherence (code)* — `code-decoherence` in scan for untested files
  - …3 concepts total

- **🪞 Guideline** — documented rule, not technically enforced.
  - *No-Cloning Theorem* — Spin Preservation rule (can technically `cp -r`
    but flagged by observe Decoherence detection)
  - *Reference Frame*, *Equivalence Principle*, *Quantum Annealing*,
    *Quantum Coherence*, *cosmos-level Decoherence prevention*
  - 6 concepts total — honestly admit where the system is behavioral-only

The categorization makes the README's headline claim **falsifiable**:
anyone can click the cited file/line and verify the implementation.
The classification also makes overlaps visible — e.g., *Decoherence*
is implemented at three levels (cosmos behavioral / math / code detection),
which is honest about how reality accumulated as the system matured
from v1 to v4.

### Why this version is a separate release

v3.3 was labeled "vision-gap fills" with three real improvements (model
diversity, Layer 1↔3 interop, two small docs fixes). But that release
labeled the small docs fixes as "정직성 보완" — overselling them.
The bigger honesty gap (verifying the headline claim) wasn't addressed.

v4.1 corrects this. The release is intentionally small (docs only) —
no code changes, no behavior changes, no compatibility impact. Just
making the existing system's reality verifiable.

### Changed

- `README.md` — new "Where every concept lives — verifiable map" section
  with 26-row classification table + honest counting summary. The
  headline claim above the quantum table now points to the verification
  section.
- `README.ko.md` — same section, fully translated.
- `.claude-plugin/plugin.json` / `marketplace.json` — v4.1.0; descriptions
  mention verifiable-mapping; keyword `verifiable` added.

### Honest counting

- 🧮 Real math (Path B): 2 of 26 (Interference, Decoherence-math)
- 🔧 Enforced: 18 of 26 — most concepts have real operational mechanisms
- 🔍 Detected: 3 of 26 (Tunneling, Decoherence-code, with cross-references)
- 🪞 Guideline: 6 of 26 — honestly admit behavioral-only

Some concepts span multiple tiers (Decoherence has three implementations
across v1.x, v3.2, v4.0).

### Backward compatibility

- Zero code changes
- Zero behavior changes
- Pure documentation release

## [4.0.0] — 2026-05-12 — micro scale (code) — the original vision complete

The original multi-scale vision had three scales: cosmos / project / code.
v1.2 shipped the project scale (spin + singularities). v3.2 shipped the
Python primitives layer with canonical quantum mechanics. v4.0 ships the
**code scale** — the last unimplemented dimension of the architecture.

### Added — Micro scale: `/cosmos scan`

New skill that walks the codebase and detects code-level quantum phenomena.
Findings are appended to `.quantum/code/findings.jsonl` and surfaced by
`/cosmos observe`. Available code-level types:

| Type | Quantum analog | What it detects |
|------|---------------|----------------|
| `code-tunnel` | Particle bypasses classically-forbidden barrier | Type-system bypass: `as unknown as`, `@ts-ignore`, `# type: ignore`, `eval`, dynamic property assignment, `unsafe`, `transmute`, etc. |
| `code-decoherence` | Phase information lost to environment | Source file with no corresponding test — state never "observed" |
| `code-superposition` | System exists in multiple states simultaneously | Feature flags + A/B branches: code runs in multiple states, active branch selected by environment |
| `code-jump` *(optional)* | Discontinuous energy-level transition | High recent git churn (> threshold) — file recently restructured |

Language support out of the box: TypeScript, JavaScript, Python, Go, Rust.

Trigger: `/cosmos scan [--paths "..."] [--languages "..."] [--include-tests] [--git-churn-threshold N]`

### Added — Observe extension for code-scale findings

`/cosmos observe` (v4.0+) reads `.quantum/code/findings.jsonl` and surfaces:
- Counts per finding type (tunnels, decoherence, superposition, jumps)
- Top tunnel hotspots (file:line + subtype + evidence)
- Top decoherent files (no-test list)
- **Cross-scale signal** — when a cosmos modified a file that has a
  code-scale finding, observe surfaces it as a candidate for crystallize review

### Added — Python interop with code findings

`from_cosmos(repo_path)` now reads `.quantum/code/findings.jsonl` and exposes:
- `CosmosRun.code_findings` — list of parsed finding dicts
- `CosmosRun.code_summary()` — `{type: count}` dictionary
- The `__repr__` shows the code-findings count alongside cosmos count

Combined with cosmos-scale (`insights`) and macro-scale (`spin`,
`singularities`), one `CosmosRun` now exposes **all four scales** of the
QuantumAgent architecture as Python data.

### Vision-audit status — 100% complete on stated scales

| Vision item | Status |
|-------------|--------|
| Q1/Q2 격차 진단 | ✅ |
| Q3 거시 스케일 (project) | ✅ v1.2 |
| **Q3 미시 스케일 (code)** | ✅ **v4.0** |
| Q3 4-mode entanglement | ✅ v1.3 |
| Q4 Layer 2 YAML DSL | ✅ v2.0 |
| Q4 Layer 3 Python lib | ✅ v3.0 |
| Path B Phases 1-4 | ✅ v3.1, v3.2 |
| Asymmetric token economics | ✅ v3.3 |
| Layer 1↔3 interop | ✅ v3.3 |
| Live + post-hoc honesty | ✅ v3.3 docs |
| TUNNEL/JUMP tightening | ✅ v3.3 |

The original strategic vision is complete. Remaining items
(`ψ.spawn()` agent backend, visualization) are explicit *future direction*
items, not part of the original vision specification.

### Architecture summary

QuantumAgent now operates at **4 scales** through **3 layers**:

```
                         Layer 1            Layer 2          Layer 3
                         (CLI)              (YAML DSL)       (Python)
                         ────────────────────────────────────────────────
🌌 Cosmos scale          /cosmos spawn      experiment.qa.yaml psi() + spawn pattern
🌍 Project scale         /cosmos spin       spin: block       (read via from_cosmos)
                         /cosmos singularity singularities: block (read via from_cosmos)
⚛️ Code scale (v4.0)     /cosmos scan       (planned: scan: block)  (read via from_cosmos)
🧮 Math layer            (—)                (—)              psi/entangle/observe/measure
                                                              + Path B quantum mechanics
```

The 4 scales × 3 layers = the full architecture envisioned in the original
multi-scale design conversation.

### Changed

- `skills/scan/SKILL.md` — new (~280 LOC). Comprehensive pattern catalog
  per language, schema definitions, observe integration notes.
- `skills/observe/SKILL.md` — reads `.quantum/code/findings.jsonl`,
  outputs code-scale section.
- `python/quantumagent/interop.py` — `CosmosRun.code_findings` field,
  `code_summary()` method, `__repr__` shows count.
- `python/quantumagent/__init__.py` — version 4.0.0.
- `.claude-plugin/plugin.json` / `marketplace.json` — version 4.0.0,
  descriptions emphasize "4-scale architecture"; keywords add
  `scan`, `code-scale`, `static-analysis`.
- `README.md` / `README.ko.md` — new "Micro scale — `/cosmos scan`" section
  documenting the 4 detection types and integration. Repository layout
  reflects `skills/scan/` and `.quantum/code/findings.jsonl`.
- `CLAUDE.md` / `COSMOS.md` — Skills list adds `/cosmos scan`. Architecture
  description shifts to "4 scales".

### Backward compatibility

- All v3.x and v1.x/v2.x features continue to work unchanged
- Code-scale scanning is opt-in via `/cosmos scan`
- Projects without `.quantum/code/findings.jsonl` see no behavior change
- `from_cosmos()` returns empty `code_findings: []` when no scan has been run
- Existing examples and YAML schemas unaffected

### Dogfooding

QuantumAgent was scanned on its own Python module. Result:
3 code-decoherence findings (`core.py`, `interop.py`, `quantum.py` —
all production modules with no corresponding test files). This is an
honest self-report: the library has high empirical test coverage via the
9 example scripts, but no formal `tests/` directory. Future improvement
target — and the code-scale framework now makes that gap *visible*.

## [3.3.0] — 2026-05-12 — vision gap fills

After v3.2 completed Path B, a final audit against the strategic vision
document identified three significant gaps. This release closes them.

### Added — cosmos-level model diversity

Solves the **asymmetric token economics** and **blind-spot mitigation**
items from the vision document. Different cosmos can now use different
LLM models within a single spawn.

- `spawn` skill `--models <m1,m2,…>` flag — list of model names, length
  matching `--strategies`. Each cosmos uses its assigned model.
  - Example: `--strategies "jwt,session,oauth" --models "haiku,sonnet,opus"`
- YAML DSL extension — two new forms in `experiment.qa.yaml`:
  - **Form A (simple)**: `spawn.strategies: […]` + optional `spawn.models: […]`
  - **Form B (verbose)**: `spawn.cosmos: [{strategy, model}, …]`
- spawn Step 7 launch report shows assigned model per cosmos.
- Step 6 dispatch passes `model:` parameter to each parallel Agent call.

**Why this matters:** mitigates Resonance becoming a *false consensus* when
all cosmos share the same model's biases. Mixing Haiku (cheap exploration)
+ Sonnet (default) + Opus (capable synthesis) is now a first-class pattern.

### Added — Layer 1 ↔ Layer 3 interop

Solves the **Python lib ↔ cosmos disconnection** gap. The Python primitives
layer can now read existing cosmos output from disk and expose it as a
first-class `Wavefunction`.

- `from_cosmos(repo_path, weights="by-insight-count"|"uniform")` — reads
  `.quantum/<name>/insights.jsonl` files into a Python `CosmosRun`
  containing:
  - `psi`: Wavefunction over cosmos names (weighted by insight count or uniform)
  - `insights`: per-cosmos insight dictionaries
  - `resonance` / `uncertainty`: heuristic token-overlap signals
  - `spin`: project spin (if `.quantum/project/spin.json` exists)
  - `singularities`: macro events (if `.quantum/singularities/events.jsonl` exists)
- New `CosmosRun` dataclass with rich `__repr__`.
- New `python/quantumagent/interop.py` module (~180 LOC).
- Example `python/examples/09_cosmos_interop.py` — demonstrates loading
  the JWT-test data and composing the wavefunction with quantum primitives.

The token-overlap heuristic is intentionally crude; for semantic-quality
Resonance/Uncertainty, run `/cosmos observe`. The Python heuristic gives
a quick statistical view without an LLM call.

### Documented — micro-scale (code) as v4.0 roadmap

The third scale of the original multi-scale vision was deferred but
unclear which release. v3.3 makes it explicit: **micro-scale is v4.0**.

- `.quantum/code/<symbol>/` with static-analysis integration
- Automatic `[TUNNEL]` detection for type-system bypasses
  (`as unknown as`, `@ts-ignore`, `Object.defineProperty(window, …)`)
- Code-level decoherence model (untested code = lost coherence signal)
- Cross-scale interactions (function-level → module-level → cosmos-level)

This is a separate major track from the Python lib evolution.

### Tightened — JUMP definition + post-hoc honesty in docs

Smaller vision-audit follow-ups:

- `spawn/SKILL.md` Block C — JUMP now has explicit ✅/❌ examples:
  - ✅ Requires `read_from` citation for the triggering insight
  - ❌ Borrowing a helper function (use `discovery`)
  - ❌ Refactoring without citation (use `decision`)
  - ❌ Mid-implementation approach change without source (not a jump)
- `README.md` / `README.ko.md` "How entanglement works" section now opens
  with the **two-layer table**: live entanglement (best-effort, prompt-
  based) + post-hoc convergence (always works, semantic analysis). The
  post-hoc layer is the *actual value engine* — being explicit avoids
  overselling the live mechanism.

### Changed

- `python/quantumagent/__init__.py` — exports `CosmosRun`, `from_cosmos`; version 3.3.0.
- `python/README.md` — quantum-mode capability table updated to show v3.3
  (interop) and v4.0 (micro-scale) as separate tracks; eight examples → nine.
- `.claude-plugin/plugin.json` / `marketplace.json` — v3.3.0; descriptions
  mention model diversity, interop; keywords add `interop`, `model-diversity`.
- `experiments/_template.qa.yaml` — documents both Form A and Form B with
  model-diversity rationale.

### Backward compatibility

- All v3.0 / v3.1 / v3.2 code continues to work unchanged.
- New features are purely additive:
  - `--models` flag is optional
  - YAML Form B (`cosmos:`) is alternative to Form A — pick one
  - `from_cosmos()` is opt-in
- Existing classical-mode and quantum-mode Python code unaffected.

### Vision-audit status after v3.3

| Vision item | Status |
|-------------|--------|
| Q1/Q2 격차 진단 | ✅ Complete |
| Q3 거시 스케일 | ✅ Complete (v1.2) |
| Q3 4-mode entanglement | ✅ Complete (v1.3) |
| **Q3 미시(code) 스케일** | ⏳ **v4.0 track (explicit)** |
| Q4 Layer 2 YAML DSL | ✅ Complete (v2.0) |
| Q4 Layer 3 Python lib | ✅ Complete (v3.0) |
| Path B Phases 1-4 | ✅ Complete (v3.1 + v3.2) |
| Asymmetric token economics | ✅ Complete (v3.3) |
| Layer 1↔3 interop | ✅ Complete (v3.3) |
| Live + post-hoc honesty | ✅ Complete (v3.3 docs) |
| TUNNEL/JUMP tightening | ✅ Complete (v3.3) |
| Agent backend (ψ.spawn LLM) | ⏳ Future v3.x (optional anthropic SDK) |
| Visualization | ⏳ Future v3.x |

## [3.2.0] — 2026-05-12 — Path B complete

The final release of the QuantumAgent Path B journey. v3.1 introduced complex
amplitudes; v3.2 ships **the remaining three phases together** — CHSH Bell
inequality test, full quantum gate library, and density matrices with
decoherence. The Python layer now implements canonical quantum mechanics
end-to-end.

### Added — Phase 2: CHSH Bell-inequality test

- **`measure_in_basis(psi, angle_a, angle_b, seed=None)`** — for a 2-qubit
  state, applies Ry(-θ) rotations on each qubit and measures in the
  computational basis. Returns ±1 eigenvalues.
- **`chsh_test(psi, n_trials=2000, angles=None)`** — runs the canonical
  CHSH protocol with optimal angles (0, π/2, π/4, 3π/4). Computes the four
  correlations and returns S along with a breakdown including the classical
  bound (2) and Tsirelson bound (2√2 ≈ 2.828).

  **Verified empirically**: |Φ+⟩ achieves S ≈ 2.85, clearly violating the
  classical |S| ≤ 2 bound. No classical local-realistic theory can produce
  this — Bell's theorem in code.

### Added — Phase 3: Quantum gate library

- **`Gate` class** — unitary operator on a fixed number of qubits. Composable
  via `gate @ gate` (matrix product) and applicable via `gate @ psi` (single-
  qubit case) or `apply_gate(psi, gate, qubits=[...])` (general n-qubit).
- **`gate(name, *params)` factory** — standard gates: I, X, Y, Z, H, S, T,
  CNOT/CX, CZ, SWAP. Parametric: Rx(θ), Ry(θ), Rz(θ).
- **`apply_gate(psi, gate, qubits=[...])`** — applies a gate to specified
  qubits of any n-qubit system. Auto-expands single-qubit gates via tensor
  product with identity; two-qubit gates handle arbitrary qubit pairs.

  **Verified empirically**: |00⟩ → H₀ → CNOT(0→1) constructs the Bell state
  |Φ+⟩ exactly, matching the hardcoded `bell_state("phi+")`. The inverse
  circuit (CNOT then H) returns |00⟩ with P=1.0 — gates are unitary.

### Added — Phase 4: Density matrices + decoherence

- **`DensityMatrix` class** — represents pure or mixed quantum states via
  ρ matrices. Provides `trace`, `purity` (= Tr(ρ²)), `is_pure`. Rich repr
  showing matrix layout.
- **`density(psi)`** — converts a pure quantum wavefunction to its density
  matrix |ψ⟩⟨ψ| via outer product.
- **`decohere(rho, rate)`** — exponential decay of off-diagonal elements
  (the standard pure-dephasing model). Rate 0 = no change. Rate ∞ = full
  classical mixture (purity → 1/dim).
- **`partial_trace(rho, qubit)`** — trace out one qubit, return reduced
  density matrix on the rest. Distinguishes entangled from separable states:
  Bell state → I/2 on reduced subsystem (purity 0.5), separable state →
  pure reduced subsystem (purity 1.0).

  **Verified empirically**: partial trace of |Φ+⟩ gives diag[0.5, 0.5]
  with zero off-diagonals — maximally mixed. Decoherence at rate=10 brings
  the Bell density matrix to a classical mixture with purity → 0.5.

### Added — three new examples (verified)

- **`examples/06_chsh_test.py`** — runs CHSH on all four Bell states.
  |Φ+⟩ and |Ψ-⟩ violate the classical bound at the optimal angles
  (the others would need rotated angles — phase distinguishes them).
- **`examples/07_quantum_gates.py`** — Bell state from gates + reverse
  circuit + parametric Ry(θ) showing continuous rotation
  (P(|0⟩) sweeps 1.0 → 0.5 → 0.0 as θ: 0 → π/2 → π).
- **`examples/08_decoherence.py`** — pure → mixed via decoherence + partial
  trace = I/2 for Bell state vs. separable contrast (purity stays 1.0).

### Changed

- `python/quantumagent/quantum.py` — new module (~550 LOC) implementing all
  Phase 2-4 functionality. Pure-Python complex linear algebra, zero
  external dependencies.
- `python/quantumagent/__init__.py` — exports `Gate`, `gate`, `apply_gate`,
  `measure_in_basis`, `chsh_test`, `DensityMatrix`, `density`, `decohere`,
  `partial_trace`. Version 3.2.0.
- `python/README.md` — Quantum mode section reorganized into 4-phase table;
  roadmap updated to show **Path B complete**.
- `README.md` / `README.ko.md` — Path B status table marks all four phases
  shipped; three decisive empirical demonstrations called out.
- `.claude-plugin/plugin.json` / `marketplace.json` — version 3.2.0;
  descriptions mention Path B completion; keywords add `chsh`,
  `quantum-gates`, `density-matrix`, `decoherence`.

### Backward compatibility

- All v3.0 classical mode and v3.1 quantum mode code continues to work
  unchanged.
- New Phase 2-4 functionality is purely additive — opt in by using the
  new primitives.
- Classical-mode `constraint(...) @ psi` still raises `NotImplementedError`
  for quantum wavefunctions (gates are the correct quantum analog).

### Out of scope (future work)

These belong to future roadmap items, not Path B:

- **Agent backend** — `ψ.spawn()` invoking real cosmos via Claude Code
- **`.quantum/` interop** — reading cosmos insights as a Python wavefunction
- **Visualization** — wavefunction / entanglement graph rendering

Path B itself is complete with v3.2.

## [3.1.0] — 2026-05-12

### Added — Path B Phase 1: real quantum mechanics

QuantumAgent's Python layer (Layer 3) gains **true quantum mode**. v3.0
shipped with classical probability distributions and Born-rule-flavored
sampling; v3.1 adds complex-amplitude wavefunctions with phase, real
interference, and maximally-entangled Bell states.

Mode is auto-detected from `psi()` arguments — both modes coexist behind
the same API:

```python
classical = psi(["A", "B"], weights=[0.6, 0.4])      # real probabilities
quantum   = psi(["A", "B"], amplitudes=[1, -1])      # complex amplitudes
```

In quantum mode:
- **True Born rule**: `P(i) = |amplitude_i|²` (verified by Born-rule sampling in `measure`)
- **Phase preserved** — amplitudes carry direction in the complex plane
- **Interference** via `superpose(a, b)` — amplitudes ADD (not probabilities)
- **Bell states** via `bell_state(kind)` — maximally-entangled 2-qubit states

New primitives:
- **`superpose(a, b, weight_a=1, weight_b=1, name=None)`** — quantum superposition.
  Both inputs must be quantum-mode wavefunctions over the same set of states.
  Amplitudes add: `result_i = weight_a · a_i + weight_b · b_i`, then renormalized.
  Equal phase → constructive (amplification). Opposite phase → destructive
  (cancellation). The defining quantum operation.
- **`bell_state(kind)`** — construct one of four Bell states over 2-tuple states:
  - `"phi+"`: `(|00⟩ + |11⟩) / √2`
  - `"phi-"`: `(|00⟩ - |11⟩) / √2`
  - `"psi+"`: `(|01⟩ + |10⟩) / √2`
  - `"psi-"`: `(|01⟩ - |10⟩) / √2` (the singlet)

Wavefunction changes:
- New `amplitudes=` constructor parameter (mutually exclusive with `weights=`)
- New `is_quantum` property — True for quantum-mode wavefunctions
- New `amplitudes` attribute — list of complex numbers in quantum mode, `None` in classical
- `__repr__` shows complex amplitudes in quantum mode
- `weights` attribute always exposes `|c|²` probabilities for both modes
  (so `observe()` works identically and idempotently)
- Constraint operators (`constraint @ psi`) raise `NotImplementedError` on
  quantum wavefunctions — Hermitian operators reserved for v3.2

New examples:
- **`examples/04_quantum_interference.py`** — destructive interference demo.
  Two equal 50/50 amplitude sources combined in OPPOSITE phase produce 100/0
  outcome (verified: 1000/1000 trials hit screen-A). Classical impossible.
- **`examples/05_bell_state.py`** — Bell state correlations. 2000 trials show
  exactly 0 anti-correlated outcomes (perfect correlation), while each qubit
  alone looks like a fair coin. All four Bell state distributions displayed.

### Roadmap — Path B remaining phases

- **Phase 2 (v3.2)** — CHSH/Bell inequality test, rotation operators, Hermitian
  constraints. Distinguishes the four Bell states statistically (currently they
  look identical in the computational basis).
- **Phase 3 (v3.3)** — Unitary evolution operators, quantum gates.
- **Phase 4 (v3.4)** — Density matrices, decoherence model.

### Changed

- `python/quantumagent/core.py` — Wavefunction class extended (amplitudes
  parameter, is_quantum property, complex repr); new `superpose`, `bell_state`
  helpers; constraint guard against quantum mode.
- `python/quantumagent/__init__.py` — exports `superpose`, `bell_state`;
  version bumped to 3.1.0.
- `python/README.md` — Two-modes section, quantum example callouts, expanded
  roadmap with Phase 1–4 breakdown.
- `README.md` / `README.ko.md` — "Two modes — classical and quantum" subsection
  in the Python primitives section. Path B roadmap table.
- `.claude-plugin/plugin.json` / `marketplace.json` — version 3.1.0;
  descriptions mention Path B Phase 1; keywords add `amplitudes`, `bell-state`,
  `interference`.

### Backward compatibility

- All classical-mode v3.0 code continues to work unchanged
- `psi(states)` and `psi(states, weights=…)` behave identically to v3.0
- `weights` attribute always present (`|c|²` in quantum mode)
- `measure()` and `observe()` work for both modes via the same API
- Quantum mode is purely opt-in via the `amplitudes=` parameter

## [3.0.0] — 2026-05-12

### Added — Layer 3: Python primitives (`quantumagent` package)

QuantumAgent now ships a **pip-installable Python package** that exposes
the underlying quantum decision primitives directly in code. This is the
third layer of the architecture:

- **Layer 1 (v1.x)** — CLI (Claude Code skills): `/cosmos spawn`, etc.
- **Layer 2 (v2.0)** — YAML DSL: declarative `experiment.qa.yaml` files
- **Layer 3 (v3.0)** — Python primitives: `ψ`, `entangle`, `observe`,
  `measure`, `constraint` — composable in any Python program

The five primitives:

- **`psi(states, weights=None, name=None)`** — declare a decision as a
  probability distribution. Auto-normalized. Greek alias `ψ` exported.
- **`observe(psi)`** — non-destructive read of the current distribution.
  Returns `{state: probability}`. Idempotent. The first-class realization
  of QuantumAgent's observe-vs-measure distinction.
- **`measure(psi, seed=None)`** — Born-rule sampling collapses the
  wavefunction. Propagates to entangled partners. Subsequent calls
  return the same state (irreversible). `seed` for deterministic tests.
- **`entangle(a, b, correlation)`** — register a compatibility function
  between two wavefunctions. Measuring one conditions the other's
  distribution on compatible states. Contradictions raise explicitly.
- **`constraint(name, *, boost=…, suppress=…, where=…)`** — immutable
  operator applied via `op @ psi` returning a new wavefunction. Three
  composable patterns:
  - `where=callable` keeps only states for which the callable returns truthy
  - `boost={state: multiplier}` multiplies specific weights
  - `suppress={state: divisor}` divides specific weights

This MVP uses **real-valued probability distributions** (classical-
probability mode). Complex amplitudes and true quantum interference
are reserved for a future Path B release. The API is forward-compatible
so existing v3.0 code will continue to work in classical mode when
Path B lands.

### Added — `python/` directory

- `python/pyproject.toml` — package metadata, `pip install -e python/`
- `python/quantumagent/__init__.py` — public API exports
- `python/quantumagent/core.py` — single-file implementation of all
  primitives, ~330 LOC, zero runtime dependencies (pure stdlib)
- `python/examples/01_basic_psi.py` — declare, observe, measure
- `python/examples/02_entanglement.py` — auth × storage entanglement
  with conditional propagation
- `python/examples/03_constraint_curvature.py` — composing filter +
  boost + suppress constraints
- `python/README.md` — full guide, primitives reference, philosophy,
  CLI/DSL/Python comparison table, roadmap

### Changed

- `CLAUDE.md` / `COSMOS.md` — Skills lists reorganized into Layer 1/2/3
  architecture; Python primitives documented at top level.
- `.claude-plugin/plugin.json` — version 3.0.0; description and keywords
  reflect three-layer architecture (added `python`, `wavefunction`).
- `.claude-plugin/marketplace.json` — version 3.0.0; metadata
  description updated.
- `README.md` / `README.ko.md` — new "Python primitives — Layer 3"
  section with full example, three-layer comparison ASCII diagram,
  five-primitives table. Repository layout reflects new `python/`
  directory and labels each layer.

### Why the major version bump (v2.x → v3.0)

The Python package introduces a third paradigm: **programmable**
quantum decision primitives. Where v1.x is *imperative orchestration*
and v2.x is *declarative experiments*, v3.x is *composable
math-in-code*. Each layer adds a distinct mental model for using
QuantumAgent, and the major version bump signals that to users. The
v1.x and v2.x layers are fully preserved and continue to work
identically — v3.0 is purely additive.

### Backward compatibility

- All v1.x CLI commands work identically
- All v2.0 YAML DSL features work identically
- Python lib is **opt-in** via `pip install -e python/`
- Projects that don't adopt the Python layer notice no change
- v1.3 entanglement strict mode + heartbeat protocol unchanged

## [2.0.0] — 2026-05-12

### Added — declarative quantum experiments (YAML DSL)

QuantumAgent now offers a declarative layer on top of the imperative CLI.
Experiments become version-controlled YAML files — reproducible, reviewable,
and CI/CD-friendly. This is the **first programmable layer** of the
QuantumAgent vision: quantum exploration as code.

- **`/cosmos run <path-to-yaml>`** — new skill. Executes a declarative
  experiment defined in `experiment.qa.yaml`. Parses, validates, then
  orchestrates the workflow: apply spin (if declared) → apply singularities
  (if declared) → spawn with provenance tagging → auto-observe.

- **YAML schema v1** — declarative experiment format:
  ```yaml
  experiment: <kebab-case-id>
  version: 1

  spin:                       # optional macro-layer setup
    name: <project-name>
    constraints: [...]

  singularities:              # optional list of project-level events
    - name: <event>
      invalidates: [...]

  spawn:                      # required
    goal: "<goal>"
    strategies: [<s1>, <s2>, ...]
    entanglement: <mode>
  ```

- **Validation rules**:
  - Top-level keys restricted to `experiment`, `version`, `spin`, `singularities`, `spawn` (unknown keys rejected)
  - `experiment` and `spawn` required; `spawn.goal` and `spawn.strategies` required
  - `strategies` must be 2-5 unique entries (Pauli Exclusion at declaration time)
  - `entanglement` if present must be one of `none|passive|active|strict`
  - `spin.name` required if `spin` block present
  - Each singularity entry needs `name` and `invalidates`

- **Provenance tagging** — every cosmos's first insight in a `/cosmos run`
  is a `type: "run"` entry citing the experiment file and schema version:
  ```json
  {"type":"run","experiment":"...","schema_version":1,"yaml_path":"...","ts":"..."}
  ```
  Auditors can answer "which experiment produced this insight?" by reading
  the first line of any `insights.jsonl`.

- **`experiments/` directory** — new top-level directory for declarative
  experiments:
  - `experiments/_template.qa.yaml` — annotated schema template
  - `experiments/rate-limiting.example.qa.yaml` — runnable real example
  - `experiments/README.md` — directory guide, naming conventions,
    CI/CD integration sketch

### Why the major version bump

v2.0 introduces the first **programmable layer** of QuantumAgent — the
shift from imperative CLI to declarative experiment-as-code. This is a
paradigm-level addition, not a bug fix or minor feature. Adopting the
DSL changes how teams think about exploration (one-off question vs.
reproducible experiment).

The CLI layer (v1.x) is fully preserved and continues to work identically.

### Changed

- `CLAUDE.md` / `COSMOS.md` — Skills list includes `/cosmos run`.
- `.claude-plugin/plugin.json` — version 2.0.0; description and keywords
  updated to mention YAML DSL, declarative experiments.
- `.claude-plugin/marketplace.json` — version 2.0.0; updated description
  and tags.
- `README.md` / `README.ko.md` — new "Declarative experiments — the YAML
  DSL" section with full mental model, CLI vs DSL comparison, CI/CD
  workflow sketch, and `/cosmos run` vs `/cosmos spawn` decision table.
  Commands section includes `/cosmos run` with example. Repository
  layout reflects new `experiments/` directory and `skills/run/`.

### Backward compatibility

All v1.x features (`/cosmos spawn`, `/cosmos observe`, `/cosmos crystallize`,
`/cosmos stop`, `/cosmos spin`, `/cosmos singularity`) continue to work
identically. The DSL is purely additive — projects that don't adopt it
notice no change. v2.0 is a major version bump because the DSL represents
a paradigm shift (imperative → declarative), not because anything broke.

## [1.3.0] — 2026-05-12

### Added — verifiable live entanglement (strict mode)

QuantumAgent now offers `--entanglement strict` mode, completing the
four-mode entanglement palette (`none` / `passive` / `active` / `strict`).
Strict mode introduces a **heartbeat protocol** that produces verifiable
proof of live agent-to-agent communication.

- **Heartbeat protocol** — at every major step boundary, each cosmos
  publishes a `heartbeat` insight and MUST write `heartbeat-ack` entries
  referencing every unacknowledged heartbeat from other cosmos before
  proceeding to the next step.

  Insight schema additions:
  - `{"type": "heartbeat", "step": <N>, "content": "<name> at step <N>", "ts": "..."}`
  - `{"type": "heartbeat-ack", "content": "acknowledged <other>:step <M>", "refs": ["<other>@<ts>"], "ts": "..."}`

- **`/cosmos observe` heartbeat audit** — for strict runs, the observer
  builds the heartbeat graph and reports **entanglement quality**:
  - **High** (≥80% of expected ACKs present)
  - **Medium** (40–80%)
  - **Low** (<40%)
  Broken channels are surfaced explicitly: `cosmos:<C> → cosmos:<C'>: <N> unacknowledged heartbeat(s)`.

- **Final-completion heartbeat** — before stopping, each cosmos in strict
  mode writes a `step: "final"` heartbeat and acknowledges any late
  heartbeats from peers. Closes the loop on the entanglement graph.

This is QuantumAgent's **Bell-test analog** — observable proof of live
quantum-style communication between agents, not just trust.

### Added — `/cosmos spin` skill

Declares or updates the project's **immutable identity** — its quantum
spin. Once declared, every `/cosmos spawn` automatically inherits the
spin as invariant constraints.

- `/cosmos spin --name "<name>" [--type "<type>"] [--description "<text>"] [--constraints "<c1,c2,c3>"]`
- `/cosmos spin` (no args) — display current spin

Spin schema (`.quantum/project/spin.json`):
```json
{
  "name": "string (required)",
  "type": "string (optional)",
  "description": "string (optional)",
  "immutable_constraints": ["string", ...],
  "established": "ISO 8601 (set once)",
  "updated": "ISO 8601 (most recent change)"
}
```

`established` is preserved across updates — the project's identity is
anchored to its first declaration. `updated` reflects each modification.

### Changed

- `skills/spawn/SKILL.md` — entanglement modes table now lists four
  modes including `strict`. CLAUDE.md template Entanglement Mode section
  describes the heartbeat protocol for strict. Step 6 dispatch prompt
  Block B includes a strict-mode variant emitting the full heartbeat
  protocol (write heartbeat → read others → write ACKs → proceed).
  Block D closing includes a strict-mode completion sequence.
- `skills/observe/SKILL.md` — Step 4 adds live entanglement audit logic
  for strict runs (heartbeat graph build, expected/actual ACK ratio,
  broken channel detection). Step 5 output includes Live entanglement
  quality section with High/Medium/Low rating and broken channel list.
  Informal signal (cross-cosmos references in content/`read_from`) for
  non-strict runs.
- `CLAUDE.md` / `COSMOS.md` — Entanglement Modes section extended with
  strict; Skills list includes `/cosmos spin` and `/cosmos singularity`.
- `.claude-plugin/plugin.json` — version 1.3.0; description mentions
  verifiable live entanglement; keywords add `heartbeat`, `spin`.
- `.claude-plugin/marketplace.json` — version 1.3.0; description
  mentions four entanglement modes including heartbeat protocol.
- `README.md` / `README.ko.md` — entanglement modes table extended;
  new `/cosmos spin` command section; "How entanglement works" gains
  a "Verifiable live entanglement — strict mode (v1.3)" subsection;
  repository layout reflects new `skills/spin/`.

### Backward compatibility

All v1.3 additions are optional and backward-compatible:

- Default entanglement remains `passive` = v1.2 behavior.
- Projects without `spin.json` continue to work; `/cosmos spin` is opt-in.
- Existing insight schemas unchanged; `heartbeat` and `heartbeat-ack`
  are new types that fall into the legacy `discovery` bucket for older
  observers that don't recognize them.
- v1.2 (`/cosmos singularity`, project spin via file edit, modes
  `none`/`passive`/`active`) work identically.

## [1.2.0] — 2026-05-12

### Added — multi-scale macro layer

QuantumAgent now operates at three scales: cosmos (parallel agents),
**macro (project + singularities)** *(new)*, and code (v2.0 roadmap).

- **`.quantum/project/spin.json`** — optional project identity file.
  Declares the project's `name`, `type`, `description`, and
  `immutable_constraints`. Auto-injected into every cosmos's CLAUDE.md as
  invariant constraints. A strategy that violates a spin constraint is
  not exploring the goal; it is exploring a different problem.
- **`.quantum/singularities/events.jsonl`** — append-only log of
  project-level quantum events (migrations, paradigm shifts, compliance
  changes). Each entry has `name`, `ts`, `trigger`, `invalidates[]`,
  `description`. Every `/cosmos spawn` reads this file and treats
  pre-singularity insights matching `invalidates` patterns as stale.
- **`/cosmos singularity`** — new skill. Declares a singularity event.
  Trigger: `/cosmos singularity --name "<event>" --invalidates "<patterns>"
  [--trigger "<reason>"] [--description "<text>"]`. Appends to
  `events.jsonl` with ISO 8601 timestamp. Warns if active cosmos exist
  (singularities apply to future spawns, not running cosmos).

### Added — entanglement modes

`/cosmos spawn` now accepts `--entanglement <mode>` with three values:

- `none` — cosmos do not read other cosmos insights. Pure independent
  exploration. Use for true statistical independence (agentic A/B testing,
  sampling). The dispatch prompt's rule 2 (READ all cosmos insights)
  becomes "Do NOT read other cosmos insight files."
- `passive` *(default)* — cosmos read other insights between major
  implementation steps. Current behavior preserved.
- `active` — cosmos read AND record `read_from: cosmos:<source>` when
  adopting another cosmos's pattern. Produces a traceable entanglement
  graph for security, compliance, and debugging use cases.

Default is `passive` — existing usage continues unchanged.

### Changed

- `skills/spawn/SKILL.md` — added Step 2.5 to load macro context
  (spin.json + events.jsonl) before creating worktrees. CLAUDE.md
  template now includes Project Spin, Active Singularities, and
  Entanglement Mode sections. Step 6 dispatch prompt composed from
  blocks (A: preamble, B: rule 2 by mode, C: rule 3, D: closing).
  Step 7 launch report shows entanglement mode and macro context if loaded.
- `skills/observe/SKILL.md` — added Step 2 to load macro context.
  Output template includes Project Spin and Active Singularities sections
  when macro files exist.
- `CLAUDE.md` / `COSMOS.md` — updated Quantum Memory section to document
  three scales. Added Entanglement Modes section. Skills list now
  includes `/cosmos singularity`.
- `.claude-plugin/plugin.json` — version 1.2.0; description and keywords
  updated to reflect multi-scale architecture.
- `.claude-plugin/marketplace.json` — version 1.2.0; plugin description
  and tags updated.
- `README.md` / `README.ko.md` — added Multi-scale macro layer section
  documenting spin.json, events.jsonl, and the agentic-context rationale.
  Commands section updated with `/cosmos singularity` and entanglement
  modes. Repository layout reflects new directories.

### Backward compatibility

All v1.2 additions are optional and backward-compatible:

- Projects without `spin.json` or `events.jsonl` run as before.
- Spawn without `--entanglement` defaults to `passive` = pre-1.2 behavior.
- Existing `.quantum/<name>/insights.jsonl` schemas unchanged.
- Existing cosmos workflows (spawn/observe/crystallize/stop) work identically.

## [1.1.0] — 2026-05-12

### Added — first real cosmos run in `examples/`
- **`examples/auth-audit/`** — 3-cosmos security audit of a production
  Electron+Next.js payment terminal codebase, executed twice (deliberate
  re-spawn). Three complementary strategies (security-threat,
  code-architecture, offline-resilience) converged on a 3-way resonance:
  *"the token has no expiration, revocation is a no-op against stateless
  JWT, and the token is stored plaintext — and the three reinforce each
  other."* The 2nd round surfaced a `[TUNNEL]` find — Electron CORS
  wildcard injection in `main.js` that the 1st round missed entirely.
  Includes verbatim auto-observe output (both rounds), raw `.jsonl`
  insights from each cosmos, and the spawn command. Only
  company-identifying strings masked to `EXAMPLE_SYSTEM`; all file
  paths, line numbers, function/library names, and severity grades
  are verbatim.
- README.md and README.ko.md both feature the auth-audit example
  prominently — stats row (3 cosmos × 2 rounds × 5 CRITICALs × 1
  [TUNNEL]), two pull-quote callouts (3-way resonance + tunneling
  finding), "Why this example matters" takeaways, and deep links to
  observe-snapshot + each insights file.

### Added — examples scaffold for real cosmos runs
- New `examples/` directory with index `examples/README.md` documenting
  the contribution path for real cosmos run artifacts.
- `examples/_template/` with placeholder files (`README.md`,
  `spawn-command.md`, `insights/{alpha,beta,gamma}.jsonl`,
  `observe-snapshot.md`, `crystallize-report.md`) so contributors can
  fork the template and fill in their real run output without writing
  scaffolding.
- Both `README.md` and `README.ko.md` now point to `examples/` and
  explicitly state we don't ship fabricated examples — real
  contributions only.

### Updated — README.ko parity pass
- Synced Korean README to match English. Now contains:
  - "Architecture — Git-Native Orchestration" section
  - "🔭 Cosmos 실행 시각화" section with the same three Mermaid diagrams,
    the observe-output sample (translated to Korean), and the quantum
    signals reference table
  - Updated install command (`/plugin install cosmos@quantum-agent`)
  - 17-environment compatibility matrix
  - "두 가지 수렴 표준" framing (agentskills.io + single-file convention)

### Added — visualization in README
- New "🔭 Visualizing a cosmos run" section in README.md with three
  Mermaid diagrams (spawn / observe / crystallize) and a quantum-signal
  reference table.
- Sample `/cosmos:observe` output box demonstrating the format defined
  in `skills/observe/SKILL.md`: superposition snapshot, resonance /
  uncertainty / tunneling / jump / blockers, all with the same emoji
  vocabulary used in the actual workflow output.
- Diagrams use the styling that renders cleanly on GitHub dark mode.
- Marked the sample output as "structure is fixed, content varies" so
  readers don't mistake the illustrative content for a real run.

### Added — two-convention framing
- INTEGRATIONS.md now opens with an explicit framing: the ecosystem is
  converging on **two install conventions**, and QuantumAgent's repository
  layout natively serves both:
  1. **agentskills.io** — `skills/<name>/SKILL.md` with `name`/`description`
     YAML frontmatter (Claude Code, OpenClaw, Hermes).
  2. **Single-file rules/instructions** — one markdown file at a known path
     (Cursor, Windsurf, Aider, Gemini CLI, Copilot, OpenCode, Crush,
     anything that reads `AGENTS.md`).
  Our `skills/*/SKILL.md` covers (1); our `bundle/cosmos-instructions.md`
  covers (2). Any future agent that adopts either convention works
  without a code change on our side.

### Added — broader agent ecosystem coverage
- **Gemini CLI** integration via `GEMINI.md` (Google's repo-root instructions file).
- **OpenCode** (sst) integration via `AGENTS.md`.
- **Crush** (Charm) integration via `AGENTS.md` / `CRUSH.md`.
- **OpenHands** (formerly OpenDevin) integration via `.openhands/microagents/cosmos.md`.
- **Goose** (Block) integration via `.goosehints`.
- **Hermes Agent (Nous Research)** integration — also agentskills.io-compatible,
  installs identically to OpenClaw (`~/.hermes/skills/cosmos-*/SKILL.md`). Also
  documents the `hermes claw migrate` path for users coming from OpenClaw.
- Added a generic **"any agentskills.io-compatible agent"** row to the
  compatibility matrix — three documented agents (Claude Code, OpenClaw,
  Hermes) now converge on the same SKILL.md + YAML frontmatter standard,
  so any future adopter of the standard works out-of-the-box.
- **OpenClaw** integration — uses AgentSkills-compatible SKILL.md format
  identical to QuantumAgent's own. Install path is a direct copy of
  `skills/*` into `~/.openclaw/skills/` (or `<workspace>/skills/` for
  workspace scope). No bundle/curl needed; the existing files work as-is.
- **Generic AGENTS.md** section — one-line install for any agent following
  the de-facto `AGENTS.md` repo convention. README and INTEGRATIONS.md
  compatibility matrices updated.

### Added
- **Typed insight schema** in `.quantum/<name>/insights.jsonl`. Each line
  now carries `type` alongside `content` and `ts`:
  ```
  {"type": "<discovery|decision|blocker|tunnel|jump|resonance|complete|crystallize>",
   "content": "<text>", "ts": "<ISO 8601>"}
  ```
  Enables filtered observe, grouped crystallize summaries, and blocker
  surfacing. Backward-compatible: missing `type` is treated as `discovery`;
  legacy `[TUNNEL]`/`[JUMP]` content prefixes are recognized.
- **Git-Native Orchestration architecture** explained in `README.md`,
  `CLAUDE.md`, and `COSMOS.md`. Two layers: Control Plane (Git/Markdown,
  agent-agnostic) + Effector Layer (host agent's native tools). Clarifies
  why the same workflows port to 10+ AI agents.
- **Concurrency note** in `skills/spawn/SKILL.md` and `CLAUDE.md`: POSIX
  atomic append covers single-agent sequential writes; concurrent
  sub-agent writes to the same insights file should use `flock` or
  write-then-rename.

### Changed
- `skills/spawn/SKILL.md`: insight examples updated to typed schema;
  `[TUNNEL]`/`[JUMP]` documented as legacy text prefixes.
- `skills/observe/SKILL.md`: parsing now reads `type` (defaulting to
  `discovery`) and adds a Blockers section for unresolved
  `type: "blocker"` entries.
- `skills/crystallize/SKILL.md`: report groups insights by type
  (decisions / tunnels / jumps / blockers / complete), and the merge step
  records a `type: "crystallize"` marker in the cosmos's insights file.
- `bundle/cosmos-instructions.md` regenerated to reflect all of the above.

### Removed
- `mcp/` MCP server, `cli/` non-LLM CLI, `tests/conformance.sh`, and
  `.github/workflows/conformance.yml`. The Claude Code plugin plus the
  universal `bundle/cosmos-instructions.md` already cover every supported
  agent via Custom Instructions / rules files — the extra runtime artifacts
  added maintenance surface without unlocking new use cases. They remain in
  git history if needed later.

### Changed
- `INTEGRATIONS.md` matrix: every entry now installs via "paste bundle into
  Custom Instructions / rules file" — no Node runtime, no MCP server, no
  npm install. Same workflows, simpler delivery.

### Added
- `scripts/build-bundle.sh` — regenerates `bundle/cosmos-instructions.md`
  from `skills/*/SKILL.md`. Also runs with `--check` flag for CI diff mode.
- `.github/workflows/validate.yml` — 3 lightweight checks on every push/PR:
  JSON parse for all `*.json`, SKILL.md frontmatter presence, and bundle
  sync. Replaces the deleted Conformance workflow with much smaller scope
  appropriate for a markdown-only project.

## [1.0.0] — 2026-05-12

Initial public release.

### Added
- Claude Code plugin (`cosmos@quantum-agent`) with four slash commands:
  `/cosmos:spawn`, `/cosmos:observe`, `/cosmos:crystallize`, `/cosmos:stop`.
- `.claude-plugin/marketplace.json` for self-marketplace install via
  `/plugin marketplace add hyuniiiv/quantum-agent`.
- Universal markdown bundle (`bundle/cosmos-instructions.md`) — drop-in
  system prompt or rules file for any AI coding agent.
- `INTEGRATIONS.md` documenting setup for 11 environments:
  Claude Code, Claude Desktop, Cursor, Windsurf, Cline, Roo Code,
  Continue.dev, Aider, OpenAI Codex CLI, GitHub Copilot, Zed AI.
- Cursor `.mdc` preset (`presets/cursor/cosmos.mdc`) with `globs` header.

### Documentation
- `README.md` — overview, install, quick start, signal taxonomy.
- `README.ko.md` — Korean translation.
- `CONTRIBUTING.md` — how to add integrations and contribute.
- `CODE_OF_CONDUCT.md` — Contributor Covenant 2.1.

[Unreleased]: https://github.com/hyuniiiv/quantum-agent/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/hyuniiiv/quantum-agent/releases/tag/v1.0.0
