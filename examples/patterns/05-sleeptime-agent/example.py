"""Sleeptime agent: Background memory processing.

Sleeptime agents have a background process that periodically reviews
conversations and updates memory blocks. This enables agents to
reflect on interactions and consolidate knowledge.
"""

import os
from letta_client import Letta

client = Letta(api_key=os.getenv("LETTA_API_KEY"))

# --- Create a sleeptime agent ---

agent = client.agents.create(
    name="sleeptime_example",
    model="openai/gpt-4o-mini",
    memory_blocks=[
        {
            "label": "persona",
            "value": "I am an assistant that learns from conversations over time.",
        },
        {
            "label": "human",
            "value": "Unknown user. I should learn about them through our conversations.",
        },
    ],
    enable_sleeptime=True,  # Enable background processing
)

print(f"Created sleeptime agent: {agent.id}")
print(f"Group ID: {agent.multi_agent_group.id}")

# --- Configure sleeptime frequency ---
# Frequency = how many messages before sleeptime agent runs
# MUST be nested inside manager_config

group_id = agent.multi_agent_group.id

client.groups.update(
    group_id,
    manager_config={
        "manager_type": "sleeptime",
        "sleeptime_agent_frequency": 5,  # Run after every 5 messages
    },
)

print("Set sleeptime frequency to 5 messages")

# --- Send some messages ---

messages = [
    "Hi, I'm Cameron and I work on AI agents.",
    "I mainly use Python and TypeScript.",
    "My biggest challenge is managing agent memory effectively.",
]

for text in messages:
    response = client.agents.messages.create(
        agent_id=agent.id,
        messages=[{"role": "user", "content": text}],
    )
    for msg in response.messages:
        if msg.message_type == "assistant_message":
            print(f"\nUser: {text}")
            print(f"Agent: {msg.content[:100]}...")

# --- Check memory blocks for sleeptime updates ---
# Sleeptime processes conversations and may update blocks

blocks = client.agents.blocks.list(agent.id)
print("\n=== Current Memory ===")
for block in blocks:
    print(f"\n{block.label}:")
    print(f"  {block.value[:200]}")

# --- Key points ---
# 1. Sleeptime triggers based on TOTAL messages across ALL conversations
# 2. Both interval_seconds AND min_messages must be met
# 3. Sleeptime agent sees transcripts but doesn't re-execute tools
# 4. Updates are visible to all conversations on next context compilation

# --- Cleanup ---

client.agents.delete(agent.id)
