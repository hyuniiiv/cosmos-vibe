# 🌌 Cosmos Vibe

> 하나의 접근법에 확정짓기 전에, 세 가지를 동시에 탐색하세요.

Claude Code 플러그인으로, 여러 AI 에이전트가 동시에 실행됩니다. 각자 같은 목표를
다른 전략으로 탐색합니다. 에이전트들은 실시간으로 발견을 공유합니다. 독립적으로
같은 결론에 도달하면 — 그게 신뢰 신호입니다. 다르게 갈라지면 — 그게 진짜 트레이드오프입니다.

```
/cosmos spawn --goal "사용자 인증 구현" --strategies "jwt,session,oauth2"
```

---

## 해결하는 문제

Claude Code로 무언가를 만들고 있습니다. Claude가 하나의 접근법으로 구현합니다.
배포합니다. 3주 후 아키텍처가 확장되지 않거나, 보안 엣지 케이스를 발견하거나,
다른 접근법이 더 나았을 거라는 걸 깨닫습니다.

Cosmos는 확정짓기 전에 탐색을 실행합니다. 이론적 비교가 아니라 — 실제 작동하는
구현체로, 진짜 문제를 발견하면서.

---

## 양자역학 → 개발

Cosmos Vibe는 여섯 가지 양자물리학 개념을 구체적인 개발 신호로 매핑합니다:

**중첩 (Superposition)** — N개의 cosmos가 동시에 실행됩니다. 각자 다른 전략으로.
해결 공간은 중첩 상태로 존재합니다 — 당신이 의식적으로 붕괴시키기 전까지는 승자가
없습니다. 하나를 만드는 시간에 N개의 탐색을 얻습니다.

**얽힘 (Entanglement)** — 에이전트들은 매 구현 단계 사이에 서로의 인사이트를
읽습니다. 한 cosmos의 발견이 전략을 합치지 않으면서 다른 cosmos로 실시간 전파됩니다.
alpha가 경쟁 조건 수정을 발견하면, beta와 gamma가 그걸 읽고 각자 구현에 적용합니다.

**공명 (Resonance)** — 여러 cosmos가 서로 복사하지 않고 독립적으로 같은 결론에
도달하면, 그 결정은 견고합니다. 모든 전략이 찾아냈습니다. 망설임 없이 채택하세요.

```
⚡ Resonance — 믿어도 됩니다:
   "15분 토큰 만료" — 3개 cosmos 독립 수렴
   "{ error: { code, message } } 포맷" — 3개 cosmos 독립 수렴
   "unknown email에도 dummy bcrypt 실행" — 3개 cosmos 독립 수렴
```

**불확정성 (Uncertainty)** — cosmos들이 진짜로 다른 결론을 내리면, 그건 실패가
아닙니다 — 진짜 트레이드오프입니다. 모든 차원을 동시에 최적화할 수 없습니다.
의식적인 선택을 하세요.

```
🌀 Uncertainty — 당신이 결정:
   "서명 알고리즘" — alpha: HS256 (단일 서버 단순성)
                     beta:  RS256 (멀티 서비스 키 배포)
   "bcrypt rounds" — alpha/gamma: 12 (보안 마진)
                     beta: 10 (NIST 기준, 더 빠름)
```

**관측 (Observation)** — 양자역학에서 관측은 시스템을 붕괴시키지 않습니다 — 현재
상태를 읽을 뿐입니다. `/cosmos observe`도 마찬가지입니다. cosmos들이 실행 중일 때
얼마든지 실행할 수 있습니다. 중첩은 유지됩니다. 매 관측은 지금 이 순간 각 cosmos가
어디 있는지의 스냅샷입니다 — 결정을 강요하지 않습니다.

**결정화 (Crystallization)** — 파동함수 붕괴. 충분히 관측했습니다.
`/cosmos crystallize <id>`는 하나의 현실을 선택하고, 결과를 추출하고, 선택적으로
메인 브랜치에 병합합니다. 다른 cosmos는 stop하기 전까지 중첩 상태를 유지합니다.

**결어긋남 (Decoherence)** — cosmos가 자신의 전략을 버리고 다른 cosmos를 통째로
복사하면, 독립적인 샘플로서의 가치를 잃습니다. 얽힘 규칙이 이를 명시적으로
방지합니다: 영향은 허용, 통째 채택은 금지입니다.

---

## 설치

```bash
claude plugins install https://github.com/hyuniiiv/cosmos-vibe
```

Python 없음. 벡터 DB 없음. subprocess 없음. 순수 마크다운 스킬.
Quantum Memory는 디스크의 평범한 JSON Lines 파일입니다.

---

## 빠른 시작

```
/cosmos spawn --goal "rate limiting 미들웨어 구현" --strategies "token-bucket,sliding-window,fixed-window"
```

