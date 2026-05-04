package main

import (
	"os"
	"path/filepath"
	"runtime"
	"strings"
)

// PathClassification is the outcome of resolving a single rm operand.
type PathClassification int

const (
	PathSafe          PathClassification = iota // inside a safe path
	PathOutsideSafe                             // outside, but not catastrophic
	PathCatastrophic                            // /, $HOME, /etc, /usr, ...
	PathSafeRootSelf                            // exactly a safe-path root, e.g., "/tmp"
	PathSharedRootGlob                          // top-level glob inside a shared root, e.g., "/tmp/*"
	PathUnresolvable                            // contains $VAR, $(...), ?-glob, etc.
)

// SafePaths is the resolved allowlist for one hook invocation.
// All paths are absolute and realpath-normalised.
//
// Catastrophic paths are split into three buckets:
//   - exact: a path is catastrophic ONLY if it equals one of these (e.g.,
//     "/" or $HOME — but $HOME/some-project is NOT catastrophic).
//   - prefix: anything strictly under one of these is catastrophic
//     (/etc, /usr, /var, ...). Carved out by explicit safe paths.
//   - homeProtected: subdirs under $HOME that are unsafe to delete
//     (.ssh, Library, Documents, ...). Also carved out by explicit safe paths.
//
// "Carved out" means: if a path is inside any explicit safe path (sp.dirs),
// catastrophic checks are skipped. This is what lets /var/tmp/foo and
// ~/Library/Caches/foo work despite /var and ~/Library being protected.
type SafePaths struct {
	dirs               []string
	catastrophicExact  []string
	catastrophicPrefix []string
	homeProtected      []string
	cwdContributes     bool
	cwd                string
}

// NewSafePaths builds the allowlist. cwd is the hook-input cwd.
// If cwd is "/", "$HOME", "/Users", or "/home", it does NOT contribute
// to the safe path subtree (consilium P0 Gemini): the cwd subtree check
// would otherwise whitelist everything under root or all user homes.
func NewSafePaths(cwd string, extra []string) *SafePaths {
	sp := &SafePaths{}

	cwdReal := realpath(cwd)
	sp.cwd = cwdReal

	if !isCwdRoot(cwdReal) {
		sp.cwdContributes = true
		sp.dirs = append(sp.dirs, cwdReal)
	}

	candidates := []string{
		"/tmp",
		"/private/tmp",
		"/var/tmp",
		"/private/var/tmp",
		os.Getenv("TMPDIR"),
		os.Getenv("XDG_CACHE_HOME"),
		os.Getenv("XDG_RUNTIME_DIR"),
		filepath.Join(homeDir(), ".cache"),
	}
	if runtime.GOOS == "darwin" {
		candidates = append(candidates, filepath.Join(homeDir(), "Library", "Caches"))
	}
	for _, c := range candidates {
		if c == "" {
			continue
		}
		r := realpath(c)
		if r == "" {
			continue
		}
		sp.dirs = append(sp.dirs, r)
	}

	for _, e := range extra {
		r := realpath(e)
		if r == "" {
			continue
		}
		sp.dirs = append(sp.dirs, r)
	}

	sp.dirs = dedupe(sp.dirs)

	// Exact-only catastrophic: catastrophic ONLY when the path equals one of
	// these. $HOME/<random-project> is NOT catastrophic; $HOME itself is.
	sp.catastrophicExact = []string{
		"/",
		homeDir(),
		"/Users",
		"/home",
	}

	// Prefix catastrophic: anything strictly inside is catastrophic, unless
	// carved out by an explicit safe path (e.g., /var/tmp under /var).
	sp.catastrophicPrefix = []string{
		"/etc",
		"/usr",
		"/var",
		"/System",
		"/Library",
		"/Applications",
		"/bin",
		"/sbin",
		"/opt",
		"/private/etc",
		"/private/var",
	}

	// $HOME-relative protected subdirs. Treated as catastrophic when path is
	// inside $HOME/<sub>, unless explicitly carved out by safe-paths
	// (e.g., ~/Library/Caches whitelisted on macOS).
	sp.homeProtected = []string{
		".ssh", ".gnupg", ".aws", ".kube", ".docker", ".config",
		"Library", "Documents", "Desktop", "Downloads",
		"Movies", "Music", "Pictures", "Public",
	}

	sp.catastrophicExact = dedupe(sp.catastrophicExact)
	sp.catastrophicPrefix = dedupe(sp.catastrophicPrefix)

	return sp
}

