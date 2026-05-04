package main

import "strings"

// stripExecutorPrefix removes one layer of executor wrapper from argv,
// returning the stripped argv and a flag indicating whether a wrapper was
// recognised. The walker calls this in a loop until isWrapper=false.
//
// Wrappers covered: sudo/doas, env, command/builtin/exec, time/nice/nohup/ionice/setsid,
// timeout, chroot, ssh (the special remote case is handled here).
//
// xargs / find / shell-evaluators (-c) / eval are NOT here — they get
// dedicated handlers in parser.go because they synthesize new ExecutedCommands.
func stripExecutorPrefix(argv []string, ctx walkContext) ([]string, bool, walkContext) {
	if len(argv) == 0 {
		return argv, false, ctx
	}
	cmd := basenameLower(argv[0])
	switch cmd {
	case "sudo", "doas":
		return stripSudoLike(argv, ctx)
	case "env":
		return stripEnv(argv, ctx)
	case "command", "builtin":
		return stripCommandBuiltin(argv, ctx)
	case "exec":
		return stripExec(argv, ctx)
	case "time", "nice", "nohup", "ionice", "setsid":
		return stripUntilNonFlag(argv, ctx, 1)
	case "timeout", "gtimeout":
		// timeout DURATION command... — duration is a non-flag operand,
		// skip flags first then one mandatory operand.
		return stripUntilNonFlag(argv, ctx, 2)
	case "chroot":
		newCtx := ctx
		newCtx.chrooted = true
		return stripUntilNonFlag(argv, newCtx, 2) // newroot + cmd
	case "ssh":
		return stripSSH(argv, ctx)
	case "rsync":
		// rsync only matters if --rsync-path runs a remote command; rare,
		// not worth special handling — leave as-is, rules won't fire.
		return argv, false, ctx
	}
	return argv, false, ctx
}

// stripSudoLike: skip sudo flags then return the inner argv.
func stripSudoLike(argv []string, ctx walkContext) ([]string, bool, walkContext) {
	i := 1
	for i < len(argv) {
		a := argv[i]
		if a == "--" {
			i++
			break
		}
		if !strings.HasPrefix(a, "-") {
			break
		}
		// flags that take an argument
		if a == "-u" || a == "-g" || a == "-C" || a == "-D" || a == "-h" || a == "-p" || a == "-T" {
			i += 2
			continue
		}
		// long form with value
		if strings.HasPrefix(a, "--user=") || strings.HasPrefix(a, "--group=") ||
			strings.HasPrefix(a, "--chdir=") || strings.HasPrefix(a, "--prompt=") ||
			strings.HasPrefix(a, "--type=") {
			i++
			continue
		}
		// long form taking next token
		if a == "--user" || a == "--group" || a == "--chdir" || a == "--prompt" || a == "--type" {
			i += 2
			continue
		}
		// standalone flags
		i++
	}
	if i >= len(argv) {
		return argv, false, ctx
	}
	return argv[i:], true, ctx
}

// stripEnv: skip leading KEY=VALUE assignments and env's own flags.
func stripEnv(argv []string, ctx walkContext) ([]string, bool, walkContext) {
	i := 1
	for i < len(argv) {
		a := argv[i]
		if a == "--" {
			i++
			break
		}
		if a == "-i" || a == "--ignore-environment" || a == "-0" || a == "--null" || a == "-v" {
			i++
			continue
		}
		if a == "-u" || a == "--unset" {
			i += 2
			continue
		}
		if strings.HasPrefix(a, "--unset=") {
			i++
			continue
		}
		if strings.HasPrefix(a, "-S") || strings.HasPrefix(a, "--split-string") {
			// `env -S ...` re-parses string — bail (rare, conservative).
			return argv, false, ctx
		}
		// KEY=VALUE
		if eq := strings.IndexByte(a, '='); eq > 0 && !strings.HasPrefix(a, "-") {
			i++
			continue
		}
		break
	}
	if i >= len(argv) {
		return argv, false, ctx
	}
	return argv[i:], true, ctx
}

