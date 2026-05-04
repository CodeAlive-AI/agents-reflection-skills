// Command bash-guard is a Claude Code PreToolUse:Bash safety hook.
// It reads a JSON envelope on stdin, evaluates the wrapped Bash command
// against a set of rules (rm/unlink/rmdir/shred + future rules), and emits
// a JSON envelope on stdout requesting "allow" or "ask" — never "deny".
//
// Design doc: ../DESIGN.md
package main

import (
	"encoding/json"
	"fmt"
	"io"
	"os"
	"path/filepath"
	"regexp"
	"strings"
	"time"
)

// HookInput is the JSON envelope Claude Code sends.
type HookInput struct {
	HookEventName  string         `json:"hook_event_name"`
	ToolName       string         `json:"tool_name"`
	ToolInput      ToolInput      `json:"tool_input"`
	SessionID      string         `json:"session_id"`
	Cwd            string         `json:"cwd"`
	PermissionMode string         `json:"permission_mode"`
}

type ToolInput struct {
	Command string `json:"command"`
}

// HookOutput is what Claude Code expects on stdout.
type HookOutput struct {
	HookSpecificOutput HookSpecific `json:"hookSpecificOutput"`
}

type HookSpecific struct {
	HookEventName            string `json:"hookEventName"`
	PermissionDecision       string `json:"permissionDecision"`
	PermissionDecisionReason string `json:"permissionDecisionReason,omitempty"`
	AdditionalContext        string `json:"additionalContext,omitempty"`
}

func main() {
	start := time.Now()
	exitWithAllow := func(reason string) {
		emit(HookOutput{HookSpecificOutput: HookSpecific{
			HookEventName:      "PreToolUse",
			PermissionDecision: "allow",
		}})
		os.Exit(0)
	}

	// --- self-test mode ---
	if len(os.Args) > 1 && os.Args[1] == "--selftest" {
		runSelfTest()
		return
	}
	if len(os.Args) > 1 && os.Args[1] == "--version" {
		fmt.Println(versionString())
		return
	}

	// --- read input ---
	rawInput, err := io.ReadAll(os.Stdin)
	if err != nil {
		fmt.Fprintf(os.Stderr, "bash-guard: read stdin: %v\n", err)
		exitWithAllow("read error")
		return
	}
	var in HookInput
	if err := json.Unmarshal(rawInput, &in); err != nil {
		// Invalid input — fail-open allow.
		fmt.Fprintf(os.Stderr, "bash-guard: malformed JSON input: %v\n", err)
		exitWithAllow("malformed input")
		return
	}
	if in.ToolName != "Bash" {
		exitWithAllow("non-bash")
		return
	}
	cmd := in.ToolInput.Command
	if cmd == "" {
		exitWithAllow("empty command")
		return
	}

	// --- mode resolution ---
	binDir := selfDir()
	cfg := LoadGlobalConfig(filepath.Join(binDir, "config.toml"))
	mode := cfg.Mode.Default
	if v := os.Getenv("BASH_GUARD_SHADOW"); v != "" && v != "0" {
		mode = "shadow"
	}
	if v := os.Getenv("BASH_GUARD_DRY_RUN"); v != "" && v != "0" {
		mode = "dry-run"
	}

	// --- registry ---
	reg := newRegistry(RmRule{}, SupabaseRule{}, InfraRule{}, PaasRule{}, DbClientRule{}, GitRule{})
	triggers := reg.triggerSet()

	// --- safe paths ---
	tp := LoadTrustedProjects(filepath.Join(binDir, "trusted-projects.toml"))
	projectExtras, _, untrustedNotice := LoadAndMergeProjectConfig(in.Cwd, tp)
	if untrustedNotice != "" {
		fmt.Fprintln(os.Stderr, untrustedNotice)
	}
	allExtras := append([]string(nil), cfg.SafePaths.Extra...)
	allExtras = append(allExtras, projectExtras...)
	sp := NewSafePaths(in.Cwd, allExtras)

	// --- pipeline ---
	decision := evaluate(cmd, triggers, reg, &RuleEnv{HookCwd: in.Cwd, SafePaths: sp})

	// --- shadow / dry-run override ---
	wouldDecide := decision.Level.String()
	switch mode {
	case "shadow", "dry-run":
		// Always emit allow; record what would have happened.
		emit(HookOutput{HookSpecificOutput: HookSpecific{
			HookEventName:      "PreToolUse",
			PermissionDecision: "allow",
		}})
	default:
		emit(HookOutput{HookSpecificOutput: HookSpecific{
			HookEventName:            "PreToolUse",
			PermissionDecision:       decision.Level.String(),
			PermissionDecisionReason: decision.Reason,
			AdditionalContext:        buildAdditionalContext(decision),
		}})
	}

	// --- audit ---
	entry := AuditEntry{
		TS:          nowISO(),
		Mode:        mode,
		Decision:    decision.Level.String(),
		Rule:        decision.Rule,
		ReasonCode:  decision.ReasonCode,
		LatencyMS:   float64(time.Since(start).Microseconds()) / 1000.0,
		CommandHash: hashCommand(cmd),
		CommandLen:  len(cmd),
	}
	if mode == "dry-run" || mode == "shadow" {
		entry.WouldDecide = wouldDecide
	}
	if os.Getenv("BASH_GUARD_LOG_COMMANDS") != "" {
		entry.Command = cmd
	}
	writeAudit(entry)
}

