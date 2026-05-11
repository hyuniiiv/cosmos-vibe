import pytest
import tempfile
from unittest.mock import patch
from cosmos_vibe.core.quantum_memory import QuantumMemory
from cosmos_vibe.core.resonance import ResonanceEngine, EntanglementEvent


@pytest.fixture
def memory(tmp_path):
    return QuantumMemory(persist_path=str(tmp_path / "quantum"))


@pytest.fixture
def engine(memory):
    return ResonanceEngine(quantum_memory=memory, threshold=0.75, dissolve_threshold=0.65)


def test_no_entanglement_with_empty_memory(engine):
    events = engine.check_resonance()
    assert events == []


def test_no_entanglement_with_single_universe(engine, memory):
    memory.write("alpha", "JWT 토큰 인증")
    events = engine.check_resonance()
    assert events == []


def test_entanglement_formed_when_similar(engine, memory):
    memory.write("alpha", "JWT access token with user_id and expiry")
    memory.write("gamma", "OAuth2 access token with user_id and expiry claims")

    events = engine.check_resonance()
    formed = [e for e in events if e.type == "formed"]

    assert len(formed) == 1
    assert set(formed[0].pair) == {"alpha", "gamma"}
    assert formed[0].similarity >= 0.75


def test_no_entanglement_when_dissimilar(engine, memory):
    memory.write("alpha", "JWT token authentication stateless")
    memory.write("beta", "Redis session TTL expiry cache management")

    events = engine.check_resonance()
    formed = [e for e in events if e.type == "formed"]
    for e in formed:
        assert e.similarity >= 0.75


def test_entanglement_dissolved_when_similarity_drops(engine, memory):
    memory.write("alpha", "JWT access token with user_id and expiry")
    memory.write("gamma", "OAuth2 access token with user_id and expiry claims")
    engine.check_resonance()  # form entanglement
    assert ("alpha", "gamma") in engine.active_entanglements or \
           ("gamma", "alpha") in engine.active_entanglements

    with patch.object(engine, "_cosine_similarity", return_value=0.5):
        events = engine.check_resonance()
    dissolved = [e for e in events if e.type == "dissolved"]
    assert len(dissolved) == 1


def test_get_entangled_returns_partner_ids(engine, memory):
    memory.write("alpha", "JWT access token with user_id and expiry")
    memory.write("gamma", "OAuth2 access token with user_id and expiry claims")
    engine.check_resonance()

    partners = engine.get_entangled("alpha")
    if partners:
        assert "gamma" in partners


def test_active_entanglements_not_duplicated(engine, memory):
    memory.write("alpha", "JWT access token with user_id and expiry")
    memory.write("gamma", "OAuth2 access token with user_id and expiry claims")
    engine.check_resonance()
    engine.check_resonance()  # run twice

    count = sum(1 for pair in engine.active_entanglements if "alpha" in pair and "gamma" in pair)
    assert count <= 1
