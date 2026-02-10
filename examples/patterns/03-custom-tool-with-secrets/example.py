"""Complete custom tool workflow: creation, secrets, attachment, and usage.

Shows the full lifecycle of building a tool that needs API keys,
attaching it to an agent, and having the agent use it.
"""

import os
from letta_client import Letta

client = Letta(api_key=os.getenv("LETTA_API_KEY"))

# --- Step 1: Define the tool (Python source code as string) ---

tool_source = '''
def search_database(query: str, max_results: int = 5) -> str:
    """Search our internal database for relevant records.

    Args:
        query: The search query string.
        max_results: Maximum number of results to return (default 5).

    Returns:
        JSON string of matching records.
    """
    import os
    import json

    # Access secrets via environment variables (set at agent level)
    db_api_key = os.getenv("DB_API_KEY")

    # In production, this would call your actual API
    # For this example, return mock data
    results = [
        {"id": 1, "title": f"Result for '{query}'", "relevance": 0.95},
        {"id": 2, "title": f"Another match for '{query}'", "relevance": 0.87},
    ]

    return json.dumps({"query": query, "results": results[:max_results]})
'''

# --- Step 2: Create the tool ---

tool = client.tools.create(source_code=tool_source)
print(f"Created tool: {tool.name} (id: {tool.id})")

# --- Step 3: Create agent with the tool ---

agent = client.agents.create(
    name="database_search_agent",
    model="openai/gpt-4o-mini",
    memory_blocks=[
        {
            "label": "persona",
            "value": "I am a database assistant. I can search our internal database using the search_database tool.",
        },
        {
            "label": "human",
            "value": "A user who needs to find records in the database.",
        },
    ],
    tool_ids=[tool.id],
    # Set secrets that the tool can access via os.getenv()
    tool_exec_environment_variables={"DB_API_KEY": "mock-secret-key-12345"},
)

print(f"Created agent: {agent.id}")

# --- Step 4: Use the tool ---

response = client.agents.messages.create(
    agent_id=agent.id,
    messages=[{"role": "user", "content": "Search for records about memory blocks"}],
)

for msg in response.messages:
    if msg.message_type == "tool_call_message":
        print(f"\nTool call: {msg.tool_call.name}({msg.tool_call.arguments})")
    if msg.message_type == "tool_return_message":
        print(f"Tool returned: {msg.tool_return[:100]}...")
    if msg.message_type == "assistant_message":
        print(f"\nAssistant: {msg.content}")

# --- Cleanup ---

client.agents.delete(agent.id)
client.tools.delete(tool.id)
