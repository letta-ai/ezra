#!/bin/bash
# Search codebase for evidence of a claim

CLAIM="$1"
REPO_PATH="${2:-$HOME/lettabot}"

if [ -z "$CLAIM" ]; then
  echo "Usage: check-code.sh <claim> [repo_path]"
  exit 1
fi

echo "CLAIM: $CLAIM"
echo "METHOD: code"
echo "REPO: $REPO_PATH"
echo "---"

# Extract key terms from claim (simple word extraction)
TERMS=$(echo "$CLAIM" | tr '[:upper:]' '[:lower:]' | grep -oE '\b[a-z]{4,}\b' | sort -u | head -5)

FOUND=0
EVIDENCE=""

for term in $TERMS; do
  # Search for term in code files
  RESULTS=$(grep -ri "$term" "$REPO_PATH/src" --include="*.ts" --include="*.js" --include="*.py" 2>/dev/null | head -3)
  if [ -n "$RESULTS" ]; then
    FOUND=$((FOUND + 1))
    EVIDENCE="$EVIDENCE\n  - TERM '$term':\n$(echo "$RESULTS" | sed 's/^/      /')"
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
