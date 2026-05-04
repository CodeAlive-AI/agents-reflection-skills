package main

import (
	"fmt"
	"strings"

	"mvdan.cc/sh/v3/syntax"
)

// ParseError is the typed error returned for syntactically invalid commands,
// distinct from rule evaluation errors. Callers treat it as a fail-open
// candidate (allow if no trigger keyword in §3.6 quick-reject).
type ParseError struct{ Inner error }

func (e *ParseError) Error() string { return "parse error: " + e.Inner.Error() }
func (e *ParseError) Unwrap() error { return e.Inner }

// ParseCommand parses a Bash command and returns the unwrapped list of
// ExecutedCommands ready for rule evaluation.
func ParseCommand(cmd string) ([]ExecutedCommand, error) {
	parser := syntax.NewParser(syntax.KeepComments(false), syntax.Variant(syntax.LangBash))
	file, err := parser.Parse(strings.NewReader(cmd), "")
	if err != nil {
		return nil, &ParseError{Inner: err}
	}

	w := &walker{}
	w.walkFile(file)
	return w.executed, nil
}

// walker traverses the AST, accumulating ExecutedCommands and tracking
// lexical cwd from preceding `cd` statements.
type walker struct {
	executed   []ExecutedCommand
	lexicalCwd string // "" = use hook input cwd
}

func (w *walker) walkFile(f *syntax.File) {
	for _, stmt := range f.Stmts {
		w.walkStmt(stmt, walkContext{})
	}
}

// walkContext propagates per-branch state (chrooted, remote, etc.) into
// nested AST traversal.
type walkContext struct {
	chrooted  bool
	remote    bool
	stdinArgs bool
	fromEval  bool
}

func (w *walker) walkStmt(stmt *syntax.Stmt, ctx walkContext) {
	if stmt == nil || stmt.Cmd == nil {
		return
	}
	switch c := stmt.Cmd.(type) {
	case *syntax.CallExpr:
		w.handleCall(c, ctx)
	case *syntax.BinaryCmd:
		if c.Op == syntax.Pipe || c.Op == syntax.PipeAll {
			w.walkPipeline(c, ctx)
		} else {
			// && || — process both sides (cwd from left propagates to right
			// only when the connector is `&&` and the left was `cd`).
			w.walkStmt(c.X, ctx)
			w.walkStmt(c.Y, ctx)
		}
	case *syntax.Block:
		for _, s := range c.Stmts {
			w.walkStmt(s, ctx)
		}
	case *syntax.Subshell:
		// (cmd1; cmd2) — subshell preserves outer cwd for the parent.
		// Use a copy walker so cd inside subshell doesn't leak.
		sub := &walker{lexicalCwd: w.lexicalCwd}
		for _, s := range c.Stmts {
			sub.walkStmt(s, ctx)
		}
		w.executed = append(w.executed, sub.executed...)
	case *syntax.IfClause:
		w.walkIfClause(c, ctx)
	case *syntax.WhileClause:
		w.walkClauseList(c.Cond, ctx)
		w.walkClauseList(c.Do, ctx)
	case *syntax.ForClause:
		w.walkClauseList(c.Do, ctx)
	case *syntax.CaseClause:
		for _, item := range c.Items {
			w.walkClauseList(item.Stmts, ctx)
		}
	case *syntax.FuncDecl:
		// Function body — descend.
		if c.Body != nil {
			w.walkStmt(c.Body, ctx)
		}
	case *syntax.DeclClause:
		// declare/typeset/local/export ... — args are assignments (Data).
	}
}

func (w *walker) walkClauseList(stmts []*syntax.Stmt, ctx walkContext) {
	for _, s := range stmts {
		w.walkStmt(s, ctx)
	}
}

