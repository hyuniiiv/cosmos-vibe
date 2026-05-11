import pytest
from cosmos_vibe.core.quantum_memory import QuantumMemory
from cosmos_vibe.core.resonance import ResonanceEngine
from cosmos_vibe.mcp.server import create_server


@pytest.fixture
def full_stack(tmp_path):
    memory = QuantumMemory(persist_path=str(tmp_path / "quantum"))
    engine = ResonanceEngine(quantum_memory=memory, threshold=0.70)
    server = create_server(memory=memory, engine=engine)
    return memory, engine, server


def test_full_flow_write_resonate_observe(full_stack):
    """Universe들이 insight를 기록하고, 얽히고, observe로 확인되는 전체 흐름."""
    memory, engine, server = full_stack

    # 1. 두 Universe가 각자 인사이트 기록
    server.call_tool("quantum_write", {
        "universe_id": "alpha",
        "content": "JWT access token with user_id, role, and expiry timestamp"
    })
    server.call_tool("quantum_write", {
        "universe_id": "gamma",
        "content": "OAuth2 access token containing user_id, scope, and expiry"
    })

    # 2. Resonance 확인
    events = engine.check_resonance()

    # 3. Observe — 모든 Universe 상태 반환
    snapshot = server.call_tool("quantum_observe", {})
    assert "alpha" in snapshot["universes"]
    assert "gamma" in snapshot["universes"]
    assert len(snapshot["universes"]["alpha"]["insights"]) == 1

    # 4. 얽힘 발생 시 entangled context 읽기 가능
    entangled = server.call_tool("quantum_read_entangled", {"universe_id": "alpha"})
    assert isinstance(entangled, list)

    # 5. Crystallize — alpha Universe 결정화, gamma는 superposition 유지
    crystal = server.call_tool("quantum_crystallize", {"universe_id": "alpha"})
    assert crystal["universe_id"] == "alpha"
    assert "crystallized_at" in crystal

    # gamma Universe는 여전히 독립적으로 존재
    gamma_insights = memory.get_by_universe("gamma")
    assert len(gamma_insights) == 1


def test_superposition_never_forced_to_collapse(full_stack):
    """crystallize 후에도 모든 Universe가 Quantum Memory에 독립적으로 존재한다."""
    memory, engine, server = full_stack

    server.call_tool("quantum_write", {"universe_id": "alpha", "content": "alpha insight"})
    server.call_tool("quantum_write", {"universe_id": "beta", "content": "beta insight"})
    server.call_tool("quantum_write", {"universe_id": "gamma", "content": "gamma insight"})

    # alpha를 crystallize
    server.call_tool("quantum_crystallize", {"universe_id": "alpha"})

    # 모든 Universe가 여전히 Quantum Memory에 존재
    assert len(memory.get_by_universe("alpha")) == 1
    assert len(memory.get_by_universe("beta")) == 1
    assert len(memory.get_by_universe("gamma")) == 1
