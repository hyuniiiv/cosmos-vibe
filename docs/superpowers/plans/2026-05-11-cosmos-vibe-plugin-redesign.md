# Cosmos Vibe Plugin Redesign — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 기존 Python/ChromaDB/MCP 백엔드를 완전히 제거하고, `claude plugins install`로 설치 가능한 순수 Claude Code 플러그인으로 재구현한다.

**Architecture:** `.claude-plugin/plugin.json` + `skills/*/SKILL.md` 4개 파일로 구성. Python 파일 없음. 각 스킬은 Claude Code가 직접 해석·실행한다. Quantum Memory는 `.quantum/<name>/insights.jsonl` JSON Lines 파일로 대체. 실시간 얽힘은 서브에이전트 프롬프트가 "매 구현 단계 완료 시 `.quantum/*/insights.jsonl`을 직접 Read"하도록 명시해서 달성한다.

**Tech Stack:** Markdown skill files, git worktrees, Claude Code `Agent` tool (parallel dispatch), JSON Lines files

---

## File Map

```
cosmos-vibe/
  .claude-plugin/
    plugin.json              ← 플러그인 매니페스트 (name, version, keywords)
  skills/
    spawn/
      SKILL.md               ← /cosmos spawn — worktree 생성 + 병렬 에이전트 디스패치
    observe/
      SKILL.md               ← /cosmos observe — superposition 스냅샷 + entanglement 출력
    crystallize/
      SKILL.md               ← /cosmos crystallize <id> — 결과 추출
    stop/
      SKILL.md               ← /cosmos stop — worktree + 브랜치 정리
  CLAUDE.md                  ← 플러그인 설치 시 자동 로드 컨텍스트
  README.md
  .gitignore                 ← .quantum/ 포함

DELETE:
  cosmos_vibe/               ← Python 패키지 전체
  tests/                     ← Python 테스트 전체
  pyproject.toml             ← Python 빌드 설정
```

---

## Task 1: Python 백엔드 제거

**Files:**
- Delete: `cosmos_vibe/` (전체)
- Delete: `tests/` (전체)
- Delete: `pyproject.toml`

- [ ] **Step 1: Python 파일 삭제**

```bash
git rm -r cosmos_vibe/ tests/ pyproject.toml
```

Expected output:
```
rm 'cosmos_vibe/__init__.py'
rm 'cosmos_vibe/adapters/__init__.py'
...
rm 'pyproject.toml'
```

- [ ] **Step 2: 삭제 확인**

```bash
git status
```

Expected: 삭제된 파일들이 `deleted:` 로 staged 상태. `cosmos_vibe/`, `tests/`, `pyproject.toml` 없음.

- [ ] **Step 3: 커밋**

```bash
git commit -m "chore: remove Python backend (cosmos_vibe, tests, pyproject.toml)"
```

---

## Task 2: 플러그인 매니페스트

**Files:**
- Create: `.claude-plugin/plugin.json`

- [ ] **Step 1: 디렉토리 + plugin.json 생성**

파일: `.claude-plugin/plugin.json`

```json
{
  "name": "cosmos-vibe",
  "description": "Multiverse AI harness: parallel agents that observe and entangle",
  "version": "1.0.0",
  "keywords": ["multiverse", "parallel-agents", "entanglement", "exploration"]
}
```

- [ ] **Step 2: JSON 유효성 확인**

```bash
python -c "import json; json.load(open('.claude-plugin/plugin.json')); print('valid JSON')"
```

Expected: `valid JSON`

- [ ] **Step 3: 커밋**

```bash
git add .claude-plugin/plugin.json
git commit -m "feat: add .claude-plugin/plugin.json manifest"
```

---

## Task 3: spawn 스킬

**Files:**
- Create: `skills/spawn/SKILL.md`

- [ ] **Step 1: 디렉토리 생성**

```bash
mkdir -p skills/spawn skills/observe skills/crystallize skills/stop
```

- [ ] **Step 2: spawn/SKILL.md 작성**

파일: `skills/spawn/SKILL.md`

