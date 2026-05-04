package main

import "strings"

// PaasRule covers destructive commands on PaaS / dev cloud CLIs:
// railway, fly/flyctl, heroku, vercel, doctl (DigitalOcean), netlify,
// linode-cli.
//
// Motivation: the PocketOS class of incident (April 2026) — an agent finds a
// broad-scope vendor token in the repo and issues a single destructive call
// (volume delete, app destroy, DB reset). bash-guard cannot replace
// platform-level guardrails (scoped tokens, server-side confirmation gates),
// but it can ask before any destroy/delete/reset/down call from a known
// PaaS CLI, putting a human in the loop on irreversible operations.
type PaasRule struct{}

func (PaasRule) Name() string { return "paas" }

func (PaasRule) Triggers() []string {
	return []string{
		"railway",
		"fly", "flyctl",
		"heroku",
		"vercel",
		"doctl",
		"netlify",
		"linode-cli",
	}
}

// Verbs that, anywhere in argv after the CLI name, escalate to ask. Kept
// generic on purpose — these CLIs differ in subcommand layouts (railway uses
// `volume delete`, fly uses `volumes destroy`, vercel uses `remove`) but they
// share the destruction vocabulary.
var paasGenericDestructive = []string{
	"delete", "destroy", "remove", "rm",
	"down", "reset",
}

// Heroku- and netlify-style colon-suffixed verbs: `apps:destroy`, `pg:reset`,
// `addons:destroy`, `sites:delete`, `domains:remove`, `env:unset`.
var paasColonDestructiveSuffixes = []string{
	":destroy", ":delete", ":remove", ":reset", ":unset", ":rename",
}

func (r PaasRule) Check(cmd ExecutedCommand, _ *RuleEnv) *Decision {
	for _, a := range cmd.Args {
		if a == "" || strings.HasPrefix(a, "-") {
			continue
		}
		if contains(paasGenericDestructive, a) {
			return mkAsk(r.Name(), "paas."+cmd.Name+"_destructive",
				"Destructive "+cmd.Name+" command: contains "+a, argv(cmd))
		}
		for _, suf := range paasColonDestructiveSuffixes {
			if strings.HasSuffix(a, suf) {
				return mkAsk(r.Name(), "paas."+cmd.Name+"_destructive",
					"Destructive "+cmd.Name+" command: "+a, argv(cmd))
			}
		}
	}
	return nil
}