세 cosmos가 병렬로 시작합니다. 각자 작동하는 구현체를 만들고,
매 주요 단계마다 서로의 인사이트를 읽습니다.

```
/cosmos observe
```

```
🌌 cosmos:alpha  (8 insights)  — token-bucket
   └ 원자적 카운터 업데이트를 위해 Redis HINCRBY 선택 — 경쟁 조건 방지
   └ 버스트 허용: 새 윈도우 첫 3초는 2× 속도 허용

🌌 cosmos:beta   (7 insights)  — sliding-window
   └ 슬라이딩 로그를 Redis sorted set으로 저장 (score = timestamp)
   └ ZREMRANGEBYSCORE + ZCARD 파이프라인 — 단일 라운드 트립

🌌 cosmos:gamma  (9 insights)  — fixed-window
   └ 윈도우 경계 2× 버스트 엣지 케이스 — 문서화
   └ 원자성을 위해 INCR + EXPIRE를 Lua 스크립트로 처리

⚡ Resonance — 믿어도 됩니다:
   "원자성을 위한 Redis Lua 스크립트 또는 파이프라인" — 3개 cosmos 독립 수렴
   "429 Too Many Requests + Retry-After 헤더" — 3개 cosmos 수렴
   "rate limit 헤더 (X-RateLimit-Limit, Remaining)" — 3개 cosmos 수렴

🌀 Uncertainty — 당신이 결정:
   "버스트 처리" — alpha: 명시적 버스트 허용 | gamma: 엣지 케이스만 문서화
   "사용자당 메모리" — beta: O(요청수) 슬라이딩 로그 | alpha/gamma: O(1) 카운터
```

원하는 결과 선택:

```
/cosmos crystallize beta    # beta 추출 — 현재 브랜치에 merge 여부 선택
/cosmos stop                # 모든 worktree와 브랜치 정리
```

---

## 커맨드

### `/cosmos spawn`

```
/cosmos spawn --goal "<목표>" --strategies "<s1,s2,...>"
```

전략마다 cosmos 하나씩 실행합니다. 이름은 알파벳 순으로 자동 할당
(alpha, beta, gamma, delta, epsilon — 최대 5개). 각 cosmos에 생성:

- `cosmos/<name>`에 격리된 git worktree
- `cosmos/<name>` 브랜치
- `.quantum/<name>/insights.jsonl` 양자 메모리 파일
- 목표·전략·얽힘 규칙이 담긴 `CLAUDE.md`

에이전트는 병렬 실행됩니다. 모두 완료되면 `/cosmos observe` 자동 실행.

| 플래그 | 설명 |
|--------|------|
| `--goal` | 모든 cosmos가 향해 작업하는 목표 |
| `--strategies` | 쉼표 구분 목록 — 전략마다 cosmos 하나 |

---

### `/cosmos observe`

모든 `.quantum/*/insights.jsonl`을 읽어 출력:

- 중첩 스냅샷 (cosmos별 최신 인사이트 2개)
- **Resonance 맵** — 모든 전략이 독립적으로 수렴한 결정
- **Uncertainty 맵** — 전략들이 진짜로 갈라진 결정
- Decoherence 경고 (cosmos가 전략 정체성을 잃었을 때)

---

### `/cosmos crystallize <id>`

하나의 cosmos를 독립 결과물로 결정화:

1. 핵심 결정, 거부된 대안, 얽힘 영향 요약
2. 최근 커밋 10개와 diff 통계 표시
3. merge(`git merge cosmos/<id> --no-ff`) 또는 브랜치 보존 선택

다른 cosmos는 영향받지 않습니다 — stop 전까지 중첩 유지.

---

### `/cosmos stop`

모든 cosmos worktree와 브랜치 제거. `.quantum/` 삭제 여부 선택
(기본적으로 인사이트는 보존됨).

---

## 얽힘이 동작하는 방식

각 에이전트 프롬프트는 매 주요 구현 단계 사이에 모든 `.quantum/*/insights.jsonl`을
읽도록 요구합니다:

```bash
# 매 단계 사이에 각 에이전트가 실행:
for f in $(ls .quantum/*/insights.jsonl 2>/dev/null); do cat "$f"; done
```

```bash
# 각 에이전트는 자신의 인사이트를 추가 (덮어쓰기 금지):
echo '{"content": "원자성을 위한 Redis Lua 스크립트", "ts": "2026-05-12T10:31:00Z"}' \
  >> .quantum/alpha/insights.jsonl
```

alpha가 2단계에서 "Redis Lua 스크립트가 경쟁 조건을 방지한다"고 기록하면,
beta가 3단계에서 그걸 읽고 슬라이딩 윈도우 전략을 유지하면서 패턴을 채택할 수 있습니다.
그게 얽힘입니다: 수렴 없는 영향.

