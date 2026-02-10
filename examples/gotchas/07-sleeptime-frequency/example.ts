/**
 * Correct way to update sleeptime agent frequency (TypeScript).
 *
 * Frequency must be nested inside manager_config.
 */

import Letta from "@letta-ai/letta-client";

const client = new Letta({ apiKey: process.env.LETTA_API_KEY });

const agent = await client.agents.create({
  name: "sleeptime_freq_ts_example",
  model: "openai/gpt-4o-mini",
  memory_blocks: [
    { label: "persona", value: "Assistant with background processing." },
    { label: "human", value: "Testing sleeptime." },
  ],
  enable_sleeptime: true,
});

const groupId = agent.multi_agent_group.id;

// WRONG: top-level (silently ignored)
// await client.groups.update(groupId, { sleeptime_agent_frequency: 25 });

// RIGHT: nested in manager_config
await client.groups.update(groupId, {
  manager_config: {
    manager_type: "sleeptime",
    sleeptime_agent_frequency: 25,
  },
});

console.log("Updated sleeptime frequency to 25");

await client.agents.delete(agent.id);
