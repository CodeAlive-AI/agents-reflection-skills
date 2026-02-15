# Chapter 2: Planning and Design

## Start with use cases

Before writing any code, identify 2-3 concrete use cases your skill should enable.

**Good use case definition:**

```
Use Case: Project Sprint Planning
Trigger: User says "help me plan this sprint" or "create sprint tasks"
Steps:
1. Fetch current project status from Linear (via MCP)
2. Analyze team velocity and capacity
3. Suggest task prioritization
4. Create tasks in Linear with proper labels and estimates
Result: Fully planned sprint with tasks created
```

Ask yourself:
- What does a user want to accomplish?
- What multi-step workflows does this require?
- Which tools are needed (built-in or MCP?)
- What domain knowledge or best practices should be embedded?

## Common skill use case categories

At Anthropic, we've observed three common use cases:

### Category 1: Document & Asset Creation

Used for: Creating consistent, high-quality output including documents, presentations, apps, designs, code, etc.

Key techniques:
- Embedded style guides and brand standards
- Template structures for consistent output
- Quality checklists before finalizing
- No external tools required - uses Claude's built-in capabilities

### Category 2: Workflow Automation

Used for: Multi-step processes that benefit from consistent methodology, including coordination across multiple MCP servers.

Key techniques:
- Step-by-step workflow with validation gates
- Templates for common structures
- Built-in review and improvement suggestions
- Iterative refinement loops

### Category 3: MCP Enhancement

Used for: Workflow guidance to enhance the tool access an MCP server provides.

Key techniques:
- Coordinates multiple MCP calls in sequence
- Embeds domain expertise
- Provides context users would otherwise need to specify
- Error handling for common MCP issues

## Define success criteria

How will you know your skill is working?

These are aspirational targets - rough benchmarks rather than precise thresholds. Aim for rigor but accept that there will be an element of vibes-based assessment.

**Quantitative metrics:**

- Skill triggers on 90% of relevant queries
  - *How to measure:* Run 10-20 test queries that should trigger your skill. Track how many times it loads automatically vs. requires explicit invocation.
- Completes workflow in X tool calls
  - *How to measure:* Compare the same task with and without the skill enabled. Count tool calls and total tokens consumed.
- 0 failed API calls per workflow
  - *How to measure:* Monitor MCP server logs during test runs. Track retry rates and error codes.

**Qualitative metrics:**

- Users don't need to prompt Claude about next steps
  - *How to assess:* During testing, note how often you need to redirect or clarify. Ask beta users for feedback.
- Workflows complete without user correction
  - *How to assess:* Run the same request 3-5 times. Compare outputs for structural consistency and quality.
- Consistent results across sessions
  - *How to assess:* Can a new user accomplish the task on first try with minimal guidance?

## Technical requirements

### File structure

```
your-skill-name/
├── SKILL.md            # Required - main skill file
├── scripts/            # Optional - executable code
│   ├── process_data.py
│   └── validate.sh
├── references/         # Optional - documentation
│   ├── api-guide.md
│   └── examples/
└── assets/             # Optional - templates, etc.
    └── report-template.md
```

### Critical rules

**SKILL.md naming:**
- Must be exactly `SKILL.md` (case-sensitive)
- No variations accepted (SKILL.MD, skill.md, etc.)

**Skill folder naming:**
- Use kebab-case: `notion-project-setup`
- No spaces: `Notion Project Setup`
- No underscores: `notion_project_setup`
- No capitals: `NotionProjectSetup`

**No README.md:**
- Don't include README.md inside your skill folder
- All documentation goes in SKILL.md or references/
- Note: when distributing via GitHub, you'll still want a repo-level README for human users — see Distribution and Sharing.

## YAML frontmatter: The most important part

The YAML frontmatter is how Claude decides whether to load your skill. Get this right.

**Minimal required format:**

```yaml
---
name: your-skill-name
description: What it does. Use when user asks to [specific phrases].
---
```

That's all you need to start.

