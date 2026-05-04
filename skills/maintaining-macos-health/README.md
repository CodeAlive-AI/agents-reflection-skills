# maintaining-macos-health

Recovery and prevention playbook for macOS disk and memory crises. Tiered cleanup playbook plus a noise-resistant LaunchAgent alerter that catches the early warning signs of compressor saturation before they turn into a kernel panic. Built for Apple Silicon dev machines that run heavy workloads — Docker, multiple AI tools, IDEs, browsers.

## Why this skill

Modern macOS dev machines hit a specific failure mode that's not covered well anywhere else: a **watchdog-timeout kernel panic** caused by `vm_compressor` segments saturating to 100 % while the disk is too full to extend swap. The symptom is "Mac freezes for ~90 seconds, then reboots." The signal that always precedes it is `JetsamEvent` files containing `vm-compressor-space-shortage` — Apple's kernel killing processes for memory minutes before it gives up.

This skill captures the full recovery playbook (validated against a real incident that recovered ~25 % of total disk capacity) plus an alerter designed to catch that signal early, with **three CRITICAL-only triggers**, hysteresis, cooldown, and a 7-day calibration window so it doesn't cry wolf.

## Install

```bash
npx skills add CodeAlive-AI/ai-driven-development@maintaining-macos-health -g -y
```

## Prerequisites

