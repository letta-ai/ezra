"""Test: Multi-agent coordination pattern."""


def test_shared_block_coordination(client, cleanup_agents, cleanup_blocks):
    """Verify two agents can coordinate through a shared block."""
    # Create shared block
    shared = client.blocks.create(label="coordination_test", value="Status: pending")
    cleanup_blocks.append(shared.id)

    # Create two agents
    agent_a = client.agents.create(
        name="test_coord_a",
        model="openai/gpt-4o-mini",
        memory_blocks=[
            {"label": "persona", "value": "Agent A."},
            {"label": "human", "value": "Test."},
        ],
    )
    cleanup_agents.append(agent_a.id)

    agent_b = client.agents.create(
        name="test_coord_b",
        model="openai/gpt-4o-mini",
        memory_blocks=[
            {"label": "persona", "value": "Agent B."},
            {"label": "human", "value": "Test."},
        ],
    )
    cleanup_agents.append(agent_b.id)

    # Attach shared block (block_id first, agent_id as keyword)
    client.agents.blocks.attach(shared.id, agent_id=agent_a.id)
    client.agents.blocks.attach(shared.id, agent_id=agent_b.id)

    # Update shared block (simulating agent A writing)
    client.blocks.update(shared.id, value="Status: research complete")

    # Verify agent B can see the update
    blocks_b = client.agents.blocks.list(agent_b.id)
    coord_block = [b for b in blocks_b if b.label == "coordination_test"]
    assert coord_block, "Agent B should have the shared block"
    assert "research complete" in coord_block[0].value

    # Cleanup
    client.agents.blocks.detach(shared.id, agent_id=agent_a.id)
    client.agents.blocks.detach(shared.id, agent_id=agent_b.id)