```markdown
# cosmos:spawn

Spawn N parallel universe agents to explore a goal using different strategies.
Each universe runs in its own git worktree. Agents write insights to
`.quantum/<name>/insights.jsonl` in real time and periodically read each
other's insights between implementation steps — achieving live entanglement
without external infrastructure.

## Trigger

`/cosmos spawn --goal "<goal>" --strategies "<strategy1,strategy2,...>"`

## Execution Steps

### Step 1 — Parse arguments

From the user's trigger message, extract:
- `--goal` value → the shared objective
- `--strategies` value → comma-separated; split into a list

Assign universe names in order: `alpha`, `beta`, `gamma`, `delta`, `epsilon` (max 5).

Example: `--strategies "jwt,session,oauth2"` → alpha=jwt, beta=session, gamma=oauth2

### Step 2 — Detect repo root

Run:
```bash
git rev-parse --show-toplevel
```

Store the output as `<repo_root>`. All absolute paths below use this.

### Step 3 — Create quantum memory directories

For each universe `<name>`:

```bash
mkdir -p <repo_root>/.quantum/<name>
touch <repo_root>/.quantum/<name>/insights.jsonl
```

### Step 4 — Create git worktrees

For each universe `<name>`:

```bash
git worktree add <repo_root>/universes/<name> -B universe/<name>
```

If the branch already exists, append `--force`.

Verify with:
```bash
git worktree list
```

### Step 5 — Write CLAUDE.md into each worktree

For each universe `<name>` with strategy `<strategy>`, write the following to
`<repo_root>/universes/<name>/CLAUDE.md`:

```markdown
# Universe <name> — Cosmos Vibe

## Goal
<goal>

## This Universe's Strategy
<strategy>

## Quantum Memory Rules

### Writing insights
After every significant decision or discovery (new file created, test written,
design decision made, key pattern found), append one line to your insights file.

Your insights file (absolute path):
  <repo_root>/.quantum/<name>/insights.jsonl

Format — one JSON object per line, no trailing comma:
{"content": "<insight text>", "ts": "<ISO 8601 timestamp e.g. 2026-05-11T12:00:00Z>"}

Use the Write tool to append, or Bash:
```bash
echo '{"content": "...", "ts": "2026-05-11T12:00:00Z"}' >> <repo_root>/.quantum/<name>/insights.jsonl
```

### Real-time entanglement (REQUIRED)
After EACH major implementation step, read all universe insight files to see
what other universes have discovered:

  <repo_root>/.quantum/alpha/insights.jsonl
  <repo_root>/.quantum/beta/insights.jsonl
  <repo_root>/.quantum/gamma/insights.jsonl
  (read whichever exist — skip missing files)

If another universe is converging on a similar pattern, note it in your next
insight. If you see a genuinely better approach, you may adapt — but preserve
your core strategy. Entanglement ≠ merging.
```

### Step 6 — Dispatch parallel agents

In a SINGLE response, make N Agent tool calls — one per universe. All run in
true parallel. Do NOT await one before starting the next.

For each universe `<name>` with strategy `<strategy>`, dispatch this prompt:

```
You are Universe <name> in a Cosmos Vibe multiverse exploration.

Working directory: <repo_root>/universes/<name>
(This is a git worktree of the main repo.)

Your first action: cd into your worktree:
  cd <repo_root>/universes/<name>

Goal: <goal>
Your strategy: <strategy>

━━━ QUANTUM MEMORY — follow these rules throughout ━━━

1. WRITE insights after every major step (file created, test written, design
   decision, key discovery). Append to:
     <repo_root>/.quantum/<name>/insights.jsonl
   
   One JSON line per insight:
   {"content": "<insight>", "ts": "<ISO timestamp>"}
   
   Bash append:
   echo '{"content": "...", "ts": "2026-05-11T12:00:00Z"}' >> <repo_root>/.quantum/<name>/insights.jsonl

2. READ all universe insights after each major step:
     <repo_root>/.quantum/alpha/insights.jsonl  (skip if missing)
     <repo_root>/.quantum/beta/insights.jsonl   (skip if missing)
     <repo_root>/.quantum/gamma/insights.jsonl  (skip if missing)
   
   If you see convergence with another universe, note it. Preserve your strategy.

