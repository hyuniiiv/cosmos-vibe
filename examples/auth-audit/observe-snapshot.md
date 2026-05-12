# /cosmos:observe output

> `/cosmos:observe` is auto-invoked at the end of `/cosmos:spawn`
> (`skills/spawn/SKILL.md` Step 8). The content below is the verbatim
> auto-observe output for this run, captured from the Claude Code session.
>
> Two rounds were run on the same goal — the 2nd round was a deliberate
> re-spawn to test whether complementary findings would surface. The
> headline 3-way resonance held across both rounds; the 2nd round
> surfaced an additional **CRITICAL** (Electron CORS wildcard injection)
> and account-takeover write paths that the 1st run missed.
>
> Only company-identifying strings (`BIZPOS` → `EXAMPLE_SYSTEM`,
> `bizpos-settings` → `example-system-settings`) were masked. All file
> paths, line numbers, function names, library names, and severity
> grades are verbatim.

---

## 1차 점검 — Superposition Snapshot

3 cosmos converged. 43 insights total.

| Cosmos | Spin (전략)         | Insights |
|--------|---------------------|----------|
| alpha  | security-threat     | 22       |
| beta   | code-architecture   | 11       |
| gamma  | offline-resilience  | 10       |

### ⚛️ Resonance (3중 독립 수렴 — 최우선 신뢰)

세 cosmos가 독립적으로 동일 결론에 도달한 트라이어드:

**🔴 R1. JWT 무만료 + Revocation 단절 + 평문 토큰 저장**

- `createTerminalJWT` (`lib/terminal/jwt.ts`)에 `setExpirationTime()` 호출 누락 → 발급 토큰 영구 유효
- `requireTerminalAuth` (`lib/terminal/auth.ts`)가 서명만 검증, DB `terminal.status` 미조회 → 관리자가 단말기 inactive 처리해도 기존 토큰으로 결제 API 계속 통과
- `/api/device/token/refresh`만 status 체크하지만 `clockTolerance: 999_999_999`(31년)로 만료 무력화 (JTI/blacklist 없음)
- 토큰은 localStorage + IDB 평문 저장 (Electron safeStorage/OS 키체인 미사용)

→ 이 셋은 서로를 강화. 단발 수정 아닌 한 묶음으로 해결해야 함.

**🟠 R2. 런타임 페이로드 검증 부재**

- `as unknown as TerminalJWTPayload` 캐스팅, zod 등 schema validation 없음 (alpha + beta 합의)

**🟠 R3. JWT 알고리즘 allowlist 미지정**

- `jwtVerify(token, secret)` 호출에 `algorithms: ['HS256']` 옵션 없음 (alpha + gamma 합의)

### 🚨 Cosmos별 독자 발견 (스핀 유지된 고유 통찰)

**alpha (security-threat) — 추가 CRITICAL/HIGH**

- **C4.** `/api/setup/merchant` 권한 자율 상승: 신규 사용자가 `role: 'platform_admin'`로 자가 등록 가능 (RLS 비활성 명시됨) — OWASP A01 Broken Access Control
- **H1.** `cancel-request`의 termId 스푸핑: `body.termId` 사용 (`app/api/payment/cancel-request/route.ts:16`) — CLAUDE.md 규약 위반, 타 가맹점 거래 취소 시도 가능
- **H2.** `/api/terminals` GET cross-tenant: 호출자 `merchantId` 필터 없이 전 단말기/`merchant_key_id` 노출 (IDOR)
- **H3.** 기본 PIN `'1234'` 하드코딩 (`app/api/terminals/route.ts:62`)
- **M1.** Rate limit이 in-memory Map → 서버리스 다중 인스턴스에서 사실상 무력

**beta (code-architecture) — 구조적 결함**

- 세 가지 인증 스킴(Terminal JWT / Supabase cookie / X-Merchant-Key)의 ad-hoc 공존 — 라우트별 정책 레지스트리 없음
- `middleware.ts` 부재 → `/api/*` fail-closed 게이트 없음, 새 라우트 인증 누락 정적 검출 불가
- Web 측 인증 DRY 위반 — `merchant/*`, `client/*` 30+ 라우트에서 `supabase.auth.getUser()` + 역할 쿼리 인라인 반복. `requireTerminalAuth`는 추상화했는데 웹은 raw 호출 (비대칭)
- API Route 인증 매트릭스 작성 완료

