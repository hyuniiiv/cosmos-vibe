import json
from pathlib import Path


HOOKS_BLOCK = {
    "PostToolUse": [
        {
            "matcher": ".*",
            "hooks": [{"type": "command", "command": "cosmos-hook-extract"}]
        }
    ],
    "UserPromptSubmit": [
        {
            "hooks": [{"type": "command", "command": "cosmos-hook-inject"}]
        }
    ]
}

MCP_BLOCK = {
    "cosmos-vibe": {
        "command": "python",
        "args": ["-m", "cosmos_vibe.mcp.server"],
        "env": {}
    }
}


def install(project_root: Path = Path(".")) -> None:
    settings_path = project_root / ".claude" / "settings.json"
    settings_path.parent.mkdir(parents=True, exist_ok=True)

    if settings_path.exists():
        with open(settings_path) as f:
            settings = json.load(f)
    else:
        settings = {}

    settings.setdefault("hooks", {}).update(HOOKS_BLOCK)
    settings.setdefault("mcpServers", {}).update(MCP_BLOCK)

    with open(settings_path, "w") as f:
        json.dump(settings, f, indent=2, ensure_ascii=False)

    print(f"✅ Cosmos Vibe installed → {settings_path}")
    print("   Hooks: PostToolUse (extract), UserPromptSubmit (inject)")
    print("   MCP: cosmos-vibe server registered")


def uninstall(project_root: Path = Path(".")) -> None:
    settings_path = project_root / ".claude" / "settings.json"
    if not settings_path.exists():
        print("Nothing to uninstall.")
        return

    with open(settings_path) as f:
        settings = json.load(f)

    settings.get("hooks", {}).pop("PostToolUse", None)
    settings.get("hooks", {}).pop("UserPromptSubmit", None)
    settings.get("mcpServers", {}).pop("cosmos-vibe", None)

    with open(settings_path, "w") as f:
        json.dump(settings, f, indent=2, ensure_ascii=False)

    print(f"✅ Cosmos Vibe uninstalled from {settings_path}")
