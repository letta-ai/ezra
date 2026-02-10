"""Use .update() not .modify() for agent modifications.

SDK 1.0 renamed .modify() to .update() across all resources.
"""

import os
from letta_client import Letta

client = Letta(api_key=os.getenv("LETTA_API_KEY"))

agent = client.agents.create(
    name="update_example_agent",
    model="openai/gpt-4o-mini",
    memory_blocks=[
        {"label": "persona", "value": "I am a test agent."},
        {"label": "human", "value": "Test user."},
    ],
)

print(f"Original name: {agent.name}")

# --- WRONG ---
# client.agents.modify(agent.id, name="new_name")
# -> AttributeError: 'Agents' object has no attribute 'modify'

# --- RIGHT ---
updated = client.agents.update(agent.id, name="updated_example_agent")
print(f"Updated name: {updated.name}")

# Also applies to blocks:
blocks = client.agents.blocks.list(agent.id)
block = blocks[0]  # First block
updated_block = client.agents.blocks.update(
    agent_id=agent.id,
    block_label=block.label,
    value="Updated value!",
)
print(f"Updated block '{updated_block.label}': {updated_block.value}")

# --- Cleanup ---

client.agents.delete(agent.id)
