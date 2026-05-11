# refactoring-csharp

Inspired by ReSharper. A Roslyn-based refactorer for C# solutions (`.sln` / `.slnx`), packaged as an agent skill with bundled .NET 10 source and optional prebuilt CLI binaries.

## Quick start

macOS / Linux:

```bash
curl -fsSL https://github.com/CodeAlive-AI/ai-driven-development/releases/download/refactoring-csharp-v0.1.0/install.sh | bash
```

Windows PowerShell:

```powershell
irm https://github.com/CodeAlive-AI/ai-driven-development/releases/download/refactoring-csharp-v0.1.0/install.ps1 | iex
```

Default install targets Codex, Claude Code, and OpenCode. Install to a specific agent:

```bash
curl -fsSL https://github.com/CodeAlive-AI/ai-driven-development/releases/download/refactoring-csharp-v0.1.0/install.sh | bash -s -- --agent cursor
```

```powershell
iex "& { $(irm https://github.com/CodeAlive-AI/ai-driven-development/releases/download/refactoring-csharp-v0.1.0/install.ps1) } -Agent cursor"
```

Install to all supported global agent skill directories:

```bash
curl -fsSL https://github.com/CodeAlive-AI/ai-driven-development/releases/download/refactoring-csharp-v0.1.0/install.sh | bash -s -- --all-agents
```

```powershell
iex "& { $(irm https://github.com/CodeAlive-AI/ai-driven-development/releases/download/refactoring-csharp-v0.1.0/install.ps1) } -AllAgents"
```

Pin a release:

```bash
REFACTORING_CSHARP_VERSION=refactoring-csharp-v0.1.0 \
  curl -fsSL https://github.com/CodeAlive-AI/ai-driven-development/releases/download/refactoring-csharp-v0.1.0/install.sh | bash
```

```powershell
$env:REFACTORING_CSHARP_VERSION = "refactoring-csharp-v0.1.0"
irm https://github.com/CodeAlive-AI/ai-driven-development/releases/download/refactoring-csharp-v0.1.0/install.ps1 | iex
```

## What it does

- Renames C# symbols across a whole solution using Roslyn.
- Supports `.sln` and `.slnx`.
- Resolves targets from `file_path`, 1-based `line_number`, and required `old_name`.
- Applies by default; dry-run is opt-in.
- Renames comments by default.
- Safely moves matching type files by default so git can detect a rename.
- Uses the target solution's normal MSBuild/Roslyn cache instead of creating a second project cache.
- Ships source with the skill so agents can build, inspect, patch, and test it locally.

## Supported agents

The installer follows the global skill directories from the Skills CLI ecosystem and supports:

`adal`, `amp`, `antigravity`, `augment`, `claude-code`, `cline`, `codebuddy`,
`codex`, `command-code`, `continue`, `crush`, `cursor`, `droid`, `gemini-cli`,
`github-copilot`, `goose`, `iflow-cli`, `junie`, `kilo`, `kimi-cli`, `kiro-cli`,
`kode`, `mcpjam`, `mistral-vibe`, `mux`, `neovate`, `openclaw`, `opencode`,
`openhands`, `pi`, `pochi`, `qoder`, `qwen-code`, `replit`, `roo`, `trae`,
`trae-cn`, `windsurf`, and `zencoder`.

Useful flags:

- `--agent <id>` / `-Agent <id>` installs to one agent. Repeatable in bash.
- `--all-agents` / `-AllAgents` installs to every supported global skill directory.
- `--detected` / `-Detected` installs only to agents whose global config directory exists.
- `--no-binary` / `-NoBinary` installs only the skill source.

## Use directly

Preferred, if installed from release with a prebuilt binary:

```bash
~/.codex/skills/refactoring-csharp/bin/csharp-refactor rename-symbol \
  /repo/src/App.slnx \
  /repo/src/Foo.cs \
  42 \
  OldName \
  NewName
```

Source fallback:

```bash
dotnet run --project ~/.codex/skills/refactoring-csharp/src/CSharpRefactoring.Cli -- \
  rename-symbol /repo/src/App.slnx /repo/src/Foo.cs 42 OldName NewName
```

`line_number` is 1-based and can be copied directly from `rg -n`.

## Contract

```text
rename-symbol <solution> <file> <line> <oldName> <newName> [dryRun=false|true]
```

Defaults:

- `dryRun=false`
- `rename_file=true`
- `rename_in_comments=true`
- `rename_in_strings=false`
- `rename_overloads=false`

## Build and test

```bash
cd skills/refactoring-csharp
dotnet build src/CSharpRefactoring.slnx
dotnet test src/CSharpRefactoring.slnx
```

## Release

```bash
cd skills/refactoring-csharp
./release.sh refactoring-csharp-v0.1.0
```

The release script creates:

- `dist/refactoring-csharp-skill.tar.gz`
- `dist/csharp-refactor-darwin-arm64.tar.gz`
- `dist/csharp-refactor-darwin-x64.tar.gz`
- `dist/csharp-refactor-linux-arm64.tar.gz`
- `dist/csharp-refactor-linux-x64.tar.gz`
- `dist/csharp-refactor-win-x64.zip`
- `dist/SHA256SUMS`

## License

MIT.
