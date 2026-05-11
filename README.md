# 🌌 Cosmos Vibe

> 병렬 AI 에이전트들이 고립된 채 경쟁하는 게 아니라, 서로 관측하고 공명하며 함께 탐색한다.

양자역학의 **얽힘(Entanglement)** 과 **중첩(Superposition)** 을 AI 개발 워크플로우에 적용한 오픈소스 하네스.

## ⚡ 5분 퀵스타트

```bash
pip install cosmos-vibe
cosmos install          # Claude Code 설정
cosmos spawn --goal "사용자 인증 구현" --strategies "jwt,session,oauth2"
cosmos observe          # 3개 Universe의 superposition 상태 확인
```

## 🔬 무슨 일이 일어나나?

1. `spawn` → 3개 git worktree에서 Claude Code가 병렬 실행
2. 각 Claude Code가 작업하며 인사이트를 **Quantum Memory** (ChromaDB)에 기록
3. **Resonance Engine** 이 의미적 유사성을 감지 → 자동으로 **얽힘 채널** 형성
4. 얽힌 Universe는 상대방 컨텍스트를 받아 자신의 방향을 조정 (합쳐지는 게 아님)
5. `observe` → 모든 Universe가 동시에 존재하는 superposition 스냅샷

## 💡 기존 도구와의 차이

| | 기존 병렬 에이전트 | Cosmos Vibe |
|---|---|---|
| 에이전트 관계 | 고립, 경쟁 | 얽힘, 공명 |
| 결과 | 하나를 선택 | superposition 유지 |
| 인사이트 | 탐색 경로 소멸 | Quantum Memory에 보존 |
| 수렴 | 강제 | 선택적 (crystallize) |

## 🧩 아키텍처

```
AI 도구 (Claude Code / Cursor / Codex)
        │ MCP Protocol
cosmos-mcp  ← MCP 서버 (핵심)
        │
Quantum Memory (ChromaDB)  ← Universe별 인사이트 임베딩
        │ monitors
Resonance Engine  ← similarity > θ → 얽힘 생성
        │ creates/destroys
Entanglement Registry  ← 활성 얽힘 채널
```

## 🛠 MCP 툴

| 툴 | 설명 |
|---|---|
| `quantum_write` | Universe 인사이트를 Quantum Memory에 기록 |
| `quantum_read_entangled` | 얽힌 Universe들의 최신 인사이트 반환 |
| `quantum_observe` | 전체 superposition 스냅샷 반환 |
| `quantum_crystallize` | Universe 결과 추출 (나머지 계속 실행) |

## 📋 CLI

```bash
cosmos install                              # Claude Code hooks + MCP 서버 등록
cosmos spawn --goal "목표" --strategies "a,b,c"  # Universe 생성 및 병렬 실행
cosmos observe                              # superposition 스냅샷 출력
cosmos watch                                # 실시간 대시보드 (http://localhost:7777)
cosmos crystallize alpha                    # alpha Universe 결과 추출
cosmos stop                                 # 모든 Universe 종료
```

## ⚠️ 비용 안내

Universe N개 = Claude Code API 비용 N배. Resonance Engine 임베딩은 로컬(`sentence-transformers`) 처리로 추가 비용 없음.

기본값 3 Universe. 비용 민감 시 `--strategies "a,b"` 로 2개 사용 권장.

## 🤝 기여하기

Cursor, Codex, Windsurf 어댑터 기여 환영 → `cosmos_vibe/adapters/`

MIT License
