#!/usr/bin/env bash
set -euo pipefail

REPO="CodeAlive-AI/ai-driven-development"
SKILL_NAME="refactoring-csharp"
SKILL_ASSET="refactoring-csharp-skill.tar.gz"

with_binary=1
source_dir=""
selected_agents=()
all_agents=0
detected_agents=0

AGENT_IDS=(
  adal amp antigravity augment claude-code cline codebuddy codex command-code
  continue crush cursor droid gemini-cli github-copilot goose iflow-cli junie
  kilo kimi-cli kiro-cli kode mcpjam mistral-vibe mux neovate openclaw opencode
  openhands pi pochi qoder qwen-code replit roo trae trae-cn windsurf zencoder
)

usage() {
  cat <<'EOF'
Usage:
  install.sh [--agent ID ...] [--all-agents|--detected] [--no-binary] [--source PATH]

Defaults:
  Installs to Codex and Claude Code global skill directories:
    ~/.codex/skills/refactoring-csharp
    ~/.claude/skills/refactoring-csharp

Agent selection:
  --agent codex          Install to one agent. Repeat for multiple agents.
  --codex               Alias for --agent codex.
  --claude              Alias for --agent claude-code.
  --all                 Alias for --all-agents.
  --all-agents          Install to all supported global agent skill directories.
  --detected            Install to supported agents whose global config dir exists.

Environment:
  REFACTORING_CSHARP_VERSION=refactoring-csharp-vX.Y.Z

Supported agent IDs:
  adal amp antigravity augment claude-code cline codebuddy codex command-code
  continue crush cursor droid gemini-cli github-copilot goose iflow-cli junie
  kilo kimi-cli kiro-cli kode mcpjam mistral-vibe mux neovate openclaw opencode
  openhands pi pochi qoder qwen-code replit roo trae trae-cn windsurf zencoder
EOF
}

agent_skill_dir() {
  case "$1" in
    adal) echo "$HOME/.adal/skills/$SKILL_NAME" ;;
    amp) echo "$HOME/.config/agents/skills/$SKILL_NAME" ;;
    antigravity) echo "$HOME/.gemini/antigravity/skills/$SKILL_NAME" ;;
    augment) echo "$HOME/.augment/skills/$SKILL_NAME" ;;
    claude-code|claude) echo "$HOME/.claude/skills/$SKILL_NAME" ;;
    cline) echo "$HOME/.cline/skills/$SKILL_NAME" ;;
    codebuddy) echo "$HOME/.codebuddy/skills/$SKILL_NAME" ;;
    codex) echo "$HOME/.codex/skills/$SKILL_NAME" ;;
    command-code) echo "$HOME/.commandcode/skills/$SKILL_NAME" ;;
    continue) echo "$HOME/.continue/skills/$SKILL_NAME" ;;
    crush) echo "$HOME/.config/crush/skills/$SKILL_NAME" ;;
    cursor) echo "$HOME/.cursor/skills/$SKILL_NAME" ;;
    droid) echo "$HOME/.factory/skills/$SKILL_NAME" ;;
    gemini-cli|gemini) echo "$HOME/.gemini/skills/$SKILL_NAME" ;;
    github-copilot|copilot) echo "$HOME/.copilot/skills/$SKILL_NAME" ;;
    goose) echo "$HOME/.config/goose/skills/$SKILL_NAME" ;;
    iflow-cli|iflow) echo "$HOME/.iflow/skills/$SKILL_NAME" ;;
    junie) echo "$HOME/.junie/skills/$SKILL_NAME" ;;
    kilo) echo "$HOME/.kilocode/skills/$SKILL_NAME" ;;
    kimi-cli|kimi) echo "$HOME/.config/agents/skills/$SKILL_NAME" ;;
    kiro-cli|kiro) echo "$HOME/.kiro/skills/$SKILL_NAME" ;;
    kode) echo "$HOME/.kode/skills/$SKILL_NAME" ;;
    mcpjam) echo "$HOME/.mcpjam/skills/$SKILL_NAME" ;;
    mistral-vibe) echo "$HOME/.vibe/skills/$SKILL_NAME" ;;
    mux) echo "$HOME/.mux/skills/$SKILL_NAME" ;;
    neovate) echo "$HOME/.neovate/skills/$SKILL_NAME" ;;
    openclaw) echo "$HOME/.openclaw/skills/$SKILL_NAME" ;;
    opencode) echo "$HOME/.config/opencode/skills/$SKILL_NAME" ;;
    openhands) echo "$HOME/.openhands/skills/$SKILL_NAME" ;;
    pi) echo "$HOME/.pi/agent/skills/$SKILL_NAME" ;;
    pochi) echo "$HOME/.pochi/skills/$SKILL_NAME" ;;
    qoder) echo "$HOME/.qoder/skills/$SKILL_NAME" ;;
    qwen-code|qwen) echo "$HOME/.qwen/skills/$SKILL_NAME" ;;
    replit) echo "$HOME/.config/agents/skills/$SKILL_NAME" ;;
    roo) echo "$HOME/.roo/skills/$SKILL_NAME" ;;
    trae) echo "$HOME/.trae/skills/$SKILL_NAME" ;;
    trae-cn) echo "$HOME/.trae-cn/skills/$SKILL_NAME" ;;
    windsurf) echo "$HOME/.codeium/windsurf/skills/$SKILL_NAME" ;;
    zencoder) echo "$HOME/.zencoder/skills/$SKILL_NAME" ;;
    *) return 1 ;;
  esac
}

