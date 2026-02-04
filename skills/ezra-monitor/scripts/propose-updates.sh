#!/bin/bash
# Generate proposed memory block updates based on analysis

INPUT=${1:-"/data/ezra/skills/ezra-monitor/data/analysis.json"}
AGENT_ID=${EZRA_PRIME_AGENT_ID:-"agent-57ce3ea1-72ad-43e5-a444-7e3724f706e8"}
OUTPUT_DIR="/data/ezra/skills/ezra-monitor/data"

# Fetch current memory blocks for comparison
echo "Fetching current memory blocks..."
curl -s "https://api.letta.com/v1/agents/${AGENT_ID}/core-memory/blocks" \
  -H "Authorization: Bearer $LETTA_API_KEY" > "$OUTPUT_DIR/current_blocks.json"

node -e "
const fs = require('fs');
const analysis = JSON.parse(fs.readFileSync('$INPUT'));
const blocks = JSON.parse(fs.readFileSync('$OUTPUT_DIR/current_blocks.json'));

const proposals = {
  generated_at: new Date().toISOString(),
  corrections_to_review: [],
  pattern_observations: [],
  block_suggestions: []
};

// Flag potential corrections for manual review
if (analysis.potential_corrections?.length > 0) {
  proposals.corrections_to_review = analysis.potential_corrections.map(c => ({
    date: c.date,
    content: c.content.slice(0, 500),
    action: 'Review for factual corrections to add to response_guidelines'
  }));
}

// Suggest pattern observations
if (analysis.patterns && Object.keys(analysis.patterns).length > 0) {
  const topPatterns = Object.entries(analysis.patterns).slice(0, 10);
  proposals.pattern_observations = topPatterns.map(([word, count]) => ({
    term: word,
    frequency: count,
    suggestion: 'Consider if this recurring topic needs better documentation'
  }));
}

// Check memory block sizes and suggest cleanup
blocks.forEach(b => {
  const usage = b.value?.length || 0;
  const limit = b.limit || 5000;
  const pct = (usage / limit * 100).toFixed(1);
  
  if (usage / limit > 0.85) {
    proposals.block_suggestions.push({
      block: b.label,
      current_size: usage,
      limit: limit,
      usage_pct: pct + '%',
      action: 'Consider archiving old entries or splitting into sub-blocks'
    });
  }
});

// Tool usage insights
if (analysis.tool_usage) {
  const tools = Object.entries(analysis.tool_usage).sort((a,b) => b[1]-a[1]);
  proposals.tool_insights = {
    most_used: tools.slice(0, 5),
    total_calls: tools.reduce((sum, [_, c]) => sum + c, 0)
  };
}

fs.writeFileSync('$OUTPUT_DIR/proposals.json', JSON.stringify(proposals, null, 2));

// Output summary
console.log('=== MEMORY UPDATE PROPOSALS ===');
console.log('');
console.log('Corrections to review:', proposals.corrections_to_review.length);
console.log('Pattern observations:', proposals.pattern_observations.length);
console.log('Block maintenance suggestions:', proposals.block_suggestions.length);
console.log('');

if (proposals.corrections_to_review.length > 0) {
  console.log('--- CORRECTIONS TO REVIEW ---');
  proposals.corrections_to_review.forEach((c, i) => {
    console.log((i+1) + '. [' + c.date?.slice(0,10) + '] ' + c.content.slice(0, 100) + '...');
  });
}

if (proposals.block_suggestions.length > 0) {
  console.log('');
  console.log('--- BLOCKS NEAR CAPACITY ---');
  proposals.block_suggestions.forEach(b => {
    console.log('  ' + b.block + ': ' + b.usage_pct + ' (' + b.current_size + '/' + b.limit + ')');
  });
}
"

echo ""
echo "Full proposals saved to $OUTPUT_DIR/proposals.json"
