"""Test: Message roles."""


def test_user_message(client, cleanup_agents):
    """Verify user messages work."""
    agent = client.agents.create(
        name="test_msg_roles",
        model="openai/gpt-4o-mini",
        memory_blocks=[
            {"label": "persona", "value": "Test."},
            {"label": "human", "value": "Test."},
        ],
    )
    cleanup_agents.append(agent.id)

    response = client.agents.messages.create(agent_id=agent.id, input="Hi")
    assert response.messages, "Should get messages back"

    assistant_msgs = [m for m in response.messages if m.message_type == "assistant_message"]
    assert assistant_msgs, "Should have assistant response"
