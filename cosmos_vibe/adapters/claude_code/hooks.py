import os
import sys
import json
from cosmos_vibe.core.quantum_memory import QuantumMemory
from cosmos_vibe.core.resonance import ResonanceEngine

_WRITE_TOOLS = {"Write", "Edit", "Bash", "PowerShell"}


def extract_hook(hook_input: dict, env: dict | None = None) -> None:
    env = env or os.environ
    universe_id = env.get("COSMOS_UNIVERSE_ID")
    persist_path = env.get("COSMOS_MCP_PATH", ".quantum")

    if not universe_id:
        return

    tool_name = hook_input.get("tool_name", "")
    if tool_name not in _WRITE_TOOLS:
        return

    tool_input = hook_input.get("tool_input", {})
    tool_response = hook_input.get("tool_response", {})

    content = f"[{tool_name}] {json.dumps(tool_input, ensure_ascii=False)}"
    if isinstance(tool_response, dict) and tool_response.get("result"):
        content += f" → {str(tool_response['result'])[:200]}"

    memory = QuantumMemory(persist_path=persist_path)
    memory.write(universe_id, content)


def inject_hook(prompt_input: dict, env: dict | None = None) -> dict:
    env = env or os.environ
    universe_id = env.get("COSMOS_UNIVERSE_ID")
    persist_path = env.get("COSMOS_MCP_PATH", ".quantum")

    if not universe_id:
        return prompt_input

    memory = QuantumMemory(persist_path=persist_path)
    engine = ResonanceEngine(quantum_memory=memory)
    engine.check_resonance()

    partners = engine.get_entangled(universe_id)
    if not partners:
        return prompt_input

    context_lines = []
    for partner_id in partners:
        insights = memory.get_by_universe(partner_id)
        recent = insights[-3:]
        for insight in recent:
            context_lines.append(f"  [{partner_id}] {insight['content']}")

    if not context_lines:
        return prompt_input

    injected = (
        "[ENTANGLED CONTEXT] — 얽힌 Universe의 최신 인사이트\n"
        + "\n".join(context_lines)
        + "\n[END ENTANGLED CONTEXT]\n\n"
        + prompt_input["prompt"]
    )
    return {**prompt_input, "prompt": injected}


def main_extract() -> None:
    data = json.load(sys.stdin)
    extract_hook(hook_input=data)


def main_inject() -> None:
    data = json.load(sys.stdin)
    result = inject_hook(prompt_input=data)
    print(json.dumps(result, ensure_ascii=False))
