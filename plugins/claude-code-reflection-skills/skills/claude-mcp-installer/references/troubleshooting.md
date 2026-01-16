# MCP Troubleshooting

## Check Server Status

```bash
# In Claude Code
/mcp

# CLI commands
claude mcp list
claude mcp get <server-name>
```

## Common Issues

### "Options must come before server name"

**Wrong:**
```bash
claude mcp add my-server --transport http https://example.com
```

**Correct:**
```bash
claude mcp add --transport http my-server https://example.com
```

### Server Not Connecting

1. **Check URL is correct** - Must be full URL with protocol
2. **Verify credentials** - Run `/mcp` to re-authenticate
3. **Check timeout** - Increase with `MCP_TIMEOUT=30000 claude`

### Stdio Server Fails to Start

1. **Verify command exists:**
   ```bash
   which npx
   npx -y @package/name --help
   ```

2. **Check environment variables are set:**
   ```bash
   echo $API_KEY
   ```

3. **Windows users** - Use `cmd /c` wrapper:
   ```bash
   claude mcp add --transport stdio my-server -- cmd /c npx -y @some/package
   ```

### Output Truncated

MCP output is limited to 25,000 tokens by default. Increase with:

```bash
export MAX_MCP_OUTPUT_TOKENS=50000
claude
```

Warning threshold is at 10,000 tokens.

### OAuth Authentication Issues

1. Run `/mcp` in Claude Code
2. Follow browser login prompts
3. Tokens are stored and refreshed automatically

If issues persist, remove and re-add the server:
```bash
claude mcp remove github
claude mcp add --transport http github https://api.githubcopilot.com/mcp/
```

### Environment Variable Not Expanding

**Check syntax:**
- `${VAR}` - Expands to value
- `${VAR:-default}` - Uses default if not set

**Verify variable is set:**
```bash
echo $MY_API_KEY
```

**In .mcp.json:**
```json
{
  "env": {
    "API_KEY": "${MY_API_KEY}"
  }
}
```

## Key Environment Variables

| Variable | Purpose | Default |
|----------|---------|---------|
| `MCP_TIMEOUT` | Server startup timeout (ms) | 10000 |
| `MAX_MCP_OUTPUT_TOKENS` | Maximum output tokens | 25000 |
| `CLAUDE_PLUGIN_ROOT` | Plugin path expansion | - |

## Security Notes

- Third-party MCP servers are not verified by Anthropic
- Be cautious with servers that fetch untrusted content (prompt injection risk)
- Use local scope for sensitive credentials
- Review project-scoped servers before enabling

## Resources

- MCP Server Directory: https://github.com/modelcontextprotocol/servers
- Build Custom Servers: https://modelcontextprotocol.io/quickstart/server
