# refactoring-csharp

Agent skill plus bundled .NET 10 Roslyn CLI for C# symbol rename workflows.

The executable source lives in `src/` so the skill is self-contained after install. The agent-facing contract is in `SKILL.md`.

## Build

```bash
cd skills/refactoring-csharp
dotnet build src/CSharpRefactoring.slnx
```

## Test

```bash
cd skills/refactoring-csharp
dotnet test src/CSharpRefactoring.slnx
```

## Run

```bash
cd skills/refactoring-csharp
dotnet run --project src/CSharpRefactoring.Cli -- rename-symbol <sln> <file> <line> <oldName> <newName> [dryRun=true|false]
```

`line` is 1-based and intended to be copied directly from `rg -n` output. `oldName` is required and acts as the target anchor.