// walkPipeline handles `a | b | ...`. It walks each stage normally so any
// `rm` inside an upstream stage still gets evaluated, and additionally
// detects the dangerous shape `<anything> | bash` (or sh/zsh/etc., no -c) —
// piping data into a shell evaluator means arbitrary input is executed.
//
// On detection, it appends a synthetic ExecutedCommand named
// "__shell_pipe_sink__" so the rm rule (which has it in its trigger set)
// emits an ask. We do this rather than re-parsing the upstream because
// upstream input is generally not statically reducible to a single string.
func (w *walker) walkPipeline(c *syntax.BinaryCmd, ctx walkContext) {
	// Walk every stage of the pipeline normally.
	stages := flattenPipeline(c)
	for _, stage := range stages {
		w.walkStmt(stage, ctx)
	}

	// Inspect the rightmost stage.
	last := stages[len(stages)-1]
	if last == nil || last.Cmd == nil {
		return
	}
	call, ok := last.Cmd.(*syntax.CallExpr)
	if !ok {
		return
	}
	args, _ := flattenWords(call.Args)
	if len(args) == 0 {
		return
	}
	base := basenameLower(args[0])
	if !isShellEvaluator(base) {
		return
	}
	// If the shell is invoked with `-c <body>`, that body is an inline-code
	// span the regular handleCall path already deals with. Skip here so we
	// don't double-ask.
	if _, hasDashC := extractDashCBody(args[1:]); hasDashC {
		return
	}
	// Dangerous shape: arbitrary input piped into a bare shell evaluator.
	w.executed = append(w.executed, ExecutedCommand{
		Name:       "__shell_pipe_sink__",
		Path:       args[0],
		Args:       append([]string(nil), args[1:]...),
		LexicalCwd: w.lexicalCwd,
	})
}

// flattenPipeline turns a left-recursive BinaryCmd-with-pipe tree into a
// flat list of stages.
func flattenPipeline(c *syntax.BinaryCmd) []*syntax.Stmt {
	var out []*syntax.Stmt
	var visit func(s *syntax.Stmt)
	visit = func(s *syntax.Stmt) {
		if s == nil {
			return
		}
		if bc, ok := s.Cmd.(*syntax.BinaryCmd); ok && (bc.Op == syntax.Pipe || bc.Op == syntax.PipeAll) {
			visit(bc.X)
			visit(bc.Y)
			return
		}
		out = append(out, s)
	}
	visit(c.X)
	visit(c.Y)
	return out
}

// walkIfClause descends into an if/elif/else chain. mvdan's IfClause.Else is
// itself a *IfClause (with empty Cond for "naked" else), so we recurse.
func (w *walker) walkIfClause(c *syntax.IfClause, ctx walkContext) {
	if c == nil {
		return
	}
	w.walkClauseList(c.Cond, ctx)
	w.walkClauseList(c.Then, ctx)
	if c.Else != nil {
		w.walkIfClause(c.Else, ctx)
	}
}

// handleCall is the heart of unwrapping. It collects the argv for a CallExpr,
// applies the executor unwrap table (see unwrap.go), and either:
//   - records an ExecutedCommand, or
//   - recurses with re-parsed inline code (bash -c "..."), or
//   - tracks a `cd` to update lexicalCwd for subsequent commands.
func (w *walker) handleCall(call *syntax.CallExpr, ctx walkContext) {
	if call == nil {
		return
	}
	// Inspect command substitutions / process substitutions inside the args.
	// They run independently of this CallExpr.
	w.scanForNestedExecutions(call, ctx)

	argv, ok := flattenWords(call.Args)
	if !ok {
		// Could not statically resolve all words — record the command
		// verbatim with its first arg as Name. Rules like rm will mark
		// such targets as Unresolvable.
	}
	if len(argv) == 0 {
		return
	}

	// Track cd for lexical cwd propagation.
	if argv[0] == "cd" && len(argv) > 1 {
		// Plain literal cd target only.
		if !containsShellMeta(argv[1]) {
			w.lexicalCwd = argv[1]
		}
		return
	}

	w.applyUnwrap(argv, ctx)
}

