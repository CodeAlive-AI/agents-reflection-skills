# Mole techniques (what to borrow)

Mole (`mo`, github.com/tw93/mole) is the safety-floor tool. Its bash modules implement battle-tested guards for destructive cleanup that we replicate when running shell commands by hand.

## Table of contents

- [Marker → target map for `mo purge`](#marker--target-map-for-mo-purge)
- [Critical safety guards](#critical-safety-guards)
- [Age thresholds](#age-thresholds-mole-defaults--adopt-these)
- [Tier classification](#tier-classification-moles-mental-model)
- [Operational logging](#operational-logging)
- [Mole commands worth remembering](#mole-specific-commands-worth-remembering)
- [Anti-patterns Mole avoids](#anti-patterns-mole-avoids-and-why)
- [Integration recipe](#integration-recipe-when-running-shell-commands-hand-rolled)

## Marker → target map for `mo purge`

`mo purge` finds dev projects by marker files and removes regenerable build/dependency directories. All targets must be **mtime ≥ 7 days** (the `MIN_AGE_DAYS` default).

| Marker | Tooling | Targets |
|---|---|---|
| `package.json`, `yarn.lock`, `pnpm-lock.yaml` | npm/yarn/pnpm | `node_modules`, `.next`, `.nuxt`, `.output`, `dist`, `build`, `.turbo`, `.parcel-cache` |
| `Cargo.toml` | Rust | `target` |
| `pom.xml` | Maven | `target` |
| `build.gradle`, `settings.gradle` | Gradle | `build`, `.gradle` |
| `pyproject.toml`, `requirements.txt`, `Pipfile` | Python | `__pycache__`, `venv`, `.venv`, `.pytest_cache`, `.mypy_cache`, `.tox`, `.nox`, `.ruff_cache` |
| `composer.json` | PHP Composer | `vendor` |
| `go.mod` | Go | `vendor` (protected by default — most Go projects don't vendor) |
| `Gemfile` | Rails/Ruby | `vendor` (protected — Rails vendor often hand-curated) |
| `pubspec.yaml` | Flutter/Dart | `.dart_tool` |
| `Package.swift` | Swift PM | `.build` |
| `build.zig`, `build.zig.zon` | Zig | `.zig-cache`, `zig-out` |
| `*.csproj`, `*.fsproj`, `*.vbproj` | .NET | `bin`, `obj` (with .NET-confirmation guard) |
| `*.xcodeproj` | Xcode | project-local `DerivedData` (global one is protected) |
| `Podfile`, `Podfile.lock` | CocoaPods | `Pods` |
| `app.json` (Expo) | Expo / React Native | `.cxx`, `.expo` |
| `nx.json`, `lerna.json`, `pnpm-workspace.yaml`, `rush.json` | Monorepo | applies recursively to subprojects |
| `angular.json` | Angular | `.angular` |
| `svelte.config.*` | SvelteKit | `.svelte-kit` |
| `astro.config.*` | Astro | `.astro` |
| any project | universal | `coverage` |

### Default scan paths (Mole)

```
~/www, ~/dev, ~/Projects, ~/GitHub, ~/Code, ~/Workspace, ~/Repos, ~/Development
```

Plus auto-discovery of immediate `$HOME` subdirectories that contain `.git`. Configurable via `mo purge --paths` (file at `~/.config/mole/purge_paths`, plain text, one path per line, supports `~`).

## Critical safety guards

### bin/ guard (.NET only)

`bin/` is purged ONLY if the parent has both:
1. A `*.csproj`, `*.fsproj`, or `*.vbproj` file
2. A `Debug/` or `Release/` subdirectory inside `bin/`

This prevents accidentally deleting Go-built binaries, generated CLI scripts, or `bin/` aliasing.

### vendor/ guard (PHP only)

`vendor/` is purged ONLY if `composer.json` is present. Go's `vendor/` (which contains hand-pinned dependencies) is protected. Rails `vendor/` (with vendored gems and assets) is protected.

### DerivedData guard

The global `~/Library/Developer/Xcode/DerivedData` is protected (other Xcode logic handles it). Project-local `DerivedData/` (inside an `.xcodeproj` project) is fair game.

### Project root detection

Build artifacts are purged only if they're inside a detected project (project must have at least one marker file, ≥ 2 levels deep, and `.git` directory or `Makefile` boost).

### Symlink validation

Symlinks are resolved and checked; if the target points into a protected system path (`/System/*`, `/bin/*`, etc.) the symlink itself is NOT followed for deletion.

### Path validator (`validate_path_for_deletion`)

Every destructive path goes through this gate (in `lib/core/file_ops.sh`):
- Reject empty path
- Reject relative paths (must be absolute)
- Reject `..` as a complete path component (`/foo/../bar` rejected; `Firefox.../` allowed because `..` not whole component)
- Reject control characters in paths
- Block list of system roots (see `never-touch.md` § Hard-protected paths)
- Allowlist for specific `/private/...` subpaths

These checks happen BEFORE any `rm` runs. Even with sudo, blocked paths are rejected.

## Age thresholds (Mole defaults — adopt these)

```bash
MOLE_TEMP_FILE_AGE_DAYS=7        # /private/tmp, app temp
MOLE_LOG_AGE_DAYS=7              # *.log, *.gz, *.asl
MOLE_CRASH_REPORT_AGE_DAYS=7     # /Library/Logs/DiagnosticReports
MOLE_ORPHAN_AGE_DAYS=30          # data for uninstalled apps
MOLE_SAVED_STATE_AGE_DAYS=30     # ~/Library/Saved Application State
MOLE_MAIL_AGE_DAYS=30            # Mail attachments (also size-gated)
MOLE_TM_BACKUP_SAFE_HOURS=...    # Time Machine incomplete-backup safety window
MOLE_XCODE_DEVICE_SUPPORT_KEEP=2 # iOS DeviceSupport: keep N most recent
```

When adapting cleanup to bare `find` calls, always include `-mtime +7` (or +30 for orphan/saved state). This single rule eliminates 90 % of "I just created that yesterday" surprises.

## Tier classification (Mole's mental model)

Mole's runtime classifies cleanup actions in three tiers. We follow the same:

### Tier 1 — Auto-include (run without confirmation)
- Package manager caches: npm, pnpm, yarn, bun, cargo, gradle, maven, NuGet, brew
- Tool-specific: TypeScript, Webpack, Vite, Turbo, Parcel, ESLint, Prettier, node-gyp, Electron
- Python: pip, poetry, uv, pipenv (caches only)
- Go: `go clean -cache && go clean -modcache`
- System logs > 7 days
- System temp > 7 days
- Crash reports > 7 days
- Browser code-signing clones in `/private/var/folders/.../X/*.code_sign_clone`
- macOS-managed: `/private/var/db/diagnostics`, `/private/var/db/powerlog`, `/private/var/db/reportmemoryexception`
- Trash, recent items lists

### Tier 2 — Hint-only (Mole prints "Review: ..." and does nothing)
- Docker (says: `Review: docker system df`, `Prune: docker system prune --filter until=720h`)
- iPhone backups (`~/Library/Application Support/MobileSync/Backup`)
- Project build artifacts (handed to `mo purge`, which is interactive)
- Stale launch agents
- Large system data > 2 GB

### Tier 3 — Hard-protected (NEVER touched, see `never-touch.md`)

## Operational logging

Mole writes every destructive operation to `~/.config/mole/operations.log` and `~/Library/Logs/mole/operations.log` (append-only). Format:

```
TIMESTAMP\tCOMMAND\tACTION\tPATH\tSIZE\tSTATUS
2025-01-15 09:12:43\tpurge\tREMOVED\t~/node_modules\t1.1G\tOK
```

Adopt the same pattern for hand-rolled cleanups. It's the audit trail when "what did we delete?" comes up later.

## Mole-specific commands worth remembering

| Command | Use |
|---|---|
| `mo` | TUI menu — start here if user wants to be guided |
| `mo clean` | Tier 1 cache cleanup (always with `--dry-run` first) |
| `mo clean --dry-run --debug` | Preview + risk assessment |
| `mo purge` | Interactive project-artifact removal |
| `mo purge --paths` | Edit scan paths in `$EDITOR` |
| `mo uninstall <app>` | Remove app + 12 location traces |
| `mo analyze` | Disk usage TUI (no destructive ops) |
| `mo analyze /Volumes` | Same for external drives |
| `mo status` | Live CPU/mem/disk dashboard |
| `mo installer` | Find and remove .dmg/.pkg/.zip installers |
| `mo optimize` | Rebuild system DBs, reset services (use sparingly) |
| `mo --whitelist` | Manage protected paths (user-additions to never-touch list) |

## Anti-patterns Mole avoids (and why)

| Anti-pattern | Why bad | Mole's approach |
|---|---|---|
| `find ... -delete` | Race conditions; if dir contents change mid-delete, partial state | Uses `safe_remove`/`safe_sudo_remove` with explicit `validate_path_for_deletion` |
| `rm -rf $VAR` | If `$VAR` empty due to bug, deletes wrong root | Validates `$VAR` is non-empty, absolute, not in blocklist before any `rm` |
| Auto-confirm | User can't recover from mistake | Every destructive op requires explicit confirm or dry-run flag |
| Aggressive whitelist | Misses edge cases | Defaults conservative, user can opt in to more via `--whitelist` |
| Trust file extensions | `*.log` could be a critical file misnamed | Combines extension + age + path-allowlist |

## Integration recipe (when running shell commands hand-rolled)

If implementing a custom sweep without Mole, port these patterns:

```bash
# Wrapper
safe_clean() {
  local target="$1"
  [ -z "$target" ] && return 1
  case "$target" in /|/System*|/bin*|/sbin*|/usr*|/etc*|/private/var/db/uuidtext*|/Library/Extensions*) return 1 ;; esac
  case "$target" in *..*) return 1 ;; esac
  [ -e "$target" ] || return 0
  rm -rf "$target"
}

# Apply with -mtime
find "$ROOT" -maxdepth 4 \
  -name "node_modules" \
  -prune -mtime +7 \
  -print0 | xargs -0 -I{} bash -c 'safe_clean "$1"' _ {}
```

This is the minimal Mole-style harness. Anything more aggressive belongs in `mo purge` proper.
