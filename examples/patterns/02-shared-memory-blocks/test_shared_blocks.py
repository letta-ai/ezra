"""Test: Shared memory blocks pattern."""


def test_shared_block_same_id(client, cleanup_agents, cleanup_blocks):
    """Verify two agents share the exact same block."""
    # Create shared block
    block = client.blocks.create(label="test_shared", value="original")
    cleanup_blocks.append(block.id)

    # Create two agents
    agent_a = client.agents.create(
        name="test_shared_a",
        model="openai/gpt-4o-mini",
        memory_blocks=[
            {"label": "persona", "value": "A."},
            {"label": "human", "value": "Test."},
        ],
    )
    cleanup_agents.append(agent_a.id)

    agent_b = client.agents.create(
        name="test_shared_b",
        model="openai/gpt-4o-mini",
        memory_blocks=[
            {"label": "persona", "value": "B."},
            {"label": "human", "value": "Test."},
        ],
    )
    cleanup_agents.append(agent_b.id)

    # Attach shared block to both
    # Signature: attach(block_id, *, agent_id=...)
    client.agents.blocks.attach(block.id, agent_id=agent_a.id)
    client.agents.blocks.attach(block.id, agent_id=agent_b.id)

    # Verify same block ID
    blocks_a = client.agents.blocks.list(agent_a.id)
    blocks_b = client.agents.blocks.list(agent_b.id)

    shared_a = [b for b in blocks_a if b.label == "test_shared"]
    shared_b = [b for b in blocks_b if b.label == "test_shared"]

    assert shared_a and shared_b, "Both should have the shared block"
    assert shared_a[0].id == shared_b[0].id, "Should be the same block object"

    # Update and verify propagation
    client.blocks.update(block.id, value="updated")
    blocks_a_new = client.agents.blocks.list(agent_a.id)
    shared_a_new = [b for b in blocks_a_new if b.label == "test_shared"]
    assert shared_a_new[0].value == "updated"

    # Cleanup: detach before agent deletion
    client.agents.blocks.detach(block.id, agent_id=agent_a.id)
    client.agents.blocks.detach(block.id, agent_id=agent_b.id)
