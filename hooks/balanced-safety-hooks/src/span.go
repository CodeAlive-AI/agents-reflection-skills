package main

// SpanKind classifies AST subtrees so rules only fire on real executable code,
// not on strings, heredoc bodies, or assignments where dangerous-looking words
// happen to appear (e.g., the word "find" inside a heredoc body — FP-1).
type SpanKind int

const (
	// SpanExecuted: a real command being invoked (after executor unwrap).
	SpanExecuted SpanKind = iota
	// SpanData: literal data — string contents, assignment RHS — bash doesn't
	// execute these on its own.
	SpanData
	// SpanHeredocBody: the body of a heredoc; treated as Data.
	SpanHeredocBody
	// SpanInlineCode: a string passed to a known shell evaluator
	// (`bash -c "..."`, `eval ...`). Re-parsed as Executed.
	SpanInlineCode
)

// ExecutedCommand is the unit on which rules operate.
// One Bash submission can produce multiple of these (chains, pipelines,
// command substitutions, unwrapped wrappers).
type ExecutedCommand struct {
	Name string   // base name of the command, e.g., "rm" (not "/bin/rm")
	Path string   // original path token, e.g., "/usr/bin/rm" or "rm"
	Args []string // remaining args after Name

	// Provenance flags propagated from the wrapper unwrap pass.
	// Rules use these to decide between allow/ask when local context
	// (e.g., the safe-paths allowlist) doesn't apply.
	StdinArgs bool // args come from stdin (xargs, parallel)
	Chrooted  bool // running under chroot — paths reinterpreted
	Remote    bool // ssh/scp remote command — local fs context N/A
	FromEval  bool // came from eval/bash -c (audit-only marker)

	// LexicalCwd is the cwd as it appears at the AST point of this command,
	// taking into account preceding `cd <path>` in the same statement chain.
	// Empty means "use the global cwd from hook input".
	LexicalCwd string
}
