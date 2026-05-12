# Integrations — Using QuantumAgent in any AI coding agent

QuantumAgent ships as a Claude Code plugin, but its core is just **markdown instructions** that any LLM-powered coding agent can follow. This document shows how to install the same `cosmos` workflows in 10+ other environments.

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

| Environment | Mechanism | Trigger |
|---|---|---|
| **Claude Code** | Native plugin | `/cosmos:spawn`, etc. |
| **Claude Desktop / claude.ai** | Custom Instructions | Natural language |
| **Cursor** | `.cursor/rules/*.mdc` | Auto-attach by glob |
| **Windsurf** | `.windsurfrules` | Always-on rule |
| **Cline (VS Code)** | Custom Instructions | "run cosmos spawn …" |
| **Roo Code** | Custom Instructions | "run cosmos spawn …" |
| **Continue.dev** | `config.json` system message | Slash command alias |
| **Aider** | `CONVENTIONS.md` / `--read` | "/run cosmos spawn …" |
| **OpenAI Codex CLI** | Prompt file via `--prompt-file` | Per-invocation |
| **Gemini CLI** | `GEMINI.md` in repo root | Natural language |
| **GitHub Copilot** | `.github/copilot-instructions.md` | Conversation hint |
| **Zed AI** | Assistant rules / config | Always-on rule |
| **OpenCode** (sst) | `AGENTS.md` in repo root | Natural language |
| **Crush** (Charm) | `AGENTS.md` / `CRUSH.md` | Natural language |
| **OpenHands** | Microagent file in `.openhands/microagents/` | Natural language |
| **Goose** (Block) | Goose hints file / profile | Natural language |
| **Any AGENTS.md-aware agent** | `AGENTS.md` in repo root | Natural language |

Every entry is the same workflow — paste `bundle/cosmos-instructions.md` (or a curl-fetched copy) into the agent's instructions surface. No code, no install step, no dependencies.

> **AGENTS.md convention**: a growing number of AI coding agents (OpenCode, Crush, and others) read `AGENTS.md` from the repository root by default. Dropping the bundle there gives you instant compatibility with the entire AGENTS.md ecosystem in one move — see the [generic install](#generic-any-agentmd-aware-agent) section below.

## Universal bundle

For most agents, we ship a single consolidated instructions file:

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

Open Cline (or Roo Code) settings → **Custom Instructions** → paste the contents of `bundle/cosmos-instructions.md`.

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

### Gemini CLI

Gemini CLI reads `GEMINI.md` from the repo root automatically (Google's equivalent of `CLAUDE.md`):

```bash
curl -L https://raw.githubusercontent.com/hyuniiiv/quantum-agent/master/bundle/cosmos-instructions.md \
  -o GEMINI.md
```

Then in any Gemini CLI session: "spawn 3 parallel cosmos for X with strategies A, B, C".

### GitHub Copilot (Chat)

Copy `bundle/cosmos-instructions.md` into `.github/copilot-instructions.md`. Copilot Chat will respect it for the repo.

### Zed AI

Add to your Zed assistant config (Settings → Assistant → Custom System Prompt):
```
@import bundle/cosmos-instructions.md
```

### Claude Desktop / claude.ai

Open the conversation, click the **Custom Instructions** (or system prompt) panel, and paste `bundle/cosmos-instructions.md`. Then ask:

> spawn cosmos for "implement rate limiting" with strategies "token-bucket,sliding-window,fixed-window"

Claude will execute the workflow using its filesystem tools.

### OpenCode (sst)

OpenCode reads `AGENTS.md` from the repo root:

```bash
curl -L https://raw.githubusercontent.com/hyuniiiv/quantum-agent/master/bundle/cosmos-instructions.md \
  -o AGENTS.md
opencode
```

Then ask: "spawn cosmos for X with strategies Y, Z, W".

### Crush (Charm)

Crush also follows the `AGENTS.md` convention (and recognizes `CRUSH.md` as an alternative). If you already added `AGENTS.md` from the OpenCode section above, Crush picks it up automatically. Otherwise:

```bash
curl -L https://raw.githubusercontent.com/hyuniiiv/quantum-agent/master/bundle/cosmos-instructions.md \
  -o AGENTS.md
crush
```

### OpenHands (formerly OpenDevin)

Add a repository microagent so OpenHands loads cosmos instructions for every session in this repo:

```bash
mkdir -p .openhands/microagents
curl -L https://raw.githubusercontent.com/hyuniiiv/quantum-agent/master/bundle/cosmos-instructions.md \
  -o .openhands/microagents/cosmos.md
```

Then in OpenHands: "spawn parallel cosmos for X with strategies Y, Z".

### Goose (Block)

Drop the bundle into your Goose hints file (path varies by Goose version; typical locations include `.goosehints` in the repo or a profile-level hints file under your Goose config dir):

```bash
curl -L https://raw.githubusercontent.com/hyuniiiv/quantum-agent/master/bundle/cosmos-instructions.md \
  -o .goosehints
```

### Generic (any AGENTS.md-aware agent)

The `AGENTS.md` convention is becoming a de-facto standard for repo-level AI agent instructions. If your agent supports it, install in one line:

```bash
curl -L https://raw.githubusercontent.com/hyuniiiv/quantum-agent/master/bundle/cosmos-instructions.md \
  -o AGENTS.md
```

One file unlocks compatibility with the whole AGENTS.md ecosystem at once. If your agent doesn't read `AGENTS.md`, check its documentation for the equivalent instructions/rules/hints file — the bundle is plain markdown and works in all of them.

## Cross-agent invariants

All integrations rely on the same on-disk contract:

- `.quantum/<cosmos_name>/insights.jsonl` — JSON Lines, one insight per line
- `cosmos/<cosmos_name>/` — git worktree per cosmos
- `cosmos/<cosmos_name>` branch — branch tracking the worktree
- `.gitignore` excludes `.quantum/` and `cosmos/`

This means **you can spawn cosmos in Cursor, observe in Claude Code, and crystallize in Aider** — all on the same `.quantum/` memory. The harness is fundamentally a filesystem protocol, not a runtime.

Contributions adding support for additional environments are welcome — open a PR adding a section to this file.
