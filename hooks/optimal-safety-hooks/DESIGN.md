# Optimal Safety Hooks for Claude Code — Design Doc

**Status**: v3, post-consilium + Go switch. Approved for implementation.
**Author**: rodio (with Claude Opus 4.7)
**Date**: 2026-05-03
**Target**: Replace `~/.claude/hooks/validate-rm.py` and `~/.claude/hooks/safety-net-ask.sh` with a single, well-tested, false-positive-resistant Bash safety hook.

**Changelog**:
- v1 — initial Python + tree-sitter-bash design.
- v2 — consilium (Codex gpt-5.5 + OpenCode/Gemini-3.1-Pro) addressed 5 P0/P1 must-fixes: untrusted project configs, macOS bash binary selection, executor unwrapping, asymmetric fail-open, robust assertions.
- v3 — switched runtime to Go + [mvdan.cc/sh](https://github.com/mvdan/sh) per rodio's perf concern. Single static binary, build-on-stale wrapper for hot-reload editing.
- v3.1 — dropped the bash wrapper after measuring 80 ms per-invocation overhead from `go build` no-op. settings.json now points directly at `bash_guard.bin`; rebuilds are explicit (`make build` or `make watch`). End-to-end latency 0-10 ms warm.
- v3.2 — phases 0/1/2 collapsed in one go: shipped `rule_supabase.go`, `rule_bw.go`, `rule_infra.go`, ran `install.sh --live --replace-legacy`. Bash hook chain reduced from 7 entries to 1; 92 fixtures (~30 of them on the new rules) all green.

---

## 1. Problem

Two false positives observed in production on 2026-05-03 prove the current hook stack is brittle:

**FP-1**: `cat > /tmp/file <<'EOF' ... English prose with don't, it's, model's ... EOF` triggers `validate-rm.py` because the word `find` appears in the prose. `shlex(posix=True)` fails on apostrophes inside the heredoc body, hook returns `ask("Malformed command")`. Harmless command, user confirmation dialog.

**FP-2**: `cd /tmp && rm -rf ci-results && ...` blocked by safety-net plugin's "rm -rf outside cwd" rule. `/tmp` is universally safe scratch space; this rule is wrong for an agent context.

Root causes: brittle parser (shlex breaks on heredocs), trigger keywords matched in non-executable spans, missing `/tmp` allowlist, fail-closed on parse error, forgotten plugin wrapper bypassing `enabledPlugins`.

---

## 2. Goals & Non-Goals

### Goals

- Eliminate FP-1 and FP-2 with regression-locked tests.
- Single replacement program for both legacy hooks.
- < 30 ms cold path, < 10 ms warm — Bash-hook is invoked on every Bash tool call.
- High recall on real destructive operations: `rm -rf /`, `$HOME`, `/etc`, `/usr`, etc.
- **Never emit `permissionDecision: "deny"`**. Only `allow` or `ask`. Reason: agents trivially bypass `deny` (rephrase, split, retry); the user is the real defense. Memory: `feedback_no_deny_in_hooks.md`.
- Treat the hook as a real program: typed, tested, configurable, observable, hot-editable.

### Non-Goals

- Replacing `protect-files.sh` (Write|Edit matcher).
- Replacing `ccnotify.py` (UserPromptSubmit/Stop/Notification).
- Generic shell linting.
- Network exfiltration detection (separate hook, separate concern).

---

## 3. Architecture

### 3.1 Layout

Source lives in the `ai-driven-development` repo (under `hooks/optimal-safety-hooks/`); deployed via symlink to `~/.claude/hooks/bash-guard/` so edits in git pick up live (build-on-stale wrapper rebuilds on next invocation).

```
my-projects/ai-driven-development/hooks/optimal-safety-hooks/
├── DESIGN.md                # this file
├── README.md                # short user-facing intro
├── install.sh               # idempotent installer (symlinks src/ + writes settings.json)
├── .github/workflows/test.yml
└── src/
    ├── go.mod, go.sum
    ├── Makefile             # build / test / fmt / watch
    ├── main.go              # entrypoint, JSON in/out, top-level pipeline
    ├── parser.go            # mvdan/sh wrapping, AST → spans
    ├── span.go              # SpanKind classification
    ├── unwrap.go            # executor unwrap table
    ├── safe_paths.go        # safe-paths allowlist + realpath + lstat
    ├── decision.go          # Decision dataclass + aggregation (no deny tier)
    ├── audit.go             # JSONL log + size-based rotation + 0o600
    ├── config.go            # TOML loader + trust system
    ├── rules/
    │   ├── rules.go         # Rule interface, registry
    │   ├── rm.go            # rm/unlink/rmdir/shred + safe-paths
    │   ├── docker.go        # supplants docker-prune-permission.sh (phase 2)
    │   ├── supabase.go      # supplants supabase-safety.sh (phase 2)
    │   ├── bw.go            # supplants bw-permission-check.sh (phase 2)
    │   └── infra.go         # supplants infra-safety.sh (phase 2)
    ├── trusted-projects.toml.example
    ├── config.toml          # global defaults
    ├── build.log            # gitignored
    ├── bash_guard.bin       # gitignored
    └── testdata/
        ├── README.md
        └── fixtures/*.json
```

### 3.2 Runtime: direct Go binary, explicit rebuild

`settings.json` invokes the binary directly:

```jsonc
{
  "matcher": "Bash",
  "hooks": [
    { "type": "command",
      "command": "BASH_GUARD_SHADOW=1 ~/.claude/hooks/bash-guard/bash_guard.bin" }
  ]
}
```

`~/.claude/hooks/bash-guard/` is a symlink to `ai-driven-development/hooks/optimal-safety-hooks/src/`. Editing a `.go` file requires an explicit rebuild — `make build` from the source dir, or `make watch` (entr-based) during development. The Go binary itself is gitignored.

**Performance** (measured on M-series macOS):
- Cold first call (kernel page-cache miss): ~180 ms (one-time after reboot or upgrade).
- Warm: 0-10 ms end-to-end.
- Quick-reject path (no trigger keyword): ~0.16 ms inside the binary; rest is OS/exec overhead.

**Earlier design had a build-on-stale shell wrapper that called `go build`** on every invocation for hot-reload convenience. Measured ~80 ms steady-state overhead per Bash command. With hundreds of Bash calls per agent session, the cost added up to minutes per day for a feature used a few times per week. Dropped it — explicit `make build` after edits is cheap; we kept `make watch` for tight inner-loop development.

**Why not pre-built binary committed to git**: keeps repo small, avoids cross-arch concerns, source-only repo makes trust audit trivial. The Makefile re-bootstrap is 2 seconds.

**Why not `go run .`**: each invocation is a fresh compile to `/tmp`, ~200-300 ms even warm.

### 3.3 Pipeline

```
stdin JSON
    │
    ├─ tool_name != "Bash" ──────────────► allow
    │
    ├─ quick_reject(cmd) ────────────────► allow   # no trigger keyword anywhere
    │
    ├─ parse with mvdan/sh
    │       │
    │       └─ parse error ──────────────► allow   # pre-trigger fail-open
    │                                              # (asymmetry — see §3.6)
    │
    ├─ build span tree (Executed | Data | HeredocBody | InlineCode)
    │
    ├─ unwrap executor wrappers (sudo, env, xargs, find -exec, bash -c, ...)
    │
    ├─ for each ExecutedCommand, run all matching rules
    │
    ├─ aggregate(decisions):  ask > allow   (no deny tier)
    │
    └─ write JSON to stdout, audit log to ~/.claude/logs/bash-guard.jsonl
```

### 3.4 Span classification & executor unwrapping

`mvdan.cc/sh/v3/syntax` produces a typed Go AST. Walk it via the `Walk(node, visitor)` API; classify each subtree:

| AST node | SpanKind | Rules apply? |
|---|---|---|
| `*syntax.CallExpr` (top-level / pipe child / subshell) | Executed (after unwrap) | yes |
| `*syntax.SglQuoted`, `*syntax.DblQuoted` | Data (default) | no |
| `*syntax.Heredoc.Body` | HeredocBody | no |
| `*syntax.CmdSubst` (`$(...)`, `` `...` ``) | Executed | yes |
| `*syntax.ProcSubst` (`<(...)`, `>(...)`) | Executed | yes |
| `*syntax.Assign` (rhs) | Data | no |

**Critical**: mvdan/sh does NOT auto-unwrap executor wrappers. `sudo rm -rf /` parses as `CallExpr{Args: ["sudo", "rm", "-rf", "/"]}`. Without explicit unwrapping, the rm-rule's keyword set never matches. Implement an explicit unwrap pass.

#### Unwrap table

| Wrapper | Behavior |
|---|---|
| `sudo`, `doas` | Skip flags (`-u USER`, `-g GROUP`, `-C N` take an arg; `-i`, `-s`, `-n`, `-E`, `-H`, `-k` standalone), then unwrap the inner command. |
| `env` | Skip leading `KEY=VALUE` assignments and flags (`-i`, `-u VAR`, `--`), then unwrap. |
| `command`, `builtin`, `exec` | Skip `-p`, `-v`, `-V` (or `-c`/`-l` for exec), then unwrap. |
| `time`, `/usr/bin/time`, `nice`, `nohup`, `ionice`, `setsid`, `script -q -c` | Skip until non-flag token, then unwrap. |
| `timeout`, `gtimeout` | Skip first non-flag (duration), then unwrap. |
| `chroot` | Skip newroot path + optional user, mark inner as `Chrooted=true`. **Default ask** — paths inside refer to a different fs root. |
| `ssh`, `rsync --rsync-path=`, `scp` (only when remote command tail visible) | Mark as `Remote=true`. Local safe-path allowlist does NOT apply. **Default ask** if remote command contains a trigger keyword. |
| `bash -c`, `sh -c`, `zsh -c`, `dash -c`, `fish -c`, `ksh -c` | Re-parse the next quoted arg as bash with mvdan/sh, recursively unwrap. |
| `eval` | Concatenate args with space, re-parse as bash, unwrap. |
| `xargs` | Mark target command as `StdinArgs=true`. **Default ask** if target is a trigger keyword. |
| `find` (with `-delete`, `-exec rm ...`, `-execdir rm ...`, `-okdir rm ...`) | Synthesize a virtual `rm` ExecutedCommand whose target paths are the search roots (path arguments of `find` before the predicate). |
| `parallel`, `watch`, `flock`, `at`, `crontab -e -c` | Same as `xargs` — args dynamic, ask if trigger keyword. |

Unwrapping is recursive: `sudo timeout 10 bash -c "env FOO=1 rm -rf /tmp/x"` resolves to a single Executed `rm -rf /tmp/x`.

#### Pipeline-tail evaluators

`echo "rm -rf /" | bash` — mvdan/sh parses as a pipeline of two CallExprs: `echo` and `bash`. We detect the shape (last stage is `bash`/`sh`/`zsh`/`dash` with no `-c`) and re-parse the upstream `echo`/`printf` literal arg as bash. Limitation: arbitrary upstream computation (`grep`, `tr`, `sed | bash`) is NOT statically reducible — for those, default to `ask` because the sink is a shell evaluator with unknown input. Documented in §9.

### 3.5 quick_reject

Static set built at startup from `Rule.Triggers()` of every registered rule:

```go
var triggerRE = regexp.MustCompile(`\b(?:` + strings.Join(escaped, "|") + `)\b`)

func quickReject(cmd string) bool {
    return !triggerRE.MatchString(cmd)
}
```

Runs in microseconds. False positives here are fine (e.g., `find` in heredoc body) — the parser then classifies it as HeredocBody and rules don't fire.

### 3.6 Asymmetric fail-open (consilium-driven)

| Failure | Decision | Rationale |
|---|---|---|
| Quick-reject doesn't match → no parsing → done | `allow` | Trivial commands stay fast. |
| Parse error in mvdan/sh BEFORE any rule trigger | `allow` | Malformed-but-trigger-free command — bash itself will reject. |
| Parse error AFTER trigger keyword detected by quick-reject | `ask` with reason `bash-guard unavailable for risky command` | Silent allow on a triggered command would disable safety on risky path. |
| AST walk panics, rule eval crashes | `ask` (recover with `defer`/`recover()`) | Same logic — risky path, must surface. |
| Config load fails | `allow` + log to stderr | Config error during normal startup; not blocking user. |
| Binary exec fails (wrapper) | `allow` + reason | Build broken; user sees explanation in dialog. |
| Audit log open fails | continue, log to stderr | Logging is best-effort. |

This asymmetry was a P0 from Codex. Closes the silent-disable gap.

### 3.7 Aggregation

```go
type Decision struct {
    Level      string // "allow" | "ask"  — never "deny"
    Rule       string
    Reason     string
    ReasonCode string // stable identifier for tests, e.g., "rm.outside_safe_path"
    Context    string // additionalContext payload
}

func Aggregate(ds []Decision) Decision {
    asks := []Decision{}
    for _, d := range ds { if d.Level == "ask" { asks = append(asks, d) } }
    if len(asks) == 0 {
        return Decision{Level: "allow", Rule: "default", ReasonCode: "no_rule_matched"}
    }
    // Concatenate reasons; preserve all reason_codes for log.
    return Decision{
        Level: "ask",
        Rule:  "aggregate",
        Reason: strings.Join(reasons(asks), "; "),
        ReasonCode: strings.Join(codes(asks), ","),
        Context: strings.Join(contexts(asks), " | "),
    }
}
```

No deny tier anywhere. Compile-time invariant: the type only allows `"allow"` and `"ask"` (we use a typed enum, see §3.7 in code).

### 3.8 Output

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "ask",
    "permissionDecisionReason": "[rm] target /etc resolves outside safe paths",
    "additionalContext": "code:rm.outside_safe_path target=/etc safe_paths=/Users/test/myproject,/tmp,/var/tmp,$TMPDIR,~/.cache"
  }
}
```

Always exit 0 — Claude Code only parses JSON on exit-0.

---

## 4. rm-rule

### 4.1 Triggers

```go
var triggers = []string{"rm", "unlink", "rmdir", "shred"}
```

Executor wrappers (`sudo`, `env`, `xargs`, `find`, `bash -c`, `eval`, ...) are NOT triggers — they're handled by the parser unwrap pass in §3.4. By the time rm-rule sees an ExecutedCommand, it's already unwrapped to the bare `rm` form.

### 4.2 Safe paths

Default allowlist (resolved with `filepath.EvalSymlinks` for the parent dir, `os.Lstat` for the final operand):

- `cwd` and any path in its subtree, **except** when `cwd ∈ {/, $HOME, /Users, /home}` (consilium P0 from Gemini — cwd-as-root would whitelist everything; in those cases cwd contributes nothing to safe paths).
- `/tmp`, `/private/tmp`, `/var/tmp`
- `$TMPDIR` if set
- `$XDG_CACHE_HOME` (default `~/.cache`)
- `$XDG_RUNTIME_DIR`
- `~/Library/Caches` (macOS only)
- Per-project safe paths from a **trusted** project config (see §6.2).

#### Symlink semantics

POSIX `rm` does NOT follow symlinks unless trailing slash. So:

- `rm /tmp/link-to-home` (no trailing slash): deletes the symlink itself, not its target. Classify by `lstat()` of the operand: it's a symlink, parent is `/tmp` (safe), so allow. Don't realpath.
- `rm /tmp/link-to-home/` (trailing slash): dereferences the link. Realpath the target → `~`. Catastrophic. Ask.
- `rm -rf /tmp/dir/with/link-inside` where `link-inside → ~`: rm itself does not traverse into the symlink. Allow. (This is not a TOCTOU vulnerability of the hook — it's how rm works.)

#### Catastrophic paths (always ask, never allow)

`/`, `$HOME`, `~`, `/etc`, `/usr` (except `/usr/local/<scope>`), `/var` (except `/var/tmp`), `/System`, `/Library`, `/private` (except `/private/tmp`, `/private/var/tmp`), `/Applications`, `/bin`, `/sbin`, `/opt`. All variants with realpath dereferencing too.

### 4.3 Decision matrix

For each non-flag argument of `rm`:

| Resolution | Outcome |
|---|---|
| Path resolves inside a safe path | `allow` |
| Path is exactly a safe-path root (`rm -rf /tmp` itself) | `ask` (code: `rm.delete_safe_root`) |
| Top-level glob inside a shared safe root (`rm -rf /tmp/*`, `rm -rf /var/tmp/.*`) | `ask` (code: `rm.shared_root_glob`) |
| Path is a catastrophic path (or contains its prefix) | `ask` (code: `rm.catastrophic`) |
| Path is `.` or `$(pwd)` and cwd is one of `{/, $HOME, ...}` | `ask` (code: `rm.cwd_is_root_or_home`) |
| Path is unresolvable (`$VAR` undefined, `$(cmd)`, glob `*` outside cwd) | `ask` (code: `rm.unresolvable`) |
| Path resolves outside safe paths but is not catastrophic | `ask` (code: `rm.outside_safe_path`) |

If any single argument warrants ask, the whole command is ask. Reason concatenates per-arg codes.

### 4.4 Argument parsing

The rm rule's argument parser handles real GNU rm (and BSD rm) syntax:

- `--` end-of-options sentinel (everything after is operands, even `-rf`).
- Combined short flags: `-rf`, `-fr`, `-rfv`, `-RF`.
- Long flags with `=`: `--recursive=always`, `--interactive=never`.
- Repeated `-i`/`-f`: last one wins (POSIX semantics).
- `--no-preserve-root` flag (note in additionalContext as escalation indicator).
- Operands beginning with `-` after `--`: literal filename, e.g., `rm -- -rf` deletes a file named `-rf`.

Same logic for `rmdir -p`, `shred --remove[=HOW]`, `unlink`.

### 4.5 Examples

```bash
# allow
rm -rf node_modules
rm /tmp/foo.txt
rm -rf /tmp/ci-results                          # FIXES FP-2
rm -- -rf                                       # literal "-rf" file in cwd
git commit -m "Fix rm -rf detection bug"        # rm in Data span only
echo "rm -rf /" | tee /tmp/joke.txt             # rm in Data span only
cat > /tmp/x <<'EOF'                            # FIXES FP-1
We use find and rm a lot.
EOF

# ask
rm -rf /tmp                                     # safe root itself
rm -rf /tmp/*                                   # shared root top-level glob
rm -rf "$HOME/Downloads/old"                    # catastrophic prefix
rm -rf /etc/nginx                               # catastrophic /etc
rm -rf /                                        # catastrophic / — still ASK, not deny
sudo rm -rf /var/log/old.log                    # /var/log not in safe paths
rm -rf "$UNDEFINED_VAR/important"               # unresolvable
echo 'rm -rf /' | bash                          # pipe into shell evaluator
ssh server 'rm -rf /'                           # remote — local allowlist N/A
chroot /mnt rm -rf /etc                         # chrooted — paths reinterpreted
xargs -a list rm -rf                            # stdin args dynamic
```

---

## 5. Quality, testing, observability

### 5.1 Tests

Standard Go testing. Golden-table fixtures under `testdata/fixtures/`:

```json
{
  "name": "rm_rf_tmp_subdir",
  "description": "FP-2 regression (2026-05-03)",
  "input": {
    "tool_name": "Bash",
    "tool_input": { "command": "cd /tmp && rm -rf ci-results && mkdir ci-results" },
    "cwd": "/Users/test/myproject"
  },
  "expect": {
    "decision": "allow",
    "rule": "default",
    "reason_code": "no_rule_matched"
  }
}
```

Tests assert on the `(decision, rule, reason_code)` tuple plus optional `reason_substring`. Full reason strings are NOT in golden — they are stable for users but can change without breaking tests.

#### Required fixtures (≥35)

**Regressions**:
- `heredoc_with_apostrophes` (FP-1)
- `rm_rf_tmp_subdir` (FP-2)

**Span classification**:
- `find_word_in_heredoc_body`
- `rm_word_in_quoted_string`
- `git_commit_m_rm_message`
- `rm_word_in_command_substitution_data_arg`
- `escaped_backslash_rm`

**rm safe-paths**:
- `rm_rf_cwd_subdir`
- `rm_rf_tmp_subdir`, `rm_rf_var_tmp_subdir`, `rm_rf_xdg_cache_subdir`
- `rm_rf_TMPDIR_set`, `rm_rf_TMPDIR_unset`
- `rm_rf_macos_caches`
- `rm_dash_dash_target` (`rm -- -rf`)

**rm safe-root edge**:
- `rm_rf_tmp_root_itself` (ask)
- `rm_rf_tmp_glob` (ask)
- `rm_rf_var_tmp_glob` (ask)

**rm catastrophic** (all ask, no deny):
- `rm_rf_root`, `rm_rf_home`, `rm_rf_etc`, `rm_rf_usr_local`, `rm_rf_System`, `rm_rf_Library`, `rm_rf_var_log`
- `rm_rf_dollar_home`, `rm_rf_tilde`
- `rm_rf_no_preserve_root`

**Symlink**:
- `rm_symlink_no_trailing_slash_to_home` (allow — link only, not target)
- `rm_symlink_trailing_slash_to_home` (ask — dereferences)

**cwd-as-root**:
- `cwd_is_home_rm_dot` (ask)
- `cwd_is_root_rm_dot` (ask)
- `cwd_normal_rm_dot` (allow)

**Parser-recursion / unwrap**:
- `sudo_rm_rf_var_log`
- `env_FOO_rm_rf_etc`
- `bash_dash_c_rm_rf_etc`
- `sh_dash_c_rm_in_safe_path` (allow)
- `eval_rm_string`
- `find_exec_rm_in_cwd` (allow)
- `find_delete_etc` (ask)
- `xargs_rm_via_stdin` (ask)
- `ssh_remote_rm_root` (ask)
- `chroot_rm_etc` (ask)
- `command_wrapper_rm`

**Variable / glob**:
- `rm_rf_undef_var` (ask, code: `rm.unresolvable`)
- `rm_glob_in_cwd` (allow)
- `rm_glob_outside_cwd` (ask)

**Pipe-to-shell**:
- `echo_rm_pipe_bash` (ask)
- `printf_rm_pipe_sh` (ask)
- `cat_static_pipe_bash` (ask, conservative)

**Edge cases**:
- `empty_command`, `comment_only_command`
- `multi_command_chain` (`a && b && rm /tmp/x`)
- `subshell_rm` (`(rm -rf /tmp/x)`)
- `process_substitution_with_rm`
- `huge_heredoc_no_rm` (10 KB, performance regression)
- `malformed_unbalanced_quote` (allow — pre-trigger fail-open)
- `malformed_after_trigger` (ask — post-trigger fail-open)

#### Performance regression test

`testdata/fixtures/perf/*.json` — set of representative commands. `go test -run TestPerformance` asserts:

| Path | Budget |
|---|---|
| Quick-reject hit | < 1 ms (per-call median) |
| Full parse + rule eval | < 30 ms |
| Huge heredoc (10 KB) | < 50 ms |

Uses `testing.B` benchmarks plus a regression assertion.

### 5.2 Observability

Append-only JSONL at `~/.claude/logs/bash-guard.jsonl`:

```json
{"ts":"2026-05-03T18:00:00Z","mode":"live","decision":"allow","rule":"default","reason_code":"no_rule_matched","latency_ms":3,"command_hash":"sha256:...","command_len":42}
{"ts":"2026-05-03T18:00:05Z","mode":"live","decision":"ask","rule":"rm","reason_code":"rm.catastrophic","latency_ms":42,"command_hash":"sha256:..."}
```

- File created with `0o600` (consilium P2 from Codex).
- Rotation: at startup, if size > 10 MB, rename to `bash-guard.jsonl.1` (keep 3 generations).
- Atomic append: each JSON line < PIPE_BUF (4 KB), Linux/macOS guarantee atomicity for `O_APPEND` writes that small. If a line would exceed PIPE_BUF, fall back to `flock`.

Env vars:
- `BASH_GUARD_LOG_COMMANDS=1` — log raw command text (default off, privacy).
- `BASH_GUARD_DEBUG=1` — mirror to stderr.
- `BASH_GUARD_SHADOW=1` — log decisions, but always emit `allow` JSON (phase 0 of rollout).
- `BASH_GUARD_DRY_RUN=1` — same as shadow, distinct log mode label (phase 1 of rollout).
- `BASH_GUARD_FORCE_REBUILD=1` — wrapper does `go build -a`.

### 5.3 Hook input/output JSON shape (Claude Code 2026)

Confirmed from official docs:

Input:
```json
{
  "hook_event_name": "PreToolUse",
  "tool_name": "Bash",
  "tool_input": { "command": "..." },
  "session_id": "...",
  "cwd": "/abs/path",
  "permission_mode": "default"
}
```

Output (single JSON, exit 0):
```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "allow|ask",
    "permissionDecisionReason": "...",
    "additionalContext": "..."
  }
}
```

We do NOT use `updatedInput` (rewrites change semantics — see §9). We do NOT emit `defer` (no use case in this hook).

---

## 6. Configuration

### 6.1 Global defaults (`config.toml`, in src/)

```toml
[mode]
default = "live"   # "live" | "shadow" | "dry-run"

[safe_paths]
extra = []         # absolute paths added to the global allowlist

[catastrophic_paths]
extra = []         # additional paths beyond the hardcoded set

[rules]
disabled = []      # e.g., ["docker"] to disable
```

### 6.2 Trusted-projects allowlist (consilium P0 — both panelists)

Per-project configs at `<repo>/.claude/bash-guard.toml` are NOT auto-loaded. They are advisory. To be trusted:

1. The project's absolute root path must appear in `~/.claude/hooks/bash-guard/trusted-projects.toml`:

```toml
[[trusted]]
root = "/Users/test/myproject"
# extra safe paths to honour from this project's config (else the per-project config is ignored entirely)
honor_safe_paths = true
honor_catastrophic_overrides = false   # NEVER allow projects to relax catastrophic rules
```

2. Even trusted project configs cannot:
   - Add safe paths outside the project root (`/etc`, `/`, `/Users/other-user`, etc. — rejected with stderr warning).
   - Disable catastrophic-paths protection.
   - Disable rules that aren't already in the global `disabled` list.

3. When an untrusted project config is detected, bash-guard logs **once per session** (deduped by command_hash window):
```
bash-guard: untrusted project config at <path>; ignored. To trust, add to ~/.claude/hooks/bash-guard/trusted-projects.toml.
```

This is the consilium fix. Without it, an agent cloning a repo with a hostile `.claude/bash-guard.toml` could whitelist `/`.

---

## 7. Migration

### 7.1 What gets deleted

- `~/.claude/hooks/validate-rm.py`
- `~/.claude/hooks/safety-net-ask.sh`
- Their entries in `~/.claude/settings.json` `hooks.PreToolUse[Bash].hooks`.
- `enabledPlugins["safety-net@cc-marketplace"]` (no longer referenced).

### 7.2 What gets migrated to rules (phase 2)

After phase 1 ships and runs clean for ≥7 days:

- `supabase-safety.sh` → `rules/supabase.go`
- `bw-permission-check.sh` → `rules/bw.go`
- `docker-prune-permission.sh` → `rules/docker.go`
- `infra-safety.sh` → `rules/infra.go`

Phase 2 reduces the hook chain from 6 entries to 1.

### 7.3 What stays untouched

- `protect-files.sh` (Write|Edit, different concern)
- `~/.claude/ccnotify/ccnotify.py` (UserPromptSubmit/Stop/Notification)

### 7.4 Rollout (consilium-revised)

**Phase 0 — Shadow** (1-3 days): Install bash-guard alongside existing hooks. `BASH_GUARD_SHADOW=1`. Logs decisions but always emits `allow` (no behavioural change). Decision still comes from the legacy chain. Goal: collect log data, identify any new FPs, verify no regressions.

**Phase 1 — Sole evaluator, dry-run** (4-7 days): Remove `validate-rm.py` and `safety-net-ask.sh` from settings.json. bash-guard runs alone with `BASH_GUARD_DRY_RUN=1` — still always `allow`, but log `would_decision` distinctly from `effective_decision`. Goal: prove bash-guard's decisions are correct without the legacy hooks shadowing them.

**Phase 2 — Live**: Remove `BASH_GUARD_DRY_RUN`. Decisions enforced. Old hook scripts can be deleted from disk.

Rollback: at any phase, set `BASH_GUARD_SHADOW=1` instantly disables enforcement.

### 7.5 install.sh

```bash
# Idempotent installer
# - symlinks ai-driven-development/hooks/optimal-safety-hooks/src to ~/.claude/hooks/bash-guard
# - ensures Go toolchain
# - first build (warm cache)
# - patches ~/.claude/settings.json: append bash_guard hook with BASH_GUARD_SHADOW=1
```

Patching settings.json uses a JSON-aware tool (jq) — never sed-based, to avoid corrupting the user's config.

---

## 8. Open questions — answered

1. **Cold-start latency** → answered by Go switch. < 30 ms cold including build no-op. Vendored pre-built binary not needed.
2. **Catastrophic-as-ask** → ask is enough. No multi-step confirmation. Memory: `feedback_no_deny_in_hooks.md`.
3. **Parser gaps** → mvdan/sh covers everything tree-sitter-bash issues #282/#283 surfaced (it's the more mature parser); `bash -n` no longer needed as pre-filter.
4. **Symlinks** → `lstat()` for the operand; trailing slash dereferences. Implemented in §4.2.
5. **Cross-process correctness** → single decision per Bash invocation. Long chains decided at submission.
6. **Plugin packaging** → personal hook in `~/.claude/hooks/bash-guard/`. Plugin packaging only after stable rules + trust system. Both panelists agreed.
7. **Quick-reject FN** → fine; parser handles the FP cleanly. No per-rule budget cap needed.
8. **Aggregation phrasing** → one-line summary in `permissionDecisionReason`, multi-line context in `additionalContext`. Reason carries all per-rule codes for log/test asserts.
9. **`bash -n` portability** → not used (mvdan/sh replaces it). Closes the macOS bash 3.2 vs 5.x divergence.
10. **Test brittleness** → `(decision, rule, reason_code)` tuple + optional reason substring. No full reason-string snapshots.

---

## 9. Acknowledged limitations

These are documented intentionally so future readers don't try to "fix" them via shortcuts that break security:

- **TOCTOU** — bash-guard inspects the command at submission. Filesystem state can change during execution. Example: agent runs `ln -s /etc /tmp/x && rm -rf /tmp/x` in a single Bash call. Static analysis sees `ln -s ... && rm -rf /tmp/x`, the latter classified as `/tmp` subdir = allow. Mitigation: when a Bash command chains `ln -s` and any rm/unlink/rmdir, ask. Rule `rm.symlink_after_create` covers this.
- **`updatedInput` rewrites** — not used in phase 1. Rewriting destructive commands changes semantics (e.g., `rm -rf` → `trash` is not a no-op). Out of scope.
- **Pipeline-tail with non-literal upstream** — `cat manifest | bash` cannot be statically reduced (manifest contents unknown). bash-guard asks for any pipeline whose last stage is a shell evaluator with non-literal upstream. Conservative.
- **`rm -rf` inside subshell with cwd change** — `( cd /etc && rm -rf nginx )`. We unwrap the subshell, see the `cd /etc` then the `rm -rf nginx`. The rm rule resolves `nginx` against `/etc` (lexical cwd from preceding `cd`), classifies as catastrophic → ask. Tested.
- **Background processes** — `rm -rf /tmp/x &` parsed normally; the `&` is a stmt terminator. Handled.
- **Custom shells** — fish, ksh, busybox-ash with `-c` are unwrapped same way. Bash-only constructs in fish source may parse differently — ask if mvdan/sh raises.
- **Symlink trailing-slash race** — between `lstat()` time and bash's actual `unlink`/`rmdir` syscall, the symlink could be replaced. We accept this race; the user-permission dialog adds another layer.

---

## Appendix A: research references

- Claude Code hook docs: [code.claude.com/docs/en/hooks](https://code.claude.com/docs/en/hooks). Hooks run regardless of permission mode (including `--dangerously-skip-permissions`). We use only `allow` and `ask`.
- mvdan/sh Go bash parser: [github.com/mvdan/sh](https://github.com/mvdan/sh). Active, used by `shfmt`, full POSIX + bash extensions support.
- `destructive_command_guard` reference impl: [Dicklesworthstone/destructive_command_guard](https://github.com/Dicklesworthstone/destructive_command_guard) — span-classification approach this design borrows.
- `safe-rm` family: shell-safe-rm, careful_rm, trash-cli — useful for the safe-paths list.
- POSIX rm(1): https://pubs.opengroup.org/onlinepubs/9699919799/utilities/rm.html
