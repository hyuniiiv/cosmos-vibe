# Changelog

All notable changes to QuantumAgent are documented here. Format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/). Versioning follows
[Semantic Versioning](https://semver.org/).

## [Unreleased]

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
