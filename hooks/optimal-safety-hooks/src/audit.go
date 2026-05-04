package main

import (
	"crypto/sha256"
	"encoding/hex"
	"encoding/json"
	"fmt"
	"os"
	"path/filepath"
	"sync"
	"time"
)

const (
	auditMaxBytes  = 10 * 1024 * 1024 // 10 MB before rotation
	auditKeepFiles = 3
)

// AuditEntry is one JSONL row.
type AuditEntry struct {
	TS          string  `json:"ts"`
	Mode        string  `json:"mode"` // live | shadow | dry-run
	Decision    string  `json:"decision"`
	Rule        string  `json:"rule"`
	ReasonCode  string  `json:"reason_code"`
	LatencyMS   float64 `json:"latency_ms"`
	CommandHash string  `json:"command_hash"`
	CommandLen  int     `json:"command_len"`
	Command     string  `json:"command,omitempty"` // only when BASH_GUARD_LOG_COMMANDS=1
	WouldDecide string  `json:"would_decide,omitempty"`
}

var auditMu sync.Mutex

func writeAudit(entry AuditEntry) {
	logDir := filepath.Join(homeDir(), ".claude", "logs")
	if err := os.MkdirAll(logDir, 0o700); err != nil {
		return
	}
	path := filepath.Join(logDir, "bash-guard.jsonl")

	auditMu.Lock()
	defer auditMu.Unlock()

	rotateIfNeeded(path)

	f, err := os.OpenFile(path, os.O_CREATE|os.O_APPEND|os.O_WRONLY, 0o600)
	if err != nil {
		return
	}
	defer f.Close()

	enc := json.NewEncoder(f)
	enc.SetEscapeHTML(false)
	_ = enc.Encode(entry)

	if os.Getenv("BASH_GUARD_DEBUG") != "" {
		// Mirror to stderr for live debugging.
		_ = json.NewEncoder(os.Stderr).Encode(entry)
	}
}

func rotateIfNeeded(path string) {
	st, err := os.Stat(path)
	if err != nil {
		return
	}
	if st.Size() < auditMaxBytes {
		return
	}
	// Cascade-rename: bash-guard.jsonl.2 → .3, .1 → .2, current → .1
	for i := auditKeepFiles - 1; i >= 1; i-- {
		from := fmt.Sprintf("%s.%d", path, i)
		to := fmt.Sprintf("%s.%d", path, i+1)
		_ = os.Rename(from, to) // ignore ENOENT
	}
	_ = os.Rename(path, path+".1")
}

func hashCommand(cmd string) string {
	h := sha256.Sum256([]byte(cmd))
	return "sha256:" + hex.EncodeToString(h[:8]) // short prefix for log compactness
}

func nowISO() string {
	return time.Now().UTC().Format(time.RFC3339)
}
