#!/usr/bin/env bash
# Re-download the agency PDFs listed in papers/DOWNLOAD_MANIFEST.csv.
#
# The PDFs are ~110 MB of freely available government documents, so they are
# not stored in git. Their plain-text extractions ARE stored (papers/*.txt),
# and those are what every number in db/ was read from. Run this only if you
# want the original PDFs back, e.g. to check a page or a figure.
#
# Usage:  bash scripts/fetch_papers.sh
set -uo pipefail

here="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
manifest="$here/papers/DOWNLOAD_MANIFEST.csv"
[ -f "$manifest" ] || { echo "missing $manifest" >&2; exit 1; }

# Some agency hosts (CDC, OEHHA) reject a bare curl with HTTP 403.
UA='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36'

ok=0; fail=0
while IFS=, read -r filename url logged; do
    [ "$filename" = "filename" ] && continue
    [ -z "${url:-}" ] && continue
    filename="${filename%\"}"; filename="${filename#\"}"
    dest="$here/papers/$filename"
    if [ -s "$dest" ]; then
        echo "have    $filename"; ok=$((ok+1)); continue
    fi
    echo "fetch   $filename"
    if curl -fsSL --max-time 300 -A "$UA" \
            -H 'Accept: application/pdf,*/*' \
            -H 'Accept-Language: en-US,en;q=0.9' \
            -H 'Sec-Fetch-Dest: document' -H 'Sec-Fetch-Mode: navigate' \
            -H 'Sec-Fetch-Site: none' \
            -o "$dest" "$url" && [ -s "$dest" ]; then
        # Guard against a WAF challenge page being saved as a .pdf
        if head -c 5 "$dest" | grep -q '%PDF'; then
            ok=$((ok+1))
        else
            echo "  !! not a PDF (likely a bot challenge); removing" >&2
            rm -f "$dest"; fail=$((fail+1))
        fi
    else
        echo "  !! failed: $url" >&2
        rm -f "$dest"; fail=$((fail+1))
    fi
done < "$manifest"

echo
echo "$ok present, $fail failed"
[ "$fail" -eq 0 ] || echo "See papers/SOURCES_*.md for alternative URLs and notes." >&2