### Field requirements

**name** (required):
- kebab-case only
- No spaces or capitals
- Should match folder name

**description** (required):
- MUST include BOTH:
  - What the skill does
  - When to use it (trigger conditions)
- Under 1024 characters
- No XML tags (`<` or `>`)
- Include specific tasks users might say
- Mention file types if relevant

**license** (optional):
- Use if making skill open source
- Common: MIT, Apache-2.0

**compatibility** (optional):
- 1-500 characters
- Indicates environment requirements: e.g. intended product, required system packages, network access needs, etc.

**metadata** (optional):
- Any custom key-value pairs
- Suggested: author, version, mcp-server
- Example:

```yaml
metadata:
  author: ProjectHub
  version: 1.0.0
  mcp-server: projecthub
```

### Security restrictions

Forbidden in frontmatter:
- XML angle brackets (`< >`)
- Skills with "claude" or "anthropic" in name (reserved)

Why: Frontmatter appears in Claude's system prompt. Malicious content could inject instructions.

## Writing effective skills

### The description field

According to Anthropic's engineering blog: "This metadata...provides just enough information for Claude to know when each skill should be used without loading all of it into context." This is the first level of progressive disclosure.

**Structure:**

```
[What it does] + [When to use it] + [Key capabilities]
```

**Examples of good descriptions:**

```yaml
# Good - specific and actionable
description: Analyzes Figma design files and generates developer handoff documentation. Use when user uploads .fig files, asks for "design specs", "component documentation", or "design-to-code handoff".

# Good - includes trigger phrases
description: Manages Linear project workflows including sprint planning, task creation, and status tracking. Use when user mentions "sprint", "Linear tasks", "project planning", or asks to "create tickets".

# Good - clear value proposition
description: End-to-end customer onboarding workflow for PayFlow. Handles account creation, payment setup, and subscription management. Use when user says "onboard new customer", "set up subscription", or "create PayFlow account".
```

**Examples of bad descriptions:**

```yaml
# Too vague
description: Helps with projects.

# Missing triggers
description: Creates sophisticated multi-page documentation systems.

# Too technical, no user triggers
description: Implements the Project entity model with hierarchical relationships.
```

## Writing the main instructions

After the frontmatter, write the actual instructions in Markdown.

**Recommended structure:**

Adapt this template for your skill. Replace bracketed sections with your specific content.

```markdown
---
name: your-skill
description: [...]
---

# Your Skill Name

## Instructions

### Step 1: [First Major Step]
Clear explanation of what happens.

Example:
` ``bash
python scripts/fetch_data.py --project-id PROJECT_ID
` ``

Expected output: [describe what success looks like]

(Add more steps as needed)

## Examples

### Example 1: [common scenario]
User says: "Set up a new marketing campaign"
Actions:
1. Fetch existing campaigns via MCP
2. Create new campaign with provided parameters
Result: Campaign created with confirmation link

(Add more examples as needed)

## Troubleshooting

### Error: [Common error message]
Cause: [Why it happens]
Solution: [How to fix]

(Add more error cases as needed)
```

### Best Practices for Instructions

**Be Specific and Actionable**

Good:
```
Run `python scripts/validate.py --input {filename}` to check data format.
If validation fails, common issues include:
- Missing required fields (add them to the CSV)
- Invalid date formats (use YYYY-MM-DD)
```

Bad:
```
Validate the data before proceeding.
```

**Include error handling**

```markdown
## Common Issues

### MCP Connection Failed
If you see "Connection refused":
1. Verify MCP server is running: Check Settings > Extensions
2. Confirm API key is valid
3. Try reconnecting: Settings > Extensions > [Your Service] > Reconnect
```

**Reference bundled resources clearly**

```
Before writing queries, consult `references/api-patterns.md` for:
- Rate limiting guidance
- Pagination patterns
- Error codes and handling
```

**Use progressive disclosure**

Keep SKILL.md focused on core instructions. Move detailed documentation to `references/` and link to it.
