/**
 * Correct message roles when sending messages to agents (TypeScript).
 *
 * Only user, system, and assistant roles are allowed.
 */

import Letta from "@letta-ai/letta-client";

const client = new Letta({ apiKey: process.env.LETTA_API_KEY });

const agent = await client.agents.create({
  name: "message_roles_ts_example",
  model: "openai/gpt-4o-mini",
  memory_blocks: [
    { label: "persona", value: "I am a helpful assistant." },
    { label: "human", value: "A user testing message roles." },
  ],
});

// Simple user message
const response = await client.agents.messages.create(agent.id, {
  input: "Hello!",
});

for (const msg of response.messages) {
  if (msg.message_type === "assistant_message") {
    console.log(`Assistant: ${msg.content}`);
  }
}

// Multiple messages with roles
const response2 = await client.agents.messages.create(agent.id, {
  messages: [
    { role: "system", content: "The user prefers short answers." },
    { role: "user", content: "What is 2+2?" },
  ],
});

for (const msg of response2.messages) {
  if (msg.message_type === "assistant_message") {
    console.log(`Assistant: ${msg.content}`);
  }
}

// WRONG: role: "tool" will fail with 422
// messages: [{ role: "tool", content: "result data" }]

await client.agents.delete(agent.id);