agent_config_dir() {
  case "$1" in
    adal) echo "$HOME/.adal" ;;
    amp|kimi-cli|replit) echo "$HOME/.config/agents" ;;
    antigravity) echo "$HOME/.gemini/antigravity" ;;
    augment) echo "$HOME/.augment" ;;
    claude-code) echo "$HOME/.claude" ;;
    cline) echo "$HOME/.cline" ;;
    codebuddy) echo "$HOME/.codebuddy" ;;
    codex) echo "$HOME/.codex" ;;
    command-code) echo "$HOME/.commandcode" ;;
    continue) echo "$HOME/.continue" ;;
    crush) echo "$HOME/.config/crush" ;;
    cursor) echo "$HOME/.cursor" ;;
    droid) echo "$HOME/.factory" ;;
    gemini-cli) echo "$HOME/.gemini" ;;
    github-copilot) echo "$HOME/.copilot" ;;
    goose) echo "$HOME/.config/goose" ;;
    iflow-cli) echo "$HOME/.iflow" ;;
    junie) echo "$HOME/.junie" ;;
    kilo) echo "$HOME/.kilocode" ;;
    kiro-cli) echo "$HOME/.kiro" ;;
    kode) echo "$HOME/.kode" ;;
    mcpjam) echo "$HOME/.mcpjam" ;;
    mistral-vibe) echo "$HOME/.vibe" ;;
    mux) echo "$HOME/.mux" ;;
    neovate) echo "$HOME/.neovate" ;;
    openclaw) echo "$HOME/.openclaw" ;;
    opencode) echo "$HOME/.config/opencode" ;;
    openhands) echo "$HOME/.openhands" ;;
    pi) echo "$HOME/.pi" ;;
    pochi) echo "$HOME/.pochi" ;;
    qoder) echo "$HOME/.qoder" ;;
    qwen-code) echo "$HOME/.qwen" ;;
    roo) echo "$HOME/.roo" ;;
    trae) echo "$HOME/.trae" ;;
    trae-cn) echo "$HOME/.trae-cn" ;;
    windsurf) echo "$HOME/.codeium/windsurf" ;;
    zencoder) echo "$HOME/.zencoder" ;;
    *) return 1 ;;
  esac
}

normalize_agent_id() {
  case "$1" in
    claude) echo "claude-code" ;;
    gemini) echo "gemini-cli" ;;
    copilot) echo "github-copilot" ;;
    iflow) echo "iflow-cli" ;;
    kimi) echo "kimi-cli" ;;
    kiro) echo "kiro-cli" ;;
    qwen) echo "qwen-code" ;;
    *) echo "$1" ;;
  esac
}

add_agent() {
  local id
  id="$(normalize_agent_id "$1")"
  if ! agent_skill_dir "$id" >/dev/null; then
    echo "error: unsupported agent id: $1" >&2
    exit 2
  fi
  selected_agents+=("$id")
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --agent|-a)
      shift
      if [[ $# -eq 0 || -z "${1:-}" ]]; then
        echo "error: --agent requires an ID" >&2
        exit 2
      fi
      add_agent "$1"
      ;;
    --agent=*) add_agent "${1#--agent=}" ;;
    --codex) add_agent codex ;;
    --claude) add_agent claude-code ;;
    --all|--all-agents) all_agents=1 ;;
    --detected) detected_agents=1 ;;
    --no-binary) with_binary=0 ;;
    --source)
      shift
      if [[ $# -eq 0 || -z "${1:-}" ]]; then
        echo "error: --source requires a path" >&2
        exit 2
      fi
      source_dir="$1"
      ;;
    --source=*) source_dir="${1#--source=}" ;;
    -h|--help) usage; exit 0 ;;
    *) echo "error: unknown arg: $1" >&2; usage; exit 2 ;;
  esac
  shift
done

require() {
  command -v "$1" >/dev/null 2>&1 || {
    echo "error: $1 is required" >&2
    exit 1
  }
}

resolve_tag() {
  if [[ -n "${REFACTORING_CSHARP_VERSION:-}" ]]; then
    echo "$REFACTORING_CSHARP_VERSION"
    return
  fi

  curl -fsSL "https://api.github.com/repos/${REPO}/releases?per_page=50" \
    | grep -oE '"tag_name":[[:space:]]*"refactoring-csharp-v[^"]*"' \
    | head -1 \
    | sed -E 's/.*"(refactoring-csharp-v[^"]*)"/\1/'
}

