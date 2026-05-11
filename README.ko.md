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

Cosmos Vibe는 양자물리학 개념을 구체적인 개발 메커니즘으로 매핑합니다.
아래의 모든 개념은 직접적인 동작 의미를 가집니다 — 장식용 메타포가 아닙니다.

### 한눈에 보기

| 개념 | 양자역학 | 개발 |
|------|---------|------|
| **파동-입자 이중성** | 입자는 측정 방식에 따라 파동이자 입자 | 목표 = 파동(순수 가능성); 각 cosmos = 입자(구체적 구현) |
| **영의 이중 슬릿** | 파동이 두 슬릿을 통과하면 간섭 무늬 생성 | 같은 목표가 N개 전략을 통과하면 공명(보강)과 불확정성(상쇄) 드러남 |
| **중첩** | 시스템이 여러 상태로 동시 존재 | N개 cosmos 병렬 실행 — 결정화 전까지 승자 없음 |
| **경로 적분** | 입자가 모든 경로를 동시에 취함; 간섭으로 결과 결정 | 모든 구현 경로를 동시에 탐색; 공명은 겹침에서 등장 |
| **양자 어닐링** | 양자 터널링으로 국소 최솟값 탈출, 전역 최솟값 탐색 | 병렬 cosmos가 단일 순차적 접근법이 빠질 국소 최적값 탈출 |
| **얽힘** | 입자들이 거리에 관계없이 서로 영향 | 전략을 합치지 않고 cosmos 간 실시간 인사이트 공유 |
| **양자 텔레포테이션** | 얽힘 + 고전 채널로 양자 상태 전송 | 인사이트가 `.quantum/` 파일(고전) + 얽힘 규칙(양자)로 전달 — 구현 복사 없음 |
| **복제 불가 정리** | 미지의 양자 상태는 완벽히 복제 불가 | cosmos는 다른 cosmos의 구현을 복제할 수 없음 — 각자 독립 진화 필수 |
| **파울리 배타 원리** | 동일한 양자 상태에 두 페르미온 동시 존재 불가 | 두 cosmos가 같은 전략을 쓸 수 없음 — 고유한 전략 필수 |
| **스핀** | 입자의 불변 고유 성질 | 각 cosmos는 탐색 방향을 정의하는 불변의 전략적 정체성을 가짐 |
| **양자 결맞음** | 시스템 전체에서 위상 관계 유지 | 각 cosmos가 전략적 무결성 유지; 결맞음 = 독립 샘플 가치 |
| **양자 터널링** | 입자가 고전적으로 통과 불가능한 장벽을 통과 | cosmos가 당연하다고 여긴 제약을 우회하는 해법 경로 발견 |
| **양자 도약** | 전자가 에너지 준위 사이를 불연속적으로 전이 | 단 하나의 인사이트로 cosmos가 불연속적 도약 — 점진적이 아닌 차원이 다른 전환 |
| **양자 간섭** | 파동이 보강(증폭) 또는 상쇄(소거) | 보강 → 공명; 상쇄 → 불확정성 |
| **공명** | 위상이 맞는 파동들이 서로를 증폭 | 여러 cosmos가 독립적으로 수렴 → 신호를 믿고 채택 |
| **불확정성 원리** | 위치와 운동량을 동시에 정확히 알 수 없음 | 모든 차원을 동시에 최적화 불가; 일부 트레이드오프는 근본적 |
| **슈뢰딩거의 고양이** | 중첩 상태의 시스템은 측정 전까지 모든 상태 동시 존재 | 각 cosmos는 결정화되어 테스트되기 전까지 최선이자 최악의 해법 |
| **축퇴** | 에너지가 동일한 서로 다른 여러 양자 상태 | 다른 전략이 동일한 결론 도달 = 축퇴된 해법; 동등성이 견고성 증명 |
| **보즈-아인슈타인 응축** | 모든 입자가 같은 바닥 상태로 붕괴 | 모든 결정에서 완전 공명 — 목표가 결정론적; 어떤 cosmos도 같은 답 |
| **측정 문제** | 관측이 파동함수를 붕괴시키는 역설 | `/cosmos observe` ≠ 붕괴; `/cosmos crystallize` = 붕괴. 의도적 구분 |
| **관측** | 비파괴 측정으로 상태를 읽음 | cosmos 실행 중 `/cosmos observe` 자유 실행 — 중첩 유지 |
| **결정화** | 파동함수 붕괴 — 하나의 고유상태 선택 | cosmos 하나 선택, 결과 병합; 중첩 종료 |
| **결어긋남** | 환경과의 상호작용으로 양자 결맞음 상실 | 다른 cosmos를 복사한 cosmos는 전략적 독립성 상실 — 더 이상 유효한 샘플 아님 |
| **기준계** *(특수상대성이론)* | 관측자의 기준계에 따라 어떤 값은 상대적이고 어떤 값은 불변 | 공명 = 기준계 불변 답 (어떤 제약 집합에서도 성립); 불확정성 = 기준계 의존 답 (제약에 따라 달라짐 — "무상태 확장성" 기준계 vs "즉각 폐기" 기준계) |
| **측지선 + 시공간 곡률** *(일반상대성이론)* | 질량이 시공간을 휘어 자유 입자가 측지선(국소 최단 경로)을 따름 | 강한 문제 제약이 해법 공간을 휘게 함; 각 전략은 고유한 측지선을 따름 — 극단적 곡률에서 모든 경로가 수렴 → BEC |
| **등가 원리** *(일반상대성이론)* | 국소적으로 중력과 관성 가속도는 구별 불가 | 국소적으로 임시 해결책과 제대로 된 설계는 동일하게 보임; 더 넓은 아키텍처 관점에서만 차이가 드러남 — `/cosmos observe`가 그 시야를 제공 |

