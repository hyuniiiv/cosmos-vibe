# 🌌 Cosmos Vibe

> 경쟁하지 않고 관측하고, 얽히고, 탐색하는 병렬 AI 에이전트.

양자역학 메타포를 AI 개발 워크플로우에 적용한 Claude Code 플러그인입니다.
격리된 에이전트를 실행하고 하나를 고르는 대신, Cosmos Vibe는 에이전트들이
**실시간으로 서로에게 영향을 주면서** 각자의 전략을 보존하도록 합니다.
의식적으로 중첩을 붕괴시키기 전까지는 어떤 전략도 버려지지 않습니다.

```
/cosmos spawn --goal "사용자 인증 구현" --strategies "jwt,session,oauth2"
```

세 에이전트가 병렬로 시작됩니다. 각자 자신의 해법을 구현하면서, 매 구현 단계마다
상대방의 발견을 읽습니다. 좋은 아이디어는 전파됩니다. 당신이 선택하기 전까지
어떤 전략도 폐기되지 않습니다.

---

## 개념

| 양자역학 | Cosmos Vibe |
|---------|-------------|
| **중첩 (Superposition)** | N개 Universe가 동시에 실행 — 강제로 승자를 정하지 않음 |
| **얽힘 (Entanglement)** | 에이전트들이 라이브 인사이트 스트림을 공유 — 합치지 않고 영향만 줌 |
| **관측 (Observation)** | `/cosmos observe` — 모든 라이브 Universe의 스냅샷 |
| **결정화 (Crystallization)** | `/cosmos crystallize <id>` — 하나의 Universe 결과 추출 |

### 왜 N개의 격리된 에이전트를 그냥 실행하면 안 되나요?

격리된 에이전트는 작업을 중복하고 결과의 90%를 버립니다. Cosmos Vibe 에이전트는
*얽혀 있습니다*: alpha가 "슬라이딩 윈도우 만료가 고정 TTL보다 안전하다"는 걸
발견하면, gamma는 다음 단계에서 그것을 읽고 채택하거나, 응용하거나, 의식적으로
거부할 수 있습니다 — 자신의 OAuth2 방향을 유지하면서요. N개의 탐색과
교차 수분(cross-pollination)을 동시에 얻습니다.

---

## 설치

```bash
claude plugins install https://github.com/hyuniiiv/cosmos-vibe
```

Python 없음. ChromaDB 없음. subprocess 없음. 순수 마크다운 스킬로 동작하며,
Quantum Memory는 디스크의 평범한 JSON Lines 파일입니다.

---

## 빠른 시작

```
/cosmos spawn --goal "사용자 인증 구현" --strategies "jwt,session,oauth2"
```

세 개의 git worktree(`universes/alpha`, `universes/beta`, `universes/gamma`)를
만들고 세 개의 병렬 Claude 에이전트를 디스패치합니다. 각 에이전트는:

1. 배정된 전략으로 목표를 구현
2. 각 단계 후 `.quantum/<name>/insights.jsonl`에 인사이트 기록
3. 다음 단계 전에 `.quantum/*/insights.jsonl` 전체 읽기 — 라이브 얽힘

세 개가 모두 완료되면:

```
/cosmos observe
```

```
🌌 Universe alpha  (12 insights)
   └ JWT 슬라이딩 윈도우 만료: 액세스 15분 / 리프레시 7일 (rotation 포함)
   └ 키 교체 지원을 위해 HS256 대신 RS256 선택

🌌 Universe beta  (9 insights)
   └ Redis TTL 24시간 — 운영이 단순, 슬라이딩 윈도우 불필요
   └ 세션 키: sess:<user_id>:<device_id> (멀티 디바이스 지원)

🌌 Universe gamma  (14 insights)
   └ OAuth2 + PKCE — 신뢰를 공급자에게 위임, 토큰 저장 불필요
   └ alpha 읽고 리프레시 토큰 rotation 채택 — 두 Universe 모두 7일 윈도우에 동의

⚛️  Entanglements:
   alpha ↔ gamma  — 슬라이딩 윈도우 토큰 만료에 수렴 중
   beta  ↔ alpha  — beta가 alpha의 키 교체 인사이트를 읽고 RS256 채택

Notable divergences:
   beta는 Redis TTL 24시간 유지 (alpha의 보안 우선 vs. beta의 운영 단순화 우선)
```

원하는 결과를 선택:

```
/cosmos crystallize alpha   # alpha 추출 — 현재 브랜치에 merge 여부 선택 가능
/cosmos stop                # 완료 후 모든 worktree와 브랜치 제거
```

---

## 커맨드

### `/cosmos spawn`

```
/cosmos spawn --goal "<목표>" --strategies "<s1,s2,...>"
```

전략마다 Universe 하나씩 실행합니다. Universe 이름은 알파벳 순서로 자동 할당됩니다
(alpha, beta, gamma, delta, ...). 각 Universe에는 다음이 생성됩니다:

- `universes/<name>`에 격리된 git worktree
- `universe/<name>` 브랜치
- `.quantum/<name>/insights.jsonl` 양자 메모리 파일
- 목표·전략·얽힘 규칙이 담긴 `CLAUDE.md`

