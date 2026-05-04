"""
ufo_windows_qa_mcp_server.py

Stdio MCP server that exposes UFO's real Windows automation tools to Claude Code.

Composes UFO's UICollector, HostUIExecutor, AppUIExecutor into ONE server
via FastMCP.mount(). No mocks, no re-implementation.

Requires: UFO installed (pip install from repo), fastmcp, pydantic
"""

from __future__ import annotations

import time
from typing import Annotated, Any, Dict, List, Optional

from fastmcp import FastMCP
from pydantic import Field

from ufo.client.mcp.mcp_registry import MCPRegistry
from ufo.client.mcp.local_servers import load_all_servers


def _get_ufo_server(namespace: str) -> FastMCP:
    """Load all UFO servers, then fetch by namespace."""
    load_all_servers()
    if not MCPRegistry.is_registered(namespace):
        raise RuntimeError(
            f"UFO MCP server '{namespace}' not registered. "
            f"Available: {MCPRegistry.list()}"
        )
    return MCPRegistry.get(namespace)


# Compose into one server
mcp = FastMCP("UFO Windows QA (UIA/Win32)")

mcp.mount(_get_ufo_server("UICollector"))
mcp.mount(_get_ufo_server("HostUIExecutor"))
mcp.mount(_get_ufo_server("AppUIExecutor"))


# QA helper tools (thin wrappers around UFO tools)

@mcp.tool()
def qa_refresh_and_list_windows(
    remove_empty: Annotated[bool, Field(description="Drop empty/ghost windows.")] = True
) -> Annotated[List[Dict[str, Any]], Field(description="Window list.")]:
    """Refresh + list windows in one call. Wraps UICollector.get_desktop_app_info."""
    return mcp.call_tool_sync(
        "get_desktop_app_info",
        {"remove_empty": remove_empty, "refresh_app_windows": True},
    )


@mcp.tool()
def qa_refresh_controls(
    field_list: Annotated[List[str], Field(description="Fields to fetch per control.")],
) -> Annotated[List[Dict[str, Any]], Field(description="Controls for selected window.")]:
    """Refresh control map for the selected window. Wraps UICollector.get_app_window_controls_info."""
    return mcp.call_tool_sync(
        "get_app_window_controls_info", {"field_list": field_list}
    )


@mcp.tool()
def qa_wait_for_text_contains(
    id: Annotated[str, Field(description="Control id.")],
    name: Annotated[str, Field(description="Control name.")],
    expected_substring: Annotated[str, Field(description="Substring that must appear.")],
    timeout_s: Annotated[float, Field(description="Max wait seconds.")] = 10.0,
    poll_s: Annotated[float, Field(description="Poll interval seconds.")] = 0.5,
) -> Annotated[Dict[str, Any], Field(description="Result with ok flag and observed text.")]:
    """Poll texts(id,name) until expected_substring appears or timeout. Avoids arbitrary sleeps."""
    deadline = time.time() + max(0.1, timeout_s)
    last_text: Optional[str] = None

    while time.time() < deadline:
        res = mcp.call_tool_sync("texts", {"id": id, "name": name})
        last_text = res if isinstance(res, str) else str(res)
        if expected_substring in last_text:
            return {"ok": True, "text": last_text, "matched": expected_substring}
        time.sleep(max(0.05, poll_s))

    return {
        "ok": False,
        "text": last_text,
        "matched": expected_substring,
        "timeout_s": timeout_s,
    }


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
