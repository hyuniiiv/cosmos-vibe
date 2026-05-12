# Changelog

All notable changes to QuantumAgent are documented here. Format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/). Versioning follows
[Semantic Versioning](https://semver.org/).

## [Unreleased]

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
- MCP server (`@hyuniiiv/quantum-agent-mcp`) — exposes the four cosmos
  workflows as MCP prompts for any MCP-compatible host.
- Non-LLM CLI (`@hyuniiiv/quantum-agent-cli`) — deterministic cosmos
  lifecycle ops: `init`, `list`, `insight`, `observe`, `crystallize`, `stop`.
- Cursor `.mdc` preset (`presets/cursor/cosmos.mdc`) with `globs` header.
- Conformance test suite (`tests/conformance.sh`) — 16 filesystem-contract
  checks runnable against any implementation.

### Documentation
- `README.md` — overview, install, quick start, signal taxonomy.
- `README.ko.md` — Korean translation.
- `CONTRIBUTING.md` — how to add integrations and contribute.
- `CODE_OF_CONDUCT.md` — Contributor Covenant 2.1.

[Unreleased]: https://github.com/hyuniiiv/quantum-agent/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/hyuniiiv/quantum-agent/releases/tag/v1.0.0
