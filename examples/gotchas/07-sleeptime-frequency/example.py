"""Correct way to update sleeptime agent frequency.

The frequency must be nested inside manager_config - a top-level
parameter is silently ignored.
"""

import os
from letta_client import Letta

client = Letta(api_key=os.getenv("LETTA_API_KEY"))

# Create a sleeptime agent
agent = client.agents.create(
    name="sleeptime_freq_example",
    model="openai/gpt-4o-mini",
    memory_blocks=[
        {"label": "persona", "value": "I am an assistant with background processing."},
        {"label": "human", "value": "A user testing sleeptime."},
    ],
    enable_sleeptime=True,
)

print(f"Created sleeptime agent: {agent.id}")

# Get the sleeptime group ID
group_id = agent.multi_agent_group.id
print(f"Group ID: {group_id}")

# --- WRONG: Top-level field (silently ignored) ---
# client.groups.update(group_id, sleeptime_agent_frequency=25)

# --- RIGHT: Nested inside manager_config ---
client.groups.update(
    group_id,
    manager_config={
        "manager_type": "sleeptime",
        "sleeptime_agent_frequency": 25,
    },
)

print("Updated sleeptime frequency to 25 messages")

# --- Cleanup ---

client.agents.delete(agent.id)
