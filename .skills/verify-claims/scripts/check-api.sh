#!/bin/bash
# Test claims via live API calls

CLAIM="$1"

if [ -z "$CLAIM" ]; then
  echo "Usage: check-api.sh <claim>"
  exit 1
fi

if [ -z "$LETTA_API_KEY" ]; then
  echo "ERROR: LETTA_API_KEY not set"
  exit 1
fi

echo "CLAIM: $CLAIM"
echo "METHOD: api"
echo "---"

CLAIM_LOWER=$(echo "$CLAIM" | tr '[:upper:]' '[:lower:]')

# Pattern matching for common testable claims
if echo "$CLAIM_LOWER" | grep -q "pagination\|paginated\|\.items"; then
  echo "Testing: List agents pagination..."
  RESULT=$(curl -s "https://api.letta.com/v1/agents?limit=2" \
    -H "Authorization: Bearer $LETTA_API_KEY")
  
  # Check if result is array or has pagination wrapper
  IS_ARRAY=$(echo "$RESULT" | jq 'if type == "array" then "array" else "object" end' 2>/dev/null)
  HAS_ITEMS=$(echo "$RESULT" | jq 'has("items")' 2>/dev/null)
  
  echo "EVIDENCE:"
  echo "  - Response type: $IS_ARRAY"
  echo "  - Has .items field: $HAS_ITEMS"
  
  if [ "$HAS_ITEMS" = "true" ]; then
    echo "STATUS: VERIFIED"
    echo "CONFIDENCE: high"
  else
    echo "STATUS: PARTIAL"
    echo "CONFIDENCE: medium"
    echo "NOTE: Raw API returns array, SDK may wrap with .items"
  fi

elif echo "$CLAIM_LOWER" | grep -q "agent.*visible\|ade.*agent"; then
  echo "Testing: Agent visibility..."
  AGENTS=$(curl -s "https://api.letta.com/v1/agents?limit=5" \
    -H "Authorization: Bearer $LETTA_API_KEY" | jq 'length')
  
  echo "EVIDENCE:"
  echo "  - Found $AGENTS agents via API"
  echo "  - If agents exist, they're visible to API (and thus ADE)"
  
  if [ "$AGENTS" -gt 0 ]; then
    echo "STATUS: VERIFIED"
    echo "CONFIDENCE: high"
  else
    echo "STATUS: NEEDS_MANUAL"
    echo "CONFIDENCE: low"
  fi

elif echo "$CLAIM_LOWER" | grep -q "archival\|vector\|embed"; then
  echo "Testing: Archival/embedding config..."
  # Get first agent's embedding config
  AGENT_ID=$(curl -s "https://api.letta.com/v1/agents?limit=1" \
    -H "Authorization: Bearer $LETTA_API_KEY" | jq -r '.[0].id // empty')
  
  if [ -n "$AGENT_ID" ]; then
    EMBED_CONFIG=$(curl -s "https://api.letta.com/v1/agents/$AGENT_ID" \
      -H "Authorization: Bearer $LETTA_API_KEY" | jq '.embedding_config')
    
    echo "EVIDENCE:"
    echo "  - Embedding config exists: $(echo "$EMBED_CONFIG" | jq 'keys')"
    echo "STATUS: VERIFIED"
    echo "CONFIDENCE: high"
  else
    echo "STATUS: NEEDS_MANUAL"
    echo "CONFIDENCE: low"
  fi

else
  echo "STATUS: NEEDS_MANUAL"
  echo "CONFIDENCE: low"
  echo "NOTE: No automated test pattern for this claim type"
  echo "SUGGESTION: Write a custom test or verify manually"
fi
