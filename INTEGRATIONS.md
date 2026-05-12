# Integrations — Using QuantumAgent in any AI coding agent

QuantumAgent ships as a Claude Code plugin, but its core (markdown SKILL files + bash commands) is **platform-neutral**. This document shows how to install the same `cosmos` workflow in 10+ other AI coding environments.

## Why it ports cleanly

Each `cosmos:*` command is a single markdown file (`skills/<name>/SKILL.md`) that contains:
- A description of the workflow
- Step-by-step bash commands the host agent should execute
- Conventions for reading and writing `.quantum/*.jsonl` files

No Claude-specific APIs. No proprietary runtime. Any agent that can:
1. Load markdown instructions as context, and
2. Execute shell commands

… can run QuantumAgent.

## Compatibility matrix

| Environment | Mechanism | Status | Trigger |
|---|---|---|---|
| **Claude Code** | Native plugin | ✅ First-class | `/cosmos:spawn`, etc. |
| **Claude Desktop / claude.ai** | MCP server (run from source) or Custom Instructions | ✅ Available | Natural language |
| **Cursor** | `.cursor/rules/*.mdc` | ✅ Drop-in | Auto-attach by glob |
| **Windsurf** | `.windsurfrules` | ✅ Drop-in | Always-on rule |
| **Cline (VS Code)** | Custom Instructions / MCP | ✅ Drop-in | "run cosmos spawn …" |
| **Roo Code** | Custom Instructions / MCP | ✅ Drop-in | "run cosmos spawn …" |
| **Continue.dev** | `config.json` rules + MCP | ✅ Drop-in | Slash command alias |
| **Aider** | `CONVENTIONS.md` / `--read` | ✅ Drop-in | "/run cosmos spawn …" |
| **OpenAI Codex CLI** | Prompt file via `--prompt-file` | ✅ Drop-in | Per-invocation |
| **GitHub Copilot** | `.github/copilot-instructions.md` | ✅ Drop-in | Conversation hint |
| **Zed AI** | Assistant rules / config | ✅ Drop-in | Always-on rule |

> **Drop-in** = copy `bundle/cosmos-instructions.md` into the agent's instructions file. No code changes.

## Universal bundle

For agents that don't have a plugin system, we ship a single consolidated instructions file:

**[`bundle/cosmos-instructions.md`](bundle/cosmos-instructions.md)** — all four `cosmos:*` workflows concatenated, ready to paste as a system prompt or rules file.

## Per-platform setup

### Cursor

```bash
mkdir -p .cursor/rules
curl -L https://raw.githubusercontent.com/hyuniiiv/quantum-agent/master/presets/cursor/cosmos.mdc \
  -o .cursor/rules/cosmos.mdc
```

The preset includes a `globs: ["**/*"]` header so Cursor auto-attaches the rule when working in any file. Trigger by typing "cosmos spawn ..." or "spawn parallel cosmos for X".

### Windsurf

```bash
curl -L https://raw.githubusercontent.com/hyuniiiv/quantum-agent/master/bundle/cosmos-instructions.md \
  -o .windsurfrules
```

Windsurf treats `.windsurfrules` as always-on context.

### Cline / Roo Code (VS Code)

Open Cline settings → **Custom Instructions** → paste the contents of `bundle/cosmos-instructions.md`.

Or use MCP — add to `cline_mcp_settings.json`:
```json
{
  "mcpServers": {
    "quantum-agent": {
      "command": "node",
      "args": ["/absolute/path/to/quantum-agent/mcp/index.js"]
    }
  }
}
```

### Continue.dev

`~/.continue/config.json`:
```json
{
  "systemMessage": "@./bundle/cosmos-instructions.md",
  "slashCommands": [
    { "name": "cosmos", "description": "Run cosmos workflow" }
  ]
}
```

### Aider

```bash
curl -L https://raw.githubusercontent.com/hyuniiiv/quantum-agent/master/bundle/cosmos-instructions.md \
  -o CONVENTIONS.md
aider --read CONVENTIONS.md
```

Then ask Aider: "spawn 3 parallel cosmos to implement X with strategies A, B, C".

### OpenAI Codex CLI

```bash
codex --prompt-file bundle/cosmos-instructions.md "spawn cosmos for rate limiting with 3 strategies"
```

### GitHub Copilot (Chat)

Copy `bundle/cosmos-instructions.md` into `.github/copilot-instructions.md`. Copilot Chat will respect it for the repo.

### Zed AI

Add to your Zed assistant config (Settings → Assistant → Custom System Prompt):
```
@import bundle/cosmos-instructions.md
```

### Claude Desktop / claude.ai (via MCP)

Edit `claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "quantum-agent": {
      "command": "node",
      "args": ["/absolute/path/to/quantum-agent/mcp/index.js"]
    }
  }
}
```

First clone the repo somewhere, then point the `args` path at `mcp/index.js`:
```bash
git clone https://github.com/hyuniiiv/quantum-agent ~/tools/quantum-agent
cd ~/tools/quantum-agent/mcp && npm install
```

The MCP server exposes four prompts (`cosmos_spawn`, `cosmos_observe`, `cosmos_crystallize`, `cosmos_stop`) to any MCP-compatible host. See [`mcp/README.md`](mcp/README.md) for details.

> npm publish (`@hyuniiiv/quantum-agent-mcp`) is deferred until there's demand. Open an issue if you want one-line `npx` install instead of the clone-and-run flow above.

## Cross-agent invariants

All integrations rely on the same on-disk contract:

- `.quantum/<cosmos_name>/insights.jsonl` — JSON Lines, one insight per line
- `cosmos/<cosmos_name>/` — git worktree per cosmos
- `cosmos/<cosmos_name>` branch — branch tracking the worktree
- `.gitignore` excludes `.quantum/` and `cosmos/`

This means **you can spawn cosmos in Cursor, observe in Claude Code, and crystallize in Aider** — all on the same `.quantum/` memory. The harness is fundamentally a filesystem protocol, not a runtime.

## Status & roadmap

- [x] Claude Code plugin (`/cosmos:*`)
- [x] Universal markdown bundle
- [x] Documentation for 10+ environments
- [x] MCP server source in `mcp/` (run via `node mcp/index.js`)
- [x] Cursor `.mdc` preset with glob hints — see `presets/cursor/cosmos.mdc`
- [x] CLI source in `cli/` (run via `node cli/index.js`)
- [x] Conformance tests verifying each integration honors the filesystem contract — see `tests/conformance.sh` (16 checks, all pass against the local CLI)
- [ ] npm publish (`@hyuniiiv/quantum-agent-mcp`, `@hyuniiiv/quantum-agent-cli`) — deferred; current path is git clone + node

Contributions adding support for additional environments are welcome — open a PR adding a section to this file plus any platform-specific shim.
