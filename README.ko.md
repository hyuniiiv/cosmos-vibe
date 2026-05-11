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

## 활용 사례

여러 가지 유효한 접근법이 존재하고 처음부터 정답이 명확하지 않은 모든 상황에
적합합니다. 전략들이 서로에게서 배울 수 있을수록 얽힘의 가치는 커집니다.

### 인증 & 인가

```
/cosmos spawn \
  --goal "사용자 인증 구현" \
  --strategies "jwt-stateless,session-redis,oauth2-pkce"
```

*얻을 수 있는 인사이트:* JWT의 무상태 확장성 vs. 세션의 즉각적 만료 처리
vs. OAuth2의 자격증명 미보관. alpha가 슬라이딩 윈도우 만료를 발견하면
gamma가 채택하는 경우가 많습니다 — 전송 방식은 달라도 만료 패턴은 수렴합니다.

---

```
/cosmos spawn \
  --goal "역할 기반 접근 제어(RBAC) 구현" \
  --strategies "rbac-flat,rbac-hierarchical,abac"
```

*얻을 수 있는 인사이트:* 플랫 RBAC은 쿼리가 단순하고, 계층형 RBAC은 조직 트리를
자연스럽게 처리하며, ABAC은 동적 정책으로 확장 가능한 유일한 방식입니다.
얽힘을 통해 계층형과 ABAC이 동일한 권한 검사 인터페이스로 수렴하는 경우가 많습니다.

---

### API 설계

```
/cosmos spawn \
  --goal "태스크 관리 서비스의 공개 API 설계" \
  --strategies "rest-resource,graphql,grpc"
```

*얻을 수 있는 인사이트:* REST는 캐시 친화적이고 범용적이며, GraphQL은 복잡한
클라이언트의 오버페칭을 제거하고, gRPC는 내부 서비스 처리량에서 우수합니다.
얽힘은 페이지네이션 설계를 드러내는 경우가 많습니다 — 세 전략 모두 커서 기반으로
수렴합니다.

---

```
/cosmos spawn \
  --goal "API 버저닝 전략 수립" \
  --strategies "url-path,header,query-param"
```

*얻을 수 있는 인사이트:* URL 경로는 가장 가시적이고 캐시 친화적이며, 헤더 버저닝은
URL을 깔끔하게 유지하지만 리버스 프록시에서 놀라운 동작을 유발할 수 있고,
쿼리 파라미터는 테스트가 가장 용이합니다. 세 방식은 명확한 승자 없이 diverge하는 경우가 많습니다.

---

### 데이터베이스 & 스토리지

```
/cosmos spawn \
  --goal "소셜 피드 스키마 설계" \
  --strategies "relational-normalized,document-denormalized,graph"
```

*얻을 수 있는 인사이트:* 정규화 스키마는 쓰기 일관성에 강하고, 문서 모델은
읽기 중심 피드 렌더링을 빠르게 하며, 그래프는 팔로워 순회를 쉽게 만듭니다.
얽힘을 통해 관계형과 문서 모두 별도의 activity 테이블이 필요하다는 결론에
독립적으로 도달하는 경우가 많습니다.

---

```
/cosmos spawn \
  --goal "전문 검색(Full-text search) 구현" \
  --strategies "postgresql-fts,elasticsearch,meilisearch"
```

*얻을 수 있는 인사이트:* PostgreSQL FTS는 인프라 오버헤드가 없지만 랭킹이 제한적이며,
Elasticsearch는 풍부한 스코어링을 가진 업계 표준이고, Meilisearch는 오타 허용이
내장된 빠른 설정을 제공합니다. alpha의 인덱싱 전략(부분 업데이트 vs. 전체 재인덱싱)이
세 전략 모두에 채택되는 경우가 많습니다.

---

```
/cosmos spawn \
  --goal "상품 목록 캐싱 레이어 설계" \
  --strategies "redis-cache-aside,redis-write-through,cdn-edge"
```

*얻을 수 있는 인사이트:* Cache-aside는 단순하고 명시적이며, write-through는 캐시를
항상 최신 상태로 유지하지만 쓰기와 결합되고, CDN 엣지 캐싱은 공개 콘텐츠에서 가장
빠릅니다. TTL 전략이 반복되는 얽힘 포인트입니다 — 세 전략 모두 "stale"의 정의에
동의해야 합니다.