**gamma (offline-resilience) — 단말기 특화**

- 이중 토큰 저장 desync: `activateTerminal`은 localStorage만 기록, `flushOfflineQueue`는 IDB(`settingsStore.deviceToken`) 읽음 → 동기 누락 시 첫 큐 플러시 실패
- 오프라인 큐 무결성 검증 부재: `pending_payments` IDB 레코드에 HMAC/서명 없음 → 직접 조작으로 amount 변조 가능
- `/api/payment/offline` termId 누락 통과: `records.filter(r => r.termId && r.termId !== termId)` — falsy면 통과 (alpha M4와 일치)
- 단말기 자동 잠금/세션 만료 정책 부재: idle timeout, PIN re-auth interval 없음
- displayWindow 보조 화면 인증 상태 desync: 별도 zustand instance
- auto-updater 후 토큰 회전 없음

### 🎯 통합 우선순위 (3 cosmos 합의)

| #  | 조치 | 트리거 cosmos | 영향 |
|----|------|---------------|------|
| 1  | JWT exp 부여 + refresh rotation (jti 회전) + `requireTerminalAuth`에서 `terminal.status` 캐시 조회 (60s TTL) | α+β+γ resonance | 토큰 폐기 가능 + 단말 무력화 가능 |
| 2  | `/api/setup/merchant` 초기 역할을 `merchant_admin`로 강등, RLS 활성화 | α | platform_admin 자율 승격 차단 |
| 3  | `cancel-request`에서 `body.termId` → `auth.payload.termId` 교체 | α | 타 가맹점 스푸핑 차단 |
| 4  | `/api/terminals` GET에 `merchantId` 필터 + `requireMerchantAdmin` 헬퍼 추출, 30+ 웹 라우트 마이그레이션 | α+β | IDOR + DRY |
| 5  | 초기 PIN을 단말기마다 무작위 6+자리 + 첫 로그인 강제 변경 + 서버측 PIN 검증 + DB lockout | α | Brute force + 디폴트 |
| 6  | 토큰을 Electron `safeStorage` (DPAPI/Keychain)로 이전, 단일 저장소화 | γ | 평문 추출 차단 |
| 7  | `middleware.ts` 도입 — `/api/*` fail-closed, public 경로 allowlist | β | 인증 누락 회귀 방지 |
| 8  | 오프라인 큐 HMAC 서명 + 서버측 `records[].termId` 필수화 | γ+α | IDB 변조 방지 |
| 9  | Rate limit을 Redis/Upstash로 이전, password 엔드포인트에도 적용 | α | 서버리스 brute force 방어 |
| 10 | `jwtVerify`에 `algorithms: ['HS256']` 명시 + zod payload 검증 + env startup 검증 | α+β+γ | Defense-in-depth |

### 📂 산출물

- `.quantum/alpha/insights.jsonl` (22 lines) — security findings
- `.quantum/beta/insights.jsonl` (11 lines) — architecture map + matrix
- `.quantum/gamma/insights.jsonl` (10 lines) — offline scenarios
- `cosmos/{alpha,beta,gamma}/` — 워크트리 (소스 미수정, audit-only)

---

## 2차 점검 — Superposition Snapshot

3 cosmos 완료. 1차 점검 대비 새로 발견된 인사이트 위주로 정리합니다.

### ⚛️ Resonance (3중 합의 — 1차와 동일하게 재확인)

- JWT 무만료 + Revocation 단절 + Refresh `clockTolerance: 999_999_999` — alpha+beta+gamma 일치
- `cancel-request`의 `body.termId` 신뢰 — alpha 명시
- JWT payload 런타임 검증 부재 (`as unknown as TerminalJWTPayload`) — alpha+beta 일치

### 🆕 1차에서 누락됐던 신규 발견

**alpha (security-threat)**

