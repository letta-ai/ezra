"""Streaming responses from Letta agents.

Shows how to use SSE streaming for real-time token delivery,
including the include_pings parameter for Cloudflare timeout prevention.
"""

import os
from letta_client import Letta

client = Letta(api_key=os.getenv("LETTA_API_KEY"))

agent = client.agents.create(
    name="streaming_example",
    model="openai/gpt-4o-mini",
    memory_blocks=[
        {"label": "persona", "value": "I am an assistant that gives detailed explanations."},
        {"label": "human", "value": "A user testing streaming."},
    ],
)

# --- Basic streaming ---

print("=== Streaming response ===")
stream = client.agents.messages.stream(
    agent_id=agent.id,
    messages=[{"role": "user", "content": "Explain how memory works in Letta in 2-3 sentences."}],
)

for chunk in stream:
    # Each chunk is a message event
    if hasattr(chunk, "message_type"):
        if chunk.message_type == "assistant_message":
            # Token-level streaming
            print(chunk.content, end="", flush=True)

print()  # newline after streaming

# --- With keepalive pings (for long-running requests) ---
# Prevents Cloudflare 524 timeout on requests > 2 minutes

print("\n=== With keepalive pings ===")
stream = client.agents.messages.stream(
    agent_id=agent.id,
    messages=[{"role": "user", "content": "What is 2+2? Be brief."}],
    include_pings=True,  # Sends pings every 30s to keep connection alive
)

for chunk in stream:
    if hasattr(chunk, "message_type"):
        if chunk.message_type == "assistant_message":
            print(chunk.content, end="", flush=True)
    # Ping events are silently handled - no action needed

print()

# --- Cleanup ---

client.agents.delete(agent.id)
