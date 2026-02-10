"""Test: Custom tool with secrets pattern."""


def test_tool_with_env_vars(client, cleanup_agents, cleanup_tools):
    """Verify tool creation and agent attachment with env vars."""
    source = '''
def mock_search(query: str) -> str:
    """Search for records.

    Args:
        query: The search term.
    """
    import os
    import json
    api_key = os.getenv("TEST_API_KEY")
    return json.dumps({"query": query, "has_key": api_key is not None})
'''

    tool = client.tools.create(source_code=source)
    cleanup_tools.append(tool.id)

    agent = client.agents.create(
        name="test_tool_secrets",
        model="openai/gpt-4o-mini",
        memory_blocks=[
            {"label": "persona", "value": "Search assistant."},
            {"label": "human", "value": "Test user."},
        ],
        tool_ids=[tool.id],
        tool_exec_environment_variables={"TEST_API_KEY": "test-key"},
    )
    cleanup_agents.append(agent.id)

    # Verify tool is attached
    agent_tools = client.agents.tools.list(agent.id)
    tool_names = [t.name for t in agent_tools]
    assert "mock_search" in tool_names
