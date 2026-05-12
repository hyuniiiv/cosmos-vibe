# quantum-agent CLI

Non-LLM CLI for [QuantumAgent](https://github.com/hyuniiiv/quantum-agent). Manages cosmos worktrees and Quantum Memory (`.quantum/*.jsonl`) deterministically — no AI required.

Pair it with any LLM agent (Claude Code, Cursor, Cline, Aider, Continue, etc.) that follows the same filesystem contract.

> **npm publish deferred.** Run from a local clone for now. If you'd like an
> `npx`-able package, open an issue on the parent repo.

## Install (from source)

```bash
git clone https://github.com/hyuniiiv/quantum-agent
cd quantum-agent
# (no install step — pure Node, no dependencies)
```

Optional: alias for convenience:
```bash
alias qagent="node /absolute/path/to/quantum-agent/cli/index.js"
```

## Usage

```bash
node cli/index.js init alpha                  # create cosmos/alpha worktree + branch
node cli/index.js insight alpha "discovery"   # append to .quantum/alpha/insights.jsonl
node cli/index.js list                        # show active cosmos
node cli/index.js observe                     # print all insights
node cli/index.js observe --cosmos alpha      # one cosmos only
node cli/index.js crystallize alpha           # mark alpha as the collapsed solution
node cli/index.js stop                        # remove all worktrees (keep .quantum/)
node cli/index.js stop --purge                # also delete .quantum/
node cli/index.js help                        # show all commands
```

## Filesystem contract

- `cosmos/<name>/` — git worktree on branch `cosmos/<name>`
- `.quantum/<name>/insights.jsonl` — append-only JSON Lines

Verified by the upstream conformance suite (`tests/conformance.sh`, 16 checks).

## License

MIT — see [LICENSE](../LICENSE).
