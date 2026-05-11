# COSMOS.md — Cosmos Vibe 하네스 헌법

## 이 프로젝트에서의 규칙

이 저장소는 Cosmos Vibe 멀티유니버스 하네스로 관리됩니다.

## Universe 규칙
- 각 Universe는 `universes/<name>/` 워크트리에서 독립적으로 실행됩니다
- 다른 Universe의 코드를 직접 읽거나 복사하지 마세요
- 발견한 패턴은 `quantum_write` 툴로 기록하세요
- 주입된 [ENTANGLED CONTEXT]는 참고만 하고 자신의 전략을 유지하세요

## Quantum Memory
- 위치: `.quantum/` (git에서 제외됨)
- 각 Universe는 자신의 namespace에만 씁니다
- 모든 Universe가 읽을 수 있습니다

## 관측
- `cosmos observe` — 현재 상태 스냅샷
- `cosmos watch` — 실시간 대시보드 (http://localhost:7777)
- Universe는 결코 강제로 하나로 수렴되지 않습니다
