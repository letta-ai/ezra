#!/bin/bash
# Analyze messages for patterns, recurring issues, and potential memory updates

INPUT=${1:-"/data/ezra/skills/ezra-monitor/data/messages.json"}
OUTPUT_DIR="/data/ezra/skills/ezra-monitor/data"

node -e "
const fs = require('fs');
const messages = JSON.parse(fs.readFileSync('$INPUT'));

const analysis = {
  total_messages: messages.length,
  user_messages: [],
  assistant_responses: [],
  tool_calls: [],
  patterns: {},
  potential_corrections: [],
  unanswered_patterns: []
};

// Extract content from messages
messages.forEach(m => {
  if (m.message_type === 'user_message' && m.content) {
    analysis.user_messages.push({
      date: m.date,
      content: typeof m.content === 'string' ? m.content : JSON.stringify(m.content)
    });
  } else if (m.message_type === 'assistant_message' && m.content) {
    analysis.assistant_responses.push({
      date: m.date,
      content: typeof m.content === 'string' ? m.content : JSON.stringify(m.content)
    });
  } else if (m.message_type === 'tool_call_message') {
    const toolName = m.tool_call?.name || 'unknown';
    analysis.tool_calls.push(toolName);
  }
});

// Count tool usage
const toolCounts = {};
analysis.tool_calls.forEach(t => {
  toolCounts[t] = (toolCounts[t] || 0) + 1;
});
analysis.tool_usage = toolCounts;

// Look for correction indicators in user messages
const correctionKeywords = ['wrong', 'incorrect', 'actually', 'no,', 'that\\'s not', 'correction'];
analysis.user_messages.forEach(m => {
  const lower = m.content.toLowerCase();
  if (correctionKeywords.some(k => lower.includes(k))) {
    analysis.potential_corrections.push(m);
  }
});

// Look for repeated question patterns (keywords appearing multiple times)
const questionWords = {};
analysis.user_messages.forEach(m => {
  const words = m.content.toLowerCase().split(/\\s+/);
  words.forEach(w => {
    if (w.length > 5) {
      questionWords[w] = (questionWords[w] || 0) + 1;
    }
  });
});

// Find words appearing 3+ times (potential recurring topics)
Object.entries(questionWords)
  .filter(([w, c]) => c >= 3)
  .sort((a, b) => b[1] - a[1])
  .slice(0, 20)
  .forEach(([word, count]) => {
    analysis.patterns[word] = count;
  });

// Summary
analysis.summary = {
  message_count: messages.length,
  user_questions: analysis.user_messages.length,
  responses: analysis.assistant_responses.length,
  potential_corrections: analysis.potential_corrections.length,
  top_tools: Object.entries(toolCounts).sort((a,b) => b[1]-a[1]).slice(0,5)
};

fs.writeFileSync('$OUTPUT_DIR/analysis.json', JSON.stringify(analysis, null, 2));
console.log(JSON.stringify(analysis.summary, null, 2));
"

echo ""
echo "Full analysis saved to $OUTPUT_DIR/analysis.json"
