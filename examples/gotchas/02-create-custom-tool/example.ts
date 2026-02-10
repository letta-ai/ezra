/**
 * Correct way to create custom tools for Letta agents (TypeScript).
 *
 * Key rules:
 * 1. Tool source code is ALWAYS Python (even from TypeScript SDK)
 * 2. Imports inside the function
 * 3. os.getenv() for secrets
 */

import Letta from "@letta-ai/letta-client";

const client = new Letta({ apiKey: process.env.LETTA_API_KEY });

// Tool source code is Python, even when using TypeScript SDK
const toolSource = `
def lookup_weather(location: str) -> str:
    """Get the current weather for a location.

    Args:
        location: City name or zip code to look up weather for.

    Returns:
        A string describing the current weather conditions.
    """
    import os
    import json

    api_key = os.getenv("WEATHER_API_KEY")

    return json.dumps({
        "location": location,
        "temperature": "72F",
        "conditions": "sunny",
        "note": "This is mock data."
    })
`;

// Register the tool
const tool = await client.tools.create({ sourceCode: toolSource });
console.log(`Created tool: ${tool.name} (id: ${tool.id})`);

// Create agent with the tool
const agent = await client.agents.create({
  name: "weather_agent_ts_example",
  model: "openai/gpt-4o-mini",
  memory_blocks: [
    { label: "persona", value: "I am a weather assistant." },
    { label: "human", value: "The user wants weather information." },
  ],
  tool_ids: [tool.id],
});

console.log(`Created agent: ${agent.id}`);

// Use the tool
const response = await client.agents.messages.create(agent.id, {
  messages: [{ role: "user", content: "What's the weather in NYC?" }],
});

for (const msg of response.messages) {
  if (msg.message_type === "tool_call_message") {
    console.log(`Tool call: ${msg.tool_calls[0].name}`);
  }
  if (msg.message_type === "assistant_message") {
    console.log(`Assistant: ${msg.content}`);
  }
}

// Cleanup
await client.agents.delete(agent.id);
await client.tools.delete(tool.id);
