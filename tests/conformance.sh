#!/usr/bin/env bash
# QuantumAgent filesystem-contract conformance tests.
#
# Any integration (Claude Code plugin, MCP server, Cursor rule, Cline, Aider,
# CLI wrapper, ...) MUST produce the same on-disk artifacts after running the
# four cosmos workflows. This script verifies the contract in an isolated
# temporary repo.
#
# Usage:
#   tests/conformance.sh                # run with the local CLI (cli/index.js)
#   tests/conformance.sh --cmd "my-cmd" # run against an alternative impl
#
# Exit codes: 0 = all pass, 1 = any check failed.

set -euo pipefail

CMD="${CMD:-node $(dirname "$0")/../cli/index.js}"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --cmd) CMD="$2"; shift 2 ;;
    *) echo "Unknown arg: $1" >&2; exit 2 ;;
  esac
done

PASS=0
FAIL=0

ok() { echo "  ✓ $1"; PASS=$((PASS+1)); }
fail() { echo "  ✗ $1" >&2; FAIL=$((FAIL+1)); }

check() {
  local name="$1"; shift
  if "$@" >/dev/null 2>&1; then ok "$name"; else fail "$name"; fi
}

TMPDIR=$(mktemp -d -t qagent-conformance-XXXXXX)
trap 'rm -rf "$TMPDIR"' EXIT

cd "$TMPDIR"
git init -q
git commit --allow-empty -q -m "initial"
echo ".quantum/" > .gitignore
echo "cosmos/" >> .gitignore
git add .gitignore
git commit -q -m "ignore cosmos artifacts"

echo "── 1. init creates worktree + branch + quantum namespace ──"
$CMD init alpha >/dev/null
check "cosmos/alpha/ worktree exists" test -d cosmos/alpha
check "cosmos/alpha branch exists"    git show-ref --verify --quiet refs/heads/cosmos/alpha
check ".quantum/alpha/insights.jsonl exists" test -f .quantum/alpha/insights.jsonl
check "insights.jsonl is non-empty" test -s .quantum/alpha/insights.jsonl

echo "── 2. insights are valid JSONL ──"
$CMD insight alpha "test discovery" >/dev/null
LINES=$(wc -l < .quantum/alpha/insights.jsonl | tr -d ' ')
[ "$LINES" -ge 2 ] && ok "insights.jsonl has ≥2 lines ($LINES)" || fail "insights.jsonl line count: $LINES"

while IFS= read -r line; do
  if echo "$line" | node -e "const l = require('fs').readFileSync(0,'utf8').trim(); const o = JSON.parse(l); if (!o.content || !o.ts) process.exit(1);"; then
    :
  else
    fail "invalid insight JSON: $line"
  fi
done < .quantum/alpha/insights.jsonl
ok "all insights parse as {content, ts}"

echo "── 3. list reflects active cosmos ──"
$CMD init beta >/dev/null
$CMD list | grep -q alpha && ok "list includes alpha" || fail "list missing alpha"
$CMD list | grep -q beta  && ok "list includes beta"  || fail "list missing beta"

echo "── 4. observe surfaces insights from all cosmos ──"
$CMD insight beta "beta discovery"  >/dev/null
OBS=$($CMD observe)
echo "$OBS" | grep -q "test discovery"  && ok "observe shows alpha insight" || fail "alpha insight missing"
echo "$OBS" | grep -q "beta discovery"  && ok "observe shows beta insight"  || fail "beta insight missing"

echo "── 5. crystallize records collapse marker ──"
$CMD crystallize alpha >/dev/null
grep -q "CRYSTALLIZE" .quantum/alpha/insights.jsonl && ok "crystallize marker recorded" || fail "no CRYSTALLIZE marker"

echo "── 6. stop removes worktrees and branches ──"
$CMD stop >/dev/null
[ ! -d cosmos/alpha ] && ok "cosmos/alpha worktree removed" || fail "cosmos/alpha still present"
[ ! -d cosmos/beta  ] && ok "cosmos/beta worktree removed"  || fail "cosmos/beta still present"
git show-ref --verify --quiet refs/heads/cosmos/alpha && fail "cosmos/alpha branch still exists" || ok "cosmos/alpha branch deleted"
test -d .quantum && ok "quantum memory preserved by default" || fail ".quantum/ wrongly deleted"

echo "── 7. stop --purge clears quantum memory ──"
$CMD init gamma >/dev/null
$CMD stop --purge >/dev/null
[ ! -d .quantum ] && ok ".quantum/ purged on --purge" || fail ".quantum/ remained after --purge"

echo
echo "═════════════════════════════════════"
echo "  PASS: $PASS    FAIL: $FAIL"
echo "═════════════════════════════════════"
[ "$FAIL" -eq 0 ]
