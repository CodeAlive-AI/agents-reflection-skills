# Triage — first 5 minutes

When the user reports trouble, or an alert fires, identify which signal class fired before doing anything destructive. The right response differs.

## Table of contents

- [Quick state snapshot](#quick-state-snapshot-always-run-first)
- [Signal classification](#signal-classification)
  - [A. Disk-driven](#a-disk-driven-most-common)
  - [B. Memory-driven](#b-memory-driven)
  - [C. Kernel-panic / watchdog-timeout](#c-kernel-panic--watchdog-timeout-rare-but-severe)
  - [D. JetsamEvent with vm-compressor-space-shortage](#d-jetsamevent-with-vm-compressor-space-shortage)
  - [E. "Mac just feels slow"](#e-mac-just-feels-slow)
- [Decision tree](#decision-tree)
- [What to NOT do at triage](#what-to-not-do-at-triage)

## Quick state snapshot (always run first)

```bash
echo "=== Disk ==="
df -h /System/Volumes/Data
diskutil info /System/Volumes/Data | grep -E "Free|Used|Capacity|Container Free"

echo "=== Memory ==="
memory_pressure | head -20
sysctl vm.swapusage hw.memsize hw.model
vm_stat

echo "=== Recent panics & jetsam ==="
ls -lt /Library/Logs/DiagnosticReports/ 2>/dev/null | head -10
ls -lt /Library/Logs/DiagnosticReports/Retired/ 2>/dev/null | head -5

echo "=== Top RSS processes ==="
ps -axo pid,rss,vsz,pcpu,pmem,command | sort -k2 -n -r | head -15

echo "=== Health-check log if installed ==="
test -f ~/Library/Logs/mac-health/health.log && tail -20 ~/Library/Logs/mac-health/health.log

echo "=== Uptime, load ==="
uptime
```

## Signal classification

### A. Disk-driven (most common)

Symptoms: `df` shows < 20 % free, user complains "out of space".

- **`pct_free < 10 %`** → CRITICAL. Run Tier 1–4 from `cleanup-tiers.md` immediately. swap extension may already be blocked.
- **`pct_free 10–20 %`** → HIGH. Run Tier 1–3, propose Tier 4. Probably manageable.
- **`pct_free > 20 %`** → user perception issue. Check `du -d1 -h ~ | sort -h | tail -15` and address specifically.

The canonical incident hit ~8 % free, well below the 10 % critical threshold. APFS purgeable can lag — `diskutil info` "Container Free" is the real number.

### B. Memory-driven

Symptoms: Mac slow, beachballs, swap > 6 GB, fans running.

- Check `memory_pressure` output for system-wide memory free percentage.
  - **Critical (< 10 %)** + **swap > 8 GB**: imminent thrashing. Close heavy apps. Stop new work.
  - **Warning (10–25 %)**: heavy load but stable. Monitor.
  - **Normal (> 25 %)**: false alarm.
- A 16–18 GB Mac under heavy AI/Docker is expected to swap 2–4 GB. Don't panic on swap alone; pair with pressure level.
- VM-driven: if `com.apple.Virtualization.VirtualMachine` shows in top RSS (Docker Desktop), check Docker memory limit:
  ```bash
  jq '.MemoryMiB' ~/Library/Group\ Containers/group.com.docker/settings-store.json
  ```
  Rule of thumb: Docker memory ≤ 1/3 of host RAM. On 16–18 GB hosts, > 6 GB allocation is dangerous; 4–5 GB is the safe ceiling.

### C. Kernel-panic / watchdog-timeout (rare but severe)

Symptoms: Mac rebooted unexpectedly. Panic dialog after wake.

```bash
ls -lt /Library/Logs/DiagnosticReports/Retired/*.panic 2>/dev/null
cat /Library/Logs/DiagnosticReports/.contents.panic 2>/dev/null | jq -r '.panic_string' | head -50
```

Look for in `panicString`:
- `watchdog timeout: no checkins from watchdogd in N seconds` → Mac was non-responsive for N seconds. Almost always caused by:
  - **`Compressor Info: ... 100% of segments limit (BAD)`** + **`LOW swap space`** + many swapfiles → memory thrashing (the canonical incident).
  - I/O stall on boot SSD (rare on Apple Silicon healthy NAND).
  - Spinlock deadlock — all cores at the same PC; needs KDK + LLDB to symbolicate.
- The full panic JSON has `processByPid` with each process's `residentMemoryBytes` and `pageFaults` — find the top RSS process. In the canonical incident: `com.apple.Virtualization.VirtualMachine` 9.4 GB RSS, 512 M pageFaults.
- Cross-check Disk free at the time: was it already low? (panic file's `memoryStatus.compressorSize` × 16 KB = compressed pages on hand)

After a panic of this class:
1. Confirm it was a one-off (check Retired/ for prior panics).
2. Run cleanup Tier 1–7 to give breathing room.
3. Install/verify the alerter (`alerting.md`).
4. Discuss reducing Docker memory if a VM was the proximate cause.

### D. JetsamEvent with `vm-compressor-space-shortage`

This is the alerter's loudest signal — it's a leading indicator of (C). Find the file:

```bash
grep -l "vm-compressor-space-shortage" /Library/Logs/DiagnosticReports/JetsamEvent-*.ips 2>/dev/null
```

If exists and recent (last 30 min): system already started killing processes for memory. **Treat as imminent panic risk**:
1. Save user work.
2. Quit Docker Desktop, browser tabs, AI tools.
3. Don't run `mo clean` or anything heavy — that itself thrashes memory.
4. Wait 5 min for system to settle, then proceed with cleanup if still in trouble.

### E. "Mac just feels slow"

Probably memory pressure or thermal throttling. Check:
```bash
sudo powermetrics --samplers cpu_power,thermal -i 1000 -n 5
```
- If thermal pressure shows `Heavy`: close apps, let it cool, check fans.
- Else fall back to memory-driven flow (B).

## Decision tree

```
ALERT or USER REPORT
       │
       ▼
   df -h <20%? ──yes──▶ A. Disk-driven (cleanup-tiers.md)
       │
       no
       ▼
   panic in
   last hour? ──yes──▶ C. Read panic, identify top RSS, propose cleanup + alerter
       │
       no
       ▼
   JetsamEvent
   vm-compressor? ──yes──▶ D. Triage immediate, then cleanup
       │
       no
       ▼
   memory_pressure
   not Normal? ──yes──▶ B. Memory-driven, check Docker, top RSS
       │
       no
       ▼
   thermal? ──yes──▶ E. Power/thermal advice
       │
       no
       ▼
   user perception → du audit, propose targeted cleanup
```

## What to NOT do at triage

- Don't run `mo clean` or `mo purge` reflexively. Identify what's hurting first.
- Don't `kill -9` the top RSS process — saving work first matters; a hard kill on Docker can corrupt volumes.
- Don't `sudo rm -rf /private/var/vm/swapfile*` — guaranteed kernel panic.
- Don't blindly empty Trash if the user might still want recently deleted items.
