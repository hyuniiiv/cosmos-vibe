# Contributing to QuantumAgent

Thanks for your interest in QuantumAgent. This project is small enough that any
contribution moves the needle — from a typo fix to a new agent integration.

## Ways to help

1. **Add a new integration** — port the cosmos workflows to another AI agent
   (Trae, Cody, AI2 Code, JetBrains AI, etc.). See `INTEGRATIONS.md` for the
   compatibility matrix and per-platform format.
2. **Improve workflows** — refine `skills/*/SKILL.md` for better LLM
   compliance, clearer steps, or new quantum signals.
3. **Bug reports** — open an issue with a minimal reproduction.
4. **Documentation** — corrections, translations (Korean `README.ko.md`
   especially welcome), or new examples.
5. **CLI/MCP server improvements** — `cli/index.js` and `mcp/index.js` are
   intentionally small. PRs adding tests, better error messages, or new
   subcommands are welcome.

## Development setup

```bash
git clone https://github.com/hyuniiiv/quantum-agent
cd quantum-agent

# Run the conformance suite — should output: PASS: 16  FAIL: 0
bash tests/conformance.sh
```

No build step. Skills are plain markdown; CLI/MCP are plain Node.js.

## Filesystem contract (do not break)

These invariants are tested by `tests/conformance.sh` and run in CI on every
PR. Any change that breaks them will fail:

- `cosmos/<name>/` is a git worktree on branch `cosmos/<name>`
- `.quantum/<name>/insights.jsonl` is append-only JSON Lines, one line per
  insight: `{"content": "...", "ts": "ISO-8601"}`
- `stop` removes worktrees + branches but preserves `.quantum/` unless `--purge`
- `cosmos/` and `.quantum/` are in `.gitignore`

Multiple agents must be able to interoperate on the same on-disk state —
that's the whole point of QuantumAgent. Don't introduce vendor-specific
state files.

## Adding a new agent integration

1. Add a row to the **Compatibility matrix** in `INTEGRATIONS.md` with the
   mechanism (system prompt, rules file, MCP, etc.) and trigger format.
2. Add a per-platform **setup section** with concrete install commands
   (`curl`, JSON config snippet, etc.).
3. Verify the agent can:
   - Read instructions from a markdown file
   - Execute `git worktree add`, file reads/writes, `tail -f` (or
     equivalent) on `.quantum/*.jsonl`
4. If the agent supports MCP, point to `mcp/README.md`.
5. Open a PR titled `feat(integration): support <agent name>`.

## PR checklist

- [ ] `bash tests/conformance.sh` passes locally
- [ ] No secrets, API keys, tokens, or personal data
- [ ] If `skills/*/SKILL.md` changed, mirror the change in `mcp/skills/` (or
      run `cd mcp && npm run sync-skills`)
- [ ] If `bundle/cosmos-instructions.md` is regenerated, document the change
- [ ] CHANGELOG entry under `## [Unreleased]` (if user-visible)

## Commit messages

Conventional Commits style:

- `feat:` — new feature / new integration
- `fix:` — bug fix
- `docs:` — documentation only
- `chore:` — tooling, deps, ignored files
- `test:` — test infrastructure changes

Scope is optional but encouraged for integrations: `feat(cursor):`,
`feat(mcp):`, `feat(cli):`.

## Code style

- **JavaScript**: ES modules, no transpiler. Match the existing terse style in
  `cli/index.js` and `mcp/index.js`.
- **Markdown**: 80-column soft wrap, prefer `—` over `--` in prose.
- **Bash**: `set -euo pipefail` for any non-trivial script.

## Release process (maintainer only)

1. Update `CHANGELOG.md` — move `[Unreleased]` items under a new version heading.
2. Bump versions in `mcp/package.json` and `cli/package.json` (if user-visible).
3. Commit: `chore: release vX.Y.Z`.
4. Tag: `git tag vX.Y.Z && git push --tags`.
5. Create a GitHub Release from the tag with notes from `CHANGELOG.md`.

> npm publish is currently deferred. When demand justifies it, restore
> `.github/workflows/publish.yml` from git history and configure `NPM_TOKEN`.

## Code of conduct

This project follows the [Contributor Covenant 2.1](./CODE_OF_CONDUCT.md).
Be respectful. Disagree on substance, not people.

## Questions

Open a [Discussion](https://github.com/hyuniiiv/quantum-agent/discussions) for
questions, ideas, or "show and tell". Open an [Issue](https://github.com/hyuniiiv/quantum-agent/issues)
for bugs and concrete feature requests.
