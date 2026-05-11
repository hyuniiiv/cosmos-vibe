from dataclasses import dataclass
import chromadb
from sentence_transformers import SentenceTransformer


@dataclass
class Insight:
    universe_id: str
    content: str
    embedding: list[float]


class QuantumMemory:
    def __init__(self, persist_path: str = ".quantum"):
        self.client = chromadb.PersistentClient(path=persist_path)
        self.collection = self.client.get_or_create_collection(
            name="quantum_memory",
            metadata={"hnsw:space": "cosine"},
        )
        self._model = SentenceTransformer("all-MiniLM-L6-v2")
        self._counters: dict[str, int] = {}

    def write(self, universe_id: str, content: str) -> None:
        count = self._counters.get(universe_id, 0)
        self._counters[universe_id] = count + 1
        embedding = self._model.encode(content).tolist()
        self.collection.add(
            documents=[content],
            embeddings=[embedding],
            metadatas=[{"universe_id": universe_id}],
            ids=[f"{universe_id}_{count}"],
        )

    def get_by_universe(self, universe_id: str) -> list[dict]:
        results = self.collection.get(
            where={"universe_id": universe_id},
            include=["documents", "metadatas"],
        )
        return [
            {"universe_id": universe_id, "content": doc}
            for doc in results["documents"]
        ]

    def get_latest_embeddings(self) -> dict[str, dict]:
        results = self.collection.get(include=["embeddings", "metadatas", "documents"])
        if not results["documents"]:
            return {}
        latest: dict[str, dict] = {}
        for doc, emb, meta in zip(
            results["documents"], results["embeddings"], results["metadatas"]
        ):
            uid = meta["universe_id"]
            latest[uid] = {"embedding": emb, "content": doc}
        return latest