━━━ Now implement the goal using your strategy. Work autonomously until complete. ━━━
```

### Step 7 — Report launch status

Before dispatching agents, output:

```
🌌 Spawning <N> universes...

  [alpha] universes/alpha  strategy: <strategy1>
  [beta]  universes/beta   strategy: <strategy2>
  [gamma] universes/gamma  strategy: <strategy3>

⚛️  Quantum Memory: .quantum/

Agents running. Will show superposition snapshot when complete.
```

### Step 8 — Auto-observe on completion

After all agents return, automatically run `/cosmos observe` to show the
superposition snapshot.
```

- [ ] **Step 3: 파일 존재 확인**

```bash
cat skills/spawn/SKILL.md | head -5
```

Expected: `# cosmos:spawn` 로 시작하는 헤더 확인

- [ ] **Step 4: 커밋**

```bash
git add skills/spawn/SKILL.md
git commit -m "feat: add cosmos:spawn skill with real-time entanglement"
```

---

## Task 4: observe 스킬

**Files:**
- Create: `skills/observe/SKILL.md`

- [ ] **Step 1: observe/SKILL.md 작성**

파일: `skills/observe/SKILL.md`

```markdown
# cosmos:observe

Show the current superposition snapshot: all universe insights and detected
entanglements. Uses Claude's semantic judgment rather than cosine similarity.

## Trigger

`/cosmos observe`

Also called automatically after `/cosmos spawn` completes.

## Execution Steps

### Step 1 — Detect repo root

```bash
git rev-parse --show-toplevel
```

Store as `<repo_root>`.

### Step 2 — Read all insights

Read every file matching `<repo_root>/.quantum/*/insights.jsonl`.

For each file that exists, parse each line as JSON:
`{"content": "<text>", "ts": "<timestamp>"}`

Build a map: `universe_id → [insights sorted by ts]`

If `.quantum/` is empty or missing, output:
```
(no universes active — run /cosmos spawn first)
```

### Step 3 — Output superposition snapshot

For each universe (sorted alphabetically), output:

```
🌌 Universe <name>  (<N> insights)
   └ <most recent insight, truncated to 100 chars>
   └ <second most recent insight, truncated to 100 chars>
```

Example:
```
🌌 Universe alpha  (12 insights)
   └ JWT sliding window expiry: access 15m, refresh 7d with rotation
   └ Chose RS256 over HS256 for key rotation support

🌌 Universe beta  (9 insights)
   └ Redis hash TTL 24h, no sliding window — simpler but less flexible
   └ Session store key: sess:<user_id>:<device_id>

🌌 Universe gamma  (14 insights)
   └ OAuth2 refresh token rotation + sliding expiry on access token
   └ Convergence with alpha detected: both using sliding expiry
```

### Step 4 — Detect entanglements

Analyze all insights semantically. Identify pairs of universes where the
same pattern, strategy, or conclusion is emerging independently.

For each detected entanglement pair:
- Name the pair (e.g., `alpha ↔ gamma`)
- Explain WHY they are entangled in one sentence (what pattern is converging)

Also identify strong divergences that are interesting:
- Pairs exploring fundamentally different approaches to the same sub-problem

### Step 5 — Output entanglement map

```
⚛️  Entanglements:
   alpha ↔ gamma  — both converging on sliding window token expiry strategy
   beta  ↔ gamma  — both handling refresh token rotation, different TTL values

🔀 Notable divergences:
   alpha vs beta  — stateless JWT (alpha) vs stateful Redis session (beta): fundamentally different trust models
```

If no entanglements:
```
⚛️  Entanglements:
   (none detected yet — agents may still be in early stages)
```
```

- [ ] **Step 2: 파일 확인**

```bash
cat skills/observe/SKILL.md | head -3
```

Expected: `# cosmos:observe`

- [ ] **Step 3: 커밋**

```bash
git add skills/observe/SKILL.md
git commit -m "feat: add cosmos:observe skill with semantic entanglement detection"
```

---

## Task 5: crystallize 스킬

**Files:**
- Create: `skills/crystallize/SKILL.md`

- [ ] **Step 1: crystallize/SKILL.md 작성**

파일: `skills/crystallize/SKILL.md`

```markdown
# cosmos:crystallize

Extract a specific universe's insights and branch state as a standalone result.
Other universes remain in superposition — they are NOT affected by crystallize.

## Trigger

`/cosmos crystallize <universe_id>`

Example: `/cosmos crystallize alpha`

## Execution Steps

### Step 1 — Detect repo root

```bash
git rev-parse --show-toplevel
```

Store as `<repo_root>`.

### Step 2 — Read insights

Read `<repo_root>/.quantum/<universe_id>/insights.jsonl`.
Parse each line as JSON.

If the file is empty or missing:
```
❌ Universe '<universe_id>' has no insights yet.
   Run /cosmos spawn first, or wait for agents to record insights.
```
Then stop.

### Step 3 — Summarize worktree branch state

```bash
git -C <repo_root>/universes/<universe_id> log --oneline -10
git -C <repo_root>/universes/<universe_id> diff HEAD --stat
git -C <repo_root>/universes/<universe_id> status --short
```

Show:
- Current branch name
- Last 10 commits
- Changed/uncommitted files

### Step 4 — Extract key decisions

From the insights, identify and summarize:
1. **Core design decisions** — What architectural choices were made?
2. **Key trade-offs** — What alternatives were considered and rejected?
3. **Final approach** — What is the universe's answer to the goal?
4. **Entanglement influence** — Did this universe adapt from another universe's insights?

Present as:

```
💎 Universe <universe_id> — Crystallization Report
════════════════════════════════════════════════

Strategy: <strategy>
Insights recorded: <N>
Branch: universe/<universe_id>

Core Decisions:
  1. <decision>
  2. <decision>

Key Trade-offs:
  - <trade-off>

Final Approach:
  <summary>

Entanglement Influence:
  <any cross-universe adaptation, or "none detected">
```

### Step 5 — Offer merge

Ask the user:

> Crystallization complete. Merge `universe/<universe_id>` into main?
> 
> - **yes** — `git merge universe/<universe_id> --no-ff`
> - **no** — keep the branch for later

Wait for user response.

**If yes:**
```bash
git merge universe/<universe_id> --no-ff -m "feat: crystallize universe/<universe_id>

Insights recorded: <N>
Strategy: <strategy>"
```

Output: `✅ Merged universe/<universe_id> into main.`

**If no:**
Output: `Branch universe/<universe_id> preserved. Run /cosmos crystallize <universe_id> again to merge later.`
```

- [ ] **Step 2: 파일 확인**

```bash
cat skills/crystallize/SKILL.md | head -3
```

Expected: `# cosmos:crystallize`

- [ ] **Step 3: 커밋**

```bash
git add skills/crystallize/SKILL.md
git commit -m "feat: add cosmos:crystallize skill"
```

---

## Task 6: stop 스킬

**Files:**
- Create: `skills/stop/SKILL.md`

- [ ] **Step 1: stop/SKILL.md 작성**

파일: `skills/stop/SKILL.md`

```markdown
# cosmos:stop

Remove all universe worktrees and branches. Optionally clean quantum memory.

## Trigger

`/cosmos stop`

## Execution Steps

### Step 1 — Detect repo root

```bash
git rev-parse --show-toplevel
```

Store as `<repo_root>`.

### Step 2 — List active worktrees

```bash
git worktree list
```

Identify all worktrees whose path contains `universes/`. Extract their names
(the final path segment: `alpha`, `beta`, etc.).

If no universe worktrees are found:
```
(no active universes)
```
Then skip to Step 5.

### Step 3 — Remove each worktree

For each universe worktree `<name>`:

```bash
git worktree remove <repo_root>/universes/<name> --force
```

If the command fails (worktree already removed), continue to the next.

### Step 4 — Delete universe branches

For each universe that had a worktree:

```bash
git branch -D universe/<name>
```

Ignore errors for branches that don't exist.

### Step 5 — Offer quantum memory cleanup

Ask the user:

> Delete `.quantum/` directory (all recorded insights)? 
> 
> - **yes** — permanently delete all insights
> - **no** — keep insights for reference

**If yes:**
```bash
rm -rf <repo_root>/.quantum/
```

**If no:**
Insights preserved at `.quantum/`.

### Step 6 — Confirm

Output:

```
🛑 All universes stopped.

   Worktrees removed: alpha, beta, gamma
   Branches deleted:  universe/alpha, universe/beta, universe/gamma
   Quantum memory: <deleted | preserved at .quantum/>
```
```

- [ ] **Step 2: 파일 확인**

```bash
cat skills/stop/SKILL.md | head -3
```

Expected: `# cosmos:stop`

- [ ] **Step 3: 커밋**

```bash
git add skills/stop/SKILL.md
git commit -m "feat: add cosmos:stop skill"
```

---

## Task 7: CLAUDE.md 업데이트

**Files:**
- Modify: `CLAUDE.md`

- [ ] **Step 1: CLAUDE.md 재작성**

파일: `CLAUDE.md`

```markdown
# COSMOS.md — Cosmos Vibe Harness Constitution

This repository is managed as a Cosmos Vibe multiverse harness.

## Universe Rules

- Each Universe runs independently in its own `universes/<name>/` worktree
- Do NOT directly copy code from other universes
- Record every significant discovery to `.quantum/<name>/insights.jsonl`
- After each major implementation step, read `.quantum/*/insights.jsonl` to
  pick up insights from other universes
- Entanglement means influence, not convergence — preserve your strategy

## Quantum Memory

- Location: `.quantum/` at repo root (excluded from git)
- Each universe writes ONLY to its own namespace: `.quantum/<name>/insights.jsonl`
- All universes may READ all namespaces
- Format: one JSON object per line — `{"content": "...", "ts": "..."}`

## Skills

- `/cosmos spawn --goal "<goal>" --strategies "<s1,s2,s3>"` — launch universes
- `/cosmos observe` — superposition snapshot + entanglement map
- `/cosmos crystallize <id>` — extract a universe's result
- `/cosmos stop` — remove all worktrees and branches
```

