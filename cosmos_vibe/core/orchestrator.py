from dataclasses import dataclass
from pathlib import Path
import git
from jinja2 import Environment, FileSystemLoader

UNIVERSE_NAMES = ["alpha", "beta", "gamma", "delta", "epsilon"]
TEMPLATES_DIR = Path(__file__).parent.parent / "adapters" / "claude_code" / "templates"


@dataclass
class Universe:
    id: str
    strategy: str
    worktree_path: Path
    goal: str


class MultiverseOrchestrator:
    def __init__(self, repo_path: str = "."):
        self.repo = git.Repo(repo_path)
        self.repo_path = Path(repo_path)
        self._universes: dict[str, Universe] = {}
        self._jinja = Environment(loader=FileSystemLoader(str(TEMPLATES_DIR)))

    def spawn(self, goal: str, strategies: list[str]) -> list[Universe]:
        universes = []
        for i, strategy in enumerate(strategies):
            name = UNIVERSE_NAMES[i]
            worktree_path = self.repo_path / "universes" / name
            worktree_path.parent.mkdir(parents=True, exist_ok=True)

            self.repo.git.worktree(
                "add", str(worktree_path), "-b", f"universe/{name}", "--force"
            )

            claude_md = self._render_claude_md(
                universe_id=name, goal=goal, strategy=strategy
            )
            (worktree_path / "CLAUDE.md").write_text(claude_md, encoding="utf-8")

            universe = Universe(
                id=name,
                strategy=strategy,
                worktree_path=worktree_path,
                goal=goal,
            )
            self._universes[name] = universe
            universes.append(universe)

        return universes

    def _render_claude_md(self, universe_id: str, goal: str, strategy: str) -> str:
        template = self._jinja.get_template("CLAUDE.md.j2")
        return template.render(universe_id=universe_id, goal=goal, strategy=strategy)

    def list_universes(self) -> list[Universe]:
        return list(self._universes.values())

    def get_universe(self, universe_id: str) -> Universe | None:
        return self._universes.get(universe_id)

    def stop(self) -> None:
        for name in list(self._universes.keys()):
            worktree_path = self.repo_path / "universes" / name
            try:
                self.repo.git.worktree("remove", str(worktree_path), "--force")
            except git.GitCommandError:
                pass
        self._universes.clear()
