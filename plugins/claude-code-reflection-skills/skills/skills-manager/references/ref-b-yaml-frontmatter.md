# Reference B: YAML Frontmatter

## Required fields

```yaml
---
name: skill-name-in-kebab-case
description: What it does and when to use it. Include specific trigger phrases.
---
```

## All optional fields

```yaml
name: skill-name
description: [required description]
license: MIT                                    # Optional: License for open-source
allowed-tools: "Bash(python:*) Bash(npm:*) WebFetch"  # Optional: Restrict tool access
metadata:                                       # Optional: Custom fields
  author: Company Name
  version: 1.0.0
  mcp-server: server-name
  category: productivity
  tags: [project-management, automation]
  documentation: https://example.com/docs
  support: support@example.com
```

## Security notes

**Allowed:**
- Any standard YAML types (strings, numbers, booleans, lists, objects)
- Custom metadata fields
- Long descriptions (up to 1024 characters)

**Forbidden:**
- XML angle brackets (`< >`) - security restriction
- Code execution in YAML (uses safe YAML parsing)
- Skills named with "claude" or "anthropic" prefix (reserved)
