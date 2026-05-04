# Active alerting

Design and operations of the `mac-health-check` LaunchAgent — the active complement to passive Stats menubar monitoring.

## Table of contents

- [Design principles](#design-principles)
- [Files (canonical paths)](#files-canonical-paths)
- [Why these specific tools](#why-these-specific-tools-current-status)
- [Install / restore on a new Mac](#install--restore-on-a-new-mac)
- [Configuration tuning](#configuration-tuning)
- [Daily operations](#daily-operations)
- [Troubleshooting](#troubleshooting)
- [Removal](#removal-if-user-wants-out)
- [When to re-validate (after macOS updates)](#when-to-re-validate-after-macos-updates)

## Design principles

1. **Three CRITICAL-only triggers**, no warnings or hints:
   - Disk free below configured % (default 10 %)
   - Memory pressure Critical AND swap > 8 GB
   - New `JetsamEvent-*.ips` containing `vm-compressor-space-shortage`
2. **Hysteresis**: 3 consecutive readings before alert (15 min on a 5-min cadence). Eliminates transient spikes.
3. **Cooldown**: 30 min between repeats of the same alert. Prevents storms.
4. **Calibration window**: first 7 days log only, no notifications. Lets you observe the noise floor before alerts engage.
5. **Suppress-flag**: `touch ~/.config/mac-health/silent` disables alerts during heavy work. No need to unload the LaunchAgent.
6. **No auto-cleanup actions**. Alert notifies the human; the human decides.

This design follows Google SRE alert-fatigue principles plus practitioner consensus from incident.io and Netdata Academy.

## Files (canonical paths)

```
~/bin/mac-health-check                              # the script
~/.config/mac-health/config.sh                      # thresholds & switches
~/.config/mac-health/silent                         # touch to suppress (manual)
~/Library/LaunchAgents/com.local.mac-health-check.plist
~/Library/Logs/mac-health/health.log                # script's own log
~/Library/Logs/mac-health/launchd.{out,err}.log     # captured stdio from launchd
~/.local/state/mac-health/install_date              # epoch of first run (for calibration)
~/.local/state/mac-health/jetsam_seen               # dedup of jetsam files we've seen
~/.local/state/mac-health/counter.{disk,memory}     # hysteresis counters
~/.local/state/mac-health/cooldown.<key>            # cooldown timestamps
```

The skill's `assets/` directory holds the reference copies of the script, plist, and config.

## Why these specific tools (current status)

| Choice | Reason |
|---|---|
| `alerter` (vjeantet/alerter) | `terminal-notifier` is **dead** (last release 2019-11) and silently fails on Apple Silicon Sequoia/Tahoe (issue #312). `osascript display notification` from launchd attributes to "Script Editor" and is unreliable. `alerter` is Swift, actively maintained, works in launchd context. |
| `StartCalendarInterval` (12 entries) | `StartInterval` clock pauses during sleep on laptops (radar 6630231); missed intervals never coalesce. `StartCalendarInterval` fires once on wake regardless of how many minute marks were missed. |
| `EnvironmentVariables.PATH` in plist | LaunchAgent default PATH is `/usr/bin:/bin:/usr/sbin:/sbin` — `/opt/homebrew/bin` (where alerter lives) is absent. Without setting PATH, `command -v alerter` fails inside the script. |
| Hardcoded `/bin/bash` interpreter | `#!/usr/bin/env bash` would resolve to /bin/bash 3.2 anyway under launchd, since EnvironmentVariables apply AFTER shebang lookup. Better to be explicit. |
| File polling for JetsamEvent (not `log show`) | `log show --last 6m` takes 30+ seconds even with `--start` on a busy machine. File polling has async-write latency but on a 5-min cadence it's fine. |
| `/Library/Logs/DiagnosticReports/` not `~/Library/Logs/DiagnosticReports/` | JetsamEvent files are written by kernel to system-wide path. The user-level dir does not always exist. |

## Install / restore on a new Mac

Standard install. Set `SKILL` to wherever this skill is installed (default below assumes the user-level Claude Code skills directory; adjust if you installed it elsewhere):

```bash
SKILL=$HOME/.claude/skills/maintaining-macos-health
mkdir -p ~/bin ~/.config/mac-health ~/Library/Logs/mac-health ~/.local/state/mac-health

cp "$SKILL/assets/mac-health-check"          ~/bin/
cp "$SKILL/assets/config.sh"                 ~/.config/mac-health/
# The plist contains __HOME__ placeholders — substitute the user's actual $HOME
# (launchd does not expand ~ or env vars in plist paths)
sed "s|__HOME__|$HOME|g" "$SKILL/assets/com.local.mac-health-check.plist" \
  > ~/Library/LaunchAgents/com.local.mac-health-check.plist
chmod +x ~/bin/mac-health-check

# Notifier
brew install vjeantet/tap/alerter

# First-launch permission grant (otherwise notifications go nowhere)
alerter --message "mac-health-check installation test" --title "First launch" --timeout 3
# A macOS dialog should ask permission. Accept. Then check System Settings → Notifications → alerter and ensure Alert style is set.

# Passive monitor (recommended companion)
brew install --cask stats
open -a Stats

# Activate
launchctl load -w ~/Library/LaunchAgents/com.local.mac-health-check.plist
launchctl list | grep mac-health    # should show PID and exit code 0
sleep 6
tail -10 ~/Library/Logs/mac-health/health.log
```

Verify it works:

```bash
# Force a synthetic disk-trigger using an override config (no real harm)
TMP=/tmp/mh-test.sh
cat > "$TMP" <<EOF
DISK_VOLUME=/System/Volumes/Data
DISK_CRITICAL_PCT=99
SWAP_CRITICAL_GB=999
MEM_FREE_CRITICAL_PCT=0
COOLDOWN_MINUTES=30
HYSTERESIS_READINGS=1
CALIBRATION_DAYS=0
SUPPRESS_FILE=/dev/null/never
NTFY_URL=
NOTIFIER=alerter
JETSAM_DIR=/tmp/no-such-dir
EOF
rm -f ~/.local/state/mac-health/counter.disk ~/.local/state/mac-health/cooldown.disk_critical
MAC_HEALTH_CONFIG="$TMP" /bin/bash ~/bin/mac-health-check
tail -8 ~/Library/Logs/mac-health/health.log
rm -f "$TMP" ~/.local/state/mac-health/counter.disk ~/.local/state/mac-health/cooldown.disk_critical
```

You should see "ALERT key=disk_critical ... -> delivered via alerter" and a notification in Notification Center.

## Configuration tuning

Edit `~/.config/mac-health/config.sh`:

| Variable | Default | When to change |
|---|---|---|
| `DISK_CRITICAL_PCT` | 10 | Lower if you regularly run >90 % full and accept the risk; raise if you want earlier warning |
| `SWAP_CRITICAL_GB` | 8 | On 16 GB machines lower to 5; on 32+ GB raise to 12 |
| `MEM_FREE_CRITICAL_PCT` | 10 | Match what you observe during normal heavy use + 5 % margin |
| `COOLDOWN_MINUTES` | 30 | Lower to 10 if you want more reminders; raise to 60 to silence repeats |
| `HYSTERESIS_READINGS` | 3 | 1 for instant trigger, 5 for very stable conditions |
| `CALIBRATION_DAYS` | 7 | Set to 0 to skip calibration after restore on a known-good machine |
| `NOTIFIER` | auto | Force `alerter` / `terminal-notifier` / `osascript` / `none` for testing |
| `NTFY_URL` | empty | Set to `https://ntfy.sh/<unguessable-uuid>` for phone push (subscribe in ntfy mobile app) |
| `JETSAM_DIR` | /Library/Logs/DiagnosticReports | Override only for testing |

## Daily operations

```bash
# Check it's running
launchctl list | grep mac-health
# (PID column non-dash means actively running; non-zero exit code means recent failure)

# Watch the log
tail -f ~/Library/Logs/mac-health/health.log

# Suppress alerts during heavy work
touch ~/.config/mac-health/silent
# ... work ...
rm ~/.config/mac-health/silent

# Force a check now (bypasses calendar)
/bin/bash ~/bin/mac-health-check
```

## Troubleshooting

### LaunchAgent not running

```bash
launchctl list | grep mac-health
# If absent:
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.local.mac-health-check.plist
# Or:
launchctl load -w ~/Library/LaunchAgents/com.local.mac-health-check.plist

# Check launchd's stderr capture
cat ~/Library/Logs/mac-health/launchd.err.log
```

### Notifications go nowhere

1. Run `alerter --message test --title "permission test" --timeout 3` interactively in Terminal. macOS should prompt.
2. System Settings → Notifications → alerter — set to Alerts (not Banners), enable sound and Notification Center.
3. Confirm `which alerter` returns `/opt/homebrew/bin/alerter`.
4. Confirm plist's `EnvironmentVariables.PATH` includes `/opt/homebrew/bin`.

### Notifications attributed to "Script Editor"

osascript fallback fired instead of alerter. Either alerter wasn't on PATH, or it failed. Check:
- `cat ~/.config/mac-health/config.sh` — confirm `NOTIFIER=auto` (not `osascript`)
- Run `command -v alerter` in the script context: temporarily edit the script, add `command -v alerter >> ~/Library/Logs/mac-health/health.log` near the top.

### Constant alerts during heavy dev work

You're past the calibration window and your normal workload exceeds the thresholds. Either:
- Suppress when needed: `touch ~/.config/mac-health/silent`
- Raise thresholds in config.sh
- Increase `HYSTERESIS_READINGS` to 5 or 6

### "I want phone push too"

Set `NTFY_URL=https://ntfy.sh/<your-private-uuid-topic>` in config.sh. Pick a long unguessable string (at least 32 chars) — ntfy.sh public topics are world-readable. Subscribe to that topic in the ntfy mobile app. Test:

```bash
curl -d "test push from mac-health" \
  -H "Title: Test" \
  -H "Priority: high" \
  https://ntfy.sh/<your-topic>
```

For sensitive use, self-host ntfy. The van Werkhoven blog (2025) has the canonical walkthrough.

## Removal (if user wants out)

```bash
launchctl unload ~/Library/LaunchAgents/com.local.mac-health-check.plist
rm ~/Library/LaunchAgents/com.local.mac-health-check.plist
rm ~/bin/mac-health-check
rm -rf ~/.config/mac-health ~/.local/state/mac-health ~/Library/Logs/mac-health
brew uninstall alerter   # optional
brew uninstall --cask stats   # optional
```

Verify clean:

```bash
launchctl list | grep mac-health   # should be empty
ls ~/bin/mac-health-check 2>&1     # No such file
```

## When to re-validate (after macOS updates)

- After every major macOS upgrade (.0 release): re-test the synthetic trigger. TCC permissions sometimes reset, alerter binary may need re-grant.
- If notifications go quiet for > 7 days without explanation: trigger a manual run, check launchd.err.log, re-grant alerter permission.