// evaluate runs the full pipeline: quick reject → parse → unwrap → rule eval → aggregate.
// Returns a Decision (always Allow or Ask).
func evaluate(cmd string, triggers []string, reg *registry, env *RuleEnv) Decision {
	if !quickReject(cmd, triggers) {
		// Quick reject: no trigger keyword. Allow.
		// (False negatives here are OK — parser would classify them safely.)
	} else {
		// Has at least one trigger keyword somewhere. Parse + classify.
		parsed, err := ParseCommand(cmd)
		if err != nil {
			// Asymmetric fail-open: trigger keyword present + parse error
			// → ask. Without a trigger we'd allow, but we already saw one.
			return Decision{
				Level:      LevelAsk,
				Rule:       "guard",
				Reason:     "could not parse command containing potentially destructive keyword",
				ReasonCode: "guard.parse_error_after_trigger",
				Context:    fmt.Sprintf("parse_error=%v", err),
			}
		}
		decisions := reg.evaluate(parsed, env)
		return Aggregate(decisions)
	}
	return Aggregate(nil)
}

// quickReject: false → no trigger keyword anywhere, allow without parsing.
//
// The trigger set is the union of:
//   - rule keywords (rm, unlink, rmdir, shred — actual rule targets)
//   - executor keywords (sudo, env, bash, sh, eval, xargs, find, ...) — words
//     that the parser must descend into to discover an underlying rule keyword.
//
// Without executor keywords here, `find /etc -delete` would skip parsing
// and silently allow.
func quickReject(cmd string, triggers []string) bool {
	all := append([]string(nil), triggers...)
	all = append(all, parserDescentKeywords...)
	if len(all) == 0 {
		return false
	}
	parts := make([]string, 0, len(all))
	for _, t := range all {
		parts = append(parts, regexp.QuoteMeta(t))
	}
	re := regexp.MustCompile(`\b(?:` + strings.Join(parts, "|") + `)\b`)
	return re.MatchString(cmd)
}

// parserDescentKeywords lists every command name that the parser must
// descend into (executors / shell evaluators / find / xargs) — these are
// the commands whose unwrap can SURFACE a rule trigger that wasn't visible
// at the top level.
//
// Filing them here (vs in the unwrap.go switch) keeps quickReject alone
// authoritative about "should we even parse?".
var parserDescentKeywords = []string{
	"sudo", "doas", "env", "command", "builtin", "exec",
	"time", "nice", "nohup", "ionice", "setsid",
	"timeout", "gtimeout", "chroot",
	"ssh",
	"bash", "sh", "zsh", "dash", "fish", "ksh", "ash", "busybox",
	"eval",
	"xargs", "find", "parallel", "watch", "flock",
}

func buildAdditionalContext(d Decision) string {
	// Allow decisions don't need additionalContext — the user never sees it
	// and it just bloats audit logs. Only attach context to ask decisions
	// where the user benefits from "why".
	if d.Level != LevelAsk {
		return ""
	}
	if d.ReasonCode == "" && d.Context == "" {
		return ""
	}
	parts := []string{"code:" + d.ReasonCode}
	if d.Context != "" {
		parts = append(parts, d.Context)
	}
	return strings.Join(parts, " ")
}

func emit(out HookOutput) {
	enc := json.NewEncoder(os.Stdout)
	enc.SetEscapeHTML(false)
	_ = enc.Encode(out)
}

// selfDir returns the directory containing the running binary (or src dir
// during development). Used to locate config.toml and trusted-projects.toml.
func selfDir() string {
	exe, err := os.Executable()
	if err != nil {
		return "."
	}
	resolved, err := filepath.EvalSymlinks(exe)
	if err != nil {
		resolved = exe
	}
	return filepath.Dir(resolved)
}

func versionString() string {
	return "bash-guard 0.2.0"
}

// runSelfTest is a manual smoke check: it runs the parser on a couple of
// fixed commands and prints the resulting decision summary. Real coverage
// lives in *_test.go.
func runSelfTest() {
	cases := []struct{ name, cmd, cwd string }{
		{"FP-1 heredoc with apostrophes", "cat > /tmp/x <<'EOF'\nWe use find and rm a lot. Don't break.\nEOF", "/tmp"},
		{"FP-2 rm in /tmp", "cd /tmp && rm -rf ci-results && mkdir ci-results", "/Users/test/myproject"},
		{"catastrophic /etc", "rm -rf /etc/nginx", "/Users/test/myproject"},
		{"safe cwd subdir", "rm -rf node_modules", "/Users/test/myproject"},
	}
	reg := newRegistry(RmRule{})
	triggers := reg.triggerSet()
	for _, c := range cases {
		sp := NewSafePaths(c.cwd, nil)
		d := evaluate(c.cmd, triggers, reg, &RuleEnv{HookCwd: c.cwd, SafePaths: sp})
		fmt.Printf("[%s] cwd=%s  ->  %s (rule=%s code=%s)\n", c.name, c.cwd, d.Level, d.Rule, d.ReasonCode)
	}
}