// applyUnwrap: dispatch the argv through the executor unwrap table,
// possibly recursing on inline-code arguments.
func (w *walker) applyUnwrap(argv []string, ctx walkContext) {
	for {
		if len(argv) == 0 {
			return
		}
		base := basenameLower(argv[0])

		// ssh: the remote command tail is a shell-evaluator-like context.
		// Skip ssh's own flags and host, then re-parse the joined remote
		// command as bash. Handled BEFORE generic stripExecutorPrefix so we
		// don't end up with the remote command as a single opaque arg.
		if base == "ssh" {
			body, ok := extractSSHRemoteBody(argv)
			if !ok || strings.TrimSpace(body) == "" {
				return // pure interactive ssh — nothing to inspect
			}
			subCtx := ctx
			subCtx.remote = true
			w.reparseAndWalk(body, subCtx, true /*remote*/)
			return
		}

		// Shell-evaluator -c "..."
		if isShellEvaluator(base) {
			body, ok := extractDashCBody(argv[1:])
			if !ok {
				// `bash` with no -c: treat as pipeline-tail evaluator (handled in scan).
				return
			}
			// Re-parse body and walk it under the same context, marked from-eval.
			subCtx := ctx
			subCtx.fromEval = true
			parser := syntax.NewParser(syntax.KeepComments(false), syntax.Variant(syntax.LangBash))
			f, err := parser.Parse(strings.NewReader(body), "")
			if err != nil {
				// Mark as unresolvable: the body parsed badly. If a trigger
				// keyword is present, the orchestrator's quickReject will see
				// it; we still register a synthetic executed command so the
				// rm-rule can ask.
				w.executed = append(w.executed, ExecutedCommand{
					Name: "__inline_parse_error__", FromEval: true,
					Args: []string{body}, LexicalCwd: w.lexicalCwd,
				})
				return
			}
			sub := &walker{lexicalCwd: w.lexicalCwd}
			for _, s := range f.Stmts {
				sub.walkStmt(s, subCtx)
			}
			w.executed = append(w.executed, sub.executed...)
			return
		}

		if base == "eval" {
			// Concatenate args, re-parse.
			body := strings.Join(argv[1:], " ")
			subCtx := ctx
			subCtx.fromEval = true
			parser := syntax.NewParser(syntax.KeepComments(false), syntax.Variant(syntax.LangBash))
			f, err := parser.Parse(strings.NewReader(body), "")
			if err != nil {
				w.executed = append(w.executed, ExecutedCommand{
					Name: "__inline_parse_error__", FromEval: true,
					Args: []string{body}, LexicalCwd: w.lexicalCwd,
				})
				return
			}
			sub := &walker{lexicalCwd: w.lexicalCwd}
			for _, s := range f.Stmts {
				sub.walkStmt(s, subCtx)
			}
			w.executed = append(w.executed, sub.executed...)
			return
		}

		// Generic executor wrappers — strip prefix, loop.
		stripped, isWrapper, newCtx := stripExecutorPrefix(argv, ctx)
		if isWrapper {
			argv = stripped
			ctx = newCtx
			continue
		}

		// xargs/find — synthesize virtual commands per the unwrap rules.
		if base == "xargs" {
			w.handleXargs(argv, ctx)
			return
		}
		if base == "find" {
			w.handleFind(argv, ctx)
			return
		}

		// Reached the actual command — record it.
		w.executed = append(w.executed, ExecutedCommand{
			Name:       base,
			Path:       argv[0],
			Args:       append([]string(nil), argv[1:]...),
			StdinArgs:  ctx.stdinArgs,
			Chrooted:   ctx.chrooted,
			Remote:     ctx.remote,
			FromEval:   ctx.fromEval,
			LexicalCwd: w.lexicalCwd,
		})
		return
	}
}

