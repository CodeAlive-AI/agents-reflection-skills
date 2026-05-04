# Never-touch list

Categories that **must not be deleted** even if the user asks, even with sudo, even when desperate for space. Pushback expected: explain the consequence, suggest an alternative.

## Table of contents

- [Hard-protected paths (system roots)](#hard-protected-paths-system-roots)
- [Sudo allowlist](#sudo-allowlist-the-only-exceptions-inside-private)
- [Hard-protected app bundle categories](#hard-protected-app-bundle-categories)
- [Auth & credential dotfiles](#auth--credential-dotfiles)
- [macOS storage classes that look generic but hold primary data](#macos-storage-classes-that-look-generic-but-hold-primary-data)
- [User content paths](#user-content-paths-never-auto-clean)
- [Per-app subfolders that LOOK like cache but contain state](#per-app-subfolders-that-look-like-cache-but-contain-state)
- [OS-level operations that NEVER apply](#os-level-operations-that-never-apply)
- [How to handle pushback](#how-to-handle-pushback)

Lists are derived from Mole's `app_protection.sh` (community-vetted) plus additions from real incidents.

---

## Hard-protected paths (system roots)

Never delete inside these prefixes — even one wrong path can brick the OS. macOS SIP usually blocks these, but a sudo'd `rm -rf` can still cause damage to the writable parts.

```
/
/System
/bin
/sbin
/usr
/etc
/var
/private
/Library/Extensions
```

### Sudo allowlist (the only exceptions inside `/private/...`)

These specific subpaths are safe under sudo, with a `find -mtime` filter:

```
/private/tmp
/private/var/tmp
/private/var/log
/private/var/folders         # Per-user temp; only $TMPDIR subset
/private/var/db/diagnostics
/private/var/db/DiagnosticPipeline
/private/var/db/powerlog
/private/var/db/reportmemoryexception
```

Anything else under `/private/var/db` (especially `uuidtext`, `receipts`, `BootCaches`, `mds`, `mds_stores`) — leave alone. `uuidtext` is the CrashReporter symbol cache; deleting it breaks symbolication of any future crash.

---

## Hard-protected app bundle categories

These bundle ID prefixes are never auto-cleaned by Mole and must not be touched manually. Even Caches/CodeCache subfolders for these apps are risky.

### System components (touching these breaks macOS)
- `com.apple.*` (entire family for system services)
- `loginwindow`, `dock`, `finder`, `safari`, `systempreferences`
- `com.apple.SystemSettings`, `com.apple.controlcenter*`
- `com.apple.Spotlight`, `com.apple.notificationcenterui`
- `com.apple.SecurityAgent`, `com.apple.securityd`, `com.apple.trustd`
- `com.apple.cloudd`, `com.apple.iCloud*`
- `com.apple.WiFi*`, `com.apple.Bluetooth*`, `com.apple.airport*`
- `com.apple.coreservices*`, `com.apple.metadata*`
- `com.apple.MobileSoftwareUpdate*`, `com.apple.SoftwareUpdate*`
- `com.apple.installer*`
- `com.apple.frameworks*`
- `com.apple.background*`

### Specific known-broken-if-deleted
- **`com.apple.coreaudio` / `coreaudiod`** — Mole issue #553. Deleting cache breaks audio on Intel Macs (Apple Silicon less affected, still avoid).
- **`com.apple.controlcenter*` caches** — Mole issue #136. Causes blank Settings panel on Sonoma/Sequoia/Tahoe.
- **`org.cups.*` (printing subsystem)** — Mole issue #731. Wipes saved printers and recent-printer list.
- **`com.apple.tcc.db`** — TCC permission database. Deleting forces re-grant of every Notification/Camera/Mic/etc. permission.
- **Keychains** (`~/Library/Keychains/*`) — passwords, certificates, tokens. Deletion = lost auth across all apps.
- **Microsoft Office Group Container** (`~/Library/Group Containers/UBF8T346G9.Office`) — shared state for Word/Excel/PowerPoint/Teams: license activation, Outlook profile, autosave drafts. Often 1–3 GB; looks bulky but **deletion forces re-licensing and loses Outlook profile** (eclecticlight.co: Group Containers explained).

### Input methods (deleting wipes user dictionaries)
- `com.tencent.inputmethod.QQInput`
- `com.sogou.inputmethod.*`
- `com.baidu.inputmethod.*`
- `*.inputmethod`, `*IME`
- `com.apple.inputmethod.*`
- `org.pqrs.Karabiner*` (key remapping — config + license)

### Password managers
- `com.1password.*`
- `com.agilebits.*` (1Password legacy)
- `com.lastpass.*`
- `com.dashlane.*`
- `com.bitwarden.*`
- `com.keepassx*`, `org.keepassx*`, `org.keepassxc.*`
- `com.authy.*`, `com.yubico.*`

### AI tools (chat history is in Application Support)
- `com.anthropic.claude*`, `Claude` — chat history
- `com.openai.chat*`, `ChatGPT`
- **Cursor** (`com.todesktop.*` — Cursor uses ToDesktop)
- `com.ollama.ollama`, `Ollama` — installed models (often 10+ GB but user data)
- `com.lmstudio.lmstudio`, `LM Studio`
- `Gemini`
- `com.perplexity.Perplexity`
- `Antigravity`
- Custom AI editors with chat state

For AI tools, only Cache / Code Cache / GPUCache / Service Worker / CacheStorage subfolders are clearable. Never IndexedDB, Local Storage, or anything outside the cache families.

### Database clients (saved connections, query history, registered databases)
- `com.sequelpro.*`, `com.sequel-ace.*`
- `com.dbeaver.*`
- `com.navicat.*`
- `com.mongodb.compass`
- `com.redis.RedisInsight`
- `com.pgadmin.pgadmin4`
- `com.dbvis.DbVisualizer`
- `com.valentina-db.*`
- `com.Neo4j.Neo4jDesktop` / `Neo4j Desktop` — registered DBMSes, plugins, project files (per-DB graph data lives under Application Support — never auto-clean even when 1+ GB)

### API clients (collections, environments, history)
- `com.postmanlabs.mac`
- `com.konghq.insomnia`
- `com.usebruno.app`
- `com.charlesproxy.charles`, `com.CharlesProxy.*`
- `com.proxyman.*`
- `com.luckymarmot.Paw`, `com.getpaw.*`
- `com.telerik.Fiddler`

### VPN / proxy clients
- `com.clash.*`, `ClashX*`, `clash-verge*`
- Shadowsocks, V2Ray
- Tailscale (auth tokens)
- Mullvad, NordVPN, ProtonVPN
- WireGuard (`com.wireguard.*`, Group Container `L82V4Y2P3C.group.com.wireguard.macos` — tunnel configs + private keys; deletion = re-import every tunnel)
- Outline (`org.outline.macos.client`, Group Container `QT8Z3Q9V3A.org.outline.macos.client` — server access keys)
- AmneziaVPN, BlancVPN — bundled configs and credentials live in Application Support; no in-app re-import without backup

### IDEs (project history, settings, indexes)
- `com.jetbrains.*`, `JetBrains*`
- `com.microsoft.VSCode`, `com.microsoft.VSCodeInsiders`
- `com.visualstudio.code.*`
- `com.sublimetext.*`, `com.sublimehq.*`
- `com.apple.dt.Xcode`
- `com.coteditor.CotEditor`, `com.macromates.TextMate`
- `com.panic.Nova`
- `abnerworks.Typora`, `com.uranusjr.macdown`

For IDEs, only logs, caches, indexes, plugin caches are safe. Never user settings, project lists, license files.

### Terminal apps & multiplexers
- **iTerm2** — `com.googlecode.iterm2` bundle, `~/Library/Preferences/com.googlecode.iterm2.plist` (all profiles + keybindings; corrupted file = full reset, GitLab #6095), `~/Library/Application Support/iTerm2/DynamicProfiles/` (script-managed profiles).
- **Warp** — `dev.warp.Warp-Stable`, **primary store is in Group Container**: `~/Library/Group Containers/2BBY89MBSN.dev.warp/Library/Application Support/dev.warp.Warp-Stable/warp.sqlite` (block history, AI prefs, Warp Drive).
- **Ghostty** — `com.mitchellh.ghostty`, config at `~/.config/ghostty/config` (XDG path takes priority; do not also write to App Support — causes "cycle detected" bug, GH #11268).
- **Kitty** / **WezTerm** / **Alacritty** — XDG-only configs at `~/.config/{kitty,wezterm,alacritty}/`. No Application Support fallback. Wiping `~/.config/` sweeps all of these.
- **Tabby** (`org.tabby`), **Hyper** (`co.zeit.hyper`), **Rio** (`com.raphaelamorim.rio`).
- **tmux-resurrect / tmux-continuum** — `~/.tmux/resurrect/` plaintext snapshots + `last` symlink. Delete = all saved sessions gone, no recovery (tmux-resurrect issues #379, #155).
- **Zellij** — `~/.config/zellij/`, layouts in `~/Library/Application Support/org.Zellij-Contributors.Zellij/`.

### Note-taking / PKM apps
- **Obsidian** — global registry `~/Library/Application Support/obsidian/obsidian.json` lists all known vaults (delete = Obsidian forgets vaults, requires re-add). Per-vault `<vault>/.obsidian/` is plugins + workspace + community plugin data — looks like a dotfolder but it's the entire per-vault config.
- **Bear** — `com.shinyfrog.bear`, **single source of truth**: `~/Library/Group Containers/9K33E3U3T4.net.shinyfrog.bear/Application Data/database.sqlite`. No iCloud copy without Bear Pro. Deletion = total note loss (official Bear FAQ).
- **Joplin** — `~/.config/joplin-desktop/` is a self-contained profile: SQLite + attachments + **E2E encryption keys**. Delete with E2E enabled = cloud copy becomes permanently undecryptable (Joplin user-profile spec).
- **DEVONthink** — `~/Library/Application Support/DEVONthink 3/` holds the proprietary `.dtBase2` knowledge base if user did not relocate. Delete = entire database loss.
- **Logseq** — graph at user-chosen path, but config + plugins in `~/.logseq/config/` and `~/Library/Application Support/Logseq/`.
- **Craft** (`com.lukilabs.lukiapp`), **Reflect** (`im.reflect.app`), **NotePlan** (`co.noteplan.NotePlan3`), **Notion Calendar** (formerly Cron, `notion.id`) — local DBs + sync state in Application Support.

### Cloud sync clients
- **Dropbox** — `~/Library/Application Support/Dropbox/` (sync queue + config) + `~/Library/CloudStorage/Dropbox` (File Provider, macOS 12.3+). `rm -rf` on the CloudStorage path is **not permitted** through Finder, but Safe-Mode delete is irreversible and bypasses Trash (MacRumors, ianbetteridge.com).
- **OneDrive** — `~/Library/CloudStorage/OneDrive-Personal/` and per-tenant variants. Cloud-only files appear as local stubs; deleting a stub deletes the cloud file. Re-download blocked by `MaxClientMBTransferredPerDay` once tripped.
- **Box**, **pCloud**, **Sync.com**, **Yandex.Disk**, **Mega**, **iDrive**, **Tresorit** — all use File Provider extensions under `~/Library/CloudStorage/<vendor>/`. Same rule.
- **iCloud Drive** — `~/Library/Mobile Documents/com~apple~CloudDocs/` (already in user content list, but also a sync target — deletion propagates to all devices).

### Crypto wallets / hardware wallet apps
- **Exodus** — `~/Library/Application Support/Exodus/` holds encrypted seed-derived wallet files. Without the 12-word recovery phrase, deletion = irreversible loss of access to funds.
- **Electrum** — `~/Library/Application Support/Electrum/wallets/` (per-wallet `.dat` files, encrypted with passphrase).
- **Ledger Live** (`com.ledger.live-desktop`) — `~/Library/Application Support/Ledger Live/` stores account list + transaction history. Funds are on the hardware device, but recovery phrase is needed to rebuild account state if app data is lost (Ledger support ZD-8490479490533).
- **Trezor Suite** (`io.trezor.Trezor-Suite`) — `~/Library/Application Support/@trezor/suite-desktop/`.
- **MetaMask** browser extension state lives inside the browser profile (Chrome/Brave/Arc). Deleting the browser profile = wallet seed loss unless backed up.

### Container & VM runtimes
- **OrbStack** — `~/Library/Application Support/OrbStack/` (machines + Docker engine state, often 10–50 GB) and Group Container `HUAQ24HBR6.dev.orbstack`. Looks bulky but contains all VM disk images.
- **UTM** — `~/Library/Containers/com.utmapp.UTM/Data/Documents/` (Mac App Store sandboxed) or `~/Library/Application Support/UTM/` (Homebrew). VMs live there.
- **Parallels Desktop** — `~/Parallels/` (default VM library), `~/Library/Group Containers/4C6364ACXT.com.parallels.desktop.appstore/` (license + shared state).
- **VMware Fusion** — `~/Virtual Machines.localized/`, `~/Library/Preferences/VMware Fusion/`.
- **Lima**, **Colima** — `~/.lima/`, `~/.colima/` (Linux VM images for Docker-compatible runtimes).
- **Tart** — `~/.tart/vms/` (macOS VMs for CI).

These VM directories are the single largest legitimate footprint on dev machines after Xcode and Docker. They look like cache to Mac-cleaner UIs but contain the user's entire dev environment. Never auto-clean.

---

## Auth & credential dotfiles

These dotfiles are tiny but contain irreplaceable credentials. Mac-cleaner UIs that scan `$HOME` for "old hidden files" can flag them; never include in any cleanup pass, even one focused on `~/.cache/` or "old dotfiles".

| Path | What it stores | Recovery if deleted |
|---|---|---|
| `~/.ssh/id_*`, `~/.ssh/*.pem`, `~/.ssh/google_compute_engine` | Private SSH keys | None — must regenerate and re-distribute public keys to every server / GitHub / GCP |
| `~/.ssh/config`, `~/.ssh/known_hosts` | Host aliases + fingerprints | `known_hosts` regenerates on first connect (with TOFU prompts); `config` is irrecoverable |
| `~/.gnupg/` (`pubring.kbx`, `private-keys-v1.d/`, `trustdb.gpg`) | GPG keyring incl. secret keys | None — encrypted data and signed-only-by-you content become unrecoverable |
| `~/.aws/credentials`, `~/.aws/config`, `~/.aws/sso/` | AWS access keys + SSO cache | New keys via IAM console; old keys cannot be recovered (AWS re:Post) |
| `~/.config/gh/hosts.yml` | GitHub CLI OAuth tokens | `gh auth login` re-issues; on macOS also stored in Keychain — both must be cleared together |
| `~/.config/op/` | 1Password CLI session | Regenerated by `op signin`; harmless to delete |
| `~/.netrc` | Plaintext FTP/HTTP credentials | Plaintext — copy from password manager |
| `~/.kube/config` | Kubernetes cluster contexts + tokens | Re-fetch via `gcloud container clusters get-credentials` / `aws eks update-kubeconfig` etc. |
| `~/.docker/config.json` | Registry auth tokens | `docker login` re-issues; tokens stored in Keychain on macOS |
| `~/.npmrc`, `~/.yarnrc`, `~/.pypirc`, `~/.cargo/credentials` | Package-registry auth tokens | Re-issue from each registry's web UI |
| `~/.git-credentials`, `~/.config/git/credentials` | Git HTTPS credentials | `git credential` helper or Keychain re-prompt |

Heuristic: **any dotfile or dotfolder in `$HOME` outside `~/.cache/`, `~/.local/share/<app>/cache*`, `~/.npm/_cacache`, and language-specific `~/.gradle/caches/`-style explicit caches should be assumed credential-bearing or config-bearing.** Validate via `file` / `head` only when in doubt — never bulk-delete dotfiles.

---

## macOS storage classes that look generic but hold primary data

These four `~/Library/...` parents are common targets for "Mac cleanup" tools because their names sound like cache. They are not. Each subdirectory inside them belongs to a specific app and is treated by that app as primary data, not regenerable cache.

### `~/Library/Saved Application State/`
- Per-app subfolders ending in `.savedState/` store window layout, scrollback (terminals), tab order, and unsaved Document state.
- **Excluded from Time Machine by default** — losing this folder loses state with no automatic backup (iboysoft.com, iTerm2 GitLab #6145).
- Common loss vector: Mac-cleaners and reset scripts treat this as garbage. cmux, iTerm2, Terminal.app, Console.app, Finder layout, and many others all live here.
- Rule: **never wipe wholesale. If a single app's saved state is suspected corrupt, remove that one subfolder by name only.**

### `~/Library/Group Containers/`
- Shared sandboxed storage between an app, its widgets, Share Extensions, Watch companions, and login items (Apple Developer docs; eclecticlight.co "What are all those Containers?").
- Each subfolder is identified by a Team ID prefix (`UBF8T346G9.*` = Microsoft, `9K33E3U3T4.*` = Bear, `2BBY89MBSN.*` = Warp, `6N38VWS5BX.*` = Telegram, etc.).
- **Each subfolder is the primary store for the corresponding app**, not a cache. Microsoft Office, Telegram, Bear, Warp, OrbStack, WireGuard, Outline all keep main data here.
- Deletion can simultaneously break the app + its widgets + its Watch companion + its Share Extension. Rule: **treat every Group Container as Application Support of its owner — same protection level.**

### `~/Library/Containers/<bundle-id>/`
- Sandbox roots for Mac App Store apps (System Settings → Privacy & Security → App Management lists which apps).
- `Containers/<bundle>/Data/Documents/` is **the user-visible Documents folder for that sandboxed app** — equivalent to `~/Documents` for non-sandboxed apps. Bear (App Store edition), DEVONthink, Affinity suite, Things 3, Numbers/Pages/Keynote (when used standalone), UTM, all keep user-created content here.
- `Containers/<bundle>/Data/Library/Application Support/` is the sandboxed app's primary state; everything inside is non-regenerable.
- Rule: **never recurse into `Containers/`. If freeing space, target only the Mole-style cache families inside `Containers/<bundle>/Data/Library/Caches/`.**

### `~/Library/CloudStorage/`
- File Provider mount points for Dropbox, OneDrive, Box, pCloud, Google Drive (Desktop), Yandex.Disk, Mega, iDrive — listed by name (`Dropbox`, `OneDrive-Personal`, `GoogleDrive-<email>`, etc.).
- macOS hides eviction state — locally evicted files appear as transparent stubs. **Deleting a stub deletes the cloud original** (it is the cloud original, just dehydrated locally).
- Safe Mode `rm` bypasses File Provider's protection and goes directly to disk — irreversible, no Trash (MacRumors).
- Rule: **never delete inside `~/Library/CloudStorage/<vendor>/` from the shell. Only from the app's own UI, after confirming sync state.**

---

## User content paths (never auto-clean)

- `~/Library/Mobile Documents/` — iCloud Drive locally synced. User files. Even subdirectories that look like cache (`.DocumentRevisions-V100`) are not actually cache from a user perspective.
- `~/Library/CloudStorage/<vendor>/` — File Provider mount points (Dropbox, OneDrive, Google Drive Desktop, Box, pCloud, Yandex.Disk, etc.). See [macOS storage classes](#macos-storage-classes-that-look-generic-but-hold-primary-data) — never delete from shell.
- `~/Pictures/Photos Library.photoslibrary` — Photos database. Even with iCloud, the local library bundle is the source of truth for Photos.app. Direct manipulation corrupts the library.
- `~/Library/Messages/` — Messages.app database. `chat.db` and `Attachments/`. Deleting attachments removes them from Messages history.
- `~/Library/Mail/V*/MailData/` — Mail.app local mailboxes (if Mail.app is used).
- `~/Library/Application Support/AddressBook/` — Contacts data.
- `~/Library/Application Support/com.apple.sharedfilelist/` — Recent Items lists, login items.
- `~/.Trash` — only empty if user explicitly OK; recently deleted files may still be wanted.
- `~/Documents`, `~/Desktop`, `~/Pictures`, `~/Movies`, `~/Music` (root level) — user content. Only delete specific files identified individually.

---

## Per-app subfolders that LOOK like cache but contain state

These are inside Application Support but are NOT regenerable. Only the cache-family subfolders (`Cache`, `Code Cache`, `GPUCache`, `Service Worker/CacheStorage`, `DawnCache`, etc.) are clean targets.

| App | Path | What it actually is |
|---|---|---|
| Telegram | `~/Library/Application Support/Telegram Desktop/tdata/` | Full chat history + session keys. Delete = logout + lost local history. |
| Telegram | `~/Library/Group Containers/*.com.tdesktop/` | Same |
| Granola | `~/Library/Application Support/Granola/File System/` | Meeting transcripts and notes |
| Granola | `~/Library/Application Support/Granola/IndexedDB/` | Structured transcript data |
| Notion | `~/Library/Application Support/Notion/Partitions/notion/IndexedDB/` | Offline page data |
| Slack | `~/Library/Application Support/Slack/storage/`, `IndexedDB/` | Workspace prefs, draft messages |
| Arc | `~/Library/Application Support/Arc/User Data/Default/IndexedDB/` | Extension state, 1Password vault refs |
| Arc | `~/Library/Application Support/Arc/User Data/Default/Local Extension Settings/` | Same |
| Zed | `~/Library/Application Support/Zed/db/0-stable/` | LSP index, project history |
| opencode | `~/.local/share/opencode/opencode.db` | Conversation history |
| Codex | `~/.codex/sessions/` | Conversation history (NOT log/) |
| Claude Code | `~/.claude/projects/*/` | Per-project session history |
| Claude Code | `~/Library/Application Support/Claude/vm_bundles/claudevm.bundle/` | **9.7 GB Linux sandbox runtime — active, never delete** |
| Voice Memos | `~/Library/Application Support/com.apple.voicememos/Recordings/` | User audio recordings |
| Notes | `~/Library/Group Containers/group.com.apple.notes/` | Notes content + attachments |
| cmux | `~/.cmuxterm/` | Claude-hook session store (`claude-hook-sessions.json`) — maps Claude session IDs to cmux workspaces. Delete = lose tab→session mapping. |
| cmux | `~/Library/Saved Application State/com.cmuxterm.app.savedState/` | Open tabs, split layout, scrollback. Delete = next launch starts with empty window, all tabs gone. **Common loss vector** since `Saved Application State` is a generic Mac-cleanup target. |
| cmux | `~/.config/cmux/`, `~/Library/Application Support/cmux/`, `~/Library/Application Support/com.cmuxterm.app/` | Settings, runtime data, telemetry. Delete only if fully reinstalling. |
| iTerm2 | `~/Library/Saved Application State/com.googlecode.iterm2.savedState/` | Open windows, scrollback, profile selections. **Excluded from Time Machine**, so deletion is unrecoverable from a backup (GitLab #6145). |
| iTerm2 | `~/Library/Application Support/iTerm2/DynamicProfiles/` | JSON profiles managed by external scripts (e.g. SSH config sync). Delete = lose all script-managed profiles. |
| Warp | `~/Library/Group Containers/2BBY89MBSN.dev.warp/Library/Application Support/dev.warp.Warp-Stable/warp.sqlite` | Block history, AI prefs, Warp Drive. Group-Container path means many backup tools miss it. |
| Bear | `~/Library/Group Containers/9K33E3U3T4.net.shinyfrog.bear/Application Data/database.sqlite` | **Single source of truth for all notes.** Without Bear Pro / iCloud sync, this is the only copy. |
| Obsidian | `~/Library/Application Support/obsidian/obsidian.json` | Registry of all known vaults. Delete = Obsidian "forgets" vaults; user must re-add each by path. |
| Obsidian | `<vault>/.obsidian/` | Per-vault plugins, themes, workspace. Looks like a dotfolder; it is the entire per-vault config. |
| Joplin | `~/.config/joplin-desktop/` | SQLite + attachments + **E2E encryption keys**. With E2E enabled, deletion makes the cloud copy permanently undecryptable. |
| DEVONthink | `~/Library/Application Support/DEVONthink 3/` | Default location of `.dtBase2` knowledge base if not relocated. |
| Microsoft Office | `~/Library/Group Containers/UBF8T346G9.Office/` | Shared Office state: license activation, Outlook profile, autosave. Often 1–3 GB; deletion forces re-licensing and loses Outlook profile. |
| OrbStack | `~/Library/Application Support/OrbStack/`, `~/Library/Group Containers/HUAQ24HBR6.dev.orbstack/` | VM disk images + Docker state. Often 10–50 GB but contains the entire dev environment. |
| Ledger Live | `~/Library/Application Support/Ledger Live/` | Account list + transaction history. Funds safe on device, but recovery phrase required to rebuild app state. |
| Exodus | `~/Library/Application Support/Exodus/` | Encrypted wallet files. Without seed phrase, deletion = permanent loss of funds. |
| tmux-resurrect | `~/.tmux/resurrect/` | Plaintext session snapshots + `last` symlink. No restore mechanism after deletion. |
| Neo4j Desktop | `~/Library/Application Support/Neo4j Desktop/` | Registered DBMSes, graph data, plugins. Often 1–2 GB but holds primary user databases. |

When in doubt for an Application Support folder: only Cache/CodeCache/GPUCache/Service Worker subdirs are safe. Everything else, ask.

---

## OS-level operations that NEVER apply

- `rm -rf /private/var/vm/swapfile*` — guaranteed kernel panic. Live swap files cannot be removed; macOS manages lifecycle.
- `rm /private/var/vm/sleepimage` — only safe if hibernation is disabled first via `sudo pmset -a hibernatemode 0 standby 0`. Otherwise corrupts sleep/wake.
- Force-killing live processes for "memory pressure" — corrupts open file handles. Docker volumes, databases, in-flight git operations, unsaved files. Suggest user close gracefully.
- Auto-emptying Trash — user may still want recent items.
- Auto-cleanup tied to alerts — anti-pattern (Google SRE consensus). Alert notifies; human decides.
- Disabling SIP for "deeper monitoring access" — CVE-2024-44243 demonstrated kernel attack surface. Not justified for personal monitoring.
- Modifying TCC database (`tccutil reset` is fine, direct SQLite edits are not).
- `rm` inside `~/Library/CloudStorage/<vendor>/` — File Provider treats every local entry as a handle to the cloud original, including dehydrated stubs. Shell `rm` propagates the deletion to the cloud and bypasses Trash; in Safe Mode it bypasses the File Provider protection entirely (MacRumors, ianbetteridge.com).
- Wiping a browser profile (`~/Library/Application Support/{Google/Chrome,BraveSoftware,Arc,Microsoft Edge,...}/Default/`) when MetaMask / browser-extension wallets or password sync are in use — extension state is per-profile; deleting it = lost seed phrase unless backed up via the extension's recovery flow.
- Removing `~/Library/Saved Application State/` wholesale to "fix a stuck app" — affects every app, not just the broken one. Remove only the targeted `<bundle>.savedState/`.

---

## How to handle pushback

User says "I know it's risky, just delete it":

1. State the consequence in concrete terms ("you'll lose your last 6 months of meeting transcripts", not "user data").
2. Offer alternative: archive instead of delete, or use the app's own export, or move to external SSD.
3. If they insist, document in chat: confirm exact path, exact action, exact intended effect. Make them say "yes, delete X.path which contains Y, I accept losing Z."
4. Even then, prefer non-destructive: `mv` to `~/.deleted-YYYYMMDD/` instead of `rm`. Easy to recover if they regret it.

Risk is asymmetric: false caution costs them disk space; one bad delete costs them weeks of work. Bias toward caution.
