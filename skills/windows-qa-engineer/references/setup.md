# Setup: UFO + MCP Server

## Table of Contents
- [Install UFO](#install-ufo)
- [Configure MCP in Claude Code](#configure-mcp-in-claude-code)
- [Verify](#verify)
- [Backend Selection](#backend-selection)

## Install UFO

Prerequisites: Windows 11, Python 3.10+ (3.11 recommended), Git.

```powershell
cd $env:USERPROFILE
git clone https://github.com/microsoft/UFO.git
cd UFO
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Quick check:
```powershell
python -c "from ufo.client.mcp.local_servers import load_all_servers; load_all_servers(); print('OK')"
python -c "from ufo.client.mcp.mcp_registry import MCPRegistry; print(MCPRegistry.list())"
```

Expected: UICollector, HostUIExecutor, AppUIExecutor registered.

## Configure MCP in Claude Code

Add to your project `.mcp.json`:

```json
{
  "mcpServers": {
    "ufo-windows-qa": {
      "type": "stdio",
      "command": "python",
      "args": [
        ".claude/skills/windows-qa-engineer/scripts/ufo_windows_qa_mcp_server.py"
      ],
      "env": {
        "CONTROL_BACKEND": "uia",
        "MAXIMIZE_WINDOW": "false",
        "SHOW_VISUAL_OUTLINE_ON_SCREEN": "true",
        "RUN_CONFIGS": "true"
      }
    }
  }
}
```

Restart Claude Code, then run `/mcp` to confirm tools are available.

## Verify

Run the doctor script:
```powershell
.\.claude\skills\windows-qa-engineer\scripts\doctor.ps1
```

Or check in Claude Code that these tools appear:
`get_desktop_app_info`, `select_application_window`, `get_app_window_controls_info`,
`click_input`, `set_edit_text`, `texts`, `capture_window_screenshot`,
`qa_refresh_and_list_windows`, `qa_refresh_controls`, `qa_wait_for_text_contains`.

## Backend Selection

- `CONTROL_BACKEND=uia` (default, recommended for WinForms/WPF stability)
- `CONTROL_BACKEND=win32` (fallback if UIA fails for a specific SUT)

Set via the `env` block in `.mcp.json`.
