"""Test: Update method exists, modify does not."""

import pytest


def test_update_exists(client, cleanup_agents):
    """Verify .update() works for agents."""
    agent = client.agents.create(
        name="test_update_method",
        model="openai/gpt-4o-mini",
        memory_blocks=[
            {"label": "persona", "value": "Test."},
            {"label": "human", "value": "Test."},
        ],
    )
    cleanup_agents.append(agent.id)

    updated = client.agents.update(agent.id, name="test_update_renamed")
    assert updated.name == "test_update_renamed"


def test_modify_does_not_exist(client):
    """Verify .modify() raises AttributeError."""
    assert not hasattr(client.agents, "modify"), ".modify() should not exist in SDK 1.0+"