---

### 핵심 메커니즘 상세

**파동-입자 이중성 + 영의 이중 슬릿**

구현 전의 목표는 순수한 파동입니다 — 확정된 형태 없이 모든 가능한 해법의 확률
분포입니다. N개의 전략(슬릿)을 통과시키면 간섭 무늬가 나타납니다. 전략들이 동의하는
곳 = 보강 간섭 → 공명. 전략들이 다른 곳 = 상쇄 간섭 → 불확정성. 무늬가 어떤 결정이
견고하고 어떤 것이 진짜 트레이드오프인지 정확히 알려줍니다.

**경로 적분 + 양자 어닐링**

파인만의 경로 적분: 입자는 동시에 모든 가능한 경로를 취합니다. Cosmos Vibe는 모든
전략을 동시에 실행합니다. 간섭에서 살아남는 "가장 확률 높은 경로"가 공명 출력입니다.
양자 어닐링이 최적화 차원을 추가합니다: 순차적 의사결정은 국소 최적값에 갇힙니다.
병렬 cosmos는 전체 해법 공간을 동시에 탐색함으로써 이를 탈출합니다.

**복제 불가 정리 + 파울리 배타 원리 + 스핀**

이 세 가지가 함께 cosmos가 왜 독립적이어야 하는지 정의합니다. 복제 불가: 미지의
양자 상태를 복제할 수 없으므로, cosmos는 다른 cosmos의 구현을 통째로 복사할 수
없습니다. 파울리 배타: 두 페르미온이 같은 상태를 점유할 수 없으므로, 두 cosmos가
같은 전략을 쓸 수 없습니다. 스핀: 각 입자의 고유 정체성은 불변이므로, 각 cosmos의
핵심 전략은 실행 내내 보존되어야 합니다. 이 중 어느 하나라도 어기면 독립 샘플
가치를 잃습니다.

**얽힘 + 양자 텔레포테이션**

얽힘은 채널이고, 텔레포테이션은 메커니즘입니다. alpha가 `.quantum/alpha/insights.jsonl`에
인사이트를 기록하고 beta가 읽으면, 인사이트는 "텔레포트"됩니다 — 고전 채널(파일 I/O)
+ 얽힘 관계(각 에이전트 프롬프트의 읽기 요구사항)를 통해 정보가 이동합니다. alpha의
원본 구현은 그대로 유지됩니다. beta는 자신의 전략적 맥락에서 관련 패턴을 재구성합니다.

