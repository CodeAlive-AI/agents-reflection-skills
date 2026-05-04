#!/usr/bin/env bash
# install.sh — idempotent installer for bash-guard.
#
# What it does:
#   1. Verifies Go is installed (>= 1.21).
#   2. Creates a symlink at ~/.claude/hooks/bash-guard pointing at this src/.
#   3. Triggers a first build (warms Go cache).
#   4. Patches ~/.claude/settings.json to add the bash-guard hook entry,
#      preserving the existing hooks. Uses jq for JSON-aware editing.
#
# Re-running is safe: the symlink is recreated, the build is a no-op, and
# the settings.json patch is a no-op when our entry already exists.
#
# Modes:
#   --shadow    Add hook with BASH_GUARD_SHADOW=1 (logs only, never blocks).
#               This is the default for first-time installation.
#   --dry-run   Add hook with BASH_GUARD_DRY_RUN=1 (logs `would_decide`).
#   --live      Add hook with no env override (real enforcement).
#   --uninstall Remove our hook entry from settings.json AND delete the symlink.

set -euo pipefail

usage() {
    cat <<EOF
Usage: $0 [--shadow|--dry-run|--live|--uninstall]

Default mode: --shadow (always-allow + log everything).
EOF
}

mode="shadow"
replace_legacy=0
for arg in "$@"; do
    case "$arg" in
        --shadow)         mode="shadow" ;;
        --dry-run)        mode="dry-run" ;;
        --live)           mode="live" ;;
        --uninstall)      mode="uninstall" ;;
        --replace-legacy) replace_legacy=1 ;;
        -h|--help)        usage; exit 0 ;;
        *) echo "Unknown arg: $arg"; usage; exit 2 ;;
    esac
done

REPO_SRC_DIR="$(cd -- "$(dirname -- "$0")" && pwd)/src"
HOOK_DIR="$HOME/.claude/hooks/bash-guard"
SETTINGS="$HOME/.claude/settings.json"

require_jq() {
    if ! command -v jq >/dev/null 2>&1; then
        echo "error: jq is required for safe settings.json editing" >&2
        echo "install:  brew install jq" >&2
        exit 1
    fi
}

require_go() {
    if ! command -v go >/dev/null 2>&1; then
        if [[ -x /opt/homebrew/bin/go ]]; then
            export PATH="/opt/homebrew/bin:$PATH"
        else
            echo "error: go toolchain not found" >&2
            echo "install: brew install go" >&2
            exit 1
        fi
    fi
}

backup_settings() {
    if [[ -f "$SETTINGS" ]]; then
        local ts
        ts="$(date +%Y%m%d-%H%M%S)"
        cp "$SETTINGS" "$SETTINGS.bak.$ts"
        echo "  backup: $SETTINGS.bak.$ts"
    fi
}

create_symlink() {
    if [[ -e "$HOOK_DIR" && ! -L "$HOOK_DIR" ]]; then
        echo "error: $HOOK_DIR exists and is not a symlink." >&2
        echo "       Move/remove it manually before installing." >&2
        exit 1
    fi
    if [[ -L "$HOOK_DIR" ]]; then
        local current
        current="$(readlink "$HOOK_DIR")"
        if [[ "$current" != "$REPO_SRC_DIR" ]]; then
            echo "  replacing existing symlink ($current -> $REPO_SRC_DIR)"
            rm "$HOOK_DIR"
        else
            # Explicit return 0 — without it, `return` inherits the exit
            # status of the preceding `[[ ... ]]` test (1 when paths match)
            # and `set -e` then kills the script silently.
            return 0
        fi
    fi
    mkdir -p "$(dirname "$HOOK_DIR")"
    ln -s "$REPO_SRC_DIR" "$HOOK_DIR"
    echo "  linked: $HOOK_DIR -> $REPO_SRC_DIR"
}

first_build() {
    ( cd "$REPO_SRC_DIR" && go build -o bash_guard.bin . )
    echo "  built: $REPO_SRC_DIR/bash_guard.bin"
}

