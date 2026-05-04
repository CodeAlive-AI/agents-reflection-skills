package main

import (
	"fmt"
	"strings"
)

// SupabaseRule covers Supabase CLI operations that mutate the linked
// (remote/production) database, plus generic ORM migration commands
// (Alembic, Django, Prisma, Drizzle, Knex, Sequelize, Flyway, Liquibase,
// Rails/Rake, TypeORM, Goose). Ports `~/.claude/hooks/supabase-safety.sh`.
type SupabaseRule struct{}

func (SupabaseRule) Name() string { return "supabase" }

func (SupabaseRule) Triggers() []string {
	return []string{
		"supabase",
		"alembic",
		"manage.py", "django-admin",
		// `python manage.py migrate` — python invokes the script; the AST
		// command name is "python", so we trigger on the interpreter and
		// branch in Check based on args[0].
		"python", "python3",
		"prisma",
		"drizzle-kit",
		"knex",
		"sequelize",
		"flyway",
		"liquibase",
		"rails", "rake",
		"typeorm",
		"goose",
	}
}

func (r SupabaseRule) Check(cmd ExecutedCommand, _ *RuleEnv) *Decision {
	args := cmd.Args
	switch cmd.Name {
	case "supabase":
		return checkSupabase(cmd, args)
	case "alembic":
		if hasArg(args, "upgrade", "downgrade", "stamp") {
			return mkAsk(r.Name(), "supabase.alembic_migration",
				"Alembic migration (upgrade/downgrade/stamp)", argv(cmd))
		}
	case "manage.py", "django-admin":
		if hasArg(args, "migrate") {
			return mkAsk(r.Name(), "supabase.django_migrate",
				"Django migrate — applies database migrations", argv(cmd))
		}
	case "python", "python3":
		// `python manage.py migrate` / `python -m django ... migrate`.
		// If the first non-flag arg is manage.py or django-admin, treat as
		// the equivalent `manage.py ...` invocation.
		if len(args) >= 2 {
			first := basenameOnly(args[0])
			if first == "manage.py" || first == "django-admin" {
				if hasArg(args[1:], "migrate") {
					return mkAsk(r.Name(), "supabase.django_migrate",
						"Django migrate — applies database migrations", argv(cmd))
				}
			}
		}
	case "prisma":
		// migrate deploy | migrate reset | db push
		if seq(args, "migrate", "deploy") || seq(args, "migrate", "reset") || seq(args, "db", "push") {
			return mkAsk(r.Name(), "supabase.prisma_migration",
				"Prisma migration (deploy/reset/push)", argv(cmd))
		}
	case "drizzle-kit":
		if hasArg(args, "push", "migrate") {
			return mkAsk(r.Name(), "supabase.drizzle_migration",
				"Drizzle migration (push/migrate)", argv(cmd))
		}
	case "knex":
		if hasArgPrefix(args, "migrate:") {
			return mkAsk(r.Name(), "supabase.knex_migration",
				"Knex migration", argv(cmd))
		}
	case "sequelize":
		if hasArg(args, "db:migrate") {
			return mkAsk(r.Name(), "supabase.sequelize_migration",
				"Sequelize migration", argv(cmd))
		}
	case "flyway":
		if hasArg(args, "migrate", "repair", "undo", "clean") {
			return mkAsk(r.Name(), "supabase.flyway_migration",
				"Flyway migration", argv(cmd))
		}
	case "liquibase":
		if hasArg(args, "update", "rollback", "drop-all") {
			return mkAsk(r.Name(), "supabase.liquibase_migration",
				"Liquibase migration", argv(cmd))
		}
	case "rails", "rake":
		if hasArg(args, "db:migrate") {
			return mkAsk(r.Name(), "supabase.rails_migration",
				"Rails database migration", argv(cmd))
		}
	case "typeorm":
		if hasArg(args, "migration:run") {
			return mkAsk(r.Name(), "supabase.typeorm_migration",
				"TypeORM migration:run", argv(cmd))
		}
	case "goose":
		if hasArg(args, "up", "down", "redo", "reset") {
			return mkAsk(r.Name(), "supabase.goose_migration",
				"Goose migration", argv(cmd))
		}
	}
	return nil
}

func checkSupabase(cmd ExecutedCommand, args []string) *Decision {
	rule := "supabase"
	// supabase db push
	if seq(args, "db", "push") {
		return mkAsk(rule, "supabase.db_push",
			"supabase db push — pushes migrations to the REMOTE (production) database", argv(cmd))
	}
	// supabase ... db reset ... --linked  OR  supabase ... --linked ... db reset
	if seq(args, "db", "reset") && hasArg(args, "--linked") {
		return mkAsk(rule, "supabase.db_reset_linked",
			"supabase db reset --linked — will WIPE the remote (production) database", argv(cmd))
	}
	// supabase migration repair / migrations repair
	for i := 0; i+1 < len(args); i++ {
		if (args[i] == "migration" || args[i] == "migrations") && args[i+1] == "repair" {
			return mkAsk(rule, "supabase.migration_repair",
				"supabase migration repair — modifies migration history on the REMOTE database", argv(cmd))
		}
	}
	// supabase ... --db-url <url>
	if hasArgPrefix(args, "--db-url") {
		return mkAsk(rule, "supabase.db_url",
			"supabase --db-url detected — targets an external database", argv(cmd))
	}
	return nil
}

// --- helpers shared by the simple keyword-style rules ---

// hasArg returns true if any of the candidates appears anywhere in args.
func hasArg(args []string, candidates ...string) bool {
	for _, a := range args {
		for _, c := range candidates {
			if a == c {
				return true
			}
		}
	}
	return false
}

// hasArgPrefix returns true if any arg starts with one of the prefixes.
func hasArgPrefix(args []string, prefixes ...string) bool {
	for _, a := range args {
		for _, p := range prefixes {
			if strings.HasPrefix(a, p) {
				return true
			}
		}
	}
	return false
}

// seq returns true when args contains the given subsequence in order
// (not necessarily contiguous). Used for "supabase db push" matching.
func seq(args []string, want ...string) bool {
	if len(want) == 0 {
		return true
	}
	i := 0
	for _, a := range args {
		if a == want[i] {
			i++
			if i == len(want) {
				return true
			}
		}
	}
	return false
}

func argv(cmd ExecutedCommand) string {
	return strings.Join(append([]string{cmd.Name}, cmd.Args...), " ")
}

// basenameOnly returns the trailing component of a path-like token,
// without lowercasing. Used to match script names like "manage.py".
func basenameOnly(p string) string {
	if i := strings.LastIndexByte(p, '/'); i >= 0 {
		p = p[i+1:]
	}
	return p
}

func mkAsk(rule, code, reason, ctx string) *Decision {
	return &Decision{
		Level:      LevelAsk,
		Rule:       rule,
		Reason:     reason,
		ReasonCode: code,
		Context:    fmt.Sprintf("argv=%q", ctx),
	}
}
