#!/bin/bash
# Fetch recent conversations and messages from ezra-prime

HOURS=${1:-24}
LIMIT=${2:-50}
AGENT_ID=${EZRA_PRIME_AGENT_ID:-"agent-57ce3ea1-72ad-43e5-a444-7e3724f706e8"}
OUTPUT_DIR="/data/ezra/skills/ezra-monitor/data"

mkdir -p "$OUTPUT_DIR"

echo "Fetching conversations from last ${HOURS} hours..."

# Get conversations
CONVOS=$(curl -s "https://api.letta.com/v1/conversations?agent_id=${AGENT_ID}&limit=20" \
  -H "Authorization: Bearer $LETTA_API_KEY")

echo "$CONVOS" > "$OUTPUT_DIR/conversations.json"

# Extract conversation IDs and fetch messages
node -e "
const fs = require('fs');
const convos = JSON.parse(fs.readFileSync('$OUTPUT_DIR/conversations.json'));
const cutoff = Date.now() - ($HOURS * 60 * 60 * 1000);

const recent = convos.filter(c => new Date(c.created_at).getTime() > cutoff);
console.log('Recent conversations:', recent.length);

// Output IDs for message fetching
recent.forEach(c => console.log('CONV_ID:' + c.id));
" 2>/dev/null | while read line; do
  if [[ $line == CONV_ID:* ]]; then
    CONV_ID="${line#CONV_ID:}"
    echo "Fetching messages from $CONV_ID..."
    curl -s "https://api.letta.com/v1/conversations/${CONV_ID}/messages?limit=${LIMIT}" \
      -H "Authorization: Bearer $LETTA_API_KEY" >> "$OUTPUT_DIR/messages_raw.json"
    echo "" >> "$OUTPUT_DIR/messages_raw.json"
  else
    echo "$line"
  fi
done

# Combine and filter to user/assistant messages
node -e "
const fs = require('fs');
const raw = fs.readFileSync('$OUTPUT_DIR/messages_raw.json', 'utf8');
const messages = [];

// Parse each JSON array (separated by newlines)
raw.split('\n').forEach(line => {
  if (line.trim().startsWith('[')) {
    try {
      const parsed = JSON.parse(line);
      messages.push(...parsed);
    } catch(e) {}
  }
});

// Filter to relevant message types
const relevant = messages.filter(m => 
  ['user_message', 'assistant_message', 'tool_call_message', 'tool_return_message'].includes(m.message_type)
);

console.log('Total messages:', relevant.length);
fs.writeFileSync('$OUTPUT_DIR/messages.json', JSON.stringify(relevant, null, 2));
"

echo "Output saved to $OUTPUT_DIR/messages.json"
