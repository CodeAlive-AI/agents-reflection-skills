package main

import (
	"strings"
)

// InfraRule covers destructive infra-mutation commands across the toolchain:
// kubectl, gcloud, helm, docker, mongo*, terraform/tofu, gsutil, git push -f,
// curl-vs-OpenSearch. Ports `~/.claude/hooks/infra-safety.sh` and
// `~/.claude/hooks/docker-prune-permission.sh`.
//
// Rationale: these are infrequent, high-impact commands where a confirmation
// dialog is cheap and prevents tired-Tuesday accidents.
type InfraRule struct{}

func (InfraRule) Name() string { return "infra" }

func (InfraRule) Triggers() []string {
	return []string{
		"kubectl",
		"gcloud",
		"helm",
		"docker",
		"mongo", "mongosh", "mongodump", "mongorestore",
		"terraform", "tofu",
		"gsutil",
		"git",
		"curl",
		// Hyperscaler CLIs (PocketOS-class coverage)
		"aws", "az", "oci", "ibmcloud",
	}
}

// Cloud control-plane API hostnames. Mutating HTTP verbs (POST/PUT/PATCH/
// DELETE) targeting these escalate to ask. Matches as substring (case-
// insensitive) so subdomains like `compute.googleapis.com` or
// `ec2.us-east-1.amazonaws.com` are covered without enumerating each one.
var cloudControlPlaneHosts = []string{
	"backboard.railway.com",  // Railway GraphQL
	"api.fly.io",
	"api.heroku.com",
	"api.vercel.com",
	"api.netlify.com",
	"api.digitalocean.com",
	"api.linode.com",
	"googleapis.com",      // covers compute.googleapis.com, iam.googleapis.com, …
	"amazonaws.com",       // covers ec2.*.amazonaws.com, iam.amazonaws.com, …
	"management.azure.com",
	"oraclecloud.com",
	"cloud.ibm.com",
}

var (
	kubectlDestructive = []string{
		"delete", "apply", "patch", "replace", "scale", "rollout", "drain",
		"cordon", "uncordon", "taint", "label", "annotate", "edit", "create",
		"run", "expose", "set", "autoscale", "certificate", "auth",
	}
	gcloudDestructive = []string{
		"delete", "destroy", "remove", "reset", "stop", "resize",
		"update", "create", "deploy",
		"set-iam", "add-iam", "remove-iam",
		"set-iam-policy", "add-iam-policy-binding", "remove-iam-policy-binding",
	}
	helmDestructive = []string{
		"install", "upgrade", "uninstall", "delete", "rollback",
	}
	dockerDestructive = []string{
		"rm", "rmi", "stop", "kill", "prune", "push",
	}
	terraformDestructive = []string{
		"apply", "destroy", "import", "taint", "untaint", "force-unlock",
	}
	gsutilDestructive = []string{
		"rm", "mv", "cp", "rsync",
	}
	mongoDestructiveTokens = []string{
		"drop", "deleteMany", "deleteOne", "remove",
		"updateMany", "updateOne", "insertMany", "insertOne",
		"replaceOne", "bulkWrite", "findAndModify",
		"findOneAndDelete", "findOneAndReplace", "findOneAndUpdate",
		"createIndex", "dropIndex", "renameCollection",
		"$out", "$merge",
	}
)

