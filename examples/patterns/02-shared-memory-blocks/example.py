"""Shared memory blocks: Multiple agents reading/writing the same block.

Create a block independently, attach to multiple agents. When one agent
writes, others see the update on their next context compilation.
"""

import os
from letta_client import Letta

client = Letta(api_key=os.getenv("LETTA_API_KEY"))

# --- Create a shared block ---

shared_block = client.blocks.create(
    label="shared_knowledge",
    value="Company policy: All responses must be under 100 words.",
)
print(f"Created shared block: {shared_block.id}")

# --- Create two agents ---

agent_a = client.agents.create(
    name="agent_a_shared_blocks",
    model="openai/gpt-4o-mini",
    memory_blocks=[
        {"label": "persona", "value": "I am Agent A, a customer support agent."},
        {"label": "human", "value": "User interacting with Agent A."},
    ],
)

agent_b = client.agents.create(
    name="agent_b_shared_blocks",
    model="openai/gpt-4o-mini",
    memory_blocks=[
        {"label": "persona", "value": "I am Agent B, a technical support agent."},
        {"label": "human", "value": "User interacting with Agent B."},
    ],
)

print(f"Agent A: {agent_a.id}")
print(f"Agent B: {agent_b.id}")

# --- Attach the shared block to both agents ---

client.agents.blocks.attach(shared_block.id, agent_id=agent_a.id)
client.agents.blocks.attach(shared_block.id, agent_id=agent_b.id)

print("Attached shared_knowledge block to both agents")

# --- Verify both see the same content ---

blocks_a = client.agents.blocks.list(agent_a.id)
blocks_b = client.agents.blocks.list(agent_b.id)

for block in blocks_a:
    if block.label == "shared_knowledge":
        print(f"\nAgent A sees: {block.value}")

for block in blocks_b:
    if block.label == "shared_knowledge":
        print(f"Agent B sees: {block.value}")

# --- Update the shared block ---

client.blocks.update(
    shared_block.id,
    value="Company policy: All responses must be under 50 words. Updated Feb 2026.",
)

# Both agents now see the updated value on next context compilation
blocks_a_updated = client.agents.blocks.list(agent_a.id)
for block in blocks_a_updated:
    if block.label == "shared_knowledge":
        print(f"\nAfter update, Agent A sees: {block.value}")

# --- Cleanup ---

# Detach before deleting agents
client.agents.blocks.detach(shared_block.id, agent_id=agent_a.id)
client.agents.blocks.detach(shared_block.id, agent_id=agent_b.id)
client.agents.delete(agent_a.id)
client.agents.delete(agent_b.id)
client.blocks.delete(shared_block.id)
