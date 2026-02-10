"""Multi-user conversations: Multiple users chatting with one agent in parallel.

Uses the Conversations API to create isolated sessions that share
the same agent memory. Each user gets their own conversation_id.
"""

import os
from letta_client import Letta

client = Letta(api_key=os.getenv("LETTA_API_KEY"))

# --- Create a shared agent ---

agent = client.agents.create(
    name="shared_support_agent",
    model="openai/gpt-4o-mini",
    memory_blocks=[
        {
            "label": "persona",
            "value": "I am a support agent. I help users with their questions.",
        },
        {
            "label": "human",
            "value": "Multiple users may contact me through different conversations.",
        },
    ],
)
print(f"Created shared agent: {agent.id}")

# --- Create separate conversations for each user ---

conv_alice = client.conversations.create(agent_id=agent.id)
conv_bob = client.conversations.create(agent_id=agent.id)

print(f"Alice's conversation: {conv_alice.id}")
print(f"Bob's conversation: {conv_bob.id}")

# --- Users chat in parallel (different conversations) ---

# Alice sends a message
# conversations.messages.create returns a Stream
alice_stream = client.conversations.messages.create(
    conv_alice.id,
    messages=[{"role": "user", "content": "Hi, I'm Alice. I need help with memory blocks."}],
)

# Consume the stream to get all chunks
for chunk in alice_stream:
    if hasattr(chunk, "message_type") and chunk.message_type == "assistant_message":
        print(f"\nAlice got: {str(chunk.content)[:100]}...")

# Bob sends a message (different conversation - no blocking)
bob_stream = client.conversations.messages.create(
    conv_bob.id,
    messages=[{"role": "user", "content": "Hey, I'm Bob. How do custom tools work?"}],
)

for chunk in bob_stream:
    if hasattr(chunk, "message_type") and chunk.message_type == "assistant_message":
        print(f"\nBob got: {str(chunk.content)[:100]}...")

# --- Key points ---
# 1. Both users share the same agent (same memory blocks)
# 2. Conversations are isolated (Alice can't see Bob's messages)
# 3. True parallelism - no blocking between conversations
# 4. Only blocking within a single conversation (can't double-send)

# --- Cleanup ---

client.agents.delete(agent.id)
