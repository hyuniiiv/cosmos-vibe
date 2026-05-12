# Changelog

All notable changes to QuantumAgent are documented here. Format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/). Versioning follows
[Semantic Versioning](https://semver.org/).

## [Unreleased]

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
