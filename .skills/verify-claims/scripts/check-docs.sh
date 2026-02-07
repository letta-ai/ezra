#!/bin/bash
# Search Letta documentation for evidence of a claim

CLAIM="$1"
DOCS_PATH="${2:-$HOME/letta/letta-sdk-api-docs/src}"

if [ -z "$CLAIM" ]; then
  echo "Usage: check-docs.sh <claim> [docs_path]"
  exit 1
fi

echo "CLAIM: $CLAIM"
echo "METHOD: docs"
echo "DOCS: $DOCS_PATH"
echo "---"

# Extract key terms
TERMS=$(echo "$CLAIM" | tr '[:upper:]' '[:lower:]' | grep -oE '\b[a-z]{4,}\b' | sort -u | head -5)

FOUND=0
EVIDENCE=""

for term in $TERMS; do
  # Search docs
  RESULTS=$(grep -ri "$term" "$DOCS_PATH" --include="*.md" --include="*.mdx" 2>/dev/null | head -3)
  if [ -n "$RESULTS" ]; then
    FOUND=$((FOUND + 1))
    # Extract just filenames and snippets
    SNIPPETS=$(echo "$RESULTS" | sed 's|.*/||' | cut -c1-100)
    EVIDENCE="$EVIDENCE\n  - TERM '$term':\n$(echo "$SNIPPETS" | sed 's/^/      /')"
  fi
done

if [ $FOUND -ge 2 ]; then
  echo "STATUS: VERIFIED"
  echo "CONFIDENCE: high"
elif [ $FOUND -eq 1 ]; then
  echo "STATUS: PARTIAL"
  echo "CONFIDENCE: medium"
else
  echo "STATUS: NOT_VERIFIED"
  echo "CONFIDENCE: low"
fi

echo -e "EVIDENCE:$EVIDENCE"
