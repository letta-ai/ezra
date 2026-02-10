"""Correct message roles when sending messages to agents.

Only user, system, and assistant roles are allowed.
Tool messages are auto-generated during execution - you can't send them.
"""

import os
from letta_client import Letta

client = Letta(api_key=os.getenv("LETTA_API_KEY"))

agent = client.agents.create(
    name="message_roles_example",
    model="openai/gpt-4o-mini",
    memory_blocks=[
        {"label": "persona", "value": "I am a helpful assistant."},
        {"label": "human", "value": "A user testing message roles."},
    ],
)

# --- Correct: Simple user message ---

response = client.agents.messages.create(
    agent_id=agent.id,
    input="Hello!",  # Shorthand for a single user message
)

for msg in response.messages:
    if msg.message_type == "assistant_message":
        print(f"Assistant: {msg.content}")

# --- Correct: Multiple messages with roles ---

response = client.agents.messages.create(
    agent_id=agent.id,
    messages=[
        {"role": "system", "content": "The user prefers short answers."},
        {"role": "user", "content": "What is 2+2?"},
    ],
)

for msg in response.messages:
    if msg.message_type == "assistant_message":
        print(f"Assistant: {msg.content}")

# --- WRONG: role='tool' will fail with 422 ---

# client.agents.messages.create(
#     agent_id=agent.id,
#     messages=[{"role": "tool", "content": "result data"}],
# )
# -> 422 Unprocessable Entity

# --- Cleanup ---

client.agents.delete(agent.id)
