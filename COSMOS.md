# COSMOS.md — QuantumAgent 하네스 헌법 (한국어)

이 저장소는 QuantumAgent 멀티버스 하네스(병렬 cosmos 탐색)로 관리됩니다.
영문 정본은 [`CLAUDE.md`](CLAUDE.md)이며, 이 문서는 한국어 요약입니다.

## 아키텍처 — Git-Native Orchestration

QuantumAgent는 2-계층 구조를 따릅니다:

- **Control Plane** — 의도, 계획, 문맥, 기억, 검토는 git 작업 트리 안의
  Markdown/JSONL 파일로 존재합니다. 사람과 AI 에이전트 모두 같은 파일을
  읽고 쓰며, 모든 변경은 diff/review/revert가 가능합니다.
- **Effector Layer** — 외부 API, DB, 브라우저, 로컬 실행은 호스트
  에이전트의 기본 도구(MCP, CLI 등)에 위임합니다. QuantumAgent는 이
  레이어를 소유하지 않으므로 Control Plane은 에이전트-중립적입니다.

파일시스템 계약(`.quantum/<name>/insights.jsonl`, `cosmos/<name>/`
워크트리)이 상호운용 경계입니다. 마크다운을 읽고 `git worktree`를 실행할
수 있는 모든 에이전트가 참여 가능합니다.

## Cosmos 규칙

- 각 cosmos는 `cosmos/<name>/` 워크트리에서 독립 실행됩니다
- 다른 cosmos의 코드를 직접 복사하지 마세요
- 모든 중요한 발견은 `.quantum/<name>/insights.jsonl`에 기록하세요
- 각 주요 구현 단계 후 `.quantum/*/insights.jsonl`을 모두 읽으세요
- 공명(수렴) = 신호 신뢰. 결깨짐(전면 복사) = 금지
- 양자얽힘은 영향이지 수렴이 아닙니다 — 자신의 전략을 유지하세요

## Quantum Memory

- 위치: 저장소 루트의 `.quantum/` (git 제외)
- 각 cosmos는 자기 네임스페이스에만 씁니다: `.quantum/<name>/insights.jsonl`
- 모든 cosmos는 모든 네임스페이스를 읽을 수 있습니다
- 형식: 한 줄당 JSON 객체 —
  `{"type": "<타입>", "content": "...", "ts": "<ISO 8601>"}`
- `type` 어휘: `discovery` (기본값), `decision`, `blocker`, `tunnel`,
  `jump`, `resonance`, `complete`, `crystallize`
- 레거시 항목(`type` 없거나 `[TUNNEL]`/`[JUMP]` 접두사)도 그대로 읽힙니다.
  `type` 누락 시 `discovery`로 취급.
- 동시성: POSIX에서 PIPE_BUF 미만 append는 원자적입니다. 단일 에이전트의
  순차 append는 안전. 같은 insights 파일에 동시 쓰기가 가능한 서브
  에이전트를 띄울 경우 `flock` 또는 임시파일+`mv`로 감싸세요.

## Quantum Signals

- **Resonance(공명)** — 여러 cosmos가 독립적으로 같은 결론에 도달 → 자신감 있게 ship
- **Uncertainty(불확실성)** — cosmos가 결정에서 갈림 → 의식적 트레이드오프, 개발자가 선택
- **Degeneracy(축퇴)** — 다른 전략이 기능적으로 동일한 구현을 만듦 → 자연 유일해 존재
- **Decoherence(결깨짐)** — cosmos가 전략을 잃고 다른 cosmos를 복사 → 표본 가치 상실
- **Quantum Tunneling** (`type: "tunnel"`) — 가정된 제약을 우회하는 해법 → 예상 외 경로
- **Quantum Jump** (`type: "jump"`) — 단 한 번의 얽힘 읽기가 불연속적 아키텍처 도약 유발
- **Bose-Einstein Condensate** — uncertainty 0 + 공명 결정 ≥3 + 모든 cosmos 참여 → 목표가 결정론적

## Skills

- `/cosmos spawn --goal "<목표>" --strategies "<s1,s2,s3>"` — cosmos 발진
- `/cosmos observe` — 중첩 스냅샷 + 공명/불확실성 맵
- `/cosmos crystallize <id>` — 한 cosmos를 결과로 붕괴
- `/cosmos stop` — 모든 워크트리/브랜치 제거