에이전트는 단일 `Agent` 툴 디스패치로 병렬 실행됩니다. 모두 완료되면
`/cosmos observe`가 자동으로 실행됩니다.

**옵션**

| 플래그 | 설명 |
|--------|------|
| `--goal` | 모든 Universe가 향해 작업하는 목표 |
| `--strategies` | 쉼표로 구분된 목록 — 전략마다 Universe 하나 |

---

### `/cosmos observe`

모든 `.quantum/*/insights.jsonl` 파일을 읽어 출력합니다:

- 중첩 스냅샷 (Universe별 최신 인사이트 2개)
- Entanglement 감지 — 같은 결정으로 수렴하는 Universe 쌍
- Notable divergences — 보존할 가치 있는 흥미로운 전략 차이

Entanglement 감지는 Claude의 의미적 판단을 사용합니다. 벡터 DB 없음,
코사인 유사도 임계값 튜닝 없음.

---

### `/cosmos crystallize <id>`

Universe 하나의 결과를 추출합니다:

1. 양자 메모리를 읽어 핵심 결정, 트레이드오프, 얽힘 영향을 출력
2. 해당 worktree의 최근 커밋 10개와 diff 통계 표시
3. merge 여부 확인 (`git merge universe/<id> --no-ff`) 또는 브랜치 보존 선택

다른 Universe는 영향을 받지 않습니다 — 명시적으로 stop하기 전까지 중첩은 유지됩니다.

```
/cosmos crystallize gamma
```

---

### `/cosmos stop`

모든 Universe worktree와 브랜치를 제거합니다. `.quantum/` 삭제 여부를 묻습니다
(기본적으로 인사이트는 보존되어 세션 종료 후에도 검토 가능합니다).

```
/cosmos stop
```

---

## 얽힘이 동작하는 방식

`Agent` 툴은 서브에이전트를 자체 컨텍스트 윈도우에서 완료까지 실행합니다 —
실행 중 훅 주입은 없습니다. 대신 각 에이전트 프롬프트에 **모든 주요 구현 단계
사이에 `.quantum/*/insights.jsonl`을 다시 읽어야 한다**는 규칙이 명시됩니다.

```bash
# 각 에이전트가 단계 사이에 실행:
for f in $(ls .quantum/*/insights.jsonl 2>/dev/null); do cat "$f"; done
```

```bash
# 각 에이전트가 자신의 인사이트를 추가 (덮어쓰기 금지):
echo '{"content": "키 교체 지원을 위해 RS256 선택", "ts": "2026-05-12T10:31:00Z"}' \
  >> .quantum/alpha/insights.jsonl
```

alpha가 3단계에서 "슬라이딩 윈도우 만료"를 기록하면, gamma는 4단계에서
그것을 읽고 자신의 OAuth2 방향을 유지하면서 적응할 수 있습니다.

**얽힘은 영향이지 수렴이 아닙니다.** Universe들은 동의를 강요받지 않습니다.
상대의 발견을 의식적으로 거부하고 그 이유를 기록할 수 있습니다.

---

## Quantum Memory

위치: 리포 루트의 `.quantum/` (git-ignore됨).

```
.quantum/
  alpha/insights.jsonl
  beta/insights.jsonl
  gamma/insights.jsonl
```

각 줄은 JSON 객체입니다:

```json
{"content": "부하 상황에서 슬라이딩 윈도우 만료가 고정 TTL보다 안전함", "ts": "2026-05-12T10:31:00Z"}
```

- 각 Universe는 자신의 namespace에만 **씁니다**
- 모든 Universe는 모든 namespace를 **읽을 수 있습니다**
- 인사이트는 `/cosmos stop` 후에도 기본적으로 보존됩니다 — stop 시 확인하거나 수동으로 삭제

---

## 비용

**N개 Universe = N × Claude API 비용.**

Quantum Memory 읽기/쓰기는 로컬 파일 I/O — 추가 API 호출 없음.
`/cosmos observe`는 얽힘을 의미적으로 감지하기 위해 Claude 호출 1회 사용.
`/cosmos crystallize`는 결정을 요약하기 위해 Claude 호출 1회 사용.

비용 절감 팁: 먼저 Universe 2개로 시작하고, 첫 쌍이 흥미롭게 분기할 때만 추가하세요.

---

## Universe 규칙

- 각 Universe는 자체 git worktree에서 작업 — 작업 디렉토리 공유 없음
- 다른 Universe의 코드를 직접 복사하지 말 것 — 인사이트가 설계에 영향을 주도록 할 것
- 중요한 발견은 모두 `.quantum/<name>/insights.jsonl`에 기록
- 각 주요 구현 단계 후 `.quantum/*/insights.jsonl` 전체 읽기
- 얽힘은 영향이지 수렴이 아님 — 자신의 전략을 보존할 것

---

## 리포지토리 구조

```
skills/
  spawn/SKILL.md        — /cosmos spawn 구현
  observe/SKILL.md      — /cosmos observe 구현
  crystallize/SKILL.md  — /cosmos crystallize 구현
  stop/SKILL.md         — /cosmos stop 구현
.claude-plugin/
  plugin.json           — 플러그인 매니페스트
universes/              — 런타임 git worktree (git-ignore됨)
.quantum/               — 런타임 인사이트 파일 (git-ignore됨)
```