detect_platform() {
  local os arch
  os="$(uname -s | tr '[:upper:]' '[:lower:]')"
  arch="$(uname -m)"

  case "$os" in
    darwin|linux) ;;
    mingw*|msys*|cygwin*) os="win" ;;
    *) echo "error: unsupported OS: $os" >&2; exit 1 ;;
  esac

  case "$arch" in
    arm64|aarch64) arch="arm64" ;;
    x86_64|amd64) arch="x64" ;;
    *) echo "error: unsupported arch: $arch" >&2; exit 1 ;;
  esac

  echo "${os}-${arch}"
}

copy_skill_from_source() {
  local src="$1" dest="$2"
  rm -rf "$dest"
  mkdir -p "$dest"
  tar \
    --exclude='./bin' \
    --exclude='./obj' \
    --exclude='./dist' \
    --exclude='*/bin' \
    --exclude='*/obj' \
    -C "$src" -cf - . | tar -C "$dest" -xf -
}

install_skill_archive() {
  local tag="$1" dest="$2"
  local tmp
  tmp="$(mktemp -d)"

  curl -fsSL "https://github.com/${REPO}/releases/download/${tag}/${SKILL_ASSET}" \
    -o "$tmp/${SKILL_ASSET}"
  rm -rf "$dest"
  mkdir -p "$dest"
  tar -xzf "$tmp/${SKILL_ASSET}" -C "$dest" --strip-components=1
  rm -rf "$tmp"
}

install_binary() {
  local tag="$1" dest="$2"
  local platform asset archive tmp base binary_name
  platform="$(detect_platform)"
  binary_name="csharp-refactor"
  asset="csharp-refactor-${platform}.tar.gz"
  if [[ "$platform" == win-* ]]; then
    asset="csharp-refactor-${platform}.zip"
    binary_name="csharp-refactor.exe"
  fi

  tmp="$(mktemp -d)"
  base="https://github.com/${REPO}/releases/download/${tag}"
  archive="$tmp/$asset"

  curl -fsSL "$base/$asset" -o "$archive"
  curl -fsSL "$base/SHA256SUMS" -o "$tmp/SHA256SUMS"

  if command -v shasum >/dev/null 2>&1; then
    (cd "$tmp" && shasum -a 256 -c SHA256SUMS --ignore-missing >/dev/null)
  elif command -v sha256sum >/dev/null 2>&1; then
    (cd "$tmp" && sha256sum -c SHA256SUMS --ignore-missing >/dev/null)
  else
    echo "error: shasum or sha256sum is required for checksum verification" >&2
    exit 1
  fi

  mkdir -p "$dest/bin"
  case "$asset" in
    *.zip)
      require unzip
      unzip -q "$archive" -d "$tmp/bin"
      ;;
    *.tar.gz)
      tar -xzf "$archive" -C "$tmp"
      ;;
  esac

  mv "$tmp/$binary_name" "$dest/bin/$binary_name"
  chmod +x "$dest/bin/$binary_name"
  rm -rf "$tmp"
}

build_agent_list() {
  if [[ "$all_agents" == 1 ]]; then
    selected_agents=("${AGENT_IDS[@]}")
  elif [[ "$detected_agents" == 1 ]]; then
    selected_agents=()
    local id config_dir
    for id in "${AGENT_IDS[@]}"; do
      config_dir="$(agent_config_dir "$id")"
      if [[ -d "$config_dir" ]]; then
        selected_agents+=("$id")
      fi
    done
  elif [[ ${#selected_agents[@]} -eq 0 ]]; then
    selected_agents=(codex claude-code)
  fi
}

main() {
  require curl
  require tar

  build_agent_list

  local tag destinations=() id dest seen_destinations
  seen_destinations="
"
  for id in "${selected_agents[@]}"; do
    dest="$(agent_skill_dir "$id")"
    if [[ "$seen_destinations" != *"
$dest
"* ]]; then
      seen_destinations="${seen_destinations}${dest}
"
      destinations+=("$dest")
    fi
  done

  if [[ ${#destinations[@]} -eq 0 ]]; then
    echo "error: no destination selected" >&2
    exit 1
  fi

  tag=""
  if [[ -z "$source_dir" || "$with_binary" == 1 ]]; then
    tag="$(resolve_tag)"
  fi
  if [[ -z "$tag" && -z "$source_dir" ]]; then
    echo "error: no refactoring-csharp-v* release found in ${REPO}" >&2
    exit 1
  fi

  for dest in "${destinations[@]}"; do
    echo "Installing ${SKILL_NAME} -> ${dest}"
    if [[ -n "$source_dir" ]]; then
      copy_skill_from_source "$source_dir" "$dest"
    else
      install_skill_archive "$tag" "$dest"
    fi

    if [[ "$with_binary" == 1 && -n "$tag" ]]; then
      install_binary "$tag" "$dest"
      echo "  binary: ${dest}/bin/csharp-refactor"
    fi
  done

  echo
  echo "Done. Restart any agent that should discover this skill for the first time."
}

main
