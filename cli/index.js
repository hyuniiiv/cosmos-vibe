#!/usr/bin/env node
/**
 * QuantumAgent CLI — non-LLM execution of cosmos lifecycle operations.
 *
 * This is the deterministic side of QuantumAgent: setting up worktrees,
 * appending insights, listing cosmos, and tearing down. It does NOT
 * generate code — that's the LLM's job inside each cosmos. But the
 * scaffolding around the LLMs (filesystem contract enforcement) can run
 * without any LLM at all.
 *
 * Usage:
 *   quantum-agent init <name> [--from <ref>]
 *   quantum-agent list
 *   quantum-agent insight <name> <content>
 *   quantum-agent observe [--cosmos <name>]
 *   quantum-agent crystallize <name>
 *   quantum-agent stop [--purge]
 */

import { execSync } from "child_process";
import { existsSync, mkdirSync, appendFileSync, readFileSync, readdirSync, rmSync } from "fs";
import { join, resolve } from "path";

const HELP = `quantum-agent — cosmos lifecycle CLI

Commands:
  init <name> [--from <ref>]   Create a cosmos worktree and quantum namespace
  list                          List active cosmos
  insight <name> <text>         Append an insight to .quantum/<name>/insights.jsonl
  observe [--cosmos <name>]     Print insights from all cosmos (or one)
  crystallize <name>            Mark a cosmos as the collapsed solution
  stop [--purge]                Remove all cosmos worktrees; --purge also deletes .quantum/
  help                          Show this message

Filesystem contract:
  cosmos/<name>/                git worktree (branch: cosmos/<name>)
  .quantum/<name>/insights.jsonl   one JSON per line: {"content":"...","ts":"..."}

This CLI does not generate code. Pair it with any LLM agent that respects
the same contract — Claude Code, Cursor, Aider, Cline, Continue, etc.`;

function sh(cmd) {
  return execSync(cmd, { encoding: "utf8", stdio: ["ignore", "pipe", "pipe"] }).trim();
}

function repoRoot() {
  try {
    return sh("git rev-parse --show-toplevel");
  } catch {
    console.error("Not inside a git repository.");
    process.exit(1);
  }
}

function parseArgs(argv) {
  const cmd = argv[0];
  const args = [];
  const flags = {};
  for (let i = 1; i < argv.length; i++) {
    if (argv[i].startsWith("--")) {
      const key = argv[i].slice(2);
      const next = argv[i + 1];
      if (next && !next.startsWith("--")) {
        flags[key] = next;
        i++;
      } else {
        flags[key] = true;
      }
    } else {
      args.push(argv[i]);
    }
  }
  return { cmd, args, flags };
}

function init(name, flags) {
  const root = repoRoot();
  const worktreePath = join(root, "cosmos", name);
  const branchName = `cosmos/${name}`;
  const from = flags.from || "HEAD";

  if (existsSync(worktreePath)) {
    console.error(`Cosmos already exists: ${worktreePath}`);
    process.exit(1);
  }

  sh(`git worktree add -b ${branchName} "${worktreePath}" ${from}`);

  const qDir = join(root, ".quantum", name);
  mkdirSync(qDir, { recursive: true });
  appendFileSync(
    join(qDir, "insights.jsonl"),
    JSON.stringify({ content: `Cosmos '${name}' initialized from ${from}`, ts: new Date().toISOString() }) + "\n"
  );

  console.log(`✨ Cosmos '${name}' born`);
  console.log(`   Worktree:  ${worktreePath}`);
  console.log(`   Branch:    ${branchName}`);
  console.log(`   Quantum:   .quantum/${name}/insights.jsonl`);
}

function list() {
  const root = repoRoot();
  const cosmosDir = join(root, "cosmos");
  if (!existsSync(cosmosDir)) {
    console.log("(no active cosmos)");
    return;
  }
  const cosmos = readdirSync(cosmosDir, { withFileTypes: true })
    .filter((d) => d.isDirectory())
    .map((d) => d.name);

  if (!cosmos.length) {
    console.log("(no active cosmos)");
    return;
  }

  for (const name of cosmos) {
    const jsonl = join(root, ".quantum", name, "insights.jsonl");
    const count = existsSync(jsonl)
      ? readFileSync(jsonl, "utf8").split("\n").filter(Boolean).length
      : 0;
    console.log(`  ${name.padEnd(20)} ${count} insight(s)`);
  }
}

