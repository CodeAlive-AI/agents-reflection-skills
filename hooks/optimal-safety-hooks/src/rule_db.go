package main

import (
	"regexp"
	"strings"
)

// DbClientRule covers DB CLI clients invoking destructive SQL or commands
// directly: psql, mysql/mariadb, redis-cli. (mongosh / mongo / mongodump /
// mongorestore are handled in InfraRule.)
//
// Detection model:
//   - For SQL clients we extract the inline SQL body passed via -c, -e,
//     --command, --execute (and short-flag concatenations like -cSQL/-eSQL).
//     Substring scan for DROP / TRUNCATE / DELETE FROM / ALTER … DROP
//     keywords with word boundaries.
//   - For redis-cli we treat the verb tokens FLUSHALL / FLUSHDB / SHUTDOWN /
//     MIGRATE as destructive when present anywhere in argv.
//
// Known limitation: SQL passed via stdin (`psql < file.sql`) or from a file
// (`psql -f file.sql`) is not inspected — that requires reading the file,
// which we deliberately don't do (TOCTOU + scope creep). This is documented;
// the proper guard for that case is least-privilege DB credentials.
type DbClientRule struct{}

func (DbClientRule) Name() string { return "db_client" }

func (DbClientRule) Triggers() []string {
	return []string{
		"psql",
		"mysql", "mariadb",
		"redis-cli",
	}
}

// Match destructive SQL keywords with word boundaries (case-insensitive).
// Intentionally broad: we'd rather ask about a `DELETE FROM ... WHERE id=1`
// than miss `DELETE FROM users` — the false-positive cost is one click.
var sqlDestructiveRe = regexp.MustCompile(
	`(?i)\b(drop\s+(database|table|schema|index|view|user|role|tablespace|column)|truncate\s+table\b|truncate\s+\w+\b|delete\s+from\b|alter\s+\w+\s+\w+\s+drop\b)`)

// Destructive Redis verbs. Kept narrow on purpose; CONFIG SET, DEBUG, SCRIPT
// are dual-use enough that asking on every invocation would be noisy.
var redisDestructiveCommands = []string{
	"FLUSHALL", "FLUSHDB", "SHUTDOWN", "MIGRATE",
}

func (r DbClientRule) Check(cmd ExecutedCommand, _ *RuleEnv) *Decision {
	switch cmd.Name {
	case "psql", "mysql", "mariadb":
		body := extractSQLBody(cmd.Args)
		if body == "" {
			return nil
		}
		if sqlDestructiveRe.MatchString(body) {
			return mkAsk(r.Name(), "db_client.sql_destructive",
				"Destructive SQL via "+cmd.Name+": "+strings.TrimSpace(body), argv(cmd))
		}
	case "redis-cli":
		for _, a := range cmd.Args {
			up := strings.ToUpper(a)
			if contains(redisDestructiveCommands, up) {
				return mkAsk(r.Name(), "db_client.redis_destructive",
					"Destructive Redis command: "+up, argv(cmd))
			}
		}
	}
	return nil
}

// extractSQLBody pulls the inline SQL given via -c/-e/--command/--execute.
// Handles:
//   - `-c SQL` / `-e SQL` (separate args)
//   - `-cSQL` / `-eSQL` (concatenated short flag)
//   - `--command=SQL` / `--execute=SQL`
//   - `--command SQL` / `--execute SQL`
//
// Returns empty string when no inline SQL is found.
func extractSQLBody(args []string) string {
	for i, a := range args {
		switch {
		case a == "-c" || a == "-e" || a == "--command" || a == "--execute":
			if i+1 < len(args) {
				return args[i+1]
			}
		case strings.HasPrefix(a, "-c") && len(a) > 2 && !strings.HasPrefix(a, "--"):
			return a[2:]
		case strings.HasPrefix(a, "-e") && len(a) > 2 && !strings.HasPrefix(a, "--"):
			return a[2:]
		case strings.HasPrefix(a, "--command="):
			return strings.TrimPrefix(a, "--command=")
		case strings.HasPrefix(a, "--execute="):
			return strings.TrimPrefix(a, "--execute=")
		}
	}
	return ""
}
