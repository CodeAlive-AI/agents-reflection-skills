---
name: maintaining-macos-health
description: Hands-on playbook for macOS disk cleanup, dev-machine optimization, and proactive health alerting. Use when the Mac is full or slow, when a kernel panic / watchdog timeout / vm-compressor-space-shortage / Jetsam event happened, when the user asks to free disk space, audit storage, set up disk/memory alerts, or restore the same monitoring on a new Mac. Built around Mole (`mo` CLI) for safety guards plus a custom LaunchAgent-based alerter for active warnings. Covers Apple Silicon laptops with heavy AI/Docker workloads.
---

# Maintaining macOS Health

Recovery and prevention playbook for macOS disk and memory crises. Validated against a real watchdog-timeout kernel panic on Apple Silicon caused by `vm_compressor` segments saturated to 100 % with the disk over 90 % full. The same playbook works for routine cleanup or first-time setup on a new machine.

## Table of contents

- [When to use](#when-to-use)
- [Skill layout](#skill-layout)
- [Core mental model](#core-mental-model)
- [Standard workflows](#standard-workflows)
  - [A. "Free space NOW" (incident response)](#a-free-space-now-incident-response)
  - [B. "Set up alerting" (new machine or first time)](#b-set-up-alerting-new-machine-or-first-time)
  - [C. Alerter stopped working / making noise](#c-already-have-alerter-but-it-stopped-working--making-noise)
  - [D. "Uninstall an app cleanly"](#d-uninstall-an-app-cleanly)
- [Safety rules (non-negotiable)](#safety-rules-non-negotiable)
- [Domain quirks captured](#domain-quirks-captured)
- [Outcomes scale](#outcomes-scale)

## When to use

Trigger on any of:

- Disk free < 20 % or user complains about being out of space
- Watchdog-timeout / kernel panic / "no checkins from watchdogd"
- New `JetsamEvent-*.ips` with `vm-compressor-space-shortage`
- "Mac is slow", swap > 6 GB, sustained Critical memory pressure
- User wants to set up monitoring/alerting from scratch
- Migration to a new Mac → restore the same alerter
- General "clean my Mac" / "audit storage" / "free space" requests

## Skill layout

| File | Use for |
|---|---|
| `references/triage.md` | First 5 minutes — which signal fired, which tier of cleanup to start with |
| `references/cleanup-tiers.md` | Tiered cleanup playbook (10 tiers, zero-risk → discuss-first), copy-paste-safe shell blocks |
| `references/never-touch.md` | Categories that **must not** be deleted even under sudo (Mole-derived blacklist + incident-derived additions) |
| `references/mole-techniques.md` | What Mole does that we borrow: marker→target map for `mo purge`, safe-path validators, age thresholds |
| `references/alerting.md` | Full alerter design: 3 CRITICAL-only triggers, hysteresis, calibration, alerter vs terminal-notifier vs osascript, install/restore commands |
| `assets/mac-health-check` | Production-ready bash script (~250 lines, bash 3.2 compatible) |
| `assets/com.local.mac-health-check.plist` | LaunchAgent plist with `StartCalendarInterval` (StartInterval is broken on laptops) |
| `assets/config.sh` | Default config with safe thresholds |

Read the relevant reference before acting. Do NOT operate from memory of these files — the details are calibrated to a real incident and small changes break safety.

## Core mental model

1. **Monitor passively** — Stats menubar (`brew install --cask stats`) — you see issues forming, not just when they explode.
2. **Alert actively** — only on truly CRITICAL conditions: disk < 10 %, memory pressure Critical AND swap > 8 GB, or new JetsamEvent with `vm-compressor-space-shortage`. Anything else is noise.
3. **Cleanup tiers** — start zero-risk (caches, orphan data), only escalate to project artifacts and sudo categories if needed. Mole's `mo purge` and `mo clean` are the right primary tools.
4. **Mole is the safety floor** — even when running shell commands by hand, follow Mole's path-validation rules: never delete inside `/System`, `/bin`, `/usr`, `/etc`, `/var/db` outside specific allowlisted subpaths; bin/ only under .NET; vendor/ only under PHP; protect AI/password/VPN/keychain bundle IDs.

## Standard workflows

### A. "Free space NOW" (incident response)

1. **Triage** — read `references/triage.md`, identify which signal fired and how urgent.
2. **Snapshot baseline** — `df -h /System/Volumes/Data` and write down free GB.
3. **Tier 1 → 4** sweep — copy from `references/cleanup-tiers.md`. Each tier ends with a `df` checkpoint.
4. **Run `mo purge`** if dev projects exist. Mole's marker-based detection + bin/.NET guard + vendor/PHP guard makes it safer than hand-rolled `find`.
5. **`mo clean --dry-run`** for cache categories Mole knows about. Show user before confirming.
6. **Stop at goal** — most users target 100 GB free. Don't go below that just for sport.

### B. "Set up alerting" (new machine or first time)

1. Copy `assets/mac-health-check` to `~/bin/mac-health-check` (mkdir first; chmod +x).
2. Copy `assets/com.local.mac-health-check.plist` to `~/Library/LaunchAgents/`.
3. Copy `assets/config.sh` to `~/.config/mac-health/config.sh` (mkdir first).
4. `brew install vjeantet/tap/alerter` (NOT terminal-notifier — it's broken in 2026 on Sequoia/Tahoe).
5. `brew install --cask stats` for passive layer.
6. `launchctl load -w ~/Library/LaunchAgents/com.local.mac-health-check.plist`.
7. First run permission prompt: open `alerter` once interactively (`alerter --message test`) so macOS asks for Notification Center permission.
8. Tell the user: 7-day calibration is silent (logs only). Edit `config.sh` after a week if pattern noisy.

Verify with `launchctl list | grep mac-health` (should show PID and exit 0) and `tail -f ~/Library/Logs/mac-health/health.log`.

### C. "Already have alerter, but it stopped working / making noise"

Read `references/alerting.md` § Troubleshooting. Common causes:
- Stuck/old `terminal-notifier` (the cask) instead of `alerter` — replace.
- LaunchAgent not loading after macOS update — `launchctl bootstrap gui/$(id -u) <plist>`.
- Notifications going to Script Editor — TCC permission was revoked, re-grant.
- Constant alerts during heavy dev work — `touch ~/.config/mac-health/silent` to suppress.

### D. "Uninstall an app cleanly"

`mo uninstall <app>` — Mole scans 12+ locations for app traces (Application Support, Containers, Group Containers, Caches, Preferences, Saved State, LaunchAgents, LaunchDaemons, login items, etc.). Always show dry-run first, never bypass.

## Safety rules (non-negotiable)

1. **Never delete without dry-run + user confirmation** for any tier ≥ 5 or any sudo operation.
2. **Never bypass `references/never-touch.md`** — even if user explicitly asks. Push back, explain the consequence.
3. **`mo purge` and `mo clean` always with `--dry-run` first.** Show estimated reclaim, get confirm.
4. **For Time Machine backups: `tmutil delete <path>`, never `rm`.** TM-tagged paths require the `tmutil` API.
5. **For sudo cleanup of `/Library`, `/private/var/db/*`**: only the allowlisted subpaths from `references/never-touch.md` § Sudo allowlist.
6. **No auto-cleanup hooks tied to alerts.** Alerts notify; user decides. Documented anti-pattern (Google SRE, also confirmed by community 2025-2026 — see `references/alerting.md`).
7. **Don't delete swap files.** `rm /private/var/vm/swapfile*` while running = guaranteed kernel panic.

## Domain quirks captured

- macOS Tahoe (26.x) ships `/bin/bash` 3.2.57. `set -u` + `local var` (no init) = unbound on first reference. The shipped script handles this.
- LaunchAgent **does not inherit user PATH**. Plist must declare `EnvironmentVariables.PATH` and use absolute paths for interpreters.
- `StartInterval` clock pauses during sleep on Apple Silicon laptops (radar 6630231). Use `StartCalendarInterval` with explicit minute entries (the shipped plist has all 12).
- `terminal-notifier` is effectively unmaintained (last release 2019-11) and silently fails on Sequoia/Tahoe Apple Silicon. Use `alerter` instead.
- `osascript display notification` from launchd attributes to "Script Editor" and is unreliable. Use `alerter` from launchd context.
- `log show --last 6m` is too slow (30+ s) for periodic checks. Poll `/Library/Logs/DiagnosticReports/JetsamEvent-*.ips` instead — async write delay is acceptable on a 5-min cadence.
- `JetsamEvent-*.ips` files live in `/Library/Logs/DiagnosticReports/` (system-wide), NOT `~/Library/Logs/DiagnosticReports/`.
- APFS purgeable space lags behind actual deletion by minutes. After cleanup, `df` may not show the change immediately; wait or run `diskutil info /System/Volumes/Data | grep "Container Free"`.

## Outcomes scale

A representative recovery from a Mac that hit ~8 % free after long memory-pressure sessions on a heavily-loaded dev profile (Docker, multiple AI tools, IDEs, browsers):

- ~25 % of total disk capacity recovered in a 4-hour session
- Largest single contribution: project build artifacts via `mo purge` (~30–50 GB across many scan paths)
- Stale IDE installations + caches + preferences: ~10 GB
- Docker reclaim (unused images, dead builders, orphan volumes): ~10 GB
- `~/Downloads` review (old installers, recordings, archived repos): ~15 GB
- Package-manager caches (npm, pnpm, gradle, maven, cargo, brew): ~5 GB
- Sudo-tier cleanup (system logs, vendor-app depots): ~5–10 GB

Active alerter installed with 7-day calibration window; verified via synthetic disk-trigger test before going live. Stats menubar app installed for passive monitoring.

Numbers scale with workload and disk size. Light users will see less; heavy AI/Docker/IDE users will see more.
