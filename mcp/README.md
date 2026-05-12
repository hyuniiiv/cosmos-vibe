# quantum-agent MCP server

MCP (Model Context Protocol) server for [QuantumAgent](https://github.com/hyuniiiv/quantum-agent). Exposes the four `cosmos:*` workflows as MCP prompts for any MCP-compatible AI agent host.

> **npm publish deferred.** Run from a local clone for now. If you'd like an
> `npx`-able package, open an issue on the parent repo.

## What it does

The server provides four prompts:

- `cosmos_spawn` — Spawn N parallel cosmos agents
- `cosmos_observe` — Inspect superposition of running cosmos
- `cosmos_crystallize` — Collapse one cosmos into a deliverable
- `cosmos_stop` — Tear down all cosmos

When a host LLM requests one of these prompts, the server returns the full SKILL.md workflow instructions. The host LLM then executes the steps using its own bash/file tools. **The MCP server itself has no privileged shell access** — it's a pure instruction provider.

## Install (from source)

```bash
git clone https://github.com/hyuniiiv/quantum-agent ~/tools/quantum-agent
cd ~/tools/quantum-agent/mcp
npm install
```

Then point your MCP host at the absolute path of `index.js`.

### Claude Desktop

`claude_desktop_config.json`:
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

### Cline (VS Code)

`cline_mcp_settings.json`:
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
  "mcpServers": [
    {
      "name": "quantum-agent",
      "command": "node",
      "args": ["/absolute/path/to/quantum-agent/mcp/index.js"]
    }
  ]
}
```

### Roo Code

Settings → MCP Servers → Add:
```json
{
  "quantum-agent": {
    "command": "node",
    "args": ["/absolute/path/to/quantum-agent/mcp/index.js"]
  }
}
```

## Usage

After your host loads the server, ask its LLM:

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
npm run sync-skills   # copy latest SKILL.md from parent
npm start             # start the server (stdio)
```

## License

MIT — see [LICENSE](../LICENSE).
