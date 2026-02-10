"""Test: Streaming responses pattern."""


def test_streaming_returns_chunks(client, cleanup_agents):
    """Verify streaming produces message chunks."""
    agent = client.agents.create(
        name="test_streaming",
        model="openai/gpt-4o-mini",
        memory_blocks=[
            {"label": "persona", "value": "Be brief."},
            {"label": "human", "value": "Test."},
        ],
    )
    cleanup_agents.append(agent.id)

    # Use .stream() method (not create_stream)
    stream = client.agents.messages.stream(
        agent_id=agent.id,
        messages=[{"role": "user", "content": "Say hello in one word."}],
    )

    chunks = list(stream)
    assert len(chunks) > 0, "Should receive at least one chunk"