func (r InfraRule) Check(cmd ExecutedCommand, _ *RuleEnv) *Decision {
	switch cmd.Name {
	case "kubectl":
		if firstNonFlag(cmd.Args) != "" && contains(kubectlDestructive, firstNonFlag(cmd.Args)) {
			return mkAsk(r.Name(), "infra.kubectl_destructive",
				"Destructive kubectl command: kubectl "+firstNonFlag(cmd.Args), argv(cmd))
		}
	case "gcloud":
		// gcloud has a deep verb tree (e.g., `gcloud compute instances delete`).
		// Match if any token in args is a destructive verb.
		for _, a := range cmd.Args {
			if contains(gcloudDestructive, a) {
				return mkAsk(r.Name(), "infra.gcloud_destructive",
					"Destructive gcloud command: contains "+a, argv(cmd))
			}
			// `gcloud storage rm/mv/cp/rsync ...`
			if a == "storage" {
				if hasArg(cmd.Args, gsutilDestructive...) {
					return mkAsk(r.Name(), "infra.gcs_storage_mutation",
						"GCS storage mutation via gcloud storage", argv(cmd))
				}
			}
		}
		// gcloud compute ssh ... --command=<destructive>
		if seq(cmd.Args, "compute", "ssh") {
			if hasRemoteCommandMutation(cmd.Args) {
				return mkAsk(r.Name(), "infra.gcloud_ssh_remote_mutation",
					"Remote-command mutation via gcloud compute ssh --command", argv(cmd))
			}
		}
	case "helm":
		if firstNonFlag(cmd.Args) != "" && contains(helmDestructive, firstNonFlag(cmd.Args)) {
			return mkAsk(r.Name(), "infra.helm_mutation",
				"Helm mutation: helm "+firstNonFlag(cmd.Args), argv(cmd))
		}
	case "docker":
		v := firstNonFlag(cmd.Args)
		if contains(dockerDestructive, v) {
			return mkAsk(r.Name(), "infra.docker_destructive",
				"Destructive docker command: docker "+v, argv(cmd))
		}
		// docker system prune
		if v == "system" && hasArg(cmd.Args, "prune") {
			return mkAsk(r.Name(), "infra.docker_system_prune",
				"docker system prune removes unused containers, networks, and images", argv(cmd))
		}
	case "mongo", "mongosh", "mongodump", "mongorestore":
		full := argv(cmd)
		for _, tok := range mongoDestructiveTokens {
			if strings.Contains(full, tok) {
				return mkAsk(r.Name(), "infra.mongo_destructive",
					"Destructive MongoDB command: contains "+tok, full)
			}
		}
	case "terraform", "tofu":
		v := firstNonFlag(cmd.Args)
		if contains(terraformDestructive, v) {
			return mkAsk(r.Name(), "infra.terraform_mutation",
				cmd.Name+" mutation: "+cmd.Name+" "+v, argv(cmd))
		}
		// `terraform state rm/mv/push`
		if v == "state" {
			rest := cmd.Args[indexOf(cmd.Args, "state")+1:]
			if firstNonFlag(rest) == "rm" || firstNonFlag(rest) == "mv" || firstNonFlag(rest) == "push" {
				return mkAsk(r.Name(), "infra.terraform_state_mutation",
					cmd.Name+" state mutation", argv(cmd))
			}
		}
	case "gsutil":
		if contains(gsutilDestructive, firstNonFlag(cmd.Args)) {
			return mkAsk(r.Name(), "infra.gsutil_mutation",
				"GCS mutation: gsutil "+firstNonFlag(cmd.Args), argv(cmd))
		}
	case "git":
		// git push --force / -f
		if firstNonFlag(cmd.Args) == "push" {
			for _, a := range cmd.Args {
				if a == "--force" || a == "-f" || a == "--force-with-lease" || a == "+HEAD" {
					return mkAsk(r.Name(), "infra.git_force_push",
						"Git force push", argv(cmd))
				}
				if strings.HasPrefix(a, "--force-with-lease=") {
					return mkAsk(r.Name(), "infra.git_force_push",
						"Git force push with lease", argv(cmd))
				}
				// short-flag combo like -fu
				if strings.HasPrefix(a, "-") && len(a) >= 2 && a[1] != '-' && strings.ContainsRune(a, 'f') {
					return mkAsk(r.Name(), "infra.git_force_push",
						"Git force push", argv(cmd))
				}
			}
		}
	case "curl":
		method := curlMethod(cmd.Args)
		if method != "POST" && method != "PUT" && method != "DELETE" && method != "PATCH" {
			return nil
		}
		joined := strings.ToLower(argv(cmd))
		// Mutating OpenSearch / Elasticsearch requests (existing).
		if strings.Contains(joined, "opensearch") ||
			strings.Contains(joined, "elasticsearch") ||
			strings.Contains(joined, ":9200") ||
			strings.Contains(joined, ":9300") {
			return mkAsk(r.Name(), "infra.opensearch_mutation",
				"Mutating "+method+" request to OpenSearch/Elasticsearch", argv(cmd))
		}
		// Cloud control-plane API endpoints (PocketOS-class coverage).
		for _, h := range cloudControlPlaneHosts {
			if strings.Contains(joined, h) {
				return mkAsk(r.Name(), "infra.cloud_api_mutation",
					"Mutating "+method+" request to cloud control-plane API ("+h+")", argv(cmd))
			}
		}
		// GraphQL mutation in body — catches custom GraphQL endpoints not in
		// the hostname list. Word-boundary check on "mutation" to avoid
		// matching the literal "mutation" appearing in field names.
		if strings.Contains(joined, "graphql") &&
			(strings.Contains(joined, " mutation ") ||
				strings.Contains(joined, "\"mutation") ||
				strings.Contains(joined, "{mutation") ||
				strings.Contains(joined, "{ mutation")) {
			return mkAsk(r.Name(), "infra.graphql_mutation",
				"Mutating GraphQL request (mutation in body)", argv(cmd))
		}
	case "aws":
		// AWS CLI: verbs starting with delete-/terminate-/destroy-/purge-/
		// remove-/deregister-/revoke- mutate AWS resources.
		for _, a := range cmd.Args {
			if a == "" || strings.HasPrefix(a, "-") {
				continue
			}
			if strings.HasPrefix(a, "delete-") ||
				strings.HasPrefix(a, "terminate-") ||
				strings.HasPrefix(a, "destroy-") ||
				strings.HasPrefix(a, "purge-") ||
				strings.HasPrefix(a, "remove-") ||
				strings.HasPrefix(a, "deregister-") ||
				strings.HasPrefix(a, "revoke-") {
				return mkAsk(r.Name(), "infra.aws_destructive",
					"Destructive aws command: "+a, argv(cmd))
			}
		}
		// `aws s3 rm s3://bucket/...` (without --recursive a single object;
		// with --recursive, a tree). Either is a deletion.
		if seq(cmd.Args, "s3", "rm") {
			return mkAsk(r.Name(), "infra.aws_s3_rm",
				"aws s3 rm — removes S3 objects", argv(cmd))
		}
	case "az":
		// Azure CLI: `delete` / `purge` as a verb anywhere in argv. Azure
		// uses noun-verb structure (`az group delete`, `az vm delete`,
		// `az storage account delete`).
		for _, a := range cmd.Args {
			if a == "delete" || a == "purge" {
				return mkAsk(r.Name(), "infra.azure_destructive",
					"Destructive az command: contains "+a, argv(cmd))
			}
		}
	case "oci":
		// Oracle Cloud CLI: `delete` / `terminate` as the action verb.
		for _, a := range cmd.Args {
			if a == "delete" || a == "terminate" {
				return mkAsk(r.Name(), "infra.oci_destructive",
					"Destructive oci command: contains "+a, argv(cmd))
			}
		}
	case "ibmcloud":
		// IBM Cloud CLI: `delete` verb plus hyphenated *-delete/*-rm forms
		// (`is volume-delete`, `cs cluster-rm`, `ks cluster-rm`).
		for _, a := range cmd.Args {
			if a == "delete" || a == "destroy" {
				return mkAsk(r.Name(), "infra.ibmcloud_destructive",
					"Destructive ibmcloud command: contains "+a, argv(cmd))
			}
			if strings.HasSuffix(a, "-delete") || strings.HasSuffix(a, "-rm") || strings.HasSuffix(a, "-destroy") {
				return mkAsk(r.Name(), "infra.ibmcloud_destructive",
					"Destructive ibmcloud command: "+a, argv(cmd))
			}
		}
	}
	return nil
}

