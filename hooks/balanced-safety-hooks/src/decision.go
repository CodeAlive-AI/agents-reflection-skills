package main

import (
	"fmt"
	"strings"
)

// Level is the permission decision emitted to Claude Code.
// Only Allow or Ask — never Deny. Memory feedback_no_deny_in_hooks.md:
// agents trivially bypass deny (rephrase, split, retry); ask keeps the user
// in the loop, which is the actual defense.
type Level int

const (
	LevelAllow Level = iota
	LevelAsk
)

func (l Level) String() string {
	switch l {
	case LevelAsk:
		return "ask"
	default:
		return "allow"
	}
}

// Decision is the verdict of one rule on one ExecutedCommand,
// or the aggregated verdict for the whole Bash invocation.
type Decision struct {
	Level      Level
	Rule       string
	Reason     string
	ReasonCode string // stable id for golden tests / log analysis
	Context    string // mapped to Claude Code's additionalContext
}

// Aggregate folds rule decisions into a single hook output.
// Any Ask wins; only when all rules abstain (no decision returned) or
// all return Allow do we end up at Allow. There is no Deny tier.
func Aggregate(ds []Decision) Decision {
	var asks []Decision
	for _, d := range ds {
		if d.Level == LevelAsk {
			asks = append(asks, d)
		}
	}
	switch len(asks) {
	case 0:
		return Decision{Level: LevelAllow, Rule: "default", ReasonCode: "no_rule_matched"}
	case 1:
		return asks[0]
	}
	reasons := make([]string, 0, len(asks))
	codes := make([]string, 0, len(asks))
	contexts := make([]string, 0, len(asks))
	for _, d := range asks {
		reasons = append(reasons, fmt.Sprintf("[%s] %s", d.Rule, d.Reason))
		codes = append(codes, d.ReasonCode)
		if d.Context != "" {
			contexts = append(contexts, d.Context)
		}
	}
	return Decision{
		Level:      LevelAsk,
		Rule:       "aggregate",
		Reason:     strings.Join(reasons, "; "),
		ReasonCode: strings.Join(codes, ","),
		Context:    strings.Join(contexts, " | "),
	}
}
