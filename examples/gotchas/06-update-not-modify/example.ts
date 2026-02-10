/**
 * Use .update() not .modify() for agent modifications (TypeScript).
 */

import Letta from "@letta-ai/letta-client";

const client = new Letta({ apiKey: process.env.LETTA_API_KEY });

const agent = await client.agents.create({
  name: "update_ts_example",
  model: "openai/gpt-4o-mini",
  memory_blocks: [
    { label: "persona", value: "Test agent." },
    { label: "human", value: "Test user." },
  ],
});

console.log(`Original: ${agent.name}`);

// WRONG: client.agents.modify(...)
// RIGHT:
const updated = await client.agents.update(agent.id, { name: "updated_ts_example" });
console.log(`Updated: ${updated.name}`);

await client.agents.delete(agent.id);
