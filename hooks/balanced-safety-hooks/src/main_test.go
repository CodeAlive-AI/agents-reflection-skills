package main

import (
	"encoding/json"
	"os"
	"path/filepath"
	"runtime"
	"strings"
	"testing"
)

// FixtureInput is the part of HookInput that fixtures specify.
type FixtureInput struct {
	ToolName  string    `json:"tool_name"`
	ToolInput ToolInput `json:"tool_input"`
	Cwd       string    `json:"cwd"`
}

// FixtureExpect is what a fixture asserts about the hook's decision.
// reason_substring is optional; if present, the actual reason must contain it.
type FixtureExpect struct {
	Decision        string `json:"decision"`
	Rule            string `json:"rule"`
	ReasonCode      string `json:"reason_code"`
	ReasonSubstring string `json:"reason_substring,omitempty"`
}

// Fixture is one test case stored as testdata/fixtures/<name>.json.
type Fixture struct {
	Name        string        `json:"name"`
	Description string        `json:"description,omitempty"`
	Skip        string        `json:"skip,omitempty"` // non-empty = skip with this reason
	Env         map[string]string `json:"env,omitempty"`
	Input       FixtureInput  `json:"input"`
	Expect      FixtureExpect `json:"expect"`
}

func TestGoldenFixtures(t *testing.T) {
	files, err := filepath.Glob("testdata/fixtures/*.json")
	if err != nil {
		t.Fatalf("glob fixtures: %v", err)
	}
	if len(files) == 0 {
		t.Fatal("no fixtures found")
	}
	for _, f := range files {
		f := f
		name := strings.TrimSuffix(filepath.Base(f), ".json")
		t.Run(name, func(t *testing.T) {
			data, err := os.ReadFile(f)
			if err != nil {
				t.Fatalf("read: %v", err)
			}
			var fx Fixture
			if err := json.Unmarshal(data, &fx); err != nil {
				t.Fatalf("unmarshal: %v", err)
			}
			if fx.Skip != "" {
				t.Skip(fx.Skip)
			}
			if fx.Input.ToolName == "" {
				fx.Input.ToolName = "Bash"
			}
			// Apply per-fixture env, restore after test.
			for k, v := range fx.Env {
				old, present := os.LookupEnv(k)
				t.Cleanup(func() {
					if present {
						os.Setenv(k, old)
					} else {
						os.Unsetenv(k)
					}
				})
				if v == "<unset>" {
					os.Unsetenv(k)
				} else {
					os.Setenv(k, v)
				}
			}

			d := decisionFor(fx.Input)
			gotDecision := d.Level.String()
			if gotDecision != fx.Expect.Decision {
				t.Errorf("decision: got %q, want %q\n  rule=%q reason_code=%q reason=%q",
					gotDecision, fx.Expect.Decision, d.Rule, d.ReasonCode, d.Reason)
			}
			if fx.Expect.Rule != "" && d.Rule != fx.Expect.Rule {
				t.Errorf("rule: got %q, want %q", d.Rule, fx.Expect.Rule)
			}
			if fx.Expect.ReasonCode != "" && d.ReasonCode != fx.Expect.ReasonCode {
				t.Errorf("reason_code: got %q, want %q", d.ReasonCode, fx.Expect.ReasonCode)
			}
			if fx.Expect.ReasonSubstring != "" && !strings.Contains(d.Reason, fx.Expect.ReasonSubstring) {
				t.Errorf("reason_substring: %q not found in %q", fx.Expect.ReasonSubstring, d.Reason)
			}
		})
	}
}

// decisionFor runs the hook pipeline for a fixture's input and returns the
// raw Decision (before mode-shadow override).
func decisionFor(in FixtureInput) Decision {
	if in.ToolName != "Bash" {
		return Decision{Level: LevelAllow, Rule: "default", ReasonCode: "no_rule_matched"}
	}
	cmd := in.ToolInput.Command
	if cmd == "" {
		return Decision{Level: LevelAllow, Rule: "default", ReasonCode: "no_rule_matched"}
	}
	reg := newRegistry(RmRule{}, SupabaseRule{}, InfraRule{}, PaasRule{}, DbClientRule{})
	triggers := reg.triggerSet()
	sp := NewSafePaths(in.Cwd, nil)
	return evaluate(cmd, triggers, reg, &RuleEnv{HookCwd: in.Cwd, SafePaths: sp})
}

// BenchmarkEvaluate measures hot-path latency for the orchestrator. Two
// representative inputs:
//   - "no trigger" path: a typical innocuous command. Quick-reject should
//     short-circuit before any AST parse, so this is the high-volume case.
//   - "trigger + ask" path: a command that hits a destructive rule, exercising
//     parser, unwrap, rule eval, and aggregation.
func BenchmarkEvaluate(b *testing.B) {
	reg := newRegistry(RmRule{}, SupabaseRule{}, InfraRule{}, PaasRule{}, DbClientRule{})
	triggers := reg.triggerSet()
	env := &RuleEnv{HookCwd: "/Users/test/myproject", SafePaths: NewSafePaths("/Users/test/myproject", nil)}

	b.Run("no_trigger", func(b *testing.B) {
		cmd := "echo hello && pwd && ls -la /tmp | head -5"
		b.ReportAllocs()
		b.ResetTimer()
		for i := 0; i < b.N; i++ {
			_ = evaluate(cmd, triggers, reg, env)
		}
	})

	b.Run("trigger_rm_catastrophic", func(b *testing.B) {
		cmd := "rm -rf /etc/nginx"
		b.ReportAllocs()
		b.ResetTimer()
		for i := 0; i < b.N; i++ {
			_ = evaluate(cmd, triggers, reg, env)
		}
	})

	b.Run("trigger_curl_railway_graphql", func(b *testing.B) {
		cmd := `curl -X POST https://backboard.railway.com/graphql/v2 -H "Authorization: Bearer x" -d '{"query":"mutation { volumeDelete(id: 1) }"}'`
		b.ReportAllocs()
		b.ResetTimer()
		for i := 0; i < b.N; i++ {
			_ = evaluate(cmd, triggers, reg, env)
		}
	})

	b.Run("trigger_aws_delete", func(b *testing.B) {
		cmd := "aws ec2 delete-volume --volume-id vol-12345"
		b.ReportAllocs()
		b.ResetTimer()
		for i := 0; i < b.N; i++ {
			_ = evaluate(cmd, triggers, reg, env)
		}
	})
}

// TestPlatformSkipMacOSOnly skips fixtures marked darwin-only when not on darwin.
// This is just a marker for any future platform-specific paths.
func TestPlatformSentinel(t *testing.T) {
	if runtime.GOOS != "darwin" && runtime.GOOS != "linux" {
		t.Skip("only darwin/linux supported")
	}
}