- [ ] **Step 2: 확인**

```bash
head -5 CLAUDE.md
```

Expected: `# COSMOS.md — Cosmos Vibe Harness Constitution`

- [ ] **Step 3: 커밋**

```bash
git add CLAUDE.md
git commit -m "docs: update CLAUDE.md for plugin redesign"
```

---

## Task 8: README.md 업데이트

**Files:**
- Modify: `README.md`

- [ ] **Step 1: README.md 재작성**

파일: `README.md`

```markdown
# 🌌 Cosmos Vibe

> Parallel AI agents that observe, entangle, and explore — not compete.

A Claude Code plugin implementing quantum-physics metaphors for AI development:
**superposition** (multiple solutions coexist), **entanglement** (agents influence
each other in real time), and **crystallization** (selective collapse).

## Install

```bash
claude plugins install <repo-url>
```

## Usage

```
/cosmos spawn --goal "implement user auth" --strategies "jwt,session,oauth2"
```

This creates 3 git worktrees (`universes/alpha`, `universes/beta`, `universes/gamma`)
and dispatches 3 parallel Claude agents. Each agent:

1. Implements the goal with its own strategy
2. Records insights to `.quantum/<name>/insights.jsonl` after each step
3. Reads all `.quantum/*/insights.jsonl` between steps — live entanglement

```
/cosmos observe
```

Shows the superposition snapshot:

```
🌌 Universe alpha  (12 insights)
   └ JWT sliding window expiry: 15m access, 7d refresh with rotation
   └ Chose RS256 for key rotation support

🌌 Universe beta  (9 insights)
   └ Redis TTL 24h — simpler but no sliding window
   └ Session key: sess:<user_id>:<device_id>

⚛️  Entanglements:
   alpha ↔ gamma  — both converging on sliding window expiry
```

```
/cosmos crystallize alpha   # extract alpha's result (merge optional)
/cosmos stop                # clean up all worktrees
```

## How entanglement works

The `Agent` tool runs subagents to completion in their own context — there's no
mid-run hook injection. Instead, each agent prompt explicitly instructs the agent
to **re-read `.quantum/*/insights.jsonl` between every major implementation step**.

If alpha writes "chose sliding window expiry" at step 3, gamma will read it at
step 4 and can adapt — while still maintaining its own OAuth2 strategy.

## No external dependencies

Pure markdown skills. No Python, no ChromaDB, no subprocess. Quantum Memory is
plain JSON Lines files. Resonance is Claude's semantic judgment.

## Cost

N universes = N × Claude API cost. All `.quantum/` reads/writes use local files.
```

