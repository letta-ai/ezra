#!/bin/bash
# Main verification orchestrator - runs all verification methods

CLAIM="$1"
REPO_PATH="${2:-$HOME/lettabot}"
DOCS_PATH="${3:-$HOME/letta/letta-sdk-api-docs/src}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [ -z "$CLAIM" ]; then
  echo "Usage: verify.sh <claim> [repo_path] [docs_path]"
  echo ""
  echo "Example: verify.sh 'lettabot supports skills'"
  exit 1
fi

echo "=========================================="
echo "CLAIM VERIFICATION REPORT"
echo "=========================================="
echo "Claim: $CLAIM"
echo "Date: $(date -u +"%Y-%m-%dT%H:%M:%SZ")"
echo "=========================================="
echo ""

# Run all verification methods
echo "=== CODE INSPECTION ==="
CODE_RESULT=$("$SCRIPT_DIR/check-code.sh" "$CLAIM" "$REPO_PATH" 2>&1)
echo "$CODE_RESULT"
CODE_STATUS=$(echo "$CODE_RESULT" | grep "^STATUS:" | cut -d' ' -f2)
echo ""

echo "=== DOCUMENTATION SEARCH ==="
DOCS_RESULT=$("$SCRIPT_DIR/check-docs.sh" "$CLAIM" "$DOCS_PATH" 2>&1)
echo "$DOCS_RESULT"
DOCS_STATUS=$(echo "$DOCS_RESULT" | grep "^STATUS:" | cut -d' ' -f2)
echo ""

echo "=== LIVE API TEST ==="
API_RESULT=$("$SCRIPT_DIR/check-api.sh" "$CLAIM" 2>&1)
echo "$API_RESULT"
API_STATUS=$(echo "$API_RESULT" | grep "^STATUS:" | cut -d' ' -f2)
echo ""

# Aggregate results
echo "=========================================="
echo "SUMMARY"
echo "=========================================="
echo "Code:  $CODE_STATUS"
echo "Docs:  $DOCS_STATUS"
echo "API:   $API_STATUS"
echo ""

VERIFIED_COUNT=0
[ "$CODE_STATUS" = "VERIFIED" ] && VERIFIED_COUNT=$((VERIFIED_COUNT + 1))
[ "$DOCS_STATUS" = "VERIFIED" ] && VERIFIED_COUNT=$((VERIFIED_COUNT + 1))
[ "$API_STATUS" = "VERIFIED" ] && VERIFIED_COUNT=$((VERIFIED_COUNT + 1))

if [ $VERIFIED_COUNT -ge 2 ]; then
  echo "FINAL: VERIFIED (${VERIFIED_COUNT}/3 methods confirmed)"
  echo "RECOMMENDATION: Safe to add to memory with evidence"
elif [ $VERIFIED_COUNT -eq 1 ]; then
  echo "FINAL: PARTIAL (${VERIFIED_COUNT}/3 methods confirmed)"
  echo "RECOMMENDATION: Add with caveat or seek additional verification"
else
  echo "FINAL: NOT_VERIFIED"
  echo "RECOMMENDATION: Do NOT add to memory without manual verification"
fi
