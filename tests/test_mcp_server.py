import pytest
import tempfile
from cosmos_vibe.core.quantum_memory import QuantumMemory
from cosmos_vibe.core.resonance import ResonanceEngine
from cosmos_vibe.mcp.server import create_server


@pytest.fixture
def setup(tmp_path):
    memory = QuantumMemory(persist_path=str(tmp_path / "quantum"))
    engine = ResonanceEngine(quantum_memory=memory)
    server = create_server(memory=memory, engine=engine)
    return server, memory, engine


def test_quantum_write_records_insight(setup):
    server, memory, _ = setup
    result = server.call_tool("quantum_write", {"universe_id": "alpha", "content": "JWT 토큰 설계"})
    assert result["status"] == "recorded"
    assert result["universe_id"] == "alpha"
    insights = memory.get_by_universe("alpha")
    assert len(insights) == 1


def test_quantum_read_entangled_returns_partner_insights(setup):
    server, memory, engine = setup
    memory.write("alpha", "JWT access token with user_id and expiry")
    memory.write("gamma", "OAuth2 access token with user_id and expiry claims")
    engine.check_resonance()

    result = server.call_tool("quantum_read_entangled", {"universe_id": "alpha"})
    assert isinstance(result, list)


def test_quantum_observe_returns_snapshot(setup):
    server, memory, _ = setup
    memory.write("alpha", "JWT 인증")
    memory.write("beta", "세션 인증")

    result = server.call_tool("quantum_observe", {})
    assert "universes" in result
    assert "entanglements" in result
    assert "alpha" in result["universes"]


def test_quantum_crystallize_returns_universe_state(setup):
    server, memory, _ = setup
    memory.write("alpha", "JWT 인증 완성")

    result = server.call_tool("quantum_crystallize", {"universe_id": "alpha"})
    assert result["universe_id"] == "alpha"
    assert len(result["insights"]) == 1
    assert "crystallized_at" in result