---

### 성능 최적화

```
/cosmos spawn \
  --goal "주문 API p99 레이턴시를 800ms에서 200ms 이하로 개선" \
  --strategies "db-indexing,query-rewrite,response-caching"
```

*얻을 수 있는 인사이트:* 인덱싱은 근본 원인을 영구적으로 해결하고, 쿼리 재작성은
스키마 변경 없이 N+1을 제거하며, 캐싱은 레이턴시를 마스킹하지만 무효화 복잡성을
추가합니다. alpha의 인덱스 선택이 beta의 쿼리 재작성에 영향을 주는 경우가 많습니다
— 중요한 컬럼이 어디인지 수렴합니다.

---

```
/cosmos spawn \
  --goal "이미지 전달 파이프라인 최적화" \
  --strategies "cdn-offload,webp-conversion,lazy-loading"
```

*얻을 수 있는 인사이트:* CDN은 오리진 부하를 가장 극적으로 줄이고, WebP는 페이로드를
30~50% 절감하며, 지연 로딩은 페이로드 크기 없이 체감 성능을 향상시킵니다.
세 전략은 흔히 깔끔하게 결합됩니다 — 얽힘은 순서를 표면화합니다
(먼저 변환, 그 다음 캐시, 마지막으로 클라이언트에서 지연 로딩).

---

### 리팩터링 & 아키텍처

```
/cosmos spawn \
  --goal "거대한 UserService(2000줄) 분리" \
  --strategies "extract-class,strangler-fig,event-driven"
```

*얻을 수 있는 인사이트:* Extract-class는 가장 안전하고 기계적이며, Strangler Fig은
대규모 재작성 없이 점진적 마이그레이션을 가능하게 하고, 이벤트 기반은 미래 성장을
분리하지만 비동기 복잡성을 추가합니다. Strangler Fig과 이벤트 기반은 실행 방식이
달라도 같은 경계선으로 수렴하는 경우가 많습니다.

---

```
/cosmos spawn \
  --goal "콜백에서 async/await으로 마이그레이션" \
  --strategies "incremental-per-module,codemods,full-rewrite"
```

*얻을 수 있는 인사이트:* 점진적 방식은 리스크가 낮지만 혼합 코드가 수개월간 유지되며,
코드모드는 기계적 부분을 자동화하지만 엣지 케이스를 놓치고, 전체 재작성은 빠르지만
기능 동결이 필요합니다. 에러 전파와 취소 처리가 공통 얽힘 포인트로 등장합니다.

---

### 보안

```
/cosmos spawn \
  --goal "크리덴셜 스터핑 공격으로부터 로그인 엔드포인트 강화" \
  --strategies "rate-limiting,captcha,device-fingerprinting"
```

*얻을 수 있는 인사이트:* 속도 제한은 기본이지만 분산 IP로 우회 가능하며, CAPTCHA는
실제 사용자 UX를 저하시키고, 기기 핑거프린팅은 보이지 않지만 스토리지가 필요합니다.
세 전략 모두 점진적 마찰 — N회 실패 후 차단, 그 이전엔 허용 — 로 수렴하는 경우가
많습니다.

---

```
/cosmos spawn \
  --goal "사용자 DB의 PII 저장 보호" \
  --strategies "column-encryption,field-level-encryption,tokenization"
```

*얻을 수 있는 인사이트:* 컬럼 암호화는 구현이 가장 단순하며, 필드 레벨은 컴플라이언스를
위한 세분화된 제어를 제공하고, 토큰화는 데이터를 민감하지 않은 토큰으로 대체하여
시스템 간 동작합니다. 키 교체 전략이 반복되는 얽힘 포인트입니다.

---

### 테스트 전략

```
/cosmos spawn \
  --goal "CI 속도 저하 없이 결제 플로우 신뢰도 향상" \
  --strategies "unit-mocks,integration-real-db,contract-pact"
```

*얻을 수 있는 인사이트:* 모킹 단위 테스트는 빠르지만 목/프로덕션 불일치로 무음 장애가
발생하고, 실제 DB 통합 테스트는 진짜 버그를 잡지만 느리며, Pact 계약 테스트는 전체
통합 없이 경계를 검증합니다. 단위 테스트와 계약 테스트가 서로를 보완한다는 사실이
얽힘을 통해 드러납니다.