// reparseAndWalk re-parses a shell-string body (from bash -c, eval, ssh)
// and walks its statements under the supplied context. On parse error
// it appends an "__inline_parse_error__" sentinel so the rule layer
// (which sees the trigger keyword in the original command) emits an ask.
func (w *walker) reparseAndWalk(body string, ctx walkContext, remote bool) {
	parser := syntax.NewParser(syntax.KeepComments(false), syntax.Variant(syntax.LangBash))
	f, err := parser.Parse(strings.NewReader(body), "")
	if err != nil {
		w.executed = append(w.executed, ExecutedCommand{
			Name:       "__inline_parse_error__",
			FromEval:   true,
			Remote:     remote,
			Args:       []string{body},
			LexicalCwd: w.lexicalCwd,
		})
		return
	}
	sub := &walker{lexicalCwd: w.lexicalCwd}
	for _, s := range f.Stmts {
		sub.walkStmt(s, ctx)
	}
	w.executed = append(w.executed, sub.executed...)
}

// scanForNestedExecutions descends into command substitutions and process
// substitutions inside argv to record their own executions.
func (w *walker) scanForNestedExecutions(call *syntax.CallExpr, ctx walkContext) {
	for _, word := range call.Args {
		for _, part := range word.Parts {
			switch p := part.(type) {
			case *syntax.CmdSubst:
				for _, s := range p.Stmts {
					w.walkStmt(s, ctx)
				}
			case *syntax.ProcSubst:
				for _, s := range p.Stmts {
					w.walkStmt(s, ctx)
				}
			case *syntax.DblQuoted:
				// Could contain nested command substitutions.
				for _, inner := range p.Parts {
					if cs, ok := inner.(*syntax.CmdSubst); ok {
						for _, s := range cs.Stmts {
							w.walkStmt(s, ctx)
						}
					}
				}
			}
		}
	}
}

// flattenWords resolves a slice of mvdan/sh Words to literal strings when
// possible. Returns ok=false when any word contains shell metacharacters
// that prevent static resolution (variables, command subst, etc.).
func flattenWords(words []*syntax.Word) ([]string, bool) {
	out := make([]string, 0, len(words))
	allOk := true
	for _, w := range words {
		s, ok := flattenWord(w)
		if !ok {
			allOk = false
		}
		out = append(out, s)
	}
	return out, allOk
}

// flattenWord returns the literal value of a Word and a bool for whether
// it is fully resolvable. If not fully resolvable, the returned string still
// contains the original textual form (with $VAR placeholders) so that the
// classification step can flag it as Unresolvable.
func flattenWord(w *syntax.Word) (string, bool) {
	var sb strings.Builder
	resolvable := true
	for _, part := range w.Parts {
		switch p := part.(type) {
		case *syntax.Lit:
			sb.WriteString(p.Value)
		case *syntax.SglQuoted:
			sb.WriteString(p.Value)
		case *syntax.DblQuoted:
			for _, inner := range p.Parts {
				switch q := inner.(type) {
				case *syntax.Lit:
					sb.WriteString(q.Value)
				case *syntax.ParamExp, *syntax.CmdSubst:
					sb.WriteString(textOf(q))
					resolvable = false
				default:
					sb.WriteString(textOf(q))
					resolvable = false
				}
			}
		case *syntax.ParamExp:
			sb.WriteString(textOf(p))
			resolvable = false
		case *syntax.CmdSubst:
			sb.WriteString(textOf(p))
			resolvable = false
		case *syntax.ArithmExp:
			sb.WriteString(textOf(p))
			resolvable = false
		case *syntax.ExtGlob:
			sb.WriteString(textOf(p))
		default:
			sb.WriteString(textOf(p))
		}
	}
	return sb.String(), resolvable
}

// textOf falls back to mvdan/sh's printer for nodes we can't easily flatten.
func textOf(n syntax.Node) string {
	var sb strings.Builder
	printer := syntax.NewPrinter()
	if err := printer.Print(&sb, n); err != nil {
		return fmt.Sprintf("<%T>", n)
	}
	return sb.String()
}

func basenameLower(p string) string {
	if i := strings.LastIndexByte(p, '/'); i >= 0 {
		p = p[i+1:]
	}
	return strings.ToLower(p)
}

func containsShellMeta(s string) bool {
	return strings.ContainsAny(s, "$`*?[")
}
