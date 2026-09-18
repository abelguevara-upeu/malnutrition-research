#!/usr/bin/env bash
# Genera el PDF de un documento markdown de docs/docs.
# Uso: docs/assets/build-pdf.sh <nombre-sin-extension>
#
# Pandoc escapa las entidades HTML dentro de los bloques mermaid, de modo que
# hay que desescaparlas antes de que la libreria las lea; sin ese paso el
# diagrama sale como "Syntax error in text".
set -euo pipefail

DOC="${1:?uso: build-pdf.sh <nombre-sin-extension>}"
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
DIR="$ROOT/docs/docs"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

pandoc "$DIR/$DOC.md" -o "$TMP/doc.html" --standalone \
  --css="$ROOT/docs/assets/doc-print.css" --embed-resources

python3 - "$TMP/doc.html" <<'PY'
import sys, re, html, pathlib
p = pathlib.Path(sys.argv[1]); h = p.read_text(encoding="utf-8")
m = re.search(r'<pre class="mermaid">\s*<code>(.*?)</code>\s*</pre>', h, re.S)
if m:
    h = h[:m.start()] + '<pre class="mermaid">' + html.unescape(m.group(1)) + '</pre>' + h[m.end():]
if 'mermaid.min.js' not in h and 'class="mermaid"' in h:
    h = h.replace('</head>', '''<script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
<script>mermaid.initialize({startOnLoad:true,theme:"base",themeVariables:{fontSize:"13px",primaryColor:"#eef3f9",primaryBorderColor:"#003366",primaryTextColor:"#1a2530",lineColor:"#5a7ca6"}});</script>
<style>.mermaid{text-align:center;margin:8px 0 12px;page-break-inside:avoid;background:none;border:none;padding:0}
.mermaid svg{width:100%;max-width:520px;height:auto}</style>
</head>''')
p.write_text(h, encoding="utf-8")
PY

"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless --disable-gpu \
  --no-pdf-header-footer --virtual-time-budget=15000 \
  --print-to-pdf="$DIR/$DOC.pdf" "file://$TMP/doc.html" 2>/dev/null

pandoc "$DIR/$DOC.md" -o "$DIR/$DOC.docx"
echo "generado: $DOC.pdf y $DOC.docx"
