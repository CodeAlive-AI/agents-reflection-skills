.PHONY: build build-all test fmt vet bench clean install watch

# Default target: build the binary in place. Run after editing any .go
# source so the next hook invocation picks up the change.
build:
	go build -o bash_guard.bin .

# Cross-compile release binaries into ./dist/. Used by the release
# workflow; produces stable filenames the prebuilt installer expects.
# CGO is disabled to keep binaries fully static.
build-all: clean-dist
	@mkdir -p dist
	GOOS=darwin  GOARCH=arm64 CGO_ENABLED=0 go build -trimpath -ldflags="-s -w" -o dist/bash-guard-darwin-arm64 .
	GOOS=darwin  GOARCH=amd64 CGO_ENABLED=0 go build -trimpath -ldflags="-s -w" -o dist/bash-guard-darwin-amd64 .
	GOOS=linux   GOARCH=arm64 CGO_ENABLED=0 go build -trimpath -ldflags="-s -w" -o dist/bash-guard-linux-arm64 .
	GOOS=linux   GOARCH=amd64 CGO_ENABLED=0 go build -trimpath -ldflags="-s -w" -o dist/bash-guard-linux-amd64 .
	@cd dist && shasum -a 256 bash-guard-* > SHA256SUMS
	@ls -lh dist/

clean-dist:
	rm -rf dist/

test:
	go test -count=1 ./...

vet:
	go vet ./...

fmt:
	gofmt -w .

bench:
	go test -run='^$$' -bench=. -benchmem ./...

clean:
	rm -f bash_guard.bin build.log

# Run install.sh from the parent directory.
install:
	../install.sh --shadow

# Auto-rebuild on .go save while the dev edits. Requires `entr`:
#     brew install entr
# Use this instead of a runtime build-on-stale wrapper.
watch:
	@if ! command -v entr >/dev/null; then \
		echo "entr not installed. brew install entr" >&2; exit 1; \
	fi
	ls *.go | entr -c go build -o bash_guard.bin .