# Build the JSON snippet for our hook entry. Mode determines env vars.
# Claude Code passes the command through `sh -c`, so env-var prefix works
# verbatim. We point directly at the .bin to avoid a wrapper layer that
# costs ~50 ms per invocation; rebuilds are explicit (`make build`).
hook_entry_json() {
    local target='~/.claude/hooks/bash-guard/bash_guard.bin'
    local entry
    case "$mode" in
        shadow)  entry="{\"type\":\"command\",\"command\":\"BASH_GUARD_SHADOW=1 $target\"}" ;;
        dry-run) entry="{\"type\":\"command\",\"command\":\"BASH_GUARD_DRY_RUN=1 $target\"}" ;;
        live)    entry="{\"type\":\"command\",\"command\":\"$target\"}" ;;
    esac
    printf '%s' "$entry"
}

patch_settings_install() {
    require_jq
    backup_settings
    [[ -f "$SETTINGS" ]] || echo '{}' > "$SETTINGS"

    local hook_entry
    hook_entry="$(hook_entry_json)"

    # 1. Make sure hooks.PreToolUse exists.
    # 2. Find or create the {matcher: "Bash", hooks: [...]} block.
    # 3. Drop any existing bash-guard entries (idempotent re-install) and
    #    append our current one.
    local tmp
    tmp="$(mktemp)"
    jq --argjson entry "$hook_entry" '
      .hooks //= {} |
      .hooks.PreToolUse //= [] |
      .hooks.PreToolUse |=
        ( map( if .matcher == "Bash" then
                 .hooks //= [] |
                 .hooks |= ( map(select((.command // "") | test("bash-guard") | not)) + [$entry] )
               else . end ) ) |
      # If no Bash matcher block existed at all, add a new one.
      ( if any(.hooks.PreToolUse[]?; .matcher == "Bash") then .
        else .hooks.PreToolUse += [{"matcher":"Bash","hooks":[$entry]}] end )
    ' "$SETTINGS" > "$tmp"
    mv "$tmp" "$SETTINGS"
    echo "  patched: $SETTINGS"
}

# Remove legacy shell-hook entries that bash-guard now supersedes.
# Files on disk are NOT deleted — only the settings.json references.
# Easy rollback: restore from $SETTINGS.bak.<timestamp>.
patch_settings_remove_legacy() {
    require_jq
    [[ -f "$SETTINGS" ]] || return
    local legacy_pattern='safety-net-ask|validate-rm|supabase-safety|bw-permission-check|docker-prune-permission|infra-safety'
    local tmp
    tmp="$(mktemp)"
    jq --arg pat "$legacy_pattern" '
      if .hooks.PreToolUse then
        .hooks.PreToolUse |=
          map( if .matcher == "Bash" then
                 .hooks |= map(select((.command // "") | test($pat) | not))
               else . end )
      else . end
    ' "$SETTINGS" > "$tmp"
    mv "$tmp" "$SETTINGS"
    echo "  removed legacy shell-hook entries from $SETTINGS"
}

patch_settings_uninstall() {
    require_jq
    [[ -f "$SETTINGS" ]] || return
    backup_settings
    local tmp
    tmp="$(mktemp)"
    jq '
      if .hooks.PreToolUse then
        .hooks.PreToolUse |=
          map( if .matcher == "Bash" then
                 .hooks |= map(select((.command // "") | test("bash-guard") | not))
               else . end )
      else . end
    ' "$SETTINGS" > "$tmp"
    mv "$tmp" "$SETTINGS"
    echo "  removed bash-guard from $SETTINGS"
}

case "$mode" in
    shadow|dry-run|live)
        echo "Installing bash-guard ($mode mode)"
        require_go
        create_symlink
        first_build
        patch_settings_install
        if [[ "$replace_legacy" == 1 ]]; then
            patch_settings_remove_legacy
        fi
        echo
        echo "Done."
        echo "  Verify: jq '.hooks.PreToolUse' $SETTINGS"
        echo "  Selftest: $REPO_SRC_DIR/bash_guard.bin --selftest"
        ;;
    uninstall)
        echo "Uninstalling bash-guard"
        patch_settings_uninstall
        if [[ -L "$HOOK_DIR" ]]; then
            rm "$HOOK_DIR"
            echo "  removed symlink: $HOOK_DIR"
        fi
        echo "Done."
        ;;
esac