// --- helpers ---

func firstNonFlag(args []string) string {
	for _, a := range args {
		if a == "--" {
			continue
		}
		if strings.HasPrefix(a, "-") {
			continue
		}
		return a
	}
	return ""
}

func contains(haystack []string, needle string) bool {
	if needle == "" {
		return false
	}
	for _, h := range haystack {
		if h == needle {
			return true
		}
	}
	return false
}

func indexOf(args []string, target string) int {
	for i, a := range args {
		if a == target {
			return i
		}
	}
	return -1
}

// curlMethod scans for `-X METHOD` or `--request METHOD`.
func curlMethod(args []string) string {
	for i, a := range args {
		if (a == "-X" || a == "--request") && i+1 < len(args) {
			return strings.ToUpper(args[i+1])
		}
		if strings.HasPrefix(a, "-X") && len(a) > 2 {
			return strings.ToUpper(a[2:])
		}
		if strings.HasPrefix(a, "--request=") {
			return strings.ToUpper(strings.TrimPrefix(a, "--request="))
		}
	}
	return ""
}

// hasRemoteCommandMutation: `... --command=<body>` or `--command <body>` with
// destructive verb inside.
func hasRemoteCommandMutation(args []string) bool {
	body := ""
	for i, a := range args {
		if a == "--command" && i+1 < len(args) {
			body = args[i+1]
			break
		}
		if strings.HasPrefix(a, "--command=") {
			body = strings.TrimPrefix(a, "--command=")
			break
		}
	}
	if body == "" {
		return false
	}
	mutators := []string{"rm ", "apt ", "snap ", "install", "uninstall", "systemctl",
		"reboot", "shutdown", "mv ", "cp ", "chmod", "chown", "sed ", "tee ", "dd ",
		"mkfs", "mount", "umount", "iptables", "ufw"}
	for _, m := range mutators {
		if strings.Contains(body, m) {
			return true
		}
	}
	return false
}