---

## Quantum Memory

위치: 리포 루트의 `.quantum/` (git-ignore됨).

```
.quantum/
  alpha/insights.jsonl
  beta/insights.jsonl
  gamma/insights.jsonl
```

각 줄은 JSON 객체:

```json
{"content": "원자적 INCR+EXPIRE를 위한 Redis Lua 스크립트로 경쟁 조건 방지", "ts": "2026-05-12T10:31:00Z"}
```

- 각 cosmos는 자신의 namespace에만 **씁니다**
- 모든 cosmos는 모든 namespace를 **읽을 수 있습니다**
- 인사이트는 `/cosmos stop` 후에도 기본적으로 보존됩니다

---

## 언제 써야 하나

**적합:**
- 여러 유효한 접근법이 있고 트레이드오프가 명확하지 않을 때
- 이론 비교가 아니라 실제 작동하는 코드가 필요할 때
- 구현 세부사항이 중요할 때 (버그는 이론화가 아닌 코딩 중에 드러남)
- 평소라면 어떤 접근법을 써야 할지 조사에 몇 시간을 썼을 때

**불필요:**
- 답이 명확하다 — 그냥 Claude에게 물어보세요
- 작업이 작다 (1시간 이하) — 에이전트 오버헤드가 이점을 초과
- 이미 구현 중간이다 — 실행 도중이 아닌 결정 시점에 spawn
- 비용 제약이 타이트하다 — N개 cosmos = N × Claude API 비용

---

## 활용 사례

### 인증

```
/cosmos spawn --goal "사용자 인증 구현" --strategies "jwt-stateless,session-redis,oauth2-pkce"
```
*Resonance 예상:* 토큰 만료 전략, 에러 포맷, 타이밍 공격 방지
*Uncertainty 예상:* 무상태 vs 즉각 만료, 키 관리 복잡성

---

### API 설계

```
/cosmos spawn --goal "태스크 서비스 공개 API 설계" --strategies "rest,graphql,grpc"
```
*Resonance 예상:* 커서 기반 페이지네이션, 에러 envelope 형태
*Uncertainty 예상:* 스키마 유연성 vs 계약 엄격성, 전송 오버헤드

---

### 데이터베이스 스키마

```
/cosmos spawn --goal "소셜 피드 스키마 설계" --strategies "relational-normalized,document-denormalized,graph"
```
*Resonance 예상:* 별도의 activity/event 로그 필요성
*Uncertainty 예상:* 쓰기 vs 읽기 최적화 트레이드오프

---

### 성능 최적화

```
/cosmos spawn --goal "주문 API p99 레이턴시 개선" --strategies "db-indexing,query-rewrite,response-caching"
```
*Resonance 예상:* 실제 병목인 컬럼/쿼리
*Uncertainty 예상:* 캐시 무효화 복잡성 vs 순수 속도

---

### 리팩터링

```
/cosmos spawn --goal "거대한 UserService 분리" --strategies "extract-class,strangler-fig,event-driven"
```
*Resonance 예상:* 실제 경계가 어디인지
*Uncertainty 예상:* 마이그레이션 리스크 vs 클린 아키텍처

---

### 보안 강화

```
/cosmos spawn --goal "크리덴셜 스터핑 공격으로부터 로그인 엔드포인트 강화" --strategies "rate-limiting,captcha,device-fingerprinting"
```
*Resonance 예상:* 하드 차단보다 점진적 마찰이 낫다
*Uncertainty 예상:* UX 저하 vs 보안 마진

---

### LLM 비용 절감

```
/cosmos spawn --goal "LLM API 비용 60% 절감" --strategies "prompt-caching,model-routing,response-caching"
```
*Resonance 예상:* 절감 효과를 쌓는 연산 순서
*Uncertainty 예상:* 각 접근법의 결정론적 가정

---

## 리포지토리 구조

```
skills/
  spawn/SKILL.md        — /cosmos spawn
  observe/SKILL.md      — /cosmos observe
  crystallize/SKILL.md  — /cosmos crystallize
  stop/SKILL.md         — /cosmos stop
.claude-plugin/
  plugin.json           — 플러그인 매니페스트
cosmos/                 — 런타임 git worktree (git-ignore됨)
.quantum/               — 런타임 인사이트 파일 (git-ignore됨)
```

## 비용

N개 cosmos = N × Claude API 비용. Quantum Memory 읽기/쓰기는 로컬 파일 I/O.
`/cosmos observe`는 의미 분석을 위해 Claude 호출 1회.
`/cosmos crystallize`는 요약 리포트를 위해 Claude 호출 1회.

2개 cosmos로 시작하고, 첫 쌍이 흥미롭게 분기할 때만 추가하세요.
