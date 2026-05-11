import asyncio
from dataclasses import dataclass
from typing import AsyncIterator
import numpy as np
from cosmos_vibe.core.quantum_memory import QuantumMemory


@dataclass
class EntanglementEvent:
    type: str  # "formed" | "dissolved"
    pair: tuple[str, str]
    similarity: float


class ResonanceEngine:
    def __init__(
        self,
        quantum_memory: QuantumMemory,
        threshold: float = 0.75,
        dissolve_threshold: float = 0.65,
        interval: float = 2.0,
    ):
        self.qm = quantum_memory
        self.threshold = threshold
        self.dissolve_threshold = dissolve_threshold
        self.interval = interval
        self.active_entanglements: dict[tuple[str, str], float] = {}

    def _cosine_similarity(self, a: list[float], b: list[float]) -> float:
        va, vb = np.array(a), np.array(b)
        denom = np.linalg.norm(va) * np.linalg.norm(vb)
        if denom == 0:
            return 0.0
        return float(np.dot(va, vb) / denom)

    def _canonical_pair(self, a: str, b: str) -> tuple[str, str]:
        return (a, b) if a < b else (b, a)

    def check_resonance(self) -> list[EntanglementEvent]:
        events: list[EntanglementEvent] = []
        embeddings = self.qm.get_latest_embeddings()
        universe_ids = sorted(embeddings.keys())

        for i in range(len(universe_ids)):
            for j in range(i + 1, len(universe_ids)):
                a, b = universe_ids[i], universe_ids[j]
                pair = self._canonical_pair(a, b)
                sim = self._cosine_similarity(
                    embeddings[a]["embedding"],
                    embeddings[b]["embedding"],
                )

                if sim >= self.threshold and pair not in self.active_entanglements:
                    self.active_entanglements[pair] = sim
                    events.append(EntanglementEvent("formed", pair, sim))
                elif sim < self.dissolve_threshold and pair in self.active_entanglements:
                    del self.active_entanglements[pair]
                    events.append(EntanglementEvent("dissolved", pair, sim))

        return events

    def get_entangled(self, universe_id: str) -> list[str]:
        partners = []
        for pair in self.active_entanglements:
            if universe_id in pair:
                partner = pair[1] if pair[0] == universe_id else pair[0]
                partners.append(partner)
        return partners

    async def monitor(self) -> AsyncIterator[EntanglementEvent]:
        while True:
            for event in self.check_resonance():
                yield event
            await asyncio.sleep(self.interval)
