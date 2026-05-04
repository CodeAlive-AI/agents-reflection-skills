package main

import (
	"fmt"
	"strings"
)

// RmRule classifies rm/unlink/rmdir/shred operations against the safe-paths
// allowlist. The rule never returns "deny"; risky operations get "ask" with
// a stable ReasonCode for tests/log analysis.
type RmRule struct{}

func (RmRule) Name() string { return "rm" }

func (RmRule) Triggers() []string {
	return []string{"rm", "unlink", "rmdir", "shred", "__inline_parse_error__", "__shell_pipe_sink__"}
}

func (r RmRule) Check(cmd ExecutedCommand, env *RuleEnv) *Decision {
	// Inline-parse-error sentinel: we tried to re-parse a `bash -c "..."` body
	// and failed. Quick-reject already saw a trigger keyword, so we must NOT
	// silently allow — ask. (consilium: post-trigger fail-open)
	if cmd.Name == "__inline_parse_error__" {
		return &Decision{
			Level:      LevelAsk,
			Rule:       r.Name(),
			Reason:     "could not parse inline shell body containing potentially destructive command",
			ReasonCode: "rm.inline_parse_error",
			Context:    fmt.Sprintf("inline_body=%q", strings.Join(cmd.Args, " ")),
		}
	}

	// Shell-pipe-sink: pipeline ends in a bare `bash`/`sh`/`zsh`/...
	// Arbitrary upstream input gets executed by the shell.
	if cmd.Name == "__shell_pipe_sink__" {
		return &Decision{
			Level:      LevelAsk,
			Rule:       r.Name(),
			Reason:     "command piped into shell evaluator (" + cmd.Path + ") — arbitrary input would be executed",
			ReasonCode: "rm.shell_pipe_sink",
			Context:    fmt.Sprintf("sink=%s", cmd.Path),
		}
	}

	// Remote command (ssh): local fs allowlist N/A.
	if cmd.Remote {
		return &Decision{
			Level:      LevelAsk,
			Rule:       r.Name(),
			Reason:     "remote " + cmd.Name + " — local safe-paths cannot be verified",
			ReasonCode: "rm.remote",
			Context:    fmt.Sprintf("argv=%q", strings.Join(append([]string{cmd.Name}, cmd.Args...), " ")),
		}
	}

	// Chrooted: path semantics differ from local fs.
	if cmd.Chrooted {
		return &Decision{
			Level:      LevelAsk,
			Rule:       r.Name(),
			Reason:     cmd.Name + " under chroot — path semantics differ from host fs",
			ReasonCode: "rm.chrooted",
			Context:    fmt.Sprintf("argv=%q", strings.Join(append([]string{cmd.Name}, cmd.Args...), " ")),
		}
	}

	// xargs/parallel/etc — args from stdin are unknown.
	if cmd.StdinArgs {
		return &Decision{
			Level:      LevelAsk,
			Rule:       r.Name(),
			Reason:     cmd.Name + " with arguments piped from stdin (xargs/parallel) — targets unknown",
			ReasonCode: "rm.stdin_args",
			Context:    fmt.Sprintf("argv=%q", strings.Join(append([]string{cmd.Name}, cmd.Args...), " ")),
		}
	}

	flags, operands, hasNoPreserveRoot := parseRmArgs(cmd.Args)
	_ = flags

	if len(operands) == 0 {
		// Pure flags-only or `rm --` with no operands. Bash itself errors;
		// no decision to make.
		return nil
	}

	// Per-operand classification; first concern wins.
	var worst *Decision
	for _, op := range operands {
		d := classifyOperand(cmd, op, env)
		if d == nil {
			continue
		}
		if worst == nil || severityRank(d.ReasonCode) > severityRank(worst.ReasonCode) {
			worst = d
		}
	}
	if worst == nil {
		return nil
	}

	// --no-preserve-root is an escalation indicator regardless of target.
	if hasNoPreserveRoot {
		worst.Context = strings.TrimSpace(worst.Context + " escalation=--no-preserve-root")
	}
	return worst
}

