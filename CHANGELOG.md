# Changelog

All notable changes to QuantumAgent are documented here. Format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/). Versioning follows
[Semantic Versioning](https://semver.org/).

## [Unreleased]

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
