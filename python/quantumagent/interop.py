"""Layer 1 ↔ Layer 3 interop — read .quantum/ cosmos output into Python.

The CLI/DSL layers (v1.x/v2.x) write JSONL insight files to ``.quantum/<name>/``.
This module reads those files and exposes them as a Python ``Wavefunction``
over the strategies (cosmos names), with the insights themselves available
as metadata.

Once cosmos has run, you can do statistical analysis or compose with other
Python primitives without re-running the agents.

Example::

    # 1) From the shell: /cosmos spawn --goal "..." --strategies "a,b,c"
    # 2) Wait for completion.
    # 3) In Python:
    from quantumagent import from_cosmos, observe

    cosmos = from_cosmos(".")
    print(cosmos.psi)               # Wavefunction over ["alpha", "beta", "gamma"]
    print(cosmos.insights["alpha"]) # list of insight dicts for alpha
    print(cosmos.resonance)         # list of decisions that appeared across cosmos
    print(cosmos.uncertainty)       # list of decisions where they diverged
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from typing import Dict, List, Optional

from .core import Wavefunction


@dataclass
class CosmosRun:
    """A snapshot of a cosmos run read from disk — all four scales.

    Attributes:
        names: cosmos names (e.g., ["alpha", "beta", "gamma"])
        psi: classical-mode Wavefunction over the cosmos names. Weights
            proportional to insight count (the cosmos with more recorded
            findings gets more probability mass). For a uniform-weight
            wavefunction, pass ``weights="uniform"`` to ``from_cosmos``.
        insights: ``{name: list-of-insight-dicts}``. Each insight is a parsed
            JSON object from the JSONL line.
        resonance: list of finding-summaries that appeared across cosmos
            (parsed heuristically from insight content via lowercase token
            overlap). For high-quality Resonance analysis, prefer running
            ``/cosmos observe`` which uses Claude's semantic judgment.
        uncertainty: list of finding-summaries that appeared in some cosmos
            but not others.
        spin: project spin dict if ``.quantum/project/spin.json`` exists.
        singularities: list of singularity events if present.
        code_findings: list of code-level quantum findings (v4.0+) from
            ``.quantum/code/findings.jsonl``. Each entry is a parsed JSON
            dict with at least ``type`` (one of ``code-tunnel``,
            ``code-decoherence``, ``code-superposition``, ``code-jump``).
    """

    names: List[str]
    psi: Wavefunction
    insights: Dict[str, List[dict]] = field(default_factory=dict)
    resonance: List[str] = field(default_factory=list)
    uncertainty: List[str] = field(default_factory=list)
    spin: Optional[dict] = None
    singularities: List[dict] = field(default_factory=list)
    code_findings: List[dict] = field(default_factory=list)

    def code_summary(self) -> Dict[str, int]:
        """Count code-scale findings by type. Returns dict like
        ``{"code-tunnel": 12, "code-decoherence": 5, ...}``."""
        out: Dict[str, int] = {}
        for f in self.code_findings:
            t = f.get("type", "unknown")
            out[t] = out.get(t, 0) + 1
        return out

    def __repr__(self) -> str:
        bits = [f"<CosmosRun {len(self.names)} cosmos: {', '.join(self.names)}"]
        if self.spin:
            bits.append(f"spin={self.spin.get('name', '?')}")
        if self.singularities:
            bits.append(f"singularities={len(self.singularities)}")
        bits.append(f"resonance={len(self.resonance)}")
        bits.append(f"uncertainty={len(self.uncertainty)}")
        if self.code_findings:
            bits.append(f"code-findings={len(self.code_findings)}")
        return " | ".join(bits) + ">"


def from_cosmos(
    repo_path: str = ".",
    *,
    weights: str = "by-insight-count",
) -> CosmosRun:
    """Read the .quantum/ directory of a cosmos run into a Python CosmosRun.

    Args:
        repo_path: path to the repository root (where ``.quantum/`` lives)
        weights: how to weight the resulting wavefunction:
            - ``"by-insight-count"`` *(default)*: cosmos with more insights
              get higher weight. Reflects how engaged each strategy was.
            - ``"uniform"``: equal weight across all cosmos. Neutral prior.

    Returns:
        A ``CosmosRun`` dataclass with ``psi`` (Wavefunction), ``insights``,
        ``resonance``, ``uncertainty``, and macro-layer state.

    Raises:
        FileNotFoundError: if ``.quantum/`` does not exist or contains no
            ``<name>/insights.jsonl`` files.
        ValueError: if ``weights`` is not a recognized mode.
    """
    quantum_dir = os.path.join(repo_path, ".quantum")
    if not os.path.isdir(quantum_dir):
        raise FileNotFoundError(
            f"No .quantum/ directory at {repo_path!r}. "
            f"Run /cosmos spawn first, or pass a repo_path that has one."
        )

    # Find cosmos namespaces
    names: List[str] = []
    insights: Dict[str, List[dict]] = {}
    for entry in sorted(os.listdir(quantum_dir)):
        candidate = os.path.join(quantum_dir, entry, "insights.jsonl")
        if entry in ("project", "singularities"):
            continue
        if not os.path.isfile(candidate):
            continue
        items = _read_jsonl(candidate)
        names.append(entry)
        insights[entry] = items

    if not names:
        raise FileNotFoundError(
            f".quantum/ at {repo_path!r} contains no cosmos insight files."
        )

    # Compute weights
    if weights == "by-insight-count":
        counts = [max(1, len(insights[n])) for n in names]
        w = counts
    elif weights == "uniform":
        w = [1.0] * len(names)
    else:
        raise ValueError(
            f"Unknown weights mode: {weights!r}. Use 'by-insight-count' or 'uniform'."
        )

    psi = Wavefunction(states=names, weights=w, name="cosmos-run")

    # Read macro layer
    spin = None
    spin_path = os.path.join(quantum_dir, "project", "spin.json")
    if os.path.isfile(spin_path):
        with open(spin_path, "r", encoding="utf-8") as f:
            try:
                spin = json.load(f)
            except json.JSONDecodeError:
                spin = None

    singularities: List[dict] = []
    sing_path = os.path.join(quantum_dir, "singularities", "events.jsonl")
    if os.path.isfile(sing_path):
        singularities = _read_jsonl(sing_path)

    # Code-scale findings (v4.0+)
    code_findings: List[dict] = []
    code_path = os.path.join(quantum_dir, "code", "findings.jsonl")
    if os.path.isfile(code_path):
        code_findings = _read_jsonl(code_path)

    # Heuristic resonance/uncertainty (token overlap)
    resonance, uncertainty = _compute_overlap_signals(names, insights)

    return CosmosRun(
        names=names,
        psi=psi,
        insights=insights,
        resonance=resonance,
        uncertainty=uncertainty,
        spin=spin,
        singularities=singularities,
        code_findings=code_findings,
    )


def _read_jsonl(path: str) -> List[dict]:
    """Read a JSONL file into a list of dicts. Skip malformed lines."""
    out: List[dict] = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                out.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return out


def _compute_overlap_signals(
    names: List[str], insights: Dict[str, List[dict]]
) -> tuple[List[str], List[str]]:
    """Heuristic resonance/uncertainty detection via lowercase token overlap.

    This is intentionally crude. For semantic-quality analysis, use
    ``/cosmos observe`` (which delegates to Claude's judgment) instead.
    The Python heuristic is a *cheap* signal — useful when you want a
    quick statistical view without an LLM call.
    """
    # Extract significant tokens (length ≥ 4) from each cosmos's content
    tokens_per_cosmos: Dict[str, set] = {}
    for name in names:
        toks: set = set()
        for it in insights[name]:
            content = it.get("content", "")
            if not isinstance(content, str):
                continue
            for word in content.lower().split():
                w = word.strip(".,;:()[]{}\"'!?")
                if len(w) >= 5 and not w.isdigit():
                    toks.add(w)
        tokens_per_cosmos[name] = toks

    # Resonance: tokens present in ≥ ceil(N/2)+1 cosmos
    if not names:
        return [], []
    all_tokens: set = set().union(*tokens_per_cosmos.values()) if tokens_per_cosmos else set()
    threshold = (len(names) // 2) + 1
    resonance_tokens: List[str] = []
    uncertain_tokens: List[str] = []
    for tok in sorted(all_tokens):
        count = sum(1 for name in names if tok in tokens_per_cosmos[name])
        if count >= threshold and count == len(names):
            resonance_tokens.append(f"{tok} ({count}/{len(names)})")
        elif count == 1:
            uncertain_tokens.append(f"{tok} (1/{len(names)})")

    # Return top-30 of each to keep output digestible
    return resonance_tokens[:30], uncertain_tokens[:30]
