"""Test: Sleeptime agent pattern."""


def test_sleeptime_agent_has_group(client, cleanup_agents):
    """Verify sleeptime agent creates a multi-agent group."""
    agent = client.agents.create(
        name="test_sleeptime_pattern",
        model="openai/gpt-4o-mini",
        memory_blocks=[
            {"label": "persona", "value": "Test."},
            {"label": "human", "value": "Test."},
        ],
        enable_sleeptime=True,
    )
    cleanup_agents.append(agent.id)

    assert agent.multi_agent_group is not None
    assert agent.multi_agent_group.id.startswith("group-")


def test_sleeptime_responds_normally(client, cleanup_agents):
    """Verify sleeptime agents process messages (may use tools or respond directly)."""
    agent = client.agents.create(
        name="test_sleeptime_responds",
        model="openai/gpt-4o-mini",
        memory_blocks=[
            {"label": "persona", "value": "Be brief."},
            {"label": "human", "value": "Test."},
        ],
        enable_sleeptime=True,
    )
    cleanup_agents.append(agent.id)

    response = client.agents.messages.create(
        agent_id=agent.id,
        messages=[{"role": "user", "content": "Say hi."}],
        streaming=False,
    )

    # Sleeptime agent may respond with assistant message OR use memory tools first
    assert response.messages, "Sleeptime agent should produce some messages"
