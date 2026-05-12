# @hyuniiiv/quantum-agent-mcp

MCP (Model Context Protocol) server for [QuantumAgent](https://github.com/hyuniiiv/quantum-agent). Exposes the four `cosmos:*` workflows as MCP prompts for any MCP-compatible AI agent host.

## What it does

The server provides four prompts:

- `cosmos_spawn` — Spawn N parallel cosmos agents
- `cosmos_observe` — Inspect superposition of running cosmos
- `cosmos_crystallize` — Collapse one cosmos into a deliverable
- `cosmos_stop` — Tear down all cosmos

When a host LLM requests one of these prompts, the server returns the full SKILL.md workflow instructions. The host LLM then executes the steps using its own bash/file tools. **The MCP server itself has no privileged shell access** — it's a pure instruction provider.

## Install

### Claude Desktop

`claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "quantum-agent": {
      "command": "npx",
      "args": ["-y", "@hyuniiiv/quantum-agent-mcp"]
    }
  }
}
```

### Cline (VS Code)

`cline_mcp_settings.json`:
```json
{
  "mcpServers": {
    "quantum-agent": {
      "command": "npx",
      "args": ["-y", "@hyuniiiv/quantum-agent-mcp"]
    }
  }
}
```

### Continue.dev

`~/.continue/config.json`:
```json
{
  "mcpServers": [
    {
      "name": "quantum-agent",
      "command": "npx",
      "args": ["-y", "@hyuniiiv/quantum-agent-mcp"]
    }
  ]
}
```

### Roo Code

Settings → MCP Servers → Add:
```json
{
  "quantum-agent": {
    "command": "npx",
    "args": ["-y", "@hyuniiiv/quantum-agent-mcp"]
  }
}
```

### Generic (any MCP host)

```bash
npx -y @hyuniiiv/quantum-agent-mcp
```

The server speaks MCP over stdio.

## Usage

After install, ask the host LLM:

> Use cosmos_spawn to explore "implement rate limiting middleware" with strategies "token-bucket,sliding-window,fixed-window"

The host will request the `cosmos_spawn` prompt with arguments, receive the workflow, and execute the git worktree + Quantum Memory setup steps using its own tools.

## Filesystem contract

All cosmos workflows share the same on-disk protocol regardless of which MCP host invokes them:

- `cosmos/<name>/` — git worktree per cosmos
- `.quantum/<name>/insights.jsonl` — append-only insights, one JSON per line

This means you can spawn cosmos in Cline, observe in Claude Desktop, and crystallize in Continue — all on the same `.quantum/` memory.

## Development

```bash
npm install
npm run sync-skills  # copy latest SKILL.md from parent
npm start            # start the server (stdio)
```

## License

MIT — see [LICENSE](../LICENSE).
