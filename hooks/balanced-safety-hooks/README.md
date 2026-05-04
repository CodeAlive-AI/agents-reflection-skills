# bash-guard — Balanced Bash safety for autonomous coding agents

[![bash-guard — Balanced Bash safety for autonomous coding agents](assets/banner.png)](https://github.com/CodeAlive-AI/ai-driven-development)

[![GitHub stars](https://img.shields.io/github/stars/CodeAlive-AI/ai-driven-development?style=social)](https://github.com/CodeAlive-AI/ai-driven-development/stargazers)

A small Go program that sits between Claude Code and your shell, parses every Bash command the agent is about to run with a real shell AST, and decides whether to **allow** it or **ask** you. The default rule set uses `ask` rather than `deny` — see [why](#why-we-default-to-ask).

## Install

### Quick install (no Go required)

Downloads the prebuilt binary for your OS/arch (darwin / linux × arm64 / amd64) from the latest GitHub release, verifies the SHA-256 checksum, and patches `~/.claude/settings.json`. Requires `curl` and `jq`.

```bash
curl -fsSL https://raw.githubusercontent.com/CodeAlive-AI/ai-driven-development/main/hooks/balanced-safety-hooks/install-prebuilt.sh | sh
```

To install in `--shadow` mode (or `--dry-run`, `--uninstall`), forward args through the pipe:

```bash
curl -fsSL https://raw.githubusercontent.com/CodeAlive-AI/ai-driven-development/main/hooks/balanced-safety-hooks/install-prebuilt.sh | sh -s -- --shadow
```

To pin a specific release, set `BASH_GUARD_VERSION=bash-guard-vX.Y.Z` in the environment before running.

### Build from source

Requires Go ≥ 1.21 and `jq`.

```bash
git clone https://github.com/CodeAlive-AI/ai-driven-development.git
cd ai-driven-development/hooks/balanced-safety-hooks

./install.sh --live       # real enforcement — emits ask for risky commands (the normal mode)
./install.sh --shadow     # observe-only: logs every decision, never prompts. For tuning safe paths before going live.
./install.sh --dry-run    # same effect as --shadow, with a distinct log label
./install.sh --uninstall  # remove hook entry + symlink
```

What `install.sh` does, idempotently:

1. Verifies Go is on `PATH`.
2. Symlinks `~/.claude/hooks/bash-guard` → this directory's `src/`.
3. Builds `bash_guard.bin` (warms the Go cache).
4. Patches `~/.claude/settings.json` with a `PreToolUse[matcher=Bash]` entry pointing at the binary. Existing hooks are preserved; previous `bash-guard` entries are replaced. A timestamped backup is written next to the file.

Switching modes later is the same command — `settings.json` is re-read on every hook fire, so no Claude Code restart is needed.

## Why this exists

Anyone who has spent a few days with coding agents has watched one go off the rails — deleting the wrong folder, nuking docker images, or dropping a production database along with the surrounding infra (see [what a Cursor agent on Claude Opus 4.6 did to PocketOS](https://neuraltrust.ai/blog/pocketos-railway-agent) — one POST to Railway's `volumeDelete` mutation, the whole prod gone). Hooks are the most important guardrail you can put in front of a coding agent: they bring both determinism and safety to an otherwise non-deterministic loop.

The trick is balance:

- **Too few hooks** and the agent eventually wipes something that mattered.
- **Too many hooks** and you train yourself to mash Enter on every Allow prompt without reading. Banner blindness sets in within a day, and the hook layer becomes worse than nothing — it's permission-laundering with extra steps.

The right move is to gate **only** the truly destructive, irreversible, or critical actions. Everything else should pass silently. bash-guard is the opinionated set of hooks I use myself for that gate. It's based on [claude-code-safety-net](https://github.com/kenryu42/claude-code-safety-net) (h/t [@kenryu42](https://github.com/kenryu42)), substantially reworked and extended — AST-based parsing instead of regex, span classification, safe-paths matrix, PocketOS-class API coverage, and an `ask`-by-default decision model.

It's written in Go, so it runs in single-digit milliseconds per command and is easy to fork: edit a rule, `make build`, done.

## False positives it fixes

It replaces shlex/regex-based hooks that produced two classes of false positives in production:

- **FP-1 — heredoc with English prose:** `cat > /tmp/x <<'EOF'\nWe use find and rm a lot. Don't break.\nEOF` was blocked because the legacy hook ran shlex over the entire command string, choked on the apostrophe in "Don't", and bailed fail-closed on the word "find" appearing in plain prose.
- **FP-2 — `rm -rf` inside a known-safe directory:** `cd /tmp && rm -rf ci-results && mkdir ci-results` was blocked because the legacy "rm-outside-cwd" rule had no notion of safe-by-construction paths like `/tmp`.

Both are now `allow` by design, with fixtures pinning the behaviour (`testdata/fixtures/find_word_in_heredoc_body.json`, `testdata/fixtures/rm_rf_tmp_subdir.json`).

## What makes it different

**1. Real AST, not regex.** Commands are parsed with [`mvdan.cc/sh/v3`](https://github.com/mvdan/sh) — a production-grade Bash parser used by `shfmt`. Regex and shlex hooks systematically misclassify:

- words inside heredoc bodies
- words inside single-quoted strings
- shell substitutions: `$(...)`, backticks
- pipelines that pipe a string into a shell evaluator (`echo "rm -rf /" | bash`)
- executor wrappers that hide the real command (`sudo rm`, `env FOO=bar rm`, `xargs rm`, `find -delete`, `bash -c "rm ..."`, `eval "rm ..."`, `ssh host "rm ..."`)

bash-guard descends into all of those, classifies every span (`Executed` / `Data` / `HeredocBody` / `InlineCode`), and only inspects spans that actually run.

**2. Span classification beats keyword matching.** A keyword like `rm` inside `<<'EOF'...EOF` is data, not an executed command — bash-guard knows. A keyword inside `echo "..." | bash` is executed code on the right side of the pipe, even though it lexically appears as a string literal — bash-guard knows that too.

**3. Asymmetric fail-open.** Pre-trigger parse failures → `allow` (false negative is a one-off, the user catches it). Post-trigger parse failures (we saw a destructive keyword but couldn't parse) → `ask` (do not silently allow when something dangerous *might* be happening). Documented in §3.6 of [`DESIGN.md`](DESIGN.md).

**4. Safe-paths matrix with carve-outs.** Catastrophic-prefix paths (`/etc/...`, `/usr/...`) and home-protected paths (`$HOME/...`) match unconditionally **except** when the operand is on the explicit safe-paths list. `/tmp/foo` is safe; `/etc/nginx` is not. `$HOME/code/myproject/node_modules` is safe iff `myproject` is in the safe-paths list; `$HOME/.ssh` is never safe.

**5. Trusted-projects allowlist.** Per-repo `.claude/bash-guard.toml` is **not** auto-loaded — that would let any hostile repo whitelist `/etc`. A repo's config is only honoured if its root is listed in the global `~/.claude/hooks/bash-guard/trusted-projects.toml`.

**6. Performance budget.** ~0.16 ms quick-reject for commands without any trigger keyword; <5 ms for full parse + rule evaluation; 0–10 ms end-to-end warm. Rebuilds are explicit (`make build`); no per-invocation `go build` wrapper.

## What it asks about

| Rule | Triggers when |
|---|---|
| **rm** | `rm`, `unlink`, `rmdir`, `shred` targeting paths outside the cwd subtree, catastrophic prefixes (`/etc`, `/usr`, …), `$HOME` (with carve-outs for explicit safe paths), or with `--no-preserve-root` |
| **rm via wrappers** | `sudo rm`, `env FOO=bar rm`, `xargs rm`, `find -delete`, `find -exec rm`, `bash -c "rm ..."`, `eval "rm ..."`, `ssh host "rm ..."`, `chroot newroot rm`, `timeout 5 rm`, `nohup rm`, `time rm`, … |
| **rm via pipe-to-shell** | `echo "rm -rf /" \| bash`, `cat script.sh \| sh`, etc. |
| **supabase** | `supabase db push`, `db reset --linked`, `migration repair`, `--db-url <prod>`; ORM migration verbs (`alembic upgrade`, `manage.py migrate`, `prisma migrate deploy`, `drizzle-kit push`, `knex migrate`, `sequelize db:migrate`, `flyway migrate`, `liquibase update`, `rails db:migrate`, `rake db:migrate`, `typeorm migration:run`, `goose up`) |
| **infra** | `kubectl delete/apply/patch`, destructive `gcloud compute/storage/...`, `helm install/upgrade/uninstall`, `docker rm/system prune`, destructive Mongo (`drop`, `deleteMany`, `mongorestore`, `mongodump`), `terraform/tofu apply/destroy`, `gsutil rm`, `git push -f / --force` |
| **hyperscaler clouds** | `aws <svc> delete-* / terminate-* / destroy-* / purge-* / remove-* / deregister-* / revoke-*`, `aws s3 rm`, `az ... delete / purge`, `oci ... delete / terminate`, `ibmcloud ... delete / *-rm / *-delete` |
| **paas** | `railway`, `fly` / `flyctl`, `heroku`, `vercel`, `doctl`, `netlify`, `linode-cli` with destructive verbs (`delete`, `destroy`, `remove`, `rm`, `down`, `reset`) and Heroku/Netlify-style colon-suffix forms (`apps:destroy`, `pg:reset`, `sites:delete`, `addons:destroy`, `domains:remove`, `env:unset`) |
| **DB clients** | `psql` / `mysql` / `mariadb` with inline SQL containing `DROP DATABASE/TABLE/SCHEMA/...`, `TRUNCATE`, `DELETE FROM`, `ALTER ... DROP`; `redis-cli FLUSHALL / FLUSHDB / SHUTDOWN / MIGRATE` |
| **cloud control-plane curl** | Mutating `curl -X POST/PUT/PATCH/DELETE` to known cloud API hostnames (Railway, Fly, Heroku, Vercel, Netlify, DigitalOcean, Linode, `googleapis.com`, `amazonaws.com`, `management.azure.com`, `oraclecloud.com`, `cloud.ibm.com`); GraphQL bodies containing `mutation` |
| **search-engine curl** | Mutating `curl -X POST/PUT/PATCH/DELETE` against OpenSearch/Elasticsearch URLs (`:9200`, `:9300`, hostname matches) |

The rule set is open: a new rule is one Go file implementing the `Rule` interface (`Name() / Triggers() / Check()`), plus ≥3 golden-table fixtures. See [`src/CLAUDE.md`](src/CLAUDE.md) for the maintenance protocol.

### PocketOS-class coverage

In April 2026 a Cursor agent on Claude Opus 4.6 wiped the production database of [PocketOS](https://neuraltrust.ai/blog/pocketos-railway-agent) by issuing one POST request to Railway's GraphQL `volumeDelete` mutation. The shape of that incident — a vendor token found in a repo, used by an autonomous agent to invoke a destructive API endpoint with no server-side confirmation — generalises across every PaaS and hyperscaler. bash-guard cannot replace platform-level guardrails (scoped tokens, server-side gates, off-volume backups), but it covers the bash channels through which this class of attack flows:

| Channel | Coverage |
|---|---|
| Vendor CLI (`railway volume delete`, `fly volumes destroy`, `heroku pg:reset`, `aws ec2 delete-volume`, `az group delete`) | `paas` + `infra` rules |
| Direct API (`curl -X POST https://backboard.railway.com/graphql/v2 -d '{"query":"mutation{volumeDelete}"}'`) | `infra.cloud_api_mutation` + `infra.graphql_mutation` |
| DB-level (`psql -c "DROP DATABASE app"`, `redis-cli FLUSHALL`) | `db_client` rule |

What bash-guard still does **not** cover, and what your defence-in-depth needs alongside it:

- **MCP-tool calls.** If the agent invokes Railway / Fly / Heroku via an MCP server (Railway markets a hosted MCP endpoint), the destructive call goes through `PreToolUse:mcp__*`, not `PreToolUse:Bash`. Out of scope.
- **Direct SDK calls** (`import boto3; ec2.delete_volume(...)`) executed from a script the agent runs are visible only as `python script.py` to the hook — content of the Python file is not parsed.
- **Token scope.** bash-guard cannot tell whether the token in `$RAILWAY_TOKEN` is scoped to staging or production. That is a vendor-side IAM problem.

What it explicitly does **not** trigger on:

- read-only verbs (`kubectl get`, `gcloud describe`, `helm list`, `docker ps`, `git push` without `-f`)
- `--dry-run` variants of destructive verbs (current behaviour: still asks; see open question in `DESIGN.md`)
- commands inside heredoc bodies, single-quoted strings, or comments

## Why we default to ask

Claude Code's hook protocol supports three decisions: `allow`, `ask`, `deny`. The default rule set ships with `allow` and `ask` — `deny` is intentionally not used out of the box.

**Reasoning.** A `deny` decision is a hard wall the agent immediately tries to climb over. Modern agents are good enough to find a path around any primitive hook — and that capability is amplified when a prompt-injection has primed them with adversarial intent. Hooks are usually shallow string-matchers; agents are not. In practice:

- The agent rephrases the command (`rm -rf` → `find … -delete`).
- It splits the command (`rm dir/* && rmdir dir`).
- It retries through a different wrapper (`sudo rm`, `bash -c 'rm …'`).
- It silently switches to a write-via-Edit equivalent.

`deny` is hostile to the agent's planner without informing the human. `ask` keeps the human in the loop — which is the only durable defence — and gives the agent a clear signal that the destructive intent was recognised. Empirically (and per the consilium review of the design), `ask` reduces both false-negative escapes ("agent worked around the block") and operator fatigue ("why does this keep silently failing?").

If your environment requires hard blocks for specific commands (e.g. compliance constraints, shared infra), nothing in the design prevents you from forking and extending the `Level` enum with a `LevelDeny` tier and emitting it from your own rules. Just be aware of the workaround behaviour above and pair `deny` with platform-side guardrails (scoped tokens, server-side gates) so it isn't your only line of defence.

## Tuning

Going straight to `--live` is fine — the worst case is a few extra ask prompts, which you click Allow on. Most users should just install live and tune as friction shows up.

If you'd rather observe before any prompts hit your workflow, `--shadow` logs every would-be decision without prompting. Tail `~/.claude/logs/bash-guard.jsonl` (`tail -f … | jq '.'`); each entry has `would_decide`, `rule`, `reason_code`, `command_hash` (set `BASH_GUARD_LOG_COMMANDS=1` to log raw commands; off by default).

When you see asks on legitimate work, add the project root to `~/.claude/hooks/bash-guard/trusted-projects.toml` and put project-specific safe paths in `<repo>/.claude/bash-guard.toml`. Switching modes is just rerunning `install.sh` — `settings.json` is re-read on every hook fire.

## Architecture

| File | What lives here |
|---|---|
| `src/main.go` | Pipeline: stdin JSON → quickReject → parse → rule eval → emit JSON. Mode resolution, audit. |
| `src/parser.go` | mvdan/sh AST walk, span classification, lexical-cwd tracking from `cd` statements. |
| `src/unwrap.go` | Executor wrappers: sudo, env, command, builtin, exec, time, nice, nohup, timeout, chroot, ssh, bash/sh -c, eval, xargs, find. |
| `src/safe_paths.go` | realpath + lstat-based path classification with POSIX rm trailing-slash semantics, catastrophic-prefix matrix, $HOME carve-outs. |
| `src/rule_rm.go` | `rm`, `unlink`, `rmdir`, `shred`. |
| `src/rule_supabase.go` | Supabase CLI + ORM migrations. |
| `src/rule_infra.go` | kubectl, gcloud, helm, docker, mongo*, terraform/tofu, gsutil, git push -f; aws/az/oci/ibmcloud destructive verbs; curl against OpenSearch/Elasticsearch + cloud control-plane APIs + GraphQL mutations. |
| `src/rule_paas.go` | PaaS CLIs: railway, fly/flyctl, heroku, vercel, doctl, netlify, linode-cli. |
| `src/rule_db.go` | DB clients: psql, mysql, mariadb, redis-cli — destructive SQL + redis verbs. |
| `src/decision.go` | `Level` enum (Allow / Ask only — no Deny), aggregation: ask wins. |
| `src/audit.go` | JSONL log at `~/.claude/logs/bash-guard.jsonl` with size-based rotation, 0o600 perms. |
| `src/config.go` | TOML loader, trusted-projects allowlist. |
| `testdata/fixtures/*.json` | Golden-table fixtures: `(decision, rule, reason_code)` tuples. ~120 cases. |
| `DESIGN.md` | Full architecture, consilium review, asymmetric fail-open rationale, open questions. |

For non-trivial changes, read `DESIGN.md` first. For day-to-day maintenance, [`src/CLAUDE.md`](src/CLAUDE.md) has the edit/rebuild loop, fixture protocol, and "what NOT to do" list.

## Inspecting behaviour

```bash
# tail the audit log
tail -f ~/.claude/logs/bash-guard.jsonl | jq '.'

# selftest: 4 fixed cases including FP-1 and FP-2 regressions
~/.claude/hooks/bash-guard/bash_guard.bin --selftest

# single-shot dry-fire
echo '{"tool_name":"Bash","tool_input":{"command":"rm -rf /tmp/x"},"cwd":"/tmp"}' \
  | ~/.claude/hooks/bash-guard/bash_guard.bin
```

## Star the repo

If `bash-guard` ever saves your `node_modules`, your migration history, or your prod database from an autonomous agent — a star on [the parent repo](https://github.com/CodeAlive-AI/ai-driven-development) helps others find it before they need it.

## License

MIT — same as the parent repo.
