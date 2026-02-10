"""Correct way to create custom tools for Letta agents.

Key rules:
1. ALL imports must be INSIDE the function (sandbox requirement)
2. Use os.getenv() for secrets, not function arguments
3. Type hints + docstring = automatic JSON schema generation
"""

import os
from letta_client import Letta

client = Letta(api_key=os.getenv("LETTA_API_KEY"))


# --- Define the tool function ---

def lookup_weather(location: str) -> str:
    """Get the current weather for a location.

    Args:
        location: City name or zip code to look up weather for.

    Returns:
        A string describing the current weather conditions.
    """
    # IMPORTANT: Imports must be INSIDE the function.
    # The sandbox doesn't have access to your global imports.
    import os
    import json

    # IMPORTANT: Use os.getenv() for secrets.
    # Configure secrets via agent-level environment variables, not function args.
    api_key = os.getenv("WEATHER_API_KEY")

    # For this example, return mock data
    return json.dumps({
        "location": location,
        "temperature": "72F",
        "conditions": "sunny",
        "note": "This is mock data. Replace with real API call."
    })


# --- Register the tool ---

tool = client.tools.create(source_code=lookup_weather)
print(f"Created tool: {tool.name} (id: {tool.id})")
print(f"Schema: {tool.json_schema}")

# --- Attach to an agent ---

agent = client.agents.create(
    name="weather_agent_example",
    model="openai/gpt-4o-mini",
    memory_blocks=[
        {"label": "persona", "value": "I am a weather assistant."},
        {"label": "human", "value": "The user wants weather information."},
    ],
    tool_ids=[tool.id],
)

print(f"Created agent: {agent.id} with tool {tool.name}")

# --- Use the tool ---

response = client.agents.messages.create(
    agent_id=agent.id,
    messages=[{"role": "user", "content": "What's the weather in San Francisco?"}],
)

for msg in response.messages:
    if msg.message_type == "tool_call_message":
        print(f"Tool call: {msg.tool_call.name}({msg.tool_call.arguments})")
    if msg.message_type == "assistant_message":
        print(f"Assistant: {msg.content}")

# --- Cleanup ---

client.agents.delete(agent.id)
client.tools.delete(tool.id)
