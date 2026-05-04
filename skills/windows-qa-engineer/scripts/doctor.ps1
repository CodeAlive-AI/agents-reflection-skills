Write-Host "== Windows QA + UFO Doctor ==" -ForegroundColor Cyan

python -c "import platform; print('Platform:', platform.platform())"
python -c "import ufo; print('UFO import OK')"
python -c "from ufo.client.mcp.local_servers import load_all_servers; load_all_servers(); print('UFO local servers loaded OK')"
python -c "from ufo.client.mcp.mcp_registry import MCPRegistry; print('Registered:', MCPRegistry.list())"

Write-Host ""
Write-Host "If you see UICollector/HostUIExecutor/AppUIExecutor registered, you're good." -ForegroundColor Green