| Tool | Why | Install |
|---|---|---|
| [Mole](https://github.com/tw93/mole) (`mo`) | Safety floor for cleanup — marker-based project artifact detection (`mo purge`), system cache cleanup (`mo clean`), thorough app uninstall (`mo uninstall`) | `brew install mole` |
| [alerter](https://github.com/vjeantet/alerter) | macOS notifications from launchd (replaces dead `terminal-notifier`) | `brew install vjeantet/tap/alerter` |
| [Stats](https://github.com/exelban/stats) (recommended) | Passive menubar monitoring (memory pressure, disk, swap) | `brew install --cask stats` |

Apple Silicon Mac running macOS Sequoia (15.x) or Tahoe (26.x) recommended. Bash 3.2 (Apple-shipped) is the minimum — no Homebrew bash required.

## Quick start

The skill is consulted by an agent when the user reports macOS health trouble. Typical flows:

```text
# Free space NOW (incident response)
"My Mac is full" / "out of disk space" / kernel panic happened
  → agent reads triage.md, identifies signal, runs cleanup-tiers.md tier 1→N

# Set up alerting on a new machine
"set up disk alert" / "monitor memory pressure" / restoring after macOS reinstall
  → agent reads alerting.md, copies assets/ files to ~/bin and ~/Library/LaunchAgents

# Audit storage
"what's eating my disk?" / "audit storage"
  → agent runs Mole's `mo analyze`, then suggests targeted tier from cleanup-tiers.md
```

Manual install of the alerter (without the agent):

```bash
SKILL=$HOME/.claude/skills/maintaining-macos-health
mkdir -p ~/bin ~/.config/mac-health ~/Library/Logs/mac-health ~/.local/state/mac-health
cp "$SKILL/assets/mac-health-check"          ~/bin/
cp "$SKILL/assets/config.sh"                 ~/.config/mac-health/
sed "s|__HOME__|$HOME|g" "$SKILL/assets/com.local.mac-health-check.plist" \
  > ~/Library/LaunchAgents/com.local.mac-health-check.plist
chmod +x ~/bin/mac-health-check
launchctl load -w ~/Library/LaunchAgents/com.local.mac-health-check.plist
```

## What it does

The skill packages two complementary capabilities:

| Capability | Entry point | Use |
|---|---|---|
| **Triage + cleanup playbook** | `references/triage.md`, `references/cleanup-tiers.md`, `references/never-touch.md`, `references/mole-techniques.md` | Tells the agent how to classify a health signal, which 10-tier cleanup block to run, and what categories to never touch |
| **Active alerter** | `references/alerting.md` + `assets/{mac-health-check, config.sh, com.local.mac-health-check.plist}` | Bash + launchd implementation. 3 CRITICAL-only triggers with hysteresis, cooldown, calibration window |

### Triage flow (signal classification)

Read `references/triage.md`. First-five-minutes decision tree:

- **Disk-driven** (most common): `df` < 20 % free → run cleanup tiers
- **Memory-driven**: `memory_pressure` ≠ Normal + sustained swap → check Docker memory limit
- **Kernel-panic / watchdog-timeout**: parse panic file, identify top-RSS process, install alerter
- **JetsamEvent with `vm-compressor-space-shortage`**: imminent panic — close apps, do not run heavy cleanup
- **Thermal**: powermetrics, let it cool

### Cleanup tiers (10 levels, risk-ordered)

Read `references/cleanup-tiers.md`. Each tier ends with a `df` checkpoint so the agent knows when to stop:

1. **Trivial wins** (~25 GB) — Aerial wallpapers, Trash, Warp updates, orphan app data, hang traces, cached extension VSIXs
2. **Package manager caches** (~10 GB) — npm `_npx`, Playwright, Puppeteer, NuGet, Gradle, Cargo, brew cleanup
3. **Electron caches** (~4 GB) — Slack, Notion, Arc, Cursor, etc. (Quit apps first)
4. **Stale IDE versions** (~10 GB) — JetBrains old major.minor data dirs
5. **`~/Downloads`** (~15-20 GB, interactive) — installers, recordings, archived repos
6. **System logs + vendor depots** (sudo, ~5-8 GB) — `/private/var/db/diagnostics`, Logitech depots
7. **`mo purge`** (~30-50 GB) — project artifacts via Mole's marker-based detection
8. **Docker** (~10 GB) — unused images, dead builders, orphan volumes
9. **Dev artifacts** (~5 GB, manual) — venvs, node_modules in inactive projects
10. **Discuss-first** — Maven repo, Rust nightly, dotTrace workspaces, etc.

### Active alerter (3 CRITICAL-only triggers)

Read `references/alerting.md`. Runs every 5 min via `StartCalendarInterval`. Triggers:

1. **Disk free < 10 %** for 3 consecutive readings (15 min sustained)
2. **Memory pressure Critical AND swap > 8 GB** for 3 consecutive readings
3. **New `JetsamEvent-*.ips` containing `vm-compressor-space-shortage`** (immediate, no hysteresis — this is the early-warning signal)

Plus: 30-min cooldown between repeats, 7-day calibration window (logs only, no notifications), `~/.config/mac-health/silent` flag for manual suppression during heavy work, optional `ntfy.sh` URL for phone push.

## Key features

- **Mole-grounded safety** — adopts Mole's path validator (`/System`, `/bin`, `/usr` blocked even under sudo; specific `/private/...` subpaths allowlisted), `.NET-only bin/` guard, PHP-only `vendor/` guard, mtime ≥ 7 days for cache deletions
- **Never-touch list** — explicit blacklist with consequence notes: `com.apple.coreaudio` (Mole issue #553), `com.apple.controlcenter*` (issue #136), `org.cups.*` (issue #731 — wipes saved printers), AI/password/VPN/keychain bundle IDs, `Telegram tdata`, `Granola transcripts`, Claude `vm_bundles`, etc.
- **Three CRITICAL-only triggers** — Google SRE alert-fatigue principles: every alert requires intelligence to resolve. Disk free, memory pressure + swap, JetsamEvent compressor shortage. No warnings, no hints, no auto-cleanup actions.
- **2026 macOS quirks captured** — `terminal-notifier` is dead (last release 2019-11), use `alerter`. `StartInterval` clock pauses during sleep on laptops (radar 6630231), use `StartCalendarInterval` with explicit minute-entries. LaunchAgent default `PATH` does not include `/opt/homebrew/bin`, must declare in plist. `osascript display notification` from launchd attributes to Script Editor and is unreliable.
- **Bash 3.2 compatible** — runs against Apple-shipped `/bin/bash` 3.2.57 with no `set -u` quirks. Label-aware `awk` parsing for `vm.swapusage` (survives field-position changes).
- **File-polling JetsamEvent** — `log show --last 6m` is too slow (30+ s) on a busy machine; polling `/Library/Logs/DiagnosticReports/JetsamEvent-*.ips` has acceptable async-write latency on a 5-min cadence.

## Sources and methodology

- **Apple TN3155** — Reading a kernel panic, panic JSON layout, Compressor Info interpretation
- **Apple developer docs** — [Identifying high-memory use with Jetsam Event Reports](https://developer.apple.com/documentation/xcode/identifying-high-memory-use-with-jetsam-event-reports)
- **xnu vm_compressor** — segments-vs-pages distinction, `vm-compressor-space-shortage` reason code
- **Mole** ([github.com/tw93/mole](https://github.com/tw93/mole)) — battle-tested cleanup safety guards (path validator, project-artifact marker→target map, age thresholds, protected app bundle list)
- **Google SRE Workbook** — alert-fatigue prevention, "every alert must require intelligence to resolve"
- **alerter** ([github.com/vjeantet/alerter](https://github.com/vjeantet/alerter)) — Swift-based notification CLI that works in launchd background context (issue #259 of `terminal-notifier` documents the failure mode being avoided)
- **launchd quirks** — radar 6630231 documents `StartInterval` clock-pause during sleep
- **Real-incident validation** — recovered ~25 % of total disk capacity on a single Apple Silicon Mac across the 10 cleanup tiers; alerter verified via synthetic disk-trigger test

## File structure

```
skills/maintaining-macos-health/
├── README.md                       # this file
├── SKILL.md                        # agent-facing entry point with workflows
├── references/
│   ├── triage.md                   # First 5 min: signal classification + decision tree
│   ├── cleanup-tiers.md            # 10 risk-ordered cleanup tiers, copy-paste-safe
│   ├── never-touch.md              # Hard-protected categories with consequence notes
│   ├── mole-techniques.md          # Marker→target map, safety guards to borrow
│   └── alerting.md                 # Alerter design + install + troubleshoot
└── assets/
    ├── mac-health-check            # Bash 3.2-compatible health-check script
    ├── config.sh                   # Default thresholds (sourced by the script)
    └── com.local.mac-health-check.plist   # LaunchAgent (uses __HOME__ placeholder)
```

## License

MIT
