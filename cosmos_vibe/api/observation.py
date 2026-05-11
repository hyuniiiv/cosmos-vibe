from datetime import datetime, timezone
from fastapi import FastAPI, HTTPException, WebSocket
from cosmos_vibe.core.quantum_memory import QuantumMemory
from cosmos_vibe.core.resonance import ResonanceEngine


def create_app(memory: QuantumMemory, engine: ResonanceEngine) -> FastAPI:
    app = FastAPI(title="Cosmos Vibe Observation API")

    @app.get("/observe")
    def observe() -> dict:
        embeddings = memory.get_latest_embeddings()
        return {
            "universes": {
                uid: {"insights": memory.get_by_universe(uid)}
                for uid in embeddings
            },
            "entanglements": [
                {"pair": list(pair), "similarity": round(sim, 4)}
                for pair, sim in engine.active_entanglements.items()
            ],
            "superposition": "active",
        }

    @app.get("/universes/{universe_id}")
    def get_universe(universe_id: str) -> dict:
        insights = memory.get_by_universe(universe_id)
        if not insights and universe_id not in memory.get_latest_embeddings():
            raise HTTPException(status_code=404, detail=f"Universe '{universe_id}' not found")
        return {"universe_id": universe_id, "insights": insights}

    @app.get("/entanglements")
    def get_entanglements() -> list:
        return [
            {"pair": list(pair), "similarity": round(sim, 4)}
            for pair, sim in engine.active_entanglements.items()
        ]

    @app.post("/crystallize/{universe_id}")
    def crystallize(universe_id: str) -> dict:
        insights = memory.get_by_universe(universe_id)
        return {
            "universe_id": universe_id,
            "insights": insights,
            "entanglements": [
                list(pair)
                for pair in engine.active_entanglements
                if universe_id in pair
            ],
            "crystallized_at": datetime.now(timezone.utc).isoformat(),
        }

    @app.websocket("/stream")
    async def stream(websocket: WebSocket) -> None:
        await websocket.accept()
        import asyncio, json
        try:
            while True:
                engine.check_resonance()
                snapshot = {
                    "universes": list(memory.get_latest_embeddings().keys()),
                    "entanglements": [list(p) for p in engine.active_entanglements],
                }
                await websocket.send_text(json.dumps(snapshot))
                await asyncio.sleep(2)
        except Exception:
            pass

    return app
