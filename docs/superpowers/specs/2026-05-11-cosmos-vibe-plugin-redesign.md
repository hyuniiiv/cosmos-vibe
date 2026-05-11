# Cosmos Vibe — Plugin Redesign Spec

**날짜:** 2026-05-11
**상태:** Approved
**버전:** 1.0.0

---

## 1. 비전

> "병렬 AI 에이전트들이 고립된 채 경쟁하는 게 아니라, 서로 관측하고 공명하며 함께 탐색한다."

기존 구현(Python CLI + MCP 서버 + ChromaDB)을 완전히 제거하고, superpowers 플러그인과 동일한 방식으로 재설계한다. Claude Code에 `claude plugins install`로 설치하면 `/cosmos spawn`, `/cosmos observe`, `/cosmos crystallize` 스킬이 즉시 사용 가능해진다.

---

## 2. 무엇이 바뀌는가

| | 기존 | 새 설계 |
|---|---|---|
| 인터페이스 | Python CLI (`cosmos spawn`) | Claude Code 스킬 (`/cosmos spawn`) |
| 에이전트 실행 | `subprocess.Popen("claude ...")` | Claude `Agent` 툴 (내장, superpowers 방식) |
| Quantum Memory | ChromaDB + sentence-transformers | `.quantum/*.jsonl` 파일 |
| Resonance | 코사인 유사도 수치 | Claude의 의미적 판단 + 설명 |
| 설치 | `pip install cosmos-vibe` | `claude plugins install` |
| 외부 의존성 | Python, ChromaDB, GitPython, Jinja2 | 없음 |

---

## 3. 플러그인 구조

```
cosmos-vibe/
  .claude-plugin/
    plugin.json              ← 이름, 버전, 키워드
  skills/
    spawn/
      SKILL.md               ← /cosmos spawn 스킬
    observe/
      SKILL.md               ← /cosmos observe 스킬
    crystallize/
      SKILL.md               ← /cosmos crystallize 스킬
    stop/
      SKILL.md               ← /cosmos stop 스킬
  CLAUDE.md                  ← 플러그인 설치 시 자동 로드 컨텍스트
  README.md
```

기존 `cosmos_vibe/`, `tests/`, `pyproject.toml` 등 Python 관련 파일 전체 삭제.

---

## 4. 스킬 상세

### 4.1 `cosmos:spawn`

**트리거:** `/cosmos spawn --goal "<목표>" --strategies "<전략1,전략2,...>"`

**동작 순서:**

1. `--strategies` 파싱 → universe 이름 할당 (`alpha`, `beta`, `gamma`, ...)
2. 각 universe에 git worktree 생성:
   ```bash
   git worktree add universes/<name> -B universe/<name>
   ```
3. 각 worktree에 `CLAUDE.md` 작성 (목표, 전략, Quantum Memory 규칙 포함)
4. `.quantum/<name>/` 디렉토리 생성
5. `Agent` 툴로 N개 서브에이전트를 병렬 디스패치 (superpowers `dispatching-parallel-agents` 패턴):
   - 단일 응답에서 여러 `Agent` 툴 호출 → 진짜 병렬 실행
   - 각 에이전트는 독립된 컨텍스트에서 실행
6. 각 에이전트 프롬프트에 포함:
   - 목표 + 전략
   - worktree 경로에서 작업 (`cwd: universes/<name>`)
   - 인사이트 기록 규칙 (`.quantum/<name>/insights.jsonl` append)
   - **실시간 얽힘 규칙**: 매 주요 구현 단계 완료 후(파일 생성, 설계 결정, 테스트 통과 등) `.quantum/*/insights.jsonl`을 다시 읽어 다른 Universe의 최신 인사이트를 확인하고, 유의미한 수렴/발산이 있으면 자신의 전략에 반영
7. 모든 에이전트 완료 후 자동으로 `cosmos:observe` 실행

> **실시간 얽힘 메커니즘**: `Agent` 툴로 실행되는 서브에이전트는 단일 컨텍스트에서 완료까지 실행되므로 외부에서 hook을 주입할 수 없다. 대신, 각 서브에이전트 프롬프트에 **"각 구현 단계 완료 시마다 `.quantum/*/insights.jsonl`을 Read 툴로 직접 읽어라"** 고 명시한다. 이를 통해 alpha가 sliding window 인사이트를 기록하면, beta는 다음 단계에서 그 내용을 읽고 자신의 접근법을 조정할 수 있다.