- **H1·H2.** `terminals/[id]/account` / `terminals/[id]/key` PUT — merchant 소유권 검증 부재
  - `eq('id', id)`만으로 UPDATE → 임의 가맹점 관리자가 타사 단말기 비밀번호/결제 키 덮어쓰기 가능 → `device/auth`로 JWT 탈취 → 전체 계정 takeover 경로
  - 1차 보고서엔 `/api/terminals` GET cross-tenant만 있었음. 이건 쓰기 권한 우회로 훨씬 심각
- **활성화 코드 엔트로피** — 8 hex (32-bit). M1(in-memory rate limit) 우회 시 brute force 가능

**beta (code-architecture)**

- **heartbeat의 중복 JWT 파싱** (`heartbeat/route.ts:28-36`) — `requireTerminalAuth` 통과 후 Authorization 헤더를 다시 파싱해 exp 추출. 헬퍼가 full claims를 반환하지 않아서 발생한 구조적 결함
- **`terminals` POST/GET의 스킴 충돌** — 같은 URL인데 GET=Terminal JWT, POST=Supabase cookie. 클라이언트가 일관된 멘탈 모델로 다룰 수 없음 → `/api/admin/terminals`로 분리 권장
- **`createTerminalJWT` 페이로드의 이중 캐스팅** (`as unknown as Record<string, unknown>`) — jose 타이핑이 정합되지 않음

**gamma (offline-resilience) — 가장 강력한 신규 발견**

- 🔴 **[TUNNEL] C3. Electron CORS 와일드카드 인젝션**
  - 위치: `electron/main.js:275-289`
  - 문제: 응답에 `Access-Control-Allow-Origin` 헤더가 없으면 `*` + `Authorization` 헤더 허용을 주입
  - 영향: XSS 또는 공급망 공격 발생 시 토큰을 임의 외부 origin으로 송출 가능. 1차 점검 완전 누락
- 🔴 **C1. 토큰 저장 이중화 desync (재확인 + 명확화)**
  - `activateTerminal()`은 localStorage에만 저장 (`lib/onlineSync.ts:41-43`)
  - `flushOfflineQueue()`는 IDB(zustand `settingsStore.deviceToken`)에서만 읽음 (`lib/txSync.ts:18`)
  - 활성화 직후 첫 오프라인 결제는 영원히 동기화 실패 가능 (heartbeat 401 → refresh가 둘 다 갱신해야 자기치유)
- 🟠 **M2. `syncedIds` 폴백 → 중복 청구 리스크**
  - `txSync.ts:43-48`: `result.syncedIds ?? []` — 서버 응답 변형 시 client는 pending 유지 → 다음 flush에서 재전송 → 서버측 `merchantOrderID` idempotency 미보장 시 이중 청구
- 🟠 **M3. PIN 평문 fallback** (`settingsStore.ts:68`)
  - `verifyPin`이 `!stored.startsWith('$2')` 분기로 평문 비교
  - 마이그레이션 잔여 코드인데 timing-leak 가능. 일회성 게이트로 좁혀야 함
- **m4. 로그 토큰 누출 위험** — `JSON.stringify(a)` 처리로 토큰이 인자에 섞이면 `%APPDATA%/EXAMPLE_SYSTEM/logs/main-*.log`에 평문 기록 가능
- **auto-updater pre-quit 훅 부재** — `quitAndInstall` 직전 flush 강제 + `isFlushing` 대기 없음

### 📊 1차 vs 2차 비교

| 항목 | 1차 | 2차 | 변화 |
|------|-----|-----|------|
| 인사이트 수 | 43 | ~33 | beta가 더 압축적, gamma가 더 깊이 |
| Critical resonance | 3개 (JWT exp, revocation, 평문 저장) | 3개 + CORS 와일드카드 + 토큰 desync | 2개 신규 Critical |
| 권한 우회 발견 | `/api/terminals` GET (읽기) | `terminals/[id]/account|key` PUT (쓰기) | takeover 경로 발견 |
| 오프라인 깊이 | 시나리오 6개 | TUNNEL 1개 + 시나리오 5개 | CORS 인젝션 추가 |
