#!/usr/bin/env bash
# Genera un PDF de diapositivas a partir de un markdown con bloques ::: slide
# Uso: docs/assets/build-slides.sh <nombre-sin-extension>
set -euo pipefail

DOC="${1:?uso: build-slides.sh <nombre-sin-extension>}"
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
DIR="$ROOT/docs/docs"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

pandoc "$DIR/$DOC.md" -o "$TMP/doc.html" --standalone \
  --css="$ROOT/docs/assets/slides-print.css" --embed-resources

"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless --disable-gpu \
  --no-pdf-header-footer --virtual-time-budget=8000 \
  --print-to-pdf="$DIR/$DOC.pdf" "file://$TMP/doc.html" 2>/dev/null

echo "generado: $DOC.pdf"
