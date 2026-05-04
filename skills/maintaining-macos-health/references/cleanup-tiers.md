# Cleanup tiers

Ten tiers, ordered by risk and reward. Always start at the lowest, only escalate if the goal isn't met. Each tier ends with a `df` checkpoint.

## Table of contents

- [Tier 1 — Trivial wins (~25 GB, zero risk)](#tier-1--trivial-wins-25-gb-zero-risk)
- [Tier 2 — Package manager caches (~10 GB)](#tier-2--package-manager-caches-10-gb)
- [Tier 3 — Electron caches (~4 GB)](#tier-3--electron-caches-4-gb)
- [Tier 4 — Stale IDE versions (~10 GB)](#tier-4--stale-ide-versions-10-gb)
- [Tier 5 — `~/Downloads` (~15–20 GB, interactive)](#tier-5--downloads-1520-gb-interactive)
- [Tier 6 — System logs and Logitech depots (sudo)](#tier-6--system-logs-and-logitech-depots-sudo-58-gb)
- [Tier 7 — `mo purge` for project artifacts](#tier-7--mo-purge-for-project-artifacts-3050-gb)
- [Tier 8 — Docker (~10 GB)](#tier-8--docker-10-gb)
- [Tier 9 — Dev artifacts (~5 GB, manual)](#tier-9--dev-artifacts-5-gb-manual)
- [Tier 10 — Discuss-first](#tier-10--discuss-first)
- [Reset prevention recipes](#reset-prevention-recipes)
- [After cleanup](#after-cleanup)

**Goal anchor:** scale to your disk size — typical targets are 20 % free for routine cleanup, 25–30 % free for memory-pressure prevention. The canonical incident recovered roughly 25 % of total capacity across tiers 1–9.

**Before any tier:** baseline + close apps that hold the targets:

```bash
df -h /System/Volumes/Data
date "+%Y-%m-%d %H:%M:%S"
# For tiers 3 (Electron caches) and 4 (JetBrains): close the apps first.
```

---

## Tier 1 — Trivial wins (~25 GB, zero risk)

All targets regenerate or are obviously stale. No state lost.

```bash
# Trash
osascript -e 'tell application "Finder" to empty trash' 2>/dev/null || rm -rf ~/.Trash/* 2>/dev/null

# Aerial wallpaper videos (~12 GB on most setups; macOS re-downloads on demand)
rm -rf ~/Library/Application\ Support/com.apple.wallpaper/aerials/videos/

# Warp autoupdate stale bundles
rm -rf ~/Library/Application\ Support/dev.warp.Warp-Stable/autoupdate/

# Old Claude Code CLI versions (keep current via $(readlink ~/.local/bin/claude))
CURRENT=$(basename "$(readlink ~/.local/bin/claude 2>/dev/null)")
for v in ~/.local/share/claude/versions/*/; do
  name=$(basename "$v")
  [ -n "$CURRENT" ] && [ "$name" != "$CURRENT" ] && rm -rf "$v"
done

# Codex stale logs (NOT sessions — those are chat history)
rm -rf ~/.codex/log
[ -f ~/.codex/logs_2.sqlite ] && rm ~/.codex/logs_2.sqlite

# Zed hang traces
rm -rf ~/Library/Application\ Support/Zed/hang_traces

# Cached extension VSIXs (Antigravity / Cursor / VS Code)
rm -rf ~/Library/Application\ Support/Antigravity/CachedData \
       ~/Library/Application\ Support/Cursor/CachedExtensionVSIXs \
       ~/Library/Application\ Support/Code/CachedExtensionVSIXs

# Orphan app data — apps removed, data left behind.
# Find candidates: list every app data dir whose name has no matching .app in /Applications.
# Then remove the ones for apps you remember uninstalling. Sample pattern:
for d in <bundle-name-or-app-folder>; do
  test -d ~/Library/Application\ Support/"$d" && rm -rf ~/Library/Application\ Support/"$d"
done
# Tip: `mo uninstall <app>` does this systematically (12+ trace locations) for any app.
# Tip: `mo analyze` highlights large Application Support folders for inspection.
```

---

## Tier 2 — Package manager caches (~10 GB)

All regenerate on next build. Use the tool's own cleanup command when available — they handle index integrity better than `rm`.

```bash
# npm npx (per-invocation packages — heavy)
rm -rf ~/.npm/_npx

# Playwright/Puppeteer old browser versions
# 1. List what's installed:
ls ~/Library/Caches/ms-playwright/ 2>/dev/null
ls ~/Library/Caches/ms-playwright-go/ 2>/dev/null
# 2. Pick which versions to keep (usually the latest only); replace OLDVER below with
#    the version numbers from the listing above. Example:
#      rm -rf ~/Library/Caches/ms-playwright/chromium-1208 \
#             ~/Library/Caches/ms-playwright/chromium_headless_shell-1208
# 3. Puppeteer cache (regenerable on next puppeteer install):
rm -rf ~/.cache/puppeteer

# NuGet HTTP cache (regenerates on next dotnet restore)
dotnet nuget locals http-cache --clear 2>/dev/null || rm -rf ~/.local/share/NuGet/http-cache

# Gradle
rm -rf ~/.gradle/wrapper/dists ~/.gradle/jdks/*.tar.gz ~/.gradle/jdks/*.zip

# Cargo source tarballs
rm -rf ~/.cargo/registry/src

# Bun
command -v bun >/dev/null && bun pm cache rm

# opencode (logs only — NOT opencode.db chat history)
rm -rf ~/.cache/opencode/packages ~/.cache/oh-my-opencode
rm -rf ~/.local/share/opencode/log

# Homebrew
brew cleanup -s --prune=all
rm -rf "$(brew --cache)"

# .NET old SDK (only if newer same-major exists)
ls ~/.dotnet/sdk/  # confirm before removing
# rm -rf ~/.dotnet/sdk/8.0.400  # keep 8.0.401+
```

---

## Tier 3 — Electron caches (~4 GB)

⚠️ **Quit the apps first.** While running, they regenerate cache mid-write and may glitch.

```bash
for app in \
  ~/Library/Application\ Support/Slack \
  ~/Library/Application\ Support/Notion/Partitions/notion \
  ~/Library/Application\ Support/Notion/Partitions/meeting-notification \
  ~/Library/Application\ Support/Notion\ Mail/Partitions/notionmail \
  ~/Library/Application\ Support/Arc/User\ Data/Default \
  ~/Library/Application\ Support/Google/Chrome/Default \
  ~/Library/Application\ Support/Cursor \
  ~/Library/Application\ Support/Antigravity \
  ~/Library/Application\ Support/Code \
  ~/Library/Application\ Support/Linear \
  ~/Library/Application\ Support/MongoDB\ Compass \
  ~/Library/Application\ Support/Claude \
  ~/Library/Application\ Support/Granola; do
  for sub in "Cache" "Code Cache" "GPUCache" "DawnCache" "DawnGraphiteCache" \
             "DawnWebGPUCache" "Service Worker/CacheStorage" \
             "GrShaderCache" "ShaderCache" "GraphiteDawnCache"; do
    rm -rf "${app}/${sub}" 2>/dev/null
  done
done
```

⚠️ Do NOT delete `IndexedDB`, `Local Storage`, `Cookies`, or any path inside `tdata/` (Telegram), `db/0-stable/` (Zed), `File System/` (Granola). Those are user state.

---

## Tier 4 — Stale IDE versions (~10 GB)

For JetBrains: if Toolbox is the only thing in `/Applications` and old major.minor version directories exist in `~/Library/Application Support/JetBrains/` (e.g. `Rider2024.3` while `Rider2025.1` is current), the older directories are stale.

```bash
# 1. Confirm what IDE apps are actually installed
ls /Applications | grep -iE "intellij|webstorm|pycharm|phpstorm|rider|datagrip|goland|clion|rubymine"

# 2. List all JetBrains data dirs and identify stale ones
ls ~/Library/Application\ Support/JetBrains/

# 3. Remove ONLY the stale major.minor directories you confirmed.
#    Example pattern (replace YYYY.M with the actual version strings to remove):
#      rm -rf ~/Library/Application\ Support/JetBrains/Rider2024.3
#      rm -rf ~/Library/Application\ Support/JetBrains/IntelliJIdea2024.3

# Bonus: caches and indexes for current versions (re-index on next launch — slow but safe)
rm -rf ~/Library/Caches/JetBrains/*/caches \
       ~/Library/Caches/JetBrains/*/index \
       ~/Library/Caches/JetBrains/*/resharper-host

# Logs across all versions
rm -rf ~/Library/Logs/JetBrains/*
```

If user doesn't use JetBrains at all → full removal (~15 GB):

```bash
# Stop autostart
launchctl unload ~/Library/LaunchAgents/com.jetbrains.toolbox.plist 2>/dev/null
osascript -e 'tell application "JetBrains Toolbox" to quit' 2>/dev/null
sleep 1
pkill -f "jetbrains-toolbox|jetbrainsd" 2>/dev/null

rm -rf "/Applications/JetBrains Toolbox.app"
rm -rf ~/Library/Application\ Support/JetBrains \
       ~/Library/Caches/JetBrains \
       ~/Library/Logs/JetBrains
rm -f ~/Library/Preferences/com.jetbrains.*.plist \
      ~/Library/Preferences/jetbrains.*.plist
rm -rf ~/Library/Saved\ Application\ State/com.jetbrains.*.savedState
rm -f ~/Library/LaunchAgents/com.jetbrains.toolbox.plist
```

---

## Tier 5 — `~/Downloads` (~15–20 GB, interactive)

Largest variable category. Show user the breakdown first.

```bash
du -d1 -h ~/Downloads | sort -h | tail -15
find ~/Downloads -maxdepth 1 -type f -size +50M -exec stat -f "%z %Sm %N" -t "%Y-%m-%d" {} \; | sort -rn | head -30
```

Categories to propose for deletion:
1. **Distros that already have a `.dmg` next to them** — keep the dmg, delete the extracted folder. Example: `AutoCAD2026_mac_extracted` next to `Autodesk.AutoCAD.2026.macOS.dmg`.
2. **`.dmg/.pkg/.iso/.zip` >30 days** — installed once, no longer needed:
   ```bash
   find ~/Downloads -maxdepth 1 -type f \
     \( -name "*.dmg" -o -name "*.pkg" -o -name "*.iso" -o -name "*.zip" \) \
     -mtime +30 ! -iname "*<UserKeepPattern>*" -delete
   ```
3. **Old recordings** (`.webm`, `.mp4`, `GMT*Recording*`, `Запись*`) >60 days.
4. **Telegram Desktop folder** — files older than 90 days are usually safe (still in Telegram cloud):
   ```bash
   find ~/Downloads/Telegram\ Desktop -type f -mtime +90 -delete
   find ~/Downloads/Telegram\ Desktop -mindepth 1 -type d -empty -delete
   ```
5. **Cloned repo archives** like `flutter-master`, `react-main`, `*-master.zip` — usually one-off look-ups.

⚠️ Always exclude active install media. Always show the list before delete.

---

## Tier 6 — System logs and Logitech depots (sudo, ~5–8 GB)

```bash
sudo -v  # cache password

# Logitech Options+ depots (keep latest subfolder)
LATEST=$(sudo ls -t /Library/Application\ Support/Logi/LogiOptionsPlus/depots/ 2>/dev/null | head -1)
for d in $(sudo ls /Library/Application\ Support/Logi/LogiOptionsPlus/depots/ 2>/dev/null); do
  [ "$d" != "$LATEST" ] && sudo rm -rf "/Library/Application Support/Logi/LogiOptionsPlus/depots/$d"
done

# Diagnostic logs >7 days
sudo find /private/var/db/diagnostics -type f -mtime +7 -delete 2>/dev/null
sudo find /private/var/db/DiagnosticPipeline -type f -mtime +7 -delete 2>/dev/null
sudo find /private/var/db/powerlog -type f -mtime +7 -delete 2>/dev/null
sudo find /private/var/db/reportmemoryexception/MemoryLimitViolations -type f -mtime +30 -delete 2>/dev/null

# DiagnosticReports >7 days
sudo find /Library/Logs/DiagnosticReports -maxdepth 1 -type f -mtime +7 -delete 2>/dev/null

# System logs >7 days
sudo find /private/var/log -maxdepth 3 -type f \
  \( -name "*.log" -o -name "*.gz" -o -name "*.asl" \) \
  -mtime +7 -delete 2>/dev/null
```

⚠️ Do NOT delete `/private/var/db/uuidtext` — that's symbol cache. Removing it breaks symbolication of any future crash.

---

## Tier 7 — `mo purge` for project artifacts (~30–50 GB)

This is the highest-reward tier on a developer machine. Mole already has the marker→target map and safety guards (see `mole-techniques.md`).

```bash
mo purge
```

Interactive menu — user picks. Mole's defaults:
- Only artifacts ≥ 7 days unmodified are pre-selected.
- bin/ only purged if parent has `.csproj`/`.fsproj`/`.vbproj` AND `Debug/Release` subdirs (avoids deleting Go binaries).
- vendor/ only purged for PHP Composer.
- Global `~/Library/Developer/Xcode/DerivedData` is protected (project-local DerivedData is fair game).

**Customize scan paths** if defaults miss something:
```bash
mo purge --paths   # opens config in $EDITOR
# Default: ~/www, ~/dev, ~/Projects, ~/GitHub, ~/Code, ~/Workspace, ~/Repos, ~/Development
# Add JetBrains-style dirs and any custom workspace roots, e.g.:
# ~/IdeaProjects, ~/PycharmProjects, ~/RiderProjects, ~/WebstormProjects, ~/work, ~/clients, etc.
```

The 47 GB freed in the canonical incident came from this single command across 15 scan paths.

---

## Tier 8 — Docker (~10 GB)

```bash
docker system df
docker system df -v   # detail per image and volume
```

Targeted (preserve running stacks):

```bash
# Unused images
docker rmi mcr.microsoft.com/playwright/dotnet:vN.N.N-noble  # if 0 containers

# Sprawl in tags (e.g. multiple mongo versions)
docker rmi mongo:7 mongo:7.0 mongo:8 mongo:8.2.3   # keep current

# Dead buildx builders
docker buildx ls
docker buildx rm <dead-builder-name>
docker volume rm buildx_buildkit_<dead-builder-name>_state
# If volume is in use:
docker stop <container_id> && docker rm <container_id>

# Orphan volumes (no associated container)
docker volume ls --filter dangling=true
docker volume rm <orphan_name>

# Build cache
docker builder prune -af
```

⚠️ NEVER `docker system prune -af --volumes` without listing volumes first — it deletes data volumes (mongodb_data, postgres data, etc.) without confirmation.

---

## Tier 9 — Dev artifacts (~5 GB, manual)

For projects not covered by `mo purge` (or where you want finer control). Always check `git status` first to ensure no uncommitted state, and don't delete `.env` files inside venvs/etc.

```bash
cd /path/to/project

# Multiple venvs sometimes coexist (e.g. venv, .venv, test_venv)
ls -d *venv*

# Remove regenerable
rm -rf venv .venv test_venv .venv-cgc .venv-scip-tools .venv-metrics-tools
rm -rf node_modules
rm -rf target build dist .next .nuxt .turbo .parcel-cache
find . -maxdepth 4 \( -name "__pycache__" -o -name ".pytest_cache" -o -name ".mypy_cache" -o -name "coverage" \) -mtime +30 -prune -exec rm -rf {} +
```

For old projects (>1 year untouched), prefer archive to external SSD before delete:

```bash
DEST=/Volumes/EXTERNAL_SSD
tar -czf "$DEST/$(basename "$PWD")-archive-$(date +%Y%m%d).tar.gz" -C "$(dirname "$PWD")" "$(basename "$PWD")" \
  && rm -rf "$PWD"
```

---

## Tier 10 — Discuss-first

Each item requires explicit user OK. Side effects are real.

```bash
# dotTrace/dotMemory saved profiling sessions
ls ~/.local/share/Workspaces/        # 21 saved sessions = 2.6 GB in canonical incident
# rm -rf ~/.local/share/Workspaces

# Maven local repository (re-downloads on next mvn build, but slow)
# rm -rf ~/.m2/repository

# Rust nightly toolchain (1.7 GB if not used)
rustup toolchain list
# rustup toolchain remove nightly-aarch64-apple-darwin

# Codex CLI runtimes (740 MB) — if Codex CLI not used
# rm -rf ~/.cache/codex-runtimes

# Homebrew large formulae review
du -shx /opt/homebrew/Cellar/* 2>/dev/null | sort -h | tail -10
# brew uninstall <formula>  if not needed

# Yandex.Disk / iCloud Drive / Dropbox local — switch to selective sync, don't rm
# Time Machine local snapshots (only if not actively backing up)
tmutil listlocalsnapshots /
# tmutil thinlocalsnapshots / 50000000000 4

# Parallels/UTM/VMware VMs on external volumes — user's content
ls -lh /Volumes/EXTERNAL/VMs/
```

---

## Reset prevention recipes

After any cleanup session, suggest these once-off changes to slow re-bloat:

```bash
# pnpm: deduplicate via global store with hardlinks
pnpm config set store-dir ~/.pnpm-store

# Gradle: stop downloading JDKs into ~/.gradle/jdks
echo "org.gradle.java.installations.auto-provisioning=false" >> ~/.gradle/gradle.properties

# JetBrains: less log noise (per IDE: Help → Edit Custom VM Options)
# Add: idea.log.level=WARN

# Docker quick-tidy alias
echo 'alias docker-tidy="docker container prune -f && docker image prune -f && docker builder prune -f"' >> ~/.zshrc

# Photos: Settings → Apple ID → iCloud → Photos → "Optimize Mac Storage" if not already
```

---

## After cleanup

1. Run final `df -h /System/Volumes/Data` and report delta.
2. If free space changed less than `du` reported deleted, wait — APFS purgeable lags.
3. Recommend installing the alerter (`alerting.md`) to prevent recurrence.
4. Recommend installing Stats (`brew install --cask stats`) for passive monitoring.