// Classify determines what bucket a single rm operand falls into.
// `arg` is the literal token from the rm argv (post tilde-expansion handled
// by parser), `lexicalCwd` is the cwd at the AST point of the rm call
// (taking preceding `cd` into account; empty means use sp.cwd).
func (sp *SafePaths) Classify(arg, lexicalCwd string) (PathClassification, string) {
	if isUnresolvable(arg) {
		return PathUnresolvable, arg
	}

	cwd := lexicalCwd
	if cwd == "" {
		cwd = sp.cwd
	}

	// Normalise. Don't resolve symlinks of the FINAL operand: rm without
	// trailing slash deletes the link itself, not its target. realpath the
	// PARENT to catch /tmp/link/../etc-style escapes.
	abs := arg
	hadTrailingSlash := strings.HasSuffix(arg, "/") && arg != "/"
	if !filepath.IsAbs(abs) {
		abs = filepath.Join(cwd, abs)
	}
	abs = filepath.Clean(abs)

	parent := filepath.Dir(abs)
	parentReal := realpath(parent)
	if parentReal == "" {
		parentReal = parent // best effort
	}
	resolvedAbs := filepath.Join(parentReal, filepath.Base(abs))

	// If trailing slash, dereference the operand itself (POSIX rm semantics).
	if hadTrailingSlash {
		if r := realpath(resolvedAbs); r != "" {
			resolvedAbs = r
		}
	}

	// Also realpath the full path when it exists. Without this, "/tmp"
	// stays "/tmp" while sp.dirs has "/private/tmp" (the realpath on
	// macOS), so SafeRootSelf and SafeInside checks would miss.
	if r := realpath(resolvedAbs); r != "" {
		resolvedAbs = r
	}

	// First: is the path explicitly inside one of the safe-paths? If yes,
	// it carves out any catastrophic-prefix or home-protected match.
	// (Catastrophic-EXACT, by contrast, is unconditional — see below.)
	explicitlySafe := false
	for _, d := range sp.dirs {
		if pathInside(resolvedAbs, d) {
			explicitlySafe = true
			break
		}
	}

	// Exact-catastrophic: the path equals "/", $HOME, /Users, /home itself.
	// Not subject to carve-out — `rm -rf $HOME` stays catastrophic even when
	// $HOME contributes to the safe-paths via cwd.
	for _, c := range sp.catastrophicExact {
		if pathExactlyEqual(resolvedAbs, c) {
			return PathCatastrophic, resolvedAbs
		}
	}

	if !explicitlySafe {
		for _, c := range sp.catastrophicPrefix {
			if pathInside(resolvedAbs, c) {
				return PathCatastrophic, resolvedAbs
			}
		}
		home := homeDir()
		if home != "" {
			for _, sub := range sp.homeProtected {
				protected := filepath.Join(home, sub)
				if pathInside(resolvedAbs, protected) {
					return PathCatastrophic, resolvedAbs
				}
			}
		}
	}

	// Exact safe-path root deletion (e.g., "rm -rf /tmp").
	for _, d := range sp.dirs {
		if pathExactlyEqual(resolvedAbs, d) {
			return PathSafeRootSelf, resolvedAbs
		}
	}

	// Top-level glob inside a SHARED safe root (/tmp, /var/tmp, $TMPDIR,
	// $XDG_*). Excludes cwd subtree — a glob inside cwd is fine.
	if isSharedRootTopLevelGlob(arg, abs, sp) {
		return PathSharedRootGlob, abs
	}

	if explicitlySafe {
		return PathSafe, resolvedAbs
	}

	return PathOutsideSafe, resolvedAbs
}

// Dirs returns the active allowlist for diagnostics.
func (sp *SafePaths) Dirs() []string { return append([]string(nil), sp.dirs...) }

// --- helpers ---

func realpath(p string) string {
	if p == "" {
		return ""
	}
	abs, err := filepath.Abs(p)
	if err != nil {
		return ""
	}
	r, err := filepath.EvalSymlinks(abs)
	if err != nil {
		// Path may not exist yet; that's fine — we still want a normalised
		// abs path so caller can compare. Caller decides safety from the
		// lexical path, not from on-disk state.
		return filepath.Clean(abs)
	}
	return r
}

func homeDir() string {
	if h := os.Getenv("HOME"); h != "" {
		return h
	}
	h, _ := os.UserHomeDir()
	return h
}

// isCwdRoot returns true when cwd is structurally too high for subtree
// whitelisting to be safe (consilium P0).
func isCwdRoot(cwd string) bool {
	switch cwd {
	case "", "/", "/Users", "/home":
		return true
	}
	home := homeDir()
	if home != "" && (cwd == home || cwd == realpath(home)) {
		return true
	}
	return false
}

// pathInside returns true when child is strictly under parent (or equal).
func pathInside(child, parent string) bool {
	if child == "" || parent == "" {
		return false
	}
	if child == parent {
		return true
	}
	if !strings.HasSuffix(parent, string(filepath.Separator)) {
		parent = parent + string(filepath.Separator)
	}
	return strings.HasPrefix(child, parent)
}

func pathExactlyEqual(a, b string) bool {
	return filepath.Clean(a) == filepath.Clean(b)
}

// isUnresolvable: contains shell metacharacters that make path resolution
// uncertain at hook-time.
func isUnresolvable(arg string) bool {
	// Variables, command substitution, history expansion.
	if strings.ContainsAny(arg, "$`!") {
		return true
	}
	// Globbing characters. We only flag if they're outside cwd:
	// `rm *` in cwd is fine, `rm /etc/*` is not.
	// At classification time we don't yet know — defer to glob handling.
	return false
}

// isSharedRootTopLevelGlob detects `/tmp/*`, `/var/tmp/.*`, `$TMPDIR/*`
// patterns. cwd globs (`./*`, plain `*` when cwd is set) are NOT shared-root.
func isSharedRootTopLevelGlob(rawArg, abs string, sp *SafePaths) bool {
	if !strings.ContainsAny(rawArg, "*?[") {
		return false
	}
	// Only flag absolute globs whose base (parent dir of the glob) is
	// exactly a SHARED safe root (i.e., not the cwd subtree).
	parent := filepath.Dir(abs)
	parentReal := realpath(parent)
	for _, d := range sp.dirs {
		if d == sp.cwd && sp.cwdContributes {
			// cwd glob is fine — skip.
			continue
		}
		if pathExactlyEqual(parentReal, d) {
			return true
		}
	}
	return false
}

func dedupe(in []string) []string {
	seen := map[string]struct{}{}
	out := make([]string, 0, len(in))
	for _, s := range in {
		if _, ok := seen[s]; ok {
			continue
		}
		seen[s] = struct{}{}
		out = append(out, s)
	}
	return out
}
