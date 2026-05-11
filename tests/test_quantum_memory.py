import pytest
import tempfile
from cosmos_vibe.core.quantum_memory import QuantumMemory


@pytest.fixture
def memory(tmp_path):
    return QuantumMemory(persist_path=str(tmp_path / "quantum"))


def test_write_and_retrieve_by_universe(memory):
    memory.write("alpha", "JWT 토큰에 user_id와 exp 포함")
    memory.write("alpha", "refresh_token은 7일 TTL로 설정")

    insights = memory.get_by_universe("alpha")
    assert len(insights) == 2
    assert insights[0]["universe_id"] == "alpha"
    assert any("JWT" in i["content"] for i in insights)


def test_multiple_universes_isolated(memory):
    memory.write("alpha", "JWT stateless 접근")
    memory.write("beta", "Redis 세션 방식")

    alpha_insights = memory.get_by_universe("alpha")
    beta_insights = memory.get_by_universe("beta")

    assert len(alpha_insights) == 1
    assert len(beta_insights) == 1
    assert alpha_insights[0]["content"] != beta_insights[0]["content"]


def test_get_latest_embeddings_returns_per_universe(memory):
    memory.write("alpha", "토큰 기반 인증")
    memory.write("beta", "세션 기반 인증")

    embeddings = memory.get_latest_embeddings()

    assert "alpha" in embeddings
    assert "beta" in embeddings
    assert len(embeddings["alpha"]["embedding"]) == 384  # all-MiniLM-L6-v2 output dim


def test_empty_memory_returns_empty(memory):
    assert memory.get_by_universe("nonexistent") == []
    assert memory.get_latest_embeddings() == {}
