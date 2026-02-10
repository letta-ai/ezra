"""Shared fixtures for Letta example tests."""

import os

import pytest
from letta_client import Letta


@pytest.fixture
def client():
    """Create a Letta client from environment."""
    api_key = os.getenv("LETTA_API_KEY")
    if not api_key:
        pytest.skip("LETTA_API_KEY not set")
    return Letta(api_key=api_key)


@pytest.fixture
def cleanup_agents(client):
    """Track agents created during tests and clean them up after."""
    created = []
    yield created
    for agent_id in created:
        try:
            client.agents.delete(agent_id)
        except Exception:
            pass


@pytest.fixture
def cleanup_tools(client):
    """Track tools created during tests and clean them up after."""
    created = []
    yield created
    for tool_id in created:
        try:
            client.tools.delete(tool_id)
        except Exception:
            pass


@pytest.fixture
def cleanup_blocks(client):
    """Track standalone blocks created during tests and clean them up after."""
    created = []
    yield created
    for block_id in created:
        try:
            client.blocks.delete(block_id)
        except Exception:
            pass
