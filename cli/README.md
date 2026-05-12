# @hyuniiiv/quantum-agent-cli

Non-LLM CLI for [QuantumAgent](https://github.com/hyuniiiv/quantum-agent). Manages cosmos worktrees and Quantum Memory (`.quantum/*.jsonl`) deterministically — no AI required.

Pair it with any LLM agent (Claude Code, Cursor, Cline, Aider, Continue, etc.) that follows the same filesystem contract.

## Install

```bash
npm install -g @hyuniiiv/quantum-agent-cli
# or run on-demand
npx -y @hyuniiiv/quantum-agent-cli help
```

## Usage

```bash
quantum-agent init alpha                    # create cosmos/alpha worktree + branch
quantum-agent insight alpha "discovery"     # append to .quantum/alpha/insights.jsonl
quantum-agent list                          # show active cosmos
quantum-agent observe                       # print all insights
quantum-agent observe --cosmos alpha        # one cosmos only
quantum-agent crystallize alpha             # mark alpha as the collapsed solution
quantum-agent stop                          # remove all worktrees (keep .quantum/)
quantum-agent stop --purge                  # also delete .quantum/
```

Also available as `qagent`.

## Filesystem contract

- `cosmos/<name>/` — git worktree on branch `cosmos/<name>`
- `.quantum/<name>/insights.jsonl` — append-only JSON Lines

Verified by the upstream conformance suite (`tests/conformance.sh`, 16 checks).

## License

MIT — see [LICENSE](https://github.com/hyuniiiv/quantum-agent/blob/master/LICENSE).
