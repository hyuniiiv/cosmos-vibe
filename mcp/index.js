#!/usr/bin/env node
/**
 * QuantumAgent MCP server.
 *
 * Exposes the four cosmos:* workflows as MCP prompts. Any MCP-compatible
 * host (Claude Desktop, Cline, Continue, Roo Code, etc.) can install this
 * server and the host LLM will then know how to run cosmos workflows using
 * its own filesystem/bash tools.
 *
 * The server returns the SKILL.md content verbatim as a prompt. The host
 * LLM executes the steps. No privileged shell access is granted by the
 * server itself — it's a pure instruction provider.
 */

import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  ListPromptsRequestSchema,
  GetPromptRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";
import { readFileSync } from "fs";
import { dirname, join } from "path";
import { fileURLToPath } from "url";

const __dirname = dirname(fileURLToPath(import.meta.url));
const SKILLS_DIR = join(__dirname, "skills");

const SKILLS = [
  {
    id: "spawn",
    summary:
      "Spawn N parallel cosmos agents in isolated git worktrees, each tackling the same goal with a different strategy.",
    args: [
      { name: "goal", description: "What to build or solve", required: true },
      {
        name: "strategies",
        description: "Comma-separated strategy names (one per cosmos)",
        required: true,
      },
    ],
  },
  {
    id: "observe",
    summary:
      "Inspect the live superposition of running cosmos — resonance, uncertainty, tunneling, condensate.",
    args: [],
  },
  {
    id: "crystallize",
    summary:
      "Collapse one cosmos from superposition into a concrete deliverable; preserve other cosmos.",
    args: [
      { name: "name", description: "Cosmos name to crystallize", required: true },
    ],
  },
  {
    id: "stop",
    summary:
      "Tear down all cosmos worktrees and branches; optionally purge Quantum Memory.",
    args: [],
  },
];

const skillContent = Object.fromEntries(
  SKILLS.map((s) => [s.id, readFileSync(join(SKILLS_DIR, `${s.id}.md`), "utf8")])
);

const server = new Server(
  { name: "quantum-agent", version: "1.0.0" },
  { capabilities: { prompts: {} } }
);

server.setRequestHandler(ListPromptsRequestSchema, async () => ({
  prompts: SKILLS.map((s) => ({
    name: `cosmos_${s.id}`,
    description: `QuantumAgent — ${s.summary}`,
    arguments: s.args,
  })),
}));

server.setRequestHandler(GetPromptRequestSchema, async (req) => {
  const name = req.params.name;
  const skillId = name.startsWith("cosmos_") ? name.slice("cosmos_".length) : null;
  if (!skillId || !skillContent[skillId]) {
    throw new Error(`Unknown prompt: ${name}`);
  }

  const argsBlock = req.params.arguments && Object.keys(req.params.arguments).length
    ? `\n\n## Invocation arguments\n\n${Object.entries(req.params.arguments)
        .map(([k, v]) => `- **${k}**: ${v}`)
        .join("\n")}\n`
    : "";

  return {
    description: `QuantumAgent cosmos:${skillId} workflow`,
    messages: [
      {
        role: "user",
        content: {
          type: "text",
          text: skillContent[skillId] + argsBlock,
        },
      },
    ],
  };
});

const transport = new StdioServerTransport();
await server.connect(transport);
