package main

// Rule is the contract every safety check implements.
//
// Triggers returns the keyword set used by the orchestrator's quick-reject
// step. If none of these appear (as a word) in the raw command, the rule
// is guaranteed not to fire and parsing is skipped entirely.
//
// Check evaluates one ExecutedCommand and returns either nil (rule doesn't
// apply / no concern) or a Decision. By design, Decision.Level is always
// LevelAllow or LevelAsk — never a "deny" tier (memory feedback_no_deny_in_hooks.md).
type Rule interface {
	Name() string
	Triggers() []string
	Check(cmd ExecutedCommand, env *RuleEnv) *Decision
}

// RuleEnv carries environment context into rules.
type RuleEnv struct {
	HookCwd   string
	SafePaths *SafePaths
}

// registry holds all enabled rules. Order doesn't matter for correctness
// (Aggregate folds decisions order-independently) but is preserved for
// reproducible reasons-strings.
type registry struct {
	rules []Rule
}

func newRegistry(rs ...Rule) *registry {
	return &registry{rules: rs}
}

// triggerSet returns the union of all rules' trigger keywords.
func (r *registry) triggerSet() []string {
	seen := map[string]struct{}{}
	out := []string{}
	for _, rule := range r.rules {
		for _, t := range rule.Triggers() {
			if _, ok := seen[t]; ok {
				continue
			}
			seen[t] = struct{}{}
			out = append(out, t)
		}
	}
	return out
}

// evaluate runs every applicable rule against every executed command.
// A rule is "applicable" when the command's Name appears in its trigger set.
func (r *registry) evaluate(cmds []ExecutedCommand, env *RuleEnv) []Decision {
	var out []Decision
	for _, ec := range cmds {
		for _, rule := range r.rules {
			if !ruleApplies(rule, ec.Name) {
				continue
			}
			if d := rule.Check(ec, env); d != nil {
				out = append(out, *d)
			}
		}
	}
	return out
}

func ruleApplies(rule Rule, name string) bool {
	for _, t := range rule.Triggers() {
		if t == name {
			return true
		}
	}
	return false
}
