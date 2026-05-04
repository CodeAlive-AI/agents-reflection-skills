# Mac Health Check — config
# Override defaults here. Sourced by ~/bin/mac-health-check.

DISK_VOLUME=/System/Volumes/Data
DISK_CRITICAL_PCT=10        # CRITICAL: disk free below this %
SWAP_CRITICAL_GB=8          # used together with critical memory pressure
MEM_FREE_CRITICAL_PCT=10    # memory_pressure 'free %' below this
COOLDOWN_MINUTES=30         # min minutes between repeat alerts of same key
HYSTERESIS_READINGS=3       # consecutive readings before alert (5min × 3 = 15min)
CALIBRATION_DAYS=7          # initial silent period (logs only, no alerts)

# Path to "silence" flag — touch this file to disable alerts on demand
SUPPRESS_FILE="$HOME/.config/mac-health/silent"

# Optional ntfy.sh URL for phone push (leave empty to skip)
# NTFY_URL="https://ntfy.sh/your-private-uuid-topic-here"
NTFY_URL=""
