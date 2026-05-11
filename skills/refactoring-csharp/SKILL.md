---
name: refactoring-csharp
description: Rename and refactor C# symbols in a solution with a one-shot Roslyn CLI. Use when the user asks to rename a symbol, preview impact, or update references across a .NET solution.
---

# Refactoring C# Symbols

This skill documents the one-shot Roslyn rename contract used by a C# refactoring CLI.
It is intentionally one-shot and stateless: one call resolves the target, validates the request,
and returns either a preview or an applied rename. There is no public prepare step.

## Canonical CLI

Use the current workspace's Roslyn refactoring CLI. The command shape is:

```bash
dotnet run --project <rename-cli-project> -- rename-symbol <sln> <file> <line> <oldName> <newName> [dryRun=true|false]
```

## Contract

| Field | Required | Default | Notes |
| --- | --- | --- | --- |
| `solution_path` | yes | - | Absolute path to the `.sln` file. |
| `file_path` | yes | - | Absolute path to a file inside the solution. |
| `line_number` | yes | - | 1-based line number. Use the value reported by `rg -n`. |
| `old_name` | yes | - | Exact current identifier on that line. This is the anchor. |
| `new_name` | yes | - | Must be a valid C# identifier. |
| `dry_run` | no | `true` | Preview only when `true`. Apply changes when `false`. |
| `rename_overloads` | no | `false` | Keep overloads unchanged by default. |
| `rename_in_strings` | no | `false` | String literals stay untouched by default. |
| `rename_in_comments` | no | `true` | Comments are renamed by default. |
| `rename_file` | no | `true` | Safe file move for supported named types. Never recreate the file as delete+add. |

## How To Use It

1. Use `rg -n` to locate the symbol and copy the 1-based line number directly.
2. Call `rename-symbol` with `dryRun=true` first unless the user explicitly asked to apply immediately.
3. If the preview is correct, call the same command again with `dryRun=false`.
4. Summarize the result by reporting the original name, new name, changed document count, total text changes, changed files, and any file move.

## Important Behavioral Rules

- The tool is stateless. It loads the solution on every call.
- A preview does not reserve state. If the workspace changes between preview and apply, rerun the preview.
- Do not invent a session or hidden prepare state.
- Do not ask for a column number. The tool resolves from `file_path`, `line_number`, and `old_name`.
- `old_name` is mandatory because it disambiguates the target when a line contains more than one renameable identifier.
- If the tool returns a preview, say preview. If it returns applied changes, say applied.
- Keep responses concise and action-oriented. Tell the user what changed and whether a file move happened.

## Supported Targets

Treat these as supported rename targets when the Roslyn symbol is source-backed and
`CanBeReferencedByName`:

- `NamedType`
- `Method`
- `Property`
- `Field`
- `Event`
- `Parameter`
- `Local`
- `TypeParameter`
- `Namespace`

Do not rename constructors, destructors, static constructors, or indexers.

## File Rename Nuance

`rename_file=true` is a convenience default, but it only produces a real safe move when the
symbol is a single-declaration named type and the file stem matches the current type name.

If the tool does not return `file_move_from_path` and `file_move_to_path`, the symbol rename is still valid,
but the file itself was not moved. Do not claim a file rename happened unless the tool reports it.

This is intentionally conservative so git sees a tracked rename instead of a delete+add pair.

## Error Handling

Use the tool's error codes as actionable guidance:

| Error code | Meaning | What to do |
| --- | --- | --- |
| `invalid_solution_path` | Solution path is missing or not a `.sln` file. | Ask for a real solution path. |
| `invalid_file_path` | File path is missing or not present on disk. | Ask for the correct file path. |
| `file_not_in_solution` | The file is not part of the loaded solution. | Ask for the correct file or solution. |
| `invalid_line_number` | Line number is outside file bounds or not 1-based. | Ask for the correct line. |
| `invalid_old_name` | `old_name` was empty or whitespace. | Ask for the exact current name. |
| `old_name_not_found_on_line` | No renameable symbol with that name exists on the line. | Ask for a better line or file. |
| `ambiguous_old_name_on_line` | More than one renameable symbol matches that name on the line. | Narrow the target or use a different line. |
| `unsupported_symbol_kind` | Roslyn found a symbol, but this kind is not renameable here. | Move to a supported symbol kind. |
| `symbol_not_in_source` | The symbol is not declared in source. | Pick a source-backed target. |
| `invalid_new_name` | `new_name` is not a valid C# identifier. | Propose a valid identifier. |
| `same_name` | New name equals the current name. | Ask for a different name. |
| `no_changes` | Roslyn produced no text edits. | Re-check the target or the new name. |
| `apply_failed` | Workspace apply failed. | Treat as a runtime failure and retry only if the state is unchanged. |
| `operation_timeout` | The rename timed out. | Retry with a larger timeout or a narrower target. |

## Success Criteria

A rename workflow is complete when:

- The target was resolved from `line_number` + `old_name`.
- The user approved the rename, or explicitly requested a dry run only.
- The tool returned changed documents, total text changes, and any file move details.
- The final answer makes the applied scope clear enough for the user to trust the change.

## Recommended Output Style

- For previews, say what would change and that nothing was applied.
- For applied changes, say what changed and whether the file was moved.
- If the file move fields are present, mention them explicitly.
- If the tool returned an error code, echo the code and the human-readable reason.