func stripCommandBuiltin(argv []string, ctx walkContext) ([]string, bool, walkContext) {
	i := 1
	for i < len(argv) {
		a := argv[i]
		if a == "--" {
			i++
			break
		}
		if a == "-p" || a == "-v" || a == "-V" {
			i++
			continue
		}
		break
	}
	if i >= len(argv) {
		return argv, false, ctx
	}
	return argv[i:], true, ctx
}

func stripExec(argv []string, ctx walkContext) ([]string, bool, walkContext) {
	i := 1
	for i < len(argv) {
		a := argv[i]
		if a == "--" {
			i++
			break
		}
		if a == "-c" || a == "-l" || a == "-a" {
			if a == "-a" {
				i += 2
				continue
			}
			i++
			continue
		}
		break
	}
	if i >= len(argv) {
		return argv, false, ctx
	}
	return argv[i:], true, ctx
}

// stripUntilNonFlag: skip leading flags, then `mandatoryOperands` further
// non-flag tokens (e.g., duration arg of timeout, newroot of chroot).
func stripUntilNonFlag(argv []string, ctx walkContext, mandatoryOperands int) ([]string, bool, walkContext) {
	i := 1
	// Skip flags first
	for i < len(argv) {
		a := argv[i]
		if a == "--" {
			i++
			break
		}
		if !strings.HasPrefix(a, "-") {
			break
		}
		i++
	}
	// Skip mandatory operands
	for k := 1; k < mandatoryOperands; k++ {
		if i >= len(argv) {
			return argv, false, ctx
		}
		i++
	}
	if i >= len(argv) {
		return argv, false, ctx
	}
	return argv[i:], true, ctx
}

// extractSSHRemoteBody peels off ssh's flags and host, returns the joined
// remote-command tail. Used to re-parse the remote command as bash (the
// remote shell will do the same on the other end). Returns ok=false when
// no remote command is present (pure interactive ssh).
func extractSSHRemoteBody(argv []string) (string, bool) {
	if len(argv) < 2 {
		return "", false
	}
	flagsWithValue := map[string]bool{
		"-l": true, "-i": true, "-p": true, "-o": true, "-F": true, "-J": true,
		"-c": true, "-m": true, "-S": true, "-W": true, "-w": true, "-D": true,
		"-L": true, "-R": true, "-Q": true, "-O": true, "-B": true, "-b": true,
		"-e": true, "-E": true, "-I": true,
	}
	i := 1
	for i < len(argv) {
		a := argv[i]
		if a == "--" {
			i++
			break
		}
		if flagsWithValue[a] {
			i += 2
			continue
		}
		if strings.HasPrefix(a, "-") && len(a) > 1 {
			i++
			continue
		}
		break
	}
	// argv[i] is host
	if i >= len(argv) {
		return "", false
	}
	i++
	if i >= len(argv) {
		return "", false
	}
	return strings.Join(argv[i:], " "), true
}

// stripSSH: legacy (kept for compatibility — no longer used since ssh is
// now handled directly in applyUnwrap via extractSSHRemoteBody).
// Retained in case future executors need its shape; safe to delete.
func stripSSH(argv []string, ctx walkContext) ([]string, bool, walkContext) {
	i := 1
	// Skip ssh flags. ssh has many; we handle the common ones with values.
	flagsWithValue := map[string]bool{
		"-l": true, "-i": true, "-p": true, "-o": true, "-F": true, "-J": true,
		"-c": true, "-m": true, "-S": true, "-W": true, "-w": true, "-D": true,
		"-L": true, "-R": true, "-Q": true, "-O": true, "-B": true, "-b": true,
		"-e": true, "-E": true, "-I": true,
	}
	for i < len(argv) {
		a := argv[i]
		if a == "--" {
			i++
			break
		}
		if flagsWithValue[a] {
			i += 2
			continue
		}
		if strings.HasPrefix(a, "-") && len(a) > 1 {
			// Combined short flags or unknown long flag — assume standalone.
			i++
			continue
		}
		break
	}
	// Now argv[i] should be host (or user@host).
	if i >= len(argv) {
		return argv, false, ctx
	}
	i++
	if i >= len(argv) {
		return argv, false, ctx
	}
	newCtx := ctx
	newCtx.remote = true
	return argv[i:], true, newCtx
}