- [ ] **Step 2: 커밋**

```bash
git add README.md
git commit -m "docs: rewrite README for plugin redesign"
```

---

## Task 9: .gitignore 확인 및 smoke test

**Files:**
- Verify: `.gitignore`

- [ ] **Step 1: .gitignore에 .quantum/ 있는지 확인**

```bash
grep "quantum" .gitignore
```

Expected: `.quantum/` 출력. 없으면:

파일 `.gitignore` 에 다음 줄 추가 (없는 경우에만):
```
.quantum/
```

- [ ] **Step 2: 플러그인 구조 확인**

```bash
find .claude-plugin skills CLAUDE.md -type f
```

Expected:
```
.claude-plugin/plugin.json
skills/spawn/SKILL.md
skills/observe/SKILL.md
skills/crystallize/SKILL.md
skills/stop/SKILL.md
CLAUDE.md
```

- [ ] **Step 3: plugin.json 재확인**

```bash
python -c "
import json
p = json.load(open('.claude-plugin/plugin.json'))
assert p['name'] == 'cosmos-vibe', f'name wrong: {p}'
assert 'version' in p, 'no version'
assert 'description' in p, 'no description'
print('plugin.json OK:', p['name'], p['version'])
"
```

Expected: `plugin.json OK: cosmos-vibe 1.0.0`