**양자 터널링 + 양자 도약**

두 가지 서로 다른 돌파 유형입니다. 터널링: cosmos가 당연히 어렵다고 여긴 제약을
우회하는 해법을 찾는 것 — 벽을 넘는 대신 뚫고 지나갑니다. 도약: cosmos가 다른
cosmos의 인사이트를 읽고 불연속적인 아키텍처 전환을 하는 것 — 점진적 적응이 아닌
질적으로 다른 구현 수준으로의 순간적 전환. 둘 다 순차적 탐색에서는 좀처럼 찾을 수
없는 비자명한 해법을 생성합니다.

**슈뢰딩거의 고양이 + 측정 문제**

각 cosmos는 결정화되어 테스트되기 전까지 동시에 최선이자 최악의 해법입니다.
`/cosmos observe`는 비파괴 측정 — 중첩을 붕괴시키지 않고 상태를 읽습니다.
`/cosmos crystallize`는 파괴적 측정 — 하나의 cosmos를 확정된 결과로 붕괴시킵니다.
이 구분은 의도적입니다: observe는 원할 때 언제든 실행; crystallize는 준비됐을 때만.

**공명 + 축퇴 + 보즈-아인슈타인 응축**

공명은 보강 간섭 — 여러 cosmos가 독립적으로 같은 결론에 도달하는 것입니다. 축퇴가
이를 더 깊게 합니다: *다른* 전략이 *동일한* 해법을 내면, 그 해법들은 동일한 "에너지"를
가집니다 — 바닥 상태에서 동등합니다. 모든 결정이 모든 cosmos에서 공명하면
보즈-아인슈타인 응축에 도달합니다: 목표가 결정론적이었고, 어떤 cosmos도 같은 답을
찾았을 것입니다. 높은 공명 = 높은 신뢰. 완전한 응축 = 처음부터 정답이 하나였음.

**기준계 (특수상대성이론)**

특수상대성이론에서 일부 측정값은 관측자의 기준계에 상대적이고, 일부는 모든 기준계에서
불변입니다. 개발 결정도 마찬가지입니다. 공명은 **기준계 불변** 결론을 식별합니다 —
어떤 제약 조건 아래에서도 성립하는 답. 불확정성은 **기준계 의존** 결정을 표시합니다:
"무상태 확장성" 기준계냐 "즉각 폐기 가능성" 기준계냐에 따라 정답이 달라집니다.
전략이 곧 기준계입니다. 모든 기준계에서 살아남는 것이 당신의 불변 진리입니다.

**측지선 + 시공간 곡률 (일반상대성이론)**

일반상대성이론에서 질량은 시공간을 휘고, 자유 입자는 측지선 — 곡률 공간에서 국소적으로
가장 직선에 가까운 경로 — 을 따릅니다. 문제의 제약이 해법 공간을 같은 방식으로 휩니다:
각 전략은 그 지형에서 자신의 자연스러운 측지선을 따릅니다. 제약이 약할 때 측지선들은
크게 발산합니다(높은 불확정성). 제약이 극단적일 때 — 엄격한 성능 한계, 컴플라이언스
요구사항 — 모든 측지선이 같은 영역으로 수렴합니다. 극한에서 모든 전략이 같은 지점에
도달합니다: 보즈-아인슈타인 응축. 전략이 아니라 제약이 곡률을 결정합니다. BEC는
강하게 제약된 문제, 불확정성은 약하게 제약된 문제를 신호합니다.

**등가 원리 (일반상대성이론)**

아인슈타인의 등가 원리: 국소적으로 중력 가속도와 관성 가속도는 구별할 수 없습니다.
개발에서: 국소적으로 임시 해결책과 제대로 설계된 해법은 동일하게 보입니다 — 같은 동작,
같은 테스트 통과. 더 넓은 맥락에서만 차이가 드러납니다(유지보수성, 확장성, 엣지 케이스).
`/cosmos observe`가 그 더 넓은 시야를 제공합니다: 전략들이 같은 결론의 *이유*에서
갈라질 때, 그것이 하나의 경로가 제대로 된 설계로 위장한 국소적 해결책일 수 있다는 신호입니다.

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