// isShellEvaluator: bash/sh/zsh/dash/fish/ksh used as a command interpreter.
// Recognised by basename only.
func isShellEvaluator(base string) bool {
	switch base {
	case "bash", "sh", "zsh", "dash", "fish", "ksh", "ash", "busybox":
		return true
	}
	return false
}

// extractDashCBody: scan args for `-c <body>`. Returns (body, true) when
// found. Allows extra flags / positional args around it.
func extractDashCBody(args []string) (string, bool) {
	for i, a := range args {
		if a == "-c" && i+1 < len(args) {
			return args[i+1], true
		}
		if strings.HasPrefix(a, "-c=") {
			return strings.TrimPrefix(a, "-c="), true
		}
	}
	return "", false
}

// handleXargs: synthesize a virtual ExecutedCommand whose args are unknown.
// Rules see StdinArgs=true and decide ask/allow accordingly.
func (w *walker) handleXargs(argv []string, ctx walkContext) {
	// Skip xargs's own flags. The first non-flag token is the command name
	// xargs will execute.
	i := 1
	for i < len(argv) && strings.HasPrefix(argv[i], "-") {
		// Some xargs flags take values: -I REPL, -L N, -n N, -P N, -d D, -E EOF, -a FILE, -s SIZE
		switch argv[i] {
		case "-I", "-L", "-n", "-P", "-d", "-E", "-a", "-s", "--replace", "--max-lines",
			"--max-args", "--max-procs", "--delimiter", "--eof", "--arg-file", "--max-chars":
			i += 2
			continue
		}
		if strings.HasPrefix(argv[i], "--replace=") ||
			strings.HasPrefix(argv[i], "--max-lines=") ||
			strings.HasPrefix(argv[i], "--max-args=") ||
			strings.HasPrefix(argv[i], "--max-procs=") ||
			strings.HasPrefix(argv[i], "--delimiter=") ||
			strings.HasPrefix(argv[i], "--eof=") ||
			strings.HasPrefix(argv[i], "--arg-file=") ||
			strings.HasPrefix(argv[i], "--max-chars=") {
			i++
			continue
		}
		i++
	}
	if i >= len(argv) {
		return
	}
	innerCtx := ctx
	innerCtx.stdinArgs = true
	w.applyUnwrap(argv[i:], innerCtx)
}

// handleFind: detect -delete / -exec rm / -execdir rm. When found, synthesize
// a virtual rm ExecutedCommand whose targets are the search roots (path
// arguments of find before the predicate begins).
func (w *walker) handleFind(argv []string, ctx walkContext) {
	if len(argv) < 2 {
		return
	}
	roots := []string{}
	predicateStart := -1
	for i := 1; i < len(argv); i++ {
		a := argv[i]
		if strings.HasPrefix(a, "-") {
			predicateStart = i
			break
		}
		// option-like: H, L, P, O — only at very front
		if i == 1 && (a == "-H" || a == "-L" || a == "-P" || strings.HasPrefix(a, "-O")) {
			continue
		}
		roots = append(roots, a)
	}
	if len(roots) == 0 {
		// Default search root is "." when none given.
		roots = []string{"."}
	}
	if predicateStart < 0 {
		return // nothing to inspect, no -delete/-exec
	}
	deletes := false
	execRm := false
	for i := predicateStart; i < len(argv); i++ {
		a := argv[i]
		if a == "-delete" {
			deletes = true
			continue
		}
		if a == "-exec" || a == "-execdir" || a == "-ok" || a == "-okdir" {
			if i+1 < len(argv) {
				next := basenameLower(argv[i+1])
				if next == "rm" || next == "unlink" || next == "rmdir" || next == "shred" {
					execRm = true
				}
			}
		}
	}
	if !deletes && !execRm {
		return
	}
	// Synthesize one virtual rm operation per root.
	w.executed = append(w.executed, ExecutedCommand{
		Name:       "rm",
		Path:       "find",
		Args:       append([]string{"-rf", "--"}, roots...),
		StdinArgs:  ctx.stdinArgs,
		Chrooted:   ctx.chrooted,
		Remote:     ctx.remote,
		FromEval:   ctx.fromEval,
		LexicalCwd: w.lexicalCwd,
	})
}
