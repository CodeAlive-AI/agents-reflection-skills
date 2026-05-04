package main

import (
	"fmt"
	"os"
	"path/filepath"

	"github.com/BurntSushi/toml"
)

// GlobalConfig is loaded from ~/.claude/hooks/bash-guard/config.toml (if present).
type GlobalConfig struct {
	Mode struct {
		Default string `toml:"default"` // live | shadow | dry-run
	} `toml:"mode"`
	SafePaths struct {
		Extra []string `toml:"extra"`
	} `toml:"safe_paths"`
	CatastrophicPaths struct {
		Extra []string `toml:"extra"`
	} `toml:"catastrophic_paths"`
	Rules struct {
		Disabled []string `toml:"disabled"`
	} `toml:"rules"`
}

// LoadGlobalConfig reads config.toml next to the binary. Missing file is
// not an error — defaults are returned. Malformed file is logged to stderr
// and defaults are used (fail-open per §3.6).
func LoadGlobalConfig(cfgPath string) GlobalConfig {
	var cfg GlobalConfig
	cfg.Mode.Default = "live"
	if cfgPath == "" {
		return cfg
	}
	data, err := os.ReadFile(cfgPath)
	if err != nil {
		return cfg
	}
	if err := toml.Unmarshal(data, &cfg); err != nil {
		fmt.Fprintf(os.Stderr, "bash-guard: malformed config %s: %v (using defaults)\n", cfgPath, err)
		return cfg
	}
	return cfg
}

// TrustedProjects describes which per-project .claude/bash-guard.toml files
// the user has explicitly opted into. Untrusted project configs are
// IGNORED, not allowed to widen the safe-paths or weaken rules.
type TrustedProjects struct {
	Trusted []TrustedProject `toml:"trusted"`
}

type TrustedProject struct {
	Root                       string `toml:"root"`
	HonorSafePaths             bool   `toml:"honor_safe_paths"`
	HonorCatastrophicOverrides bool   `toml:"honor_catastrophic_overrides"`
}

// LoadTrustedProjects reads ~/.claude/hooks/bash-guard/trusted-projects.toml.
// Missing file → empty trust list.
func LoadTrustedProjects(path string) TrustedProjects {
	var tp TrustedProjects
	data, err := os.ReadFile(path)
	if err != nil {
		return tp
	}
	if err := toml.Unmarshal(data, &tp); err != nil {
		fmt.Fprintf(os.Stderr, "bash-guard: malformed trusted-projects %s: %v\n", path, err)
		return tp
	}
	return tp
}

// ProjectConfig is the optional per-repo file at <repo>/.claude/bash-guard.toml.
type ProjectConfig struct {
	SafePaths struct {
		Extra []string `toml:"extra"`
	} `toml:"safe_paths"`
}

// LoadAndMergeProjectConfig walks up from cwd looking for .claude/bash-guard.toml.
// If found AND the project root is in the trust list AND honor_safe_paths is set,
// returns the project's safe paths after sanitisation:
//   - paths must resolve INSIDE the project root (no widening to /, /etc, etc.)
//   - catastrophic paths are NEVER allowed regardless of trust
//
// Returns the safe-path additions, the project root, and a non-empty stderr
// message if an untrusted config was found (caller logs at most once per session).
func LoadAndMergeProjectConfig(cwd string, tp TrustedProjects) (extras []string, projectRoot string, untrustedNotice string) {
	root, cfgPath := findProjectConfig(cwd)
	if root == "" || cfgPath == "" {
		return nil, "", ""
	}
	rootReal := realpath(root)

	var trusted *TrustedProject
	for i := range tp.Trusted {
		if realpath(tp.Trusted[i].Root) == rootReal {
			trusted = &tp.Trusted[i]
			break
		}
	}
	if trusted == nil {
		return nil, rootReal, fmt.Sprintf(
			"bash-guard: untrusted project config at %s; ignored. To trust, add to ~/.claude/hooks/bash-guard/trusted-projects.toml.",
			cfgPath)
	}

	data, err := os.ReadFile(cfgPath)
	if err != nil {
		return nil, rootReal, ""
	}
	var pc ProjectConfig
	if err := toml.Unmarshal(data, &pc); err != nil {
		fmt.Fprintf(os.Stderr, "bash-guard: malformed project config %s: %v\n", cfgPath, err)
		return nil, rootReal, ""
	}

	if !trusted.HonorSafePaths {
		return nil, rootReal, ""
	}

	for _, p := range pc.SafePaths.Extra {
		// Resolve relative paths against the project root.
		abs := p
		if !filepath.IsAbs(abs) {
			abs = filepath.Join(rootReal, abs)
		}
		abs = realpath(abs)
		if abs == "" {
			continue
		}
		// Must be inside the project root — no widening.
		if !pathInside(abs, rootReal) {
			fmt.Fprintf(os.Stderr,
				"bash-guard: project config at %s tried to whitelist %s outside project root — rejected\n",
				cfgPath, abs)
			continue
		}
		// And never inside a catastrophic root, even if user said so.
		if isCatastrophicByPrefix(abs) {
			fmt.Fprintf(os.Stderr,
				"bash-guard: project config at %s tried to whitelist catastrophic path %s — rejected\n",
				cfgPath, abs)
			continue
		}
		extras = append(extras, abs)
	}
	return extras, rootReal, ""
}

func findProjectConfig(cwd string) (root, cfgPath string) {
	dir := cwd
	for {
		candidate := filepath.Join(dir, ".claude", "bash-guard.toml")
		if _, err := os.Stat(candidate); err == nil {
			return dir, candidate
		}
		parent := filepath.Dir(dir)
		if parent == dir {
			return "", ""
		}
		dir = parent
	}
}

// isCatastrophicByPrefix is a smaller version of SafePaths.catastrophic check
// for use in config validation, where we don't yet have a SafePaths instance.
func isCatastrophicByPrefix(p string) bool {
	for _, c := range []string{"/", "/etc", "/usr", "/var", "/System", "/Library",
		"/Applications", "/bin", "/sbin", "/opt", "/private/etc", "/private/var"} {
		if pathInside(p, c) {
			return true
		}
	}
	return false
}
