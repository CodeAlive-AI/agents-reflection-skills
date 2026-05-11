#!/usr/bin/env bash
set -euo pipefail

REPO="CodeAlive-AI/ai-driven-development"
SKILL_NAME="refactoring-csharp"
SKILL_ASSET="refactoring-csharp-skill.tar.gz"

install_codex=1
install_claude=1
with_binary=1
source_dir=""

usage() {
  cat <<'EOF'
Usage: install.sh [--codex] [--claude] [--no-binary] [--source PATH]

Default: install to both ~/.codex/skills/refactoring-csharp and
~/.claude/skills/refactoring-csharp, then install the matching prebuilt binary
when a release asset is available.

Environment:
  REFACTORING_CSHARP_VERSION=refactoring-csharp-vX.Y.Z
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --codex) install_codex=1; install_claude=0 ;;
    --claude) install_claude=1; install_codex=0 ;;
    --all) install_codex=1; install_claude=1 ;;
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
  trap 'rm -rf "$tmp"' RETURN

  curl -fsSL "https://github.com/${REPO}/releases/download/${tag}/${SKILL_ASSET}" \
    -o "$tmp/${SKILL_ASSET}"
  rm -rf "$dest"
  mkdir -p "$dest"
  tar -xzf "$tmp/${SKILL_ASSET}" -C "$dest" --strip-components=1
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
  trap 'rm -rf "$tmp"' RETURN
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
}

main() {
  require curl
  require tar

  local tag destinations=()
  if [[ "$install_codex" == 1 ]]; then
    destinations+=("$HOME/.codex/skills/${SKILL_NAME}")
  fi
  if [[ "$install_claude" == 1 ]]; then
    destinations+=("$HOME/.claude/skills/${SKILL_NAME}")
  fi

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
  echo "Done. Restart the agent if this is a new skill installation."
}

main