function insight(name, content) {
  const root = repoRoot();
  const qDir = join(root, ".quantum", name);
  if (!existsSync(qDir)) mkdirSync(qDir, { recursive: true });
  appendFileSync(
    join(qDir, "insights.jsonl"),
    JSON.stringify({ content, ts: new Date().toISOString() }) + "\n"
  );
  console.log(`📝 Insight recorded in .quantum/${name}/`);
}

function observe(flags) {
  const root = repoRoot();
  const qRoot = join(root, ".quantum");
  if (!existsSync(qRoot)) {
    console.log("(no quantum memory)");
    return;
  }
  const targets = flags.cosmos
    ? [flags.cosmos]
    : readdirSync(qRoot, { withFileTypes: true }).filter((d) => d.isDirectory()).map((d) => d.name);

  for (const name of targets) {
    const jsonl = join(qRoot, name, "insights.jsonl");
    if (!existsSync(jsonl)) continue;
    console.log(`\n━━━ cosmos: ${name} ━━━`);
    const lines = readFileSync(jsonl, "utf8").split("\n").filter(Boolean);
    for (const line of lines) {
      try {
        const obj = JSON.parse(line);
        console.log(`  [${obj.ts || "?"}] ${obj.content}`);
      } catch {
        console.log(`  ${line}`);
      }
    }
  }
}

function crystallize(name) {
  const root = repoRoot();
  const qDir = join(root, ".quantum", name);
  if (!existsSync(qDir)) {
    console.error(`No such cosmos in quantum memory: ${name}`);
    process.exit(1);
  }
  appendFileSync(
    join(qDir, "insights.jsonl"),
    JSON.stringify({
      content: `[CRYSTALLIZE] Cosmos '${name}' chosen as collapsed solution.`,
      ts: new Date().toISOString(),
    }) + "\n"
  );
  console.log(`💎 Cosmos '${name}' marked for crystallization.`);
  console.log(`   Next: merge branch cosmos/${name} into your main branch.`);
  console.log(`   Then run: quantum-agent stop`);
}

function stop(flags) {
  const root = repoRoot();
  const cosmosDir = join(root, "cosmos");
  if (existsSync(cosmosDir)) {
    const names = readdirSync(cosmosDir, { withFileTypes: true })
      .filter((d) => d.isDirectory())
      .map((d) => d.name);
    for (const name of names) {
      try {
        sh(`git worktree remove "${join(cosmosDir, name)}" --force`);
      } catch {}
      try {
        sh(`git branch -D cosmos/${name}`);
      } catch {}
    }
    console.log(`🛑 Removed ${names.length} cosmos worktree(s).`);
  } else {
    console.log("(no cosmos to stop)");
  }
  if (flags.purge) {
    const qDir = join(root, ".quantum");
    if (existsSync(qDir)) {
      rmSync(qDir, { recursive: true, force: true });
      console.log("   Quantum memory purged.");
    }
  } else {
    console.log("   Quantum memory preserved at .quantum/ (use --purge to delete).");
  }
}

const { cmd, args, flags } = parseArgs(process.argv.slice(2));

switch (cmd) {
  case "init":
    if (!args[0]) { console.error("Usage: quantum-agent init <name>"); process.exit(1); }
    init(args[0], flags);
    break;
  case "list":
    list();
    break;
  case "insight":
    if (args.length < 2) { console.error("Usage: quantum-agent insight <name> <text>"); process.exit(1); }
    insight(args[0], args.slice(1).join(" "));
    break;
  case "observe":
    observe(flags);
    break;
  case "crystallize":
    if (!args[0]) { console.error("Usage: quantum-agent crystallize <name>"); process.exit(1); }
    crystallize(args[0]);
    break;
  case "stop":
    stop(flags);
    break;
  case "help":
  case undefined:
    console.log(HELP);
    break;
  default:
    console.error(`Unknown command: ${cmd}\n`);
    console.log(HELP);
    process.exit(1);
}
