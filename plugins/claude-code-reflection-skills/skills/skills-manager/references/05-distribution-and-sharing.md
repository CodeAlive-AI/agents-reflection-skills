# Chapter 4: Distribution and Sharing

Skills make your MCP integration more complete. As users compare connectors, those with skills offer a faster path to value, giving you an edge over MCP-only alternatives.

## Current distribution model (January 2026)

**How individual users get skills:**
1. Download the skill folder
2. Zip the folder (if needed)
3. Upload to Claude.ai via Settings > Capabilities > Skills
4. Or place in Claude Code skills directory

**Organization-level skills:**
- Admins can deploy skills workspace-wide (shipped December 18, 2025)
- Automatic updates
- Centralized management

## An open standard

We've published Agent Skills as an open standard. Like MCP, we believe skills should be portable across tools and platforms - the same skill should work whether you're using Claude or other AI platforms. That said, some skills are designed to take full advantage of a specific platform's capabilities; authors can note this in the skill's `compatibility` field.

## Using skills via API

For programmatic use cases - such as building applications, agents, or automated workflows that leverage skills - the API provides direct control over skill management and execution.

**Key capabilities:**
- `/v1/skills` endpoint for listing and managing skills
- Add skills to Messages API requests via the `container.skills` parameter
- Version control and management through the Claude Console
- Works with the Claude Agent SDK for building custom agents

**When to use skills via the API vs. Claude.ai:**

| Use Case | Best Surface |
|---|---|
| End users interacting with skills directly | Claude.ai / Claude Code |
| Manual testing and iteration during development | Claude.ai / Claude Code |
| Individual, ad-hoc workflows | Claude.ai / Claude Code |
| Applications using skills programmatically | API |
| Production deployments at scale | API |
| Automated pipelines and agent systems | API |

Note: Skills in the API require the Code Execution Tool beta, which provides the secure environment skills need to run.

## Recommended approach today

Start by hosting your skill on GitHub with a public repo, clear README (for human visitors — this is separate from your skill folder, which should not contain a README.md), and example usage with screenshots.

1. **Host on GitHub**
   - Public repo for open-source skills
   - Clear README with installation instructions
   - Example usage and screenshots

2. **Document in Your MCP Repo**
   - Link to skills from MCP documentation
   - Explain the value of using both together
   - Provide quick-start guide

3. **Create an Installation Guide**

```markdown
# Installing the [Your Service] skill

1. Download the skill:
   - Clone repo: `git clone https://github.com/yourcompany/skills`
   - Or download ZIP from Releases

2. Install in Claude:
   - Open Claude.ai > Settings > Skills
   - Click "Upload skill"
   - Select the skill folder (zipped)

3. Enable the skill:
   - Toggle on the [Your Service] skill
   - Ensure your MCP server is connected

4. Test:
   - Ask Claude: "Set up a new project in [Your Service]"
```

## Positioning your skill

Focus on outcomes, not features:

Good:
```
"The ProjectHub skill enables teams to set up complete project workspaces
in seconds — including pages, databases, and templates — instead of
spending 30 minutes on manual setup."
```

Bad:
```
"The ProjectHub skill is a folder containing YAML frontmatter and Markdown
instructions that calls our MCP server tools."
```

Highlight the MCP + skills story:
```
"Our MCP server gives Claude access to your Linear projects. Our skills
teach Claude your team's sprint planning workflow. Together, they enable
AI-powered project management."
```