### 4.2 `cosmos:observe`

**트리거:** `/cosmos observe`

**동작:**

1. `.quantum/*/insights.jsonl` 전체 읽기
2. Universe별 인사이트 목록 출력
3. Claude가 의미적으로 유사한 쌍을 감지하고 이유 설명
4. Superposition 스냅샷 출력:
   ```
   🌌 Universe alpha (jwt)     — 12 insights
      └ 토큰 만료 전략: sliding window 방식 채택
   🌌 Universe beta (session)  — 9 insights
      └ Redis TTL 24h, 슬라이딩 윈도우 없음
   🌌 Universe gamma (oauth2)  — 14 insights
      └ refresh token rotation + sliding expiry

   ⚛️  Entanglements:
      alpha ↔ gamma  — 둘 다 sliding window 만료 전략 수렴
   ```

### 4.3 `cosmos:crystallize`

**트리거:** `/cosmos crystallize <universe_id>`

**동작:**

1. 지정 universe의 `insights.jsonl` 전체 읽기
2. worktree 브랜치 상태 요약
3. 핵심 결정사항 + 구현 결과 추출하여 출력
4. (선택) 해당 브랜치를 main에 머지할지 사용자에게 확인

### 4.4 `cosmos:stop`

**트리거:** `/cosmos stop`

**동작:**

1. `git worktree remove universes/<name> --force` 로 모든 worktree 제거
2. `universes/` 디렉토리 및 `universe/*` 브랜치 정리
3. `.quantum/` 디렉토리 정리 (선택)

---

## 5. Quantum Memory 구조

```
.quantum/
  alpha/
    insights.jsonl    ← {"content": "...", "ts": "2026-05-11T12:00:00Z"}
  beta/
    insights.jsonl
  gamma/
    insights.jsonl
```

- 각 서브에이전트는 **자기 namespace에만 씀** (충돌 없음)
- **모든 namespace를 읽을 수 있음** (얽힘 컨텍스트)
- Write/Edit 툴로 직접 append
- `.gitignore`에 `.quantum/` 추가

---

## 6. 서브에이전트 CLAUDE.md 템플릿

각 worktree에 작성되는 `CLAUDE.md`:

```markdown
# Universe <id> — Cosmos Vibe

## 목표
<goal>

## 이 Universe의 전략
<strategy>

## Quantum Memory 규칙

### 인사이트 기록
중요한 발견이나 설계 결정을 내릴 때마다 다음 형식으로
`.quantum/<id>/insights.jsonl`에 한 줄 append하세요:
{"content": "<인사이트>", "ts": "<ISO 타임스탬프>"}

### 얽힘 컨텍스트
작업 중 `.quantum/*/insights.jsonl`을 읽어 다른 Universe의
발견을 참고할 수 있습니다. 참고만 하고 자신의 전략을 유지하세요.
```

---

## 7. plugin.json

```json
{
  "name": "cosmos-vibe",
  "description": "Multiverse AI harness: parallel agents that observe and entangle",
  "version": "1.0.0",
  "keywords": ["multiverse", "parallel-agents", "entanglement", "exploration"]
}
```

---

## 8. 성공 기준

| # | 기준 | 검증 방법 |
|---|---|---|
| 1 | `claude plugins install`로 설치 가능 | plugin.json 유효성 확인 |
| 2 | `/cosmos spawn`으로 N개 워크트리 + 에이전트 실행 | worktree 디렉토리 + 에이전트 실행 확인 |
| 3 | 에이전트가 `.quantum/<id>/insights.jsonl`에 기록 | 파일 내용 확인 |
| 4 | `/cosmos observe`가 superposition + entanglement 출력 | 출력 내용 확인 |
| 5 | `/cosmos crystallize <id>`가 결과 추출 | 출력 내용 확인 |

---

## 9. 마이그레이션

기존 Python 구현 파일 삭제:
- `cosmos_vibe/` 전체
- `tests/` 전체
- `pyproject.toml`
- `setup.cfg` (있다면)

유지:
- `COSMOS.md` (하네스 헌법, 내용 업데이트)
- `README.md` (내용 재작성)
- `docs/` (스펙 문서)
- `.gitignore` (`.quantum/` 추가)