---

### 인프라 & 배포

```
/cosmos spawn \
  --goal "API 서버 무중단 배포 구현" \
  --strategies "blue-green,canary,rolling"
```

*얻을 수 있는 인사이트:* 블루-그린은 즉각적 롤백이 가능한 가장 단순한 모델이고,
카나리는 트래픽 비율 라우팅으로 폭발 반경을 줄이며, 롤링은 리소스 효율적이지만
롤백이 어렵습니다. 헬스 체크 설계가 공통 얽힘 포인트입니다 — 세 전략 모두
"healthy"의 정의에 동의해야 합니다.

---

```
/cosmos spawn \
  --goal "관찰 가능성(Observability) 스택 설계" \
  --strategies "prometheus-grafana,datadog,opentelemetry"
```

*얻을 수 있는 인사이트:* Prometheus+Grafana는 오픈소스로 고도로 커스터마이즈 가능하고,
Datadog은 최고의 즉시 사용 UX를 제공하며, OpenTelemetry는 벤더 중립적으로
미래를 대비합니다. 높은 카디널리티 레이블 관리가 공통 얽힘 포인트로 등장합니다.

---

### AI & LLM 기능

```
/cosmos spawn \
  --goal "앱에 문서 Q&A 기능 추가" \
  --strategies "rag-vector,rag-bm25,fine-tuning"
```

*얻을 수 있는 인사이트:* 벡터 RAG는 의미적 유사성에 강하고, BM25는 정확한 키워드
매칭에서 더 빠르며, 파인튜닝은 지식을 모델에 내재화하지만 업데이트 비용이 높습니다.
청킹 전략이 얽힘의 핫스팟입니다 — alpha의 청킹 실험이 beta에 채택되어 중복 작업을
방지합니다.

---

```
/cosmos spawn \
  --goal "LLM API 비용 60% 절감" \
  --strategies "prompt-caching,model-routing,response-caching"
```

*얻을 수 있는 인사이트:* 프롬프트 캐싱(Anthropic 프리픽스 캐시)은 반복 시스템
프롬프트 비용을 줄이고, 모델 라우팅은 단순한 요청을 저렴한 모델로 전송하며,
응답 캐싱은 결정론적 쿼리에서 무료입니다. 세 전략은 누적 가능하며, 얽힘을 통해
절감 효과를 최대화하는 적용 순서가 드러납니다.

---

### 프론트엔드 & UX

```
/cosmos spawn \
  --goal "활동 피드 무한 스크롤 구현" \
  --strategies "intersection-observer,scroll-event-throttled,virtualized-list"
```

*얻을 수 있는 인사이트:* Intersection Observer는 CPU 비용이 낮은 현대 표준이고,
스크롤 이벤트 스로틀링은 구형 브라우저에서 호환되며, 가상화는 10만 개 이상 항목을
처리하지만 렌더링 복잡성을 추가합니다. 세 전략 모두 API와의 커서 기반 페이지네이션
계약으로 수렴합니다.

---

```
/cosmos spawn \
  --goal "다단계 폼의 클라이언트 상태 관리" \
  --strategies "react-hook-form,zustand,url-state"
```

*얻을 수 있는 인사이트:* React Hook Form은 리렌더링을 최소화하고 유효성 검사를
처리하며, Zustand는 네비게이션 간 상태를 유지하고, URL 상태는 폼을 공유 가능하고
브라우저 뒤로가기 친화적으로 만듭니다. 유효성 검사 타이밍이 공통 얽힘 포인트로
등장합니다 — 언제 검사할지(onChange vs. onBlur vs. onSubmit).

---

### Cosmos Vibe를 쓰지 말아야 할 때

- 구현이 결정론적인 경우 — 올바른 접근법이 하나뿐일 때
- 작업이 매우 작은 경우 (1시간 이하) — 에이전트 오버헤드가 이점을 초과할 때
- 이미 구현 중간인 경우 — 실행 도중이 아닌 결정 시점에 spawn할 것
- 비용 예산이 빡빡한 경우 — N개 Universe = N × API 비용; 대규모 코드베이스에서
  Universe 3개는 비용이 빠르게 늘어남

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
