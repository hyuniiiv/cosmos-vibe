import pytest
from fastapi.testclient import TestClient
from cosmos_vibe.core.quantum_memory import QuantumMemory
from cosmos_vibe.core.resonance import ResonanceEngine
from cosmos_vibe.api.observation import create_app


@pytest.fixture
def client(tmp_path):
    memory = QuantumMemory(persist_path=str(tmp_path / "quantum"))
    engine = ResonanceEngine(quantum_memory=memory)
    memory.write("alpha", "JWT 인증 구현")
    memory.write("beta", "세션 인증 구현")
    app = create_app(memory=memory, engine=engine)
    return TestClient(app), memory, engine


def test_observe_returns_snapshot(client):
    test_client, _, _ = client
    response = test_client.get("/observe")
    assert response.status_code == 200
    data = response.json()
    assert "universes" in data
    assert "entanglements" in data
    assert "alpha" in data["universes"]


def test_get_specific_universe(client):
    test_client, _, _ = client
    response = test_client.get("/universes/alpha")
    assert response.status_code == 200
    data = response.json()
    assert data["universe_id"] == "alpha"
    assert len(data["insights"]) == 1


def test_get_nonexistent_universe_returns_404(client):
    test_client, _, _ = client
    response = test_client.get("/universes/nonexistent")
    assert response.status_code == 404


def test_get_entanglements(client):
    test_client, _, _ = client
    response = test_client.get("/entanglements")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_crystallize_endpoint(client):
    test_client, _, _ = client
    response = test_client.post("/crystallize/alpha")
    assert response.status_code == 200
    data = response.json()
    assert data["universe_id"] == "alpha"
    assert "crystallized_at" in data
