#!/usr/bin/env python3
"""Shared agent definitions for multi-agent skill management.

Based on the Skills CLI registry (https://skills.sh, https://github.com/vercel-labs/add-skill).
Supports 42 AI coding agents with their skill directory configurations.
"""

from pathlib import Path
from typing import TypedDict


class AgentConfig(TypedDict):
    """Configuration for an AI coding agent."""
    name: str
    display_name: str
    project_dir: str      # Relative path for project-level skills
    global_dir: str       # Path for user-level skills (supports ~)
    detect_paths: list[str]  # Paths to check for agent installation


# All supported AI coding agents
AGENTS: dict[str, AgentConfig] = {
    "adal": {
        "name": "adal",
        "display_name": "AdaL",
        "project_dir": ".adal/skills",
        "global_dir": "~/.adal/skills",
        "detect_paths": ["~/.adal"],
    },
    "amp": {
        "name": "amp",
        "display_name": "Amp",
        "project_dir": ".agents/skills",
        "global_dir": "~/.config/agents/skills",
        "detect_paths": ["~/.config/amp"],
    },
    "antigravity": {
        "name": "antigravity",
        "display_name": "Antigravity",
        "project_dir": ".agent/skills",
        "global_dir": "~/.gemini/antigravity/skills",
        "detect_paths": ["~/.gemini/antigravity"],
    },
    "augment": {
        "name": "augment",
        "display_name": "Augment",
        "project_dir": ".augment/skills",
        "global_dir": "~/.augment/skills",
        "detect_paths": ["~/.augment"],
    },
    "claude-code": {
        "name": "claude-code",
        "display_name": "Claude Code",
        "project_dir": ".claude/skills",
        "global_dir": "~/.claude/skills",
        "detect_paths": ["~/.claude"],
    },
    "cline": {
        "name": "cline",
        "display_name": "Cline",
        "project_dir": ".cline/skills",
        "global_dir": "~/.cline/skills",
        "detect_paths": ["~/.cline"],
    },
    "codebuddy": {
        "name": "codebuddy",
        "display_name": "CodeBuddy",
        "project_dir": ".codebuddy/skills",
        "global_dir": "~/.codebuddy/skills",
        "detect_paths": ["~/.codebuddy"],
    },
    "codex": {
        "name": "codex",
        "display_name": "Codex",
        "project_dir": ".agents/skills",
        "global_dir": "~/.codex/skills",
        "detect_paths": ["~/.codex"],
    },
    "command-code": {
        "name": "command-code",
        "display_name": "Command Code",
        "project_dir": ".commandcode/skills",
        "global_dir": "~/.commandcode/skills",
        "detect_paths": ["~/.commandcode"],
    },
    "continue": {
        "name": "continue",
        "display_name": "Continue",
        "project_dir": ".continue/skills",
        "global_dir": "~/.continue/skills",
        "detect_paths": ["~/.continue"],
    },
    "crush": {
        "name": "crush",
        "display_name": "Crush",
        "project_dir": ".crush/skills",
        "global_dir": "~/.config/crush/skills",
        "detect_paths": ["~/.config/crush"],
    },
    "cursor": {
        "name": "cursor",
        "display_name": "Cursor",
        "project_dir": ".cursor/skills",
        "global_dir": "~/.cursor/skills",
        "detect_paths": ["~/.cursor"],
    },
    "droid": {
        "name": "droid",
        "display_name": "Droid",
        "project_dir": ".factory/skills",
        "global_dir": "~/.factory/skills",
        "detect_paths": ["~/.factory/skills"],
    },
    "gemini-cli": {
        "name": "gemini-cli",
        "display_name": "Gemini CLI",
        "project_dir": ".agents/skills",
        "global_dir": "~/.gemini/skills",
        "detect_paths": ["~/.gemini"],
    },
    "github-copilot": {
        "name": "github-copilot",
        "display_name": "GitHub Copilot",
        "project_dir": ".agents/skills",
        "global_dir": "~/.copilot/skills",
        "detect_paths": ["~/.copilot"],
    },
    "goose": {
        "name": "goose",
        "display_name": "Goose",
        "project_dir": ".goose/skills",
        "global_dir": "~/.config/goose/skills",
        "detect_paths": ["~/.config/goose"],
    },
    "iflow-cli": {
        "name": "iflow-cli",
        "display_name": "iFlow CLI",
        "project_dir": ".iflow/skills",
        "global_dir": "~/.iflow/skills",
        "detect_paths": ["~/.iflow"],
    },
    "junie": {
        "name": "junie",
        "display_name": "Junie",
        "project_dir": ".junie/skills",
        "global_dir": "~/.junie/skills",
        "detect_paths": ["~/.junie"],
    },
    "kilo": {
        "name": "kilo",
        "display_name": "Kilo Code",
        "project_dir": ".kilocode/skills",
        "global_dir": "~/.kilocode/skills",
        "detect_paths": ["~/.kilocode"],
    },
    "kimi-cli": {
        "name": "kimi-cli",
        "display_name": "Kimi Code CLI",
        "project_dir": ".agents/skills",
        "global_dir": "~/.config/agents/skills",
        "detect_paths": ["~/.config/kimi"],
    },
    "kiro-cli": {
        "name": "kiro-cli",
        "display_name": "Kiro CLI",
        "project_dir": ".kiro/skills",
        "global_dir": "~/.kiro/skills",
        "detect_paths": ["~/.kiro"],
    },
    "kode": {
        "name": "kode",
        "display_name": "Kode",
        "project_dir": ".kode/skills",
        "global_dir": "~/.kode/skills",
        "detect_paths": ["~/.kode"],
    },
    "mcpjam": {
        "name": "mcpjam",
        "display_name": "MCPJam",
        "project_dir": ".mcpjam/skills",
        "global_dir": "~/.mcpjam/skills",
        "detect_paths": ["~/.mcpjam"],
    },
    "mistral-vibe": {
        "name": "mistral-vibe",
        "display_name": "Mistral Vibe",
        "project_dir": ".vibe/skills",
        "global_dir": "~/.vibe/skills",
        "detect_paths": ["~/.vibe"],
    },
    "mux": {
        "name": "mux",
        "display_name": "Mux",
        "project_dir": ".mux/skills",
        "global_dir": "~/.mux/skills",
        "detect_paths": ["~/.mux"],
    },
    "neovate": {
        "name": "neovate",
        "display_name": "Neovate",
        "project_dir": ".neovate/skills",
        "global_dir": "~/.neovate/skills",
        "detect_paths": ["~/.neovate"],
    },
    "openclaw": {
        "name": "openclaw",
        "display_name": "OpenClaw",
        "project_dir": "skills",
        "global_dir": "~/.openclaw/skills",
        "detect_paths": ["~/.openclaw", "~/.clawdbot"],
    },
    "opencode": {
        "name": "opencode",
        "display_name": "OpenCode",
        "project_dir": ".agents/skills",
        "global_dir": "~/.config/opencode/skills",
        "detect_paths": ["~/.config/opencode"],
    },
    "openhands": {
        "name": "openhands",
        "display_name": "OpenHands",
        "project_dir": ".openhands/skills",
        "global_dir": "~/.openhands/skills",
        "detect_paths": ["~/.openhands"],
    },
    "pi": {
        "name": "pi",
        "display_name": "Pi",
        "project_dir": ".pi/skills",
        "global_dir": "~/.pi/agent/skills",
        "detect_paths": ["~/.pi"],
    },
    "pochi": {
        "name": "pochi",
        "display_name": "Pochi",
        "project_dir": ".pochi/skills",
        "global_dir": "~/.pochi/skills",
        "detect_paths": ["~/.pochi"],
    },
    "qoder": {
        "name": "qoder",
        "display_name": "Qoder",
        "project_dir": ".qoder/skills",
        "global_dir": "~/.qoder/skills",
        "detect_paths": ["~/.qoder"],
    },
    "qwen-code": {
        "name": "qwen-code",
        "display_name": "Qwen Code",
        "project_dir": ".qwen/skills",
        "global_dir": "~/.qwen/skills",
        "detect_paths": ["~/.qwen"],
    },
    "replit": {
        "name": "replit",
        "display_name": "Replit",
        "project_dir": ".agents/skills",
        "global_dir": "~/.config/agents/skills",
        "detect_paths": ["~/.replit"],
    },
    "roo": {
        "name": "roo",
        "display_name": "Roo Code",
        "project_dir": ".roo/skills",
        "global_dir": "~/.roo/skills",
        "detect_paths": ["~/.roo"],
    },
    "trae": {
        "name": "trae",
        "display_name": "Trae",
        "project_dir": ".trae/skills",
        "global_dir": "~/.trae/skills",
        "detect_paths": ["~/.trae"],
    },
    "trae-cn": {
        "name": "trae-cn",
        "display_name": "Trae CN",
        "project_dir": ".trae/skills",
        "global_dir": "~/.trae-cn/skills",
        "detect_paths": ["~/.trae-cn"],
    },
    "windsurf": {
        "name": "windsurf",
        "display_name": "Windsurf",
        "project_dir": ".windsurf/skills",
        "global_dir": "~/.codeium/windsurf/skills",
        "detect_paths": ["~/.codeium/windsurf"],
    },
    "zencoder": {
        "name": "zencoder",
        "display_name": "Zencoder",
        "project_dir": ".zencoder/skills",
        "global_dir": "~/.zencoder/skills",
        "detect_paths": ["~/.zencoder"],
    },
}


