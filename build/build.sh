#!/usr/bin/env bash
# Builds index.html and Flight_Software_Architecture.pdf from the chapters under
# docs/, in the order build/order.txt lists them.
#
# Needs pandoc, node with npx, and a Chromium or Chrome binary. The mermaid
# diagrams are rendered to SVG once and cached in build/.cache, so a rebuild that
# changes no diagram does not need the network.
set -Eeuo pipefail

BUILD_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$BUILD_DIR")"
WORK_DIR="$(mktemp -d /tmp/fsw-architecture.XXXXXX)"
TITLE="Flight Software Architecture"

trap 'rm -rf -- "$WORK_DIR"' EXIT

need() {
	command -v "$1" >/dev/null 2>&1 || {
		echo "ERROR: $1 is required" >&2
		exit 1
	}
}
need pandoc
need npx

# Chromium prints the PDF. Puppeteer's copy is used when the system has none,
# because mermaid-cli downloads it anyway.
find_chrome() {
	local candidate
	for candidate in "${CHROME:-}" chromium chromium-browser google-chrome google-chrome-stable; do
		[[ -n "$candidate" ]] && command -v "$candidate" >/dev/null 2>&1 &&
			command -v "$candidate" && return 0
	done
	candidate="$(find "$HOME/.cache/puppeteer" -type f -name chrome 2>/dev/null | sort | tail -1)"
	[[ -x "$candidate" ]] && echo "$candidate" && return 0
	return 1
}

echo "BUILD: collecting chapters"
: >"$WORK_DIR/document.md"
while IFS= read -r chapter; do
	[[ -n "$chapter" ]] || continue
	[[ -f "$ROOT_DIR/$chapter" ]] || {
		echo "ERROR: $chapter is listed in order.txt but missing" >&2
		exit 1
	}
	cat "$ROOT_DIR/$chapter" >>"$WORK_DIR/document.md"
	printf '\n\n' >>"$WORK_DIR/document.md"
done <"$BUILD_DIR/order.txt"

# Image paths are relative to each chapter's own directory; one concatenated file
# resolves them from the repository root instead.
sed -i -E 's#\]\((\.\./)+assets/#](assets/#g' "$WORK_DIR/document.md"

# A chapter README lists its subsections so the directory is useful on GitHub.
# The built document has its own table of contents, so that list comes out.
sed -i '/<!-- nav:start -->/,/<!-- nav:end -->/d' "$WORK_DIR/document.md"

echo "BUILD: rendering diagrams"
python3 "$BUILD_DIR/render-mermaid.py" "$WORK_DIR/document.md" "$BUILD_DIR/.cache"

echo "BUILD: writing index.html"
pandoc "$WORK_DIR/document.md" \
	--from=markdown+pipe_tables+raw_html \
	--to=html5 \
	--standalone \
	--embed-resources \
	--toc --toc-depth=3 \
	--metadata title="$TITLE" \
	--css="$BUILD_DIR/style.css" \
	--resource-path="$ROOT_DIR" \
	--output="$ROOT_DIR/index.html"

echo "BUILD: printing the PDF"
chrome="$(find_chrome)" || {
	echo "ERROR: no Chromium or Chrome found; set CHROME to its path" >&2
	exit 1
}
"$chrome" --headless --disable-gpu --no-sandbox --no-pdf-header-footer \
	--print-to-pdf="$ROOT_DIR/Flight_Software_Architecture.pdf" \
	"file://$ROOT_DIR/index.html" >"$WORK_DIR/chrome.log" 2>&1 || {
	cat "$WORK_DIR/chrome.log" >&2
	exit 1
}

printf 'BUILD RESULT: PASS  index.html %s  pdf %s\n' \
	"$(du -h "$ROOT_DIR/index.html" | cut -f1)" \
	"$(du -h "$ROOT_DIR/Flight_Software_Architecture.pdf" | cut -f1)"
