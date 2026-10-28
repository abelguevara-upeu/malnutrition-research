#!/usr/bin/env bash
# Genera un PDF de diapositivas a partir de un markdown con bloques ::: slide
# Uso: manuscrito/assets/build-slides.sh <carpeta>/<nombre-sin-extension>  (ej. validacion/presentacion_panel_expertos)
set -euo pipefail

DOC_PATH="${1:?uso: build-slides.sh <carpeta>/<nombre-sin-extension>}"
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
DIR="$ROOT/manuscrito/$(dirname "$DOC_PATH")"
DOC="$(basename "$DOC_PATH")"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

# --resource-path permite que las rutas de imagen del markdown se resuelvan
# desde la raiz del repositorio y no desde el directorio del documento.
pandoc "$DIR/$DOC.md" -o "$TMP/doc.html" --standalone \
  --css="$ROOT/manuscrito/assets/slides-print.css" --embed-resources \
  --resource-path="$ROOT:$DIR"

"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless --disable-gpu \
  --no-pdf-header-footer --virtual-time-budget=8000 \
  --print-to-pdf="$DIR/$DOC.pdf" "file://$TMP/doc.html" 2>/dev/null

echo "generado: $DOC.pdf"
