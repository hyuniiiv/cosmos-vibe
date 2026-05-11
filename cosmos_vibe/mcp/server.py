from datetime import datetime, timezone
from mcp.server.fastmcp import FastMCP
from cosmos_vibe.core.quantum_memory import QuantumMemory
from cosmos_vibe.core.resonance import ResonanceEngine


class CosmosServer:
    """Testable wrapper around the FastMCP server."""

    def __init__(self, memory: QuantumMemory, engine: ResonanceEngine):
        self.memory = memory
        self.engine = engine
        self.mcp = FastMCP("cosmos-vibe")
        self._tools: dict = {}
        self._register_tools()

    def _register_tools(self) -> None:
        memory = self.memory
        engine = self.engine

        def quantum_write(universe_id: str, content: str) -> dict:
            """Record an insight from a Universe into Quantum Memory."""
            memory.write(universe_id, content)
            return {"status": "recorded", "universe_id": universe_id}

        def quantum_read_entangled(universe_id: str) -> list[dict]:
            """Get insights from Universes entangled with the given Universe."""
            partners = engine.get_entangled(universe_id)
            results = []
            for partner_id in partners:
                insights = memory.get_by_universe(partner_id)
                results.extend(insights[-3:])
            return results

        def quantum_observe() -> dict:
            """Get the current superposition snapshot."""
            embeddings = memory.get_latest_embeddings()
            universe_ids = list(embeddings.keys())
            return {
                "universes": {
                    uid: {"insights": memory.get_by_universe(uid)}
                    for uid in universe_ids
                },
                "entanglements": [
                    {"pair": list(pair), "similarity": round(sim, 4)}
                    for pair, sim in engine.active_entanglements.items()
                ],
                "superposition": "active",
            }

        def quantum_crystallize(universe_id: str) -> dict:
            """Extract this Universe's current state as a standalone result. Other Universes keep running."""
            insights = memory.get_by_universe(universe_id)
            entanglements = [
                list(pair)
                for pair in engine.active_entanglements
                if universe_id in pair
            ]
            return {
                "universe_id": universe_id,
                "insights": insights,
                "entanglements": entanglements,
                "crystallized_at": datetime.now(timezone.utc).isoformat(),
            }

        # Register with MCP and store locally for testing
        self._tools = {
            "quantum_write": quantum_write,
            "quantum_read_entangled": quantum_read_entangled,
            "quantum_observe": quantum_observe,
            "quantum_crystallize": quantum_crystallize,
        }
        for name, fn in self._tools.items():
            self.mcp.tool()(fn)

    def call_tool(self, name: str, args: dict):
        """Synchronous tool invocation for testing."""
        return self._tools[name](**args)


def create_server(memory: QuantumMemory, engine: ResonanceEngine) -> CosmosServer:
    return CosmosServer(memory=memory, engine=engine)


def run_server(persist_path: str = ".quantum") -> None:
    """Run the MCP server in stdio mode (called by Claude Code)."""
    memory = QuantumMemory(persist_path=persist_path)
    engine = ResonanceEngine(quantum_memory=memory)
    server = create_server(memory=memory, engine=engine)
    server.mcp.run(transport="stdio")