def get_agent_config(agent: str) -> AgentConfig | None:
    """Get configuration for an agent by ID.

    Args:
        agent: Agent ID (e.g., "claude-code", "cursor")

    Returns:
        AgentConfig if found, None otherwise
    """
    return AGENTS.get(agent)


def validate_agent(agent: str) -> bool:
    """Check if an agent ID is valid.

    Args:
        agent: Agent ID to validate

    Returns:
        True if valid, False otherwise
    """
    return agent in AGENTS


def list_all_agents() -> list[AgentConfig]:
    """Return all supported agent configurations.

    Returns:
        List of all agent configs
    """
    return list(AGENTS.values())


def get_project_skills_dir(agent: str, cwd: Path | None = None) -> Path | None:
    """Get the project-level skills directory for an agent.

    Args:
        agent: Agent ID
        cwd: Working directory (defaults to current directory)

    Returns:
        Path to project skills directory, or None if agent not found
    """
    config = get_agent_config(agent)
    if not config:
        return None

    base = cwd or Path.cwd()
    return base / config["project_dir"]


def get_global_skills_dir(agent: str) -> Path | None:
    """Get the global (user-level) skills directory for an agent.

    Args:
        agent: Agent ID

    Returns:
        Path to global skills directory, or None if agent not found
    """
    config = get_agent_config(agent)
    if not config:
        return None

    return Path(config["global_dir"]).expanduser()


def detect_installed_agents() -> list[str]:
    """Detect which AI agents are installed on this system.

    Checks for the existence of agent-specific directories.

    Returns:
        List of installed agent IDs
    """
    installed = []

    for agent_id, config in AGENTS.items():
        for detect_path in config["detect_paths"]:
            path = Path(detect_path).expanduser()
            if path.exists():
                installed.append(agent_id)
                break

    return installed


def get_skills_dir(agent: str, scope: str, cwd: Path | None = None) -> Path | None:
    """Get the skills directory for an agent and scope.

    Args:
        agent: Agent ID
        scope: "project" or "global"
        cwd: Working directory for project scope

    Returns:
        Path to skills directory, or None if agent not found
    """
    if scope == "project":
        return get_project_skills_dir(agent, cwd)
    elif scope == "global":
        return get_global_skills_dir(agent)
    return None
