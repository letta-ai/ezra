"""Test: Sleeptime frequency configuration."""


def test_sleeptime_agent_creation(client, cleanup_agents):
    """Verify sleeptime agents have a multi_agent_group with an ID."""
    agent = client.agents.create(
        name="test_sleeptime_freq",
        model="openai/gpt-4o-mini",
        memory_blocks=[
            {"label": "persona", "value": "Test."},
            {"label": "human", "value": "Test."},
        ],
        enable_sleeptime=True,
    )
    cleanup_agents.append(agent.id)

    assert agent.multi_agent_group is not None, "Sleeptime agent should have multi_agent_group"
    assert agent.multi_agent_group.id is not None, "Group should have an ID"
