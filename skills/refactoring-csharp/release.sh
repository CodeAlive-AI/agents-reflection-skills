#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 1 ]]; then
  echo "Usage: ./release.sh refactoring-csharp-vX.Y.Z" >&2
  exit 2
fi

TAG="$1"
case "$TAG" in
  refactoring-csharp-v*) ;;
  *) echo "error: tag must start with refactoring-csharp-v" >&2; exit 2 ;;
esac

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DIST_DIR="$SKILL_DIR/dist"
PROJECT="$SKILL_DIR/src/CSharpRefactoring.Cli/CSharpRefactoring.Cli.csproj"

rm -rf "$DIST_DIR"
mkdir -p "$DIST_DIR"

make_skill_archive() {
  tar \
    --exclude='./bin' \
    --exclude='./obj' \
    --exclude='./dist' \
    --exclude='./*.ps1xml' \
    --exclude='*/bin' \
    --exclude='*/obj' \
    -C "$SKILL_DIR" \
    -czf "$DIST_DIR/refactoring-csharp-skill.tar.gz" \
    .
}

publish_tar() {
  local rid="$1"
  local asset_platform="$2"
  local out="$DIST_DIR/publish/$rid"
  dotnet publish "$PROJECT" \
    -c Release \
    -r "$rid" \
    --self-contained true \
    -p:PublishSingleFile=true \
    -p:PublishTrimmed=false \
    -p:DebugType=None \
    -p:DebugSymbols=false \
    -o "$out"
  cp "$out/CSharpRefactoring.Cli" "$DIST_DIR/csharp-refactor"
  chmod +x "$DIST_DIR/csharp-refactor"
  tar -C "$DIST_DIR" -czf "$DIST_DIR/csharp-refactor-${asset_platform}.tar.gz" csharp-refactor
  rm "$DIST_DIR/csharp-refactor"
}

publish_zip() {
  local rid="$1"
  local asset_platform="$2"
  local out="$DIST_DIR/publish/$rid"
  dotnet publish "$PROJECT" \
    -c Release \
    -r "$rid" \
    --self-contained true \
    -p:PublishSingleFile=true \
    -p:PublishTrimmed=false \
    -p:DebugType=None \
    -p:DebugSymbols=false \
    -o "$out"
  cp "$out/CSharpRefactoring.Cli.exe" "$DIST_DIR/csharp-refactor.exe"
  (cd "$DIST_DIR" && zip -q "csharp-refactor-${asset_platform}.zip" csharp-refactor.exe)
  rm "$DIST_DIR/csharp-refactor.exe"
}

make_skill_archive
publish_tar osx-arm64 darwin-arm64
publish_tar osx-x64 darwin-x64
publish_tar linux-arm64 linux-arm64
publish_tar linux-x64 linux-x64
publish_zip win-x64 win-x64

(
  cd "$DIST_DIR"
  shasum -a 256 \
    refactoring-csharp-skill.tar.gz \
    csharp-refactor-darwin-arm64.tar.gz \
    csharp-refactor-darwin-x64.tar.gz \
    csharp-refactor-linux-arm64.tar.gz \
    csharp-refactor-linux-x64.tar.gz \
    csharp-refactor-win-x64.zip \
    > SHA256SUMS
)

rm -rf "$DIST_DIR/publish"

echo "Release assets created in $DIST_DIR"
