#!/bin/bash
# Scan ezra-prime conversations for user corrections and learning opportunities

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DATA_DIR="${SCRIPT_DIR}/../data"
OUTPUT="${DATA_DIR}/corrections.json"

# Ensure data directory exists
mkdir -p "$DATA_DIR"

# Check for API key
if [ -z "$LETTA_API_KEY" ]; then
  echo "ERROR: LETTA_API_KEY not set"
  exit 1
fi

AGENT_ID="${1:-agent-57ce3ea1-72ad-43e5-a444-7e3724f706e8}"  # ezra-prime default
LIMIT="${2:-10}"  # Number of recent conversations to scan

echo "Scanning $LIMIT recent conversations for corrections..."

# Fetch recent conversations
CONVS=$(curl -s "https://api.letta.com/v1/conversations?agent_id=$AGENT_ID&limit=$LIMIT" \
  -H "Authorization: Bearer $LETTA_API_KEY" | jq -r '.[].id')

# Collect all messages to temp file
TEMP_FILE=$(mktemp)
echo "[]" > "$TEMP_FILE"

for conv_id in $CONVS; do
  MSGS=$(curl -s "https://api.letta.com/v1/conversations/${conv_id}/messages?limit=20" \
    -H "Authorization: Bearer $LETTA_API_KEY" 2>/dev/null)
  # Append to temp file
  jq -s 'add' "$TEMP_FILE" <(echo "$MSGS") > "${TEMP_FILE}.new" && mv "${TEMP_FILE}.new" "$TEMP_FILE"
done

# Analyze for corrections
node -e "
const fs = require('fs');
const messages = JSON.parse(fs.readFileSync('$TEMP_FILE'));

// Correction signal patterns
const correctionPatterns = [
  // Direct corrections
  /that'?s (not|wrong|incorrect)/i,
  /you('re| are) wrong/i,
  /actually,? (it'?s|the|you)/i,
  /no,? (it'?s|that'?s|the)/i,
  /correction:/i,
  /let me correct/i,
  
  // Research requests after bad answer
  /you should (check|look at|read|research)/i,
  /check (the|this) (docs|documentation|repo|github)/i,
  /did you (research|check|look)/i,
  
  // Frustration signals
  /you didn'?t (answer|understand|research)/i,
  /that doesn'?t (help|answer|make sense)/i,
  /try again/i,
  /not what I asked/i,
  
  // Team corrections (high priority)
  /\[(cameron|swooders|pacjam|4shub|cpfiffer).*\]/i,
  
  // Link sharing after response (user providing source)
  /https?:\/\/[^\s]+\.(com|io|dev|org)/i
];

const corrections = [];
const teamCorrections = [];
const linkShares = [];

// Team member IDs
const teamIds = ['232237600818200576', '1068927648274063410']; // Add known team IDs

messages.forEach((m, idx) => {
  if (m.message_type !== 'user_message' || !m.content) return;
  
  const content = typeof m.content === 'string' ? m.content : '';
  const lower = content.toLowerCase();
  
  // Check for correction patterns
  correctionPatterns.forEach(pattern => {
    if (pattern.test(content)) {
      const entry = {
        date: m.created_at,
        content: content.substring(0, 500),
        pattern: pattern.toString(),
        conversation_id: m.conversation_id || 'unknown'
      };
      
      // Check if from team member
      if (/\[(cameron|swooders|pacjam|4shub|cpfiffer)/i.test(content)) {
        entry.priority = 'HIGH';
        entry.source = 'team';
        teamCorrections.push(entry);
      } else if (/https?:\/\//.test(content)) {
        entry.priority = 'MEDIUM';
        entry.source = 'user_with_link';
        linkShares.push(entry);
      } else {
        entry.priority = 'NORMAL';
        entry.source = 'user';
        corrections.push(entry);
      }
    }
  });
});

const result = {
  scanned_at: new Date().toISOString(),
  agent_id: '$AGENT_ID',
  conversations_scanned: $LIMIT,
  total_messages: messages.length,
  findings: {
    team_corrections: teamCorrections,
    user_corrections: corrections.slice(0, 20),
    link_shares: linkShares.slice(0, 10)
  },
  summary: {
    team_corrections_count: teamCorrections.length,
    user_corrections_count: corrections.length,
    link_shares_count: linkShares.length,
    action_required: teamCorrections.length > 0
  }
};

require('fs').writeFileSync('$OUTPUT', JSON.stringify(result, null, 2));

// Print summary
console.log('=== CORRECTION SCAN RESULTS ===');
console.log('Team corrections: ' + teamCorrections.length + (teamCorrections.length > 0 ? ' (ACTION REQUIRED)' : ''));
console.log('User corrections: ' + corrections.length);
console.log('Link shares: ' + linkShares.length);
console.log('');

if (teamCorrections.length > 0) {
  console.log('=== TEAM CORRECTIONS (HIGH PRIORITY) ===');
  teamCorrections.forEach(c => {
    console.log('Date: ' + c.date);
    console.log('Content: ' + c.content.substring(0, 200) + '...');
    console.log('---');
  });
}

if (corrections.length > 0) {
  console.log('=== USER CORRECTIONS ===');
  corrections.slice(0, 5).forEach(c => {
    console.log('Date: ' + c.date);
    console.log('Content: ' + c.content.substring(0, 200) + '...');
    console.log('---');
  });
}
"

echo ""
echo "Full results saved to $OUTPUT"
