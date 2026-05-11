import pytest
from pathlib import Path
from cosmos_vibe.core.orchestrator import MultiverseOrchestrator, Universe


@pytest.fixture
def orchestrator(tmp_path):
    import git
    repo = git.Repo.init(str(tmp_path))
    repo.index.commit("initial")
    return MultiverseOrchestrator(repo_path=str(tmp_path))


def test_spawn_creates_correct_number_of_universes(orchestrator):
    universes = orchestrator.spawn(
        goal="사용자 인증 구현",
        strategies=["jwt", "session", "oauth2"],
    )
    assert len(universes) == 3


def test_spawn_assigns_correct_names(orchestrator):
    universes = orchestrator.spawn(
        goal="사용자 인증 구현",
        strategies=["jwt", "session"],
    )
    names = [u.id for u in universes]
    assert names == ["alpha", "beta"]


def test_spawn_creates_worktree_dirs(orchestrator):
    universes = orchestrator.spawn(
        goal="사용자 인증 구현",
        strategies=["jwt", "session"],
    )
    for u in universes:
        assert u.worktree_path.exists()


def test_spawn_creates_claude_md(orchestrator):
    universes = orchestrator.spawn(
        goal="사용자 인증 구현",
        strategies=["jwt 기반 stateless 인증"],
    )
    claude_md = universes[0].worktree_path / "CLAUDE.md"
    assert claude_md.exists()
    content = claude_md.read_text(encoding="utf-8")
    assert "alpha" in content
    assert "jwt 기반 stateless 인증" in content


def test_list_universes(orchestrator):
    orchestrator.spawn(goal="테스트", strategies=["a", "b"])
    assert len(orchestrator.list_universes()) == 2


def test_get_universe(orchestrator):
    orchestrator.spawn(goal="테스트", strategies=["jwt"])
    u = orchestrator.get_universe("alpha")
    assert u is not None
    assert u.id == "alpha"


def test_get_nonexistent_universe_returns_none(orchestrator):
    assert orchestrator.get_universe("nonexistent") is None