- [ ] **Step 4: 각 SKILL.md에 필수 섹션 있는지 확인**

```bash
python -c "
import pathlib
skills = ['spawn', 'observe', 'crystallize', 'stop']
for s in skills:
    content = pathlib.Path(f'skills/{s}/SKILL.md').read_text()
    assert '## Trigger' in content or '## Usage' in content, f'{s}: missing trigger/usage section'
    assert '## Execution Steps' in content or '## How to Execute' in content or '## Steps' in content, f'{s}: missing steps section'
    print(f'  skills/{s}/SKILL.md OK')
print('All skills validated.')
"
```

Expected: `All skills validated.`

- [ ] **Step 5: 최종 커밋**

```bash
git add .gitignore
git commit -m "chore: verify .gitignore has .quantum/ for plugin redesign"
```

---

## Self-Review

**Spec coverage:**
- ✅ §3 플러그인 구조 — Tasks 2-6 (plugin.json + 4 SKILL.md)
- ✅ §4.1 cosmos:spawn — Task 3 (worktree 생성, 병렬 에이전트, 실시간 얽힘 메커니즘)
- ✅ §4.2 cosmos:observe — Task 4 (superposition 스냅샷, entanglement 맵)
- ✅ §4.3 cosmos:crystallize — Task 5 (인사이트 추출, 머지 옵션)
- ✅ §4.4 cosmos:stop — Task 6 (worktree 제거, 브랜치 정리)
- ✅ §5 Quantum Memory 구조 (.quantum/<name>/insights.jsonl) — spawn SKILL.md에 경로 명시
- ✅ §6 서브에이전트 CLAUDE.md 템플릿 — spawn SKILL.md Step 5에 인라인
- ✅ §7 plugin.json — Task 2
- ✅ §9 마이그레이션 (Python 파일 삭제) — Task 1
- ✅ 실시간 얽힘 메커니즘 (spec §4.1 업데이트 내용) — spawn SKILL.md Step 6 에이전트 프롬프트에 명시

**Placeholder scan:** 없음 — 모든 단계에 완전한 파일 내용 또는 명령어 포함

**Type consistency:** SKILL.md 파일들은 코드가 아닌 마크다운이므로 타입 불일치 없음

**성공 기준 커버리지 (spec §8):**
- ✅ 기준 1: `claude plugins install` 가능 — plugin.json 유효 (Task 9 검증)
- ✅ 기준 2: `/cosmos spawn`으로 N개 worktree + 에이전트 실행 — Task 3
- ✅ 기준 3: 에이전트가 `.quantum/<id>/insights.jsonl`에 기록 — spawn SKILL.md 에이전트 프롬프트
- ✅ 기준 4: `/cosmos observe`가 superposition + entanglement 출력 — Task 4
- ✅ 기준 5: `/cosmos crystallize <id>`가 결과 추출 — Task 5
