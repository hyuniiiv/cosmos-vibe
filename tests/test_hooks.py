import json
import pytest
from unittest.mock import patch, MagicMock
from cosmos_vibe.adapters.claude_code.hooks import extract_hook, inject_hook


def test_extract_hook_writes_insight_for_write_tool():
    hook_input = {
        "tool_name": "Write",
        "tool_input": {"file_path": "auth.py"},
        "tool_response": {"type": "result", "result": "File written successfully"},
        "session_id": "test-session",
    }
    env = {"COSMOS_UNIVERSE_ID": "alpha", "COSMOS_MCP_PATH": ".quantum"}

    with patch("cosmos_vibe.adapters.claude_code.hooks.QuantumMemory") as MockMemory:
        instance = MockMemory.return_value
        extract_hook(hook_input=hook_input, env=env)
        instance.write.assert_called_once()
        call_args = instance.write.call_args
        assert call_args[0][0] == "alpha"
        assert "auth.py" in call_args[0][1] or "Write" in call_args[0][1]


def test_extract_hook_skips_read_tool():
    hook_input = {
        "tool_name": "Read",
        "tool_input": {"file_path": "auth.py"},
        "tool_response": {"type": "result", "result": "file content"},
        "session_id": "test-session",
    }
    env = {"COSMOS_UNIVERSE_ID": "alpha", "COSMOS_MCP_PATH": ".quantum"}

    with patch("cosmos_vibe.adapters.claude_code.hooks.QuantumMemory") as MockMemory:
        extract_hook(hook_input=hook_input, env=env)
        MockMemory.return_value.write.assert_not_called()


def test_inject_hook_prepends_entangled_context():
    prompt_input = {"prompt": "다음 단계를 진행해줘"}
    env = {"COSMOS_UNIVERSE_ID": "alpha", "COSMOS_MCP_PATH": ".quantum"}

    mock_insights = [
        {"universe_id": "gamma", "content": "OAuth2 refresh_token 패턴 발견"}
    ]

    with patch("cosmos_vibe.adapters.claude_code.hooks.QuantumMemory") as MockMemory:
        with patch("cosmos_vibe.adapters.claude_code.hooks.ResonanceEngine") as MockEngine:
            MockEngine.return_value.get_entangled.return_value = ["gamma"]
            MockMemory.return_value.get_by_universe.return_value = mock_insights

            result = inject_hook(prompt_input=prompt_input, env=env)

    assert "[ENTANGLED CONTEXT]" in result["prompt"]
    assert "OAuth2 refresh_token 패턴 발견" in result["prompt"]
    assert "다음 단계를 진행해줘" in result["prompt"]


def test_inject_hook_returns_unchanged_when_no_entanglement():
    prompt_input = {"prompt": "계속 진행해줘"}
    env = {"COSMOS_UNIVERSE_ID": "alpha", "COSMOS_MCP_PATH": ".quantum"}

    with patch("cosmos_vibe.adapters.claude_code.hooks.QuantumMemory") as MockMemory:
        with patch("cosmos_vibe.adapters.claude_code.hooks.ResonanceEngine") as MockEngine:
            MockEngine.return_value.get_entangled.return_value = []

            result = inject_hook(prompt_input=prompt_input, env=env)

    assert result["prompt"] == "계속 진행해줘"
