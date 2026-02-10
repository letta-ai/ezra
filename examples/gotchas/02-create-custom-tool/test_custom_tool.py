"""Test: Custom tool creation and usage."""


def test_create_tool_from_source(client, cleanup_tools, cleanup_agents):
    """Verify a tool can be created from source code and attached to an agent."""

    source = '''
def lookup_weather(location: str) -> str:
    """Get weather for a location.

    Args:
        location: City name or zip code.
    """
    import json
    return json.dumps({"location": location, "temp": "72F"})
'''

    tool = client.tools.create(source_code=source)
    cleanup_tools.append(tool.id)

    assert tool.name == "lookup_weather"
    assert tool.id.startswith("tool-")
    assert "location" in str(tool.json_schema)

    # Attach to agent
    agent = client.agents.create(
        name="test_tool_example",
        model="openai/gpt-4o-mini",
        memory_blocks=[
            {"label": "persona", "value": "Test agent."},
            {"label": "human", "value": "Test user."},
        ],
        tool_ids=[tool.id],
    )
    cleanup_agents.append(agent.id)

    # Verify tool is attached
    agent_tools = client.agents.tools.list(agent.id)
    tool_names = [t.name for t in agent_tools]
    assert "lookup_weather" in tool_names