func classifyOperand(cmd ExecutedCommand, op string, env *RuleEnv) *Decision {
	cls, resolved := env.SafePaths.Classify(op, cmd.LexicalCwd)
	switch cls {
	case PathSafe:
		return nil
	case PathOutsideSafe:
		return &Decision{
			Level:      LevelAsk,
			Rule:       "rm",
			Reason:     fmt.Sprintf("%s target %q resolves outside safe paths", cmd.Name, resolved),
			ReasonCode: "rm.outside_safe_path",
			Context:    fmt.Sprintf("operand=%q resolved=%q safe_paths=%s", op, resolved, strings.Join(env.SafePaths.Dirs(), ",")),
		}
	case PathCatastrophic:
		return &Decision{
			Level:      LevelAsk,
			Rule:       "rm",
			Reason:     fmt.Sprintf("%s target %q is a catastrophic path", cmd.Name, resolved),
			ReasonCode: "rm.catastrophic",
			Context:    fmt.Sprintf("operand=%q resolved=%q", op, resolved),
		}
	case PathSafeRootSelf:
		return &Decision{
			Level:      LevelAsk,
			Rule:       "rm",
			Reason:     fmt.Sprintf("%s target %q is the safe-path root itself", cmd.Name, resolved),
			ReasonCode: "rm.delete_safe_root",
			Context:    fmt.Sprintf("operand=%q", op),
		}
	case PathSharedRootGlob:
		return &Decision{
			Level:      LevelAsk,
			Rule:       "rm",
			Reason:     fmt.Sprintf("%s top-level glob inside shared safe root: %q", cmd.Name, op),
			ReasonCode: "rm.shared_root_glob",
			Context:    fmt.Sprintf("operand=%q", op),
		}
	case PathUnresolvable:
		return &Decision{
			Level:      LevelAsk,
			Rule:       "rm",
			Reason:     fmt.Sprintf("%s target %q has unresolvable variables/substitutions", cmd.Name, op),
			ReasonCode: "rm.unresolvable",
			Context:    fmt.Sprintf("operand=%q", op),
		}
	}
	return nil
}

// severityRank gives an ordering so we surface the most concerning operand.
// Catastrophic > unresolvable > outside-safe > glob > root-self > safe.
func severityRank(code string) int {
	switch code {
	case "rm.catastrophic":
		return 100
	case "rm.inline_parse_error":
		return 95
	case "rm.remote":
		return 90
	case "rm.chrooted":
		return 85
	case "rm.stdin_args":
		return 80
	case "rm.unresolvable":
		return 70
	case "rm.outside_safe_path":
		return 60
	case "rm.delete_safe_root":
		return 50
	case "rm.shared_root_glob":
		return 40
	}
	return 0
}

// parseRmArgs parses real GNU/BSD rm argv. Handles:
//   - end-of-options sentinel `--`
//   - combined short flags `-rf`, `-fr`, `-rfv`
//   - long flags with `=` value, e.g., `--interactive=never`
//   - `--no-preserve-root` (returned as a separate flag for context)
//   - operands beginning with `-` after `--`
//
// Returns: (flags, operands, hasNoPreserveRoot).
func parseRmArgs(args []string) (flags []string, operands []string, hasNoPreserveRoot bool) {
	endOfOpts := false
	for _, a := range args {
		if endOfOpts {
			operands = append(operands, a)
			continue
		}
		if a == "--" {
			endOfOpts = true
			continue
		}
		if a == "--no-preserve-root" {
			hasNoPreserveRoot = true
			flags = append(flags, a)
			continue
		}
		if strings.HasPrefix(a, "--") {
			flags = append(flags, a)
			continue
		}
		if strings.HasPrefix(a, "-") && len(a) > 1 {
			// Combined short flags (-rf, -rfv). rm has no short flags
			// that take values, so this is straightforward.
			flags = append(flags, a)
			continue
		}
		operands = append(operands, a)
	}
	return
}
