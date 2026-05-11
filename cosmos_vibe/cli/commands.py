import json
import os
from pathlib import Path
import typer
import uvicorn

app = typer.Typer(help="Cosmos Vibe — 다차원 멀티유니버스 AI 하네스")


def _get_persist_path() -> str:
    return str(Path(".quantum").absolute())


@app.command()
def install(
    cursor: bool = typer.Option(False, "--cursor", help="Cursor용 설치 (MCP 직접 연결)"),
) -> None:
    """Claude Code hooks + MCP 서버를 프로젝트에 설치한다."""
    from cosmos_vibe.adapters.claude_code.installer import install as do_install
    do_install(project_root=Path("."))


@app.command()
def uninstall() -> None:
    """Cosmos Vibe를 프로젝트에서 제거한다."""
    from cosmos_vibe.adapters.claude_code.installer import uninstall as do_uninstall
    do_uninstall(project_root=Path("."))


@app.command()
def spawn(
    goal: str = typer.Option(..., "--goal", "-g", help="Universe들이 탐색할 목표"),
    strategies: str = typer.Option(..., "--strategies", "-s", help="쉼표로 구분된 전략 목록"),
) -> None:
    """N개의 Universe를 병렬로 시작한다."""
    from cosmos_vibe.core.orchestrator import MultiverseOrchestrator
    strategy_list = [s.strip() for s in strategies.split(",")]
    orch = MultiverseOrchestrator()
    universes = orch.spawn(goal=goal, strategies=strategy_list)

    typer.echo(f"\n🌌 {len(universes)}개 Universe 시작")
    for u in universes:
        typer.echo(f"  [{u.id}] {u.worktree_path}  전략: {u.strategy}")
    typer.echo(f"\n⚛️  Quantum Memory: {_get_persist_path()}")
    typer.echo("👁️  `cosmos observe` 로 상태를 확인하세요\n")


@app.command()
def observe() -> None:
    """현재 superposition 스냅샷을 출력한다."""
    from cosmos_vibe.core.quantum_memory import QuantumMemory
    from cosmos_vibe.core.resonance import ResonanceEngine

    memory = QuantumMemory(persist_path=_get_persist_path())
    engine = ResonanceEngine(quantum_memory=memory)
    engine.check_resonance()

    embeddings = memory.get_latest_embeddings()
    typer.echo("\n═══ SUPERPOSITION SNAPSHOT ═══\n")

    for uid in sorted(embeddings.keys()):
        insights = memory.get_by_universe(uid)
        partners = engine.get_entangled(uid)
        entangled_str = f"  entangled: {', '.join(partners)}" if partners else ""
        typer.echo(f"🌌 Universe {uid}  ({len(insights)} insights){entangled_str}")
        for insight in insights[-2:]:
            typer.echo(f"   └ {insight['content'][:80]}")

    typer.echo("\n─── Entanglement Map ───")
    if engine.active_entanglements:
        for pair, sim in engine.active_entanglements.items():
            typer.echo(f"  {pair[0]} ↔ {pair[1]}  similarity={sim:.3f}")
    else:
        typer.echo("  (no active entanglements)")
    typer.echo()


@app.command()
def crystallize(
    universe_id: str = typer.Argument(..., help="결정화할 Universe ID"),
) -> None:
    """특정 Universe의 현재 상태를 독립 결과물로 추출한다. 나머지 Universe는 계속 실행된다."""
    from cosmos_vibe.core.quantum_memory import QuantumMemory
    from cosmos_vibe.core.resonance import ResonanceEngine
    from datetime import datetime, timezone

    memory = QuantumMemory(persist_path=_get_persist_path())
    engine = ResonanceEngine(quantum_memory=memory)
    engine.check_resonance()

    insights = memory.get_by_universe(universe_id)
    if not insights:
        typer.echo(f"❌ Universe '{universe_id}' 에 인사이트가 없습니다.")
        raise typer.Exit(1)

    result = {
        "universe_id": universe_id,
        "insights": insights,
        "entanglements": [list(p) for p in engine.active_entanglements if universe_id in p],
        "crystallized_at": datetime.now(timezone.utc).isoformat(),
    }

    output_path = Path(f"crystallized_{universe_id}.json")
    output_path.write_text(json.dumps(result, indent=2, ensure_ascii=False))
    typer.echo(f"💎 {universe_id} crystallized → {output_path}")
    typer.echo(f"   {len(insights)} insights preserved")
    typer.echo("   (다른 Universe들은 계속 실행 중)")


@app.command()
def watch() -> None:
    """Observation API 서버를 시작하고 실시간 스트리밍을 활성화한다."""
    from cosmos_vibe.core.quantum_memory import QuantumMemory
    from cosmos_vibe.core.resonance import ResonanceEngine
    from cosmos_vibe.api.observation import create_app

    memory = QuantumMemory(persist_path=_get_persist_path())
    engine = ResonanceEngine(quantum_memory=memory)
    api_app = create_app(memory=memory, engine=engine)

    typer.echo("🔭 Observation API 시작 → http://localhost:7777")
    typer.echo("   GET  /observe         superposition 스냅샷")
    typer.echo("   WS   /stream          실시간 스트리밍")
    uvicorn.run(api_app, host="0.0.0.0", port=7777)


@app.command()
def stop() -> None:
    """모든 Universe worktree를 제거한다."""
    from cosmos_vibe.core.orchestrator import MultiverseOrchestrator
    orch = MultiverseOrchestrator()
    orch.stop()
    typer.echo("🛑 모든 Universe 종료됨")
