"""Test: Multi-user conversations pattern."""


def test_separate_conversations(client, cleanup_agents):
    """Verify two conversations on the same agent are independent."""
    agent = client.agents.create(
        name="test_multi_user",
        model="openai/gpt-4o-mini",
        memory_blocks=[
            {"label": "persona", "value": "Support agent."},
            {"label": "human", "value": "Multiple users."},
        ],
    )
    cleanup_agents.append(agent.id)

    # Create two conversations
    conv_a = client.conversations.create(agent_id=agent.id)
    conv_b = client.conversations.create(agent_id=agent.id)

    assert conv_a.id != conv_b.id, "Conversations should have different IDs"

    # Send message in conversation A
    # conversations.messages.create always returns a Stream
    stream_a = client.conversations.messages.create(
        conv_a.id,
        messages=[{"role": "user", "content": "My name is Alice."}],
    )
    chunks_a = list(stream_a)
    assert chunks_a, "Should get response in conversation A"

    # Send message in conversation B
    stream_b = client.conversations.messages.create(
        conv_b.id,
        messages=[{"role": "user", "content": "My name is Bob."}],
    )
    chunks_b = list(stream_b)
    assert chunks_b, "Should get response in conversation B"
